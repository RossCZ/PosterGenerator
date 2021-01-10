import sys
from PIL import Image, ImageFont, ImageDraw
from os import walk
import os

# settings
root_dir = "Data"
file_extension = ".jpg"
delimiter = "_"
size_of_images_px = 300
space_between_images_px = 100
no_of_rows = 2
no_of_columns = 2
title = "2020"
resolution_dpi = 200
font_size_labels = 16
font_size_title = 28
width_forced_cm = 2
height_forced_cm = 2

# https://stackoverflow.com/questions/15857117/python-pil-text-to-image-and-fonts
fonts_path = "C:\Windows\Fonts"
font = ImageFont.truetype(os.path.join(fonts_path, "calibrii.ttf"), font_size_labels)
font_tit = ImageFont.truetype(os.path.join(fonts_path, "calibrib.ttf"), font_size_title)

# calculate poster dimensions
width = no_of_columns * (size_of_images_px + space_between_images_px) + space_between_images_px
height = no_of_rows * (size_of_images_px + space_between_images_px) + space_between_images_px

print(f"Output size [px]: w = {width}, h = {height}")
in_to_cm = 2.54
print(f"Calculated output size [cm]: w = {width / (resolution_dpi * in_to_cm):.2f}, h = {height / (resolution_dpi * in_to_cm):.2f}")

width = int(width_forced_cm * in_to_cm * resolution_dpi)
height = int(height_forced_cm * in_to_cm * resolution_dpi)

# load and resize images
images = []
for (dirpath, dirnames, filenames) in walk(root_dir):
    for file in filenames:
        if file.endswith(file_extension):
            print(file)
            img = Image.open(os.path.join(dirpath, file))
            img = img.resize((size_of_images_px, size_of_images_px), Image.ANTIALIAS)

            label = file.split(file_extension)[0]
            label = label.split(delimiter)[1]
            # print(text)
            # print(img)
            # img.show()
            images.append((img, label))


# create final image
poster = Image.new('RGB', (width, height), color=(255, 255, 255, 0))  # RGBA

if no_of_rows * no_of_columns != len(images):
    print(f"Wrong number of images: {no_of_rows * no_of_columns} required, {len(images)} found  ")

# iterate through a 2 by 2 grid with 100 spacing, to place my image
inx = 0
for i in range(no_of_rows):
    for j in range(no_of_columns):
        y = i * (size_of_images_px + space_between_images_px) + space_between_images_px
        x = j * (size_of_images_px + space_between_images_px) + space_between_images_px
        # print(i, j, x, y)

        # paste the image at the location
        img, label = images[inx]
        poster.paste(img, (x, y))

        # add label
        draw = ImageDraw.Draw(poster)
        draw.text((x, y + size_of_images_px + 10), label, (0, 0, 0), font=font)

        inx += 1

# add title
draw = ImageDraw.Draw(poster)
draw.text((width / 2, space_between_images_px / 2), title, (0, 0, 0), font=font_tit)
poster.show()
poster.save("poster.jpg")
poster.save("poster.pdf", "PDF", resolution=resolution_dpi)
