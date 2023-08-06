#!/usr/bin/env python3

import argparse
import os.path as osp
import time
from typing import Union

import cv2

import matplotlib
import matplotlib.pyplot as plt

import numpy as np

from PIL import Image

import torch

from torchvision import transforms

from equilib.equi2equi import TorchEqui2Equi

matplotlib.use("Agg")


def preprocess(
    img: Union[np.ndarray, Image.Image],
    is_cv2: bool = False,
) -> torch.Tensor:
    r"""Preprocesses image"""
    if isinstance(img, np.ndarray) and is_cv2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if isinstance(img, Image.Image):
        # Sometimes images are RGBA
        img = img.convert("RGB")

    to_tensor = transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    )
    img = to_tensor(img)
    assert len(img.shape) == 3, "input must be dim=3"
    assert img.shape[0] == 3, "input must be HWC"
    return img


def postprocess(
    img: torch.Tensor,
    to_cv2: bool = False,
) -> Union[np.ndarray, Image.Image]:
    if to_cv2:
        img = np.asarray(img.to("cpu").numpy() * 255, dtype=np.uint8)
        img = np.transpose(img, (1, 2, 0))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img
    else:
        to_PIL = transforms.Compose(
            [
                transforms.ToPILImage(),
            ]
        )
        img = img.to("cpu")
        img = to_PIL(img)
        return img


def test_video(path: str) -> None:
    r"""Test video"""
    # Rotation:
    pi = np.pi
    inc = pi / 180
    roll = 0  # -pi/2 < a < pi/2
    pitch = 0  # -pi < b < pi
    yaw = 0

    # Initialize equi2equi
    equi2equi = TorchEqui2Equi(h_out=320, w_out=640)
    device = torch.device("cuda")

    times = []
    cap = cv2.VideoCapture(path)

    while cap.isOpened():
        ret, frame = cap.read()

        rot = {
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,
        }

        if not ret:
            break

        s = time.time()
        src_img = preprocess(frame, is_cv2=True).to(device)
        out_img = equi2equi(
            src=src_img,
            rot=rot,
            sampling_method="torch",
            mode="bilinear",
        )
        out_img = postprocess(out_img, to_cv2=True)
        e = time.time()
        times.append(e - s)

        # cv2.imshow("video", out_img)

        # change direction `wasd` or exit with `q`
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
        if k == ord("w"):
            roll -= inc
        if k == ord("s"):
            roll += inc
        if k == ord("a"):
            pitch += inc
        if k == ord("d"):
            pitch -= inc

    cap.release()
    cv2.destroyAllWindows()

    print(sum(times) / len(times))
    x_axis = [i for i in range(len(times))]
    plt.plot(x_axis, times)
    save_path = osp.join("./results", "times_equi2equi_torch_video.png")
    plt.savefig(save_path)


def test_image(path: str) -> None:
    r"""Test single image"""
    # Rotation:
    rot = {
        "roll": 0,  #
        "pitch": np.pi / 4,  # vertical
        "yaw": np.pi / 4,  # horizontal
    }

    # Initialize equi2equi
    equi2equi = TorchEqui2Equi(h_out=320, w_out=640)
    device = torch.device("cuda")

    # Open Image
    src_img = Image.open(path)
    src_img = preprocess(src_img).to(device)

    out_img = equi2equi(
        src=src_img,
        rot=rot,
        sampling_method="torch",
        mode="bilinear",
    )
    out_img = postprocess(out_img)

    out_path = osp.join("./results", "output_equi2equi_torch_image.jpg")
    out_img.save(out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", action="store_true")
    parser.add_argument("--data", nargs="?", default=None, type=str)
    args = parser.parse_args()

    data_path = args.data
    if args.video:
        if data_path is None:
            data_path = "./data/R0010028_er_30.MP4"
        assert osp.exists(data_path)
        test_video(data_path)
    else:
        if data_path is None:
            data_path = "./data/equi.jpg"
        assert osp.exists(data_path)
        test_image(data_path)


if __name__ == "__main__":
    main()
