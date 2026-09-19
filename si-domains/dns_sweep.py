#!/usr/bin/env python3
"""Sweep .si candidates via DNS (NS lookup) to find names not present in the zone.

NOERROR  -> the name is delegated in the .si zone => REGISTERED.
NXDOMAIN -> the name is absent from the .si zone => LIKELY FREE (confirm by WHOIS
            or a registrar cart; a registered-but-undelegated name also looks
            like this).
"""
import concurrent.futures as cf
import random
import socket
import struct
import sys

SERVERS = ["8.8.8.8", "8.8.4.4"]


def ns_rcode(name: str, tries: int = 3):
    for attempt in range(tries):
        srv = SERVERS[attempt % len(SERVERS)]
        tid = random.randint(0, 65535)
        pkt = (struct.pack(">HHHHHH", tid, 0x0100, 1, 0, 0, 0)
               + b"".join(bytes([len(l)]) + l.encode() for l in name.split(".")) + b"\x00"
               + struct.pack(">HH", 2, 1))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(4)
            s.sendto(pkt, (srv, 53))
            data, _ = s.recvfrom(4096)
            s.close()
            return data[3] & 0xF
        except Exception:
            continue
    return None


def classify(label: str):
    rc = ns_rcode(f"{label}.si")
    if rc == 0:
        return "REGISTERED"
    if rc == 3:
        return "LIKELY_FREE"
    return "UNKNOWN"


def main():
    labels = []
    seen = set()
    for line in (sys.stdin if sys.argv[1] == "-" else open(sys.argv[1])):
        w = line.split("#", 1)[0].strip().lower().removesuffix(".si")
        if w and w not in seen:
            seen.add(w)
            labels.append(w)
    with cf.ThreadPoolExecutor(max_workers=24) as ex:
        for label, status in zip(labels, ex.map(classify, labels)):
            print(f"{label}.si,{status}", flush=True)


if __name__ == "__main__":
    main()
