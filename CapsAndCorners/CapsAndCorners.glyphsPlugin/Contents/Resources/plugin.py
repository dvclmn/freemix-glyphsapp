from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import (
    Glyphs,
    WINDOW_MENU,
)
from GlyphsApp.plugins import GeneralPlugin
from window import setUpWindow

from Cocoa import (
    NSMenuItem,
    NSImageNameLockLockedTemplate,
    NSImageNameLockUnlockedTemplate,
)
from constants import *
from updateDoc import documentUpdated
from updateMain import mainUpdater
import traceback


class CapsAndCorners(GeneralPlugin):

    @objc.python_method
    def settings(self):
        self.name = "Caps and Corners"

    @objc.python_method
    def start(self):
        newMenuItem = NSMenuItem.new()
        newMenuItem.setTitle_(self.name)
        newMenuItem.setAction_(self.showWindow_)
        newMenuItem.setTarget_(self)
        Glyphs.menu[WINDOW_MENU].append(newMenuItem)

    def showWindow_(self, sender):
        setUpWindow(self, sender)

    @objc.python_method
    def updateDocument(self, sender):
        documentUpdated(self, sender)

    @objc.python_method
    def updateLockButtonImage(self, lockButton, i):
        if self.isLocked[i]:
            lockButton.setImage(imageNamed=NSImageNameLockLockedTemplate)
        else:
            lockButton.setImage(imageNamed=NSImageNameLockUnlockedTemplate)

    @objc.python_method
    def update(self, sender):
        mainUpdater(self, sender)

    @objc.python_method
    def updateHint(self, cname, ctype, dimension, newValue):
        self.font.disableUpdateInterface()
        for layer in self.font.selectedLayers:
            undoHasBegun = False
            for hint in layer.hints:
                if hint.type == ctype and hint.name == cname:
                    scale = hint.pyobjc_instanceMethods.scale()
                    if dimension == "widt":
                        if abs(scale.x - newValue) < 0.00001:
                            # no change. let’s skip this hint in order to avoid “empty” undo steps
                            continue
                        if scale.x > 0:
                            scale.x = newValue
                        else:
                            scale.x = -newValue
                    else:
                        if abs(scale.y - newValue) < 0.00001:
                            continue
                        if scale.y > 0:
                            scale.y = newValue
                        else:
                            scale.y = -newValue
                    if not undoHasBegun:
                        layer.parent.beginUndo()
                        undoHasBegun = True
                    hint.setScale_(scale)
            if undoHasBegun:
                layer.parent.endUndo()
        self.font.enableUpdateInterface()
        Glyphs.redraw()

    @objc.python_method
    def editTextCallback(self, editText):
        try:
            i = 0
            for cname, ctype in self.cc:
                for dimension in ["widt", "dept"]:
                    if editText == getattr(self.w, dimension + str(i)):
                        try:
                            newValue = 0.01 * float(editText.get().strip("%"))
                        except:
                            return
                        if self.isLocked[i]:
                            self.updateHint(cname, ctype, "widt", newValue)
                            self.updateHint(cname, ctype, "dept", newValue)
                        else:
                            self.updateHint(cname, ctype, dimension, newValue)
                        return
                i += 1
                if i == NUMBER_OF_FIELDS:
                    break
        except AttributeError:
            pass

    @objc.python_method
    def fitCallback(self, fitBox):
        try:
            i = 0
            for cname, ctype in self.cc:
                if fitBox == getattr(self.w, "fit_" + str(i)):
                    for layer in self.font.selectedLayers:
                        for hint in layer.hints:
                            if hint.type == ctype and hint.name == cname:
                                hint.options = hint.options ^ 8
                    return
                i += 1
                if i == NUMBER_OF_FIELDS:
                    break
        except AttributeError:
            pass

    @objc.python_method
    def lockWidthDepthCallback(self, lockButton):
        try:
            i = 0
            for cname, ctype in self.cc:
                if lockButton == getattr(self.w, "lock" + str(i)):
                    self.isLocked[i] = not self.isLocked[i]
                    lockButton = getattr(self.w, "lock" + str(i))
                    self.updateLockButtonImage(lockButton, i)
                    if self.isLocked[i]:
                        cname, ctype = self.cc[i]
                        details = self.details[cname]
                        if details["widt"] != details["dept"]:
                            details["widt"] = (details["widt"] + details["dept"]) / 2
                            details["dept"] = details["widt"]
                            self.updateHint(cname, ctype, "widt", details["widt"])
                            self.updateHint(cname, ctype, "dept", details["widt"])
                    return
                i += 1
                if i == NUMBER_OF_FIELDS:
                    break
        except AttributeError:
            pass

    @objc.python_method
    def __del__(self):
        Glyphs.removeCallback(self.update)
        Glyphs.removeCallback(self.updateDocument)

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

    def windowClose_(self, window):
        try:
            Glyphs.removeCallback(self.update)
            Glyphs.removeCallback(self.updateDocument)
            return True
        except:
            print(traceback.format_exc())
