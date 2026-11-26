import re


def extract_nums(text: str) -> list[int]:
    """
    1. 根据、分割字符串
    2. 提取每个片段里的数字，返回int列表
    示例："10服务员、13餐饮收银员、92酒吧服务员" → [10,13,92]
    """
    parts = text.split("、")
    res = []
    for p in parts:
        match = re.search(r"\d+", p)
        if match:
            res.append(int(match.group()))
    return res


# 测试
s = "10服务员、13餐饮收银员、92酒吧服务员"
print(extract_nums(s))  # [10, 13, 92]
