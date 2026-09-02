#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_case.py - inspect a course repository, then scaffold a case that matches it.

Two modes:

  --inspect PATH     report the conventions the repository already follows,
                     so a new case can be built to fit rather than to fight it

  --new NAME         create the case folder, in those conventions, with a
                     build_case.py that generates the notebooks and checks itself

The scaffold is deliberately a working skeleton, not an empty one: it builds two
notebooks, writes a dataset, prints its own checks, and runs. Replace the content;
keep the shape.

Usage:
    python new_case.py --inspect ./course_repo
    python new_case.py --new cost_behaviour --into ./course_repo --topic "Cost Behaviour"

No dependencies. On Windows use  py -X utf8  rather than  python.
"""

import argparse
import csv
import json
import os
import re
import sys

SKIP_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", "node_modules", ".venv"}


# ------------------------------------------------------------------ inspect
def inspect(root):
    names, exts, notebooks = [], {}, []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        names += dirnames + filenames
        for fn in filenames:
            e = os.path.splitext(fn)[1].lower() or "(none)"
            exts[e] = exts.get(e, 0) + 1
            if e == ".ipynb":
                notebooks.append(os.path.relpath(os.path.join(dirpath, fn), root))
    joined = " ".join(names)

    student_suffix = None
    for s in ("_student_version", "_students", "_student"):
        if re.search(re.escape(s) + r"\b", joined, re.I):
            student_suffix = s
            break
    full_suffix = None
    for s in ("_full_version", "_full", "_solution", "_answers"):
        if re.search(re.escape(s) + r"\b", joined, re.I):
            full_suffix = s
            break

    data_dir = None
    for d in ("dataset", "datasets", "data"):
        if re.search(r"\b" + d + r"\b", joined, re.I):
            data_dir = d
            break

    group = None
    m = re.search(r"\b(Module|Session|Week|Unit|Lecture)[ _-]?\d", joined, re.I)
    if m:
        group = m.group(1)

    colab = False
    for nb in notebooks[:40]:
        try:
            with open(os.path.join(root, nb), encoding="utf-8") as f:
                head = f.read(200000)
            if "raw.githubusercontent" in head:
                colab = True
                break
        except Exception:
            pass

    return {
        "root": os.path.abspath(root),
        "file_types": dict(sorted(exts.items(), key=lambda kv: -kv[1])),
        "notebooks": len(notebooks),
        "student_suffix": student_suffix,
        "full_suffix": full_suffix,
        "paired_versions": bool(student_suffix and full_suffix),
        "data_folder": data_dir,
        "grouping_word": group,
        "deliverable_csv": bool(re.search(r"(deliver|submission|submit)[\w-]*\.csv", joined, re.I)),
        "loads_from_raw_url": colab,
        "has_license": bool(re.search(r"\bLICEN[SC]E\b", joined, re.I)),
        "readme_languages": sorted(set(re.findall(r"README-([A-Za-z]{2})\.md", joined))),
    }


def report(c):
    print("=" * 68)
    print("CONVENTIONS IN %s" % c["root"])
    print("=" * 68)
    print()
    print("  notebooks found            %d" % c["notebooks"])
    print("  student version suffix     %s" % (c["student_suffix"] or "none found"))
    print("  instructor version suffix  %s" % (c["full_suffix"] or "none found"))
    print("  data folder                %s" % (c["data_folder"] or "beside the notebook"))
    print("  folders grouped by         %s" % (c["grouping_word"] or "nothing obvious"))
    print("  deliverable is a CSV       %s" % ("yes" if c["deliverable_csv"] else "no"))
    print("  data loads from a URL      %s" % ("yes - runs in Colab" if c["loads_from_raw_url"] else "no"))
    print("  licence file               %s" % ("yes" if c["has_license"] else "no"))
    if c["readme_languages"]:
        print("  README translated into     %s" % ", ".join(c["readme_languages"]))
    print()
    print("Build the new case to match these. Do not tidy them up.")
    if not c["paired_versions"]:
        print()
        print("Note: no student/instructor pair found. Worth introducing one - a single")
        print("notebook holding both the task and the answers always leaks.")
    print()


# ---------------------------------------------------------------- scaffold
BUILD = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_case.py - generate the {topic} case.

One source of truth. Emits the student notebook, the instructor notebook and the
data, then prints checks that must pass before the case is fit to teach.

Usage:  python build_case.py
"""

import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "{data_dir}")

# ------------------------------------------------------------- source data
# Replace with the real numbers. Keep them here, not in the notebook, so the
# case can be rotated for the next year group by editing this block alone.
ROWS = [(1, 10, 100), (2, 20, 180), (3, 30, 275), (4, 40, 350)]
HEADER = ["id", "driver", "outcome"]


def md(t):
    return {{"cell_type": "markdown", "metadata": {{}},
            "source": t.strip("\\n").splitlines(keepends=True)}}


def code(t):
    return {{"cell_type": "code", "execution_count": None, "metadata": {{}},
            "outputs": [], "source": t.strip("\\n").splitlines(keepends=True)}}


def cells(full):
    def blank(name, given, hint):
        val = given if full else "None"
        if len(val.splitlines()) > 1:
            val = "(" + val + ")"
        return "%s = %s   # %s" % (name, val, hint)

    C = []
    C.append(md("""
# {topic}

**Time:** about 60 minutes. You will not write any code - every box you fill in
is a decision, written as a number or a short sentence.

Say here what the student is, what they have been given, and what they hand in.
"""))
    C.append(code(@@@
# ---- Setup. Run this cell. Do not change it. ----
import csv, os, urllib.request

RAW_URL = "https://raw.githubusercontent.com/USER/REPO/HEAD/{data_dir}/data.csv"

def load(name="data.csv"):
    for p in (name, os.path.join("{data_dir}", name), os.path.join("..", "{data_dir}", name)):
        if os.path.exists(p):
            with open(p, newline="", encoding="utf-8-sig") as f:
                return list(csv.DictReader(f))
    with urllib.request.urlopen(RAW_URL) as r:
        return list(csv.DictReader(r.read().decode("utf-8-sig").splitlines()))

rows = load()
print("Loaded %d rows." % len(rows))
@@@))
    C.append(md("""
---
## Part 1 - do it yourself first

**No AI for this part.** Short, unaided, and the floor everything later is
checked against.
"""))
    C.append(code(blank("ANSWER_1", "42", "your answer, as a number")))
    C.append(code(@@@
if ANSWER_1 is None:
    print("Fill in the cell above, then run this again.")
else:
    print("correct" if abs(ANSWER_1 - 42) < 0.5 else "not right - check which rows you used")
@@@))
    C.append(md("""
---
## Part 2 - a decision no calculation settles

The most useful part of any case. State what you would go and find out.
"""))
    C.append(code(blank("DECISION", '"investigate"', "keep / correct / investigate")))
    C.append(md("""
---
## Part 3 - would you sign it?

Paste a real tool output below as text. Every number in it must be correct, and
say so, or students spend the hour recalculating instead of judging.
"""))
    C.append(code('print("""\\n  ... captured analysis goes here ...\\n""")'))
    C.append(code(@@@
# This cell asks the analysis two awkward questions and prints the answers.
# It does NOT say pass or fail. That is the student's job.
print("Question 1. ...")
print("Question 2. ...")
@@@))
    C.append(code("\\n".join([
        blank("SIGN_OFF", '"no"', "yes / no / conditional"),
        blank("MAIN_PROBLEM", '"..."', "two or three sentences"),
    ])))
    C.append(md("""
---
## Hand in

Run the next cell, then `python check_submission.py submission.csv`.
"""))
    C.append(code(@@@
import csv
fields = [("ANSWER_1", ANSWER_1), ("DECISION", DECISION),
          ("SIGN_OFF", SIGN_OFF), ("MAIN_PROBLEM", MAIN_PROBLEM)]
missing = [k for k, v in fields if v is None or (isinstance(v, str) and not v.strip())]
if missing:
    print("Not finished. Still empty: %s" % ", ".join(missing))
else:
    with open("submission.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["field", "answer"]); w.writerows(fields)
    print("Wrote submission.csv")
@@@))
    return C


def main():
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(HEADER); w.writerows(ROWS)

    for full, name in ((False, "{slug}{student}.ipynb"), (True, "{slug}{fullsuf}.ipynb")):
        nb = {{"cells": cells(full),
              "metadata": {{"kernelspec": {{"display_name": "Python 3",
                                          "language": "python", "name": "python3"}},
                           "language_info": {{"name": "python"}}}},
              "nbformat": 4, "nbformat_minor": 5}}
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print("wrote %s" % name)

    # ---------------------------------------------------------------- checks
    # Replace these with the facts your case actually depends on: a fit that
    # must beat another, a total that must tie, a defect that must be findable.
    print()
    print("CHECKS")
    ok = len(ROWS) >= 4
    print("  enough rows to fit anything: %s" % ok)
    print("  %s" % ("all checks pass" if ok
                    else "*** CHECKS FAILED - do not teach this ***"))


if __name__ == "__main__":
    main()
'''

CHECK = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_submission.py - check the shape of a submission, and nothing else.

It verifies the format, that nothing is missing, and any arithmetic with one
right answer. It deliberately says nothing about the quality of the reasoning.
No script can mark that, and one that pretended to would teach students the
wrong lesson.
"""

import csv, os, sys

REQUIRED = ["ANSWER_1", "DECISION", "SIGN_OFF", "MAIN_PROBLEM"]
WRITTEN = {"MAIN_PROBLEM": 20}
CHOICES = {"DECISION": {"keep", "correct", "investigate"},
           "SIGN_OFF": {"yes", "no", "conditional"}}


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "submission.csv"
    if not os.path.exists(path):
        sys.exit("Cannot find %s. Run the last cell of the notebook first." % path)
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    ans = dict((r[0].strip(), (r[1] if len(r) > 1 else "").strip())
               for r in rows[1:] if r)

    problems = []
    for k in REQUIRED:
        if not ans.get(k):
            problems.append("missing or empty: %s" % k)
    for k, opts in CHOICES.items():
        v = ans.get(k, "").lower()
        if v and v not in opts:
            problems.append("%s must be one of: %s" % (k, ", ".join(sorted(opts))))
    for k, n in WRITTEN.items():
        if ans.get(k) and len(ans[k].split()) < n:
            problems.append("%s is shorter than the rubric expects" % k)

    print("SUBMISSION CHECK - %s" % os.path.basename(path))
    if problems:
        for p in problems:
            print("  x  %s" % p)
    else:
        print("  ok  format is right, nothing missing")
    print()
    print("This script has judged nothing about your answers. A person marks those.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
'''

README = """# {topic}

A runnable case. Students open the notebook and work through it; they write no code.

## What's here

- `{slug}{student}.ipynb` - hand this out
- `{slug}{fullsuf}.ipynb` - the same notebook with answers filled in
- `{data_dir}/` - the data
- `sample_submission.csv` - the shape of the deliverable
- `check_submission.py` - machine check for format and arithmetic only
- `answer_key.md` - marking guidance, instructor only
- `build_case.py` - regenerates the notebooks and the data

## Running it

No installation and no API key. To rebuild with different numbers, edit the
source block at the top of `build_case.py` and run it. It prints checks that must
pass before the case is fit to teach.

## Still to decide

- which flaw goes in the final part, and whether to rotate it each year
- whether each wrong option is one real students actually give
- the marks
"""

KEY = """# {topic} - answer key

Instructor only. Do not share before the class.

## Machine-checked

| Field | Answer |
|---|---|
| `ANSWER_1` | 42 |

## Marked by a person

| Field | Full credit | Partial | Why |
|---|---|---|---|
| `DECISION` | | | |
| `SIGN_OFF` | | | |
| `MAIN_PROBLEM` | | | |

## Wrong answers to expect

Fill this in before teaching it. Marking is an argument without it. The most
common wrong answer is usually whichever check students were taught most recently.

| Objection | Verdict | Credit |
|---|---|---|
| | | |

## Do not deduct for

List what the analysis genuinely gets right, so nobody loses marks for failing
to object to it.
"""


def scaffold(name, into, topic, conv):
    slug = re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
    folder = os.path.join(into, slug)
    if os.path.exists(folder):
        sys.exit("%s already exists. Pick another name or delete it first." % folder)
    os.makedirs(folder)

    fmt = {"topic": topic or name.replace("_", " ").title(),
           "slug": slug,
           "student": conv["student_suffix"] or "_student",
           "fullsuf": conv["full_suffix"] or "_full",
           "data_dir": conv["data_folder"] or "dataset"}

    for fn, body in (("build_case.py", BUILD), ("check_submission.py", CHECK),
                     ("README.md", README), ("answer_key.md", KEY)):
        with open(os.path.join(folder, fn), "w", encoding="utf-8") as f:
            text = body if fn == "check_submission.py" else body.format(**fmt)
            f.write(text.replace("@@@", chr(39) * 3))

    with open(os.path.join(folder, "sample_submission.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["field", "answer"])
        for k in ("ANSWER_1", "DECISION", "SIGN_OFF", "MAIN_PROBLEM"):
            w.writerow([k, ""])

    print("Created %s" % folder)
    for fn in sorted(os.listdir(folder)):
        print("   %s" % fn)
    print()
    print("Matching this repo: student suffix %s, instructor suffix %s, data in %s/"
          % (fmt["student"], fmt["fullsuf"], fmt["data_dir"]))
    print()
    print("Next:  cd %s  &&  python build_case.py" % folder)
    print("Then replace the placeholder content. Keep the shape:")
    print("  - every blank is a decision, not a line of code")
    print("  - one part that no calculation settles")
    print("  - an audit at the end where every number is correct")
    print("  - build_case.py prints checks and refuses to claim success when one fails")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inspect", metavar="PATH")
    ap.add_argument("--new", metavar="NAME")
    ap.add_argument("--into", default=".")
    ap.add_argument("--topic", default=None)
    args = ap.parse_args()

    if args.inspect:
        if not os.path.isdir(args.inspect):
            sys.exit("Not a folder: %s" % args.inspect)
        report(inspect(args.inspect))
        return
    if args.new:
        conv = inspect(args.into) if os.path.isdir(args.into) else {
            "student_suffix": None, "full_suffix": None, "data_folder": None}
        scaffold(args.new, args.into, args.topic, conv)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
