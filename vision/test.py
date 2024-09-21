import cv2
import torch
import os
from segment_anything import SamPredictor, sam_model_registry
import numpy as np

# Load the SAM model
def load_model(model_type="vit_h"):
    model_path = os.path.join("models", f"sam_{model_type}.pth")
    sam = sam_model_registry[model_type](checkpoint=model_path)
    sam_predictor = SamPredictor(sam)
    return sam_predictor

# Process each frame of the video and perform tree segmentation
def segment_trees_in_video(video_path, output_path, model_type="vit_h"):
    # Load the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Initialize video writer for output
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Load the SAM predictor
    predictor = load_model(model_type)

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to a format suitable for SAM (RGB and normalize)
        input_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_frame = input_frame.astype(np.float32) / 255.0

        # Predict the segmentation for the frame (Use a dummy prompt, you may fine-tune this later)
        predictor.set_image(input_frame)
        boxes = np.array([[50, 50, frame_width - 50, frame_height - 50]])  # Example of a bounding box
        masks, _, _ = predictor.predict(boxes=boxes, multimask_output=False)

        # Overlay the mask on the original frame
        mask = masks[0]
        mask_rgb = np.zeros_like(frame)
        mask_rgb[:, :, 1] = mask * 255  # Green mask
        overlaid_frame = cv2.addWeighted(frame, 1, mask_rgb, 0.6, 0)

        # Write the processed frame to the output video
        out.write(overlaid_frame)

        frame_num += 1
        print(f"Processed frame {frame_num}")

    cap.release()
    out.release()
    print(f"Tree segmentation completed and saved to {output_path}")

if __name__ == "__main__":
    video_path = "./videos/0012.MP4"  
    output_path = "output/res_0012.mp4"
    segment_trees_in_video(video_path, output_path)