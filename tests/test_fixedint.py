#!/usr/bin/env python3


from fixedint import *


def test_basic_init():
    assert UInt8(0) == 0
    assert UInt8(1) == 1
    assert UInt8(255) == 255
    assert UInt8(256) == 0
    assert UInt8(257) == 1
    assert UInt8(-1) == 255
    assert UInt8(-1) == UInt8(255)


def test_repr():
    spam = UInt8(21)
    assert repr(spam) == "UInt8(0x15) # 21"
    spam = UInt16(21)
    assert repr(spam) == "UInt16(0x0015) # 21"
    spam = UInt32(21)
    assert spam == 21
    assert repr(spam) == "UInt32(0x00000015) # 21"
    spam = UInt64(21)
    assert spam == 21
    assert repr(spam) == "UInt64(0x0000000000000015) # 21"


# def test_repr_str():
#     spam = uint8(21)
#     assert str(spam) == "21"
#     spam = uint16(21)
#     assert str(spam) == "21"
#     spam = uint32(21)
#     assert spam == 21
#     assert str(spam) == "21"
#     spam = uint64(21)
#     assert spam == 21
#     assert str(spam) == "21"
