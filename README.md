# BLICKWECHSEL

*A change of perspective — your lecture seen from where the student sits.
The best thing in it is usually not in the file.*

---

## It does not rewrite your lecture

Ask an AI to improve a lecture and you get something back that is tidy,
confident, plausible, and quietly worse. Not because it invented a fact. Because
it smoothed out the demonstration you always do on the tablet, merged the slide
you spend ten minutes on with the one you skip, and deleted the story you tell
every year — none of which were written down anywhere it could see.

This skill is built around that failure. It looks first, says what it measured
and what it guessed, asks you about the parts it cannot see, and only then
proposes anything. You keep every decision that matters.

> Everything it says is labelled **measured**, **inferred**, or **assumed**, so
> you can tell at a glance which of its claims survive if it misunderstood your
> subject.

## It looks before it suggests

The first thing it does is count. It opens PowerPoint, PDF, LaTeX, notebooks or
a whole course folder and reports what is actually there: how many slides repeat
the one before, which questions are asked with no way to answer them, which
slides carry more words than anyone can read and listen to at once, and how much
of a notebook the student actually writes rather than watches.

Then it reads the whole thing again as somebody who does not yet know the
answer. Where would I first get lost? What am I assumed to already know? What
can I do at the end that I could not do at the start?

Only after that does it propose anything — numbered, so you can accept or reject
each one, with a reason recorded for every rejection.

## It assumes your students already have an AI

Not that they might. That they do.

So a rule telling them not to use one is never treated as a control. Instead it
sorts your learning objectives by a blunt question — *could a student produce a
passing answer to this in under five minutes with an AI assistant?* — and shows
you the ratio of slides serving the objectives where the answer is yes against
the ones where it is no. In most material that single number carries the whole
argument for change.

Then it helps you build the other kind of task: give the student a finished
piece of work and ask them to decide whether to accept it, and why.

## Begin in three steps

### 1. Install it once

Take `teaching-with-ai.zip` from the [latest release](../../releases/latest).

> The project is **Blickwechsel**; the skill inside it is **`teaching-with-ai`**.
> That is the name you will see in your skills folder, and the one to say
> if you want a colleague to install it.

On **claude.ai**, go to Settings, Capabilities, Skills, and upload it. One
upload, nothing to choose.

In **Claude Code**, unzip it into your skills directory and restart:

```
unzip teaching-with-ai.zip -d ~/.claude/skills/
```

Or clone this repository and copy the skill folder across:

```
git clone https://github.com/CUHK-Business-School-AI-Hub/Blickwechsel
cp -r Blickwechsel/teaching-with-ai ~/.claude/skills/
```

Copy **`teaching-with-ai/` only**. `src/` is what that folder is built from, and
installing it instead gives you six half-skills that do not route.

On Windows the skills folder is `C:\Users\<you>\.claude\skills`.

### 2. Give it the file you already have

Not a rewritten one. The actual deck you taught from last term, however untidy.
It reads `.pptx`, `.pdf`, `.tex`, `.ipynb`, and whole folders.

### 3. Say what you want in ordinary words

You never name a stage or a command:

> "Here is my lecture from last term. What should I change about it?"

> "Turn this into something students can run and get their hands dirty with."

> "I need a version of this dataset with different numbers for next year."

> "Can I use AI to draft my marking scheme?"

## It asks you things, but not many

Anything it needed and did not have becomes a question — and the questions come
**last**, after the findings, in a table with three columns: what it assumed,
why, and what changes if the assumption is wrong.

That last column is the point. It tells you which rows are worth answering, and
lets you ignore the rest without blocking the work.

If you only answer one, it will tell you which: *what do you do in class that is
not on the slides?*

## Seven stages, and it loads only the one you need

| Stage | What it is for |
|---|---|
| **guardrails** | Working with an AI on academic work at all — what to check, what to disclose, which tasks never to hand over, and a red / yellow / green split for staff rather than students |
| **audit** | What the session is *for*, what is really in it, and where it falls short from a student's side |
| **rebuild** | Answers the findings you accepted. Activities, datasets that rotate each year, speaker notes, replacement exam questions, and edits to the slide file itself |
| **activities** | Twenty-eight classroom formats in eight families, offered two or three at a time so you choose |
| **case** | A case where students critique a deliberately weak AI answer before being taught the topic, then repair it |
| **verify** | Every citation and number checked by a verifier that never sees the draft |
| **publish** | A gate between authored and published that refuses rather than warns, so an answer key cannot leave with the handout |

## It argues with you, and here is the argument

This is not a neutral tool. It takes positions, and they are written into its
instructions:

- **Do not teach the tool, teach how to check its work.** Whatever tool you
  teach this year will be replaced.
- **Students do it by hand once before AI touches it.** You cannot audit an
  answer you have never produced.
- **Grade judgement, not production.** If an AI can produce the thing you are
  marking in thirty seconds, you are not marking anything useful.
- **Protect what already works**, especially the parts that are not written down.

If you disagree with any of that, say so and it will follow you. But you should
meet the argument here rather than discover it halfway through.

## What it is not

**It is for one session at a time.** A lecture, a workshop, a case. There is no
syllabus view, no sequencing, no map of where an objective is taught against
where it is assessed. That is the obvious next thing and it does not exist yet.

**It leans quantitative.** Strongest in accounting, finance, operations,
analytics and economics, where an analysis has numbers and a conclusion. Weaker
in strategy, organisational behaviour, law and ethics, where the right answer is
contested. The dataset generator only handles numbers at all.

**It has been tested on one lecture, by the person who wrote it.** That is the
weakest kind of evidence there is. Treat its early findings as a first draft, and
please say what was wrong.

## The scripts, and what happens without them

Four small Python scripts do the counting, the dataset generation, the slide
geometry check and the case scaffolding. Two need nothing but Python; reading a
`.pdf` also wants `pypdf`, and editing a deck wants `python-pptx`.

```
pip install pypdf python-pptx
```

**If you cannot run them, it still works.** Every stage says what to do instead,
and requires each hand-counted number to be labelled *inferred* rather than
*measured*. An estimated audit is useful. Estimates dressed as measurements are
not.

## If you want to change it

Edit `src/`. Never edit `teaching-with-ai/`.

```
teaching-with-ai/   what people install — generated, overwritten by every build
src/                the source: six folders and router.md
build_package.py    assembles one from the other
```

Run `python build_package.py`. It refuses to ship if the routing is broken — a
reference named but missing, one nothing routes to, a stale name pointing at a
folder that no longer exists, or a rewrite that stopped matching because
somebody changed the wording underneath it.

Every generated file opens with a line naming the source it came from, and a
GitHub Action fails the push if the committed skill is not what `src/` produces.
Otherwise the mistake is silent: you edit the generated copy, it appears to
work, and the next build deletes it.

## Credit

Parts of four stages come from the
[AI class workflow kit](https://github.com/shaoxy123-design/ai-class-workflow-kit)
by Shao Xinyuan, MIT licensed. The case design rules are that kit's file
verbatim, kept above a fence the build never rewrites.

## License

MIT. See `LICENSE`, and `UPSTREAM-LICENSE` for the parts deriving from the kit.
