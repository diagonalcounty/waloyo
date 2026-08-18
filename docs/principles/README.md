# Principle cards

**This is documentation, not code.**

## What “wealth” means here

In the sources this catalogue uses (Sowell, Williams, Hayek, and kin), **wealth is not only coin and goods**. It includes **family and posterity**: skill, health, a standing household, a child who can start ahead of you. That is the project’s working definition. A score that only counts money is the narrower sense we are not using.

Research lands here as **cards** — short, checkable notes. They are the source we use to invent chapter verbs. Nothing in `src/` (when that exists) should invent a wealth rule that is not on a card first.

When a chapter is actually built, the cards that chapter uses may be copied into data (`data/principles/*.json` or similar). That is a later step. Do not start there.

## Card shape

Every card answers:

| Field | Meaning |
|---|---|
| **Id** | Stable slug, e.g. `hayek-prices-as-signals` |
| **Name** | Plain language |
| **Source** | Who, which work |
| **Mechanism** | Why this generates (or destroys) wealth |
| **Player does** | A verb, not a quote |
| **Player fails** | How surplus dies if they do the opposite |
| **Chapters** | Where it might apply (`open` until #23) |
| **Issue** | Research ticket |

## Files

| File | Source |
|---|---|
| [hayek-use-of-knowledge.md](hayek-use-of-knowledge.md) | Hayek, *The Use of Knowledge in Society* (1945) — [#20](https://github.com/diagonalcounty/waloyo/issues/20) |
| [compassionate-self-interest.md](compassionate-self-interest.md) | Player stance in a living economy — [#24](https://github.com/diagonalcounty/waloyo/issues/24) |
| [household-stakes.md](household-stakes.md) | Care for each other; a coming season of one market worker — [#25](https://github.com/diagonalcounty/waloyo/issues/25) |

Playtest (HTML, not the game): [`prototypes/prices-as-signals/index.html`](../../prototypes/prices-as-signals/index.html) — card `hayek-prices-as-signals`.

Parent track: [#14](https://github.com/diagonalcounty/waloyo/issues/14).
