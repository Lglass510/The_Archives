"""Item constructors for the AZ-104 practice bank.

Every item is authored with the correct option(s) kept separate from the
distractors. The build script decides final option order / letter positions,
so authors never pick letters by hand and explanations are generated from the
final layout.
"""
import html

DOMAINS = {
    "ID": "Manage Azure identities and governance",
    "ST": "Implement and manage storage",
    "CO": "Deploy and manage Azure compute resources",
    "NW": "Implement and manage virtual networking",
    "MO": "Monitor and maintain Azure resources",
}

# Official weighting ranges (skills measured as of April 17, 2026).
WEIGHTS = {"ID": (20, 25), "ST": (15, 20), "CO": (20, 25), "NW": (15, 20), "MO": (10, 15)}

SCENARIOS = {}


def code(src, lang=""):
    """Escape a code sample and wrap it for display inside a stem."""
    cls = f' class="lang-{lang}"' if lang else ""
    return f"<pre><code{cls}>{html.escape(src.strip(chr(10)))}</code></pre>"


def scenario(key, name, body_html):
    SCENARIOS[key] = {"name": name, "html": body_html}
    return key


def _base(kind, dom, obj, stem, refs, conf, note, conf_note, case):
    assert dom in DOMAINS, dom
    assert 1 <= len(refs) <= 3, stem[:60]
    assert 0 <= conf <= 100
    return {
        "type": kind, "domain": dom, "objective": obj, "stem": stem,
        "refs": refs, "conf": conf, "note": note, "conf_note": conf_note,
        "case": case,
    }


def mc(dom, obj, stem, ans, why, wrong, refs, conf, note=None, conf_note=None, case=None):
    """Single answer. ans = correct option text; wrong = [(text, reason), ...] (3)."""
    d = _base("mc", dom, obj, stem, refs, conf, note, conf_note, case)
    d.update(ans=ans, why=why, wrong=wrong)
    return d


def multi(dom, obj, stem, ans, why, wrong, refs, conf, note=None, conf_note=None, case=None):
    """Multiple correct. ans = [(text, reason), ...]; wrong = [(text, reason), ...]."""
    d = _base("multi", dom, obj, stem, refs, conf, note, conf_note, case)
    d.update(ans=ans, why=why, wrong=wrong)
    return d


def hot(dom, obj, stem, rows, why, refs, conf, note=None, conf_note=None, case=None):
    """Hotspot. rows = [(label, [values], correct_value, reason), ...]."""
    d = _base("hotspot", dom, obj, stem, refs, conf, note, conf_note, case)
    for r in rows:
        assert r[2] in r[1], (stem[:50], r)
    d.update(rows=rows, why=why)
    return d


def yn(dom, obj, stem, rows, why, refs, conf, note=None, conf_note=None, case=None):
    """Yes/No series rendered as hotspot rows. rows = [(statement, 'Yes'|'No', reason)]."""
    d = hot(dom, obj, stem, [(s, ["Yes", "No"], a, r) for s, a, r in rows], why, refs, conf,
            note, conf_note, case)
    d["yesno"] = True
    return d


def dd(dom, obj, stem, steps, extras, why, refs, conf, note=None, conf_note=None, case=None):
    """Ordered drag-and-drop. steps = [(action, reason)] in correct order;
    extras = [(action, why it is not used)]."""
    d = _base("dragdrop", dom, obj, stem, refs, conf, note, conf_note, case)
    d.update(steps=steps, extras=extras, why=why)
    return d
