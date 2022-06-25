import re
from datetime import datetime
from calendar import monthrange


class dt(object):

    TODAY = "today"
    CURRENT_MONTH = "current_month"

    @classmethod
    def timerange_fromtext(cls, description) -> tuple:
        if description == cls.TODAY:
            carrytime = datetime.today()
            return (
                datetime(carrytime.year, carrytime.month, carrytime.day, 0, 0, 0),
                datetime(carrytime.year, carrytime.month, carrytime.day, 23, 59, 59)
            )
        if description == cls.CURRENT_MONTH:
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

    @classmethod
    def timerange_prevmonth(cls, months, starting_month=None) -> tuple:
        if starting_month is not None and re.match(r"^\d{4}\-\d{1,2}$", starting_month) is not None:
            year, month = map(lambda e: int(e), starting_month.split("-"))
            start_point = datetime(year, month, 1)
        else:
            start_point = datetime.today()

        target_year = start_point.year - (months // 12)
        target_month = start_point.month - (months - 12 * (months // 12))
        if target_month <= 0:
            target_month = 12 - abs(target_month)
            target_year -= 1

        startime = cls.timerange_fromtext(f"{target_year}-{target_month}")
        endtime = cls.timerange_fromtext(f"{start_point.year}-{start_point.month}")
        return (startime[0], endtime[1])


class strings(object):

    GENERAL_THOUSAND_SEPARATOR = ","
    GENERAL_DECIMAL_POINT = "."

    VN_THOUSAND_SEPARATOR = "."
    VN_DECIMAL_POINT = ","

    @classmethod
    def todecimal(cls, input: str, precision=2) -> float:
        """
        Convert 76,098.37 => float(76098.37)
        """
        number = input.replace(cls.GENERAL_THOUSAND_SEPARATOR, "")
        return round(float(number), precision)

    @classmethod
    def todecimal_dotts(cls, input: str, precision=2) -> float:
        """
        Convert 76.098,37 => float(76098.37)
        """
        # remove thousand separator
        parts = input.split(cls.VN_DECIMAL_POINT)
        number_part = parts[0].replace(cls.VN_THOUSAND_SEPARATOR, "")
        if len(parts) == 2:
            number = f"{number_part}.{parts[1]}"
        else:
            number = number_part
        return round(float(number), precision)

    @classmethod
    def toint_sipostfix(cls, input: str) -> int:
        """
        Convert 1k => 1_000
        """
        carry = 0
        for i in range(len(input)):
            if input[i].isnumeric():
                carry = carry * 10
                carry = carry + int(input[i])

        # multiply with decimal prefix
        if input[-1].isalpha():
            decimal_prefix = input[-1]
            if decimal_prefix == "k":
                carry = carry * 1000
            elif decimal_prefix == "M":
                carry = carry * 1000_000
            elif decimal_prefix == "G":
                carry = carry * 1000_000_000
        return carry

    @classmethod
    def is_numeric(cls, input: str) -> bool:
        match = re.match(r'^\d+(k|M|G)*$', input)
        return match is not None


class numeric(object):

    DECIMAL_PRECISION = 2

    @classmethod
    def floatval(cls, number, digit: int = DECIMAL_PRECISION) -> float:
        return round(float(number), digit)

    @classmethod
    def sipostfix_toint(cls, input: str) -> int:
        """
        Convert
            1k => 1_000
            1M => 1_000_000
            1G => 1_000_000_000
        """
        carry = 0
        for i in range(len(input)):
            if input[i].isnumeric():
                carry = carry * 10
                carry = carry + int(input[i])

        # multiply with decimal prefix
        if input[-1].isalpha():
            decimal_prefix = input[-1]
            if decimal_prefix == "k":
                carry = carry * 1000
            elif decimal_prefix == "M":
                carry = carry * 1000_000
            elif decimal_prefix == "G":
                carry = carry * 1000_000_000
        return carry
    pass
