# Archived: Civ-engine survey (not the product)

**Status:** archived. Waloyo is a **chapter game** about wealth-generating principles and a recurring couple ([issue #12](https://github.com/diagonalcounty/waloyo/issues/12)). This file is the earlier Unciv / Tessera / Civ IV engine study. Do not treat it as the roadmap.

---

# Waloyo — Research: Adapting Unciv (or similar) to Civilization IV rules with square tiles

**Codename:** Waloyo  
**Date:** 2026-08-15  
**Goal (superseded):** A modern, open-source, iPad-friendly implementation of Civilization IV–style gameplay (vanilla + Warlords + Beyond the Sword preferred).

---

**Unciv should not be converted in place, and Project Tessera should not be used as the game.** The maintainable path is a clean-room Godot 4 engine with square tiles and stacking as first-class primitives, using Unciv’s Civ IV JSON and unique catalog as a living specification — not as the runtime.

Unciv is an excellent playable Civ V clone and a strong *rules-data* reference. It is a poor *engine* for Civ IV because hex + 1UPT is load-bearing, stacking was rejected upstream, and the official Civ IV ruleset is an approximation on Civ V primitives. Tessera and Cv4MiniEngine are 64-bit *compatibility hosts* for the original Civ IV install and `CvGameCoreDLL`. They require proprietary assets and code, so they fail the clean-room and iPad goals.

---

## Requirements (project brief)

- Base game rules, complexity, difficulty curve, civics, religion, great people, cottage economy, combat depth, and pacing as closely as possible on **Civilization IV** (vanilla + Warlords + Beyond the Sword preferred).
- **Square tiles** (not hexes) and **unit stacking** (classic Civ IV), not 1UPT.
- Prefer starting from or heavily referencing [Unciv](https://github.com/yairm210/Unciv) (LibGDX/Kotlin) and its official [Civ IV base ruleset](https://github.com/yairm210/Civ-IV) (yairm210), while acknowledging Unciv is hex-based and 1UPT.
- Evaluate alternatives: Godot 4 (Project Tessera, clean-room efforts), other open-source 4X engines, or a hybrid (Unciv rules logic + new rendering/movement layer).
- Modern 64-bit codebase, good performance on mobile/tablet (especially iPad), strong moddability, touch-friendly UI.
- **Clean-room reimplementation of mechanics** — no proprietary assets or code.
- Historical figures (Gandhi, Caesar, Elizabeth I, etc.) may be used freely.
- License compliance and attribution for all third-party code, assets, and music (especially Unciv MPL-2.0 and CC BY-SA assets such as 0 A.D. music). Source availability and attribution must be met if the game is distributed or sold.

---

## Current status of relevant projects

| Project | What it actually is | Grid / occupancy | Civ IV fidelity | License | iPad / mobile | Status (as of mid-2026) |
|---|---|---|---|---|---|---|
| **[Unciv](https://github.com/yairm210/Unciv)** | Kotlin/LibGDX Civ **V** remake. ~11k stars, 13k+ commits, actively maintained | Hex, 1UPT (1 military + 1 civilian + air list) | Engine is Civ V. G&K still incomplete; BNW not done | **MPL-2.0** | Android/desktop first-class. **iOS explicitly not planned** | Mature, potato-friendly, touch-capable on Android tablets |
| **[yairm210/Civ-IV](https://github.com/yairm210/Civ-IV)** | Official Unciv *base ruleset* (JSON + CC icons) | Same Unciv hex/1UPT engine | Data remap: civics → policy branches, cottages as improvements, many TODOs | MPL-2.0 on JSON if copied; icons CC BY | Runs wherever Unciv runs | Last push Dec 2025; 12 open issues; playable approximation, not a simulation |
| **Warlords / BtS Unciv expansions** ([RobLoach](https://github.com/RobLoach/Civ-IV---Warlords)) | Extra JSON on top of Civ-IV | Same | Partial (leaders, UUs; engine gaps remain) | Same | Same | Low activity |
| **[Project Tessera](https://github.com/Chrischn/Project-Tessera)** | Godot 4.5 + C++ GDExtension **runtime for original Civ IV mods** | Square (Civ IV’s) | Highest possible — because it *loads* BtS 3.19 + unmodified `CvGameCoreDLL` | **GPL-3.0** | Requires owned Civ IV install; Windows/Wine host; **not iOS-viable** | Prototype 0.1.0 (Mar 2026). NIF pipeline + XML/Python extract + main menu. No terrain loop, no playable turn |
| **[Cv4MiniEngine](https://github.com/fortsnek9348/Cv4MiniEngine)** (snowern) | 64-bit **terminal** host for the original DLL | Square + stacking (vanilla) | Vanilla BtS mechanics (regular build aims for hash-identical state) | Mixed; **includes Firaxis DLL source** | Desktop TUI only | Experimental but playable SP; huge-map SIMD/pathing work |
| **[Freeciv](https://www.freeciv.org/)** / Freeciv-web / Freeciv Go | Mature 4X since 1995 | **Square default** (hex optional), **stacks** | Closest to **Civ II**, not IV. Rulesets exist but not BtS civics/religion/GP | GPL-2.0+ (web client AGPL) | Android + **iOS “Freeciv Go”** exist; UI is dated | Only production square+stack FOSS 4X that can be shipped today |
| **[civ-clone](https://github.com/civ-clone/civ-clone)** | TypeScript plugin engine | Square, stacks (Civ I style) | Civ **I**; designed so later titles could be plugins — Civ IV not built | Open (plugin model) | Web renderer; needs original Civ I art | Incomplete Civ I; original assets required |

Blake00’s CivFanatics 64-bit / multithreading thread is the historical parent of Tessera and Cv4MiniEngine. Those projects solve “run existing BtS mods in 64-bit,” not “ship a clean-room tablet game.”

---

## What Unciv provides

### Strengths worth treating as *ideas*

- Data-driven rules: JSON objects + a large **Uniques** language (modifiers, filters, conditionals).
- Clean game-state tree: `GameInfo` → civs / `TileMap` / `RuleSet`.
- Proven mobile performance (2D, low-res, turn-based, clone-the-state-then-simulate).
- The Civ-IV ruleset already encodes most *names and approximate numbers*: 5 civic categories, cottage/hamlet/village/town, many promotions, techs, nations, GP types.

### Engine assumptions that block Civ IV

Unciv’s occupancy model is hardcoded in `Tile`:

```kotlin
var militaryUnit: MapUnit? = null
var civilianUnit: MapUnit? = null
var airUnits = ArrayList<MapUnit>(0)
```

That is Civ V 1UPT, not a stack. Pathfinding treats an occupied tile as *pass-through but not enterable*. Combat is 1v1. AI, ZOC, city defense, air intercept, and the world UI all assume “one military silhouette per hex.”

Coordinate math is a first-class hex library (`HexMath.kt`, `HexCoord`). Neighbors are clock positions 2/4/6/8/10/12. Rivers store three edge bits that only make sense on a hex. Distance, wrap, map gen, LOS, city rings, and rendering all call this.

Upstream already closed stacking as **not planned** ([issue #10053](https://github.com/yairm210/Unciv/issues/10053)). The project charter is “if it was in Civ V, yes; otherwise no.” A square+stack fork would never merge.

### The official Civ IV ruleset is a translation layer, not Civ IV

`yairm210/Civ-IV` maps civics onto Unciv **policy branches** (one policy per category, mutually exclusive via `Unavailable <after adopting …>`). Civic upkeep is faked as gold-per-population. The file is full of honest TODOs:

- Slavery: “Can hurry production while sacrificing city population” — not implemented
- Emancipation: unhappiness in civs without it; cottage *growth* doubled — approximated as build-time
- Mercantilism: free specialist / no foreign trade / corporations — missing
- Nationhood: +25% espionage — missing
- Free Religion: +1 happy per religion; no state religion — missing
- Caste: unlimited artist/merchant/scientist — missing
- Universal Suffrage: gold rush — missing

Open issues include religion spreading, city-level resources, city strength, forts as ports/airbases, no embark (Civ IV should use transports, not Civ V embark), transport units, and AI water behavior.

**Unciv with the Civ IV ruleset is a Civ IV–flavored game.** It does not provide Civ IV combat depth, stack tactics, civic upkeep, cottage *growth*, or BtS corporations.

---

## Feasibility: hex/1UPT → square + stacking inside Unciv

### Square tiles — medium, but it forks the project

Technically straightforward if a `GridTopology` is introduced (neighbors, distance, wrap, river edges, world projection) and `HexMath` callers are rewritten against it.

What actually has to change:

- All neighbor / ring / distance / wrap code
- Map generator (continents, climate, resource scatter, starting locations)
- River model (4 or 8 edges vs 6)
- Tilesets (every existing tileset is hex; a new square/iso art pipeline would be required)
- LOS and city work rings (Civ IV is a square fat-cross / culture expansion, not hex rings)
- World wrap and “clock position” river/road drawing

Estimate if done as a **hard fork** with a topology abstraction: **3–6 months** for a competent Kotlin/LibGDX team to get a playable square map. Not a weekend flag.

Diagonal movement is a design choice that must be locked early (Civ IV uses 8-directional squares with diagonal movement costing the same as orthogonal — that is part of the feel).

### Stacking + Civ IV combat — large, and this is the real cost

This is not “allow `List<MapUnit>` on a tile.” Civ IV combat is a different game:

| Civ IV behavior | Unciv today |
|---|---|
| Unlimited land stack | 1 military |
| Best defender chosen (strength, bonuses, first strikes, HP) | The one unit on the tile |
| 1v1 resolution, winner stays, loser dies/withdraws | Similar 1v1, but no stack context |
| Collateral (catapults/cannons/artillery, siege + flanking) | Does not exist |
| First strikes / immunity, amphibious, animal, hidden nationality | Partial via uniques |
| Stack attack / group move / sentry / fortify-all | No stack UI |
| Air: recon, bombard, intercept, rebase, fighters on carriers/cities/forts | Civ V air list, different rules |
| Naval stacks, cargo slots, privateers | Partial |
| Collateral vs siege vs collateral immunity promotions | Missing |
| City defense from culture + buildings + garrison, not hex ZOC carpets | Different formula (mod already hacks `cityStrength*` constants) |

Then the **AI** must be rewritten. Unciv’s war AI is 1UPT positioning (front lines, ranged kiting, “don’t stack”). Civ IV AI is stack composition, siege escort, collateral, and SoD vs SoD. That is most of the remaining difficulty curve that matters.

Then **UI**, especially on iPad: stack inspector, pick attacker/defender, select-all / group-goto, “this stack has 40 units,” sentry/fortify/wake, air mission picker. 1UPT UIs collapse here. Old World’s notes are explicit: stacking was delayed because the UI is the hard part.

Honest fork estimate: **12–24 months** to get stacking + combat + AI + tablet UI to “feels like Civ IV war,” on top of the square-grid work. Then another **1–3 years** for civics-as-civics, religion spread, cottage *growth*, great people, vassals, corporations, espionage, and difficulty curve.

The fork would also permanently diverge from Unciv. Every upstream unique, multiplayer, and bugfix becomes a merge tax.

**Verdict:** converting Unciv is feasible as a *hard fork*, not as a mod and not as a PR. Effort is comparable to writing a new map/combat layer anyway — which is the argument for not starting there.

---

## Architecture recommendation

Three options, ranked for Waloyo’s goals (clean-room, iPad, square+stack, Civ IV rules, moddable, 64-bit).

### 1. Recommended: Godot 4 clean-room engine + Unciv as spec

**Keep Unciv’s data layer as a specification. Do not keep Unciv’s simulation or renderer.**

```
┌─────────────────────────────────────────────┐
│  Godot 4.x  (GDScript + C# or GDExtension)  │
│  Touch-first UI, TileMapLayer, iOS export   │
├─────────────────────────────────────────────┤
│  Game sim (project code, MIT or MPL)        │
│  Grid: square 8-dir, wrap, culture, LOS     │
│  Occupancy: Stack { units[], cargo, air }   │
│  Combat: Civ IV resolver (best defender,    │
│          collateral, first strikes)         │
│  Economy: cottages-as-state-machine,        │
│          5 civic categories, GP points      │
├─────────────────────────────────────────────┤
│  Rules data (JSON)                          │
│  Inspired by Unciv uniques + Civ-IV jsons   │
│  Clean-room numbers from public civpedia    │
└─────────────────────────────────────────────┘
```

Why Godot over a Unciv fork:

- First-class **iOS/iPad** export (macOS + Xcode + $99/year). Unciv’s author will not do iOS; LibGDX/MobiVM is a second-class path.
- Square tiles are native (`TileMapLayer`), not a conversion.
- 64-bit, MIT engine, no JVM on iOS.
- Touch UI can be designed from day one (Unciv’s UI is Android-desktop hybrid, still 1UPT).
- Xogot even runs the Godot editor on iPad, which would allow on-device iteration.

Why *not* Tessera as the base:

- It is a **mod runtime**, not a game. It must load `Civ4BeyondSword.exe`, FPK art, and the 32-bit `CvGameCoreDLL`.
- The clean-room claim applies to Tessera’s *bridge*, not to a product that would ship that way — the gameplay still comes from Firaxis code.
- GPL-3 plus “must own Civ IV” is incompatible with an independent App Store game.
- iPad cannot load a VS2003 32-bit DLL via a Wine TCP relay.

Tessera / Cv4MiniEngine should be used only as **oracles**: run the same scenario in BtS and compare combat rolls, civic upkeep, cottage growth — never copy their DLL-facing code.

### 2. Acceptable if the team is a Kotlin shop: Unciv hard fork, isolated sim

Only if the team is already fluent in Unciv and is willing to never upstream.

- New module `grid` + `stack` + `civ4combat`, no hex types leaking out.
- Keep Unciv’s unique parser, save format ideas, translations, and JSON schema.
- Expect to rewrite WorldScreen unit UI and most of the war AI.
- iOS remains a separate, expensive track (MobiVM or a later Godot client talking to a Kotlin core — possible, rarely worth it).

A “hybrid Unciv rules + new renderer” should not be attempted without extracting the sim into a headless library first. Unciv’s `GameInfo` is entangled with LibGDX transients, GUI, and hex `TileGroup`. A clean extraction is a multi-month project of its own.

### 3. Not recommended as the product foundation

| Foundation | Why it fails the brief |
|---|---|
| Tessera | Proprietary assets + DLL; GPL-3; not a game; not mobile |
| Cv4MiniEngine | Firaxis DLL source in-tree; TUI; not clean-room |
| Freeciv | Square+stack *works*, but Civ II rules; GPL; rewriting it into BtS is another 4X |
| civ-clone | Civ I + original art; TypeScript plugins are a nice *idea*, no Civ IV content |
| Unciv as a mod only | Cannot do square or stacks |

---

## Technical challenges (the ones that decide success)

**Combat and stacks.** The resolver should be implemented *before* the pretty map. Best defender, withdrawal, first strikes, collateral targeting rules, amphibious, animal, city defender, collateral immunity, flanking vs siege, air bombard vs units vs improvements. This is the product.

**Civic system.** Five independent categories, anarchy, civic upkeep (difficulty × map size × population × civic cost — the CivFanatics article the Unciv mod already cites and has not implemented), Organized trait, Pyramids / Shwedagon Paya enabling all, Slavery whip, US gold rush, Emancipation unhappiness as a *global* pressure.

**Cottage economy.** Cottage → Hamlet → Village → Town is a per-tile turn counter, paused in unrest/occupation, sped by Emancipation, gold-modified by Free Speech / Universal Suffrage. Unciv can place the improvement; it does not grow it as Civ IV does.

**Religion (BtS).** Founding by first-to-tech, missionaries, spread chance, shrine gold, holy city, state religion, Theocracy blocking non-state spread, Organized Religion missionaries without monastery, Apostolic Palace / UN. Unciv religion is G&K-shaped (beliefs, faith). The Civ-IV mod’s `Beliefs.json` is another remap.

**Great people.** Separate GP point pools per city, threshold curve, settle vs bulb vs build vs golden age, Great General from combat XP, Great Spy (BtS). Unciv has a GP manager aimed at Civ V.

**Difficulty and pacing.** Civ IV difficulty is mostly AI bonuses (free techs, production, maintenance, barbarians, unit support) plus human penalties. Unciv difficulties are Civ V-shaped. The BtS tables should be recreated, then the curve playtested — this is months of design, not a JSON paste.

**AI.** Hardest long-term piece. Stack composition, siege escort, naval invasion, cottage vs workshop, civic timing, religion use. This should be budgeted as a multi-year subsystem, not a milestone finished before vertical slice.

**Tablet UI.** Stacks of 20–80 units on a 10–11" screen. Need: stack badge counts, drill-in list, multi-select, “move stack / split / sentry,” large hit targets, no hover-dependent combat odds. This should be designed as a first-class spec, not an afterthought.

**Performance on iPad.** Turn-based 2D is easy if the renderer is Unciv-like (sprite tiles, clone state, sim off-thread). It becomes hard if 3D NIF units are rendered like Tessera. For iPad, stay 2D/2.5D isometric or orthogonal; instanced sprites; sim on a background isolate; never walk all units × all tiles naively on end-turn. Freeciv and Unciv both prove a full 4X is fine on a tablet if the renderer is modest.

**Moddability.** Follow Unciv’s lesson: data in JSON, effects in a unique/effect language, no recompile for a new civ. A Python 2.4 BtS API should not be exposed unless the goal is Tessera’s job (running existing mods). A modern Lua or Godot-resource mod API is enough.

---

## License, attribution, and legal hygiene

This is not legal advice; it is the compliance shape the project should design for.

**Mechanics and historical people.** Game rules are not copyrightable (Unciv correctly cites US Copyright Office FL-108). Gandhi, Caesar, Elizabeth I, etc. as historical figures are fine. Firaxis-specific *expression* should be avoided: leader quotes copied from the game, Civilopedia text, unique art, Baba Yetu, UI layout clones that look like Civ IV.

**The Civilization name and Firaxis logos should not be used.** Unciv’s own FAQ is the right posture. Waloyo is the internal/project name; the public title should remain original.

**Unciv (MPL-2.0).** File-level copyleft. The game may be sold. MPL notices must be kept on any Unciv files that are copied or modified, and source for those files must be shipped or linked. New files may be placed under MIT/Apache. A “Larger Work” can have a commercial wrapper. Practical approach: **do not copy Kotlin sources**; reimplement. If `Civ-IV` JSON is copied, those files stay MPL-2.0 — easy to isolate in `data/mpl/`.

**Unciv assets.** Mix of CC BY 3.0/4.0, CC BY-SA 3.0/4.0, CC0, and a few unknown. HexaRealm is CC BY-SA 3.0 (share-alike). Noun Project icons need attribution. Unknown-license promotional art should not be redistributed. Hex tilesets will not fit a square game anyway — square/iso art should be commissioned or generated.

**0 A.D. music.** CC BY-SA 3.0. It may be used commercially if Wildfire Games / the composers (Omri Lahav et al.) are **attributed** and *that music and adaptations* are licensed under CC BY-SA. Share-alike does **not** automatically infect an MIT/MPL engine, but it does infect modifications of the music and can complicate an App Store binary if handled sloppily. Safer: original music, or CC BY / CC0 tracks, and keep any BY-SA audio in a clearly attributed pack.

**Tessera is GPL-3.0.** Linking or deriving would make the game GPL-3. Combined with “requires Civ IV,” it is the wrong license for an independent App Store title.

**Cv4MiniEngine** contains original Firaxis `CvGameCoreDLL` code. It should not be copied. The BtS SDK headers are “All rights reserved.” Tessera’s ADR-007 is correct: clean-room ABI only, and even that is for a *compatibility host*, not this game.

**If the game is sold on the App Store.** MPL and MIT are App Store–compatible. GPL-3 and AGPL are painful. A source URL should be provided in-game (Credits → Source). A `NOTICE` / `CREDITS.md` should be kept the way Unciv does. Apple still requires a $99 developer account and will review trademarks — the product should not look like Civ.

---

## Recommended starting point

1. **Play Unciv + Civ-IV + Warlords + BtS mods** and keep a gap list (seeded by their GitHub issues and the TODOs in `Policies.json`).
2. **Play BtS 3.19** as the mechanical oracle. Optionally use Cv4MiniEngine later for automated comparison, without taking code.
3. **Scaffold a Godot 4 project** with: square map, multi-unit tiles, stack inspector, and a *single* combat resolver that matches published Civ IV formulas (civilization.fandom / CivFanatics).
4. **Write a project-owned JSON schema** (Unciv-inspired uniques). Re-encode numbers from public sources. Treat `yairm210/Civ-IV` as a checklist, not a copy-paste, unless those files are isolated as MPL.
5. **Do not start with 3D NIF units, Python mods, or a DLL host.** That is Tessera’s product, not Waloyo’s.

---

## High-level roadmap

### Phase 0 — Spec (4–8 weeks)

- Civic, combat, cottage, religion, and GP rule cards from public sources (not decompiled DLL).
- Unciv Civ-IV gap matrix (what the JSON pretends vs what the engine does).
- Tablet UI wireframes for stacks and city screen.
- License register and original public title.

### Phase 1 — Vertical slice (3–5 months)

- Square wrap map, 8-direction movement, roads/rivers.
- Stacks: move, split, fortify, best-defender combat, one collateral unit type.
- 8–12 units, 2 civs, 1 difficulty, cottage growth, one civic category.
- iPad export of this slice (prove the pipeline early).

### Phase 2 — Economy and civics (4–8 months)

- Full 5-category civics, anarchy, upkeep, whip, gold rush, emancipation pressure.
- Specialists, GP points, settle/bulb/GA.
- Religion founding + missionaries + state religion (skip AP/UN at first).
- Workers, improvements, health/happy, maintenance.

### Phase 3 — War and AI (6–12 months)

- Full promotion tree, first strikes, flanking, siege collateral, air, navy, cargo.
- City capture, culture defense, forts as forts (not Civ V citadels).
- AI that builds stacks, brings siege, and understands cottages vs production.

### Phase 4 — BtS systems and polish (6–12+ months)

- Vassals, corporations, espionage, events (optional), space race, UN/AP.
- Difficulty tables and pacing pass vs BtS.
- Mod API, translations, music/attribution screen.
- App Store / Play / desktop.

**Calendar reality:** a small team should plan **3–5 years** to something that veterans will call “actually Civ IV.” Unciv took ~8 years to become a *very good* Civ V. A solo developer can ship a compelling slice in a year; “full BtS” is not a side-project-sized rewrite.

---

## Bottom line

| Question | Answer |
|---|---|
| Can Unciv become square + stacking? | Yes, only as a permanent hard fork. Upstream will not take it. |
| Is that cheaper than a new engine? | Only if the team already lives in that Kotlin codebase *and* iOS is not a goal. Even then, combat/AI/UI dominate cost. |
| Is the official Civ IV Unciv mod “full Civ IV”? | No. It is a high-quality data remap onto Civ V systems, with many TODOs. |
| Is Tessera the Godot Civ IV game? | No. It is a 64-bit *host* for the original game and mods. Wrong legal and platform shape. |
| Closest *playable* square+stack FOSS 4X? | Freeciv — but it is Civ II, not IV. |
| Best start for an iPad-friendly clean-room Civ IV? | **Godot 4, square+stack first, Unciv JSON/uniques as spec, BtS as oracle, original art/music, MPL only if copied data files are isolated.** |

Highest-leverage next documents: a **combat + civic + cottage rule card** (formulas only) plus a Godot scene graph for the stack inspector — the two pieces Unciv cannot provide and Tessera will not provide cleanly.

---

## Key references

- [Unciv](https://github.com/yairm210/Unciv) — MPL-2.0, Kotlin/LibGDX Civ V remake
- [Unciv project structure](https://yairm210.github.io/Unciv/Developers/Project-structure-and-major-classes/)
- [Unciv stacking request (closed, not planned)](https://github.com/yairm210/Unciv/issues/10053)
- [yairm210/Civ-IV](https://github.com/yairm210/Civ-IV) — Unciv base ruleset
- [Project Tessera](https://github.com/Chrischn/Project-Tessera) — Godot Civ IV *mod runtime* (GPL-3.0)
- [Cv4MiniEngine](https://github.com/fortsnek9348/Cv4MiniEngine) — 64-bit TUI host (includes Firaxis DLL code)
- [Freeciv](https://www.freeciv.org/) — square + stacking, Civ II–like
- [civ-clone](https://github.com/civ-clone/civ-clone) — TypeScript plugin Civ I engine
- [US Copyright Office FL-108](https://upload.wikimedia.org/wikipedia/commons/9/96/U.S._Copyright_Office_fl108.pdf) — mechanics are not copyrightable
- [0 A.D. music](https://play0ad.com/media/music/) — CC BY-SA 3.0
