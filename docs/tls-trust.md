# CI trust after the eMudhra/emSign incident

Both data pipelines update Ubuntu's CA/OpenSSL packages and reject the run if
the resulting CA bundle still contains emSign ECC Root CA - G3 or AAA Certificate
Services (the cross-sign path). The published Linux `sofa-fetch` binaries used by
these pipelines use native OpenSSL for their HTTP requests, so updating the
actual runner store matters even though the tools are written in Rust.

Both workflows pin uv 0.13.4, which includes the fixed bundled trust roots.
Updating Python dependencies alone would not update uv's own TLS trust.

The trust check runs before downloading tools or fetching data. Custom roots,
client-specific CA overrides, and future upstream binary TLS backend changes
need separate validation. Do not add `--insecure` or disable verification to
work around a failure. The checker can be run manually:

```sh
python3 scripts/verify_trust_store.py /etc/ssl/certs/ca-certificates.crt
```

Reference and fixed versions: <https://emudhra.we-have-a-problem.com/#developers>.
