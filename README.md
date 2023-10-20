# grib2-to-wgf4

## Docker

There are some problems installing `pygrib` on macOS with ARM processors,
just use docker as environment.

```sh
docker build -t pygrib .
docker run --rm -it \
  --mount type=bind,source=$(pwd),target=/app \
  pygrib \
  /bin/bash
```

## Dependencies

```sh
apt-get update
apt-get install libeccodes-dev curl
pip install -r requirements.txt
```

## Commands

### bash scrap_regular_lat_lons.sh

```
usage: scrap_regular_lat_lons [-h] [source] [outdir]

Scraps every *.regular*.grib2.bz2 file from the source URL and uncompress it.
Both files (compressed and uncompressed) are saved into outdir.

positional arguments:
  source    source URL
  outdir    path to output directory, it will be created if does not exist.


options:
  -h        show this help message and exit
```

### python -m grib2wfg4

```
usage: grib2wgf4 [-h] outdir

Reads list of grib2-filenames via stdin and converts them to wgf4 format

positional arguments:
  outdir      Path to output directory, it will be created if does not exist.

options:
  -h, --help  show this help message and exit
```

## Usage

```sh
bash scrap_regular_lat_lons.sh \
    https://opendata.dwd.de/weather/nwp/icon-d2/grib/12/tot_prec/ \
    /tmp/input \
    | python -m grib2wgf4 /tmp/output
```

Compressed and uncompressed GRIB2-files will be stored into `/tmp/input`

```sh
find /tmp/input -type f | sort | head -4
/tmp/input/icon-d2_germany_regular-lat-lon_single-level_2023101912_000_2d_tot_prec.grib2
/tmp/input/icon-d2_germany_regular-lat-lon_single-level_2023101912_000_2d_tot_prec.grib2.bz2
/tmp/input/icon-d2_germany_regular-lat-lon_single-level_2023101912_001_2d_tot_prec.grib2
/tmp/input/icon-d2_germany_regular-lat-lon_single-level_2023101912_001_2d_tot_prec.grib2.bz2
...
```

Converted files will be stored into `/tmp/output`

```sh
find /tmp/output -type f | sort | head -4
/tmp/output/19.10.2023_12:00_1697716800/PRATE.wgf4
/tmp/output/19.10.2023_13:00_1697720400/PRATE.wgf4
/tmp/output/19.10.2023_14:00_1697724000/PRATE.wgf4
/tmp/output/19.10.2023_15:00_1697727600/PRATE.wgf4
...
```
