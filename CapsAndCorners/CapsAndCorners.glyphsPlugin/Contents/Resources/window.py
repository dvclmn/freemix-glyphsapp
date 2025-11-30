from GlyphsApp import (
    Glyphs,
    DOCUMENTACTIVATED,
    DOCUMENTWILLCLOSE,
    UPDATEINTERFACE,
)
from constants import *
import vanilla
from ArrowEdit import ArrowEditText
import traceback


def setUpWindow(plugin, sender):
    print("Hello ")
    try:
        plugin.margin = 13
        gutter = 6
        widthName = 128
        widthFitBox = 20
        widthDimensionBox = 58
        plugin.textFieldHeight = 23
        plugin.lineToLine = plugin.textFieldHeight + 5
        plugin.w = vanilla.HUDFloatingWindow(
            (100, 100), title=plugin.name, autosaveName="FMXCapsAndCorners"
        )
        posy = plugin.margin - 4
        posx = plugin.margin
        posx += widthName
        width = widthFitBox
        plugin.w.headerFit = vanilla.TextBox(
            (posx, posy, width, plugin.textFieldHeight), text="fit"
        )
        posx += width
        width = widthDimensionBox
        plugin.w.headerWidth = vanilla.TextBox(
            (posx, posy, width, plugin.textFieldHeight), text="width"
        )
        posx += width + gutter
        width = plugin.textFieldHeight - 10
        posx += width + gutter
        width = widthDimensionBox
        plugin.w.headerDepth = vanilla.TextBox(
            (posx, posy, width, plugin.textFieldHeight), text="depth"
        )
        posx += width
        dialogWidth = posx + plugin.margin
        posy += plugin.lineToLine - 8
        for i in range(NUMBER_OF_FIELDS):
            posx = plugin.margin
            width = widthName
            setattr(
                plugin.w,
                "name" + str(i),
                vanilla.TextBox(
                    (posx, posy + 2, width, plugin.textFieldHeight),
                    text="_cap.something",
                ),
            )
            posx += width
            width = widthFitBox
            setattr(
                plugin.w,
                "fit_" + str(i),
                vanilla.CheckBox(
                    (posx, posy, width, plugin.textFieldHeight),
                    callback=plugin.fitCallback,
                    title="",
                    sizeStyle="small",
                ),
            )
            posx += width
            width = widthDimensionBox
            setattr(
                plugin.w,
                "widt" + str(i),
                ArrowEditText(
                    (posx, posy, width, plugin.textFieldHeight),
                    callback=plugin.editTextCallback,
                    continuous=True,
                    readOnly=False,
                    formatter=None,
                    placeholder="multiple",
                ),
            )
            posx += width + gutter
            width = plugin.textFieldHeight - 10
            imageButton = vanilla.ImageButton(
                (posx, posy + 1, width, plugin.textFieldHeight - 2),
                callback=plugin.lockWidthDepthCallback,
            )
            imageButton.getNSButton().setBordered_(False)
            setattr(plugin.w, "lock" + str(i), imageButton)
            posx += width + gutter
            width = widthDimensionBox
            setattr(
                plugin.w,
                "dept" + str(i),
                ArrowEditText(
                    (posx, posy, width, plugin.textFieldHeight),
                    callback=plugin.editTextCallback,
                    continuous=True,
                    readOnly=False,
                    formatter=None,
                    placeholder="multiple",
                ),
            )
            posy += plugin.lineToLine
        posSize = plugin.w.getPosSize()
        plugin.w.setPosSize((posSize[0], posSize[1], dialogWidth, posSize[3]))

        plugin.updateDocument(None)
        plugin.w.open()
        plugin.w.bind("close", plugin.windowClose_)
        Glyphs.addCallback(plugin.update, UPDATEINTERFACE)
        Glyphs.addCallback(plugin.updateDocument, DOCUMENTACTIVATED)
        Glyphs.addCallback(plugin.updateDocument, DOCUMENTWILLCLOSE)
    except:
        print(traceback.format_exc())
