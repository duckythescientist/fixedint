#!/usr/bin/env python3

from nose.tools import assert_raises

from fixedint import *


def test_ordered_promotion():
    spam = uint16(42)
    eggs = spam + 1
    assert isinstance(eggs, uint16)
    assert eggs == 43
    eggs = 1 + spam
    assert not isinstance(eggs, uint16)
    assert eggs == 43


def test_soft_cast():
    spam = uint16(42)
    eggs = spam + 1
    assert isinstance(eggs, uint16)
    assert eggs == 43
    eggs = spam + 1.0
    assert isinstance(eggs, uint16)
    assert eggs == 43
    eggs = spam + 1.5
    assert isinstance(eggs, float)
    assert eggs == 43.5


def test_hard_cast():
    spam = uint16(42)
    assert spam // 5 == 8
    assert spam // 5.0 == 8
    assert_raises(TypeError, lambda: spam // 1.5)
    assert_raises(TypeError, lambda: spam & 1.5)
