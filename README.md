# MesloLGM Nerd Herdr

MesloLGM Nerd Font with the herdr-radar agent icons patched in, so iTerm2 (which
has no per-codepoint font mapping) shows both the oh-my-posh status bar glyphs
and the Herdr sidebar icons from one font.

- Base: MesloLGM Nerd Font 3.4.0 (Regular, Bold, Italic, Bold Italic)
- Icons: `HerdrAgentIconsMax-Regular.ttf` from hhdebb/herdr-radar v1.4.2
  (commit 1ba8cc4), codepoints U+E1A0–E1BA and U+E1C0–E1C5, free in Nerd Fonts.
  MIT (`LICENSE-herdr-radar`); many marks are third-party trademarks, see
  `THIRD_PARTY_NOTICES-herdr-radar.md`.
- Icons are rescaled from UPM 1000 to Meslo's 2048 and centered in the 1233-unit cell.
- Family `MesloLGM Nerd Herdr`, PostScript `MesloLGMNerdHerdr-<Style>`, so it never
  collides with the stock `MesloLGMNF-*` faces.

## Install

```sh
cp MesloLGMNerdHerdr-*.ttf ~/Library/Fonts/
```

iTerm: Settings → Profiles → Text → Font → **MesloLGM Nerd Herdr**, size 12.

## Rebuild

Needed when herdr-radar changes its icon font (the glyphs here are a copy).

```sh
uv run --with fonttools python -I ~/fonts/MesloLGM-Nerd-Herdr/merge.py \
  ~/.config/herdr/plugins/github/hhdebb.herdr-radar-*/dist/HerdrAgentIconsMax-Regular.ttf \
  ~/fonts/MesloLGM-Nerd-Herdr \
  ~/Library/Fonts/MesloLGMNerdFont-{Regular,Bold,Italic,BoldItalic}.ttf
cp ~/fonts/MesloLGM-Nerd-Herdr/MesloLGMNerdHerdr-*.ttf ~/Library/Fonts/
```

Each output line should end with `U+E0B0:ok U+E1A0:ok U+E1C5:ok` and `leftover=[]`.
