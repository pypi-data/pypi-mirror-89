import datetime

from dateutil.easter import easter  # pylint: disable=import-error

EVERY_YEAR = {
    "FI": {(1, 1), (6, 1), (1, 5), (6, 12), (24, 12), (25, 12), (26, 12)},
}

EASTER_RELATED = {
    "FI": {
        -2,  # Good Friday
        0,  # Easter Sunday
        1,  # Easter Monday
        39,  # Ascension
        49,  # Pentecost
    }
}

SPECIAL = {
    "FI": (
        lambda dt: dt.month == 6 and 20 < dt.day < 26 and dt.weekday == 6,  # Midsummer eve
        # All hallows day is always a Saturday, so not relevant
    )
}


def is_holiday(dt=None, country="FI"):
    """
    Checks if a given date is a public holiday in a country
    :param dt: datetime.datetime or None for today.
    :param country: 2 letter ISO-code
    :return: bool
    """
    if dt is None:
        dt = datetime.datetime.today().date()
    if ((dt.day, dt.month) in EVERY_YEAR[country]
            or dt.date in {(easter(dt.year) + datetime.timedelta(days=d)) for d in EASTER_RELATED[country]}
            or any(f(dt) for f in SPECIAL[country])):
        return True
    return False
