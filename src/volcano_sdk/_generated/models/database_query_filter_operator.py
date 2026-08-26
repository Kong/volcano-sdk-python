from typing import Literal

DatabaseQueryFilterOperator = Literal['eq', 'gt', 'gte', 'ilike', 'in', 'is', 'like', 'lt', 'lte', 'neq']

DATABASE_QUERY_FILTER_OPERATOR_VALUES: set[DatabaseQueryFilterOperator] = { 'eq', 'gt', 'gte', 'ilike', 'in', 'is', 'like', 'lt', 'lte', 'neq',  }

def check_database_query_filter_operator(value: str) -> DatabaseQueryFilterOperator:
    if value in DATABASE_QUERY_FILTER_OPERATOR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_QUERY_FILTER_OPERATOR_VALUES!r}")
