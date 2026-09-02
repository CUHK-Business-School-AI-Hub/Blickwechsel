---
name: safe-to-publish
description: Decide whether teaching material is safe to put in front of people, and stop the marking scheme escaping. Use when a case, an answer key, a dataset, a handout or a whole site is about to become visible to students or colleagues, when someone asks whether a solution file could leak, or when a check "keeps getting ignored". Covers putting a deterministic gate between authored and published that refuses rather than warns, exporting by whitelist rather than filter, planting sentinels in everything that must not escape, and the version of both patterns for material that is just files rather than an application.
---

# Safe to publish

Two questions, and they are the same question at different distances.

**Is this correct enough to publish?** That is a gate: a check between authored
and published whose failure mode is refusal.

**Could the wrong part of it escape?** That is a whitelist: an explicit list of
what may cross the boundary, and a test that fires if anything else does.

Both fail the same way — quietly, through convenience, at the moment somebody
is in a hurry.

---

# Part one — the gate

A gate is a deterministic check that runs between authored and published, and
its failure mode is **refusal**, not a warning line in a log.

A warning that can be ignored eventually is.

## The pattern

**1. One command, exit non-zero on any blocker.** Whatever publishes the
material runs the check first and stops. In the project this came from, the
seeding command re-verifies every case and *unpublishes* any case with a
critical finding, and a separate preflight command refuses to call an instance
safe while anything would raise in front of an audience.

**2. Check before you write, not after.** A script that writes the files and
then prints "checks failed" has already published. Compute, check, and only
then write. If a check fails, say plainly that whatever is on disk is now out
of date and must not be handed out.

**3. Allow an override, and make it cost something.** A blocked build with no
way past it gets worked around. Require an explicit flag *and* a written
reason, so the override is on the record rather than a shrug.

**4. The gate owns the truth check, once.** Each rule has exactly one
implementation and nothing re-implements it. Two implementations of one rule
will eventually disagree, and the gap between them is where errors hide. If a
check needs to latch onto something, make the material carry it — a canonical
total at the end of every worked explanation — rather than writing a second
parser.

**5. Blockers, warnings and notes are different things.** A blocker stops
publication. A warning is true and worth acting on. A note is context.

The fatal design error is a check that always fails locally: it teaches
everyone to ignore the whole command. Scope each check to the environment where
it can actually be satisfied.

**6. Gate what is reachable, not what exists.** A retired, unpublished item must
not be able to block the whole instance. Nothing the audience cannot reach can
break in front of them. This shipped as a real defect before verification
caught it.

**7. Do not refuse on somebody else's mess.** If you are editing material you
did not write, separate what *this change* broke from what was already wrong.
A gate that blocks on a pre-existing problem is a gate people learn to ignore.

**8. Retire what you no longer author.** The publishing step should unpublish
anything whose source no longer contains it, so a superseded version cannot
linger because someone forgot to delete a row.

## What to gate, for teaching material with an answer key

- Every figure in the answer key agrees with the worked explanation beside it.
- Every sentence quoted as an AI's output is verbatim from the actual run.
- Every error signature is locally identifying — it can never accuse correct work.
- At least one authored claim is true, so flagging everything scores nothing.
- References and the error taxonomy are present and not empty.
- Nothing confidential is reachable — Part two.

For anything with computed figures the check that matters most is the boring
one: **recompute the numbers from source and compare them to what is printed.**
Most published errors are a stale figure, not a wrong method.

## The test for a good gate

Ask: *can a broken version of this reach the audience if a human forgets a
step?*

If yes, the gate is advisory, and advisory is decoration.

---

# Part two — what may cross the boundary

Confidential material almost never leaks through malice. It leaks through
convenience: a serializer that dumps the whole object, a template that loops
over every key, a folder published wholesale because it was easier than
choosing, a later "simplification" that replaces a careful whitelist with the
raw structure.

The defence is a test that fires on the **whole class** of mistake, not on one
instance of it.

## The pattern

**1. Export by whitelist, never by filter.** The code that builds the outbound
surface enumerates what may pass — these tables, these notes — rather than
stripping what may not. A blacklist fails open the day somebody adds a new
confidential field. A whitelist fails closed.

The same rule applies to folders. **Publish a list of files, not a directory.**

**2. Plant a sentinel in every field that must never escape.** Build the object
with a unique marker in each one, then assert that none of them appears in the
output:

```python
SENTINELS = {
    "answer_key":       "ANSWERKEY-SENTINEL",
    "claim_verdicts":   "VERDICT-SENTINEL",
    "corrections":      "CORRECTION-SENTINEL",
    "screening_lesson": "SCREENING-SENTINEL",
}
for field, marker in SENTINELS.items():
    self.assertNotIn(marker, response_body,
                     "%s leaked into the student surface" % field)
```

If someone later switches the export to a dump of the raw structure, every
assertion fires at once and the failure names the field.

**3. Test the values, not only the field names.** A second test asserts that no
verified answer value appears in the output, with a carve-out for values
legitimately part of the public brief. **Compute the carve-out from the brief**,
never hand-list it, or it rots the first time the brief changes.

**4. Order matters as much as content.** Where the teaching depends on students
committing before they see the verdict, enforce one-way stages and write a test
that walks the illegal transition and asserts it is refused. A page that is
merely not linked is still reachable by anyone who edits a URL.

## The test for coverage

Take each confidential field and ask: **which assertion fails if this one
leaks?** A field with no answer is an uncovered boundary.

---

# For material that is only files

Not everything has a test suite. A teaching case is usually a folder. The same
two patterns still apply, and a short script does both:

- Keep answer keys, full versions, marking schemes **and the build script** in a
  folder the publishing step never copies. A build script that carries the
  verdicts is part of the marking scheme, however technical it looks.
- Have the publish step hold an explicit list of what may go out, and refuse
  anything else **by name**, so a new file defaults to private.
- Refuse any filename matching `*answer*`, `*full*`, `*solution*`, `*key*`.
- Build sentinels from the answer key and the instructor copy — the verdicts as
  they are actually written — and search every publishable file for them.
- Exit non-zero, so the check can sit in front of a deploy.

A folder holding both `case_student.ipynb` and `case_full.ipynb`, published
whole, has leaked. The link does not need to exist for a student to find it.

## Where this fits

`case-authoring` produces the material both halves of this protect.
`verify-claims` checks the citations and figures a gate cannot settle by
arithmetic.

---

*Both patterns adapted from the [AI class workflow kit](https://github.com/shaoxy123-design/ai-class-workflow-kit)
by Shao Xinyuan, MIT licensed, where they are two separate skills. Merged here
because they share most of their trigger vocabulary and are one idea at two
distances, with a section added for teaching material that lives as files
rather than as an application.*
