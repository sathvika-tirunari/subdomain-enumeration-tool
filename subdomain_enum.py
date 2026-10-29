#!/usr/bin/env python3
"""Educational subdomain enumeration using DNS lookups and a small built-in wordlist.

Use ONLY on domains you own or have permission to assess. Passive-style, low-rate DNS
lookups only; no brute-force of other services.
"""
import argparse
import re
import secrets
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor

BUILTIN_WORDLIST = [
    "www", "mail", "webmail", "smtp", "pop", "imap", "ftp", "ns1", "ns2", "dns",
    "api", "dev", "test", "staging", "stage", "beta", "demo", "portal", "admin", "login",
    "vpn", "remote", "blog", "shop", "store", "app", "apps", "m", "mobile", "cdn",
    "static", "assets", "img", "images", "media", "docs", "support", "help", "status", "git",
    "intranet", "internal", "sso", "auth", "db", "monitor", "grafana", "files", "download", "web",
]
MAX_WORDS = 5000
LABEL_RE = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")


def validate_domain(domain):
    """Return a cleaned lowercase domain or raise ValueError."""
    d = domain.strip().lower().rstrip(".")
    if d.startswith(("http://", "https://")):
        raise ValueError("Give only the domain name (example.com), not a URL.")
    if not d or len(d) > 253 or "." not in d:
        raise ValueError(f"'{domain}' is not a valid domain (example: example.com).")
    for label in d.split("."):
        if not LABEL_RE.match(label):
            raise ValueError(f"'{domain}' contains an invalid label: '{label}'.")
    return d


def load_wordlist(path=None):
    if not path:
        return list(BUILTIN_WORDLIST)
    try:
        with open(path, encoding="utf-8") as fh:
            words = [w.strip().lower() for w in fh if w.strip() and not w.startswith("#")]
    except OSError as exc:
        raise ValueError(f"Cannot read wordlist '{path}': {exc.strerror}") from None
    words = [w for w in dict.fromkeys(words) if LABEL_RE.match(w)]
    if not words:
        raise ValueError("Wordlist has no valid entries.")
    return words[:MAX_WORDS]


def resolve(name):
    """Return sorted IP list for name, or [] if it does not resolve."""
    try:
        infos = socket.getaddrinfo(name, None, proto=socket.IPPROTO_TCP)
    except (socket.gaierror, UnicodeError):
        return []
    except OSError:
        return []
    return sorted({i[4][0] for i in infos})


def detect_wildcard(domain):
    """If a random, non-existent name resolves, the domain uses wildcard DNS."""
    return set(resolve(f"{secrets.token_hex(8)}.{domain}"))


def enumerate_subdomains(domain, words, workers=20):
    wildcard = detect_wildcard(domain)
    names = [f"{w}.{domain}" for w in words]
    with ThreadPoolExecutor(max_workers=max(1, min(workers, 50))) as pool:
        answers = list(pool.map(resolve, names))
    found = []
    for name, ips in zip(names, answers):
        if ips and not (wildcard and set(ips) <= wildcard):
            found.append((name, ips))
    return wildcard, found


def main(argv=None):
    ap = argparse.ArgumentParser(description="Educational subdomain enumerator (authorised use only).")
    ap.add_argument("domain", help="Domain you own or may assess, e.g. example.com")
    ap.add_argument("-w", "--wordlist", help="Optional wordlist file (one word per line)")
    ap.add_argument("--workers", type=int, default=20, help="Parallel lookups (max 50, default 20)")
    ap.add_argument("--confirm-authorized", action="store_true",
                    help="REQUIRED: confirms you own this domain or have permission to assess it")
    args = ap.parse_args(argv)

    if not args.confirm_authorized:
        print("Refusing to run: add --confirm-authorized to confirm you own this domain or have permission.")
        return 3
    try:
        domain = validate_domain(args.domain)
        words = load_wordlist(args.wordlist)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    print(f"Enumerating {domain} with {len(words)} candidate names...")
    start = time.time()
    try:
        wildcard, found = enumerate_subdomains(domain, words, args.workers)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    if wildcard:
        print(f"WARNING: wildcard DNS detected ({', '.join(sorted(wildcard))}). "
              "Results matching the wildcard were hidden.")
    print("\nSUBDOMAIN                          IP ADDRESS(ES)")
    for name, ips in found:
        print(f"{name:<34} {', '.join(ips)}")
    if not found:
        print("(no subdomains found)")
    print(f"\nDone in {time.time() - start:.2f}s: {len(found)} resolving subdomain(s) out of {len(words)} tried.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
