from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from pqc_conformance.model import Case


@dataclass(frozen=True)
class CaseResult:
    case: Case
    observed: str
    passed: bool
    detail: str = ""


@dataclass
class Report:
    results: List[CaseResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def failures(self) -> List[CaseResult]:
        return [r for r in self.results if not r.passed]

    @property
    def ok(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def accepted_a_forgery(self) -> List[CaseResult]:
        return [
            r for r in self.results
            if not r.passed and r.case.expect == "reject" and r.observed == "accept"
        ]


def _resolve(base_dir: Path, value: str) -> str:
    if not value:
        return value
    return str((base_dir / value).resolve())


def run_case(case: Case, verifier: str, base_dir: str | Path = ".") -> CaseResult:
    """Run one case through a verifier command.

    The verifier command may use the placeholders {pk}, {msg} and {sig}. The
    command exit code decides the observed verdict, zero means accept and any
    other value means reject. The observed verdict is then compared to the
    verdict the corpus expects.
    """
    base = Path(base_dir)
    filled = (
        verifier
        .replace("{pk}", _resolve(base, case.public_key))
        .replace("{msg}", _resolve(base, case.message))
        .replace("{sig}", _resolve(base, case.signature))
    )
    try:
        completed = subprocess.run(
            shlex.split(filled),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        observed = "accept" if completed.returncode == 0 else "reject"
        detail = f"exit {completed.returncode}"
    except FileNotFoundError as error:
        return CaseResult(case=case, observed="error", passed=False, detail=str(error))

    passed = observed == case.expect
    return CaseResult(case=case, observed=observed, passed=passed, detail=detail)


def run_corpus(cases: List[Case], verifier: str, base_dir: str | Path = ".") -> Report:
    report = Report()
    for case in cases:
        report.results.append(run_case(case, verifier, base_dir))
    return report
