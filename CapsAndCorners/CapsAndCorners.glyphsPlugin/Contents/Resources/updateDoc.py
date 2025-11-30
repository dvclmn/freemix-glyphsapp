from constants import NUMBER_OF_FIELDS
from GlyphsApp import Glyphs, CORNER, CAP


def documentUpdated(plugin, sender):
    for i in range(NUMBER_OF_FIELDS):
        for prefix in ["name", "fit_", "widt", "lock", "dept"]:
            getattr(plugin.w, prefix + str(i)).show(False)
    if not Glyphs.currentDocument:
        plugin.font = None
        return
    plugin.font = Glyphs.currentDocument.font
    if not plugin.font:
        return

    corners = set()
    caps = set()
    for glyph in plugin.font.glyphs:
        for layer in glyph.layers:
            for hint in layer.hints:
                if hint.isCorner:
                    if hint.type == CORNER:
                        corners.add(hint.name)
                    else:
                        assert hint.type == CAP
                        caps.add(hint.name)
    caps = sorted(list(caps))
    corners = sorted(list(corners))
    plugin.cc = [(c, CAP) for c in caps]
    plugin.cc += [(c, CORNER) for c in corners]
    i = 0
    for cname, ctype in plugin.cc:
        if ctype == CAP:
            getattr(plugin.w, "fit_" + str(i)).show(True)
        nameBox = getattr(plugin.w, "name" + str(i))
        nameBox.set(cname)
        nameBox.show(True)
        getattr(plugin.w, "widt" + str(i)).show(True)
        getattr(plugin.w, "lock" + str(i)).show(True)
        getattr(plugin.w, "dept" + str(i)).show(True)
        i += 1
        if i == NUMBER_OF_FIELDS:
            break
    newHeight = (
        plugin.lineToLine + len(plugin.cc) * plugin.lineToLine + 2 * plugin.margin - 16
    )
    posSize = plugin.w.getPosSize()
    plugin.w.setPosSize((posSize[0], posSize[1], posSize[2], newHeight))
    plugin.isLocked = [False] * NUMBER_OF_FIELDS
    plugin.update(None)
