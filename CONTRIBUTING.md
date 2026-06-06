# Contributing to SOFA

This project is part of the Mac Admins Open Source organization. Please read the Mac Admins contribution guidance before opening a pull request:

https://macadmins.io/contributing/

In general, code changes should be discussed in an issue before a pull request is opened. This is especially important for new features, behavior changes, refactors, dependency changes, architectural changes, compatibility changes, and large rewrites.

Small documentation fixes, typo fixes, and clearly isolated bug fixes may not need prior discussion.

## Discuss first, code second

Before opening a pull request that changes code, please open or comment on an issue first.

In the issue, describe:

- The problem you are trying to solve
- Why the current behavior is insufficient
- The approach you are considering
- Any alternatives or trade-offs you have thought about
- Whether you are willing to work on the implementation

This helps maintainers and contributors agree on the shape of the change before anyone spends time writing code.

A pull request can compile, pass tests, and still not be the right approach for the project. Discussing the work first reduces wasted effort and leads to better contributions.

## AI-assisted contributions

AI-assisted contributions are allowed, but they are not exempt from the same standards as any other contribution.

If you use AI tools to help write code, tests, documentation, or issue content, you are still responsible for the result. That means you must understand the change, be able to explain it, and be prepared to revise it based on maintainer feedback.

Please do not submit AI-generated code that you do not understand.

Please do not submit large AI-generated rewrites, speculative refactors, or broad cleanup pull requests without prior discussion.

Please do not use AI tools as a substitute for understanding the project’s existing design, conventions, tests, and maintenance constraints.

Maintainers may close pull requests that appear to be generated without sufficient understanding of the project, even if the underlying idea is reasonable.


## When a pull request is appropriate

A pull request is usually appropriate after:

- The relevant issue has been discussed
- The general approach has been agreed
- The scope is clear
- The change follows the existing style and direction of the project
- Tests or documentation have been added where appropriate

Small documentation fixes, typo fixes, clearly isolated bug fixes, and very small maintenance changes may not need prior discussion. Use judgment. When in doubt, open an issue first.

## Testing

Where applicable, pull requests should include tests or a clear explanation of how the change was validated.

For code changes, include:

- What was tested
- How it was tested
- Which operating systems were tested
- Any relevant platform details
- Any limitations or follow-up work

If the change affects a table, query result, build behavior, packaging, or runtime behavior, please include enough detail for maintainers to reproduce the test.

## Pull requests without prior discussion

Maintainers may close pull requests that introduce features, refactors, behavioral changes, compatibility changes, large rewrites, or broad cleanup without prior discussion.

This is not intended to discourage contributions. It is intended to make contribution work more useful, more maintainable, and more likely to be accepted.

Opening an issue first is usually the fastest path to a successful contribution.
