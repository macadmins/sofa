"""Fail before fetching data if the runner still trusts affected emSign paths."""

import hashlib
import ssl
import sys


# emSign ECC Root CA - G3 and Sectigo's AAA Certificate Services cross-sign.
# https://emudhra.we-have-a-problem.com/#linux
REMOVED_ROOTS = {
    "86a1ecba089c4a8d3bbe2734c612ba341d813e043cf9e8a862cd5c57a36bbe6b",
    "d7a7a0fb5d7e2731d771e9484ebcdef71d5f0c3e0a2948782bc83ee0ea699ef4",
}


def main():
    context = ssl.create_default_context(cafile=sys.argv[1])
    fingerprints = {
        hashlib.sha256(cert).hexdigest()
        for cert in context.get_ca_certs(binary_form=True)
    }
    if not fingerprints or REMOVED_ROOTS & fingerprints:
        raise SystemExit("CA bundle is empty or still trusts affected emSign paths")
    print(f"Verified {len(fingerprints)} roots in {sys.argv[1]}")


if __name__ == "__main__":
    main()
