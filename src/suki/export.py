"""suki-export: back up or restore the full ~/.suki state.

Usage:
  suki export [dest.tgz]          # default: ./suki-backup-YYYY-MM-DD.tgz
  suki import <file.tgz>          # restore, never clobber (merges)

Export tars the entire SUKI_HOME. Import extracts into SUKI_HOME without
overwriting anything that already exists, preserving the accumulate-don't-
overwrite rule.
"""
import argparse
import datetime as dt
import os
import shutil
import sys
import tarfile
import tempfile

SUKI_HOME = os.environ.get("SUKI_HOME", os.path.expanduser("~/.suki"))


def default_dest():
    today = dt.date.today().strftime("%Y-%m-%d")
    return os.path.join(os.getcwd(), f"suki-backup-{today}.tgz")


def cmd_export(dest):
    if not os.path.isdir(SUKI_HOME):
        print(f"nothing to export: {SUKI_HOME} does not exist", file=sys.stderr)
        return 1
    with tarfile.open(dest, "w:gz") as tf:
        tf.add(SUKI_HOME, arcname="suki")
    print(f"exported {SUKI_HOME} -> {dest}")
    return 0


def cmd_import(src):
    if not os.path.isfile(src):
        print(f"no such backup: {src}", file=sys.stderr)
        return 1
    try:
        with tarfile.open(src, "r:gz") as tf:
            root = tf.getmembers()[0].name if tf.getmembers() else "suki"
            tmp = tempfile.mkdtemp(prefix="suki-import-")
            tf.extractall(tmp)
    except (tarfile.TarError, IndexError, OSError) as e:
        print(f"invalid backup: {e}", file=sys.stderr)
        return 1

    base = os.path.join(tmp, root)
    copied = 0
    skipped = 0
    for dirpath, _dirs, files in os.walk(base):
        rel = os.path.relpath(dirpath, base)
        for name in files:
            dst = os.path.join(SUKI_HOME, rel, name)
            if os.path.exists(dst):
                skipped += 1
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(dirpath, name), dst)
            copied += 1
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"imported {copied} file(s) into {SUKI_HOME}; skipped {skipped} existing")
    return 0


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser(description="Back up or restore ~/.suki state.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_exp = sub.add_parser("export", help="tar the state into a .tgz")
    p_exp.add_argument("dest", nargs="?", default=None)
    p_imp = sub.add_parser("import", help="merge a backup back into state")
    p_imp.add_argument("src")
    args = ap.parse_args(argv)

    if args.cmd == "export":
        return cmd_export(args.dest or default_dest())
    return cmd_import(args.src)


if __name__ == "__main__":
    sys.exit(main())
