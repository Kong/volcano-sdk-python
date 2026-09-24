from collections.abc import Callable
from typing import assert_type

from volcano_sdk._tests.test_binary_properties import (
    test_download_preserves_arbitrary_bytes,
    test_upload_preserves_remaining_binary_stream,
)
from volcano_sdk._tests.test_encoding_properties import (
    test_database_scope_encodes_user_as_one_parameter,
    test_database_scope_replacement_keeps_only_the_latest_user,
    test_storage_path_encoding_preserves_every_character,
    test_storage_path_rejects_dot_segments,
)

# Fully generated properties expose a typed, zero-argument pytest callable.
_ = assert_type(test_download_preserves_arbitrary_bytes, Callable[[], None])
_ = assert_type(test_upload_preserves_remaining_binary_stream, Callable[[], None])
_ = assert_type(test_database_scope_encodes_user_as_one_parameter, Callable[[], None])
_ = assert_type(
    test_database_scope_replacement_keeps_only_the_latest_user, Callable[[], None]
)
_ = assert_type(
    test_storage_path_encoding_preserves_every_character, Callable[[], None]
)
_ = assert_type(test_storage_path_rejects_dot_segments, Callable[[], None])
