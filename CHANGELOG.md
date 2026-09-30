# CHANGELOG


## v1.3.1 (2026-09-30)

### Bug Fixes

- Move onto the renamed arkitekt packages
  ([`c9c5047`](https://github.com/jhnnsrs/herre-next/commit/c9c5047836c4b68d1e4905b214bbbda89952b79b))

The *-next distributions were folded back onto their original PyPI names, so fakts_next,
  rekuest_next, mikro_next and fluss_next no longer exist. Imports and dependency floors now point
  at what actually shipped: fakts>=2, rekuest>=3, mikro>=3, fluss>=2.

These integrations sit behind try/except on the importing side, so the stale module paths never
  raised -- the features just silently went missing.

### Documentation

- Mark this package deprecated
  ([`3e3fef3`](https://github.com/jhnnsrs/herre-next/commit/3e3fef315ae3ad3ae7cfd1556cd7ed8925b5f49c))

It is no longer maintained. Its last release was 1.3.0 (2025-05-14).

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_018y7X4q6UvWWUyY1xYaEoK7


## v1.3.0 (2025-05-14)

### Bug Fixes

- Add qtpy dependency to development environment
  ([`9f960a9`](https://github.com/jhnnsrs/herre-next/commit/9f960a9d15b15947fb9a0f934037021c6cf32d8e))

### Features

- Enhance pydantic model configuration and add type hints
  ([`c74d6f5`](https://github.com/jhnnsrs/herre-next/commit/c74d6f5c2e5c844ba8d10f6eedf2a8e412e6ea37))

- Updated koil dependeny
  ([`a8b1e7b`](https://github.com/jhnnsrs/herre-next/commit/a8b1e7bbf50540a481376f2c4b6e8dc14e6956d1))


## v1.2.0 (2025-05-12)

### Bug Fixes

- Update project description for clarity
  ([`a12c5c5`](https://github.com/jhnnsrs/herre-next/commit/a12c5c5f586340e70b14e5ed83e8a4461dc62603))

### Features

- Add typing and added testing
  ([`e0e1e17`](https://github.com/jhnnsrs/herre-next/commit/e0e1e17136db5bdb22a92eb561b8932750d9fd86))


## v1.1.0 (2024-11-27)
