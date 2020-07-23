#!/usr/bin/env python3


from fixedint import *


def test_basic_init():
    assert uint8(0) == 0
    assert uint8(1) == 1
    assert uint8(255) == 255
    assert uint8(256) == 0
    assert uint8(257) == 1
    assert uint8(-1) == 255
    assert uint8(-1) == uint8(255)


def test_repr():
    spam = uint8(21)
    assert repr(spam) == "<uint8 0x15 (21)>"
    spam = uint16(21)
    assert repr(spam) == "<uint16 0x0015 (21)>"
    spam = uint32(21)
    assert spam == 21
    assert repr(spam) == "<uint32 0x00000015 (21)>"
    spam = uint64(21)
    assert spam == 21
    assert repr(spam) == "<uint64 0x0000000000000015 (21)>"


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
