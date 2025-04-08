import cv2
import numpy as np


def remove_background_cv2(image_path, output_path, lower_color=(240, 240, 240), upper_color=(255, 255, 255)):
    # 读取图片
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 定义背景颜色范围（RGB）
    lower = np.array(lower_color, dtype="uint8")
    upper = np.array(upper_color, dtype="uint8")

    # 创建掩码
    mask = cv2.inRange(img, lower, upper)
    # 反转掩码（前景为 255，背景为 0）
    mask = cv2.bitwise_not(mask)

    # 转换为 RGBA
    img_rgba = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    # 设置透明通道
    img_rgba[:, :, 3] = mask

    # 保存图片
    cv2.imwrite(output_path, img_rgba)
    print(f"已保存透明背景图片到: {output_path}")


# 示例调用
if __name__ == "__main__":
    input_image = "/Users/andy_mac/PycharmProjects/xai/static/9.jpg"  # 输入图片路径

    # input_image = "input.jpg"
    output_image = "./output2.png"
    remove_background_cv2(input_image, output_image)
