# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.inception_v3_quantized.demo import main as demo_main
from qai_hub_models.models.inception_v3_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    InceptionNetV3Quantizable,
)


def test_task():
    run_imagenet_classifier_test(
        InceptionNetV3Quantizable.from_pretrained(),
        MODEL_ID,
        diff_tol=0.005,
        rtol=0.02,
        atol=0.2,
        asset_version=MODEL_ASSET_VERSION,
    )


def test_trace():
    run_imagenet_classifier_trace_test(
        InceptionNetV3Quantizable.from_pretrained(),
        diff_tol=0.01,
        rtol=0.02,
        atol=0.2,
        is_quantized=True,
    )


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
