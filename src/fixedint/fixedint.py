#!/usr/bin/env python3

from functools import wraps
import struct


class FixedIntMeta(type):
    def __init__(cls, name, bases, dct):

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

        setattr(cls, "__neg__", _cast(int.__neg__))
        setattr(cls, "__pos__", _cast(int.__pos__))
        setattr(cls, "__invert__", _cast(int.__invert__))

        # For +-*/ keep everything as an int when possible.
        setattr(cls, "__add__", soft_cast(int.__add__))
        setattr(cls, "__sub__", soft_cast(int.__sub__))
        setattr(cls, "__mul__", soft_cast(int.__mul__))
        setattr(cls, "__truediv__", soft_cast(int.__truediv__))

        # For the more integer-centric maths, require integers.
        setattr(cls, "__floordiv__", hard_cast(int.__floordiv__))
        setattr(cls, "__mod__", hard_cast(int.__mod__))
        setattr(cls, "__divmod__", hard_cast(int.__divmod__))
        # __pow__ is a special case since it can take a second argument.
        setattr(cls, "__lshift__", hard_cast(int.__lshift__))
        setattr(cls, "__rshift__", hard_cast(int.__rshift__))
        setattr(cls, "__and__", hard_cast(int.__and__))
        setattr(cls, "__xor__", hard_cast(int.__xor__))
        setattr(cls, "__or__", hard_cast(int.__or__))

        return super().__init__(name, bases, dct)


class FixedInt(int, metaclass=FixedIntMeta):
    """Fixed-width integer types

    Create a class type by inheriting from FixedInt and setting
    `size` [and `byteorder`]

    the p* properties expose packed bytes representations of the integer
    """

    size = 0
    byteorder = "little"

    def __new__(cls, value=0):
        # Override __new__ because we need to control object creation
        # since we are inheriting from int. I think.
        # TODO: is this actually necessary
        original_value = value
        mask = (1 << (cls.size * 8)) - 1
        if isinstance(value, str):
            value = value.encode("ascii")
        if isinstance(value, (bytes, bytearray)):
            value = int.from_bytes(value, byteorder=cls.byteorder)

        if isinstance(value, FixedInt):
            # TODO: handle promotion/demotion
            value = int(value)

        if not isinstance(value, int):
            raise TypeError(
                f"{original_value} is of type {type(original_value)} but must be of type int, bytes, bytearray, ascii-string, or FixedInt"
            )

        value &= mask
        return super().__new__(cls, value)

    def __repr__(self):
        return f"{type(self).__name__}(0x{self:0{self.size*2}x}) # {int(self)}"

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
