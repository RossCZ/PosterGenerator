from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

# application settings
root_dir = "Data"
label_override = "labels.txt"
file_extension = ".jpg"
delimiter = "_"
size_of_images_cm = 8
space_between_images_cm = 1
space_on_hor_edges_cm = 3
space_on_ver_edges_cm = 4
no_of_rows = 7
no_of_columns = 5
title = "2020"
resolution_dpi = 300  # 300 is standard value for printing
font_size_labels = 50
font_size_title = 200

# font settings
# https://stackoverflow.com/questions/15857117/python-pil-text-to-image-and-fonts
fonts_path = Path("C:/Windows/Fonts")
font = ImageFont.truetype(Path(fonts_path, "calibrii.ttf").as_posix(), font_size_labels)
font_tit = ImageFont.truetype(Path(fonts_path, "calibri.ttf").as_posix(), font_size_title)

# constants
in_to_cm = 2.54


def calculate_total_dimension_cm(number_of_items, space_on_edges_cm):
    return number_of_items * size_of_images_cm + (number_of_items - 1) * space_between_images_cm + 2 * space_on_edges_cm


def calculate_dimension_px(dimension_cm):
    return int(round(dimension_cm * resolution_dpi / in_to_cm))


def calculate_poster_size():
    width_cm = calculate_total_dimension_cm(no_of_columns, space_on_hor_edges_cm)
    height_cm = calculate_total_dimension_cm(no_of_rows, space_on_ver_edges_cm)
    width_px = calculate_dimension_px(width_cm)
    height_px = calculate_dimension_px(height_cm)
    print(f"Calculated poster size [cm]: w = {width_cm:.2f}, h = {height_cm:.2f}")
    print(f"Calculated poster size [px]: w = {width_px}, h = {height_px}")
    return width_px, height_px


def get_overridden_labels():
    labels_override_file = Path(root_dir, label_override)
    if labels_override_file.exists():
        labels = {}

        with open(labels_override_file) as file:
            for line in file:
                line_txt = line.rstrip()
                label_parts = line_txt.split(delimiter)
                labels[label_parts[0]] = label_parts[1]
        if len(labels) > 0:
            return labels
    return {}


def load_and_resize_images(size_of_images):
    overridden_labels = get_overridden_labels()
    images = []
    for file in sorted(Path(root_dir).glob(f"*{file_extension}")):
        print(f"\t{file.stem}")
        img = Image.open(file)

        # check image aspect ratio 1:1
        if img.size[0] != img.size[1]:
            print(f"\t\tWARNING: aspect ratio 1:{img.size[0] / img.size[1]:.2f}")

        img = img.resize((size_of_images, size_of_images), Image.LANCZOS)
        # img.show()

        label_parts = file.stem.split(file_extension)[0].split(delimiter)
        label = label_parts[1]
        label_key = label_parts[0]

        # overriden label?
        if label_key in overridden_labels:
            label = overridden_labels[label_key]
            print(f"\t\t-> {label}")

        images.append((img, label))
    return images


def main():
    # calculate dimensions in pixels
    width, height = calculate_poster_size()
    size_of_images_px = calculate_dimension_px(size_of_images_cm)
    space_between_images_px = calculate_dimension_px(space_between_images_cm)
    space_on_hor_edges_px = calculate_dimension_px(space_on_hor_edges_cm)
    space_on_ver_edges_px = calculate_dimension_px(space_on_ver_edges_cm)

    images = load_and_resize_images(size_of_images_px)
    if no_of_rows * no_of_columns != len(images):
        print(f"Wrong number of images: {no_of_rows * no_of_columns} required, {len(images)} found ")
        return

    # create poster
    poster = Image.new("RGB", (width, height), color=(255, 255, 255, 0))  # RGBA

    # iterate through the specified grid with specified spacing, to place the image
    inx = 0
    for i in range(no_of_rows):
        for j in range(no_of_columns):
            y = i * (size_of_images_px + space_between_images_px) + space_on_ver_edges_px
            x = j * (size_of_images_px + space_between_images_px) + space_on_hor_edges_px
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
    draw.text(((width - text_width_approx) / 2, space_on_ver_edges_px / 2), title, (0, 0, 0), font=font_tit)
    poster.show()
    poster.save("poster.jpg")
    poster.save("poster.pdf", "PDF", resolution=resolution_dpi)


if __name__ == "__main__":
    main()
