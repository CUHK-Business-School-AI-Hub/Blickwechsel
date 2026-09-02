# Roadmap

What the seven stages are, the order they run in, where they came from, and
what is missing.

## The map

One skill. `SKILL.md` routes; each stage is a file in `reference/` that loads
only when the request needs it.

```
                          guardrails.md
                  (the rules every other stage assumes)
                                 |
   ┌─────────────────────────────┼─────────────────────────────┐
   │                             │                             │
UNDERSTAND                    CHANGE                        CHECK
   │                             │                             │
 audit.md    ──────────►    rebuild.md                    verify.md
(what is really in it,      (activities, data,          (citations, numbers)
 facts before advice)        notes, exam items,
                             the slide file)              publish.md
                                 │                      (a gate that refuses,
                    ┌────────────┴────────────┐          a whitelist for what
                    │                         │          may cross the line)
              activities.md              case.md
            (28 formats to             (a case students
             choose between)            run, and the folder
                                        that makes it work)
```

## The order they run in

**1. `guardrails.md` — before anything.** Not a step so much as the standing
rules: tell the model what it cannot see, ask instead of assuming, facts before
advice, ask for the generator rather than the answer, keep authorship of what
is said out loud. Every other stage assumes these, and it answers on its own
when the question is only about working with AI.

**2. `audit.md` — understand what exists.** Establishes the topic and the core
objective first, then measures the file, then reads it back from a student's
side. Takes PowerPoint, PDF, LaTeX, notebooks or a whole folder. Everything it
says is labelled measured, inferred or assumed, and everything assumed becomes
a question for the lecturer. Suggestions only at the end.

**3. `rebuild.md` — change it.** Activities where students commit to an answer,
datasets that rotate each year, speaker notes, replacement exam items, and the
slide file itself. Picks formats from `activities.md`, and hands the audit
exercise to `case.md` rather than designing it inline.

**4. `case.md` — build something students run.** The design rules first: one
concept, data authored so untaught errors cannot happen, the failure in the
conclusion rather than the arithmetic, claims that are not all problematic.
Then the folder that makes it run.

**5. The two checks — before any of it reaches anyone.** `verify.md` for
citations and figures; `publish.md` for the gate between authored and published
and for whitelisting what may cross a boundary.

You can stop after any stage. Each produces something usable on its own.

## Where each came from

| Stage | Origin |
|---|---|
| `audit.md` | Written here. Drives `read_material.py` (pptx, pdf, tex, ipynb, folders). |
| `rebuild.md` | Written here. Drives `make_variants.py` and `check_deck.py`. |
| `activities.md` | Written here. |
| `case.md` | **Design rules upstream, verbatim,** above a marked fence the build never rewrites. [ai-class-workflow-kit](https://github.com/shaoxy123-design/ai-class-workflow-kit), MIT, © 2026 Shao Xinyuan. The building half and `scripts/new_case.py` are local additions. |
| `verify.md` | Adapted from upstream — reworked to stand alone without the kit's bundled agent definitions and slash commands. |
| `publish.md` | Merges upstream's `fail-closed-gates` and `leakage-tests`, which shared most of their trigger vocabulary, plus a section for material that lives as files rather than as an application. |
| `guardrails.md` | Written here, with four rules sharpened by upstream's discipline. |

`UPSTREAM-LICENSE` holds the MIT licence those parts derive from.

## How it is built

The seven stages live as six source folders under `src/`. `build_package.py`
assembles them into `teaching-with-ai/`, rewriting every cross-reference the
merge invalidates, and refuses to ship if the routing is broken. See **Working
on it** in `README.md`.

**Never edit `teaching-with-ai/`.** It is rebuilt from scratch on every run, so
a change made there is deleted by the next build. Every file in it says so at
the top, and a GitHub Action fails the push if the committed skill does not
match what `src/` produces.

## Two open decisions

**Vendor the kit whole, or keep adapting it?** The checking stages are currently
*adapted*: upstream's versions reference bundled agent files, a `/commit` gate
and `quality_reports/` paths that do not exist outside the kit, so as standalone
skills they would dangle. Adapting keeps them working; it also means upstream
fixes have to be merged by hand.

The alternative is to drop the whole `.claude/` kit into a project alongside
this skill. Then the upstream versions work as written, and you get the scout /
builder / verifier agent roles and the always-on project rules that a portable
skill cannot provide. That is the better answer for anyone building software
with agents. It is worse for a colleague who only has claude.ai.

**Should `new_case.py` exist at all?** It is the one script that does not match
the public pattern — upstream's case skill is markdown only, and scaffolding a
folder is a convenience rather than something a model cannot do. Kept for now
because the convention-detection is what makes a case droppable into somebody
else's course.

## Gaps

**Five of the seven stages have no prompt version.** The prompts on the workflow
page cover the audit (Workflow A) and the rebuild (Workflow B). Anyone working
without Claude gets the course revamp and nothing else — no case design, no
citation checking, no publish gate, no leakage pattern.

**The audit prompt is narrower than its stage.** Workflow A1 says "here is my
lecture file" and asks only about slides. The audit now handles PDF and LaTeX as
well, establishes the objective before counting, and produces a question list —
none of which the prompt version does.

**Nothing covers assessment design end to end.** The rebuild's Step 6 rewrites
individual questions. Nothing helps with a whole assessment structure, which is
the thing most likely to need departmental agreement.

**Nothing knows about a syllabus.** Everything starts from a lecture, a notebook
or a case. A course-level view — coverage, sequencing, where an objective is
taught versus assessed, which is what assurance of learning asks for — is the
obvious next one. Designed but deliberately not built: it needs a real syllabus
to test against, and building it against an imagined one is how the quantitative
bias got in the first time.

**It leans quantitative, and the code shows it.** `make_variants.py` handles a
single numeric driver. Strategy, organisational behaviour, law and ethics get
the method and none of the tooling.

**`verify.md` has never been run on this package's own output.** It is the one
stage with no worked example, which is a poor advertisement for a check.

**Tested on one lecture, by its author.** The weakest kind of evidence. A pilot
with three colleagues from different disciplines should come before any wider
release.

## What would come next, in order

1. **Pilot with three colleagues**, one of them from a non-quantitative
   discipline. That is where it will break, and three is recoverable where
   sixty is not.
2. **Prompt versions for the stages that lack them**, so the no-Claude path
   covers the same ground. About an hour.
3. **Widen the A1 prompt** to match what `read_material.py` now reads.
4. **A course-level stage** — designed, not built. Needs a real course outline.
5. **A non-numeric variant generator**, which is what the qualitative
   disciplines need before any of this is much use to them.

## Installing

One zip: `zips/teaching-with-ai.zip`. One upload on claude.ai, or unzip into
`~/.claude/skills/`. See `README.md`.
