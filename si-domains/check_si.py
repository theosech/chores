#!/usr/bin/env python3
"""Bulk .si availability checker.

Queries the Slovenian registry's WHOIS (whois.register.si, TCP/43) directly.
Run this from a normal network connection -- the registry rate-limits, so
keep --delay at 2s or higher for lists of more than a few dozen names.

    python3 check_si.py candidates.txt
    python3 check_si.py candidates.txt --delay 3 --out results.csv
    echo "synthe\ngene\nthe" | python3 check_si.py -

Output: CSV of name,status where status is FREE / TAKEN / UNKNOWN.
A FREE result is not a reservation. Confirm at the registrar's cart before
believing it, and register immediately -- WHOIS lookups on hyped strings are
themselves a signal that gets watched.
"""
import argparse
import csv
import socket
import sys
import time

WHOIS_HOST = "whois.register.si"
WHOIS_PORT = 43
TIMEOUT = 15


def query(name: str) -> str:
    fqdn = name if name.endswith(".si") else f"{name}.si"
    with socket.create_connection((WHOIS_HOST, WHOIS_PORT), TIMEOUT) as sock:
        if not fqdn.isascii():  # IDN: punycode each label before sending
            fqdn = ".".join(lbl.encode("idna").decode("ascii") for lbl in fqdn.split("."))
        sock.sendall(f"{fqdn}\r\n".encode("ascii"))
        chunks = []
        while True:
            data = sock.recv(4096)
            if not data:
                break
            chunks.append(data)
    return b"".join(chunks).decode("utf-8", errors="replace")


def classify(response: str) -> str:
    low = response.lower()
    if "no entries found" in low or "not found" in low:
        return "FREE"
    if "\ndomain:" in low or low.startswith("domain:"):
        return "TAKEN"
    if "exceeded" in low or "limit" in low or "denied" in low:
        return "RATE_LIMITED"
    return "UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("infile", help="file with one name per line, or - for stdin")
    ap.add_argument("--delay", type=float, default=2.0, help="seconds between queries (default 2)")
    ap.add_argument("--out", help="write CSV here as well as stdout")
    args = ap.parse_args()

    src = sys.stdin if args.infile == "-" else open(args.infile, encoding="utf-8")
    names = []
    for line in src:
        line = line.split("#", 1)[0].strip().lower()
        if line:
            names.append(line.removesuffix(".si"))
    if src is not sys.stdin:
        src.close()

    rows, free = [], []
    for i, name in enumerate(names):
        try:
            status = classify(query(name))
        except (OSError, socket.timeout) as exc:
            status = f"ERROR:{type(exc).__name__}"
        rows.append((name, status))
        print(f"{name}.si,{status}", flush=True)
        if status == "FREE":
            free.append(name)
        if status == "RATE_LIMITED":
            print("  ! rate limited -- raise --delay and rerun the rest", file=sys.stderr)
        if i < len(names) - 1:
            time.sleep(args.delay)

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["domain", "status"])
            w.writerows([(f"{n}.si", s) for n, s in rows])

    print(f"\n{len(free)} free of {len(rows)} checked", file=sys.stderr)
    for n in free:
        print(f"  {n}.si", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
