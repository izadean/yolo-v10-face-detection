import argparse
import os

import click
from sklearn.model_selection import train_test_split


def split(images_dir: str, labels_dir: str, image_names: list[str], dst_dir: str, split_name: str) -> None:
    for image in image_names:
        os.rename(os.path.join(images_dir, image), os.path.join(dst_dir, split_name, "images", image))
        label_file = os.path.splitext(image)[0] + ".txt"
        os.rename(os.path.join(labels_dir, label_file), os.path.join(dst_dir, split_name, "labels", label_file))


def init_dirs(dst_dir: str) -> None:
    os.makedirs(dst_dir, exist_ok=True)
    os.makedirs(os.path.join(dst_dir, "train", "images"), exist_ok=True)
    os.makedirs(os.path.join(dst_dir, "train", "labels"), exist_ok=True)
    os.makedirs(os.path.join(dst_dir, "val", "images"), exist_ok=True)
    os.makedirs(os.path.join(dst_dir, "val", "labels"), exist_ok=True)
    os.makedirs(os.path.join(dst_dir, "test", "images"), exist_ok=True)
    os.makedirs(os.path.join(dst_dir, "test", "labels"), exist_ok=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", type=str, help="Path to images directory")
    parser.add_argument("--labels-dir", type=str, help="Path to labels directory")
    parser.add_argument("--dst-dir", type=str, help="Path to destination directory")
    parser.add_argument("--train-ratio", type=float, help="Training ratio")
    parser.add_argument("--val-ratio", type=float, help="Validation ratio")
    parser.add_argument("--test-ratio", type=float, help="Test ratio")
    return parser.parse_args()


@click.command
@click.argument("images-dir", type=click.Path(exists=True, file_okay=False))
@click.argument("labels-dir", type=click.Path(exists=True, file_okay=False))
@click.option("--target-dir", "-f", type=click.Path(exists=True, file_okay=False), default="data/processed")
@click.option("--val-ratio", "-v", type=float, default=0.15)
@click.option("--test-ratio", "-s", type=float, default=0.15)
def main(
        images_dir: str,
        labels_dir: str,
        target_dir: str,
        val_ratio: float,
        test_ratio: float
) -> None:
    init_dirs(target_dir)

    images = [f for f in os.listdir(images_dir)]

    train_and_val_images, test_images = train_test_split(images, test_size=test_ratio, random_state=1)
    train_images, val_images = train_test_split(
        train_and_val_images,
        test_size=val_ratio / (1 - test_ratio), random_state=1
    )

    split(images_dir, labels_dir, train_images, target_dir, "train")
    split(images_dir, labels_dir, val_images, target_dir, "val")
    split(images_dir, labels_dir, test_images, target_dir, "test")


if __name__ == "__main__":
    main()
