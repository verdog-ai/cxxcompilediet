"""The package's payload."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Payload:
    """The subroutines carry their own boundary types; this one is empty."""
