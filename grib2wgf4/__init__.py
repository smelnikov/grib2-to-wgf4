from dataclasses import dataclass
from typing import Protocol, SupportsIndex

import numpy as np
from numpy import ma

MISSING_VALUE = -100_500.0
PRECISION_DECIMALS = 6
PRECISION_SCALE = 10**PRECISION_DECIMALS

# fmt: off
class _IOProtocol(Protocol):
    def flush(self) -> object: ...
    def fileno(self) -> int: ...
    def tell(self) -> SupportsIndex: ...
    def seek(self, offset: int, whence: int, /) -> object: ...
# fmt: on


@dataclass
class FileHeader:
    min_lat: int
    max_lat: int
    min_lon: int
    max_lon: int
    step_lat: int
    step_lon: int
    scale: int

    @classmethod
    def from_latlons(cls, lats: np.ndarray, lons: np.ndarray) -> "FileHeader":
        lats, lons = lats.round(PRECISION_DECIMALS), lons.round(PRECISION_DECIMALS)
        min_lat = int(lats.min() * PRECISION_SCALE)
        max_lat = int(lats.max() * PRECISION_SCALE)
        min_lon = int(lons.min() * PRECISION_SCALE)
        max_lon = int(lons.max() * PRECISION_SCALE)
        step_lat = (max_lat - min_lat) // (lats.shape[0] - 1)
        step_lon = (max_lon - min_lon) // (lons.shape[1] - 1)

        return cls(
            min_lat, max_lat, min_lon, max_lon, step_lat, step_lon, PRECISION_SCALE
        )

    def tofile(self, fid: _IOProtocol) -> None:
        np.array(
            [
                self.min_lat,
                self.max_lat,
                self.min_lon,
                self.max_lon,
                self.step_lat,
                self.step_lon,
                self.scale,
            ],
            dtype="i",
        ).tofile(fid)


@dataclass
class GridValues:
    values: ma.MaskedArray

    @classmethod
    def from_accum(
        cls,
        curr: ma.MaskedArray,
        prev: ma.MaskedArray | None = None,
    ) -> "GridValues":
        pure_values = curr
        if prev is not None:
            pure_values = curr - prev
        return cls(pure_values)

    def tofile(self, fid: _IOProtocol) -> None:
        self.values.filled(MISSING_VALUE).astype(np.float32).tofile(fid)


@dataclass
class FileBuilder:
    header: FileHeader
    values: GridValues
    delimiter = np.array([MISSING_VALUE], dtype="f")

    def tofile(self, fid: _IOProtocol) -> None:
        self.header.tofile(fid)
        self.delimiter.tofile(fid)
        self.values.tofile(fid)
