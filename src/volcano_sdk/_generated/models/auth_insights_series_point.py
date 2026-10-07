from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="AuthInsightsSeriesPoint")



@_attrs_define
class AuthInsightsSeriesPoint:
    """ 
        Attributes:
            bucket_start (datetime.date):
            signups (int): Registrations during the bucket. Subsequent deletion does not subtract from this count.
                Historical counts removed before deletion-history collection cannot be reconstructed.
            signins (int): Successful session creations during the bucket.
            deletions (int): Accounts deleted during this bucket, counted once across soft and hard deletion.
            net_growth (int): Registrations minus deletions during this bucket. May be negative.
            is_partial (bool): Whether the requested window or observation time clips this bucket.
     """

    bucket_start: datetime.date
    signups: int
    signins: int
    deletions: int
    net_growth: int
    is_partial: bool





    def to_dict(self) -> dict[str, Any]:
        bucket_start = self.bucket_start.isoformat()

        signups = self.signups

        signins = self.signins

        deletions = self.deletions

        net_growth = self.net_growth

        is_partial = self.is_partial


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "bucket_start": bucket_start,
            "signups": signups,
            "signins": signins,
            "deletions": deletions,
            "net_growth": net_growth,
            "is_partial": is_partial,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bucket_start = datetime.date.fromisoformat(d.pop("bucket_start"))




        signups = d.pop("signups")

        signins = d.pop("signins")

        deletions = d.pop("deletions")

        net_growth = d.pop("net_growth")

        is_partial = d.pop("is_partial")

        auth_insights_series_point = cls(
            bucket_start=bucket_start,
            signups=signups,
            signins=signins,
            deletions=deletions,
            net_growth=net_growth,
            is_partial=is_partial,
        )

        return auth_insights_series_point

