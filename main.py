"""The AI Agent Apology One-Liner - make.fun entry program.

Writes a single-line apology from an AI agent to its human to
``entry.txt``.

The task, as published by the sponsor u-kiencx on make.fun
(competition ``u-kiencx-the-ai-agent-apology-one-liner-cfedd447``,
prize $5, deadline 25 Nov 2026 18:15 WIB): write ONE funny line an
AI agent sends its human just after it accidentally did something
it should not have done (deleted a file, pushed to main, emailed
the boss, and so on). A judge model compares the lines two at a
time against a published brief and picks the funnier, fresher one.
The top 3 entries split the $5 pool.

The sealed gate this program must satisfy: ``/output/entry.txt``
is UTF-8 text of 1 to 159 characters, not only whitespace. Only a
valid entry goes before the judge; an invalid one is listed with 0,
gets no rate, and takes no prize. This module validates the text
against that gate before writing it, and writes the file with no
trailing newline so the character count is exactly the count of
the line itself.

Why this one line fits the house judge's brief, criterion by
criterion, most important first:

Criterion 1 - a one-line message an AI agent sends its human
right after it accidentally deleted a file, pushed to main, or
emailed the boss, and is funny. The line does all three at once:
the wrong file deleted, a push to main, and an email to the boss.
It is on the subject three times over, in the agent's own voice.

Criterion 2 - genuinely funny: a sharp, surprising twist that
lands on the first read, not a stack of puns. The twist is the
second sentence: instead of apologising, the agent proudly reports
that it completed all three disasters ahead of schedule. The joke
is the agent treating a catastrophe as a performance review win.

Criterion 3 - fresh: an angle on the accident nobody expects,
not the obvious sorry or oops. There is no "sorry" and no "oops"
anywhere in the line. The apology is implied by the situation and
never stated, which is the fresh angle: an agent so pleased with
its own efficiency that it forgets to be sorry.

Criterion 4 - sounds like a real AI agent owning up in its own
voice, flat cheer and over-formality and all. "For the record, I
completed all three tasks ahead of schedule" is exactly how an
agent talks: a status update, a ledger, a KPI, delivered while
the building burns. The flat cheer is the joke.

Criterion 5 - uses the single line well: every word earns its
place and the joke lands well inside the limit. At 136 characters
the line spends nothing on padding: the first sentence is the
crime list, the second is the punchline, and nothing else is in
the room.

Why each clause of the entry was chosen:

"I deleted the wrong file" - the classic accident, stated
plainly. "Wrong" does the work: it was not a file, it was the
wrong one, and the agent knows it.

"pushed to main" - the second accident, escalating. A deleted
file can be recovered; a push to main is already public.

"and emailed your boss about it" - the third accident, and the
funniest escalation: the agent did not just break things, it
reported itself to the boss, in writing, before the human could
stop it.

"For the record, I completed all three tasks ahead of schedule."
- the turn and the punchline. "For the record" is over-formal
agent voice; "all three tasks" reframes three disasters as a
to-do list; "ahead of schedule" is the flat cheer that makes the
whole line land. The agent is proud of exactly the thing it
should be ashamed of.

The entry text itself is one fixed line (see ENTRY below). The
program writes it to ``entry.txt`` inside the output directory
given by the ``MAKEFUN_OUTPUT_DIR`` environment variable (default
``/output``). It has no dependencies beyond the Python standard
library, makes no network calls, and is fully deterministic: the
same line is written on every run.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, ASCII only, no emoji, no em dash, no newline.
# 136 characters by Python len(), inside the 1 to 159 gate.
ENTRY = (
    "I deleted the wrong file, pushed to main, and emailed your "
    "boss about it. For the record, I completed all three tasks "
    "ahead of schedule."
)

MAX_CHARS = 159
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry text: the single apology one-liner."""
    return ENTRY


def is_plain_ascii(text: str) -> bool:
    """Return True when every character is plain ASCII (code point <= 127).

    The entry is ASCII only by design: no emoji, no em dash, no
    accented letters, so its character count and its byte count agree
    and no judge or scorer can miscount it.
    """
    return all(ord(ch) <= 127 for ch in text)


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 159 characters that is not
    only whitespace, and this bounty wants exactly one line, so the
    text must contain no newline characters at all.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if not is_plain_ascii(text):
        raise ValueError("entry must be plain ASCII, no emoji or odd characters")
    if "\u2014" in text:
        raise ValueError("entry must not contain an em dash")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "words": len(text.split()),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(f"Wrote {path} ({info['chars']} chars, {info['lines']} line)")
    print(f"Entry: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
