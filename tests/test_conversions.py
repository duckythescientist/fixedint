#!/usr/bin/env python3

import pytest

from fixedint import *


def test_inheritance():
    spam = UInt8(12)
    assert isinstance(spam, int)


def test_cast():
    spam = UInt8(12)
    eggs = UInt32(0xDEADBEEF)
    sausage = spam.cast(0xDEADBEEF)
    assert sausage == 0xEF
    assert type(sausage) == type(spam)
    sausage = eggs.cast(spam)
    assert sausage == 12
    assert type(sausage) == type(eggs)

    assert UInt8().cast(0xDEADBEEF) == 0xEF
    assert UInt8.cast(0xDEADBEEF) == 0xEF


def test_floats():
    f1 = 420.75
    v1 = UInt32.from_float(f1)
    r1 = UInt32(0x43D26000)
    assert v1 == r1
    assert f1 == r1.as_float


def test_pack_unpack():
    spam = UInt16(b"AB")
    assert spam == 0x4241
    assert bytes(spam) == b"AB"

    eggs = UInt16_be(b"AB")
    assert eggs == 0x4142
    assert bytes(eggs) == b"AB"


def test_bad_initial_value():
    # Try making a FixedInt from two things that are definitely not
    # castable to FixedInt
    pytest.raises(TypeError, UInt8, pytest)
    pytest.raises(TypeError, UInt8, object)
    # Also a float isn't pleasantly castable to int.
    pytest.raises(TypeError, UInt8, 3.0)
    pytest.raises(TypeError, UInt8, 3.14)
