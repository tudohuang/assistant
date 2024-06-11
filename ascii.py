from PIL import Image

def rgb_to_ansi(r, g, b):
    """將 RGB 轉換為 ANSI 顏色碼"""
    return f"\033[38;2;{r};{g};{b}m"

def image_to_ascii(image_path, output_width=500, character_set=None):
    if character_set is None:
        # 使用更多的字符來表示不同的灰度級別
        character_set = "@%#WMN8B@WMmamwoc=;:-,. "

    char_len = len(character_set)

    # 使用 os.path.join 以避免跨平台問題
    image_path1 = image_path.replace("\\", "/")

    img = Image.open(image_path1).convert("RGB")  # Convert image to RGB
    width, height = img.size
    ratio = height / width
    output_height = int(output_width * ratio * 0.55)  # 0.55因子用於調整寬高比，使得ASCII字符不會過於擁擠
    img = img.resize((output_width, output_height))

    pixels = list(img.getdata())

    # 將灰度值轉換為字符
    grayscale_characters = [character_set[(r + g + b) // 3 * (char_len - 1) // 255] for (r, g, b) in pixels]
    ascii_image = [grayscale_characters[index: index + output_width] for index in range(0, len(grayscale_characters), output_width)]

    # 打印帶顏色的 ASCII 圖像
    for y, row in enumerate(ascii_image):
        for x, char in enumerate(row):
            r, g, b = img.getpixel((x, y))
            print(f"{rgb_to_ansi(r, g, b)}{char}", end="")
        print("\033[0m")  # 重置 ANSI 顏色


# 測試函數
image_to_ascii("image.png")
