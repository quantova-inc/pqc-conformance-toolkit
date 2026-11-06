# Contributing

Contributions that widen the reject coverage for post quantum signatures are welcome. The aim is a corpus and a harness that a laboratory, a vendor and a reviewer can all point at, so that agreement means two independent implementations refused the same case for the same reason.

## Good first contributions

- An SLH-DSA reject profile as a corpus manifest, drawing on the cases in `pq-sign-vectors/slh-dsa-reject`.
- The ML-DSA-44 and ML-DSA-87 reference profiles alongside the ML-DSA-65 one.
- A verifier adapter for a common library so a user does not have to write the verify command by hand.
- A new reject class with a FIPS 204 or FIPS 205 citation and a case that exercises it.

## Add a reject case

A corpus manifest is a tab separated file with a header row. Each row carries an id, the parameter set, the expected result of accept or reject, a reject class for reject cases, the message, the public key and the signature paths, the FIPS clause, and a short note. Paths are relative to the base directory passed on the command line. Every reject case must name the verification step that refuses it.

## Add a verifier adapter

A verifier is any command that returns zero to accept and nonzero to refuse, using the placeholders `{pk}`, `{msg}` and `{sig}`. If a library needs more than a one line command, add a small wrapper script under a `verifiers` directory and document it.

## Run the checks

```
pip install pytest
PYTHONPATH=src python -m pytest tests -q
```

A new reject case should come with a note that explains why a conforming verifier refuses it, and should verify under the reference OpenSSL before it is added.

## How I review

Only Quantova maintainers merge. Automatic merging is off. No contribution reaches the main branch without review and approval by a maintainer. State in the pull request whether any part of the contribution was produced with the help of an automated tool, so a reviewer can read it line by line.

## License

By contributing you agree that your contribution is licensed under Apache-2.0 OR MIT, the same terms as the project.
