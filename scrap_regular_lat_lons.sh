#
Usage()
{
echo "usage: scrap_regular_lat_lons [-h] [source] [outdir]

Scraps every *.regular*.grib2.bz2 file from the source URL and uncompress it.
Both files (compressed and uncompressed) are saved into outdir.

positional arguments:
  source    source URL
  outdir    path to output directory, it will be created if does not exist.


options:
  -h        show this help message and exit"
}

while getopts ":h" option; do
   case "$option" in
      h) 
        Usage
        exit ;;
   esac
done

if [ -z "$1" ]
then
  echo "error: the following arguments are required: source"
fi
if [ -z "$2" ]
then
  echo "error: the following arguments are required: outdir"
  exit 1
fi

(
mkdir -p $2 && cd $2;
curl -s $1 \
  | tr '"' '\n' \
  | tr "'" '\n' \
  | grep -e 'icon-.\+regular.\+grib2.bz2$' \
  | xargs -I% -P10  bash -c "curl -sO -C - '$1%' && echo %" \
  | xargs -I% -P10 bash -c "bunzip2 -f -k % && echo $PWD'/%' | sed 's/.bz2//'" \
  | sort
)
