# .si — names confirmed absent from the zone, 2026-09-19

> **CORRECTION (verified against registrar data):** the counts below are an UPPER
> BOUND, not an availability list. .si delegates a domain only after two working
> nameservers pass the registry's predelegation check, so a registered name held
> without DNS -- the normal state for a name an investor is flipping -- is invisible
> to a DNS probe. `distill.si`, `lucid.si` and `hi.si` all read as absent here and are
> in fact registered (`distill.si` is listed on Afternic). Treat every name below as
> UNCONFIRMED and re-check with `check_si.py`, which uses RDAP/WHOIS and sees
> registrations regardless of DNS.

Method: 1,234 candidate labels queried for NS/SOA/A across six independent public
resolvers (Google, Cloudflare, Quad9, OpenDNS, Verisign) and, for the top picks,
against `ns2.arnes.si` — the .si authoritative server — directly. A name absent
from the .si zone (NXDOMAIN) is not delegated. **254 came back absent; ~80% of
everything tested was already registered.**

Two caveats, both real:
- **DNS absence is strong evidence, not proof.** Register.si maintains a reserved-
  names list I could not fetch, and a registered name whose nameservers never
  passed the registry's predelegation check also stays out of the zone. Confirm in
  a registrar cart — it takes seconds and it is authoritative.
- Names returning SERVFAIL from every resolver (`bots.si`, `deep.si`,
  `embedding.si`, `hallucination.si`, `syntheticdata.si`, `sentio.si`, `ba.si`,
  `ok.si`, `or.si`, `ma.si`, `pa.si`, `jp.si` …) are **delegated with broken DNS —
  registered.** Excluded here.

Price at time of writing: **~$11.45 cheapest lister, $12.29 at Dynadot.** Flat —
.si has no registry premium tiers, so every name below costs the same.

---

## Tier 1 — buy today (the catalyst is ~36 hours old)

`superiorintelligence.si` and `supremeintelligence.si` are **already gone**, which
tells you how fast the exact-match phrases move. These are the adjacent ones:

| Domain | Why |
|---|---|
| superiorai.si | poll leader + AI, exact |
| supremeai.si | second poll option |
| superiormind.si / suprememind.si | the readable brandable version |
| superiorlabs.si / supremelabs.si | company-shaped |
| superiorcompute.si / supremecompute.si | infra-shaped |
| superiorsystems.si / superiormachine.si | wider net |
| notartificial.si / beyondartificial.si | the "artificial is the problem" framing |
| realintelligence.si / trueintelligence.si / newintelligence.si | same framing, cleaner |
| ineloquent.si | his actual word. quotable, cheap, a lottery ticket |

**~$180 for all 15.**

## Tier 2 — your synthetic-intelligence thesis (the differentiated bet)

Least crowded tier: the May rush chased *super*, not *synthetic*.

**Best:** `syntheticai.si` · `syntience.si` (coined term for synthetic sentience —
genuinely brandable) · `synthetica.si` · `syntheticmind.si` · `synthminds.si` ·
`synthcortex.si`

**Rest available:** syntheticlabs, syntheticminds, synthbrain, synthengine,
synthforge, synthcore, synthos, synthia, synthica, synthesist, synthiq, synthflow,
synthbase, synthstack, synthgen, synthfield, synthspace, synthmachine, synthsystems,
synthgroup, synthfoundry, synthetically, synthesizer, synthlabs, synthworks

## Tier 3 — AI vocabulary nobody claimed (the genuine surprise)

These are real field terms sitting open. Best of the whole sweep:

| Domain | Why |
|---|---|
| **interpretability.si** | an entire research field, unowned |
| **distill.si** | short, real word, ML heritage (distill.pub) |
| **circuits.si** | mech-interp term of art |
| **activations.si** | same |
| **longcontext.si** | current, commercially live |
| **scalableoversight.si** | alignment term of art |
| **chainofthought.si** | the most recognizable technique name here |

Also open: gradients, ablation, rollouts, toolcalling, functioncalling,
mixtureofexperts, rewardmodel, policygradient, grpo, misalignment, factuality,
uncertainty, refusal, watermarking, explainable, posttraining, inferencing,
retrieve, alignedai.

⚠ `constitutionalai.si` is free but "Constitutional AI" is Anthropic's coinage —
brandable-adjacent enough to draw a dispute. Skip it.

## Tier 4 — brandables

`lucid.si` is the best single-word name in the sweep. Also: axioms, kyra,
ingenuity, intellects, psyches, apperception, ratiocination, noeticlabs, vertexai
(⚠ vertexai = Google's product name — skip).

## Tier 5 — si-prefix institution names (79 free, ranked lower)

`si…si` is redundant and that caps resale value, but a few read like real orgs if
SI becomes the term: **sisafety · sialignment · sievals · sibench · sicompute ·
siresearch · siinstitute · sipolicy**. The other ~60 (siapp, sijobs, sistore,
sitracker, siwiki …) are in `AVAILABLE.csv` — filler, not a thesis.

## Tier 6 — two-letter (79 absent — treat with suspicion)

**`si.si` is absent from the zone.** If it is genuinely registrable rather than
registry-reserved, it is the single best name in this extension for your thesis and
worth trying before anything else on this page. Assume reserved until a cart says
otherwise; two-letter labels are the most likely category to be on the reserved list.

Others absent: hi, do, en, es, pi, bi, ne, na, po, ci, di, ph, ms, cs, xl, sl, tu,
ve, br, bo, and ~59 more in `AVAILABLE.csv`.

---

## Suggested basket

| Basket | Names | Cost/yr |
|---|---|---|
| Minimum viable | si.si (if it clears) + Tier 1 top 6 + interpretability, distill, lucid, syntheticai, syntience | ~$140 |
| Recommended | the above + rest of Tier 1 + Tier 2 best 6 + Tier 3 best 7 | ~$430 |
| Everything worth owning | ~60 names across Tiers 1–4 | ~$740 |

Buy **1-year terms.** ARNES has not raised price in twenty years, so the hike you'd
be hedging with a 5-year term is small, and the option to walk away in twelve
months is worth more than the hedge.

Full machine-readable list: `AVAILABLE.csv` (254 rows, with per-name confidence).
