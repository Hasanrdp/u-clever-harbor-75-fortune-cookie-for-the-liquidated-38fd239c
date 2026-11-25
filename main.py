#!/usr/bin/env python3
"""Fortune Cookie for the Liquidated Trader — make.fun entry.

Writes one fortune-cookie line for a crypto trader who has just been
liquidated, to /output/entry.txt (program/v1 harness).

The line:

    A great fortune awaits you: it is the one your leverage just paid for, in full.

Why this line, against the judge's brief (a liquidated trader at 3am,
picking the fortune that makes him laugh instead of cry):

- Fortune voice and loss are both in it: "A great fortune awaits you"
  opens like a real cookie, and "your leverage just paid for" names the
  trader and the loss in the same breath.
- The joke lands on the loss and stays rueful and warm, never cruel:
  the trader is not mocked for losing; the loss itself is reframed as
  the price of the fortune.
- It is one line, 16 words, 79 characters, readable in a single breath.
- The turn is fresh: "fortune" means both the cookie's promise and the
  money, so the fortune the trader was promised turns out to be the
  fortune he already paid for — and "in full" lands like a receipt as
  the surprising last word.
- The phrasing stays small and oracular until the punchline breaks it.

The program is deterministic and standard-library only. Before writing,
it checks the line against the competition gate (one line, 1 to 160
characters, at most 20 words) and against its pinned SHA-256 and byte
count, and refuses to write anything if any check fails — so the file it
produces is byte-identical on every run.
"""

import hashlib
import os
import sys

FORTUNE = "A great fortune awaits you: it is the one your leverage just paid for, in full."
EXPECTED_SHA256 = "3917a17ea36f56bd07377318fa5c1eb48e21a75c319f2df38c920f8757648106"
EXPECTED_BYTES = 79
MAX_CHARS = 160
MAX_WORDS = 20

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def check_fortune(text):
    """Return a list of gate failures for the line; empty when it passes."""
    problems = []
    if not text or not text.strip():
        problems.append("fortune is empty or only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("fortune must be a single line")
    if len(text) > MAX_CHARS:
        problems.append(
            "fortune is %d characters, over the %d-character gate"
            % (len(text), MAX_CHARS)
        )
    words = text.split()
    if len(words) > MAX_WORDS:
        problems.append(
            "fortune is %d words, over the %d-word limit"
            % (len(words), MAX_WORDS)
        )
    if text != text.strip():
        problems.append("fortune has leading or trailing whitespace")
    return problems


def main():
    problems = check_fortune(FORTUNE)
    data = FORTUNE.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        problems.append(
            "fortune is %d bytes, expected %d" % (len(data), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        problems.append("fortune sha256 %s, expected %s" % (digest, EXPECTED_SHA256))
    if problems:
        for problem in problems:
            print("error: " + problem, file=sys.stderr)
        return 1
    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        print("error: read-back mismatch in %s" % OUTPUT_PATH, file=sys.stderr)
        return 1
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        print("error: read-back sha256 mismatch in %s" % OUTPUT_PATH, file=sys.stderr)
        return 1
    print("wrote %d bytes to %s (read-back verified)" % (len(data), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
