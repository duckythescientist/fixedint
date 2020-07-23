#!/usr/bin/env python3


from fixedint import *


def test_shifts():
    spam = uint8(21)
    assert spam == 21
    assert spam >> 1 == 10
    assert spam << 1 == 42
    spam >>= 1
    assert spam == 10
    spam <<= 3
    assert spam == 80
    spam <<= 5
    assert spam == 0
    spam = uint8(21)
    assert spam >> 8 == 0


def test_bitwise():
    spam = uint8(21)
    assert spam & 0xF == 5
    assert spam | 0x3 == 23
    assert spam ^ 0x4 == 17
    assert ~spam == 0xEA
    assert spam // 2 == 10
    assert spam // 3 == 7
    assert spam * 3 == 63


def test_pow():
    spam = uint32(3)
    eggs = spam ** 2
    assert eggs == 3 ** 2
    assert isinstance(eggs, uint32)
    sausage = 2 ** spam
    assert sausage == 2 ** 3

    bacon = uint32(2)
    sausage = bacon ** spam
    assert sausage == 2 ** 3
    assert isinstance(sausage, uint32)

    spam = uint32(0xDEADBEEF)
    eggs = spam ** 17
    result = 0xDEADBEEF ** 17
    assert eggs == result % (1 << 32)
    assert pow(spam, 17) == result % (1 << 32)
    assert pow(spam, 17, 2048) == result % 2048


def test_as_signed():
    assert uint8(0).as_signed == 0
    assert uint8(1).as_signed == 1
    assert uint8(127).as_signed == 127
    assert uint8(128).as_signed == -128
    assert uint8(255).as_signed == -1


def test_msblsb():
    spam = uint8(12)
    eggs = uint8(128)
    sausage = uint8(129)
    assert spam.msb == 0
    assert spam.lsb == 0
    assert eggs.msb == 1
    assert eggs.lsb == 0
    assert sausage.msb == 1
    assert sausage.lsb == 1


def test_sar():
    spam = uint8(12)
    assert spam.sar(0) == 12
    assert spam.sar(1) == 6
    assert spam.sar(2) == 3
    assert spam.sar(3) == 1
    assert spam.sar(4) == 0
    assert spam.sar(5) == 0
    assert spam.sar(100) == 0

    eggs = uint8(-3)
    assert eggs.sar(0) == uint8(-3)
    assert eggs.sar(1) == uint8(-2)
    assert eggs.sar(2) == uint8(-1)
    assert eggs.sar(100) == uint8(-1)

    assert type(eggs) == type(eggs.sar(1))


def test_mask():
    assert uint8(12).mask == 0xFF
