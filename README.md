# Waloyo

A Civilization IV–inspired 4X. The public name is **Waloyo**. It is not Civilization, and it does not ship Firaxis art, audio, or code.

The first shippable increment is original 2D art that:

1. Drops into [Unciv](https://github.com/yairm210/Unciv) as a community audiovisual pack (hex board, current Unciv objects only).
2. Keeps a high-detail master of each subject for Waloyo later (square board, stacks, modern UI).

Mechanics come after the look is locked. Unciv is the playable spec and the first renderer, not the engine Waloyo will become.

## What this repo is not

- Not an Unciv fork.
- Not Project Tessera, Cv4MiniEngine, or any host for `CvGameCoreDLL`.
- Not a place for ripped Civ IV / V portraits, tiles, music, or Baba Yetu.

Historical people and game *mechanics* are fine. Firaxis *expression* is not.

## Repo layout

```
README.md                 this file
LICENSE                   MIT
RESEARCH.md               engine survey (Unciv vs Tessera vs clean-room)
docs/ROADMAP.md           phases
docs/ASSETS.md            catalog, issue titles, labels
docs/STYLE.md             provisional art direction
art/reference/            locked stills (style board, not Unciv-ready exports)
```

## Art direction (provisional)

Ink-line character illustration on a parchment field. Hide, rope, and knapped stone — not oil-painted reconstruction, not Noun Project icons.

The ancient starter set (Warrior, Archer, Worker, Settler) lives in [`art/reference/units/ancient/`](art/reference/units/ancient/). Each unit has a **side** walk and a **front** walk. That set is a reference for judging the direction, not a finished tileset.

See [docs/STYLE.md](docs/STYLE.md).

## Tracking work

GitHub issues are the asset ledger. One issue per Unciv object (or per object × remaining slot). Labels record **kind**, **slot**, **era**, **target**, and **status**. Conventions are in [docs/ASSETS.md](docs/ASSETS.md).

## Documents

| Doc | What it is |
|---|---|
| [docs/ROADMAP.md](docs/ROADMAP.md) | High-level phases |
| [docs/ASSETS.md](docs/ASSETS.md) | How art is catalogued and issued |
| [docs/STYLE.md](docs/STYLE.md) | Style lock notes |
| [RESEARCH.md](RESEARCH.md) | Why Unciv is the spec, not the product engine |

## License

Code and project-owned writing: MIT. Original art in this repo is project-owned unless a file says otherwise. Do not add third-party assets without a recorded license in the file’s issue.
