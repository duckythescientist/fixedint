#!/usr/bin/env python3

from .fixedint import FixedInt


class UInt8(FixedInt):
    size = 1
    byteorder = "little"


class UInt16(FixedInt):
    size = 2


class UInt32(FixedInt):
    size = 4


class UInt64(FixedInt):
    size = 8


class UInt8_be(FixedInt):
    byteorder = "big"
    size = 1


class UInt16_be(FixedInt):
    byteorder = "big"
    size = 2


class UInt32_be(FixedInt):
    byteorder = "big"
    size = 4


class UInt64_be(FixedInt):
    byteorder = "big"
    size = 8
