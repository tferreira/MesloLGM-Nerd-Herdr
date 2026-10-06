"""Copy Herdr icon glyphs into a Meslo Nerd Font face, rescaled to its grid.

Usage: merge.py <icons.ttf> <out_dir> <meslo.ttf>...
"""
import sys
from pathlib import Path

from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

OLD_FAMILY, NEW_FAMILY = "MesloLGM Nerd Font", "MesloLGM Nerd Herdr"
OLD_PS, NEW_PS = "MesloLGMNerdFont", "MesloLGMNerdHerdr"

icons_path, out_dir, *bases = sys.argv[1:]
icons = TTFont(icons_path)
icon_cmap = icons.getBestCmap()
icon_glyphs = icons.getGlyphSet()
icon_upm = icons["head"].unitsPerEm

for base_path in bases:
    base = TTFont(base_path)
    cmap = base.getBestCmap()
    assert not any(0xE1A0 <= c <= 0xE1C5 for c in cmap), f"{base_path}: codepoints taken"
    scale = base["head"].unitsPerEm / icon_upm
    cell = base["hmtx"][cmap[ord("M")]][0]

    for codepoint, name in sorted(icon_cmap.items()):
        width = icons["hmtx"][name][0] * scale
        dx = (cell - width) / 2
        pen = TTGlyphPen(None)
        icon_glyphs[name].draw(TransformPen(pen, (scale, 0, 0, scale, dx, 0)))
        glyph = pen.glyph()
        new_name = f"herdr.{name}"
        base["glyf"][new_name] = glyph
        glyph.recalcBounds(base["glyf"])
        base["hmtx"][new_name] = (cell, getattr(glyph, "xMin", 0))
        for table in base["cmap"].tables:
            if table.isUnicode():
                table.cmap[codepoint] = new_name

    for record in base["name"].names:
        text = record.toUnicode()
        renamed = text.replace(OLD_FAMILY, NEW_FAMILY).replace(OLD_PS, NEW_PS).replace("MesloLGMNF", NEW_PS)
        if renamed != text:
            record.string = renamed

    out = Path(out_dir) / Path(base_path).name.replace(OLD_PS, NEW_PS)
    base.save(out)
    check = TTFont(out)
    got = check.getBestCmap()
    names = {r.nameID: r.toUnicode() for r in check["name"].names if r.platformID == 3}
    leftover = [f"{r.nameID}={r.toUnicode()!r}" for r in check["name"].names if "MesloLGMNF" in r.toUnicode() or OLD_FAMILY in r.toUnicode()]
    probes = " ".join(f"U+{c:04X}:{'ok' if c in got else 'MISSING'}" for c in (0x41, 0xE0B0, 0xE1A0, 0xE1C5))
    print(f"{out.name}: family={names.get(1)!r} full={names.get(4)!r} ps={names.get(6)!r} uid={names.get(3)!r} leftover={leftover} {probes}")
