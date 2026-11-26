import os
import logging
from collections import Counter, defaultdict, deque
from itertools import chain, groupby
from functools import reduce
import json
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

# ============ 配置日志 ============
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# ============ 1. 环境变量操作 ============
def demo_env_operations():
    """环境变量的读取和过滤"""
    try:
        logger.info("\n========== 1. 环境变量操作 ==========")
        # 1-1 安全获取环境变量（不存在返回 None）
        openai_key = os.getenv("OPENAI_API_KEY")
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        logger.info(f"1-1 OPENAI_API_KEY: {'已设置' if openai_key else '未设置'}")
        logger.info(f"1-1 DEEPSEEK_API_KEY: {'已设置' if deepseek_key else '未设置'}")

        # 1-2 过滤环境变量（列表推导式）
        key_vars = {k: v for k, v in os.environ.items() if k.endswith("KEY")}
        logger.info(f"1-2 共找到 {len(key_vars)} 个 KEY 环境变量")
        for key in key_vars.keys():
            logger.info(f"    - {key}")
    except Exception as e:
        logger.error(f"环境变量操作失败: {e}", exc_info=True)


# ============ 2. 字符串操作 ============
def demo_string_operations():
    """字符串统计、切片、格式化"""
    try:
        logger.info("\n========== 2. 字符串操作 ==========")
        text = "assdd"

        # 2-1 字符统计（使用 Counter）
        char_count = Counter(text)
        logger.info(f"2-1 字符串: {text}")
        logger.info(f"2-1 字符统计: {dict(char_count)}")

        # 2-2 字符串切片
        s = "Hello World"
        logger.info(f"2-2 原字符串: {s}")
        logger.info(f"2-2 前5个字符: {s[:5]}")
        logger.info(f"2-2 后5个字符: {s[-5:]}")
        logger.info(f"2-2 倒序: {s[::-1]}")

        # 2-3 字符串格式化（3种方式）
        name, age = "张三", 25
        logger.info(f"2-3 f-string: 姓名={name}, 年龄={age}")
        logger.info("2-3 format: 姓名={}, 年龄={}".format(name, age))
        logger.info("2-3 %格式化: 姓名=%s, 年龄=%d" % (name, age))

        # 2-4 字符串拆分与合并
        words = "apple,banana,orange"
        split_words = words.split(",")
        logger.info(f"2-4 拆分: {split_words}")
        logger.info(f"2-4 合并: {' | '.join(split_words)}")
    except Exception as e:
        logger.error(f"字符串操作失败: {e}", exc_info=True)


# ============ 3. 列表操作 ============
def demo_list_operations():
    """列表判空、遍历、切片、推导式"""
    try:
        logger.info("\n========== 3. 列表操作 ==========")

        # 3-1 判空
        empty_list = []
        normal_list = [1, 2, 3, 4, 5]
        logger.info(f"3-1 空列表判断: {'空' if not empty_list else '非空'}")
        logger.info(f"3-1 普通列表判断: {'空' if not normal_list else '非空'}")

        # 3-2 列表推导式
        squares = [x**2 for x in range(1, 6)]
        evens = [x for x in range(1, 11) if x % 2 == 0]
        logger.info(f"3-2 平方数: {squares}")
        logger.info(f"3-2 偶数: {evens}")

        # 3-3 列表切片
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        logger.info(f"3-3 前5个: {nums[:5]}")
        logger.info(f"3-3 后5个: {nums[-5:]}")
        logger.info(f"3-3 每隔2个取1个: {nums[::2]}")
        logger.info(f"3-3 倒序: {nums[::-1]}")

        # 3-4 列表去重（保持顺序）
        items = [1, 2, 2, 3, 1, 4, 3, 5]
        unique_items = list(dict.fromkeys(items))
        logger.info(f"3-4 原列表: {items}")
        logger.info(f"3-4 去重后: {unique_items}")

        # 3-5 列表展平（flatten）
        nested = [[1, 2], [3, 4], [5, 6]]
        flat = list(chain.from_iterable(nested))
        logger.info(f"3-5 嵌套列表: {nested}")
        logger.info(f"3-5 展平后: {flat}")
    except Exception as e:
        logger.error(f"列表操作失败: {e}", exc_info=True)


# ============ 4. 字典操作 ============
def demo_dict_operations():
    """字典遍历、合并、defaultdict、推导式"""
    try:
        logger.info("\n========== 4. 字典操作 ==========")

        # 4-1 字典遍历
        user = {"name": "张三", "age": 25, "city": "北京"}
        logger.info("4-1 字典遍历:")
        for k, v in user.items():
            logger.info(f"    {k}: {v}")

        # 4-2 字典合并（3种方式）
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 3, "c": 4}
        merged1 = {**dict1, **dict2}
        merged2 = dict1.copy()
        merged2.update(dict2)
        logger.info(f"4-2 字典1: {dict1}")
        logger.info(f"4-2 字典2: {dict2}")
        logger.info(f"4-2 合并结果: {merged1}")

        # 4-3 defaultdict（自动初始化）
        word_count = defaultdict(int)
        words = ["apple", "banana", "apple", "orange", "banana", "apple"]
        for word in words:
            word_count[word] += 1
        logger.info(f"4-3 单词计数: {dict(word_count)}")

        # 4-4 字典推导式
        numbers = {"a": 1, "b": 2, "c": 3}
        squared = {k: v**2 for k, v in numbers.items()}
        logger.info(f"4-4 原字典: {numbers}")
        logger.info(f"4-4 值平方: {squared}")

        # 4-5 字典安全取值
        data = {"name": "李四"}
        logger.info(f"4-5 安全取值 name: {data.get('name', '未知')}")
        logger.info(f"4-5 安全取值 age: {data.get('age', 0)}")
    except Exception as e:
        logger.error(f"字典操作失败: {e}", exc_info=True)


# ============ 5. 集合操作 ============
def demo_set_operations():
    """集合去重、交集、并集、差集"""
    try:
        logger.info("\n========== 5. 集合操作 ==========")

        # 5-1 集合去重
        items = [1, 2, 2, 3, 1, 4, 3, 5]
        unique = set(items)
        logger.info(f"5-1 原列表: {items}")
        logger.info(f"5-1 去重后: {unique}")

        # 5-2 集合运算
        set_a = {1, 2, 3, 4, 5}
        set_b = {4, 5, 6, 7, 8}
        logger.info(f"5-2 集合A: {set_a}")
        logger.info(f"5-2 集合B: {set_b}")
        logger.info(f"5-2 交集: {set_a & set_b}")
        logger.info(f"5-2 并集: {set_a | set_b}")
        logger.info(f"5-2 差集A-B: {set_a - set_b}")
        logger.info(f"5-2 对称差集: {set_a ^ set_b}")

        # 5-3 集合成员检查（O(1)性能）
        large_set = set(range(10000))
        logger.info(f"5-3 9999 在集合中: {9999 in large_set}")
        logger.info(f"5-3 10001 在集合中: {10001 in large_set}")
    except Exception as e:
        logger.error(f"集合操作失败: {e}", exc_info=True)


# ============ 6. 排序操作 ============
def demo_sorting():
    """数字、字典、多字段排序"""
    try:
        logger.info("\n========== 6. 排序操作 ==========")

        # 6-1 数字排序
        numbers = [5, 2, 8, 1, 9]
        logger.info(f"6-1 原始: {numbers}")
        logger.info(f"6-1 正序: {sorted(numbers)}")
        logger.info(f"6-1 倒序: {sorted(numbers, reverse=True)}")

        # 6-2 字典按 key/value 排序
        data = {"b": 3, "a": 1, "c": 2}
        logger.info(f"6-2 按key排序: {dict(sorted(data.items()))}")
        logger.info(f"6-2 按value排序: {dict(sorted(data.items(), key=lambda x: x[1]))}")

        # 6-3 对象列表按单字段排序
        users = [
            {"name": "张三", "age": 25},
            {"name": "李四", "age": 20},
            {"name": "王五", "age": 30}
        ]
        sorted_users = sorted(users, key=lambda x: x["age"])
        logger.info("6-3 按年龄排序:")
        for user in sorted_users:
            logger.info(f"    {user}")

        # 6-4 多字段排序
        students = [
            {"class": "A", "score": 85, "name": "张三"},
            {"class": "B", "score": 90, "name": "李四"},
            {"class": "A", "score": 90, "name": "王五"},
            {"class": "A", "score": 85, "name": "赵六"}
        ]
        sorted_students = sorted(students, key=lambda x: (x["class"], -x["score"], x["name"]))
        logger.info("6-4 多字段排序（班级↑ 分数↓ 姓名↑）:")
        for student in sorted_students:
            logger.info(f"    {student}")
    except Exception as e:
        logger.error(f"排序操作失败: {e}", exc_info=True)


# ============ 7. 条件判断与循环 ============
def demo_control_flow():
    """if/else、for、while、break/continue"""
    try:
        logger.info("\n========== 7. 条件判断与循环 ==========")

        # 7-1 三元表达式
        age = 20
        status = "成年" if age >= 18 else "未成年"
        logger.info(f"7-1 年龄{age}，状态: {status}")

        # 7-2 for 循环遍历索引和值
        fruits = ["苹果", "香蕉", "橙子"]
        logger.info("7-2 enumerate遍历:")
        for idx, fruit in enumerate(fruits, start=1):
            logger.info(f"    {idx}. {fruit}")

        # 7-3 while 循环
        count = 0
        result = []
        while count < 5:
            result.append(count)
            count += 1
        logger.info(f"7-3 while循环结果: {result}")

        # 7-4 break 和 continue
        logger.info("7-4 break示例（遇到5停止）:")
        for i in range(1, 10):
            if i == 5:
                break
            logger.info(f"    {i}")

        logger.info("7-4 continue示例（跳过偶数）:")
        for i in range(1, 10):
            if i % 2 == 0:
                continue
            logger.info(f"    {i}")
    except Exception as e:
        logger.error(f"控制流操作失败: {e}", exc_info=True)


# ============ 8. 函数式编程 ============
def demo_functional_programming():
    """map、filter、reduce、lambda"""
    try:
        logger.info("\n========== 8. 函数式编程 ==========")

        # 8-1 map 映射
        numbers = [1, 2, 3, 4, 5]
        squared = list(map(lambda x: x**2, numbers))
        logger.info(f"8-1 原列表: {numbers}")
        logger.info(f"8-1 map平方: {squared}")

        # 8-2 filter 过滤
        evens = list(filter(lambda x: x % 2 == 0, numbers))
        logger.info(f"8-2 filter偶数: {evens}")

        # 8-3 reduce 累积
        sum_result = reduce(lambda x, y: x + y, numbers)
        product = reduce(lambda x, y: x * y, numbers)
        logger.info(f"8-3 reduce求和: {sum_result}")
        logger.info(f"8-3 reduce求积: {product}")

        # 8-4 组合使用
        result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
        logger.info(f"8-4 偶数平方: {result}")
    except Exception as e:
        logger.error(f"函数式编程失败: {e}", exc_info=True)


# ============ 9. 异常处理 ============
def demo_exception_handling():
    """try/except/else/finally"""
    try:
        logger.info("\n========== 9. 异常处理 ==========")

        # 9-1 基础异常捕获
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            logger.info(f"9-1 捕获异常: {e}")

        # 9-2 多异常捕获
        try:
            data = {"name": "张三"}
            age = data["age"]
        except KeyError as e:
            logger.info(f"9-2 KeyError: 键{e}不存在")
        except Exception as e:
            logger.info(f"9-2 其他异常: {e}")

        # 9-3 else 和 finally
        try:
            result = 10 / 2
        except ZeroDivisionError:
            logger.info("9-3 除零异常")
        else:
            logger.info(f"9-3 计算成功，结果: {result}")
        finally:
            logger.info("9-3 finally 总会执行")
    except Exception as e:
        logger.error(f"异常处理演示失败: {e}", exc_info=True)


# ============ 10. 文件操作 ============
def demo_file_operations():
    """文件读写、JSON、with语句"""
    try:
        logger.info("\n========== 10. 文件操作 ==========")

        # 使用临时目录，with 退出后自动清理，不覆盖用户文件
        with tempfile.TemporaryDirectory(prefix="python-study-") as temp_dir:
            file_path = Path(temp_dir) / "example.txt"
            file_path.write_text("Hello Python\n第二行\n", encoding="utf-8")
            content = file_path.read_text(encoding="utf-8")
            logger.info(f"10-1 Path读写文件：{file_path.name}，内容行数={len(content.splitlines())}")

        # 10-2 JSON 序列化与反序列化
        data = {"name": "张三", "age": 25, "skills": ["Python", "Java"]}
        json_str = json.dumps(data, ensure_ascii=False)
        logger.info(f"10-2 对象转JSON: {json_str}")
        logger.info(f"10-2 JSON转对象: {json.loads(json_str)}")
    except Exception as e:
        logger.error(f"文件操作失败: {e}", exc_info=True)


# ============ 11. 高级数据结构 ============
def demo_advanced_data_structures():
    """deque、Counter、groupby"""
    try:
        logger.info("\n========== 11. 高级数据结构 ==========")

        # 11-1 deque（双端队列，高性能）
        dq = deque([1, 2, 3])
        dq.append(4)
        dq.appendleft(0)
        logger.info(f"11-1 deque: {list(dq)}")
        logger.info(f"11-1 右弹出: {dq.pop()}")
        logger.info(f"11-1 左弹出: {dq.popleft()}")

        # 11-2 Counter（计数器）
        words = ["apple", "banana", "apple", "orange", "banana", "apple"]
        counter = Counter(words)
        logger.info(f"11-2 计数结果: {dict(counter)}")
        logger.info(f"11-2 最常见2个: {counter.most_common(2)}")

        # 11-3 groupby（分组）
        data = [
            {"type": "A", "value": 1},
            {"type": "A", "value": 2},
            {"type": "B", "value": 3},
            {"type": "B", "value": 4}
        ]
        sorted_data = sorted(data, key=lambda x: x["type"])
        logger.info("11-3 分组结果:")
        for key, group in groupby(sorted_data, key=lambda x: x["type"]):
            logger.info(f"    {key}: {list(group)}")
    except Exception as e:
        logger.error(f"高级数据结构失败: {e}", exc_info=True)


# ============ 12. 迭代器与生成器 ============
def fibonacci(limit: int) -> Iterator[int]:
    """生成前 limit 个斐波那契数；生成器按需产出，避免一次性创建大列表。"""
    left, right = 0, 1
    for _ in range(max(0, limit)):
        yield left
        left, right = right, left + right


def demo_iterators_and_generators() -> None:
    logger.info("\n========== 12. 迭代器与生成器 ==========")
    values = fibonacci(8)
    logger.info(f"12-1 生成器对象类型: {type(values).__name__}")
    logger.info(f"12-2 惰性取值: {list(values)}")
    logger.info(f"12-3 any/all: any([0, 2])={any([0, 2])}, all([1, 2])={all([1, 2])}")


# ============ 13. 装饰器与闭包 ============
def log_call(func):
    """演示装饰器并保留原函数元信息。"""
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@log_call
def add_numbers(left: int, right: int) -> int:
    return left + right


def make_multiplier(factor: int):
    """闭包捕获外层变量；返回一个可复用的函数。"""
    return lambda value: value * factor


def demo_decorators_and_closures() -> None:
    logger.info("\n========== 13. 装饰器与闭包 ==========")
    logger.info(f"13-1 装饰器调用结果: {add_numbers(2, 3)}")
    triple = make_multiplier(3)
    logger.info(f"13-2 闭包调用结果: {triple(4)}")


# ============ 14. 类型提示与数据类 ============
@dataclass(frozen=True)
class Student:
    name: str
    score: float


def average_score(scores: Sequence[float]) -> Optional[float]:
    """空输入明确返回 None，避免除零异常。"""
    return sum(scores) / len(scores) if scores else None


def demo_types_and_dataclasses() -> None:
    logger.info("\n========== 14. 类型提示与数据类 ==========")
    students = [Student("张三", 90.0), Student("李四", 86.5)]
    score_by_name: Dict[str, float] = {student.name: student.score for student in students}
    logger.info(f"14-1 dataclass对象: {students[0]}")
    logger.info(f"14-2 类型提示字典: {score_by_name}")
    logger.info(f"14-3 平均分: {average_score([student.score for student in students])}")
    logger.info(f"14-4 空集合平均分: {average_score([])}")


# ============ 15. 正则表达式 ============
def demo_regular_expressions() -> None:
    logger.info("\n========== 15. 正则表达式 ==========")
    text = "订单号: A20261126001，手机号: 13800138000"
    order = re.search(r"A\d{11}", text)
    phone = re.sub(r"(\d{3})\d{4}(\d{4})", r"\1****\2", text)
    logger.info(f"15-1 提取订单号: {order.group(0) if order else '未匹配'}")
    logger.info(f"15-2 脱敏手机号: {phone}")


# ============ 16. 日期时间 ============
def demo_datetime() -> None:
    logger.info("\n========== 16. 日期时间 ==========")
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    logger.info(f"16-1 格式化时间: {now:%Y-%m-%d %H:%M:%S}")
    logger.info(f"16-2 一天后: {tomorrow:%Y-%m-%d}")
    logger.info(f"16-3 ISO解析: {datetime.fromisoformat('2026-11-26T09:30:00')}")


# ============ 17. 排序与迭代工具 ============
def demo_iteration_tools() -> None:
    logger.info("\n========== 17. 排序与迭代工具 ==========")
    from itertools import islice, product

    records = [{"name": "甲", "score": 80}, {"name": "乙", "score": 95}, {"name": "丙", "score": 95}]
    logger.info(f"17-1 稳定排序: {sorted(records, key=lambda item: (-item['score'], item['name']))}")
    logger.info(f"17-2 islice惰性截取: {list(islice(range(1000000), 3))}")
    logger.info(f"17-3 product笛卡尔积: {list(product(['小', '大'], ['杯', '碗']))}")


# ============ 18. 模块入口与可重复调用 ============
def demo_main_guard() -> None:
    logger.info("\n========== 18. 脚本入口 ==========")
    logger.info("__name__ == '__main__' 时直接运行；被 import 时只定义对象，不自动执行全部示例")


# ============ 主函数 ============
def main():
    """执行所有示例"""
    logger.info("========== Python 学习示例开始 ==========")
    demo_env_operations()
    demo_string_operations()
    demo_list_operations()
    demo_dict_operations()
    demo_set_operations()
    demo_sorting()
    demo_control_flow()
    demo_functional_programming()
    demo_exception_handling()
    demo_file_operations()
    demo_advanced_data_structures()
    demo_iterators_and_generators()
    demo_decorators_and_closures()
    demo_types_and_dataclasses()
    demo_regular_expressions()
    demo_datetime()
    demo_iteration_tools()
    demo_main_guard()
    logger.info("\n========== Python 学习示例结束 ==========")


if __name__ == "__main__":
    main()
