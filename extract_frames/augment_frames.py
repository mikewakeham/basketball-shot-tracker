import os
import cv2
import albumentations as A

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=30, p=0.5),
    A.RandomBrightnessContrast(p=0.4),
    A.HueSaturationValue(p=0.3),
    A.GaussianBlur(p=0.4),
    A.GaussNoise(p=0.5)
])

input_folder = "extract_frames/video1_frames"
output_folder = "extract_frames/video1_augmented_frames"


for filename in os.listdir(input_folder):
    image_path = os.path.join(input_folder, filename)
    image = cv2.imread(image_path)

    augmented = transform(image=image)
    augmented_image = augmented['image']
    output_path = f"{output_folder}/{os.path.splitext(os.path.basename(filename))[0]}_augmented.jpg"
    cv2.imwrite(output_path, augmented_image)