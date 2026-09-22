"""Check typed callbacks and the separate durable invocation boundary."""

from typing import TypedDict, assert_type

from volcano_sdk.durable_authoring import DurableContext, FunctionHandler, durable


class Order(TypedDict):
    quantity: int


def order_quantity(event: Order, _context: DurableContext) -> int:
    return event["quantity"]


@durable
def bare(event: Order, _context: DurableContext) -> int:
    return event["quantity"]


@durable()
def called(event: Order, _context: DurableContext) -> int:
    return event["quantity"]


@durable(logger=object())
def configured(event: Order, _context: DurableContext) -> int:
    return event["quantity"]


wrapped = durable(order_quantity)
assert_type(wrapped, FunctionHandler)
assert_type(bare, FunctionHandler)
assert_type(called, FunctionHandler)
assert_type(configured, FunctionHandler)
assert_type(wrapped(object(), object()), object)
assert_type(bare(object(), object()), object)
assert_type(called(object(), object()), object)
assert_type(configured(object(), object()), object)
