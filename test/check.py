#!/usr/bin/env python3
"""Applies patches.json to the stock key layout the way HMG-API's "lines" change does, then checks the result."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
change = json.load(open(os.path.join(HERE, "..", "mod", "patches.json")))["changes"][0]
stock = open(os.path.join(HERE, "stock-cvev-260507.kl")).read().split("\n")


def keys(lines):
    """scan code -> key name, as Android's KeyLayoutMap reads it. A repeated scan code fails the whole file."""
    out = {}
    for line in lines:
        m = re.match(r"\s*key\s+(\d+)\s+(\S+)", line)
        if m:
            assert m.group(1) not in out, f"duplicate scan code {m.group(1)}"
            out[m.group(1)] = m.group(2)
    return out


for line in change["comment"]:
    assert line in stock, f"not in the stock file, exactly: {line!r}"
patched = ["#" + l if l.strip() in change["comment"] else l for l in stock]
if patched[-1] == "":
    patched.pop()
patched += change["add"]

before, after = keys(stock), keys(patched)
changed = {k: (before.get(k), after.get(k)) for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
assert changed == {"34": ("CHANNEL_UP", "CHANNEL_DOWN"), "35": ("CHANNEL_DOWN", "CHANNEL_UP")}, changed
print("ok: only scan codes 34 and 35 changed, swapped; no duplicates")
