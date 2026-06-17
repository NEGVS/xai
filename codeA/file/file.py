# 在指定的文件夹下，创建多个 指定的的文件夹

import os

"""
    在指定父目录批量创建多个文件夹
    :param parent_path: 父目录路径
    :param folder_list: 要创建的文件夹名列表
    """


def create_batch_folders(parent_path: str, folder_list: list):
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    for folder in folder_list:
        full_path = os.path.join(parent_path, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"已创建: {full_path}")


# 调用示例
if __name__ == "__main__":
    # 根目录
    base_dir = r"/Users/andy_mac/Documents/CodeSpace/srzp/ai-engineering-center"
    # 待创建文件夹
    need_folders = ["openspec", "skills", "prompts", "standards", "workflows"]
    create_batch_folders(base_dir, need_folders)
