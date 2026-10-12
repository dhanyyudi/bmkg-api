#!/usr/bin/env python3
"""Rebuild app/data/wilayah.csv from a wilayah-id export.

The region data bundled with this API is a snapshot of wilayah-id
(https://github.com/dhanyyudi/wilayah-id, Dukcapil Kemendagri 2024), the
dataset whose village codes BMKG's forecast API accepts.

Input: a headerless CSV of `code,name` covering all four levels, with codes
written without dots (11, 1101, 110101, 1101012001). From the wilayah-id
database:

    COPY (
        SELECT kode_prov, nama_provinsi FROM provinsi
        UNION ALL SELECT kode_kab, nama_kabupaten FROM kabupaten
        UNION ALL SELECT kode_kec, nama_kecamatan FROM kecamatan
        UNION ALL SELECT kode_desa, nama_desa FROM desa
    ) TO STDOUT WITH CSV;

The same rows are served by its API under /api/v1/regions/.

Usage: python scripts/update_wilayah.py export.csv
"""

import csv
import sys
from collections import Counter
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "app" / "data" / "wilayah.csv"

# Digits per level: province, district, subdistrict, village
WIDTHS = {2: (2,), 4: (2, 2), 6: (2, 2, 2), 10: (2, 2, 2, 4)}


def dotted(code: str) -> str:
    """Write a code the way BMKG does: 3174041006 -> 31.74.04.1006."""
    parts, start = [], 0
    for width in WIDTHS[len(code)]:
        parts.append(code[start:start + width])
        start += width
    return ".".join(parts)


def main(source: str) -> None:
    rows: dict[str, str] = {}
    skipped = Counter()
    with open(source, newline="", encoding="utf-8") as f:
        for record in csv.reader(f):
            if len(record) != 2:
                skipped["malformed row"] += 1
                continue
            code, name = record[0].strip(), " ".join(record[1].split())
            if not code.isdigit() or len(code) not in WIDTHS or not name:
                skipped["unexpected code or empty name"] += 1
                continue
            rows[dotted(code)] = name

    # A region whose parent is missing could never be reached by browsing.
    orphans = [code for code in rows if "." in code and code.rsplit(".", 1)[0] not in rows]
    for code in orphans:
        del rows[code]
    skipped["parent missing"] += len(orphans)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(sorted(rows.items()))

    levels = Counter(code.count(".") for code in rows)
    print(f"wrote {OUTPUT}")
    print(f"provinces {levels[0]}, districts {levels[1]}, subdistricts {levels[2]}, villages {levels[3]}")
    for reason, count in skipped.items():
        if count:
            print(f"skipped {count}: {reason}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
