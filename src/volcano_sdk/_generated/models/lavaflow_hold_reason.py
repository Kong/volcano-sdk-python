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
                LavaFlow doesn't check, such as required signatures. On a fix a person merges it names only rules that kept
                LavaFlow from starting the fix's CI, such as `code_scanning` or `workflows`, or that LavaFlow couldn't read
                them. `commit_convention`: no title can meet the repository's commit convention. `ungated_workflows`: the fix
                opened past workflows that can run it with the repository's secrets before a person approves it, as the
                project's owner allowed, or LavaFlow couldn't check its workflows, or, when LavaFlow was about to start its CI
                or add it to a merge queue, a workflow could run it with those secrets before a person approves it or couldn't
                be read, so LavaFlow takes it no further and never merges it. A fix held for another reason before its CI starts
                lists it too when that check, run without starting CI, finds such a workflow or can't finish.
                `ci_outside_actions`: when LavaFlow was about to start the fix's CI, the repository could run CI, a build or a
                preview outside GitHub Actions: the root of the fix's tree or its base branch's holds another service's
                configuration, such as `.travis.yml`, `.circleci/` or `netlify.toml`, which `paths` names, another app reported
                checks or statuses on the base branch, or LavaFlow couldn't read them in full. LavaFlow starts CI only when it
                finds no sign of CI outside GitHub Actions, so it never starts this fix's CI or merges it.
                `lineage_undoes_parent`: the fix follows up an earlier LavaFlow fix and deletes or changes lines that fix added,
                which could undo it. `lineage_cap`: the fix's lineage opened as many pull requests as it may. `lineage_held`: an
                earlier pull request in the fix's lineage was held, stopped or closed; one a person merges holds it only when
                closed. `recent_regressions`: fixes LavaFlow merged in the project recently caused new errors. `no_test`: the
                fix changes code the repository tests and adds no test, because testing it needs test infrastructure the
                repository doesn't have or the change has no effect a test can observe. `choices_to_confirm`: the fix states
                behavior it decides beyond stopping the error, listed in the run's `choices` and, on a private repository, under
                Choices to confirm in the pull request's description, for a person to confirm, and LavaFlow's reviewers didn't
                all mark each choice as needing no person. It never applies alongside `person_merges`: the person confirms the
                choices while reviewing the fix. `risky_change`: the fix adds or removes a line that converts a value, such as
                with `float()` or `parseInt()`, in a file that names a rate limit or quota, authentication or authorization, or
                money, so values such as NaN, Infinity or a negative number could get past a check there; `paths` names the
                files. `review_notes`: LavaFlow's reviewers passed the fix, but its review's last round left notes, findings
                below `major` that a later round no longer sends back for revision, such as a decision the fix makes without
                stating it. `person_merges`: a person reviews and merges the fix, because the project's autonomy is `open_pr`,
                merging was unavailable when it opened, or its run may only open a pull request; LavaFlow ran the fix's CI once
                first unless another reason, or the CI start's own checks, stopped it. Other codes name a concern LavaFlow's
                reviewers raised. New codes may appear.
            question (str): Why LavaFlow holds the fix and what to check before you merge it, in one or two sentences to
                show as given. A reviewer's reason is a question for you to answer. Reads `Hidden: this field matched a secret.`
                when it holds one of the project's secret values or a secret gitleaks detects, or when one of its `paths` reads
                `""`. Every question reads `Hidden: the fix may add a credential.`, LavaFlow's fixed sentences too, on a run
                whose `pull_request_skipped` is `possible_credential`.
            paths (list[str]): The changed paths that matched, for a path code. For `ci_outside_actions`, the entries at the
                repository's root that another CI or preview service reads, whether or not the fix changes them. `""` for a path
                that holds a control character, one of the project's secret values or a secret gitleaks detects.
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
