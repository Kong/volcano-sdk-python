from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_insights_interval import AuthInsightsInterval
from ..models.auth_insights_interval import check_auth_insights_interval
from typing import cast
import datetime






T = TypeVar("T", bound="AuthInsightsWindow")



@_attrs_define
class AuthInsightsWindow:
    """ 
        Attributes:
            from_ (datetime.date):
            to (datetime.date):
            interval (AuthInsightsInterval):
     """

    from_: datetime.date
    to: datetime.date
    interval: AuthInsightsInterval





    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        interval: str = self.interval


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "from": from_,
            "to": to,
            "interval": interval,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_ = datetime.date.fromisoformat(d.pop("from"))




        to = datetime.date.fromisoformat(d.pop("to"))




        interval = check_auth_insights_interval(d.pop("interval"))




        auth_insights_window = cls(
            from_=from_,
            to=to,
            interval=interval,
        )

        return auth_insights_window

