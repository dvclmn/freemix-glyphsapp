from GlyphsApp import (
    Glyphs,
    DOCUMENTACTIVATED,
    DOCUMENTWILLCLOSE,
    UPDATEINTERFACE,
)
from constants import *
import vanilla


def setUpWindow(thing, sender):
    print("Hello ")
    try:
        self.margin = 13
        gutter = 6
        widthName = 128
        widthFitBox = 20
        widthDimensionBox = 58
        self.textFieldHeight = 23
        self.lineToLine = self.textFieldHeight + 5
        self.w = vanilla.HUDFloatingWindow(
            (100, 100), title=self.name, autosaveName="FMXCapsAndCorners"
        )
        posy = self.margin - 4
        posx = self.margin
        posx += widthName
        width = widthFitBox
        self.w.headerFit = vanilla.TextBox(
            (posx, posy, width, self.textFieldHeight), text="fit"
        )
        posx += width
        width = widthDimensionBox
        self.w.headerWidth = vanilla.TextBox(
            (posx, posy, width, self.textFieldHeight), text="width"
        )
        posx += width + gutter
        width = self.textFieldHeight - 10
        posx += width + gutter
        width = widthDimensionBox
        self.w.headerDepth = vanilla.TextBox(
            (posx, posy, width, self.textFieldHeight), text="depth"
        )
        posx += width
        dialogWidth = posx + self.margin
        posy += self.lineToLine - 8
        for i in range(NUMBER_OF_FIELDS):
            posx = self.margin
            width = widthName
            setattr(
                self.w,
                "name" + str(i),
                vanilla.TextBox(
                    (posx, posy + 2, width, self.textFieldHeight),
                    text="_cap.something",
                ),
            )
            posx += width
            width = widthFitBox
            setattr(
                self.w,
                "fit_" + str(i),
                vanilla.CheckBox(
                    (posx, posy, width, self.textFieldHeight),
                    callback=self.fitCallback,
                    title="",
                    sizeStyle="small",
                ),
            )
            posx += width
            width = widthDimensionBox
            setattr(
                self.w,
                "widt" + str(i),
                ArrowEditText(
                    (posx, posy, width, self.textFieldHeight),
                    callback=self.editTextCallback,
                    continuous=True,
                    readOnly=False,
                    formatter=None,
                    placeholder="multiple",
                ),
            )
            posx += width + gutter
            width = self.textFieldHeight - 10
            imageButton = vanilla.ImageButton(
                (posx, posy + 1, width, self.textFieldHeight - 2),
                callback=self.lockWidthDepthCallback,
            )
            imageButton.getNSButton().setBordered_(False)
            setattr(self.w, "lock" + str(i), imageButton)
            posx += width + gutter
            width = widthDimensionBox
            setattr(
                self.w,
                "dept" + str(i),
                ArrowEditText(
                    (posx, posy, width, self.textFieldHeight),
                    callback=self.editTextCallback,
                    continuous=True,
                    readOnly=False,
                    formatter=None,
                    placeholder="multiple",
                ),
            )
            posy += self.lineToLine
        posSize = self.w.getPosSize()
        self.w.setPosSize((posSize[0], posSize[1], dialogWidth, posSize[3]))

        self.updateDocument(None)
        self.w.open()
        self.w.bind("close", self.windowClose_)
        Glyphs.addCallback(self.update, UPDATEINTERFACE)
        Glyphs.addCallback(self.updateDocument, DOCUMENTACTIVATED)
        Glyphs.addCallback(self.updateDocument, DOCUMENTWILLCLOSE)
    except:
        print(traceback.format_exc())
