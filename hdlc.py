#!/usr/bin/env python3

class HDLCBaseFrame(object):
    """
    A basic HDLC frame with all common data fields. All other frame classes
    are derived from here.
    """

    __address = None
    __control = None
    __fcs = None
    def __init__(self):
        self.__address = bytes(1)   # assign "no station" by default
        self.__control = bytes(1)   # 8 or 16 bits
        self.__fcs = bytes(2)       # 16 or 32 bits frame check sequence

    # address handling
    def parse_address(self, rawchunk):
        """
        Extract the address out of a given serial data chunk.
        The input is expected to be an instance bytes(), since
        Byte arrays can be modified while being parsed.
        """
        if not isinstance(rawchunk,bytes):
            raise TypeError("no bytes-object given")

        stripped = True
        if (126 == rawchunk[0]) and (126 == rawchunk[-1]):
                stripped = False

        if not (126 == rawchunk[0]) and (126 == rawchunk[-1]):
                raise ValueError("opening flag corrupt / not 0x7e")

        if (126 == rawchunk[0]) and not (126 == rawchunk[-1]):
                raise ValueError("closing flag corrupt / not 0x7e")

        # minimal: no data field
        if (not stripped and len(rawchunk) <= 4) or (stripped and len(rawchunk) <= 2):
            raise ValueError("to few bytes given")

        # strip given chunk for easier parsing
        __parsechunk = rawchunk
        if not stripped:
            byteslist = [rawchunk[i] for i in range(1,len(rawchunk)-1)]
            __parsechunk = bytes(byteslist)

        __parsestart = 0  # index from where parsing section starts

        # read address
        ## determine address length: MSB = 0 ->more frames to come
        ## no upper bound to address fields (see ISO-13239:2002 4.2.2)
        __addresslength =  0
        if 127 > __parsechunk[__parsestart] or 255 == __parsechunk[__parsestart]:
            # 8bit address
            __addresslength = 1
        else:
            # more than 8bits (32 max)
            # __addresslenght becomes "predicitve"
            # -> will not be incremented when last byte found
            __addresslength = 1
            # check current byte
            while 127 <= __parsechunk[__addresslength-1]:
                __addresslength += 1
        # store address internally by slicing out
        self.set_address( __parsechunk[__parsestart:__addresslength] )

        __parsestart += __addresslength
        # read control field
        ## MSB = 0 -> I-frame

    def is_allstation(self):
        """Simple self-test for being a "all stattion" (=broadcast)
        frame. It may only be used with a command frame."""

        if None == self._HDLCBaseFrame__address:
            return False

        if (1 == len(self._HDLCBaseFrame__address)) and (255 == self._HDLCBaseFrame__address[0]):
            return True
        else:
            return False

    def is_nostation(self):
        """Simple self-test for being a "no station" frame. This is used
        for testing and data stations should not react to it."""

        if None == self._HDLCBaseFrame__address:
            return False
        # length doesn't matter, just first octet has to be zeros
        if (0 == self._HDLCBaseFrame__address[0]):
            return True
        else:
            return False

    def set_address(self,address):
        """This method sets the address field. An address can consist of 0, 8
        or 16bit. In the basic format, only 8bit addresses are allowed."""
        if not isinstance(address,bytes):
            raise TypeError("given address has to be of type bytes")
        if isinstance(self,HDLCBaseFrame) and 1 != len(address):
            raise ValueError("HDLC base frame only allows 8 bit addresses")
        if 2 < len(address):
            raise ValueError("address must not exceed 16 bits")

        self.__address = address


    def get_address(self):
        """Get address currently associated with the frame."""
        return self.__address
