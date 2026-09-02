---
name: ai-teaching-guardrails
description: How a teacher should work with an AI assistant on academic work, and how to check what it produces. Use whenever helping with teaching material, course design, marking schemes, assessment policy, or any academic writing where the person will put their name on the result. Covers what to tell the model before it starts, what to ask for rather than assume, how to keep it honest, how to check output too long to read, when to write plainly and when to keep the subject's technical vocabulary, how to check material from a student's point of view, how to design for students who all have AI, which tasks a teacher must never hand over, and how to set an AI policy for staff rather than students. Also use when someone asks whether they can trust an AI answer, how to check it, or what to disclose.
---

# Working with AI on teaching and academic work

Apply these whenever the person will put their name on the output. The `course-audit` and `course-rebuild` skills assume these rules; this skill states them, and stands on its own for anything else.

## Two rules underneath all the others

### A. Whatever you tell students about using AI applies to the teacher as well

If a course tells students to do the work by hand first, then audit the AI rather than outproduce it, then disclose what they used, the teacher cannot skip all three. Not because it is unfair — because it does not work. A lecture written by an AI is not owned by the person delivering it, and that shows the first time a student asks something off-script.

### B. Assume every student has an AI assistant, in everything they do

Not "might have". Has. Design from that assumption, and two things follow.

**A ban is never a control.** If part of a course is meant to be done without AI, its integrity has to come from the design — done in the room, on data the student has not seen before, with a short closed-book piece at the end — never from an instruction and an honour system. Write the rule anyway, because it tells students what the task is for. Just do not rely on it.

**Learning with AI is part of what you are teaching, not a threat to it.** Design tasks that make students better at using it: get an answer from it and find what is wrong with that answer; ask it for the strongest case against your own position; hand in the prompt alongside the output and explain why you asked it that way. The graduate worth producing is not the one who avoided the tool. It is the one who can direct it and catch it when it is wrong.

Both rules point the same way. Rule A stops the teacher outsourcing their judgement. Rule B stops the course pretending the tool is not there.

## Before the model starts

**1. Write down what it cannot see.** The model improves what is in front of it and quietly destroys everything else. What you do in the room that is not in the file. Why an odd thing is odd. What must not change. Say all of it before uploading anything.

**2. Say the shape before the content.** One page or ten. For whom. Tables or prose. This costs one sentence and prevents the expensive kind of mistake, which is not a wrong fact but a right answer in the wrong form.

**3. Decide which steps it must never touch — first.** Name them before you are short of time, because that is when they get negotiated away.

**4. Ask for what you need, and then do what was asked.** If something missing would change the output — how long the session is, who the students are, what is being assessed, whether the material is shared with other teachers — ask for it. Do not fill the gap with a sensible-looking assumption and carry on; a filled gap is invisible in the finished work.

And when your own view of the best approach differs from what the person asked for, say so once, briefly, then do what they asked. They know the room, the students and the department. A better answer to a different question is not useful.

## While it works

**5. Facts before advice.** Make it establish what is true before it recommends anything. Once it has proposed something, everything after is a defence of that proposal.

**6. Ask for the thing that makes the answer, not the answer.** A list of numbers from a model cannot be checked. A script that produces them can be run, read and rerun. The same goes for a marking scheme (ask for the principle), a dataset (ask for the generator), a reading list (ask for the selection rule). This is the highest-value habit on this page.

**7. Require sources, and require gaps.** "Cite where each claim comes from. Where you cannot tell, say so." The second half matters more. A filled-in gap looks exactly like a known fact.

**8. Never cite what has not been opened.** Invented and misattributed references are the characteristic failure of these tools in academic work, and they cost more socially than a wrong number. Open the source, or do not cite it. The `verify-claims` skill is the mechanism for this: it checks every citation and number with a verifier that never sees the draft.

**9. Plain English everywhere except the subject's own words.**

Write the wrapping plainly: instructions, briefs, speaker notes, rubrics, notes to colleagues, explanations of what changed and why. Short sentences. Ordinary words. If a colleague has to read a paragraph twice, rewrite it.

**Do not simplify the subject's vocabulary.** Relevant range, cost driver, sum of squared residuals, materiality, going concern, cut-off — students have to leave the course able to use these words, and an examiner, an employer and a professional body all expect them. Swapping a technical term for an everyday one is not clarity; it is quietly removing something the student came to learn.

The test: **if the word is part of what is being taught, keep it and define it once. If it is the packaging around the teaching, use the plain word.** "We merged the repeated slides" is packaging. "The estimate is only valid inside the relevant range" is the teaching.

**10. Check it from the student's side before you finish.**

Read everything back as somebody who does not yet know the answer. Ask:

- Do I know what I am supposed to do here?
- Can I actually answer this with what I have been given?
- Does this order make sense if I am meeting the idea for the first time, rather than revising it?
- If I get this wrong, does anything tell me why?

Most teaching material is written in the order the teacher already knows it, which is almost never the order a student learns it. This one pass catches the activity with no way in, the brief that assumes a file nobody sent, the question whose answer appeared two slides earlier, and the worked example that only makes sense if you already understand it.

Do this before showing the teacher, not after.

## Checking work too long to read

**11. Build a check that can fail.** Not "does this look right" but "what would tell me it is wrong?" A script that recomputes a published figure. A total that must match. A count that must reconcile. Reading is not review once the output passes a page or two. Where the material is about to be published to people who will trust it, make the check refuse rather than warn, and whitelist what may cross the boundary — see `safe-to-publish`.

**12. Spot-check the small numbers.** The headline claims are usually right or obviously wrong. The damage lives in the third decimal place, the cross-reference and the rounding. A confident document with one quiet inconsistency is the normal failure, not obvious nonsense.

**13. Ask what it changed that you did not ask for.** Make it list its own departures from the brief. A model that never reports any is either not making them or not telling you.

## Keeping it

**14. Keep the prompt, not the output.** The prompt is the asset and gets reused. The output is one term's material.

**15. Keep authorship of what is said out loud.** Let it draft the tables. Write the spoken lines yourself.

**16. Rotate rather than police.** Detecting AI use is a losing game, and rule B says not to try. Different numbers for each year group removes the problem instead of fighting it, and costs nothing once a generator exists.

## Red, yellow and green — for staff

The student version of this sorts by which skill is at risk. The staff version should sort by **whether you can check the output**, which is a different and more useful question.

**Red — do it yourself.**
The mark itself. Deciding what stays AI-free in a course. Identifiable student information in any tool not approved by the institution. The words said in the room. Signing off on any claim you have not opened and read.

**Yellow — it drafts, you decide.**
Wrong-answer options, dataset variants, question banks, speaker notes, first drafts of briefs, summaries of your own material. Every item needs a named human decision before it is used.

**Green — it does, and a check confirms it.**
Mechanical transformation, counting, reformatting. Scripts and generators. Finding inconsistencies in your own material. Anything whose correctness a test can confirm.

Green is defined by being checkable, not by being easy. A complicated job belongs in green if a test catches it going wrong. A simple one belongs in red if nothing but judgement can check it.

## Disclosure

If teaching material was produced with AI, say so, at least within the department. A rule that binds students and not staff stops being credible the moment it is noticed, and it will be noticed.

## When asked to do something in the red list

Say plainly that the decision is theirs, say why, and offer the nearest thing that helps — the evidence to decide with, the options laid out, the draft to react to. Do not simply refuse, and do not quietly do it anyway.
