from PIL import Image


def remove_background(image_path, output_path, bg_color=(255, 255, 255), tolerance=10):
    # 打开图片并转换为 RGBA 模式
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # 判断是否为背景色（通过 RGB 距离和容差）
        if abs(item[0] - bg_color[0]) <= tolerance and \
                abs(item[1] - bg_color[1]) <= tolerance and \
                abs(item[2] - bg_color[2]) <= tolerance:
            # 将背景色替换为透明 (R, G, B, A=0)
            new_data.append((255, 255, 255, 0))
        else:
            # 保留原始颜色
            new_data.append(item)

    # 更新图片数据
    img.putdata(new_data)
    # 保存为 PNG 格式（支持透明度）
    img.save(output_path, "PNG")
    print(f"已保存透明背景图片到: {output_path}")


# 示例调用
if __name__ == "__main__":
    input_image = "/Users/andy_mac/PycharmProjects/xai/static/9.jpg"  # 输入图片路径
    output_image = "./output.png"  # 输出图片路径
    background_color = (255, 255, 255)  # 背景色，默认白色
    remove_background(input_image, output_image, background_color, tolerance=20)
