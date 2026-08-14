#!/usr/bin/env python3
"""check_report_code.py

Verify every ```python block in Task2_Report/Task2_Report.md against the
source file gomoku_v2_task2.py.

Two rules:
  1. The block under the "Program Full Code" heading must be IDENTICAL to
     the source file (same lines, same order).
  2. Every other ```python block is a short excerpt: each of its lines must
     appear verbatim somewhere in the source file.

"......" lines are elision markers used by the report and are ignored in
the excerpt check.

Exit code 0 = all checks pass, 1 = any check fails.
"""

import re
import sys
from difflib import unified_diff
from pathlib import Path


def find_root():
    """Walk up from this script until the repo root (containing gomoku_v2_task2.py) is found."""
    cur = Path(__file__).resolve().parent
    while cur != cur.parent:
        if (cur / "gomoku_v2_task2.py").is_file():
            return cur
        cur = cur.parent
    raise RuntimeError("could not locate repo root (gomoku_v2_task2.py not found)")


ROOT = find_root()
REPORT = ROOT / "Task2_Report" / "Task2_Report.md"
SOURCE = ROOT / "gomoku_v2_task2.py"

ELISION = "......"
MAX_DIFF_LINES = 40


def extract_blocks(text):
    """Return [(heading, [lines]), ...] for each ```python fence in order."""
    blocks = []
    heading = None
    lines = text.splitlines()
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        hm = re.match(r"^#{1,6}\s+(.*)$", line)
        if hm:
            heading = hm.group(1).strip()
            i += 1
            continue
        if line.strip() == "```python":
            i += 1
            body = []
            while i < n and lines[i].strip() != "```":
                body.append(lines[i])
                i += 1
            blocks.append((heading, body))
            i += 1  # skip closing fence
            continue
        i += 1
    return blocks


def normalize(lines):
    """Strip trailing CR and drop trailing blank lines."""
    out = [ln.rstrip("\r") for ln in lines]
    while out and out[-1].strip() == "":
        out.pop()
    return out


def check_identical(block, src):
    """Full-code rule: block must be line-for-line identical to src."""
    block, src = normalize(block), normalize(src)
    if block == src:
        return True, None
    diff = list(
        unified_diff(src, block, fromfile="report block", tofile=SOURCE.name, lineterm="")
    )[2:]  # drop the '---'/'+++' header lines
    return False, diff[:MAX_DIFF_LINES]


def _code_core(line):
    """Return a code line with its trailing '# comment' and surrounding whitespace removed."""
    return re.split(r"\s+#", line.strip(), maxsplit=1)[0].strip()


def check_excerpt(block, src_set, src_core_set):
    """Excerpt rule: each non-elision line must exist in src, ignoring indentation.

    Exact (whitespace-stripped) match -> pass. If only a trailing '# comment'
    differs, the line is reported as a warning (the code itself still matches).
    """
    missing, warns = [], []
    for lineno, ln in enumerate(block, 1):
        if ln.strip() == ELISION:
            continue
        s = ln.strip()
        if not s:  # blank line trivially exists
            continue
        if s in src_set:
            continue
        core = _code_core(s)
        if core and core in src_core_set:
            warns.append((lineno, ln))
            continue
        missing.append((lineno, ln))
    return missing, warns


def main():
    text = REPORT.read_text(encoding="utf-8")
    src = normalize(SOURCE.read_text(encoding="utf-8").splitlines())
    src_set = {ln.strip() for ln in src if ln.strip()}
    src_core_set = {_code_core(ln) for ln in src if _code_core(ln)}
    blocks = extract_blocks(text)
    if not blocks:
        print("No ```python blocks found in %s" % REPORT)
        return 1

    failed = 0
    warned = 0
    for heading, body in blocks:
        title = heading or "(no heading)"
        is_full = heading is not None and re.match(r"^Program Full Code", heading)
        if is_full:
            ok, diff = check_identical(body, src)
            if ok:
                print("PASS  [Full Code] %s  (%d lines, identical)" % (title, len(normalize(body))))
            else:
                failed += 1
                print("FAIL  [Full Code] %s  (%d differing lines shown)" % (title, len(diff)))
                print("      (- = in report block only, + = in %s only)" % SOURCE.name)
                for ln in diff:
                    print("      |" + ln)
        else:
            missing, warns = check_excerpt(body, src_set, src_core_set)
            total = sum(1 for l in body if l.strip() and l.strip() != ELISION)
            if missing:
                failed += 1
                print("FAIL  [excerpt]  %s  (%d/%d lines not found)" % (title, len(missing), total))
                for lineno, ln in missing:
                    print("      | line %d: %s" % (lineno, ln))
            elif warns:
                warned += 1
                print("WARN  [excerpt]  %s  (code matches, %d line(s) differ only in a trailing comment)" % (title, len(warns)))
                for lineno, ln in warns:
                    print("      | line %d: %s" % (lineno, ln))
            else:
                print("PASS  [excerpt]  %s  (%d lines all present)" % (title, total))

    print("-" * 60)
    if failed:
        print("RESULT: %d code-block check(s) FAILED" % failed)
        return 1
    print("RESULT: all code blocks consistent with %s%s" % (SOURCE.name, " (%d warning(s))" % warned if warned else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
