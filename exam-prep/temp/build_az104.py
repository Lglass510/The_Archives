"""Build the AZ-104 practice test bank and the Pearson VUE-style viewer.

Usage (from the exam-prep folder):
    python temp/build_az104.py                 # build + stats
    python temp/build_az104.py --check-links   # also verify every reference URL

Never hand-edit viewer/az104-exam-viewer.html - change this script or the
bank modules in temp/az104_bank/ and regenerate.
"""
import html
import importlib
import json
import math
import random
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SLUG = "az104"
TEST_SIZE = 50
SECONDS_PER_ITEM = 120          # 100 minutes per 50-item test
SEED = 104
LETTERS = "ABCDEF"
MAX_RUN = 2

sys.path.insert(0, str(HERE / "az104_bank"))
import qlib  # noqa: E402

BANK_MODULES = ["bank_identity", "bank_storage", "bank_compute", "bank_network", "bank_monitor"]


# --------------------------------------------------------------------------- load
def load_bank():
    items = []
    for name in BANK_MODULES:
        mod = importlib.import_module(name)
        items.extend(mod.ITEMS)
    return items


def validate(items):
    errs = []
    seen_stems = set()
    for i, q in enumerate(items):
        tag = f"[{q['domain']} #{i}] {re.sub('<[^>]+>', '', q['stem'])[:70]}"
        key = re.sub(r"\W+", "", q["stem"].lower())
        if key in seen_stems:
            errs.append(f"duplicate stem {tag}")
        seen_stems.add(key)
        if q["type"] == "mc":
            if len(q["wrong"]) != 3:
                errs.append(f"mc needs 3 distractors {tag}")
            texts = [q["ans"]] + [w[0] for w in q["wrong"]]
            if len(set(texts)) != len(texts):
                errs.append(f"duplicate option text {tag}")
        elif q["type"] == "multi":
            n = len(q["ans"]) + len(q["wrong"])
            if not (4 <= n <= 6) or len(q["ans"]) < 2:
                errs.append(f"multi option count {tag}")
        elif q["type"] == "hotspot":
            if not q["rows"]:
                errs.append(f"hotspot rows {tag}")
        elif q["type"] == "dragdrop":
            if len(q["steps"]) < 2:
                errs.append(f"dragdrop steps {tag}")
        for u in q["refs"]:
            if not u.startswith("https://"):
                errs.append(f"bad ref {u} {tag}")
        if q["case"] and q["case"] not in qlib.SCENARIOS:
            errs.append(f"unknown case {q['case']} {tag}")
    if errs:
        print("\n".join(errs))
        sys.exit("validation failed")


# --------------------------------------------------------------------------- tests
def domain_targets(n):
    mids = {d: sum(r) / 2 for d, r in qlib.WEIGHTS.items()}
    tot = sum(mids.values())
    return {d: mids[d] / tot * n for d in mids}


def assemble_tests(items, rng):
    """Split the bank into 50-item tests with each test mirroring the domain mix.
    Case-study items travel together as one unit."""
    units = defaultdict(list)
    singles = []
    for q in items:
        (units[q["case"]] if q["case"] else singles).append(q)
    unit_list = list(units.values()) + [[q] for q in singles]
    rng.shuffle(unit_list)
    unit_list.sort(key=len, reverse=True)          # place case studies first

    n_tests = math.ceil(len(items) / TEST_SIZE)
    sizes = [TEST_SIZE] * (n_tests - 1) + [len(items) - TEST_SIZE * (n_tests - 1)]
    tests = [[] for _ in range(n_tests)]
    counts = [Counter() for _ in range(n_tests)]
    targets = [domain_targets(s) for s in sizes]

    for unit in unit_list:
        best, best_cost = None, None
        for t in range(n_tests):
            if len(tests[t]) + len(unit) > sizes[t]:
                continue
            c = counts[t].copy()
            for q in unit:
                c[q["domain"]] += 1
            cost = sum((c[d] - targets[t][d] * (len(tests[t]) + len(unit)) / sizes[t]) ** 2
                       for d in qlib.DOMAINS)
            cost += rng.random() * 0.01
            if best_cost is None or cost < best_cost:
                best, best_cost = t, cost
        tests[best].extend(unit)
        for q in unit:
            counts[best][q["domain"]] += 1

    ordered = []
    for t, test in enumerate(tests):
        groups = defaultdict(list)
        loose = []
        for q in test:
            (groups[q["case"]] if q["case"] else loose).append(q)
        blocks = list(groups.values()) + [[q] for q in loose]
        rng.shuffle(blocks)
        seq = [q for b in blocks for q in b]
        ordered.append(seq)
    return ordered


# --------------------------------------------------------------------------- answer key
def max_run(seq):
    best = cur = 1 if seq else 0
    for a, b in zip(seq, seq[1:]):
        cur = cur + 1 if a == b else 1
        best = max(best, cur)
    return best


def n_runs(seq):
    return 1 + sum(1 for a, b in zip(seq, seq[1:]) if a != b) if seq else 0


def has_mechanical_pattern(seq):
    """Detect ABCDABCD / ABABABAB style periodic windows and AABBCCDD blocks."""
    for w in range(len(seq) - 7):
        win = seq[w:w + 8]
        for p in (2, 3, 4):
            if all(win[i] == win[i + p] for i in range(8 - p)):
                return True
        if all(win[i] == win[i + 1] for i in range(0, 8, 2)) and len(set(win)) >= 3:
            return True
    return False


def runs_ok(seq, k=4):
    n = len(seq)
    if n < 8:
        return True
    p = 1 - 1 / k
    exp = 1 + (n - 1) * p
    sd = math.sqrt((n - 1) * p * (1 - p))
    return abs(n_runs(seq) - exp) <= 2 * sd


def assign_letters(tests, rng):
    """Assign the correct-letter position for every mc item, test by test, so
    the key is balanced per test and bank-wide, has no run longer than MAX_RUN
    (also across test boundaries) and shows no mechanical pattern."""
    k = 4
    bank_extra = Counter()
    prev_tail = []
    for test in tests:
        mcs = [q for q in test if q["type"] == "mc"]
        n = len(mcs)
        base, rem = divmod(n, k)
        # give remainders to the letters least used bank-wide so far
        order = sorted(LETTERS[:k], key=lambda L: (bank_extra[L], rng.random()))
        pool = []
        for L in LETTERS[:k]:
            extra = 1 if L in order[:rem] else 0
            bank_extra[L] += extra
            pool += [L] * (base + extra)
        for _ in range(20000):
            rng.shuffle(pool)
            joined = prev_tail + pool
            if (max_run(joined) <= MAX_RUN and runs_ok(pool) and
                    not has_mechanical_pattern(joined)):
                break
        else:
            sys.exit("could not satisfy answer-key constraints")
        for q, L in zip(mcs, pool):
            q["_letter"] = L
        prev_tail = pool[-MAX_RUN:]


def lay_out(q, rng):
    """Produce final option order and answer for one item."""
    if q["type"] == "mc":
        idx = LETTERS.index(q["_letter"])
        wrong = q["wrong"][:]
        rng.shuffle(wrong)
        opts = wrong[:idx] + [(q["ans"], None)] + wrong[idx:]
        q["_options"] = [{"L": LETTERS[i], "text": t, "reason": r, "ok": r is None}
                         for i, (t, r) in enumerate(opts)]
        q["_answer"] = [q["_letter"]]
    elif q["type"] == "multi":
        opts = [(t, r, True) for t, r in q["ans"]] + [(t, r, False) for t, r in q["wrong"]]
        rng.shuffle(opts)
        q["_options"] = [{"L": LETTERS[i], "text": t, "reason": r, "ok": ok}
                         for i, (t, r, ok) in enumerate(opts)]
        q["_answer"] = [o["L"] for o in q["_options"] if o["ok"]]
    elif q["type"] == "hotspot":
        rows = []
        for label, values, correct, reason in q["rows"]:
            vals = values[:]
            if not q.get("yesno"):
                rng.shuffle(vals)
            rows.append({"label": label, "values": vals, "answer": correct, "reason": reason})
        q["_rows"] = rows
    elif q["type"] == "dragdrop":
        pool = [s for s, _ in q["steps"]] + [e for e, _ in q["extras"]]
        rng.shuffle(pool)
        q["_rows"] = [{"label": f"Step {i + 1}", "values": pool, "answer": s, "reason": r}
                      for i, (s, r) in enumerate(q["steps"])]


# --------------------------------------------------------------------------- explanations
def esc(s):
    return html.escape(s, quote=False)


def link(u):
    label = re.sub(r"^https://(learn\.microsoft\.com/(en-us/)?)?", "", u).rstrip("/")
    return f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{esc(label)}</a>'


def conf_label(score):
    return "High" if score >= 85 else "Medium" if score >= 65 else "Low"


def explain(q):
    parts = []
    t = q["type"]
    if t == "mc":
        o = next(o for o in q["_options"] if o["ok"])
        q["_answer_text"] = f"{o['L']} — {esc(o['text'])}"
        parts.append(f"<p><strong>Correct answer: {o['L']} — {esc(o['text'])}</strong></p>")
        parts.append(f"<p>{q['why']}</p>")
        parts.append("<p><strong>Why the other options are wrong</strong></p><ul>")
        for o2 in q["_options"]:
            if not o2["ok"]:
                parts.append(f"<li><strong>{o2['L']} — {esc(o2['text'])}:</strong> {o2['reason']}</li>")
        parts.append("</ul>")
    elif t == "multi":
        good = [o for o in q["_options"] if o["ok"]]
        q["_answer_text"] = ", ".join(o["L"] for o in good)
        parts.append(f"<p><strong>Correct answers: {q['_answer_text']}</strong></p>")
        parts.append(f"<p>{q['why']}</p><ul>")
        for o in good:
            parts.append(f"<li><strong>{o['L']} — {esc(o['text'])}:</strong> {o['reason']}</li>")
        parts.append("</ul><p><strong>Why the other options are wrong</strong></p><ul>")
        for o in q["_options"]:
            if not o["ok"]:
                parts.append(f"<li><strong>{o['L']} — {esc(o['text'])}:</strong> {o['reason']}</li>")
        parts.append("</ul>")
    else:
        head = "Correct order" if t == "dragdrop" else "Correct selections"
        q["_answer_text"] = "; ".join(f"{esc(r['label'])} → {esc(r['answer'])}" for r in q["_rows"])
        parts.append(f"<p><strong>{head}:</strong></p><ul>")
        for r in q["_rows"]:
            parts.append(f"<li><strong>{esc(r['label'])} → {esc(r['answer'])}.</strong> {r['reason']}</li>")
        parts.append("</ul>")
        parts.append(f"<p>{q['why']}</p>")
        if t == "dragdrop" and q["extras"]:
            parts.append("<p><strong>Actions that are not used</strong></p><ul>")
            for e, r in q["extras"]:
                parts.append(f"<li><strong>{esc(e)}:</strong> {r}</li>")
            parts.append("</ul>")
    if q["note"]:
        parts.append(f'<p class="note"><strong>Note:</strong> {q["note"]}</p>')
    lab = conf_label(q["conf"])
    if lab != "High":
        why_low = q["conf_note"] or "Behavior can vary by feature version or region; verify in current docs."
        parts.append(f'<p class="conf-note"><strong>Confidence {q["conf"]}% ({lab}):</strong> {why_low}</p>')
    parts.append("<p><strong>References</strong></p><ul class=\"refs\">")
    for u in q["refs"]:
        parts.append(f"<li>{link(u)}</li>")
    parts.append("</ul>")
    return "".join(parts)


INSTR = {
    "mc": "Choose the correct answer.",
    "multi": "Choose all that apply.",
    "hotspot": "To answer, select the appropriate option in each row.",
    "yesno": "For each statement, select Yes if the statement is true. Otherwise, select No.",
    "dragdrop": "Select the actions to perform, in the correct order. Not every action is used.",
}


def to_view(q, test_no, n):
    t = q["type"]
    instr = INSTR["yesno"] if q.get("yesno") else INSTR[t]
    if t == "multi":
        instr = f"Choose {len(q['ans'])}. Each correct selection presents part of the solution."
    v = {
        "id": q["_id"], "test": test_no, "n": n, "type": t, "yesno": bool(q.get("yesno")),
        "domain": q["domain"], "domainName": qlib.DOMAINS[q["domain"]], "objective": q["objective"],
        "case": q["case"], "stem": q["stem"], "instr": instr,
        "conf": {"score": q["conf"], "label": conf_label(q["conf"])},
        "answerText": q["_answer_text"], "expl": q["_expl"],
    }
    if t in ("mc", "multi"):
        v["options"] = [{"L": o["L"], "text": o["text"]} for o in q["_options"]]
        v["answer"] = q["_answer"]
        v["pick"] = len(q["_answer"])
    else:
        v["rows"] = [{"label": r["label"], "values": r["values"], "answer": r["answer"]} for r in q["_rows"]]
    return v


# --------------------------------------------------------------------------- stats
def report(tests):
    bank = [q for t in tests for q in t]
    print(f"\n=== Bank summary: {len(bank)} items, {len(tests)} tests "
          f"({', '.join(str(len(t)) for t in tests)}) ===")
    dc = Counter(q["domain"] for q in bank)
    print("\nPer-domain coverage (actual vs official range):")
    for d, name in qlib.DOMAINS.items():
        lo, hi = qlib.WEIGHTS[d]
        pct = dc[d] / len(bank) * 100
        print(f"  {d} {name:<45} {dc[d]:>4}  {pct:5.1f}%  (official {lo}-{hi}%)")
    print("\nPer-objective counts:")
    oc = Counter((q["domain"], q["objective"]) for q in bank)
    for (d, o), c in sorted(oc.items()):
        print(f"  {d} {o:<75} {c:>3}")
    tc = Counter(("yesno" if q.get("yesno") else q["type"]) for q in bank)
    print("\nType split:", dict(tc))
    cc = Counter(conf_label(q["conf"]) for q in bank)
    print("Confidence labels:", dict(cc))

    def key_stats(label, seq):
        c = Counter(seq)
        n = len(seq)
        split = "  ".join(f"{L}={c[L]} ({c[L] / n * 100:.0f}%)" for L in "ABCD")
        p = 0.75
        exp = 1 + (n - 1) * p
        sd = math.sqrt((n - 1) * p * (1 - p))
        chi = sum((c[L] - n / 4) ** 2 / (n / 4) for L in "ABCD")
        print(f"  {label:<8} n={n:<3} {split}  max-run={max_run(seq)}  runs={n_runs(seq)} "
              f"(expected {exp:.1f}±{2 * sd:.1f})  chi2={chi:.2f}  "
              f"pattern={'YES' if has_mechanical_pattern(seq) else 'none'}")
        return max_run(seq) <= MAX_RUN and not has_mechanical_pattern(seq) and chi < 7.81

    print("\nAnswer-key distribution (single-answer mc items):")
    ok = True
    for i, t in enumerate(tests, 1):
        ok &= key_stats(f"Test {i}", [q["_letter"] for q in t if q["type"] == "mc"])
    ok &= key_stats("Bank", [q["_letter"] for q in bank if q["type"] == "mc"])
    print("  chi2 critical value (df=3, p=0.05) = 7.81; below it means no detectable positional bias.")
    print(f"  Answer key {'PASSES' if ok else 'FAILS'} balance / run-length / pattern checks.")
    if not ok:
        sys.exit("answer key failed checks")


def check_links(bank):
    urls = sorted({u for q in bank for u in q["refs"]})
    print(f"\nChecking {len(urls)} reference URLs ...")

    def probe(u):
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 az104-bank-linkcheck"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return u, r.status
        except Exception as e:  # noqa: BLE001
            return u, getattr(e, "code", str(e))

    with ThreadPoolExecutor(12) as ex:
        results = list(ex.map(probe, urls))
    bad = [(u, s) for u, s in results if s != 200]
    for u, s in bad:
        print(f"  BROKEN {s}: {u}")
    print(f"  {len(urls) - len(bad)}/{len(urls)} OK")
    return not bad


# --------------------------------------------------------------------------- main
def main():
    rng = random.Random(SEED)
    items = load_bank()
    validate(items)
    tests = assemble_tests(items, rng)
    assign_letters(tests, rng)
    view = []
    qid = 0
    for t_no, test in enumerate(tests, 1):
        for n, q in enumerate(test, 1):
            qid += 1
            q["_id"] = qid
            lay_out(q, rng)
            q["_expl"] = explain(q)
            view.append(to_view(q, t_no, n))
    report(tests)
    if "--check-links" in sys.argv and not check_links([q for t in tests for q in t]):
        sys.exit("broken links")

    data = {
        "exam": "AZ-104: Microsoft Azure Administrator",
        "slug": SLUG,
        "outline": "Skills measured as of April 17, 2026",
        "secondsPerItem": SECONDS_PER_ITEM,
        "domains": qlib.DOMAINS,
        "cases": qlib.SCENARIOS,
        "tests": [len(t) for t in tests],
        "items": view,
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = (HERE / "viewer_template.html").read_text(encoding="utf-8")
    out = template.replace("/*__DATA__*/null", payload)
    dest = ROOT / "viewer" / f"{SLUG}-exam-viewer.html"
    dest.write_text(out, encoding="utf-8")
    (ROOT / "viewer" / f"{SLUG}-bank.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    imgs = re.findall(r'src="([^"]+)"', out)
    missing = [s for s in imgs if not (dest.parent / s).resolve().exists()]
    if missing:
        sys.exit(f"missing images: {missing}")
    print(f"\nWrote {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB), "
          f"{len(imgs)} image refs, all resolved.")


if __name__ == "__main__":
    main()
