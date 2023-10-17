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

Crawling urls from page:

```fish

export BASE_URL="https://opendata.dwd.de/weather/nwp/icon-d2/grib/12/tot_prec/"

curl $BASE_URL \
    | tr '"' '\n' \
    | tr "'" '\n' \
    | grep -e 'icon-.\+regular.\+grib2.bz2$' \
    | sort | uniq \
    | xargs -L1 -I% -P10  bash -c "curl -O '$BASE_URL%' && bunzip2 %"

```
