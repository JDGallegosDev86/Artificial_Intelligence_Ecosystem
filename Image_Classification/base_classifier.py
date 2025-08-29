# base_classifier.py
# MobileNetV2 image classifier + Grad-CAM (saves heatmap & overlay)

import os
import numpy as np
import tensorflow as tf
tf.get_logger().setLevel("ERROR")

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

from PIL import Image
from matplotlib import cm  # for a JET color map

# -------------------------------------------------
# Load pretrained classifier (ImageNet, 1000 classes)
# -------------------------------------------------
model = MobileNetV2(weights="imagenet")


# -------------------------------------------------
# Basic classification (returns predictions + top id)
# -------------------------------------------------
def classify_image(image_path: str):
    """
    Loads an image, runs MobileNetV2, prints top-3 predictions.
    Returns: (predictions ndarray, top_class_index) on success, else (None, None).
    """
    try:
        # load and preprocess
        img = image.load_img(image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = preprocess_input(x)
        x = np.expand_dims(x, axis=0)  # shape -> (1,224,224,3)

        # forward pass
        preds = model.predict(x, verbose=0)

        # decode & print top-3
        top3 = decode_predictions(preds, top=3)[0]
        print(f"\nTop-3 Predictions for {image_path}")
        for i, (_, label, score) in enumerate(top3, start=1):
            print(f"  {i}: {label} ({score:.2f})")

        # return raw preds + argmax for Grad-CAM
        return preds, int(np.argmax(preds[0]))
    except Exception as e:
        print(f"Error processing '{image_path}': {e}")
        return None, None


# -------------------------------------------------
# Grad-CAM (no OpenCV; uses Pillow + matplotlib)
# -------------------------------------------------
def grad_cam(image_path: str,
             class_index: int | None = None,
             last_conv_layer_name: str = "Conv_1",
             alpha: float = 0.4):
    """
    Creates a Grad-CAM heatmap for class_index (or model's top class)
    and saves both a colored heatmap and an overlay image.

    last_conv_layer_name: for MobileNetV2 use 'Conv_1' (final conv layer).
    alpha: blend strength for overlay [0..1].
    """
    # 1) Load original at full size (for pretty overlay)
    orig = Image.open(image_path).convert("RGB")
    W, H = orig.size

    # 2) Preprocess copy at model size
    img224 = orig.resize((224, 224))
    x = image.img_to_array(img224)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    # 3) Build a model that returns feature maps + predictions
    conv_layer = model.get_layer(last_conv_layer_name)
    grad_model = tf.keras.Model([model.inputs], [conv_layer.output, model.output])

    with tf.GradientTape() as tape:
        conv_out, preds = grad_model(x)          # conv_out: (1,H,W,C)
        if class_index is None:
            class_index = int(tf.argmax(preds[0]))
        class_score = preds[:, class_index]      # scalar for target class

    # 4) d(class_score)/d(conv_out)
    grads = tape.gradient(class_score, conv_out)          # (1,H,W,C)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))        # (C,)

    # 5) Weighted sum over channels -> heatmap
    conv_out = conv_out[0]                                # (H,W,C)
    heatmap = tf.reduce_sum(conv_out * pooled, axis=-1)   # (H,W)
    heatmap = tf.nn.relu(heatmap)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
    heatmap = heatmap.numpy()                             # 0..1

    # 6) Resize to original size & colorize (JET)
    heat_uint8 = (heatmap * 255).astype("uint8")
    heat_resized = Image.fromarray(heat_uint8).resize((W, H), resample=Image.BILINEAR)
    heat_resized = np.array(heat_resized, dtype=np.float32) / 255.0
    heat_color = cm.jet(heat_resized)[..., :3]            # RGBA->RGB, in 0..1
    heat_color_u8 = (heat_color * 255).astype("uint8")

    # 7) Blend with original
    base = np.array(orig, dtype=np.float32)
    overlay = np.clip((1.0 - alpha) * base + alpha * heat_color_u8, 0, 255).astype("uint8")

    # 8) Save images
    stem, _ = os.path.splitext(os.path.basename(image_path))
    heat_path = f"{stem}_gradcam_heatmap.png"
    overlay_path = f"{stem}_gradcam_overlay.png"
    Image.fromarray(heat_color_u8).save(heat_path)
    Image.fromarray(overlay).save(overlay_path)
    print(f"Saved: {heat_path}, {overlay_path}")

    return heat_path, overlay_path


# -------------------------------------------------
# Simple CLI
# -------------------------------------------------
if __name__ == "__main__":
    print("Image Classifier + Grad-CAM (type 'exit' to quit)\n")
    while True:
        p = input("Enter image filename: ").strip()
        if p.lower() == "exit":
            print("Goodbye!")
            break
        if not os.path.isfile(p):
            print(f"File not found: {p}")
            continue

        preds, top_idx = classify_image(p)
        if preds is not None:
            grad_cam(p, class_index=top_idx)  # visualize top class