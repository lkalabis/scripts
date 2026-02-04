#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Dict, List


def load_fields(path: str) -> List[str]:
    fields: List[str] = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue
            if raw.startswith("#"):
                continue
            fields.append(raw)
    return fields


def compile_patterns(fields: List[str]) -> Dict[str, re.Pattern]:
    patterns: Dict[str, re.Pattern] = {}
    for field in fields:
        # Exact token match: field not surrounded by word chars
        escaped = re.escape(field)
        pat = re.compile(rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])")
        patterns[field] = pat
    return patterns


def iter_files(start_path: str):
    for root, _, files in os.walk(start_path):
        for name in files:
            yield os.path.join(root, name)


def scan_file(path: str, pattern: re.Pattern) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
    except (OSError, UnicodeError):
        return False

    return pattern.search(data) is not None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find field usages under a start path (exact token match)."
    )
    parser.add_argument(
        "--fields",
        required=True,
        help="Path to fields.txt (one field per line)",
    )
    parser.add_argument(
        "--start",
        required=True,
        help="Start path to recursively search",
    )
    parser.add_argument(
        "--json-out",
        default="results.json",
        help="Where to write JSON results (default: results.json)",
    )

    args = parser.parse_args()

    fields = load_fields(args.fields)
    if not fields:
        print("No fields found in fields file.", file=sys.stderr)
        return 2

    start_path = os.path.abspath(args.start)
    if not os.path.exists(start_path):
        print(f"Start path does not exist: {start_path}", file=sys.stderr)
        return 2

    patterns = compile_patterns(fields)
    results: Dict[str, List[str]] = {f: [] for f in fields}
    files = list(iter_files(start_path))

    for field in fields:
        print(f"Pruefe Feld: {field}")
        pattern = patterns[field]
        for path in files:
            if scan_file(path, pattern):
                results[field].append(path)

    # Human-readable output
    for field in fields:
        files = results[field]
        print(field)
        if files:
            for p in files:
                print(f"  {p}")
        else:
            print("  (not found)")

    # JSON output
    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
