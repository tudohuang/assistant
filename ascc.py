import os
import time
import curses
from PIL import Image, ImageSequence
from moviepy.editor import VideoFileClip
import argparse

def rgb_to_curses_color(r, g, b):
    """將 RGB 轉換為 curses 顏色碼"""
    return 16 + 36 * (r // 51) + 6 * (g // 51) + (b // 51)

def image_to_ascii(image, width=100, character_set=None):
    if character_set is None:
        # 使用更多的字符來表示不同的灰度級別
        character_set = "@%#*+=-:. "

    char_len = len(character_set)
    img_width, img_height = image.size
    ratio = img_height / img_width / 1.65
    height = int(width * ratio)
    image = image.resize((width, height))
    pixels = list(image.getdata())

    # 將灰度值轉換為字符
    grayscale_characters = [character_set[(r + g + b) // 3 * (char_len - 1) // 255] for (r, g, b) in pixels]
    ascii_image = [grayscale_characters[index: index + width] for index in range(0, len(grayscale_characters), width)]

    return ascii_image

def display_ascii_animation(stdscr, path, width=100, sec=0.1):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(int(sec * 1000))
    curses.start_color()
    curses.use_default_colors()

    max_color_pairs = min(curses.COLORS, curses.COLOR_PAIRS - 1)
    
    for i in range(0, max_color_pairs):
        curses.init_pair(i + 1, i, -1)

    def draw_frame(frame, width):
        ascii_image = image_to_ascii(frame, width)
        for y, row in enumerate(ascii_image):
            for x, char in enumerate(row):
                r, g, b = frame.getpixel((x, y))
                color = rgb_to_curses_color(r, g, b)
                color_pair = (color % max_color_pairs) + 1
                stdscr.addstr(y, x, char, curses.color_pair(color_pair))
        stdscr.refresh()

    try:
        if width <= 300:
            file_extension = os.path.splitext(path)[-1].lower()
            last_ascii_art = None

            if file_extension == '.gif':
                try:
                    gif = Image.open(path)
                except Exception as e:
                    raise ValueError(f"Failed to open image at {path}: {e}")

                for _ in range(20):  # Loop 20 times to simulate a longer animation
                    for index, frame in enumerate(ImageSequence.Iterator(gif)):
                        if (index + 1) % 2 != 0:
                            frame = frame.convert("RGB")
                            draw_frame(frame, width)
                            time.sleep(sec)
                            if stdscr.getch() != -1:
                                return

            elif file_extension == '.mp4':
                clip = VideoFileClip(path)
                duration = clip.duration

                if duration < 300:  # Less than 5 minutes
                    for frame in clip.iter_frames(fps=24, dtype='uint8'):
                        frame_image = Image.fromarray(frame, 'RGB')
                        draw_frame(frame_image, width)
                        time.sleep(sec)
                        if stdscr.getch() != -1:
                            return
                else:
                    raise ValueError("Video is too long to convert to ASCII animation.")
            else:
                raise ValueError("Unsupported file format. Only GIF and MP4 are supported.")
        else:
            stdscr.addstr(0, 0, "Width is too large.")
            stdscr.refresh()
            time.sleep(2)

    except Exception as e:
        stdscr.addstr(0, 0, f"An error occurred: {e}")
        stdscr.refresh()
        time.sleep(2)

def ascii_display(path, width, sec):
    curses.wrapper(display_ascii_animation, path, width, sec)

def main():
    parser = argparse.ArgumentParser(description='ASCII Art Display')
    parser.add_argument('-p', '--path', type=str, required=True, help='Path to the image or video file')
    parser.add_argument('-w', '--width', type=int, default=100, help='Width of the ASCII art')
    parser.add_argument('-s', '--sec', type=float, default=0.1, help='Seconds between frames')

    args = parser.parse_args()

    ascii_display(args.path, args.width, args.sec)

if __name__ == "__main__":
    main()
