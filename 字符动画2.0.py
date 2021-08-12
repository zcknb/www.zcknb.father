from PIL import Image, ImageDraw, ImageFont
import argparse
import numpy as np

sample_rate = 0.4


def ascii_art(file):
    im = Image.open(file)

    # 计算字母纵横比
    font = ImageFont.load_default()
    # 字体 = 图像方位.true 类型（"源代码专业.ttf"，大小=12）
    aspect_ratio = font.getsize("x")[0] / font.getsize("x")[1]
    new_im_size = np.array(
        [im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]
    ).astype(int)

    # 降低图像的上下
    im = im.resize(new_im_size)

    # 保留图像副本以进行颜色采样
    im_color = np.array(im)

    # 转换为灰色比例图像
    im = im.convert("L")

    # 转换为数字阵列以进行图像操作
    im = np.array(im)

    # 以上升顺序定义所有符号，以形成最终的 ascii
    symbols = np.array(list(" .-vM"))

    # 将最小值和最大值标准化为 [0，max_symbol_index）
    im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

    # 生成ascii art
    ascii = symbols[im.astype(int)]

    # 创建用于绘制ascii文本的输出图像
    letter_size = font.getsize("x")
    im_out_size = new_im_size * letter_size
    bg_color = "black"
    im_out = Image.new("RGB", tuple(im_out_size), bg_color)
    draw = ImageDraw.Draw(im_out)

    # 绘制文本
    y = 0
    for i, line in enumerate(ascii):
        for j, ch in enumerate(line):
            color = tuple(im_color[i, j])  # 原始图像的样本颜色
            draw.text((letter_size[0] * j, y), ch[0], fill=color, font=font)
        y += letter_size[1]  # 增加y字母高度

    # 保存图像文件
    im_out.save(file + ".ascii.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert any image to ascii art.")
    parser.add_argument(
        "file", type=str, help="input image file",
    )
    args = parser.parse_args()

    ascii_art(args.file)