from __future__ import division, print_function, unicode_literals
import objc

from GlyphsApp import Glyphs, WINDOW_MENU
from GlyphsApp.plugins import GeneralPlugin

from Cocoa import (
    NSMenuItem,
    NSImageNameLockLockedTemplate,
    NSImageNameLockUnlockedTemplate,
)

from window import setUpWindow
from constants import *
from updateDoc import documentUpdated
from updateMain import mainUpdater

from helpers.widgets import match_widget
from helpers.hints import iter_matching_hints, update_hint_scale
from helpers.parsing import parse_percent


class CapsAndCorners(GeneralPlugin):

    @objc.python_method
    def settings(self):
        self.name = "Caps and Corners"

    @objc.python_method
    def start(self):
        item = NSMenuItem.new()
        item.setTitle_(self.name)
        item.setAction_(self.showWindow_)
        item.setTarget_(self)
        Glyphs.menu[WINDOW_MENU].append(item)

    def showWindow_(self, sender):
        setUpWindow(self, sender)

    @objc.python_method
    def updateDocument(self, sender):
        documentUpdated(self, sender)

    @objc.python_method
    def update(self, sender):
        mainUpdater(self, sender)

    # ------------------------------------------------------------
    #  UI helpers
    # ------------------------------------------------------------

    @objc.python_method
    def updateLockButtonImage(self, lockButton, index):
        if self.isLocked[index]:
            lockButton.setImage(imageNamed=NSImageNameLockLockedTemplate)
        else:
            lockButton.setImage(imageNamed=NSImageNameLockUnlockedTemplate)

    # ------------------------------------------------------------
    #  Hint mutation (apply widt/dept changes)
    # ------------------------------------------------------------

    @objc.python_method
    def updateHint(self, cname, ctype, dimension, newValue):

        self.font.disableUpdateInterface()
        try:
            for layer in self.font.selectedLayers:
                changed = False
                parent = layer.parent
                parent.beginUndo()

                try:
                    for hint in iter_matching_hints(layer, cname, ctype):
                        if update_hint_scale(hint, dimension, newValue):
                            changed = True
                finally:
                    if changed:
                        parent.endUndo()
                    else:
                        parent.endUndo()

        finally:
            self.font.enableUpdateInterface()
            Glyphs.redraw()

    # ------------------------------------------------------------
    #  Callbacks
    # ------------------------------------------------------------

    @objc.python_method
    def editTextCallback(self, editText):
        """
        Handles widt/dept changes.
        """
        # Determine which parameter this corresponds to
        i, cname, ctype = match_widget(self, editText, "")
        if i is None:
            return

        # Determine whether this is 'widt' or 'dept'
        dimension = None
        for dim in ("widt", "dept"):
            if editText is getattr(self.w, f"{dim}{i}", None):
                dimension = dim
                break

        if dimension is None:
            return

        new_value = parse_percent(editText)
        if new_value is None:
            return

        # Locked? Then apply to both dimensions
        if self.isLocked[i]:
            self.updateHint(cname, ctype, "widt", new_value)
            self.updateHint(cname, ctype, "dept", new_value)
        else:
            self.updateHint(cname, ctype, dimension, new_value)

    @objc.python_method
    def fitCallback(self, fitBox):
        """
        Toggle the "fit" option bit on all matching hints.
        """
        i, cname, ctype = match_widget(self, fitBox, "fit_")
        if i is None:
            return

        for layer in self.font.selectedLayers:
            for hint in iter_matching_hints(layer, cname, ctype):
                hint.options ^= 8

    @objc.python_method
    def lockWidthDepthCallback(self, lockButton):
        """
        Toggle lock state and normalise widt/dept if newly locked.
        """
        i, cname, ctype = match_widget(self, lockButton, "lock")
        if i is None:
            return

        # Flip
        self.isLocked[i] = not self.isLocked[i]
        self.updateLockButtonImage(lockButton, i)

        # If locking, force widt and dept to match
        if not self.isLocked[i]:
            return

        details = self.details[cname]
        w = details["widt"]
        d = details["dept"]

        if w != d:
            avg = (w + d) / 2.0
            details["widt"] = details["dept"] = avg
            self.updateHint(cname, ctype, "widt", avg)
            self.updateHint(cname, ctype, "dept", avg)
