from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.notification_email_settings import NotificationEmailSettings
  from ..models.notification_webhook_settings import NotificationWebhookSettings
  from ..models.scheduler_failure_alert_policy import SchedulerFailureAlertPolicy





T = TypeVar("T", bound="NotificationSettings")



@_attrs_define
class NotificationSettings:
    """ 
        Attributes:
            project_id (UUID):
            email (NotificationEmailSettings):
            webhook (NotificationWebhookSettings):
            scheduler_failures (SchedulerFailureAlertPolicy):
            updated_at (datetime.datetime | Unset): When the settings were last saved. Absent until the first save.
     """

    project_id: UUID
    email: NotificationEmailSettings
    webhook: NotificationWebhookSettings
    scheduler_failures: SchedulerFailureAlertPolicy
    updated_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.notification_email_settings import NotificationEmailSettings # noqa: PLC0415
        from ..models.notification_webhook_settings import NotificationWebhookSettings # noqa: PLC0415
        from ..models.scheduler_failure_alert_policy import SchedulerFailureAlertPolicy # noqa: PLC0415
        project_id = str(self.project_id)

        email = self.email.to_dict()

        webhook = self.webhook.to_dict()

        scheduler_failures = self.scheduler_failures.to_dict()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "email": email,
            "webhook": webhook,
            "scheduler_failures": scheduler_failures,
        })
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_email_settings import NotificationEmailSettings # noqa: PLC0415
        from ..models.notification_webhook_settings import NotificationWebhookSettings # noqa: PLC0415
        from ..models.scheduler_failure_alert_policy import SchedulerFailureAlertPolicy # noqa: PLC0415
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        email = NotificationEmailSettings.from_dict(d.pop("email"))




        webhook = NotificationWebhookSettings.from_dict(d.pop("webhook"))




        scheduler_failures = SchedulerFailureAlertPolicy.from_dict(d.pop("scheduler_failures"))




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        notification_settings = cls(
            project_id=project_id,
            email=email,
            webhook=webhook,
            scheduler_failures=scheduler_failures,
            updated_at=updated_at,
        )

        return notification_settings

