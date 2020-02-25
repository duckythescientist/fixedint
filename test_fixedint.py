#!/usr/bin/env python3

from pytest import approx

from fixedint import _cint, uint8, uint16, uint32, uint64


def test_basic_init():
    assert uint8(0) == 0
    assert uint8(1) == 1
    assert uint8(255) == 255
    assert uint8(256) == 0
    assert uint8(257) == 1
    assert uint8(-1) == 255
    assert uint8(-1) == uint8(255)

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

def test_repr_str():
    spam = uint8(21)
    assert repr(spam) == "<uint8 0x15>"
    assert str(spam) == "21"
    eggs = uint16(21)
    assert repr(eggs) == "<uint16 0x0015>"
    assert str(eggs) == "21"


def test_pack_unpack():
    spam = uint16(b"AB")
    assert spam == 0x4241
    assert bytes(spam) == b"AB"


def test_bigger():
    spam = uint32(21)
    assert spam == 21
    assert repr(spam) == "<uint32 0x00000015>"
    eggs = uint64(21)
    assert eggs == 21
    assert repr(eggs) == "<uint64 0x0000000000000015>"


def test_pow():
    spam = uint32(3)
    eggs = spam ** 2
    assert eggs == 3**2
    assert isinstance(eggs, uint32)
    sausage = 2 ** spam
    assert sausage == 2**3
    
    bacon = uint32(2)
    sausage = bacon ** spam
    assert sausage == 2**3
    assert isinstance(sausage, uint32)

    spam = uint32(0xdeadbeef)
    eggs = spam ** 17
    result = 0xdeadbeef ** 17
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


def test_cast():
    spam = uint8(12)
    eggs = uint32(0xdeadbeef)
    sausage = spam.cast(0xdeadbeef)
    assert sausage == 0xef
    assert type(sausage) == type(spam)
    sausage = eggs.cast(spam)
    assert sausage == 12
    assert type(sausage) == type(eggs)

    assert uint8().cast(0xdeadbeef) == 0xef
    assert uint8.cast(0xdeadbeef) == 0xef


def test_floats():
    f1 = 420.75
    v1 = uint32.from_float(f1)
    r1 = uint32(0x43d26000)
    assert v1 == r1
    assert f1 == r1.as_float
