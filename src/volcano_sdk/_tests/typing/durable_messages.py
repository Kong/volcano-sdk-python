"""An execution's own client token addresses its messages as documented."""

from typing import assert_type

from volcano_sdk import (
    DurableExecution,
    DurableMessage,
    DurableMessageSubscription,
    VolcanoClient,
)


async def execution_client_token(
    client: VolcanoClient, execution: DurableExecution
) -> None:
    _ = assert_type(execution.client_token, str | None)
    _sent = assert_type(
        client.durable.messages.send(
            "order-pipeline",
            execution.id,
            "address-confirmed",
            client_token=execution.client_token,
        ),
        DurableMessage,
    )
    _subscription = assert_type(
        await client.durable.messages.subscribe(
            "order-pipeline",
            execution.id,
            print,
            client_token=execution.client_token,
        ),
        DurableMessageSubscription,
    )
