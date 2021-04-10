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
        if re.match("^\d{4}\-\d{1,2}$", description) is not None:
            year, month = map(lambda e: int(e), description.split("-"))
            month_range = monthrange(year, month)
            return (
                datetime(year, month, 1, 0, 0, 0),
                datetime(year, month, month_range[1], 23, 59, 59)
            )

        return tuple()
