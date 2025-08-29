# new_filter.py
# Runs like basic_filter.py: single prompt loop (filename -> process -> save).
# Default effect = Pencil Sketch. Change CHOSEN_FILTER to "blur" to mimic the old blur.

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np
import os

# Choose which effect to run without extra prompts: "sketch" or "blur"
CHOSEN_FILTER = "sketch"   # change to "blur" if you want the old blur behavior

def apply_blur_filter(image_path, output_path="blurred_image.png", radius=2, size=(128, 128)):
    """Simple Gaussian blur after resizing (keeps behavior close to basic_filter.py)."""
    img = Image.open(image_path).convert("RGB")
    img_resized = img.resize(size, Image.LANCZOS)
    img_blurred = img_resized.filter(ImageFilter.GaussianBlur(radius=radius))
    img_blurred.save(output_path)
    print(f"Processed image saved as '{output_path}'.")

def pencil_sketch_filter(image_path, output_path="sketch.png", blur_radius=7, strength=1.0, contrast=1.15):
    """Pencil-sketch via invert + blur + color-dodge blend, then subtle contrast boost."""
    gray = Image.open(image_path).convert("L")
    inv = ImageOps.invert(gray)
    inv_blur = inv.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    g = np.asarray(gray).astype(np.float32)
    b = np.asarray(inv_blur).astype(np.float32) * strength
    denom = np.clip(255.0 - b, 1.0, 255.0)         # avoid divide-by-zero
    dodge = np.clip((g * 255.0) / denom, 0.0, 255.0).astype(np.uint8)

    sketch = Image.fromarray(dodge, mode="L")
    sketch = ImageEnhance.Contrast(sketch).enhance(contrast)

    if output_path.lower().endswith((".jpg", ".jpeg")):
        sketch = sketch.convert("RGB")
    sketch.save(output_path)
    print(f"Processed image saved as '{output_path}'.")

if __name__ == "__main__":
    print("Image Filter (type 'exit' to quit)\n")   # same simple REPL style
    while True:
        image_path = input("Enter image filename (or 'exit' to quit): ").strip()
        if image_path.lower() == "exit":
            print("Goodbye!")
            break
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            continue

        base, ext = os.path.splitext(image_path)
        try:
            if CHOSEN_FILTER == "sketch":
                output_file = f"{base}_sketch{ext}"
                pencil_sketch_filter(image_path, output_file,
                                     blur_radius=7, strength=1.0, contrast=1.15)
            else:
                output_file = f"{base}_blurred{ext}"
                apply_blur_filter(image_path, output_file,
                                  radius=2, size=(128, 128))
        except Exception as e:
            print(f"Error processing image: {e}")