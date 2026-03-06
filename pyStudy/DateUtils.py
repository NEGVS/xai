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


if __name__ == '__main__':
    print("current date ")
    print("当前date对象:", DateUtils.get_date())
    print(DateUtils.get_date())
