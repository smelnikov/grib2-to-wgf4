import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, NamedTuple

import pygrib

from grib2wgf4 import FileBuilder, FileHeader, GridValues

GRIB_FILE_PATTERN = re.compile(
    r".*_regular-lat-lon_.*_(?P<dateGen>\d{10})_(?P<bias>\d{3})_.*"
)


class FileInfo(NamedTuple):
    fpath: Path
    dage_gen: datetime
    bias: timedelta


if __name__ == "__main__":
    outdir = "output"
    if sys.stdin.isatty():
        sys.stderr.write("Please, pipe filenames via stdin\n")
        sys.exit(1)

    errors: List[str] = []
    files_info: List[FileInfo] = []
    for line in sorted(sys.stdin.readlines()):
        fpath = Path(line.strip())
        if fpath.suffix != ".grib2":
            errors.append(f"Only grib2 files are supported as stdin: {fpath}")
            continue

        ma = GRIB_FILE_PATTERN.match(fpath.stem)
        if ma is None:
            errors.append(f"Cannot destruct filename: {fpath}")
            continue
        g = ma.groupdict()
        date_gen = datetime.strptime(g["dateGen"], "%Y%m%d%H")
        bias = timedelta(hours=int(g["bias"]))
        files_info.append(FileInfo(fpath, date_gen, bias))
    if errors:
        sys.stderr.writelines(errors)
        sys.exit(1)

    curr, prev = None, None
    for fpath, date_gen, bias in files_info:
        grbs = pygrib.open(os.fspath(fpath))
        grb = grbs.select(shortName="tp")[0]
        curr, lats, lons = grb.data()

        date_bias = date_gen + bias
        outpath = Path(f"{outdir}") / date_bias.strftime("%d.%m.%Y_%H:%M_unknown")
        outpath.mkdir(parents=True, exist_ok=True)
        outpath /= "PRATE.wgf4"

        with open(outpath, mode="wb") as fid:
            FileBuilder(
                FileHeader.from_latlons(lats, lons),
                GridValues.from_accum(curr, prev),
            ).tofile(fid)
            sys.stdout.write(f"{outpath}\n")
            prev = curr

        grbs.close()
