
import sys
print(sys.prefix)

import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(path):
    return cv2.imread(path)

def show_image(image, title=None):
    """
    Displays a BGR image using matplotlib by converting it to RGB.

    Args:
        image: The image loaded with OpenCV (i.e., in BGR format).
        title: Optional title for the image.
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    if title:
        plt.title(title)
    plt.axis('off')
    plt.show()

def get_yellow_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    return cv2.inRange(hsv, lower_yellow, upper_yellow)

def crop_to_yellow_area(image, yellow_mask):
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No yellow region found in image.")
    
    x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
    return image[y:y+h, x:x+w], yellow_mask[y:y+h, x:x+w]

def calculate_non_yellow_proportion(cropped_image, yellow_mask):
    total_pixels = yellow_mask.size
    yellow_pixels = cv2.countNonZero(yellow_mask)
    non_yellow_pixels = total_pixels - yellow_pixels
    return non_yellow_pixels / total_pixels

def process_image(path):
    image = load_image(path)
    yellow_mask = get_yellow_mask(image)
    cropped_image, cropped_mask = crop_to_yellow_area(image, yellow_mask)
    non_yellow_ratio = calculate_non_yellow_proportion(cropped_image, cropped_mask)
    print(f"Proportion of cropped yellow region covered by non-yellow content: {non_yellow_ratio:.2%}")

# Example usage:
process_image("./photos/test-batch/IMG_5449.jpg")

# Test the individual steps

## 1. load the image
path = "./photos/test-batch/IMG_5449.jpg"
image = load_image(path)

# check the image
show_image(image, title = "Raw image")

## 2. get yellow mask
yellow_mask = get_yellow_mask(image)

# check the image
show_image(yellow_mask, title = "Yellow mask image")

## 3. get cropped image and cropped mask
cropped_image, cropped_mask = crop_to_yellow_area(image, yellow_mask)

# show the images
show_image(cropped_image)
show_image(cropped_mask)

## 4. calculate the ratio
non_yellow_ratio = calculate_non_yellow_proportion(cropped_image, cropped_mask)

# print the answer
print(f"Proportion of cropped yellow region covered by non-yellow content: {non_yellow_ratio:.2%}")



