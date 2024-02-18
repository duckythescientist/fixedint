# Fixed-width integers for Python

They look like `int`s, walk like `int`s and quack like `int`s, but they over/underflow like machine arithmetic.

This library is still in an early state. Expect API changes and refactoring.


Quick tutorial:

```python
from fixedint import UInt8, UInt16, UInt32, UInt64

# Or for all common types (including e.g. UInt16_be for big-endian)
# from fixedint import *


spam = UInt16(3)
print(spam)
## UInt16(0x0003) # 3

spam += 2
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
## UInt32(0x4048f5c3) # 1078523331

eggs.as_float
## 3.140000104904175

bytes(eggs)
## b'\xc3\xf5H@'

eggs.pack()
## b'\xc3\xf5H@'

# Initialize from bytes (or ASCII strings)
foo = UInt32("abcd")
UInt32(0x64636261) # 1684234849

foo.lsb
## 1

foo.msb
## 0

# Right shifts are logical by default
UInt16(0xA000) >> 4
## UInt16(0x0a00) # 2560

# But you can call sar for sign-extending shifts
UInt16(0xA000).sar(4)
## UInt16(0xfa00) # 64000

# There's also rotations
UInt16(0x0F00).ror(4)
## UInt16(0x00f0) # 240
UInt16(0x0F00).rol(4)
## UInt16(0xf000) # 61440


for i in range(UInt32(3)):
    print("Works as ints in most places")
## Works as ints in most places
## Works as ints in most places
## Works as ints in most places


# FixedInts keep their type if they the left-operand
type(UInt8(1) + 1)
## fixedint.stdint.UInt8

# but they lose their type if they are a right-operand
type(1 + UInt8(2))
## int

# The type of the left-operand is maintained.
# TODO: better control over casting.
type(UInt8(1) + UInt16(2))
## UInt8(0x03) # 3
```