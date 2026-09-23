"""Exercise mutation result failures without running the full mutator."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.check_mutation import main, module_results, summarize

MODULE = Path("src/volcano_sdk/probe.py")


def write_results(tmp_path: Path, results: object) -> None:
    metadata = tmp_path / "mutants" / f"{MODULE}.meta"
    metadata.parent.mkdir(parents=True)
    metadata.write_text(json.dumps({"exit_code_by_key": results}), encoding="utf-8")


@pytest.mark.parametrize(
    ("code", "outcome"),
    [
        (0, "survived"),
        (5, "uncovered"),
        (33, "uncovered"),
        (3, "crashed"),
        (-11, "crashed"),
        (36, "timed_out"),
        (None, "incomplete"),
        (34, "incomplete"),
        (37, "incomplete"),
    ],
)
def test_failed_mutants_keep_distinct_outcomes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, code: int | None, outcome: str
) -> None:
    monkeypatch.chdir(tmp_path)
    write_results(tmp_path, {"volcano_sdk.probe.x__f__mutmut_1": code})
    assert main([MODULE]) == 1
    report = json.loads(Path("reports/mutation.json").read_text(encoding="utf-8"))
    assert report["outcomes"] == {outcome: 1}
    assert report["failures"] == [
        f"volcano_sdk.probe.x__f__mutmut_1: {outcome} (exit {code})"
    ]


def test_all_mutants_must_be_killed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    write_results(tmp_path, {"volcano_sdk.probe.x__f__mutmut_1": 1})
    assert main([MODULE]) == 0
    assert summarize([MODULE])["outcomes"] == {"killed": 1}


def test_missing_metadata_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="Missing mutmut metadata"):
        module_results(MODULE)


@pytest.mark.parametrize(
    "payload", [{}, {"exit_code_by_key": []}, {"exit_code_by_key": {"bad": "1"}}]
)
def test_malformed_metadata_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, payload: object
) -> None:
    monkeypatch.chdir(tmp_path)
    metadata = tmp_path / "mutants" / f"{MODULE}.meta"
    metadata.parent.mkdir(parents=True)
    metadata.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid mutmut metadata"):
        module_results(MODULE)


def test_no_mutants_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_results(tmp_path, {})
    assert main([MODULE]) == 1
    assert summarize([MODULE])["unmutatable_modules"] == [str(MODULE)]
