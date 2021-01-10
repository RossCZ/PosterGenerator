import sys
from PIL import Image, ImageFont, ImageDraw
from os import walk
import os

# application settings
root_dir = "Data"
file_extension = ".jpg"
delimiter = "_"
size_of_images_px = 300
space_between_images_px = 100
space_on_edges_px = 200
no_of_rows = 2
no_of_columns = 2
title = "2020"
resolution_dpi = 150  # 300 is standard value for printing
font_size_labels = 16
font_size_title = 28
width_required_cm = 3
height_required_cm = 3

# font settings
# https://stackoverflow.com/questions/15857117/python-pil-text-to-image-and-fonts
fonts_path = "C:\Windows\Fonts"
font = ImageFont.truetype(os.path.join(fonts_path, "calibrii.ttf"), font_size_labels)
font_tit = ImageFont.truetype(os.path.join(fonts_path, "calibrib.ttf"), font_size_title)

# constants
in_to_cm = 2.54


def calculate_total_dimension_px(number_of_items):
    return number_of_items * size_of_images_px + (number_of_items - 1) * space_between_images_px + 2 * space_on_edges_px


def calculate_dimension_cm(dimension_px):
    return dimension_px / (resolution_dpi * in_to_cm)


def calculate_required_dpi(dimension_calculated, dimension_required):
    return dimension_calculated * resolution_dpi / dimension_required


def calculate_dimension_px(dimension_cm):
    return int(dimension_cm * in_to_cm * resolution_dpi)


def analyze_output_sizes():
    # calculate poster dimensions
    width = calculate_total_dimension_px(no_of_columns)
    height = calculate_total_dimension_px(no_of_rows)
    width_calculated_cm = calculate_dimension_cm(width)
    height_calculated_cm = calculate_dimension_cm(height)

    print(f"Calculated output size [px]: w = {width}, h = {height}")
    print(f"Calculated output size [cm]: w = {width_calculated_cm:.2f}, h = {height_calculated_cm:.2f}")
    print(f"Required dpi for width: {calculate_required_dpi(width_calculated_cm, width_required_cm):.2f}")
    print(f"Required dpi for height: {calculate_required_dpi(height_calculated_cm, height_required_cm):.2f}")


def load_and_resize_images():
    images = []
    for (dirpath, dirnames, filenames) in walk(root_dir):
        for file in filenames:
            if file.endswith(file_extension):
                print(f"\t{file}")
                img = Image.open(os.path.join(dirpath, file))
                img = img.resize((size_of_images_px, size_of_images_px), Image.ANTIALIAS)

                label = file.split(file_extension)[0]
                label = label.split(delimiter)[1]
                # print(text)
                # print(img)
                # img.show()
                images.append((img, label))
    return images


def main():
    analyze_output_sizes()

    images = load_and_resize_images()
    if no_of_rows * no_of_columns != len(images):
        print(f"Wrong number of images: {no_of_rows * no_of_columns} required, {len(images)} found ")
        return

    # create poster
    height = calculate_dimension_px(height_required_cm)
    width = calculate_dimension_px(width_required_cm)
    poster = Image.new('RGB', (width, height), color=(255, 255, 255, 0))  # RGBA

    # iterate through a the specified grid with specified spacing, to place the image
    inx = 0
    for i in range(no_of_rows):
        for j in range(no_of_columns):
            y = i * (size_of_images_px + space_between_images_px) + space_on_edges_px
            x = j * (size_of_images_px + space_between_images_px) + space_on_edges_px
            # print(i, j, x, y)

            # paste the image at the location
            img, label = images[inx]
            poster.paste(img, (x, y))

            # add label
            draw = ImageDraw.Draw(poster)
            draw.text((x, y + size_of_images_px + 10), label, (0, 0, 0), font=font)

            inx += 1

    # add title and save
    draw = ImageDraw.Draw(poster)
    text_width_approx = 0.5 * font_size_title * len(title)
    draw.text(((width - text_width_approx) / 2, space_on_edges_px / 2), title, (0, 0, 0), font=font_tit)
    poster.show()
    poster.save("poster.jpg")
    poster.save("poster.pdf", "PDF", resolution=resolution_dpi)


# Driver code
main()
