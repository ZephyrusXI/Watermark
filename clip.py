from PIL import Image, ImageGrab, ImageDraw, ImageFont
import tempfile
import os
import win32clipboard

Transparency = 20  # Opacity of text 0-100
font = ImageFont.truetype("arial.ttf", 30)  # Font and size
text = "Preview "  # Watermark text

def watermark():
    images = ImageGrab.grabclipboard()
    image_width, image_height = images.size
    text_width, text_height = font.getsize(text)
    alpha = (Transparency * 255) // 100
    max_repetitions_x = (image_width // (text_width + 30)) + 2  # Adjust the horizontal spacing between words
    max_repetitions_y = (image_height // (text_height + 30)) + 2  # Adjust the vertical spacing between words

    transparent_image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_image)

    for y in range(max_repetitions_y):
        for x in range(max_repetitions_x):
            text_color = (255, 255, 255, alpha) if (x + y) % 2 == 0 else (0, 0, 0, alpha)
            draw.text((x * (text_width + 30) - text_width, y * (text_height + 30) - text_height), text, font=font, fill=text_color)

    images.paste(transparent_image, (0, 0), transparent_image)

    images.show()

    # Save the new image with watermark as a temporary PNG file
    temp_file_path = os.path.join(tempfile.gettempdir(), "watermarked_image.png")
    images.save(temp_file_path, format="PNG")

    # Copy the file path to clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(temp_file_path, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()

if __name__ == "__main__":
    watermark()
