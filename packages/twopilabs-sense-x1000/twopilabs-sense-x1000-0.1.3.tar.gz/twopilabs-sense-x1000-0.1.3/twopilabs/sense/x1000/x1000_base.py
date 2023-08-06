from enum import Enum
from typing import NamedTuple
import struct
import numpy as np
import io


class SenseX1000Base(object):
    USB_VID: int = 0x1FC9
    USB_PID: int = 0x8271

    class RampMode(Enum):
        SINGLE = 0,
        DOUBLE = 1,
        ALTERNATING = 2

    class RadarStatus(Enum):
        OFF = 0,
        STANDBY = 11,
        READY = 12,
        BUSY = 15,
        DETECTFAIL = 40,
        MAGICFAIL = 45

    class ChannelCoupling(Enum):
        GND = 0,
        DC = 1,
        AC = 2

    class ChannelForce(Enum):
        NONE = 0,
        ON = 1,
        OFF = 2

    class FrequencyMode(Enum):
        CW = 0,
        SWEEP = 1

    class SweepDirection(Enum):
        DOWN = -1,
        UP = 1

    class SweepMode(Enum):
        NORMAL = 0,
        ALTERNATING = 1

    class AcqDType(Enum):
        S16RLE = 0
        S16RILE = 4

    class TrigSource(Enum):
        IMMEDIATE = 0

    class AcqHeader(NamedTuple):
        header_length: int
        header_id: int
        header_version: int
        flags: int
        bytes_total: int
        sweep_count: int
        trace_mask: int
        data_points: int
        data_size: int
        data_type: int

        @classmethod
        def struct(cls):
            return struct.Struct('<HBBLLLLLBBxxxxxx')

        @classmethod
        def from_stream(cls, stream):
            s = cls.struct()
            buffer = stream.read(s.size)
            header = s.unpack(buffer)
            info = SenseX1000Base.AcqHeader(*header)
            return info

        @property
        def trace_count(self):
            return bin(self.trace_mask).count('1')

        @property
        def trace_list(self):
            mask = self.trace_mask
            lst = []
            i = 0
            while mask > 0:
                if mask & (1 << i):
                    lst += [i]
                    mask = mask & ~(1 << i)
                i += 1
            return lst

        @property
        def acq_dtype(self):
            return SenseX1000Base.AcqDType(self.data_type)

        @property
        def np_dtype(self):
            # For converting dtype given in AcqInfo into a numpy datatype
            data_type_map = {
                SenseX1000Base.AcqDType.S16RLE.value: '<i2',
                SenseX1000Base.AcqDType.S16RILE.value: [('re', '<i2'), ('im', '<i2')]
            }

            return data_type_map[self.data_type]

        @property
        def flag_domain(self):
            return True if self.flags & (1 << 4) else False

        @property
        def flag_slope(self):
            return True if self.flags & (1 << 8) else False

        @property
        def flag_alternating(self):
            return True if self.flags & (1 << 9) else False

    class AcqData(object):
        array: np.array
        n_sweeps: int
        n_channels: int
        n_points: int
        seq_nums: list
        directions: list
        channels: list
        data_type: 'SenseX1000Base.AcqDType'
        data_size: int

        def __init__(self, data: bytes, header: 'SenseX1000Base.AcqHeader', seq_num: int, n_sweeps: int):
            self.n_sweeps = n_sweeps
            self.n_channels = header.trace_count
            self.n_points = header.data_points
            self.data_size = header.data_size
            self.data_type = header.acq_dtype
            self.array = np.reshape(
                np.frombuffer(data, dtype=header.np_dtype),
                [n_sweeps, header.trace_count, header.data_points])
            self.seq_nums = list(range(seq_num, seq_num + n_sweeps))
            self.direction = header.flag_slope
            self.directions = [bool(self.direction ^ (num % 2)) if header.flag_alternating else self.direction for
                               num in self.seq_nums]
            self.channels = header.trace_list

        @classmethod
        def from_stream(cls, stream, header, seq_num, n_sweeps):
            data = stream.read(n_sweeps * header.trace_count * header.data_points * header.data_size)
            return SenseX1000Base.AcqData(data, header, seq_num, n_sweeps)

    class Acquisition(object):
        """Class representing a data acquisition that has been triggered consisting of 1 or more successive sweeps."""
        _header: 'SenseX1000Base.AcqHeader'
        _stream: io.RawIOBase

        def __init__(self, header: 'SenseX1000Base.AcqHeader', stream: io.RawIOBase):
            self._header = header
            self._stream = stream
            self._sweeps_remaining = header.sweep_count
            self._seq_num = 0

        @property
        def header(self):
            return self._header

        @property
        def sweeps_remaining(self):
            return self._sweeps_remaining

        @property
        def seq_num(self):
            return self._seq_num

        def data(self, n_sweeps=-1):
            n_sweeps = self._sweeps_remaining if n_sweeps < 0 else min(n_sweeps, self._sweeps_remaining)

            # generator syntax
            while self._sweeps_remaining > 0:
                data = SenseX1000Base.AcqData.from_stream(self._stream, self._header, self._seq_num, n_sweeps)
                self._sweeps_remaining -= n_sweeps
                self._seq_num += n_sweeps
                yield data

        @classmethod
        def from_stream(cls, stream: io.RawIOBase):
            """Create the header from the device data stream and instantiate an Acquisition object"""
            header = SenseX1000Base.AcqHeader.from_stream(stream)
            return cls(header=header, stream=stream)
