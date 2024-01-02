import pytest
from agentpluginapi import TCPPortSelector

@pytest.fixture(scope="session")
def tcp_port_selector() -> TCPPortSelector:
    return TCPPortSelector()
