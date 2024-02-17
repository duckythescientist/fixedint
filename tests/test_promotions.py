#!/usr/bin/env python3

import pytest

from fixedint import *


def test_ordered_promotion():
    spam = UInt16(42)
    eggs = spam + 1
    assert isinstance(eggs, UInt16)
    assert eggs == 43
    eggs = 1 + spam
    assert not isinstance(eggs, UInt16)
    assert eggs == 43


def test_soft_cast():
    spam = UInt16(42)
    eggs = spam + 1
    assert isinstance(eggs, UInt16)
    assert eggs == 43
    eggs = spam + 1.0
    assert isinstance(eggs, UInt16)
    assert eggs == 43
    eggs = spam + 1.5
    assert isinstance(eggs, float)
    assert eggs == 43.5


def test_hard_cast():
    spam = UInt16(42)
    assert spam // 5 == 8
    assert spam // 5.0 == 8
    pytest.raises(TypeError, lambda: spam // 1.5)
    pytest.raises(TypeError, lambda: spam & 1.5)
