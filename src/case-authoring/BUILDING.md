# Building a productive-failure case

A companion to `SKILL.md`. That file decides what the case should contain; this
one turns the decision into a folder that runs. Read it second.

*Local addition. Not part of the upstream AI_class workflow kit.*

## The order the parts must run in

The sequence is the pedagogy, not a presentation choice:

1. Student receives the brief, the data, and the AI's confident answer.
2. Student marks each claim sound or problematic, **with no teaching yet**, and
   commits that answer.
3. Only then is the concept taught.
4. Student repairs the analysis: says what it can and cannot support.

If the teaching comes first the case becomes a recall test. If the commitment
can be revised afterwards, the reveal quietly rewrites what the student thought.
**Make the commit one-way** — the cell that writes it should refuse to overwrite
an existing file.

## Step 1 — Look at where it has to land

If there is an existing course folder or repository, read it before writing
anything:

```
python scripts/new_case.py --inspect ./their_repo
```

A case that does not match the repo it lands in is not usable, whatever else it
is. Look for: paired `_student` and `_full` versions, folders named by module
or session, whether data sits in its own folder, whether the deliverable is a
CSV with a `sample_submission` template, whether data loads from raw URLs so it
runs with no setup. **Follow what you find. Do not impose a tidier structure.**

## Step 2 — Ask what you cannot infer

1. **Do these students program?** If they do not, every blank is a decision
   written as a number or a sentence, never a line of code they must get
   syntactically right. Give them the arithmetic; take their judgement.
2. **What must they be able to do afterwards that a tool cannot do for them?**
3. **How long, and is it marked?**

## Step 3 — The folder

```
Case_<n>_<topic>/
  README.md                    what it teaches, how long, what to hand in
  <topic>_student.ipynb        the one students get
  dataset/                     the data, generated not invented
  sample_submission.csv
  check_submission.py
  build_case.py                regenerates everything
  _instructor/                 NEVER published
    <topic>_full.ipynb
    answer_key.md
```

**Keep the marking scheme in its own folder**, so publishing is a decision
about a directory rather than a decision about each file. A student notebook
and its answers sitting side by side get published together eventually.

**Generate the notebooks from a script.** One `build_case.py` emits the student
and instructor versions from the same source, so they cannot drift, and the
numbers rotate next year by changing constants at the top.

**Have the build script check itself and refuse to pass.** Print the facts the
case depends on — the fit that must beat another, the total that must tie, the
claim that must stay arithmetically true — and say clearly when one fails. A
case whose trap does not work reads perfectly well and is silently useless.
This is the most common way a generated case ships broken.

## Step 4 — Shape the notebook

Alternate markdown and code, in the order the design demands: brief, the AI's
answer, critique, commit, reveal, repair.

- **Setup cell** loads data and defines every helper, marked "run this, do not
  change it". Data loads from the folder if present, falls back to a URL.
- **Blanks are decisions.** `CLAIM_3 = None  # sound / problematic` with a hint.
  Follow each with a check cell that handles `None`, so the notebook runs top to
  bottom before anything is filled in.
- **Replay a captured response; never call a model live.** Paste real output in
  as text. The case must run with no key, no account and no internet, in a room
  with bad wifi, three years from now when that model is gone.
- **The checking cell reports, it does not conclude.** Let it print the awkward
  numbers — the value at zero activity, the prediction outside the range — and
  stop. A script that announces PASS or FAIL does the exact thing the case
  teaches students not to accept.
- **The commit is one-way.** Once part one is submitted, it cannot be edited.
  Otherwise the reveal quietly rewrites history.

## Step 5 — Machine-check only what a machine can check

`check_submission.py` verifies format, completeness, and any arithmetic with
one right answer. Then it must **say plainly that it has judged nothing else**.

Never let a script mark reasoning. Beyond being unreliable, it teaches students
that judgement is something a machine settles, which is the opposite of the
point.

## Step 6 — Publish by whitelist

Publish a list of files, never a folder. Refuse anything matching `*answer*`,
`*full*`, `*solution*`, `*key*`, or anything under `_instructor/`. Before
deploying, grep the published output for two or three verified values; if any
appears, do not deploy. A page that is merely unlinked is still reachable by
anyone who edits a URL.

See `leakage-tests` for the full pattern and `fail-closed-gates` for making the
publish step refuse rather than warn.

## What to hand back

The folder, plus three sentences on what a person still has to decide: which
failure to plant, whether the claims are ones real students would argue about,
and the marks.

## Common failures

- **More than one concept.** The commonest, and the one that ruins a demo.
- Teaching before the critique, which turns the case into a recall test.
- A trap that does not work — only a printed check catches this; reading never does.
- Every claim problematic, so flagging everything scores full marks.
- Blanks that need code from students who do not program.
- Hand-written notebooks that drift apart from each other.
- Marking judgement with a script.
- Publishing the folder rather than a list of files.

---

*Local addition to the upstream kit, written from building one case end to end.
The rules in `SKILL.md` are upstream and unmodified.*
