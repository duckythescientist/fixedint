#!/usr/bin/env python3

__all__ = [
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "uint8_be",
    "uint16_be",
    "uint32_be",
    "uint64_be",
]


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
        name = "uint{}".format(size * 8)
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
        this.size = cls.size

        def _cast(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return cls(int(func(*args, **kwargs)))

            return wrapper

        def soft_cast(func):
            # Work with integers when possible.
            @wraps(func)
            def wrapper(self, other):
                if other == int(other):
                    result = func(self, int(other))
                else:
                    result = func(self, other)
                if result == NotImplemented:
                    return NotImplemented
                elif result == int(result):
                    return cls(result)
                else:
                    return result

            return wrapper

        def hard_cast(func):
            # Require that everything is an integer
            @wraps(func)
            def wrapper(self, other):
                if other != int(other):
                    raise TypeError("Integer argument required")
                result = func(self, int(other))
                return cls(result)

            return wrapper

        # For +-*/ keep everything as an int when possible.
        setattr(cls, "__add__", soft_cast(int.__add__))
        setattr(cls, "__sub__", soft_cast(int.__sub__))
        setattr(cls, "__mul__", soft_cast(int.__mul__))
        setattr(cls, "__truediv__", soft_cast(int.__truediv__))

        # For the more integer-centric maths, require integers.
        setattr(cls, "__floordiv__", hard_cast(int.__floordiv__))
        setattr(cls, "__mod__", hard_cast(int.__mod__))
        setattr(cls, "__divmod__", hard_cast(int.__divmod__))
        # __pow__ is a special case
        setattr(cls, "__lshift__", hard_cast(int.__lshift__))
        setattr(cls, "__rshift__", hard_cast(int.__rshift__))
        setattr(cls, "__and__", hard_cast(int.__and__))
        setattr(cls, "__xor__", hard_cast(int.__xor__))
        setattr(cls, "__or__", hard_cast(int.__or__))

        setattr(cls, "__neg__", _cast(int.__neg__))
        setattr(cls, "__invert__", _cast(int.__invert__))

        return this

    def __repr__(self):
        return f"<{type(self).__name__} 0x{self:0{self.size*2}x} ({int(self)})>"

    def __bytes__(self):
        """Return the int packed as bytes

        Respects the width of the underlying fixed-width type
        """
        return int(self).to_bytes(self.size, self.byteorder)

    @classmethod
    def cast(cls, val):
        return cls(val)

    def __pow__(self, other, modulo=None):
        if modulo is None and other != int(other):
            return pow(int(self), other)
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
        elif cls.size == 8:
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


class uint8_be(_cint):
    byteorder = "big"
    size = 1


class uint16_be(_cint):
    byteorder = "big"
    size = 2


class uint32_be(_cint):
    byteorder = "big"
    size = 4


class uint64_be(_cint):
    byteorder = "big"
    size = 8


# # Programmatically create new types:
# uint32 = _cint.create_type(4)
# uint64 = _cint.create_type(8, byteorder="little")
