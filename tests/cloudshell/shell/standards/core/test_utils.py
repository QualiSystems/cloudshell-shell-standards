from __future__ import annotations

import pytest

from cloudshell.shell.standards.core.utils import split_list_of_values


@pytest.mark.parametrize(
    "string_list, expected_result",
    [
        ("a,b,c", ["a", "b", "c"]),
        ("a;b;c", ["a", "b", "c"]),
        ("a;b,c", ["a", "b", "c"]),
        ("a; ,c", ["a", "c"]),
        (" a  ; , c ", ["a", "c"]),
    ],
)
def test_split_list_of_values(string_list, expected_result):
    assert list(split_list_of_values(string_list)) == expected_result
