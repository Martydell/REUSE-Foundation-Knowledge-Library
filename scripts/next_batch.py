import csv, os, re, sys, unicodedata, difflib

MANUAL_ALIASES = {"Flo Hygeine", "Eviu", "Greenpeace Phillipenes", "Grum"}
COLS = ["Organisation","Category","Country","Website","Contact Information","Focus Area",
        "Year Established","Trading Status","Ownership","Core model","Company Size data",
        "Customers","Geographic scope","Categories","Partners","Partner Category",
        "Data (Plastic saved)","Data (Co2 Reduction)","Key Facts","Anything else","Comments"]

def slugify(name):
    name = name.strip()
    name = unicodedata.normalize("NFKD", name).encode("ascii","ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()

def compact_of(slug_or_name):
    return slugify(slug_or_name).replace("-", "")

def words_of(name):
    return slugify(name).split("-")

def name_variants(name):
    """Yield word-lists for a name, including an '&' -> 'and' expansion variant."""
    yield words_of(name)
    if "&" in name:
        yield words_of(name.replace("&", " and "))

def is_contiguous_match(words_a, words_b):
    """True if the shorter word-list appears as a contiguous run anywhere in the longer one."""
    shorter, longer = (words_a, words_b) if len(words_a) <= len(words_b) else (words_b, words_a)
    if not shorter:
        return False
    n = len(shorter)
    for i in range(len(longer) - n + 1):
        if longer[i:i+n] == shorter:
            return True
    return False

def is_match(name, done_words_list, done_compact_keys):
    compact = compact_of(name)
    if compact in done_compact_keys:
        return True
    if difflib.get_close_matches(compact, done_compact_keys, n=1, cutoff=0.94):
        return True
    for words in name_variants(name):
        for done_words in done_words_list:
            if is_contiguous_match(words, done_words):
                return True
    return False

def get_remaining(repo_root):
    done_slugs = sorted(f[:-3] for f in os.listdir(os.path.join(repo_root,"organisations")) if f.endswith(".md"))
    # ascii-fold done slugs too, in case an agent kept accented chars in a filename
    done_compact = {compact_of(s) for s in done_slugs}
    done_words_list = [s.split("-") for s in done_slugs]
    with open(os.path.join(repo_root,"data","REUSE_Master_List.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    remaining, seen, seen_compact = [], set(), set()
    for r in rows:
        name = r["Organisation"].strip()
        if not name or name in seen or name in MANUAL_ALIASES:
            continue
        seen.add(name)
        compact = compact_of(name)
        if compact in seen_compact:
            continue  # duplicate entry within the legacy list itself (e.g. "Clean Cult" / "CleanCult")
        if is_match(name, done_words_list, done_compact):
            continue
        seen_compact.add(compact)
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
