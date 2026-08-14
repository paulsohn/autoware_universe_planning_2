#!/usr/bin/env python3
"""Reparent a single-commit git-fast-export stream onto new_parent
(argv[1], empty meaning "make it a root commit") instead of its original
parent. File-change lines are passed through unmodified: since the two
source histories never touch the same paths, replaying them onto an
unrelated parent tree never conflicts.
"""
import sys


def main():
    new_parent = sys.argv[1].strip()
    new_parent_bytes = new_parent.encode() if new_parent else None

    raw = sys.stdin.buffer.read()
    out = bytearray()
    i, n = 0, len(raw)

    in_commit = False
    message_data_seen = False
    from_handled = False

    while i < n:
        nl = raw.index(b'\n', i)
        line = raw[i:nl + 1]

        if line.startswith(b'commit '):
            in_commit = True
            message_data_seen = False
            from_handled = False
            out += b'commit refs/heads/awf-latest-combined\n'
            i = nl + 1
            continue

        if line.startswith(b'data '):
            length = int(line[5:].strip())
            out += line
            i = nl + 1
            out += raw[i:i + length]
            i += length
            if in_commit:
                message_data_seen = True
            continue

        if line.startswith(b'from ') and in_commit and message_data_seen:
            if new_parent_bytes is None:
                sys.exit('unexpected parent on what should be a root commit')
            out += b'from ' + new_parent_bytes + b'\n'
            from_handled = True
            i = nl + 1
            continue

        is_filechange = (
            line.startswith(b'M ') or line.startswith(b'D ')
            or line.startswith(b'C ') or line.startswith(b'R ')
            or line.startswith(b'N ') or line.rstrip(b'\n') == b'deleteall'
        )
        if in_commit and message_data_seen and not from_handled and is_filechange:
            if new_parent_bytes is not None:
                out += b'from ' + new_parent_bytes + b'\n'
            from_handled = True

        out += line
        i = nl + 1

    sys.stdout.buffer.write(out)


if __name__ == '__main__':
    main()
