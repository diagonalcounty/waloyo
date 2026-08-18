# Style (provisional)

This is a **reference board**, not a frozen bible. The ancient starter set exists so the direction can be judged for a day or two before mass production.

## Family

- Ink outlines, muted earth palette (ochre, umber, slate, bone).
- One figure (Settler is a couple) walking, isolated on a parchment field.
- No landscape, no diorama, no text in the frame.
- Hide, rope, knapped stone. No forged steel, no quilted gambeson, no museum-photograph lighting.

Closer to a drawn character plate than to Civ IV oil, and closer to a plate than to Unciv’s line icons.

## Views

| View | File suffix | Use |
|---|---|---|
| Side walk (facing frame-right) | `-side` | Default Unciv-facing reference; HQ turnaround |
| Front walk (toward camera) | `-front` | Second view for identity; later 3D |

Do not generate a new style for each view. Front is the same kit, rotated.

A true edge-on profile can wait until the family is confirmed.

## Ancient starter set

All files under [`art/reference/units/ancient/`](../art/reference/units/ancient/):

| Unciv name | Side | Front | Notes |
|---|---|---|---|
| Warrior | `warrior-side.jpg` | `warrior-front.jpg` | Flint celt in the **left** hand; hide shield on the back |
| Archer | `archer-side.jpg` | `archer-front.jpg` | Self-bow; hide quiver; no sword |
| Worker | `worker-side.jpg` | `worker-front.jpg` | Lashed stone hoe / adze (stone-adjacent curve is accepted) |
| Settler | `settler-side.jpg` | `settler-front.jpg` | **Couple**, packs and staves, unarmed |

Warrior is the lock. The others must sit next to it without looking like a different game.

## Connection register (not the pack lock)

Two later Settler fronts read as people you can connect with. Logged only as a **feeling note**, not a replacement for the parchment plate family.

| File | Register |
|---|---|
| `settler-front-anime.jpg` | Cleaner line, slightly larger eyes, even fills, subtle smile on the woman. Anime-adjacent without cartoon stretch. |
| `settler-front-painted.jpg` | Same couple and kit; more skin texture and painterly shade. |

What landed: adult faces, a **small closed-mouth smile** on the woman (not a grin), transparent field, same hide-and-rope kit. Do not apply this register to Warrior/Archer/Worker unless a later decision says so.

Warrior extras (same folder, not the lock):

| File | What it is |
|---|---|
| `warrior-front-anime.jpg` | Locked kit, anime-clean finish |
| `warrior-front-mace.jpg` | Different man: stone mace, held shield |
| `warrior-front-macuahuitl.jpg` | Nation unique, not generic Warrior |

## Size before lock

A still that works at 320px may fail at 64px. Open [`art/reference/size-proof/index.html`](../art/reference/size-proof/index.html) before calling a family locked. Civilopedia and hex tokens can be two drawings of the same unit.

## What to reject

- Firaxis or wiki rips (including upscales).
- Metal axe silhouettes with a pale “steel” band on the bit.
- In-line spear points sold as axes.
- Pixel-art or 3D cinematic one-offs in this pack.
- Hex terrain treated as Waloyo map art (that format does not transfer).

## Dual output (when generation resumes)

Each approved brief yields:

1. **Unciv** — sized and cropped for the slot (`UnitIcons` ~100px, `UnitPortraits` 100–256 square with margin, hex unit sprite as needed).
2. **HQ** — the same subject, same family, larger, kept as the Waloyo / later-3D master.

The written brief is the source of truth. Civ I–V are a **subject list**, not image prompts.
