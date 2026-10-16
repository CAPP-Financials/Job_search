"""Audit that every firm has global, UK and India career pages accounted for (data/raw/tier_*_scopes.json).
Exit 1 and list gaps if any firm/scope is missing, unknown-status, or 'ok' without a URL.   --selftest to run the check on itself."""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCOPES = ("global", "uk", "india")
STATUS = {"ok", "via-global", "none", "blocked"}


def gaps(firms, scopes):
    out = []
    for f in firms:
        s = scopes.get(f, {})
        for sc in SCOPES:
            v = s.get(sc)
            if not v:
                out.append((f, sc, "not reported"))
            elif v.get("status") not in STATUS:
                out.append((f, sc, f"bad status {v.get('status')!r}"))
            elif v["status"] in ("ok", "via-global") and not v.get("url"):
                out.append((f, sc, "no url"))
            elif v["status"] in ("none", "blocked") and not v.get("note"):
                out.append((f, sc, "no reason given"))
    return out


def load():
    firms = [f["name"] for f in yaml.safe_load((ROOT / "firms" / "firms.yaml").read_text(encoding="utf-8"))["firms"]]
    scopes = {}
    for p in sorted((ROOT / "data" / "raw").glob("tier_*_scopes.json")):
        scopes.update(json.loads(p.read_text(encoding="utf-8")))
    return firms, scopes


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        ok = {"status": "ok", "url": "u"}
        s = {"A": {"global": ok, "uk": {"status": "none", "note": "no UK arm"}, "india": {"status": "via-global", "url": "u"}},
             "B": {"global": ok, "uk": {"status": "ok"}, "india": {"status": "blocked"}}}
        g = gaps(["A", "B", "C"], s)
        assert [x[:2] for x in g] == [("B", "uk"), ("B", "india"), ("C", "global"), ("C", "uk"), ("C", "india")], g
        print("coverage_check selftest OK")
        sys.exit()
    firms, scopes = load()
    g = gaps(firms, scopes)
    for f, sc, why in g:
        print(f"GAP  {f} | {sc} | {why}")
    print(f"{len(firms)} firms x 3 scopes = {len(firms) * 3} checks, {len(g)} gaps")
    sys.exit(1 if g else 0)
