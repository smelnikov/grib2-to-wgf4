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
