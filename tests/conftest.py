from unittest.mock import Mock

import pytest


@pytest.fixture()
def api():
    return Mock(
        DecryptPassword=lambda x: Mock(Value=x),
        GetResourceDetails=lambda x: Mock(
            UniqueIdentifier="uniq id", ChildResources=[]
        ),
    )
