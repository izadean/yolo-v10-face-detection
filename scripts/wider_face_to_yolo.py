import os

import click
import pandas as pd
from PIL import Image


@click.command
@click.argument("annotations-file", type=click.Path(exists=True, dir_okay=False))
@click.argument("labels-dir", type=click.Path(exists=True, file_okay=False))
@click.argument("images-dir", type=click.Path(exists=True, file_okay=False))
def main(annotations_file: str, labels_dir: str, images_dir: str) -> None:
    data = _to_data_frame(annotations_file, images_dir)

    for image_name in data["image_name"].unique():
        image_rows = data[data["image_name"] == image_name]
        image_width = image_rows.iloc[0, :]["image_width"]
        image_height = image_rows.iloc[0, :]["image_height"]

        target = ""

        for index, row in image_rows.iterrows():
            x1 = row["x1"]
            y1 = row["y1"]
            w = row["w"]
            h = row["h"]

            x_center = x1 + (w / 2)
            y_center = y1 + (h / 2)
            x_center /= image_width
            y_center /= image_height
            w /= image_width
            h /= image_height

            target += f"0 {x_center} {y_center} {w} {h}\n"

        yolo_file_path = os.path.join(
            labels_dir, os.path.splitext(image_name)[0] + ".txt"
        )
        with open(yolo_file_path, "a") as yolo_file:
            yolo_file.write(target)


def _get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height


def _to_data_frame(annotations_file: str, images_dir: str):
    columns = _get_column_names()
    rows = []

    with open(annotations_file) as f:
        lines = f.readlines()

    current_image_name = ""
    current_image_width_and_height = (0, 0)
    for line in lines:
        split_line = line.split(" ")
        split_length = len(split_line)
        if split_length == 11:
            x1, y1, w, h, *_ = split_line
            image_width, image_height = current_image_width_and_height
            rows.append(
                (
                    current_image_name,
                    float(x1),
                    float(y1),
                    float(w),
                    float(h),
                    image_width,
                    image_height,
                )
            )
        elif split_length == 1:
            try:
                int(line)
            except Exception:
                current_image_name = line[:-1].split("/")[-1]
                current_image_width_and_height = _get_image_size(
                    os.path.join(images_dir, current_image_name)
                )
    data = pd.DataFrame(rows, columns=columns)
    return data


def _get_column_names():
    return ["image_name", "x1", "y1", "w", "h", "image_width", "image_height"]


if __name__ == '__main__':
    main()
