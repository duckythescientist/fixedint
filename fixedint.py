#!/usr/bin/env python3

from functools import wraps
import struct

class _cint(int):
    """Fixed-width unsigned integer types

    Create a class type by inheriting from _cint and setting
    `size` [and `byteorder`] or by calling `create_type`

    the p* properties expose packed bytes representations of the integer
    """
    size = 0
    byteorder = "little"

    @classmethod
    def create_type(cls, size, byteorder="little"):
        class newclass(cls):
            pass
        newclass.size = size
        newclass.byteorder = byteorder
        name = "uint{}".format(size*8)
        newclass.__name__ = name
        return newclass

    def __new__(cls, value=0):
        mask = (1 << (cls.size * 8)) - 1
        if isinstance(value, str):
            value = value.encode("ascii")
        if isinstance(value, (bytes, bytearray)):
            value = int.from_bytes(value, byteorder=cls.byteorder)

        value = int(value)

        value &= mask
        this = int.__new__(cls, value)

        def force(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return cls(func(*args, **kwargs))
            return wrapper
        setattr(cls, "__add__",     force(int.__add__))
        setattr(cls, "__sub__",     force(int.__sub__))
        setattr(cls, "__mul__",     force(int.__mul__))
        setattr(cls, "__truediv__", force(int.__truediv__))
        setattr(cls, "__lshift__",  force(int.__lshift__))
        setattr(cls, "__rshift__",  force(int.__rshift__))
        setattr(cls, "__and__",     force(int.__and__))
        setattr(cls, "__xor__",     force(int.__xor__))
        setattr(cls, "__or__",      force(int.__or__))
        setattr(cls, "__neg__",     force(int.__neg__))
        setattr(cls, "__invert__",  force(int.__invert__))
        this.size = cls.size
        return this

    def __repr__(self):
        return f"<{type(self).__name__} 0x{self:0{self.size*2}x}>"

    def __bytes__(self):
        """Return the int packed as bytes

        Respects the width of the underlying fixed-width type
        """
        return int(self).to_bytes(self.size, self.byteorder)

    @classmethod
    def cast(cls, val):
        return cls(val)

    def __pow__(self, other, modulo=None):
        if modulo is None:
            modulo = 1 << (8 * self.size)
        return self.cast(pow(int(self), int(other), modulo))

    def sar(self, shiftnum):
        """Shift arithmetic right

        Shifts with sign extension.
        Shifting by amounts larger than the number of bits will result
        in 0 or -1 depending on the sign of the number. Careful, this is
        undefined behavior in some other languages/implementations
        """
        shiftnum = min(shiftnum, self.size * 8)
        lowmask = (1 << (self.size * 8 - shiftnum)) - 1
        top = self.mask & (0 - self.msb) & ~lowmask
        return (self >> shiftnum) | top

    @property
    def mask(self):
        return self.cast((1 << (self.size * 8)) - 1)

    @property
    def msb(self):
        return (int(self) >> (self.size * 8 - 1)) & 1

    @property
    def lsb(self):
        return int(self) & 1

    @classmethod
    def _struct_float_chr(cls):
        if cls.size == 2:
            return "e"
        elif cls.size == 4:
            return "f"
        elif cls.size == 4:
            return "d"
        else:
            return None

    @property
    def as_float(self):
        c = self._struct_float_chr()
        if c is None:
            raise NotImplementedError("No float type for size %d bytes" % self.size)
        p = self.pack(byteorder="little")
        return struct.unpack("<" + c, p)[0]

    @classmethod
    def from_float(cls, val):
        c = cls._struct_float_chr()
        if c is None:
            raise NotImplementedError("No float type for size %d bytes" % self.size)
        p = struct.pack("<" + c, val)
        return cls.cast(p)

    def pack(self, size=None, byteorder=None):
        if size is None:
            size = self.size
        if byteorder is None:
            byteorder = self.byteorder
        return int(self).to_bytes(size, byteorder)

    @property
    def p(self):
        return self.pack()

    @property
    def p8(self):
        return int(self).to_bytes(1, self.byteorder)

    @property
    def p16(self):
        return int(self).to_bytes(2, self.byteorder)

    @property
    def p32(self):
        return int(self).to_bytes(4, self.byteorder)

    @property
    def p64(self):
        return int(self).to_bytes(8, self.byteorder)

    @property
    def p128(self):
        return int(self).to_bytes(16, self.byteorder)

    @property
    def as_signed(self):
        msb = self & (1 << (self.size * 8 - 1))
        rest = self & ((1 << (self.size * 8 - 1)) - 1)
        if msb:
            return int(rest) - int(msb)
        else:
            return int(rest)


class uint8(_cint):
    size = 1
    byteorder = "little"

class uint16(_cint):
    size = 2


class uint32(_cint):
    size = 4


class uint64(_cint):
    size = 8

# # Programmatically create new types:
# uint32 = _cint.create_type(4)
# uint64 = _cint.create_type(8, byteorder="little")
