from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.update_notification_email import UpdateNotificationEmail
  from ..models.update_notification_webhook import UpdateNotificationWebhook
  from ..models.update_scheduler_failure_alert_policy import UpdateSchedulerFailureAlertPolicy





T = TypeVar("T", bound="ProjectConfigNotifications")



@_attrs_define
class ProjectConfigNotifications:
    """ Where the project's alerts go and when a failing scheduler is announced. Omitted fields keep their current value.
    The webhook signing secret is never part of the manifest: setting `webhook.url` on a project without a webhook
    generates one that is never shown. Rotate it with `POST /projects/{id}/notifications/webhook-secret` to get a secret
    you can use.

        Attributes:
            email (UpdateNotificationEmail | Unset):
            webhook (UpdateNotificationWebhook | Unset):
            scheduler_failures (UpdateSchedulerFailureAlertPolicy | Unset):
     """

    email: UpdateNotificationEmail | Unset = UNSET
    webhook: UpdateNotificationWebhook | Unset = UNSET
    scheduler_failures: UpdateSchedulerFailureAlertPolicy | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_notification_email import UpdateNotificationEmail # noqa: PLC0415
        from ..models.update_notification_webhook import UpdateNotificationWebhook # noqa: PLC0415
        from ..models.update_scheduler_failure_alert_policy import UpdateSchedulerFailureAlertPolicy # noqa: PLC0415
        email: dict[str, Any] | Unset = UNSET
        if not isinstance(self.email, Unset):
            email = self.email.to_dict()

        webhook: dict[str, Any] | Unset = UNSET
        if not isinstance(self.webhook, Unset):
            webhook = self.webhook.to_dict()

        scheduler_failures: dict[str, Any] | Unset = UNSET
        if not isinstance(self.scheduler_failures, Unset):
            scheduler_failures = self.scheduler_failures.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if email is not UNSET:
            field_dict["email"] = email
        if webhook is not UNSET:
            field_dict["webhook"] = webhook
        if scheduler_failures is not UNSET:
            field_dict["scheduler_failures"] = scheduler_failures

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_notification_email import UpdateNotificationEmail # noqa: PLC0415
        from ..models.update_notification_webhook import UpdateNotificationWebhook # noqa: PLC0415
        from ..models.update_scheduler_failure_alert_policy import UpdateSchedulerFailureAlertPolicy # noqa: PLC0415
        d = dict(src_dict)
        _email = d.pop("email", UNSET)
        email: UpdateNotificationEmail | Unset
        if isinstance(_email,  Unset):
            email = UNSET
        else:
            email = UpdateNotificationEmail.from_dict(_email)




        _webhook = d.pop("webhook", UNSET)
        webhook: UpdateNotificationWebhook | Unset
        if isinstance(_webhook,  Unset):
            webhook = UNSET
        else:
            webhook = UpdateNotificationWebhook.from_dict(_webhook)




        _scheduler_failures = d.pop("scheduler_failures", UNSET)
        scheduler_failures: UpdateSchedulerFailureAlertPolicy | Unset
        if isinstance(_scheduler_failures,  Unset):
            scheduler_failures = UNSET
        else:
            scheduler_failures = UpdateSchedulerFailureAlertPolicy.from_dict(_scheduler_failures)




        project_config_notifications = cls(
            email=email,
            webhook=webhook,
            scheduler_failures=scheduler_failures,
        )

        return project_config_notifications

