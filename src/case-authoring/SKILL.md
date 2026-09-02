---
name: case-authoring
description: How to author a productive-failure teaching case, where students critique a deliberately weak AI's answer before instruction and then repair it. Use when designing a new case, a hands-on exercise, a lab or a notebook students work through, when turning a lecture into something students can run, or when a case demos badly, feels overloaded, or lets students score well by flagging everything. Covers one concept per case, authoring the data so untaught errors cannot happen, putting the failure in the conclusion rather than the arithmetic, and keeping the marking scheme out of reach. See BUILDING.md for the folder that makes it run.
---

# Authoring a productive-failure case

A case is a scenario in which a domain-blind AI produces a confident answer
containing planned failures, and a student who has not yet been taught the
domain must decide what to challenge. The authoring rules below exist because
their violations were each tried, and each failed, in the source project.

## One concept per case

The first drafts carried eight or nine planned failures each. They demoed
badly: every minute of a demo spent on the fourth error is a minute the room
spends forgetting the first. The surviving cases carry ONE concept (the
relevant range; the cash conversion cycle netting) and at most one attributed
numeric error. Narrowing a case is not weakening it; the room remembers the
single contradiction it can see unaided.

## Author the data so wrong methods cannot hide

Design the numbers so that the error you are NOT teaching is impossible by
construction. In the cost case, the highest-hours week is also the
highest-cost week, so taking high-low on cost instead of the driver gives the
same answer, and that classic error cannot occur and distract from the one
being taught. Whatever failure the data permits, some student will chase.

## The failure lives in the conclusion, not the arithmetic

The strongest cases let the AI get every computation RIGHT and still reach an
indefensible conclusion: a correct fitted line priced far outside its evidence,
three correct ratios combined with the wrong sign. Students expect arithmetic
slips. A wrong judgement built from right numbers is the lesson their future
employer needs them to have had.

## Claims need both kinds

Alongside the figures, the AI's prose asserts claims the student may
challenge. Author both TRUE and FALSE claims, and word the ask as
"problematic: wrong, unsupported, or a conclusion the numbers will not carry",
not "false". Two of the best claims are arithmetically true and still
indefensible, which is precisely the distinction being taught. At least one
claim must be sound, so flagging everything scores nothing.

## Error signatures must be local

Each planned error carries a signature: the fingerprint of figures that error
produces. A signature keyed on an aggregate can accuse a student whose only
mistake was elsewhere; a signature must be able to say "this exact local
pattern, and nothing else, is this error". The gate refuses signatures that
could match correct work.

## Real company or authored company

Use a real company when the failure is visible in public filings (the ratio
case runs on actual 10-K figures, so a skeptical colleague can check every
number). Author a company when the data a real one would need is internal and
never disclosed (nobody publishes weekly machine hours). Never borrow a
colleague's own exhibits without asking; credit courses by code, and claim no
endorsement.

## What the student must never receive

The answer key, the taxonomy, the claim verdicts, and the corrections are the
marking scheme. They live in source, gated fail-closed (see
`skills/fail-closed-gates/`), and every surface a student can reach is covered
by a leakage test (see `skills/leakage-tests/`). The reveal shows WHICH
figures are wrong and WHY conceptually, never the verified values, or the
repair step becomes copy-typing.

---

<!-- The body above this line is the upstream skill, verbatim and unmodified.
     Only the frontmatter description was widened, so the skill is found from
     ordinary phrasing rather than by name. Everything below is a local addition.
     Upstream: github.com/shaoxy123-design/ai-class-workflow-kit (MIT). -->

## Local addition: building the case

The rules above decide **what the case should contain**. Two further things are
needed before one exists, and they are in the file next to this one:

- **`BUILDING.md`** — the order the parts must run in (critique before
  instruction, then repair), and how to build the folder: generate both
  notebooks from one script, make that script print checks and refuse to pass,
  and publish by whitelist so the marking scheme never ships.
- **`scripts/new_case.py`** — inspects a course repository, reports the
  conventions it already follows, and scaffolds a case that matches them.

Read `BUILDING.md` once the design questions above are settled.

**One name change.** The body above refers to `skills/fail-closed-gates/`
and `skills/leakage-tests/`, which is correct in the upstream kit. In this
package those two are merged into a single skill, **`safe-to-publish`** —
same two patterns, one file. The upstream text is left exactly as written.
