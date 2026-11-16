"""Share immutable design inputs; rerun the real daily validator for each mutant."""
from functools import lru_cache
import json
from typing import Any

import verify_design_deliverables as validator


@lru_cache(maxsize=1)
def design_inputs() -> tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    return (
        validator.read_csv(validator.OUT / 'reverse_lectionary_presentation.csv'),
        json.loads((validator.OUT / 'lectionary_schema.json').read_text()),
        json.loads((validator.OUT / 'BUILD_DESIGN_SUMMARY.json').read_text()),
    )


@lru_cache(maxsize=1)
def validate_design_baseline() -> None:
    # Full corpus acceptance is shared only outside mutation patches. Authentication
    # and exact daily comparison still execute afresh for every negative control.
    validator.verify_rows()


def verify_daily_artifacts() -> None:
    validator.verify_daily_rows(*design_inputs())
