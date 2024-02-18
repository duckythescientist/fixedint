#!/usr/bin/env python3

from fixedint import UInt8, UInt16, UInt32, UInt64

# Or for all common types (including e.g. UInt16_be for big-endian)
# from fixedint import *

spam = UInt16(3)
print(spam)
## UInt16(0x0003) # 3

spam += 1
## UInt16(0x0005) # 5

spam = spam & ~(1)
## UInt16(0x0004) # 4

spam <<= 2
## UInt16(0x0010) # 16

spam -= 17
## UInt16(0xffff) # 65535

spam.as_signed
## -1

spam.as_float
## nan

eggs = UInt32.from_float(3.14)
eggs
## UInt32(0x4048f5c3) # 1078523331

eggs.as_float
## 3.140000104904175

bytes(eggs)
## b'\xc3\xf5H@'

eggs.pack()
## b'\xc3\xf5H@'

eggs.pack(8)
## b'\xc3\xf5H@\x00\x00\x00\x00'

foo = UInt32("ABCD")
## UInt32(0x44434241) # 1145258561

for i in range(UInt32(3)):
    print("Works as ints in most places")
## Works as ints in most places
## Works as ints in most places
## Works as ints in most places

# FixedInts keep their type if they the right-operand
type(UInt8(1) + 1)
## fixedint.stdint.UInt8

# but they lose their type if they are a left-operand
type(1 + UInt8(2))
## int

type(UInt8(1) + UInt16(2))
## UInt8(0x03) # 3
