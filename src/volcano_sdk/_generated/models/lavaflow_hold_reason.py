from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="LavaflowHoldReason")



@_attrs_define
class LavaflowHoldReason:
    """ One reason LavaFlow holds the fix for a person.

        Attributes:
            code (str): Why the fix is held. `client_reported_commit`: the fix is built on a commit Volcano can't tie to a
                push. `path`: it changes a path in `human_review_paths`, or deploy or infrastructure configuration Volcano
                always holds, such as `volcano-config.yaml`, Terraform files, a YAML or JSON file that declares a resource, a
                YAML template that mentions `apiVersion` or `kind`, a file in a Helm chart or Kustomize directory, or, in a
                repository too large to read in full, any file no other path reason holds. `sensitive_path`: it changes another
                path Volcano always holds: authentication or authorization code, Next.js middleware included; secret, key,
                certificate or cryptography files; a coding agent's instructions or settings, or Git hook configuration; CI
                configuration; a dependency manifest or lockfile, or a `package.json` change to what installs or its install
                scripts; or runtime, container or other configuration files. `label`: the pull request has the `needs-human-
                review` label. `no_checks`: no CI ran on it. `required_check_skipped`: a required check was skipped.
                `no_required_checks`: the base branch requires no check, so passing checks alone don't vouch for the fix.
                `changes_requested`: a reviewer requested changes. `repository_requires_approval`: the repository requires an
                approving review. `person_commits`: someone other than LavaFlow pushed to the fix's branch. `rules_bypass`: the
                Volcano GitHub App can bypass a ruleset on the base branch. `unchecked_rules`: the base branch has a rule
                LavaFlow doesn't check, such as required signatures. `commit_convention`: no title can meet the repository's
                commit convention. `ungated_workflows`: the fix opened past workflows that can run it with the repository's
                secrets before a person approves it, as the project's owner allowed, or LavaFlow couldn't check its workflows,
                or, when LavaFlow was about to start its CI or add it to a merge queue, a workflow could run it with those
                secrets before a person approves it or couldn't be read, so LavaFlow takes it no further and never merges it. A
                fix held for another reason before its CI starts lists it too when that check, run without starting CI, finds
                such a workflow or can't finish. `ci_outside_actions`: when LavaFlow was about to start the fix's CI, the
                repository could run CI, a build or a preview outside GitHub Actions: the root of the fix's tree or its base
                branch's holds another service's configuration, such as `.travis.yml`, `.circleci/` or `netlify.toml`, which
                `paths` names, another app reported checks or statuses on the base branch, or LavaFlow couldn't read them in
                full. LavaFlow starts CI only when it finds no sign of CI outside GitHub Actions, so it never starts this fix's
                CI or merges it. `lineage_undoes_parent`: the fix follows up an earlier LavaFlow fix and deletes or changes
                lines that fix added, which could undo it. `lineage_cap`: the fix's lineage opened as many pull requests as it
                may. `lineage_held`: an earlier pull request in the fix's lineage was held, stopped or closed.
                `recent_regressions`: fixes LavaFlow merged in the project recently caused new errors. Other codes name a
                concern LavaFlow's reviewers raised. New codes may appear.
            question (str): What a person decides before merging the fix, written to show as given.
            paths (list[str]): The changed paths that matched, for a path code. For `ci_outside_actions`, the entries at the
                repository's root that another CI or preview service reads, whether or not the fix changes them.
     """

    code: str
    question: str
    paths: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        question = self.question

        paths = self.paths




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "question": question,
            "paths": paths,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        question = d.pop("question")

        paths = cast(list[str], d.pop("paths"))


        lavaflow_hold_reason = cls(
            code=code,
            question=question,
            paths=paths,
        )


        lavaflow_hold_reason.additional_properties = d
        return lavaflow_hold_reason

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
