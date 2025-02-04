# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import os
import stat

from torchvision.datasets import ImageNet

from qai_hub_models.datasets.common import BaseDataset
from qai_hub_models.models._shared.imagenet_classifier.app import IMAGENET_TRANSFORM
from qai_hub_models.utils.asset_loaders import CachedWebDatasetAsset

IMAGENETTE_FOLDER_NAME = "imagenette2-320"
IMAGENETTE_VERSION = 1
DEVKIT_ASSET = CachedWebDatasetAsset(
    "https://image-net.org/data/ILSVRC/2012/ILSVRC2012_devkit_t12.tar.gz",
    IMAGENETTE_FOLDER_NAME,
    IMAGENETTE_VERSION,
    "ILSVRC2012_devkit_t12.tar.gz",
)
IMAGENETTE_ASSET = CachedWebDatasetAsset(
    "https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-320.tgz",
    IMAGENETTE_FOLDER_NAME,
    IMAGENETTE_VERSION,
    "imagenette2-320.tgz",
)

# Imagenette data has 10 classes and are labeled 0-9.
# This maps the Imagenette class id to the actual Imagenet_1K class id.
IMAGENETTE_CLASS_MAP = {
    0: 0,
    1: 217,
    2: 482,
    3: 491,
    4: 497,
    5: 566,
    6: 569,
    7: 571,
    8: 574,
    9: 701,
}


class ImagenetteDataset(BaseDataset, ImageNet):
    """
    Class for using the Imagenette dataset published here:
        https://github.com/fastai/imagenette

    Contains ~4k images spanning 10 of the imagenet classes.
    """

    def __init__(self):
        self._download_data()
        BaseDataset.__init__(self, str(IMAGENETTE_ASSET.path(extracted=True)))
        ImageNet.__init__(
            self,
            root=IMAGENETTE_ASSET.path(),
            split="val",
            transform=IMAGENET_TRANSFORM,
            target_transform=lambda val: IMAGENETTE_CLASS_MAP[val],
        )

    def _validate_data(self) -> bool:
        devkit_path = DEVKIT_ASSET.path()

        # Check devkit exists
        if not devkit_path.exists():
            return False

        # Check devkit permissions
        devkit_permissions = os.stat(devkit_path).st_mode
        if devkit_permissions & stat.S_IEXEC != stat.S_IEXEC:
            return False

        # Check val data exists
        val_data_path = os.path.join(self.dataset_path, "val")
        if not os.path.exists(val_data_path):
            return False

        # Ensure 10 classes
        subdirs = os.listdir(val_data_path)
        if len(subdirs) != 10:
            return False

        # Ensure >= 300 samples per classes
        for subdir in subdirs:
            if len(os.listdir(os.path.join(val_data_path, subdir))) < 300:
                return False
        return True

    def _download_data(self) -> None:
        IMAGENETTE_ASSET.fetch(extract=True)
        devkit_path = DEVKIT_ASSET.fetch()
        devkit_st = os.stat(devkit_path)
        os.chmod(devkit_path, devkit_st.st_mode | stat.S_IEXEC)
        os.symlink(
            DEVKIT_ASSET.path(),
            IMAGENETTE_ASSET.path() / os.path.basename(DEVKIT_ASSET.path()),
        )
