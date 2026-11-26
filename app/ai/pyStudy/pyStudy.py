import os
import logging

# ============ 配置日志 ============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============ 1. 环境变量操作示例 ============
def demo_env_operations():
    """演示环境变量的读取和过滤"""
    try:
        logger.info("========== 环境变量操作示例 ==========")
        # 获取指定环境变量（安全方式，不存在返回 None）
        openai_key = os.getenv("OPENAI_API_KEY")
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        logger.info(f"OPENAI_API_KEY: {'已设置' if openai_key else '未设置'}")
        logger.info(f"DEEPSEEK_API_KEY: {'已设置' if deepseek_key else '未设置'}")

        # 过滤所有以 KEY 结尾的环境变量
        key_vars = {k: v for k, v in os.environ.items() if k.endswith("KEY")}
        logger.info(f"共找到 {len(key_vars)} 个 KEY 环境变量")
        for key in key_vars.keys():
            logger.info(f"  - {key}")
    except Exception as e:
        logger.error(f"环境变量操作失败: {e}", exc_info=True)


# ============ 2. 字符串统计示例 ============
def demo_string_count():
    """演示字符串字符统计"""
    try:
        logger.info("========== 字符串统计示例 ==========")
        text = "assdd"
        unique_chars = set(text)
        char_count = {c: text.count(c) for c in unique_chars}
        logger.info(f"字符串: {text}")
        logger.info(f"字符统计: {char_count}")
    except Exception as e:
        logger.error(f"字符串统计失败: {e}", exc_info=True)


# ============ 3. 列表/数组操作示例 ============
def demo_list_operations():
    """演示列表的判空、遍历、倒序等操作"""
    try:
        logger.info("========== 列表操作示例 ==========")
        empty_list = []
        normal_list = ["2", "d", "o"]

        # 判空示例
        logger.info(f"空列表判断: {'空' if not empty_list else '非空'}")
        logger.info(f"普通列表判断: {'空' if not normal_list else '非空'}")

        if normal_list:
            # 正序遍历
            logger.info("正序遍历:")
            for item in normal_list:
                logger.info(f"  - {item}")

            # 倒序遍历（方式1：reversed）
            logger.info("倒序遍历（方式1）:")
            for item in reversed(normal_list):
                logger.info(f"  - {item}")

            # 倒序遍历（方式2：切片）
            logger.info("倒序遍历（方式2）:")
            for item in normal_list[::-1]:
                logger.info(f"  - {item}")
    except Exception as e:
        logger.error(f"列表操作失败: {e}", exc_info=True)


# ============ 4. 排序示例 ============
def demo_sorting():
    """演示数字、字典、列表的各种排序方式"""
    try:
        logger.info("========== 排序示例 ==========")

        # 数字排序
        numbers = [1, 5, 8, 9, 33, 2]
        logger.info(f"原始数字: {numbers}")
        logger.info(f"正序排序: {sorted(numbers)}")
        logger.info(f"倒序排序: {sorted(numbers, reverse=True)}")

        # 字典按 key 排序
        data = {"b": 2, "a": 1, "c": 3}
        logger.info("字典按 key 正序:")
        for k, v in sorted(data.items(), key=lambda x: x[0]):
            logger.info(f"  {k}: {v}")

        # 字典按 value 排序
        logger.info("字典按 value 正序:")
        for k, v in sorted(data.items(), key=lambda x: x[1]):
            logger.info(f"  {k}: {v}")

        # 字典列表按单字段排序
        arr = [
            {"name": "z", "num": 9},
            {"name": "a", "num": 1},
            {"name": "m", "num": 5},
        ]
        logger.info("字典列表按 num 正序:")
        for item in sorted(arr, key=lambda d: d["num"]):
            logger.info(f"  {item}")

        # 字典列表按多字段排序
        multi_data = [
            {"dept": "A", "age": 22, "score": 80},
            {"dept": "B", "age": 20, "score": 90},
            {"dept": "A", "age": 22, "score": 75},
            {"dept": "A", "age": 20, "score": 88},
        ]
        logger.info("多字段排序（dept → age → score）:")
        for row in sorted(multi_data, key=lambda x: (x["dept"], x["age"], x["score"])):
            logger.info(f"  {row}")
    except Exception as e:
        logger.error(f"排序操作失败: {e}", exc_info=True)


# ============ 主函数 ============
def main():
    """执行所有示例"""
    logger.info("========== Python 学习示例开始 ==========")
    demo_env_operations()
    demo_string_count()
    demo_list_operations()
    demo_sorting()
    logger.info("========== Python 学习示例结束 ==========")


if __name__ == "__main__":
    main()