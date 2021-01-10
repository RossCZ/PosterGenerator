import sys
from PIL import Image, ImageFont, ImageDraw
from os import walk
import os

# settings
root_dir = "Data"
ext = ".jpg"
delim = "_"
req_size = 300  # for images
spac = 100  # between images
rows = 2
columns = 2
title = "2020"

# https://stackoverflow.com/questions/15857117/python-pil-text-to-image-and-fonts
fonts_path = "C:\Windows\Fonts"
font = ImageFont.truetype(os.path.join(fonts_path, "calibrii.ttf"), 16)
font_tit = ImageFont.truetype(os.path.join(fonts_path, "calibrib.ttf"), 28)

# calculate poster dimensions
width = columns * (req_size + spac) + spac
height = rows * (req_size + spac) + spac

print(width, height)

# load and resize images
images = []
for (dirpath, dirnames, filenames) in walk(root_dir):
    for file in filenames:
        if file.endswith(ext):
            print(file)
            img = Image.open(os.path.join(dirpath, file))
            img = img.resize((req_size, req_size), Image.ANTIALIAS)

            label = file.split(ext)[0]
            label = label.split(delim)[1]
            # print(text)
            # print(img)
            # img.show()
            images.append((img, label))


# create final image
poster = Image.new('RGB', (width, height), color=(255, 255, 255, 0))  # RGBA

# iterate through a 2 by 2 grid with 100 spacing, to place my image
inx = 0
for i in range(rows):
    for j in range(columns):
        y = i * (req_size + spac) + spac
        x = j * (req_size + spac) + spac
        print(i, j, x, y)

        # paste the image at the location
        img, label = images[inx]
        poster.paste(img, (x, y))

        # add label
        draw = ImageDraw.Draw(poster)
        draw.text((x, y + req_size + 10), label, (0, 0, 0), font=font)

        inx += 1

# add title
draw = ImageDraw.Draw(poster)
draw.text((width / 2, spac / 2), title, (0, 0, 0), font=font_tit)
poster.show()
poster.save("poster.jpg")
poster.save("poster.pdf", "PDF", resolution=200.0)
