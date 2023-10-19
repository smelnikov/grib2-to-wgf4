# grib2-to-wgf4

There are some problems installing `pygrib` on macOS with ARM processors,
just use docker as environment.

```fish

docker build -t pygrib .

docker run --rm -it \
  --mount type=bind,source=(pwd),target=/app \
  pygrib \
  /bin/bash

```

Grab `*regular*.grib2.bz2` files from source,
download them into cwd,
unpack and stdout unpacked filenames.

Notes: compressed and uncompressed files will be stored in cwd.

```fish

echo https://opendata.dwd.de/weather/nwp/icon-d2/grib/12/tot_prec/ \
    | xargs -n1 curl -s \
    | tr '"' '\n' \
    | tr "'" '\n' \
    | grep -e 'icon-.\+regular.\+grib2.bz2$' \
    | xargs -I% -P10  bash -c "curl -C- -so % '$BASE_URL%' && echo %" \
    | xargs -I% -P10 bash -c "bunzip2 -f -k % && echo $PWD'/%' | sed 's/.bz2//'" \
    | sort

```
