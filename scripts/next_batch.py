import csv, os, re, sys, unicodedata, difflib

MANUAL_ALIASES = {"Flo Hygeine"}
COLS = ["Organisation","Category","Country","Website","Contact Information","Focus Area",
        "Year Established","Trading Status","Ownership","Core model","Company Size data",
        "Customers","Geographic scope","Categories","Partners","Partner Category",
        "Data (Plastic saved)","Data (Co2 Reduction)","Key Facts","Anything else","Comments"]

def slugify(name):
    name = name.strip()
    name = unicodedata.normalize("NFKD", name).encode("ascii","ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()

def get_remaining(repo_root):
    done_slugs = sorted(f[:-3] for f in os.listdir(os.path.join(repo_root,"organisations")) if f.endswith(".md"))
    done_compact = {s.replace("-",""): s for s in done_slugs}
    with open(os.path.join(repo_root,"data","REUSE_Master_List.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    remaining, seen = [], set()
    for r in rows:
        name = r["Organisation"].strip()
        if not name or name in seen or name in MANUAL_ALIASES:
            continue
        seen.add(name)
        slug = slugify(name)
        compact = slug.replace("-","")
        if slug in done_slugs or compact in done_compact:
            continue
        if difflib.get_close_matches(compact, done_compact.keys(), n=1, cutoff=0.94):
            continue
        remaining.append(r)
    return remaining

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    group_size = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    tag = sys.argv[3] if len(sys.argv) > 3 else "batchN"
    remaining = get_remaining(repo_root)
    print(f"Total remaining: {len(remaining)}", file=sys.stderr)
    batch = remaining[:n]
    groups = [batch[i:i+group_size] for i in range(0, len(batch), group_size)]
    for gi, g in enumerate(groups):
        path = f"/tmp/{tag}_group{gi+1}.txt"
        with open(path, "w", encoding="utf-8") as out:
            for i, r in enumerate(g):
                out.write(f"### Org {i+1}: {r['Organisation'].strip()}\n")
                for c in COLS:
                    v = (r.get(c) or "").strip()
                    if v:
                        out.write(f"- {c}: {v}\n")
                out.write("\n")
        print(f"group{gi+1} ({path}): {[o['Organisation'].strip() for o in g]}", file=sys.stderr)
