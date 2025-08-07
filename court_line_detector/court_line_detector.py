import torch
import torchvision.transforms as transforms
import torchvision.models as models
import numpy as np
import cv2

class CourtLineDetector:
    def __init__(self, model_path):
        self.model = models.resnet50(pretrained=False)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 14*2)
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()

        # Exactly match training transforms
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, frame, debug=True):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        original_h, original_w = frame_rgb.shape[:2]
        
        frame_tensor = self.transform(frame_rgb).unsqueeze(0)

        with torch.no_grad():
            output = self.model(frame_tensor)

        # Get keypoints in 224x224 space (because that's what model was trained on)
        keypoints = output.squeeze().cpu().numpy()
        
        if debug:
            print("Original image size:", original_w, original_h)
            print("Raw model output (224x224 space):")
            for i in range(0, min(6, len(keypoints)), 2):
                print(f"Point {i//2}: ({keypoints[i]:.1f}, {keypoints[i+1]:.1f})")

        # Training did: keypoints *= 224.0/w
        # So scale back with: keypoints *= w/224.0
        w_scale = original_w / 224.0
        h_scale = original_h / 224.0
        
        keypoints[::2] *= w_scale
        keypoints[1::2] *= h_scale

        if debug:
            print("\nAfter scaling to original dimensions:")
            for i in range(0, min(6, len(keypoints)), 2):
                print(f"Point {i//2}: ({keypoints[i]:.1f}, {keypoints[i+1]:.1f})")

        return keypoints
    
    def draw_keypoints(self, frame, keypoints):
        frame_copy = frame.copy()
        for i in range(0, len(keypoints), 2):
            x, y = int(keypoints[i]), int(keypoints[i+1])
            
            if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                cv2.circle(frame_copy, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(frame_copy, f"{i//2}", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame_copy
    
    def draw_keypoints_on_video(self, video_frames, keypoints):
        return [self.draw_keypoints(frame, keypoints) for frame in video_frames]