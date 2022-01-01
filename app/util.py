import re
from datetime import datetime
from calendar import monthrange

class Datetime:
    @staticmethod
    def get_time_range_from_text(description) -> tuple:
        if description == "today":
            carrytime = datetime.today()
            return (
                datetime(carrytime.year, carrytime.month, carrytime.day, 0, 0, 0),
                datetime(carrytime.year, carrytime.month, carrytime.day, 23, 59, 59)
            )
        if description == "current_month":
            carrytime = datetime.today()
            month_range = monthrange(carrytime.year, carrytime.month)
            return (
                datetime(carrytime.year, carrytime.month, 1, 0, 0, 0),
                datetime(carrytime.year, carrytime.month, month_range[1], 23, 59, 59)
            )
        if re.match(r"^\d{4}\-\d{1,2}$", description) is not None:
            year, month = map(lambda e: int(e), description.split("-"))
            month_range = monthrange(year, month)
            return (
                datetime(year, month, 1, 0, 0, 0),
                datetime(year, month, month_range[1], 23, 59, 59)
            )

        return tuple()

    @staticmethod
    def get_time_range_in_past_month(months, starting_month=None) -> tuple:
        if starting_month is not None and re.match(r"^\d{4}\-\d{1,2}$", starting_month) is not None:
            year, month = map(lambda e: int(e), starting_month.split("-"))
            start_point = datetime(year, month, 1)
        else:
            start_point = datetime.today()

        target_year = start_point.year - (months//12)
        target_month = start_point.month - (months - 12*(months//12))
        if target_month <= 0 :
            target_month = 12 - abs(target_month)
            target_year -= 1

        startime = Datetime.get_time_range_from_text(f"{target_year}-{target_month}")
        endtime = Datetime.get_time_range_from_text(f"{start_point.year}-{start_point.month}")
        return ( startime[0], endtime[1])
