from unittest.mock import MagicMock

import pytest

from agentpluginapi import ITCPPortSelector


@pytest.fixture(scope="session")
def tcp_port_selector() -> ITCPPortSelector:
    return MagicMock(spec=ITCPPortSelector)
