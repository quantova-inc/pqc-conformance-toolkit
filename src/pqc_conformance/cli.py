from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pqc_conformance.model import load_corpus
from pqc_conformance.runner import Report, run_corpus


def _print_report(report: Report) -> None:
    for result in report.results:
        mark = "pass" if result.passed else "FAIL"
        line = f"[{mark}] {result.case.id}  expect {result.case.expect}  observed {result.observed}"
        if result.case.reject_class:
            line += f"  class {result.case.reject_class}"
        print(line)
    print("")
    print(f"total {report.total}  passed {report.total - len(report.failures)}  failed {len(report.failures)}")
    forgeries = report.accepted_a_forgery
    if forgeries:
        print("")
        print("A verifier accepted a signature it was required to refuse.")
        for result in forgeries:
            print(f"  {result.case.id}  class {result.case.reject_class}  {result.case.fips_clause}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pqc-conformance",
        description="Run a post quantum signature verifier against a corpus of accept and reject cases",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="run a verifier against a corpus")
    run.add_argument("--corpus", required=True, help="path to a corpus manifest")
    run.add_argument(
        "--verifier",
        required=True,
        help="verifier command using the placeholders {pk} {msg} {sig}",
    )
    run.add_argument(
        "--base-dir",
        default=None,
        help="directory the manifest paths are relative to, defaults to the manifest directory",
    )

    args = parser.parse_args(argv)

    if args.command == "run":
        manifest = Path(args.corpus)
        base_dir = args.base_dir if args.base_dir is not None else str(manifest.parent)
        cases = load_corpus(manifest)
        report = run_corpus(cases, args.verifier, base_dir)
        _print_report(report)
        return 0 if report.ok else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
