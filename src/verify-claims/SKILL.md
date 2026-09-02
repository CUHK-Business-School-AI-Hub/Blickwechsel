---
name: verify-claims
description: Check every citation and number in a draft using a verifier that never sees the draft. Use when someone says "verify my citations", "check these numbers against the source", "fact-check this section", or before publishing anything that quotes a source or states a figure it did not just compute. Extracts the checkable claims, asks an independent fresh-context check on each, and reports PASS, PARTIAL or FAIL with a severity. Also use before handing out teaching material that cites research, quotes a filing, or prints a number a student could look up.
---

# Verify claims

The model that wrote a claim is never the authority on whether that claim is
correct. This skill checks a draft's citations and numbers with a verifier that
**never sees the draft**, because an assistant that helped write a sentence
cannot impartially confirm it — it will recognise its own phrasing and agree.

Invented and misattributed references are the characteristic failure of these
tools in academic work, and they cost more socially than a wrong number.

## The procedure

1. **Read the draft.** If no path was given, ask for one.

2. **Extract the checkable claims.** Number them. Four kinds:
   - citations — author, title, year, venue, and any DOI or identifier
   - attributed findings — "Smith (2019) shows…", "the standard requires…"
   - numbers — coefficients, sample sizes, dates, totals, percentages
   - named entities — companies, standards, institutions, people

   Scope it if asked: citations only, or numbers only.

3. **Write one verification question per claim**, worded so it does not carry
   the draft's framing. Not "confirm that Smith (2019) found X" but "what did
   Smith (2019) find about X?" The first invites agreement; the second asks a
   question.

4. **Gather the source for each claim without bundling the draft.** For a
   number, find the file, table or run output it should trace back to. For a
   citation, nothing is needed — the verifier looks it up.

5. **Fork a fresh verifier.** Dispatch a sub-agent with **only** the numbered
   questions and the source material. Never pass the draft prose. Batch related
   claims and run independent batches at the same time.

   If sub-agents are not available in the current setup, do the next best thing
   and say which you did: open each source yourself and answer the questions
   from the source before re-reading the draft. Say plainly that the check was
   not independent.

6. **Classify each claim.**
   - **PASS** — confirmed by the source.
   - **PARTIAL** — substantively right but imprecise: a rounded figure, a year
     off by one, a paraphrase that overstates.
   - **FAIL** — contradicted by the source, fabricated, stitched together from
     two real sources, or impossible to verify.

7. **Assign severity.** A citation that does not exist, or a number that
   contradicts its source, is **HIGH** and should block publication until fixed
   or explicitly overridden. A PARTIAL is **MEDIUM**. Report all claims,
   including the ones that passed.

8. **Never quietly downgrade.** A claim you could not verify is UNVERIFIED. It
   is not "probably fine". Say so in the report and leave it to a human.

## What to report

```
VERIFIED: 14 PASS / 3 PARTIAL / 2 FAIL   (of 19 claims)

FAIL (HIGH)     #7   "Vendrell (2026), Computers and Education: AI"
                     — no record of this article in that journal for 2026
                     — closest match is a different venue; check the source

FAIL (HIGH)     #12  "cuts shipping cost by 10-40%"
                     — the cited article says 10-25%
                     — correct the figure or change the citation

PARTIAL (MED)   #3   "twelve weeks of data"
                     — the file has thirteen rows; one is the added week
UNVERIFIED      #16  no source was supplied for this figure

PASS            #1, 2, 4-6, 8-11, 13-15, 17-19
```

Write the report where the person can keep it, and print the summary.

## When to run it

Before publishing anything that cites a source or states a figure it did not
just compute: a lecture that quotes research, a case built on a real company's
filings, a memo to a committee, a paper section, a reading list.

Especially before anything goes in front of students. A fabricated citation in
teaching material is repeated by thirty people who trust it.

## Two failure modes to avoid

**Showing the verifier the draft.** It will agree with it. The independence is
the entire mechanism; without it this is proofreading.

**Verifying the claims you doubt.** Extract them mechanically and check all of
them. The ones that feel solid are where a fabrication hides, because they read
smoothly — that is why they were written.

---

*Chain-of-Verification. Adapted from the AI_class workflow kit, which carries
this pattern from its author's research-workflow library. Reworked here to
stand alone, without the kit's bundled agent definitions or slash commands.*
