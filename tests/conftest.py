import sys
sys.path.append('../py-hdlc')
import pytest
from hdlc import HDLCBaseFrame


@pytest.fixture(scope="module")
def baseframe():
    """create a HDLCBaseFrame-object"""
    return HDLCBaseFrame()


@pytest.fixture(scope="module")
def chunk1():
    """create a minimal/empty unicast basechunk with valid flags"""
    return b'\x7e\xff\x00\x00\x7e'
