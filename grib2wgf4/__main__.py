import pygrib

if __name__ == "__main__":
    grbs = pygrib.open(
        "./data/icon-d2_germany_regular-lat-lon_single-level_2023101712_000_2d_tot_prec.grib2"
    )

    grbs.seek(0)

    for grb in grbs.select(shortName="tp"):
        print(grb)

        values, lats, lons = grb.data()

        print(values.shape)
        print(lats.shape, lats.min(), lats.max(), lons.shape, lons.min(), lons.max())
