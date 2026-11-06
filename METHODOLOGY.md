# Reject class methodology

A verifier earns trust through two behaviours. It accepts a genuine signature and it refuses every signature that fails any required check. Known answer and accept testing cover the first behaviour and are well supported across the libraries that now ship post quantum signatures. The second behaviour, refusal, is the half that carries the security and the half that a curated corpus usually does not reach.

This document defines the reject classes for ML-DSA from FIPS 204 and SLH-DSA from FIPS 205. A reject class is a single independent reason a conforming verifier refuses a signature. A corpus holds at least one case per class, and a verifier passes only when it refuses every reject case while accepting the genuine signature.

## ML-DSA reject classes from FIPS 204

The reference profile `corpus/ml-dsa-65-reject.tsv` carries one case per class for ML-DSA-65. The same classes apply to ML-DSA-44 and ML-DSA-87.

- `flip_ctilde`. The commitment hash c tilde in the signature is altered. FIPS 204 verification recomputes the commitment hash from the recovered value and compares it to the c tilde in the signature. An altered c tilde does not match and the verifier refuses.
- `z_out_of_range`. A coefficient of the response z lies outside the interval that FIPS 204 allows, which is bounded by gamma1 minus beta. A verifier that checks the infinity norm of z refuses a coefficient outside the interval.
- `hint_over_omega`. The hint sets more than omega positions. FIPS 204 bounds the number of set positions in the hint by omega, and a hint over the bound is refused.
- `hint_noncanonical`. The hint is not in canonical encoded form. FIPS 204 fixes the hint encoding and a verifier that decodes strictly refuses a hint that does not match the canonical layout.
- `wrong_length`. The signature is shorter or longer than the fixed length for the parameter set. FIPS 204 fixes the signature length at 2420 bytes for ML-DSA-44, 3309 for ML-DSA-65 and 4627 for ML-DSA-87. A signature of any other length is refused before any arithmetic.

## SLH-DSA reject classes from FIPS 205

The SLH-DSA corpus in `pq-sign-vectors/slh-dsa-reject` covers all twelve parameter sets across the SHA2 and SHAKE families at the 128, 192 and 256 levels in both the small and fast variants. It is produced with a stock OpenSSL that offers native SLH-DSA in the pure mode with the empty context, 78 cases in total, 12 accept and 66 reject.

- `bit_flip_first`. A bit is flipped in the first signature byte. The recomputed hypertree root no longer matches the public key root and the verifier refuses.
- `bit_flip_middle`. A bit is flipped in the middle of the signature, reaching a different WOTS or tree node, and the recomputed root no longer matches.
- `wrong_public_key`. A genuine signature is verified against a different public key of the same scheme. The roots differ and the verifier refuses.
- `one_byte_short`. The signature is one byte shorter than the fixed length for the parameter set and is refused on the length check.
- `one_byte_long`. The signature is one byte longer than the fixed length and is refused on the length check.
- `cross_family`. A SHA2 signature is verified under a same size SHAKE key, or the reverse. The sizes match but the hash family does not, and a verifier that binds the parameter set to the key refuses it. This class catches a routing mistake that length alone cannot catch.

## How this complements ACVP

The ACVP signature verification test type already exercises some refusal, and this profile organises that refusal into named independent classes tied to the FIPS 204 and FIPS 205 verification steps. A profile of this shape lets a laboratory and a vendor point at the same class list, so agreement means two independent implementations refused the same case for the same reason rather than one implementation checking itself.

## Reproducibility

Every vector in the reference corpus is produced and checked with a stock OpenSSL that offers ML-DSA and SLH-DSA. The corpus shares no code with any other verifier, so a verifier that agrees with it has agreed across two independent implementations. The generation and verification scripts live in `pq-sign-vectors`.
