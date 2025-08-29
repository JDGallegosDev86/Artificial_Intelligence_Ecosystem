# AI Image Processing and Classification Project

This project is designed to give you hands-on experience working with an image classifier and enhancing your programming skills using AI assistance. The project has two parts, each focused on different aspects of image classification and processing. By the end, you'll have explored fundamental concepts like Grad-CAM, image classification, and creative image filtering.

If you’re newer to Python
“The explanation made sense. I learned why models expect a fixed input size (224×224), why we call preprocess_input (model-specific normalization), and why np.expand_dims is needed (Keras batches). I also understand how decode_predictions turns raw scores into readable labels. The try/except and simple REPL loop were easy to follow.”

Top-3 Predictions for TokyoGhoul1.jpg
  1: parachute (0.42)
  2: comic_book (0.29)
  3: balloon (0.16)

Heatmap observations (Grad-CAM on top class)

Strongest activations: around the large curved outline above/around the head (hood/hair arc) and the round head region. These high-contrast, curved shapes look like a canopy/balloon to MobileNetV2 and line up with the parachute/balloon guesses.

Moderate activations: sharp inked edges (jawline, hair spikes, cape edges). This fits the comic_book prediction since the network keys on bold contours typical of printed art.

Weak/low activations: flat background areas and most of the lower torso/clothing—regions with little texture/contrast contribute less to the decision.

Interpretation: The model is relying on global rounded contours + strong outlines, not semantic understanding of an anime character. That bias explains the misclassifications (parachute, balloon) and why comic_book appears in the top-3.

One-paragraph takeaway

“Grad-CAM highlights curved, high-contrast regions around the character’s head/hood and main outlines, with minimal attention on background or low-texture areas. The heatmap shows the classifier is keying on shape cues (rounded canopy-like arcs and bold comic edges) rather than true object semantics, which likely drove the parachute and balloon predictions and supports comic_book as a style cue.”

Enter image filename (or 'exit' to quit): TokyoGhoul1.jpg 
Processed image saved as 'TokyoGhoul1_blurred.jpg'.

If you’re new to Python

The explanations were clear and matched what I saw in the code.

I now understand why we resize before processing (makes the demo fast/consistent) and why GaussianBlur(radius=2) softens edges.

The reason to call plt.axis('off') before saving (remove axes/frames) also made sense.

The try/except block helped me see how errors (bad path, corrupt image) are handled without crashing.

One subtle point I learned: using Matplotlib’s savefig saves the figure, which isn’t guaranteed to be the same pixel size as the image array (DPI/figure-size can change the saved resolution).

Observations about how the blur is implemented

Pipeline: open → resize to 128×128 → GaussianBlur(radius=2) → imshow → savefig (figure-based save).

Downscale first: This pre-smooths the image (resampling removes high frequencies) and changes the blur’s apparent strength compared to blurring at the original resolution.

Blur specifics: GaussianBlur(radius=2) applies an isotropic Gaussian; larger radius → stronger edge/texture suppression and larger halos around high-contrast lines.

Resizing quality: Without an explicit resample (e.g., Image.LANCZOS), the default can be coarse; fine detail may alias or stair-step before blurring.

Saved output resolution: Because saving uses Matplotlib, the final file size in pixels depends on the figure size × DPI, not necessarily 128×128. You may get a differently sized PNG that contains your 128×128 image scaled to the canvas.

Filename handling: Output is derived as <base>_blurred<ext> so the original is preserved. Errors are handled gracefully with try/except.

