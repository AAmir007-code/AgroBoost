import os
import torch
import cv2
import numpy as np
from torch.utils.data import Dataset, DataLoader
from segment_anything import sam_model_registry, SamPredictor
from torchvision import transforms
import torch.optim as optim
import torch.nn as nn

class CustomDataset(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.images = os.listdir(image_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_name = os.path.join(self.image_dir, self.images[idx])
        mask_name = os.path.join(self.mask_dir, self.images[idx].replace('.jpg', '_mask.png'))
        image = cv2.imread(img_name)
        mask = cv2.imread(mask_name, cv2.IMREAD_GRAYSCALE)

        if self.transform:
            image = self.transform(image)

        return image, mask

def train_model(model, dataloader, criterion, optimizer, num_epochs=10):
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for images, masks in dataloader:
            images, masks = images.to(device), masks.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        epoch_loss = running_loss / len(dataloader)
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {epoch_loss:.4f}')

def main():
    image_dir = "dataset/images"
    mask_dir = "dataset/masks"
    
    # Model and training parameters
    model_type = "vit_h"
    batch_size = 8
    num_epochs = 10
    learning_rate = 1e-4

    # Transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Dataset and DataLoader
    dataset = CustomDataset(image_dir, mask_dir, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Load SAM model
    sam_checkpoint = os.path.join("models", f"sam_{model_type}.pth")
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    model = SamPredictor(sam).to(device)

    # Loss and optimizer
    criterion = nn.BCEWithLogitsLoss()  # or any other loss suitable for segmentation
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    train_model(model, dataloader, criterion, optimizer, num_epochs)

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    main()