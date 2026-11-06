from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pqc_conformance.model import Case, load_corpus
from pqc_conformance.runner import run_corpus

MOCK = Path(__file__).resolve().parent / "mock_verifier.py"


def _write(path: Path, data: bytes = b"x") -> Path:
    path.write_bytes(data)
    return path


def _fixture(tmp_path: Path):
    _write(tmp_path / "pk.der")
    _write(tmp_path / "message.bin")
    _write(tmp_path / "valid.sig")
    _write(tmp_path / "reject_flip.sig")
    cases = [
        Case("ok", "ML-DSA-65", "accept", "", "message.bin", "pk.der", "valid.sig", "FIPS 204", "genuine"),
        Case("flip", "ML-DSA-65", "reject", "flip_ctilde", "message.bin", "pk.der", "reject_flip.sig", "FIPS 204", "tampered"),
    ]
    return cases


def test_honest_verifier_passes_every_case(tmp_path: Path):
    cases = _fixture(tmp_path)
    verifier = f"{sys.executable} {MOCK} {{pk}} {{msg}} {{sig}}"
    report = run_corpus(cases, verifier, base_dir=tmp_path)
    assert report.ok
    assert report.total == 2
    assert report.failures == []


def test_a_verifier_that_accepts_a_forgery_fails(tmp_path: Path):
    cases = _fixture(tmp_path)
    always_accept = f"{sys.executable} -c pass"
    report = run_corpus(cases, always_accept, base_dir=tmp_path)
    assert not report.ok
    forgeries = report.accepted_a_forgery
    assert len(forgeries) == 1
    assert forgeries[0].case.id == "flip"


def test_reject_case_without_a_class_is_rejected():
    with pytest.raises(ValueError):
        Case("bad", "ML-DSA-65", "reject", "", "m", "pk", "s", "", "").validate()


def test_load_corpus_reads_the_reference_manifest():
    manifest = Path(__file__).resolve().parents[1] / "corpus" / "ml-dsa-65-reject.tsv"
    cases = load_corpus(manifest)
    assert any(c.expect == "accept" for c in cases)
    assert any(c.expect == "reject" and c.reject_class for c in cases)
    for case in cases:
        case.validate()
