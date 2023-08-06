import datetime as dt

import pytest

from ravenpy.models import HMETS


@pytest.mark.slow
class TestRavenERA5:
    def test_simple(self, era5_hr):

        params = (
            9.5019,
            0.2774,
            6.3942,
            0.6884,
            1.2875,
            5.4134,
            2.3641,
            0.0973,
            0.0464,
            0.1998,
            0.0222,
            -1.0919,
            2.6851,
            0.3740,
            1.0000,
            0.4739,
            0.0114,
            0.0243,
            0.0069,
            310.7211,
            916.1947,
        )

        model = HMETS()
        model(
            ts=era5_hr,
            params=params,
            start_date=dt.datetime(2018, 1, 1),
            end_date=dt.datetime(2018, 8, 10),
            name="Salmon",
            run_name="test-hmets-era5",
            area=4250.6,
            elevation=843.0,
            latitude=54.4848,
            longitude=-123.3659,
            rain_snow_fraction="RAINSNOW_DINGMAN",
            tas={"linear_transform": (1.0, -273.15), "time_shift": -0.25},
            pr={"linear_transform": (24000.0, 0.0), "time_shift": -0.25},
        )
