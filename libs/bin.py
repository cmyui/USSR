# Binary Serialisation lib.
import struct
from typing import Union

class BinaryWriter:
    """A binary writer used for serialisation. Primarily includes osu!'s types."""

    def __init__(self) -> None:
        self.buffer = bytearray()
    
    def write_uleb128(self, value: int) -> None:
        """Write a uleb128 value to the buffer."""
        if value == 0:
            return b"\x00"

        ret = bytearray()
        length = 0

        while value > 0:
            ret.append(value & 0b01111111)
            value >>= 7
            if value != 0:
                ret[length] |= 0b10000000
            length += 1

        self.buffer.extend(ret)
    
    def write_u64_le(self, value: int) -> "BinaryWriter":
        """Write a 64-bit unsigned integer to the buffer."""
        self.buffer += struct.pack("<Q", value)
        return self
    
    def write_i64_le(self, value: int) -> "BinaryWriter":
        """Write a 64-bit integer to the buffer."""
        self.buffer += struct.pack("<q", value)
        return self
    
    def write_i32_le(self, value: int) -> "BinaryWriter":
        """Write a 32-bit integer to the buffer."""
        self.buffer += struct.pack("<i", value)
        return self
    
    def write_u32_le(self, value: int) -> "BinaryWriter":
        """Write a 32-bit unsigned integer to the buffer."""
        self.buffer += struct.pack("<I", value)
        return self
    
    def write_i16_le(self, value: int) -> "BinaryWriter":
        """Write a 16-bit integer to the buffer."""
        self.buffer += struct.pack("<h", value)
        return self
    
    def write_u16_le(self, value: int) -> "BinaryWriter":
        """Write a 16-bit unsigned integer to the buffer."""
        self.buffer += struct.pack("<H", value)
        return self
    
    def write_i8_le(self, value: int) -> "BinaryWriter":
        """Write a 8-bit integer to the buffer."""
        self.buffer += struct.pack("<b", value)
        return self
    
    def write_u8_le(self, value: int) -> "BinaryWriter":
        """Write a 8-bit unsigned integer to the buffer."""
        self.buffer += struct.pack("<B", value)
        return self
    
    def write_raw(self, data: Union[bytes, bytearray]) -> "BinaryWriter":
        """Write raw data to the buffer."""
        self.buffer += data
        return self
    
    def write_osu_string(self, string: str) -> "BinaryWriter":
        """Write an osu! protocol style string.
        
        An osu! protocol string consists of an 'exists' byte, followed 
        by a uleb128 length, followed by the string itself.
        """
        if string:
            self.buffer += b"\x0B"
            self.write_uleb128(len(string))
            self.write_raw(string.encode("utf-8"))
        else: self.buffer += b"\x00"
        return self
