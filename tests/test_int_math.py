#!/usr/bin/env python3


from fixedint import *


def test_math_preserves_type():
    spam = UInt8(21)
    spam >>= 1
    spam |= 1
    spam += 2
    assert isinstance(spam, UInt8)
    assert not isinstance(spam, UInt16)


def test_shifts():
    spam = UInt8(21)
    assert spam == 21
    assert spam >> 1 == 10
    assert spam << 1 == 42
    spam >>= 1
    assert spam == 10
    spam <<= 3
    assert spam == 80
    spam <<= 5
    assert spam == 0
    spam = UInt8(21)
    assert spam >> 8 == 0


def test_bitwise():
    spam = UInt8(21)
    assert spam & 0xF == 5
    assert spam | 0x3 == 23
    assert spam ^ 0x4 == 17
    assert ~spam == 0xEA
    assert spam // 2 == 10
    assert spam // 3 == 7
    assert spam * 3 == 63


def test_unary():
    spam = UInt16(3)
    assert +spam == 3
    assert -spam == UInt16(-3)
    assert isinstance(+spam, UInt16)
    assert -spam == 0xFFFD
    assert isinstance(-spam, UInt16)
    assert ~spam == 0xFFFC
    assert ~spam == UInt16(~3)
    assert isinstance(~spam, UInt16)


def test_pow():
    spam = UInt32(3)
    eggs = spam**2
    assert eggs == 3**2
    assert isinstance(eggs, UInt32)
    sausage = 2**spam
    assert sausage == 2**3

    bacon = UInt32(2)
    sausage = bacon**spam
    assert sausage == 2**3
    assert isinstance(sausage, UInt32)

    spam = UInt32(0xDEADBEEF)
    eggs = spam**17
    result = 0xDEADBEEF**17
    assert eggs == result % (1 << 32)
    assert pow(spam, 17) == result % (1 << 32)
    assert pow(spam, 17, 2048) == result % 2048


def test_as_signed():
    assert UInt8(0).as_signed == 0
    assert UInt8(1).as_signed == 1
    assert UInt8(127).as_signed == 127
    assert UInt8(128).as_signed == -128
    assert UInt8(255).as_signed == -1


def test_msblsb():
    spam = UInt8(12)
    eggs = UInt8(128)
    sausage = UInt8(129)
    assert spam.msb == 0
    assert spam.lsb == 0
    assert eggs.msb == 1
    assert eggs.lsb == 0
    assert sausage.msb == 1
    assert sausage.lsb == 1


def test_sar():
    spam = UInt8(12)
    assert spam.sar(0) == 12
    assert spam.sar(1) == 6
    assert spam.sar(2) == 3
    assert spam.sar(3) == 1
    assert spam.sar(4) == 0
    assert spam.sar(5) == 0
    assert spam.sar(100) == 0

    eggs = UInt8(-3)
    assert eggs.sar(0) == UInt8(-3)
    assert eggs.sar(1) == UInt8(-2)
    assert eggs.sar(2) == UInt8(-1)
    assert eggs.sar(100) == UInt8(-1)

    assert type(eggs) == type(eggs.sar(1))


def test_mask():
    assert UInt8(12).mask == 0xFF


def test_rotate():
    spam = UInt16(0xABCD)
    assert spam.ror(4) == UInt16(0xDABC)
    assert spam.ror(4 + 16) == UInt16(0xDABC)
    assert spam.rol(4) == UInt16(0xBCDA)
    assert spam.rol(4 + 16) == UInt16(0xBCDA)
