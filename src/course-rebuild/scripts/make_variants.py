#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_variants.py - turn one teaching dataset into a set you can rotate.

Give it a CSV with a driver column and a cost column. It produces:

  base        the numbers you gave it, with the fits printed
  vN_shift    same shape, different numbers, one per year group
  outlier_real    an odd observation that is genuine  - keep it
  outlier_error   the SAME numbers, but caused by a data-entry mistake - fix it
  rival_driver    a second driver that fits better and causes nothing
  out_of_range    values past a step change, where the fitted line breaks

Every file comes with the fits printed so you can see what each one teaches.
No randomness: run it twice, get the same files.

Usage:
    python make_variants.py data.csv --x machine_hours --y cost
    python make_variants.py data.csv --shifts 4 --out ./variants
"""

import argparse
import csv
import json
import os
import re
import sys

# Fixed wobble sequences. Not random, so output is reproducible.
W1 = [3, -5, 2, 6, -4, 1, -2, 5, -3, 4, -6, 2, -1, 7, -7, 0, 4, -4, 2, -2]
W2 = [-2, 4, -6, 3, 5, -1, 2, -4, 6, -3, 1, -5, 7, -7, 0, 2, -2, 5, -5, 3]


def mean(v):
    return sum(v) / float(len(v))


def ols(xs, ys):
    n = len(xs)
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx if sxx else 0.0
    a = my - b * mx
    ssr = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    r2 = (1 - ssr / syy) if syy else 0.0
    return a, b, r2, ssr


def high_low(xs, ys):
    lo = min(range(len(xs)), key=lambda i: xs[i])
    hi = max(range(len(xs)), key=lambda i: xs[i])
    if xs[hi] == xs[lo]:
        return 0.0, 0.0, 0.0
    b = (ys[hi] - ys[lo]) / float(xs[hi] - xs[lo])
    a = ys[hi] - b * xs[hi]
    ssr = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    return a, b, ssr


def load(path, xcol, ycol):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("No rows in %s" % path)
    fields = list(rows[0].keys())

    def numeric(col):
        try:
            for r in rows:
                float(r[col])
            return True
        except (ValueError, KeyError, TypeError):
            return False

    nums = [c for c in fields if numeric(c)]
    if xcol is None or ycol is None:
        if len(nums) < 2:
            sys.exit("Need at least two numeric columns. Found: %s" % ", ".join(nums))
        # Cost is usually the bigger, more variable column; driver the other.
        if xcol is None:
            xcol = nums[0]
        if ycol is None:
            ycol = [c for c in nums if c != xcol][0]
        print("Using x = %s, y = %s   (override with --x and --y)\n" % (xcol, ycol))
    xs = [float(r[xcol]) for r in rows]
    ys = [float(r[ycol]) for r in rows]
    return xs, ys, xcol, ycol


def write_csv(out, name, header, rows):
    p = os.path.join(out, name)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return p


def fits_line(tag, xs, ys):
    a, b, r2, ssr = ols(xs, ys)
    ha, hb, hssr = high_low(xs, ys)
    return {"name": tag, "n": len(xs),
            "ols": {"a": round(a, 2), "b": round(b, 2), "r2": round(r2, 3),
                    "ssr": round(ssr, 0)},
            "high_low": {"a": round(ha, 2), "b": round(hb, 2), "ssr": round(hssr, 0)},
            "x_range": [min(xs), max(xs)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--x", default=None, help="driver column")
    ap.add_argument("--y", default=None, help="cost column")
    ap.add_argument("--out", default="variants")
    ap.add_argument("--shifts", type=int, default=3,
                    help="how many same-shape number sets to make")
    ap.add_argument("--step-at", type=float, default=None,
                    help="driver level where a fixed cost steps up")
    ap.add_argument("--step-size", type=float, default=None,
                    help="how much the fixed cost jumps at that level")
    args = ap.parse_args()

    xs, ys, xcol, ycol = load(args.csv, args.x, args.y)
    os.makedirs(args.out, exist_ok=True)
    n = len(xs)
    report = {"source": os.path.basename(args.csv), "x": xcol, "y": ycol, "fits": []}

    base_rows = list(zip(range(1, n + 1), xs, ys))
    write_csv(args.out, "base.csv", ["i", xcol, ycol], base_rows)
    base = fits_line("base", xs, ys)
    report["fits"].append(base)

    # ---- same shape, different numbers -----------------------------------
    for k in range(1, args.shifts + 1):
        f = 1.0 + 0.07 * k
        rows, nxs, nys = [], [], []
        for i in range(n):
            x2 = round(xs[i] * f + W1[i % len(W1)])
            y2 = round(ys[i] * f + W2[i % len(W2)] * 6)
            rows.append((i + 1, x2, y2))
            nxs.append(x2)
            nys.append(y2)
        write_csv(args.out, "v%d_shift.csv" % k, ["i", xcol, ycol], rows)
        report["fits"].append(fits_line("v%d_shift" % k, nxs, nys))

    # ---- the outlier pair -------------------------------------------------
    # One extra observation at a high driver level with an unusually low cost.
    hx = round(max(xs) + max(1.0, 0.02 * max(xs)))
    a, b, _, _ = ols(xs, ys)
    real_y = round(a + b * hx)
    odd_y = round(real_y * 0.68)          # what the books actually show
    true_y = real_y                       # what it should have been

    pair_rows = base_rows + [(n + 1, hx, odd_y)]
    write_csv(args.out, "outlier_real.csv", ["i", xcol, ycol], pair_rows)
    write_csv(args.out, "outlier_error.csv", ["i", xcol, ycol], pair_rows)
    write_csv(args.out, "outlier_error_CORRECTED.csv", ["i", xcol, ycol],
              base_rows + [(n + 1, hx, true_y)])

    oxs, oys = xs + [hx], ys + [odd_y]
    report["fits"].append(fits_line("with_outlier", oxs, oys))
    ha0, hb0, _ = high_low(xs, ys)
    ha1, hb1, _ = high_low(oxs, oys)
    a1, b1, _, _ = ols(oxs, oys)
    mid = round((min(xs) + max(xs)) / 2.0 + (max(xs) - min(xs)) * 0.4)
    report["outlier"] = {
        "added_point": [hx, odd_y],
        "corrected_value": true_y,
        "high_low_slope": [round(hb0, 2), round(hb1, 2),
                           round((hb1 - hb0) / hb0 * 100, 1) if hb0 else None],
        "ols_slope": [round(b, 2), round(b1, 2),
                      round((b1 - b) / b * 100, 1) if b else None],
        "forecast_at_%d" % mid: {
            "high_low_before": round(ha0 + hb0 * mid, 2),
            "high_low_after": round(ha1 + hb1 * mid, 2),
            "ols_before": round(a + b * mid, 2),
            "ols_after": round(a1 + b1 * mid, 2)},
    }

    # ---- a rival driver that fits better and causes nothing ---------------
    # Built to track the COST, not the driver, so it fits well and explains
    # nothing. Its intercept comes out near zero or negative, which is the tell.
    rival = []
    for i in range(n):
        rival.append(round(0.72 * ys[i] + 0.09 * mean(ys) * (xs[i] / mean(xs))
                           + W2[i % len(W2)] * 16))
    write_csv(args.out, "rival_driver.csv",
              ["i", xcol, "rival_measure", ycol],
              [(i + 1, xs[i], rival[i], ys[i]) for i in range(n)])
    ra, rb, rr2, _ = ols(rival, ys)
    report["rival_driver"] = {
        "real_driver": {"r2": base["ols"]["r2"], "a": base["ols"]["a"], "b": base["ols"]["b"]},
        "rival": {"r2": round(rr2, 3), "a": round(ra, 2), "b": round(rb, 2)},
        "fits_better": rr2 > base["ols"]["r2"],
        "intercept_implausible": ra < 0.10 * mean(ys),
    }

    # ---- past a step change ----------------------------------------------
    step_at = args.step_at if args.step_at is not None else max(xs) * 1.15
    step_size = args.step_size if args.step_size is not None else 0.3 * mean(ys)
    ext_rows, exs, eys = list(base_rows), list(xs), list(ys)
    span = max(xs) - min(xs)
    for k in range(8):
        x2 = round(max(xs) + span * (0.08 + 0.09 * k))
        y2 = round(a + b * x2 + (step_size if x2 >= step_at else 0)
                   + W1[k % len(W1)] * 9)
        ext_rows.append((n + 1 + k, x2, y2))
        exs.append(x2)
        eys.append(y2)
    write_csv(args.out, "out_of_range.csv", ["i", xcol, ycol], ext_rows)
    pooled = fits_line("pooled_across_step", exs, eys)
    report["fits"].append(pooled)
    over = [(x, y) for x, y in zip(exs, eys) if x >= step_at]
    errs = [y - (a + b * x) for x, y in over]
    report["out_of_range"] = {
        "step_at": step_at, "step_size": round(step_size, 2),
        "in_range_line": {"a": base["ols"]["a"], "b": base["ols"]["b"],
                          "r2": base["ols"]["r2"]},
        "pooled_line": pooled["ols"],
        "mean_under_prediction": round(mean(errs), 2) if errs else 0,
        "pooled_r2_is_higher": pooled["ols"]["r2"] > base["ols"]["r2"],
    }

    with open(os.path.join(args.out, "variants.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # ---------------- report ----------------
    W = 72
    print("=" * W)
    print("VARIANTS BUILT FROM %s" % os.path.basename(args.csv))
    print("=" * W)
    print()
    print("BASE  (%d rows, %s from %g to %g)" % (n, xcol, min(xs), max(xs)))
    print("   regression  y = %.2f + %.2f x     R2 = %.3f"
          % (base["ols"]["a"], base["ols"]["b"], base["ols"]["r2"]))
    print("   high-low    y = %.2f + %.2f x"
          % (base["high_low"]["a"], base["high_low"]["b"]))
    print()

    o = report["outlier"]
    print("OUTLIER PAIR   outlier_real.csv and outlier_error.csv")
    print("   Both files add the same point: %s = %g, %s = %g."
          % (xcol, hx, ycol, odd_y))
    print("   Only the story you hand out differs. In the error version the")
    print("   true value was %g." % true_y)
    print("   high-low slope %.2f -> %.2f  (%+.1f%%)"
          % (o["high_low_slope"][0], o["high_low_slope"][1], o["high_low_slope"][2]))
    print("   regression     %.2f -> %.2f  (%+.1f%%)"
          % (o["ols_slope"][0], o["ols_slope"][1], o["ols_slope"][2]))
    print("   -> two methods, same data, very different damage.")
    print()

    r = report["rival_driver"]
    print("RIVAL DRIVER   rival_driver.csv")
    print("   real driver  R2 = %.3f" % r["real_driver"]["r2"])
    print("   rival        R2 = %.3f   %s"
          % (r["rival"]["r2"], "(fits better)" if r["fits_better"] else "(DOES NOT fit better - see warning)"))
    print("   rival intercept = %.2f %s"
          % (r["rival"]["a"], "(near zero or negative - that is the tell)"
             if r["intercept_implausible"] else ""))
    if not r["fits_better"]:
        print()
        print("   WARNING: the rival does not fit better than the real driver, so")
        print("   the exercise does not work. Widen the spread of your cost column")
        print("   or lower the real driver's explanatory power, and run again.")
    print()

    s = report["out_of_range"]
    print("PAST A STEP CHANGE   out_of_range.csv")
    print("   A fixed cost of %.0f appears once %s reaches %g."
          % (s["step_size"], xcol, s["step_at"]))
    print("   The in-range line under-predicts by %.0f on average above it."
          % s["mean_under_prediction"])
    print("   Fitting one line across everything gives R2 = %.3f versus %.3f."
          % (s["pooled_line"]["r2"], s["in_range_line"]["r2"]))
    if s["pooled_r2_is_higher"]:
        print("   The WRONG model reports the BETTER statistic. That is the lesson.")
    print()
    print("Files written to %s/" % args.out)
    print()
    print("Check before you teach it: open each file, confirm the story is one")
    print("that happens in your industry. A defect nobody would ever see teaches")
    print("suspicion, not judgement.")


if __name__ == "__main__":
    main()
