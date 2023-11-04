from app.routes.bill import get_month_ends
import datetime

def test_get_month_ends():
    assert get_month_ends(datetime.datetime(2021, 1, 1)) == (
        datetime.datetime(2021, 1, 1, hour=0, minute=0, second=0),
        datetime.datetime(2021, 1, 31, hour=23, minute=59, second=59),
    )
    assert get_month_ends(datetime.datetime(2021, 12, 1)) == (
        datetime.datetime(2021, 12, 1, hour=0, minute=0, second=0),
        datetime.datetime(2021, 12, 31, hour=23, minute=59, second=59),
    )
    assert get_month_ends(datetime.datetime(2021, 2, 1)) == (
        datetime.datetime(2021, 2, 1, hour=0, minute=0, second=0),
        datetime.datetime(2021, 2, 28, hour=23, minute=59, second=59),
    )
    assert get_month_ends(datetime.datetime(2021, 3, 1)) == (
        datetime.datetime(2021, 3, 1, hour=0, minute=0, second=0),
        datetime.datetime(2021, 3, 31, hour=23, minute=59, second=59),
    )
    