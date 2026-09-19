#!/usr/bin/env python3
"""Authoritative .si availability checker: RDAP first, WHOIS fallback.

Run this from an ordinary network connection. Unlike a DNS probe, this sees
registrations that have no nameservers -- which on .si is a large and
systematically biased population, because the registry only delegates a domain
once two working nameservers pass its predelegation check, and investors
holding names for resale rarely bother.

    python3 check_si.py candidates.txt
    python3 check_si.py AVAILABLE.csv --out results.csv
    echo lucid | python3 check_si.py -

Accepts a plain list or the domain column of a CSV. Output: domain,status where
status is FREE / TAKEN / UNKNOWN.
"""
import argparse
import csv
import json
import socket
import sys
import time
import urllib.error
import urllib.request

RDAP_ENDPOINTS = ["https://rdap.register.si/domain/", "https://rdap.org/domain/"]
WHOIS_HOST = "whois.register.si"
TIMEOUT = 15


def via_rdap(fqdn: str):
    """Returns 'TAKEN', 'FREE', or None if RDAP is unusable."""
    for base in RDAP_ENDPOINTS:
        req = urllib.request.Request(base + fqdn, headers={"Accept": "application/rdap+json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                json.load(resp)
                return "TAKEN"
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return "FREE"
            continue          # 429/5xx -- try the next endpoint
        except Exception:
            continue
    return None


def via_whois(fqdn: str):
    with socket.create_connection((WHOIS_HOST, 43), TIMEOUT) as sock:
        sock.sendall(f"{fqdn}\r\n".encode("ascii"))
        chunks = []
        while True:
            data = sock.recv(4096)
            if not data:
                break
            chunks.append(data)
    body = b"".join(chunks).decode("utf-8", errors="replace").lower()
    if "no entries found" in body or "not found" in body:
        return "FREE"
    if "domain:" in body:
        return "TAKEN"
    if "exceeded" in body or "limit" in body or "denied" in body:
        return "RATE_LIMITED"
    return "UNKNOWN"


def check(label: str) -> str:
    fqdn = label if label.endswith(".si") else f"{label}.si"
    verdict = via_rdap(fqdn)
    if verdict:
        return verdict
    try:
        return via_whois(fqdn)
    except (OSError, socket.timeout) as exc:
        return f"ERROR:{type(exc).__name__}"


def load(path):
    src = sys.stdin if path == "-" else open(path, encoding="utf-8")
    names, seen = [], set()
    for line in src:
        field = line.split(",", 1)[0]            # tolerate CSV input
        field = field.split("#", 1)[0].strip().lower().removesuffix(".si")
        if not field or field in seen or field == "domain":
            continue
        seen.add(field)
        names.append(field)
    if src is not sys.stdin:
        src.close()
    return names


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("infile", help="list or CSV of names, or - for stdin")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between queries")
    ap.add_argument("--out", help="also write results here as CSV")
    args = ap.parse_args()

    names = load(args.infile)
    rows, free = [], []
    for i, name in enumerate(names):
        status = check(name)
        rows.append((f"{name}.si", status))
        print(f"{name}.si,{status}", flush=True)
        if status == "FREE":
            free.append(name)
        if status == "RATE_LIMITED":
            print("  ! rate limited -- raise --delay and rerun the remainder", file=sys.stderr)
        if i < len(names) - 1:
            time.sleep(args.delay)

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["domain", "status"])
            w.writerows(rows)

    print(f"\n{len(free)} genuinely free of {len(rows)} checked", file=sys.stderr)
    for n in free:
        print(f"  {n}.si", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
