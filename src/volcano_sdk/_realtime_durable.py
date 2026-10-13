"""The realtime channels durable message subscriptions follow executions on."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from ._realtime_channel import ChannelState
from ._realtime_connection import ManagedChannel
from ._realtime_messages import (
    POSTGRES_BATCH_WINDOW_MS,
    POSTGRES_MAX_BATCH_SIZE,
    postgres_fetch_config,
)
from .realtime import Channel, Realtime

if TYPE_CHECKING:
    from ._durable_messages import DurableChannel
    from ._realtime_connection import RealtimeState

FacadeT = TypeVar("FacadeT")

_CHANNEL_PREFIX = "durable:"

# Durable channels fetch nothing; every channel carries a fetch configuration.
_NO_FETCH = postgres_fetch_config(
    auto_fetch=False,
    fetch_batch_window_ms=POSTGRES_BATCH_WINDOW_MS,
    fetch_max_batch_size=POSTGRES_MAX_BATCH_SIZE,
)


class DurableChannels(Generic[FacadeT]):
    """Open and close `durable:<execution id>` channels on a shared connection."""

    def __init__(self, state: RealtimeState[FacadeT]) -> None:
        """Register durable channels with a client's realtime state."""
        self._state: RealtimeState[FacadeT] = state

    def durable_channel(
        self, execution_id: str, client_token: str | None
    ) -> ChannelState | None:
        """Open the channel an execution publishes on.

        Returns
        -------
        ChannelState | None
            The new channel, or None when this connection already has it.

        """
        state = self._state
        wire_name = _CHANNEL_PREFIX + execution_id
        if wire_name in state.channels or wire_name in state.removing_channels:
            return None
        channel = ChannelState(
            state,
            wire_name,
            "durable",
            fetch_config=_NO_FETCH,
            subscribe_data=(
                None if client_token is None else {"client_token": client_token}
            ),
        )
        state.channels[wire_name] = ManagedChannel(channel, state.factory(channel))
        return channel

    async def remove_durable_channel(self, channel: DurableChannel) -> None:
        """Unsubscribe and forget a channel, unless another has replaced it."""
        entry = self._state.channels.get(channel.name)
        if entry is None or entry.state is not channel:
            return
        await self._state.remove_channel(
            channel.name.removeprefix(_CHANNEL_PREFIX), channel_type="durable"
        )


class ClientRealtime(Realtime):
    """A client's realtime facade, whose connection durable messages share."""

    def durable_channels(self) -> DurableChannels[Channel]:
        """Open durable message channels on this facade's connection.

        Returns
        -------
        DurableChannels[Channel]
            Channels that subscribe over the same connection as this facade.

        """
        return DurableChannels(self._state)
