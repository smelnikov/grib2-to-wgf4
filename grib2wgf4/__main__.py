import struct

import pygrib

from grib2wgf4 import FileBuilder, FileHeader, GridValues

if __name__ == "__main__":
    grbs = pygrib.open(
        "./samples/icon-d2_germany_regular-lat-lon_single-level_2023101712_000_2d_tot_prec.grib2"
    )
    grb = grbs.select(shortName="tp")[0]

    values, lats, lons = grb.data()

    with open("output/temp.wgf4", mode="wb") as fid:
        FileBuilder(
            FileHeader.from_latlons(lats, lons),
            GridValues.from_accum(values, prev=None),
        ).tofile(fid)

    with open("output/temp.wgf4", mode="rb") as fid:
        print(struct.unpack("i" * 7 + "f", fid.read(32)))
        print(struct.unpack("f" * 8, fid.read(32)))
