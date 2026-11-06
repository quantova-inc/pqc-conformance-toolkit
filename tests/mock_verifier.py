"""A stand in verifier for tests and smoke runs.

It accepts a signature whose file name contains the word valid and refuses
every other signature. It performs no cryptography and is only here so the
harness can be exercised without a real verifier.
"""
import sys


def main() -> int:
    signature = sys.argv[-1].lower()
    return 0 if "valid" in signature else 1


if __name__ == "__main__":
    sys.exit(main())
