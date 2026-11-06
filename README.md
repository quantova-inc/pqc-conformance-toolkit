# pqc-conformance-toolkit

A verifier agnostic harness that tests a post quantum signature verifier against a corpus of accept and reject cases. It runs any verifier you point it at, a stock OpenSSL that offers ML-DSA, your own library, or a hardware module, and it fails the moment a verifier accepts a signature it was required to refuse.

Built by [Quantova Inc](https://quantova.org). The reject and accept vectors it runs on come from [quantova-inc/pq-sign-vectors](https://github.com/quantova-inc/pq-sign-vectors), produced with a stock OpenSSL so any reviewer can reproduce them and nothing depends on one implementation.

## Why the reject half matters

Checking that a genuine signature verifies is the easy half of interop and it is already well covered. The half that carries the security is the refusal. A conforming verifier must reject a tampered signature, a signature with a hint over the bound, a response that is out of range, and a signature of the wrong length. A verifier that accepts any of these has a hole, and the hole does not show up in accept only testing.

For banking, payments and government systems moving to post quantum signatures under the United States, European Union and Japan migration deadlines, the assurance question is not only does the right signature verify. It is does the system refuse the wrong one every time. This toolkit answers that question for ML-DSA from FIPS 204 and SLH-DSA from FIPS 205.

## What it does

- Loads a corpus manifest of accept and reject cases, each reject case naming the verification step that refuses it.
- Runs your verifier against every case using the placeholders `{pk}`, `{msg}` and `{sig}`.
- Reports a pass or fail per case and exits nonzero if any case is wrong.
- Calls out, in plain words, any case where a verifier accepted a signature it was required to refuse.

## Install

```
pip install .
```

Python 3.9 or newer. The harness itself has no third party dependencies.

## Quick check

A smoke run with the bundled stand in verifier, which performs no cryptography and only exercises the harness.

```
pqc-conformance run \
  --corpus corpus/ml-dsa-65-reject.tsv \
  --verifier "python tests/mock_verifier.py {pk} {msg} {sig}" \
  --base-dir tests/fixtures
```

## Run against the reference corpus

Clone the vectors and point the harness at the `reject-vectors` directory with a real ML-DSA verifier.

```
git clone https://github.com/quantova-inc/pq-sign-vectors
pqc-conformance run \
  --corpus corpus/ml-dsa-65-reject.tsv \
  --base-dir pq-sign-vectors/reject-vectors \
  --verifier "<your ML-DSA verify command> {pk} {msg} {sig}"
```

The verify command returns zero to accept and nonzero to refuse. The `verify.sh` script in pq-sign-vectors shows a working OpenSSL command for ML-DSA.

## The reference reject profile

`corpus/ml-dsa-65-reject.tsv` is a reference profile for ML-DSA-65. Each reject case maps to the FIPS 204 verification step a conforming verifier uses to refuse it. The classes and their meaning are described in [METHODOLOGY.md](METHODOLOGY.md). The same shape extends to ML-DSA-44, ML-DSA-87 and to SLH-DSA from FIPS 205.

## Related contributions to NIST

While building this, Quantova reported and opened fixes in the NIST cryptographic validation code and documents. These are open pull requests under review.

- ACVP-Server pull request 486, a server fault in the base ML-KEM parameter validators on a missing registration array.
- ACVP-Server pull request 488, the same fault in the base ML-DSA keyGen validator.
- ACVP-Server pull request 489, an LMS registration with no capabilities wrongly accepted.
- ACVP-Server pull request 487, an SLH-DSA validator naming the wrong algorithm in its messages.
- ACVP pull request 1648, a correction to the ML-KEM functions applicability note.

## Contributing

Reject classes for SLH-DSA, verifier adapters for common libraries, and the ML-DSA-44 and ML-DSA-87 profiles are good first contributions. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache-2.0 OR MIT. See [LICENSE-APACHE](LICENSE-APACHE) and [LICENSE-MIT](LICENSE-MIT).
