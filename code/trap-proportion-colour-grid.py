
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans

def load_image(path):
    return cv2.imread(str(path))

def show_image(image, title=None):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    if title:
        plt.title(title)
    plt.axis('off')
    plt.show()

def calibrate_yellow_range_from_references(reference_folder):
    hue_values = []

    for ref_path in Path(reference_folder).glob("*.*"):
        image = load_image(ref_path)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        default_lower = np.array([20, 100, 100])
        default_upper = np.array([35, 255, 255])
        mask = cv2.inRange(hsv, default_lower, default_upper)

        yellow_pixels = hsv[mask > 0]
        hue_values.extend(yellow_pixels[:, 0])

    if not hue_values:
        raise ValueError("No yellow pixels found in reference images.")

    h_min = max(min(hue_values) - 2, 0)
    h_max = min(max(hue_values) + 2, 179)
    print(f"✅ Calibrated hue range from references: {h_min:.1f} to {h_max:.1f}")
    return np.array([h_min, 100, 100]), np.array([h_max, 255, 255])

def crop_to_yellow_area(image, yellow_mask):
    kernel = np.ones((20, 20), np.uint8)
    filled_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(filled_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No yellow region found in image.")
    main_contour = max(contours, key=cv2.contourArea)

    epsilon = 0.01 * cv2.arcLength(main_contour, True)
    approx = cv2.approxPolyDP(main_contour, epsilon, True)

    shape_mask = np.zeros_like(yellow_mask)
    cv2.drawContours(shape_mask, [approx], -1, 255, thickness=cv2.FILLED)

    masked_yellow = cv2.bitwise_and(image, image, mask=shape_mask)

    x, y, w, h = cv2.boundingRect(approx)
    margin_w = int(w * 0.05)
    margin_h = int(h * 0.05)
    cx = x + margin_w
    cy = y + margin_h
    cw = w - 2 * margin_w
    ch = h - 2 * margin_h

    cropped_image = masked_yellow[cy:cy+ch, cx:cx+cw]
    cropped_mask = shape_mask[cy:cy+ch, cx:cx+cw]

    return cropped_image, cropped_mask

def calculate_non_yellow_proportion(cropped_image, yellow_mask):
    total_pixels = yellow_mask.size
    yellow_pixels = cv2.countNonZero(yellow_mask)
    non_yellow_pixels = total_pixels - yellow_pixels
    return non_yellow_pixels / total_pixels

def highlight_non_yellow_regions(cropped_image, lower_yellow, upper_yellow):
    cropped_hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
    local_yellow_mask = cv2.inRange(cropped_hsv, lower_yellow, upper_yellow)

    non_yellow_mask = cv2.bitwise_not(local_yellow_mask)

    # Optional: Smooth to remove noise — IMPORTANT this must be applied before highlight & return
    kernel = np.ones((3, 3), np.uint8)
    non_yellow_mask = cv2.morphologyEx(non_yellow_mask, cv2.MORPH_OPEN, kernel)

    # Create green highlight
    highlight_color = np.zeros_like(cropped_image)
    highlight_color[:, :, 1] = 255  # green

    # Apply green to non-yellow areas
    highlighted = np.where(non_yellow_mask[:, :, None] == 255, highlight_color, cropped_image)
    show_image(highlighted, "Highlighted Non-Yellow Content")

    return non_yellow_mask

def process_image(path, lower_yellow, upper_yellow):
    image = load_image(path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    cropped_image, cropped_mask = crop_to_yellow_area(image, yellow_mask)
    non_yellow_ratio = calculate_non_yellow_proportion(cropped_image, cropped_mask)

    non_yellow_mask = highlight_non_yellow_regions(cropped_image, lower_yellow, upper_yellow)

    # Match what was highlighted
    non_yellow_ratio = np.count_nonzero(non_yellow_mask) / non_yellow_mask.size
    print(f"Proportion of cropped yellow region covered by non-yellow content: {non_yellow_ratio:.2%}")



# Run the pipeline

# don't touch
reference_dir = "./photos/reference-clean/"
lower_yellow, upper_yellow = calibrate_yellow_range_from_references(reference_dir)

# modify the path to the image of your choosing

# test 1
target_image = "./photos/test-batch/image3-colour-scale.jpeg"
process_image(target_image, lower_yellow, upper_yellow)

# test 2
target_image = "./photos/test-batch/image4-colour-scale.jpeg"
process_image(target_image, lower_yellow, upper_yellow)

 # test 3
target_image = "./photos/test-batch/image5-colour-scale.jpeg"
process_image(target_image, lower_yellow, upper_yellow)



