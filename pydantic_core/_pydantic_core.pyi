import decimal
import sys
from typing import Any, TypedDict

from pydantic_core.core_schema import CoreConfig, CoreSchema, ErrorType

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired
else:
    from typing import NotRequired

__all__ = (
    '__version__',
    'build_profile',
    'SchemaValidator',
    'SchemaError',
    'ValidationError',
    'PydanticCustomError',
    'PydanticKnownError',
    'PydanticOmit',
    'list_all_errors',
)
__version__: str
build_profile: str

class SchemaValidator:
    title: str
    def __init__(self, schema: CoreSchema, config: 'CoreConfig | None' = None) -> None: ...
    def validate_python(self, input: Any, strict: 'bool | None' = None, context: Any = None) -> Any: ...
    def isinstance_python(self, input: Any, strict: 'bool | None' = None, context: Any = None) -> bool: ...
    def validate_json(
        self, input: 'str | bytes | bytearray', strict: 'bool | None' = None, context: Any = None
    ) -> Any: ...
    def isinstance_json(
        self, input: 'str | bytes | bytearray', strict: 'bool | None' = None, context: Any = None
    ) -> bool: ...
    def validate_assignment(
        self, field: str, input: Any, data: 'dict[str, Any]', strict: 'bool | None' = None, context: Any = None
    ) -> 'dict[str, Any]': ...

class SchemaError(Exception):
    pass

class ErrorDetails(TypedDict):
    type: str
    loc: 'list[int | str]'
    message: str
    input_value: Any
    context: NotRequired['dict[str, str | int | float]']

class ValidationError(ValueError):
    title: str

    def error_count(self) -> int: ...
    def errors(self, include_context: bool = True) -> 'list[ErrorDetails]': ...

class PydanticCustomError(ValueError):
    type: str
    message_template: str
    context: 'dict[str, Any] | None'

    def __init__(self, error_type: str, message_template: str, context: 'dict[str, Any] | None' = None) -> None: ...
    def message(self) -> str: ...

class PydanticKnownError(ValueError):
    type: ErrorType
    message_template: str
    context: 'dict[str, str | int | float] | None'

    def __init__(
        self, error_type: ErrorType, context: 'dict[str, str | int | float | decimal.Decimal] | None' = None
    ) -> None: ...
    def message(self) -> str: ...

class PydanticOmit(Exception):
    def __init__(self) -> None: ...

class ErrorTypeInfo(TypedDict):
    type: ErrorType
    message_template: str
    example_message: str
    example_context: 'dict[str, str | int | float] | None'

def list_all_errors() -> 'list[ErrorTypeInfo]':
    """
    Get information about all built-in errors.
    """
