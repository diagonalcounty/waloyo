# Asset catalog and issues

GitHub issues are the ledger. Product direction is [issue #12](https://github.com/diagonalcounty/waloyo/issues/12) (chapters, not an Unciv catalog). The table of what exists on disk is this folder plus [`art/reference/`](../art/reference/).

New art issues should be `art/chapter/<name>` or `art/couple/<view>`, not `art/unit/<Unciv name>`.

## File names

```
art/reference/<slot>/<era>/<unciv-name>-<view>.<ext>
```

- `<slot>` — `units`, `buildings`, `wonders`, `techs`, `resources`, `improvements`, `terrain`, `leaders`, `ui`
- `<era>` — `ancient`, `classical`, `medieval`, `renaissance`, `industrial`, `modern`, `future`, or `cross` if the object is not era-tied
- `<unciv-name>` — Unciv JSON `name`, lowercase, spaces to hyphens (`great-general`)
- `<view>` — `side`, `front`, and later `icon`, `portrait`, `hex` for exports

Reference stills (style board) stay under `art/reference/`. Unciv-ready packed atlases, when they exist, will live under `art/unciv/` and must follow [Unciv image paths](https://yairm210.github.io/Unciv/Modders/Images-and-Audio/).

## Slots are different jobs

A full-body plate can win as a Civilopedia entry and fail as a hex token. **Do not lock a style on the large still alone.** Judge each subject at the sizes in [`art/reference/size-proof/index.html`](../art/reference/size-proof/index.html) (open in a browser at 100% zoom).

| Slot | Typical size | What must read |
|---|---|---|
| Civilopedia / city art | ~320px and up | Face, kit, story (Settler couple is allowed) |
| `UnitPortraits` | 100–256px square | Costume + face |
| `UnitIcons` | ~100px | Silhouette and weapon |
| Hex / map sprite | ~32–64px | Shape only — couple, smile, and beads die here |

One subject may need **two drawings**: a pedia plate and a simpler map token. That is a style decision, not a later export trick.

## Issue titles

```
art/<slot>/<Unciv name>
```

Examples: `art/unit/Warrior`, `art/building/Library`, `art/terrain/Grassland`.

Meta work uses `meta:` (`meta: enumerate Unciv vanilla objects`).

## Issue body (template)

```markdown
## Object
- Unciv name:
- Ruleset: vanilla | Civ-IV mod | other
- Era:

## Slots
- [ ] Brief (original language; subjects from Civ I–V, not their pictures)
- [ ] Reference still, side
- [ ] Reference still, front
- [ ] Unciv icon / portrait / hex (as required)
- [ ] HQ master

## Paths
- side:
- front:
- unciv:
- hq:

## Notes
```

## Labels

Apply **one of each group** that applies. Filter on GitHub with `label:slot:unit label:era:ancient`.

### `kind:` — what the issue is

| Label | Use |
|---|---|
| `kind:art` | A graphic |
| `kind:docs` | Writing, catalog, style |
| `kind:engine` | Client / rules (Phase D) |
| `kind:legal` | License, rips, attribution |

### `slot:` — Unciv image family

| Label | Unciv home |
|---|---|
| `slot:unit` | Units, unit icons / portraits / hex sprites |
| `slot:building` | Buildings |
| `slot:wonder` | Wonders + optional 2:1 splash |
| `slot:tech` | Techs |
| `slot:resource` | Resources |
| `slot:improvement` | Tile improvements |
| `slot:terrain` | Base terrain, features, hex edges |
| `slot:leader` | Leader portraits |
| `slot:nation` | Nation icons |
| `slot:ui` | Chrome, advisors, victory art |

### `era:`

`era:ancient` `era:classical` `era:medieval` `era:renaissance` `era:industrial` `era:modern` `era:future` `era:cross`

### `target:` — who consumes the file

| Label | Meaning |
|---|---|
| `target:reference` | Style-board still (current ancient set) |
| `target:unciv` | Packs into the Unciv mod |
| `target:hq` | Waloyo master / later 3D reference |

An issue may have both `target:unciv` and `target:hq`. Terrain hex tiles are `target:unciv` only.

### `status:` — how far the art has got

| Label | Meaning |
|---|---|
| `status:brief` | Needs a written brief |
| `status:wip` | Generating or exporting |
| `status:review` | Waiting for a look |
| `status:locked` | Approved reference; do not restyle casually |

`status:locked` is the ancient starter set. New units start at `status:brief` or `status:wip`.

## What gets an issue now

- One issue per locked starter unit (points at the files).
- One issue per next ancient unit we actually intend to draw soon (Scout, Spearman).
- Meta issues for the full Unciv enumeration, export pipeline, and legal hygiene.

Do **not** open an issue per vanilla Unciv object until the enumeration pass lists them. The labels are ready so that pass can file in bulk without inventing a new scheme.
