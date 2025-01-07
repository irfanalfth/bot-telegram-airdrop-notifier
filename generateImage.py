from PIL import Image, ImageDraw, ImageFont
import os
import re

def generateImgAirdrop(heading, username, font_folder="font", 
                       font_bold_name="FiraCode-Bold.ttf", font_regular_name="FiraCode-Regular.ttf",
                       image_size=(1280, 720), background_color="black", text_color="white", font_size1=80, font_size2=50):
 
    font_path_bold = os.path.join(font_folder, font_bold_name)
    font_path_regular = os.path.join(font_folder, font_regular_name)
    
    file_path = os.path.join("img", f"{username}.jpg")
    
    if os.path.exists(file_path):
        print(f"Gambar sudah ada: {file_path}. Tidak perlu membuat ulang.")
        return file_path  
    
    image = Image.new("RGB", image_size, background_color)
    draw = ImageDraw.Draw(image)

    try:
        font1 = ImageFont.truetype(font_path_bold, font_size1)
        font2 = ImageFont.truetype(font_path_regular, font_size2)
    except IOError:
        raise FileNotFoundError("Salah satu font tidak ditemukan. Pastikan semua font tersedia di folder.")

    # Fungsi untuk menghapus ikon/emoji dari teks
    def remove_icons(text):
        # Regex untuk mendeteksi karakter non-ikon (alfabet, angka, simbol umum)
        return re.sub(r"[^\w\s.,!?@#&:;\"'(){}[\]<>+-=]", "", text)

    # Bersihkan heading dari ikon
    heading = remove_icons(heading)

    def wrap_text(text, font, max_width_px):
        lines = []
        for line in text.split("\n"):
            words = line.split()
            wrapped_line = ""
            for word in words:
                test_line = f"{wrapped_line} {word}".strip()
                bbox = draw.textbbox((0, 0), test_line, font=font)
                text_width = bbox[2] - bbox[0] 
                if text_width <= max_width_px:
                    wrapped_line = test_line
                else:
                    lines.append(wrapped_line)
                    wrapped_line = word
            if wrapped_line:
                lines.append(wrapped_line)
        return lines

    max_width_px = image_size[0] - 40  

    wrapped_heading = wrap_text(heading, font1, max_width_px)
    wrapped_username = wrap_text(username, font2, max_width_px)

    total_text_height = (len(wrapped_heading) * (font1.size + 10)) + (len(wrapped_username) * (font2.size + 10))

    current_y = (image_size[1] - total_text_height) // 2

    for line in wrapped_heading:
        bbox = draw.textbbox((0, 0), line, font=font1)
        text_width = bbox[2] - bbox[0]
        draw.text(((image_size[0] - text_width) // 2, current_y), line, font=font1, fill=text_color)
        current_y += font1.size + 10 

    current_y += 30  

    for line in wrapped_username:
        bbox = draw.textbbox((0, 0), line, font=font2)
        text_width = bbox[2] - bbox[0]
        draw.text(((image_size[0] - text_width) // 2, current_y), line, font=font2, fill=text_color)
        current_y += font2.size + 10 

    image.save(file_path)
    print(f"Gambar berhasil dibuat dan disimpan sebagai {file_path}")
    return file_path
