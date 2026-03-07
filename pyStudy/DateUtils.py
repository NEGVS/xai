import time
from datetime import datetime, date, timedelta


class DateUtils:
    """
    日期时间工具类，支持获取当前/偏移时间（返回date对象、格式化字符串、时间戳）
    偏移规则：入参为正数 → 未来N天；入参为负数 → 过去N天；无参 → 当前时间
    """
    # 定义默认的日期字符串格式（可根据需求修改）
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def get_date(cls, days_offset: int = 0) -> date:
        current_date = date.today()
        target_date = current_date + timedelta(days=days_offset)
        return target_date

    @classmethod
    def get_datetime(cls, days_offset: int = 0) -> datetime:
        """
        获取偏移后的datetime对象（含时分秒）
        :param days_offset: 天数偏移量，默认0
        :return: datetime对象（如：2026-03-06 15:30:20）
        """
        current_dt = datetime.now()
        target_dt = current_dt + timedelta(days=days_offset)
        return target_dt

    @classmethod
    def get_timestamp(cls, days_offset: int = 0) -> int:
        """
        获取偏移后的时间戳（秒级）
        :param days_offset: 天数偏移量，默认0
        :return: 秒级时间戳（如：1741452620）
        """
        target_dt = cls.get_datetime(days_offset)
        # 转换为秒级时间戳（int类型，便于使用）
        timestamp = int(target_dt.timestamp())
        return timestamp


if __name__ == '__main__':
    print("current date ")
    print("当前date对象:", DateUtils.get_date())
    print(DateUtils.get_date())
    print(DateUtils.get_datetime())
    print(DateUtils.get_timestamp())
