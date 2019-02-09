import datetime
from datetime import date
from typing import Optional

from .Utils import Utils


class Dates:
    current_date: datetime.datetime

    def __init__(self, current_date: Optional[datetime.datetime] = None):
        self.current_date = Utils.first_non_none(current_date, Dates.today_())

    @staticmethod
    def format_(date_obj: datetime.datetime, format_string: str = '%Y/%m%/d %H:%m:%s') -> str:
        return date_obj.strftime(format_string)

    @staticmethod
    def get_date_(date_obj: datetime.datetime) -> date:
        return date_obj.date()

    @staticmethod
    def subtract_(date_obj: datetime.datetime, **kwargs) -> datetime.datetime:
        return date_obj - datetime.timedelta(**kwargs)

    @staticmethod
    def subtract_days_(date_obj: datetime.datetime, days: int = 1) -> datetime.datetime:
        return Dates.subtract_(date_obj, days=days)

    @staticmethod
    def is_today_(date_obj: datetime.datetime) -> bool:
        return Dates.today_().now().date() == date_obj.date()

    @staticmethod
    def today_() -> datetime.datetime:
        return datetime.datetime.today()

    def format(self, format_string: str = '%Y/%m%/d %H:%m:%s') -> str:
        return Dates.format_(self.current_date, format_string=format_string)

    def get_date(self) -> date:
        return Dates.get_date_(self.current_date)

    def subtract(self, **kwargs) -> datetime.datetime:
        return Dates.subtract_(self.current_date, **kwargs)

    def subtract_days(self, days: int = 1) -> datetime.datetime:
        return Dates.subtract_days_(self.current_date, days=days)

    def is_today(self) -> bool:
        return Dates.is_today_(self.current_date)
