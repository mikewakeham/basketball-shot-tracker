import os
import cv2
import json
from ultralytics import YOLO
from pycocotools import mask as mask_utils

# Load the YOLOv8 model
model = YOLO('yolov8')


# Define the input and output directories
input_dir = 'extract_frames/video1_augmented_frames'
output_dir = 'output_annotations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize COCO format data structure
coco_output = {
    "info": {
        "description": "Auto-labeled Dataset",
        "version": "1.0",
        "year": 2024,
        "contributor": "",
        "date_created": ""
    },
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": []
}

# Define category mappings (assuming your model detects specific categories)
category_mapping = {0: "backboard", 1: "ball", 2: "ball in hand", 3: "ball in net", 4: "net"}  # Add any additional classes detected
category_id_mapping = {name: idx + 1 for idx, name in enumerate(category_mapping.values())}

# Add categories to coco_output
for category_name, category_id in category_id_mapping.items():
    coco_output["categories"].append({
        "id": category_id,
        "name": category_name,
        "supercategory": "object"
    })

annotation_id = 1

# Function to run inference and save annotations in COCO format
def auto_label_images(input_dir, output_dir):
    global annotation_id
    image_id = 1
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Could not read image {image_path}")
                continue

            # Get image dimensions
            height, width, _ = image.shape

            # Add image info to COCO dataset
            coco_output["images"].append({
                "id": image_id,
                "file_name": filename,
                "height": height,
                "width": width
            })

            # Run inference
            results = model.predict(source=image, save=False, conf=0.25)

            # Parse results
            for result in results:
                for box in result.boxes:
                    x_min, y_min, x_max, y_max = box.xyxy[0].tolist()  # Convert to list
                    class_id = int(box.cls[0].item())  # Convert to integer
                    if class_id in category_mapping:
                        category_id = category_id_mapping[category_mapping[class_id]]
                    else:
                        print(f"Unknown class ID: {class_id}")
                        continue  # Skip unknown classes

                    bbox_width = x_max - x_min
                    bbox_height = y_max - y_min
                    bbox = [x_min, y_min, bbox_width, bbox_height]

                    # Add annotation to COCO dataset
                    coco_output["annotations"].append({
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": bbox,
                        "area": bbox_width * bbox_height,
                        "iscrowd": 0,
                        "segmentation": []
                    })
                    annotation_id += 1

            print(f"Processed {filename}")
            image_id += 1

    # Save COCO annotations to file
    with open(os.path.join(output_dir, "annotations.json"), 'w') as f:
        json.dump(coco_output, f, indent=4)

# Auto-label images
auto_label_images(input_dir, output_dir)
