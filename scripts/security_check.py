#!/usr/bin/env python3
"""
安全检查脚本
检查项目中是否有硬编码的API密钥、密码等敏感信息
"""
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# 需要检查的文件扩展名
EXTENSIONS_TO_CHECK = {'.py', '.js', '.ts', '.java', '.yml', '.yaml', '.json', '.env', '.txt', '.md'}

# 需要排除的目录
EXCLUDE_DIRS = {
    'venv', 'myenv', 'env', '.venv', '__pycache__',
    'node_modules', '.git', 'dist', 'build', '.idea',
    '.vscode', 'target', 'bin', 'obj'
}

# 敏感信息的正则表达式模式
SENSITIVE_PATTERNS = [
    # API密钥模式
    (r'api[_-]?key\s*[=:]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?', 'API Key'),
    (r'apikey\s*[=:]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?', 'API Key'),

    # Google API密钥
    (r'AIza[0-9A-Za-z\-_]{35}', 'Google API Key'),

    # AWS密钥
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'aws_secret_access_key\s*[=:]\s*["\']?([A-Za-z0-9/+=]{40})["\']?', 'AWS Secret Key'),

    # 私钥
    (r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----', 'Private Key'),

    # 密码
    (r'password\s*[=:]\s*["\']([^"\'\s]{8,})["\']', 'Password'),
    (r'passwd\s*[=:]\s*["\']([^"\'\s]{8,})["\']', 'Password'),

    # Token
    (r'token\s*[=:]\s*["\']([A-Za-z0-9_\-\.]{20,})["\']', 'Token'),
    (r'bearer\s+([A-Za-z0-9_\-\.]{20,})', 'Bearer Token'),

    # 数据库连接字符串
    (r'(mysql|postgresql|mongodb)://[^:]+:[^@]+@', 'Database Connection String'),
]

# 允许的占位符模式（不报告为问题）
ALLOWED_PLACEHOLDERS = [
    'your_api_key_here',
    'your-api-key',
    'your_key_here',
    'placeholder',
    'dummy',
    'example',
    'test',
    'fake',
    'mock',
    'xxx',
    'yyy',
    'zzz',
    '12345',
    'abcde',
    'fghij',
    'klmno',
]


def is_placeholder(value: str) -> bool:
    """检查是否为占位符"""
    value_lower = value.lower()
    return any(placeholder in value_lower for placeholder in ALLOWED_PLACEHOLDERS)


def check_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    检查单个文件

    Args:
        file_path: 文件路径

    Returns:
        问题列表 [(行号, 问题类型, 匹配内容)]
    """
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # 跳过注释行
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//'):
                    continue

                # 检查每个敏感模式
                for pattern, issue_type in SENSITIVE_PATTERNS:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        matched_text = match.group(0)

                        # 跳过占位符
                        if is_placeholder(matched_text):
                            continue

                        # 跳过环境变量引用
                        if 'os.getenv' in line or 'os.environ' in line or '${' in line:
                            continue

                        issues.append((line_num, issue_type, matched_text[:100]))

    except Exception as e:
        print(f"⚠️  无法读取文件 {file_path}: {e}", file=sys.stderr)

    return issues


def scan_directory(root_dir: Path) -> Dict[Path, List[Tuple[int, str, str]]]:
    """
    扫描目录

    Args:
        root_dir: 根目录

    Returns:
        文件路径到问题列表的映射
    """
    results = {}

    for file_path in root_dir.rglob('*'):
        # 跳过目录
        if file_path.is_dir():
            continue

        # 跳过排除的目录
        if any(exclude in file_path.parts for exclude in EXCLUDE_DIRS):
            continue

        # 只检查指定扩展名的文件
        if file_path.suffix not in EXTENSIONS_TO_CHECK:
            continue

        # 检查文件
        issues = check_file(file_path)
        if issues:
            results[file_path] = issues

    return results


def main():
    """主函数"""
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent

    print("🔍 开始安全检查...")
    print(f"📂 项目目录: {project_dir}")
    print()

    # 扫描目录
    results = scan_directory(project_dir)

    # 输出结果
    if not results:
        print("✅ 未发现明显的安全问题！")
        return 0

    print(f"⚠️  发现 {len(results)} 个文件存在潜在安全问题：\n")

    total_issues = 0
    for file_path, issues in sorted(results.items()):
        rel_path = file_path.relative_to(project_dir)
        print(f"📄 {rel_path}")

        for line_num, issue_type, matched_text in issues:
            print(f"   行 {line_num}: [{issue_type}] {matched_text}")
            total_issues += 1

        print()

    print(f"❌ 共发现 {total_issues} 个潜在安全问题")
    print("\n建议:")
    print("1. 将所有敏感信息移到环境变量")
    print("2. 确保 .env 文件在 .gitignore 中")
    print("3. 使用 os.getenv() 或配置管理服务读取敏感信息")
    print("4. 不要在代码中硬编码任何密钥或密码")

    return 1


if __name__ == "__main__":
    sys.exit(main())
