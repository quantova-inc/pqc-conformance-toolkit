from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

FIELDS = [
    "id",
    "parameter_set",
    "expect",
    "reject_class",
    "message",
    "public_key",
    "signature",
    "fips_clause",
    "note",
]

VALID_EXPECT = {"accept", "reject"}


@dataclass(frozen=True)
class Case:
    id: str
    parameter_set: str
    expect: str
    reject_class: str
    message: str
    public_key: str
    signature: str
    fips_clause: str
    note: str

    def validate(self) -> None:
        if self.expect not in VALID_EXPECT:
            raise ValueError(
                f"case {self.id} has expect {self.expect}, use accept or reject"
            )
        if self.expect == "reject" and not self.reject_class:
            raise ValueError(f"reject case {self.id} must name a reject_class")


def load_corpus(path: str | Path) -> List[Case]:
    """Read a tab separated corpus manifest.

    A header row names the columns. Lines that start with a hash are ignored.
    """
    path = Path(path)
    rows: List[Case] = []
    header: List[str] = []
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            cells = line.split("\t")
            if not header:
                header = [c.strip() for c in cells]
                missing = [f for f in ("id", "expect") if f not in header]
                if missing:
                    raise ValueError(f"manifest {path} is missing columns {missing}")
                continue
            values = {name: "" for name in FIELDS}
            for name, cell in zip(header, cells):
                if name in values:
                    values[name] = cell.strip()
            case = Case(**values)
            case.validate()
            rows.append(case)
    if not rows:
        raise ValueError(f"manifest {path} has no cases")
    return rows
