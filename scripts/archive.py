#!/usr/bin/env python3
"""
Opus Delta — Transmission Archiver
Reads the current transmission from README.md and appends it
to a monthly archive file in /transmissions.
"""

import os
import datetime
import re


def get_current_transmission(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!-- TRANSMISSION:START -->"
    end = "<!-- TRANSMISSION:END -->"

    if start in content and end in content:
        tx = content.split(start)[1].split(end)[0].strip()
        return tx
    return None


def archive_transmission(tx, archive_dir):
    now = datetime.datetime.utcnow()
    filename = now.strftime("%Y-%m") + ".md"
    filepath = os.path.join(archive_dir, filename)

    header = f"# 📡 Transmissions — {now.strftime('%B %Y')}\n\n"
    header += f"Archived signals from the Opus Delta system.\n\n---\n\n"

    date_label = now.strftime("### %Y.%m.%d\n\n")

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing = f.read()
        # Check if today's date already exists
        if now.strftime("%Y.%m.%d") in existing:
            print(f"⊘ Already archived for {now.strftime('%Y.%m.%d')}")
            return
        content = existing + "\n---\n\n" + date_label + tx + "\n"
    else:
        content = header + date_label + tx + "\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ Archived to {filename}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(base_dir, "README.md")
    archive_dir = os.path.join(base_dir, "transmissions")

    os.makedirs(archive_dir, exist_ok=True)

    tx = get_current_transmission(readme_path)
    if tx:
        archive_transmission(tx, archive_dir)
    else:
        print("✗ No transmission found in README.md")
        exit(1)
