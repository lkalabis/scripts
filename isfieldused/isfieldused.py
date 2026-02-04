#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Tuple


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


def compile_combined_pattern(fields: List[str]) -> str:
    # Exact token match: field not surrounded by word chars
    # Sort by length to avoid partial matches when fields share prefixes
    escaped_fields = [re.escape(f) for f in sorted(fields, key=len, reverse=True)]
    joined = "|".join(escaped_fields)
    return rf"(?<![A-Za-z0-9_])(?:{joined})(?![A-Za-z0-9_])"


def iter_files(start_path: str):
    for root, _, files in os.walk(start_path):
        for name in files:
            yield os.path.join(root, name)


_PATTERN: re.Pattern | None = None


def _init_worker(pattern_str: str) -> None:
    global _PATTERN
    _PATTERN = re.compile(pattern_str)


def scan_file(path: str) -> Tuple[str, List[str]]:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
    except (OSError, UnicodeError):
        return path, []

    if _PATTERN is None:
        return path, []

    return path, list({m.group(0) for m in _PATTERN.finditer(data)})


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
    parser.add_argument(
        "--workers",
        type=int,
        default=max(os.cpu_count() or 1, 1),
        help="Number of parallel workers (default: CPU count)",
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

    pattern_str = compile_combined_pattern(fields)
    results: Dict[str, List[str]] = {f: [] for f in fields}

    files = list(iter_files(start_path))
    total = len(files)
    if total == 0:
        print("No files found under start path.")
    else:
        with ProcessPoolExecutor(
            max_workers=args.workers,
            initializer=_init_worker,
            initargs=(pattern_str,),
        ) as pool:
            futures = {pool.submit(scan_file, path): path for path in files}
            completed = 0
            for future in as_completed(futures):
                path, matched_fields = future.result()
                completed += 1
                print(f"Scanned file {completed}/{total}: {path}")
                for field in matched_fields:
                    results[field].append(path)

    # Human-readable output
    for field in fields:
        print(f"Checking field: {field}")
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
