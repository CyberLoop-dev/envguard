#!/usr/bin/env python3
"""envguard - find leaked secrets before they find the internet.

Usage:
  python envguard.py                 scan the current folder
  python envguard.py path/to/repo    scan a specific folder
  python envguard.py --staged        scan only what you're about to commit
  python envguard.py --install-hook  block leaky commits automatically
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys

RULES = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "Slack Token": r"xox[baprs]-[A-Za-z0-9-]{10,}",
    "Google API Key": r"AIza[0-9A-Za-z_\-]{35}",
    "Stripe Live Key": r"sk_live_[0-9a-zA-Z]{24,}",
    "Telegram Bot Token": r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b",
    "Private Key": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "JWT": r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
    "Hardcoded Secret": r"(?i)(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]",
}
RX = {name: re.compile(rx) for name, rx in RULES.items()}
KEYWORD = re.compile(r"(?i)key|secret|token|pass|auth")
HIGH = re.compile(r"""["']([A-Za-z0-9+/=_\-]{24,})["']""")
ENV_FILE = re.compile(r"^\.env(\..+)?$")
ENV_OK = (".example", ".sample", ".template", ".dist")
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".idea", ".vscode"}
MAX_BYTES = 1_000_000
CROSS = "✖"
CHECK = "✔"
DOT = "•"

USE_COLOR = sys.stdout.isatty()


def paint(code, text):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def mask(value):
    if len(value) <= 8:
        return DOT * 6
    return value[:4] + DOT * min(12, len(value) - 8) + value[-4:]


def entropy(s):
    if not s:
        return 0.0
    probs = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probs)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def iter_files(root, staged):
    if staged:
        names = git("diff", "--cached", "--name-only", "--diff-filter=ACM").stdout.splitlines()
        for name in names:
            data = subprocess.run(["git", "show", ":" + name], capture_output=True).stdout
            yield name, data
        return
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            path = os.path.join(folder, f)
            try:
                if os.path.getsize(path) > MAX_BYTES:
                    continue
                with open(path, "rb") as fh:
                    yield os.path.relpath(path, root), fh.read()
            except OSError:
                continue


def scan(path, data):
    findings = []
    base = os.path.basename(path)
    if ENV_FILE.match(base) and not base.endswith(ENV_OK):
        findings.append((path, 0, "Env file in repo", "remove it & add to .gitignore"))
    if b"\0" in data[:2048]:
        return findings
    text = data.decode("utf-8", errors="ignore")
    for n, line in enumerate(text.splitlines(), 1):
        if "envguard:ignore" in line or len(line) > 2000:
            continue
        hit = False
        for name, rx in RX.items():
            for m in rx.finditer(line):
                findings.append((path, n, name, mask(m.group(0))))
                hit = True
        if not hit and KEYWORD.search(line):
            for m in HIGH.finditer(line):
                if entropy(m.group(1)) > 4.5:
                    findings.append((path, n, "High-entropy string", mask(m.group(1))))
    return findings


def install_hook():
    root = git("rev-parse", "--show-toplevel").stdout.strip()
    if not root:
        sys.exit("Not inside a git repo.")
    hook = os.path.join(root, ".git", "hooks", "pre-commit")
    script = os.path.abspath(__file__)
    with open(hook, "w") as f:
        f.write('#!/bin/sh\npython3 "' + script + '" --staged\n')
    os.chmod(hook, 0o755)
    print(paint("32", CHECK + " pre-commit hook installed."), "Leaky commits will be blocked.")


def main():
    ap = argparse.ArgumentParser(description="Find leaked secrets before they find the internet.")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--staged", action="store_true", help="scan only staged changes")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--install-hook", action="store_true", help="install git pre-commit hook")
    args = ap.parse_args()

    if args.install_hook:
        return install_hook()

    findings, count = [], 0
    for path, data in iter_files(args.path, args.staged):
        count += 1
        findings.extend(scan(path, data))

    if args.json:
        keys = ("file", "line", "rule", "preview")
        print(json.dumps([dict(zip(keys, f)) for f in findings], indent=2, ensure_ascii=False))
        sys.exit(1 if findings else 0)

    if not findings:
        print(paint("32;1", CHECK + " Clean!"), "Scanned %d files, found nothing scary." % count)
        return

    current = None
    for path, line, rule, preview in findings:
        if path != current:
            print("\n" + paint("1;4", path))
            current = path
        where = "line %d" % line if line else "file"
        print("  %s %s %s %s" % (paint("31", CROSS), paint("33", rule.ljust(22)), paint("90", where.ljust(10)), preview))
    print("\n" + paint("31;1", "%d potential secret(s) in %d files." % (len(findings), count)))
    print(paint("90", "False alarm? Add  envguard:ignore  as a comment on that line."))
    sys.exit(1)


if __name__ == "__main__":
    main()
