#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file define Kylberg Texture Dataloader"""

import os

from ...dataset import Data, Dataset
from ...label import Classification
from .._utility import glob

DATASET_NAME = "KylbergTexture"


def KylbergTexture(path: str) -> Dataset:
    """
    Load the Kylberg Texture Dataset to TensorBay
    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        originalPNG/
            <imagename>.png
            ...
        withoutRotateAll/
            <imagename>.png
            ...
        RotateAll/
            <imagename>.png
            ...

    :return: a loaded dataset
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables.json"))

    for segment_name, label_getter in _LABEL_GETTERS.items():
        image_paths = glob(os.path.join(root_path, segment_name, "*.png"))

        segment = dataset.create_segment(segment_name)

        for image_path in image_paths:
            data = Data(image_path)
            stem = os.path.splitext(os.path.basename(image_path))[0]
            data.append_label(label_getter(stem))
            segment.append(data)

    return dataset


def _get_original_png_label(stem: str) -> Classification:
    """get label from stem of originalPng image name

    :param stem: stem of originalPng image name like `blanket1-a`
    :return: label of originalPng image
    """

    class_name, original_image_number = stem.split("-", 1)
    attributes = {
        "original image sample number": original_image_number,
        "patch number": None,
        "rotated degrees": 0,
    }
    return Classification(category=class_name, attributes=attributes)


def _get_without_rotate_all_label(stem: str) -> Classification:
    """get label from stem of withoutRotateAll image name

    :param stem: stem of withoutRotateAll image name like `blanket1-a-p001`
    :return: label of withoutRotateAll image
    """

    class_name, original_image_number, patch_number = stem.split("-", 2)
    attributes = {
        "original image sample number": original_image_number,
        "patch number": int(patch_number[1:]),
        "rotated degrees": 0,
    }
    return Classification(category=class_name, attributes=attributes)


def _get_rotated_all_label(stem: str) -> Classification:
    """get label from stem of RotateAll image name

    :param stem: stem of RotateAll image name like `blanket1-a-p001-r30`
    :return: label of RotateAll image
    """

    class_name, original_image_number, patch_number, rotated_degrees = stem.split("-", 3)
    attributes = {
        "original image sample number": original_image_number,
        "patch number": int(patch_number[1:]),
        "rotated degrees": int(rotated_degrees[1:]),
    }
    return Classification(category=class_name, attributes=attributes)


_LABEL_GETTERS = {
    "originalPNG": _get_original_png_label,
    "withoutRotateAll": _get_without_rotate_all_label,
    "RotatedAll": _get_rotated_all_label,
}
