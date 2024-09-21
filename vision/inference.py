import os
import cv2
import torch
import numpy as np
from segment_anything import SamPredictor, sam_model_registry

def load_sam_model(model_type="vit_h"):
    model_path = os.path.join("models", f"sam_{model_type}.pth")
    sam = sam_model_registry[model_type](checkpoint=model_path)
    return SamPredictor(sam)

def segment_frame(predictor, frame, bbox):
    input_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    predictor.set_image(input_frame)
    masks, _, _ = predictor.predict(boxes=np.array([bbox]), multimask_output=False)
    return masks[0]

def overlay_mask(frame, mask, color=(0, 255, 0), alpha=0.6):
    mask_rgb = np.zeros_like(frame)
    mask_rgb[:, :, 1] = mask * 255
    return cv2.addWeighted(frame, 1, mask_rgb, alpha, 0)

def process_video(input_video, output_video, model_type="vit_h", bbox=(50, 50, 600, 400)):
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened(): raise IOError("Error opening video file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    predictor = load_sam_model(model_type)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        mask = segment_frame(predictor, frame, bbox)
        out.write(overlay_mask(frame, mask))
    
    cap.release()
    out.release()

if __name__ == "__main__":
    input_video = "./videos/0012.MP4"  
    output_video = "output/res_0012.mp4"
    bbox = (50, 50, 600, 400)  # Modify as needed
    process_video(input_video, output_video, bbox=bbox)