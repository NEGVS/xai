import os
import os.path


class FileUtils:
    """文件/文件夹操作工具类"""

    """
         在指定文件夹下创建文件（支持写入初始内容）
         :param folder_path: 目标文件夹路径（相对/绝对）
         :param file_name: 要创建的文件名（如 "test.txt"、"data.json"）
         :param content: 文件初始内容（默认空字符串）
         :param overwrite: 是否覆盖已存在的文件（默认 False：不覆盖）
         :return: 成功返回文件完整路径，失败返回 None
    """

    # ========== 新增：创建文件方法 ==========
    @staticmethod
    def create_file(folder_path, file_name, content="", overwrite=False):

        # 1. 拼接文件完整路径
        full_file_path = os.path.join(folder_path, file_name)

        # 2. 先检查目标文件夹是否存在，不存在则提示/创建
        if not os.path.isdir(folder_path):
            print(f"错误：目标文件夹不存在 → {folder_path}")
            # 可选：自动创建目标文件夹（取消注释即可）
            # if FileUtils.create_folder(os.path.dirname(folder_path), os.path.basename(folder_path)) is None:
            #     return None
            return None

        # 3. 处理文件已存在的情况
        if os.path.exists(full_file_path) and not overwrite:
            print(f"提示：文件已存在，未覆盖 → {full_file_path}")
            return full_file_path  # 已存在也返回路径，仅提示不覆盖

        # 4. 写入文件（处理不同编码/权限问题）
        try:
            # 使用 with 语句自动关闭文件句柄（最佳实践）
            # encoding="utf-8" 确保中文等字符正常写入
            with open(full_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"文件创建成功 → {full_file_path}")
            return full_file_path

        except PermissionError:
            print(f"错误：权限不足，无法创建文件 → {full_file_path}")
            return None
        except Exception as e:
            print(f"创建文件失败：{e}")
            return None

        # 辅助方法：判断文件是否存在

    @staticmethod
    def is_file_exists(file_path):
        """判断文件是否存在"""
        return os.path.isfile(file_path)

    @staticmethod
    def create_folder(parent_dir, folder_name):
        """
        在指定的父文件夹下创建子文件夹
        :param parent_dir: 父文件夹路径（可以是相对路径或绝对路径）
        :param folder_name: 要创建的子文件夹名称
        :return: 成功返回创建的文件夹完整路径；失败返回 None
        """
        # 拼接完整的文件夹路径
        full_folder_path = os.path.join(parent_dir, folder_name)

        try:
            # exist_ok=True：如果文件夹已存在，不报错（避免重复创建的异常）
            # mode=0o755：设置文件夹权限（Linux/Mac生效，Windows忽略）
            os.makedirs(full_folder_path, exist_ok=True)
            print(f"文件夹创建成功（或已存在）：{full_folder_path}")
            return full_folder_path

        except PermissionError:
            print(f"权限不足，无法创建文件夹：{full_folder_path}")
            return None
        except FileNotFoundError:
            print(f"父文件夹不存在：{parent_dir}（无法创建嵌套文件夹）")
            return None
        except Exception as e:
            print(f"创建文件夹失败：{e}")
            return None

    # 可选扩展：判断文件夹是否存在
    @staticmethod
    def is_folder_exists(folder_path):
        """判断文件夹是否存在"""
        return os.path.isdir(folder_path)


# 测试代码（直接运行该文件时执行）
if __name__ == "__main__":
    # 创建 "test_folder" 文件夹
    parent_dir = '../../..'
    child_dir_arr = {'dao', 'model', 'utils', 'config'}

    # 创建文件
    content_str = '''# 实际项目中 强烈建议加上 __init__.py，文件可以是空的,否则有时会出现导入问题（尤其是 IDE、旧版本 Python、打包工具等）。# 作用：
            # 1️⃣ 告诉 Python 这是一个包
            # 2️⃣ IDE 能正确识别模块
            # 3️⃣ 防止导入冲突 
            # 4️⃣ 兼容旧 Python'''

    for a in child_dir_arr:
        # 示例2：创建嵌套文件夹（父文件夹不存在时，os.makedirs 会自动创建父文件夹）
        FileUtils.create_folder(parent_dir, a)

        # parent_dir_temp = parent_dir.join('/').join(a)
        parent_dir_temp = parent_dir + '/' + a
        print(parent_dir_temp)
        FileUtils.create_file(parent_dir_temp, '../__init__.py', content=content_str, overwrite=True)

    # 示例3：测试权限问题（比如系统盘根目录，可能无权限）
    # FileUtils.create_folder("C:/", "test_folder")  # Windows示例
    # FileUtils.create_folder("/root", "test_folder")  # Linux/Mac示例
