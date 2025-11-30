from constants import *
from GlyphsApp import Glyphs, CAP
import traceback


def mainUpdater(plugin, sender):
    try:
        currentDocument = Glyphs.currentDocument
        if not currentDocument or not plugin.font or not plugin.font.selectedLayers:
            return
        plugin.details = {}
        for layer in plugin.font.selectedLayers:

            for hint in layer.hints:
                if hint.isCorner:
                    scale = hint.pyobjc_instanceMethods.scale()
                    depth = abs(scale.y)
                    width = abs(scale.x)
                    isFit = hint.options & 8

                    if hint.name in plugin.details:
                        name = plugin.details[hint.name]
                        if name["widt"] != width:
                            name["widt"] = MULTIPLE_VALUES
                        if name["dept"] != depth:
                            name["dept"] = MULTIPLE_VALUES
                        if hint.type == CAP and name["fit"] != isFit:
                            name["fit"] = MULTIPLE_VALUES
                    else:
                        hintDetails = {
                            "type": hint.type,
                            "widt": width,
                            "dept": depth,
                        }
                        if hint.type == CAP:
                            hintDetails["fit"] = isFit
                        name = hintDetails
        i = 0
        for cname, ctype in plugin.cc:
            anyDetails = cname in plugin.details
            for dimension in ["widt", "dept"]:
                scaleField = getattr(plugin.w, dimension + str(i))
                if anyDetails:
                    if plugin.details[cname][dimension] == MULTIPLE_VALUES:
                        scaleField.set("")
                    else:
                        scaleField.set(
                            "{0:g}".format(plugin.details[cname][dimension] * 100.0)
                        )
                scaleField.show(anyDetails)
            lockButton = getattr(plugin.w, "lock" + str(i))
            if anyDetails:
                plugin.isLocked[i] = (
                    plugin.details[cname]["widt"] == plugin.details[cname]["dept"]
                )
                plugin.updateLockButtonImage(lockButton, i)
            lockButton.show(anyDetails)
            if ctype == CAP:
                fitBox = getattr(plugin.w, "fit_" + str(i))
                if anyDetails:
                    fitBox.set(plugin.details[cname]["fit"] != 0)
                    getattr(plugin.w, "widt" + str(i)).show(not fitBox.get())
                    # ^ for now, let’s hide this as Glyphs 3 does not report a sensible figure
                    getattr(plugin.w, "widt" + str(i)).enable(not fitBox.get())
                    getattr(plugin.w, "lock" + str(i)).show(not fitBox.get())
                fitBox.show(anyDetails)
            i += 1
            if i == NUMBER_OF_FIELDS:
                break
    except:
        print(traceback.format_exc())
