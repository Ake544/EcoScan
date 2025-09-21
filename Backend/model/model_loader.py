# Backend/model/model_loader.py (updated with detailed error handling)
import tensorflow as tf
import numpy as np
import json
import os
import traceback

class EcoScanModel:
    def __init__(self):
        self.model = None
        self.class_labels = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and class labels"""
        try:
            # Load model
            model_path = os.path.join(os.path.dirname(__file__), 'garbage_classifier_final.h5')
            print(f"Loading model from: {model_path}")
            
            # Check if model file exists
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            self.model = tf.keras.models.load_model(model_path)
            print("Model loaded successfully!")
            
            # Load class labels
            labels_path = os.path.join(os.path.dirname(__file__), 'class_labels.json')
            print(f"Loading class labels from: {labels_path}")
            
            # Check if labels file exists
            if not os.path.exists(labels_path):
                raise FileNotFoundError(f"Class labels file not found: {labels_path}")
            
            with open(labels_path, 'r') as f:
                self.class_labels = json.load(f)
                
            print(f"Class labels loaded: {len(self.class_labels)} classes")
            print("Available classes:", self.class_labels)
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Full traceback:")
            traceback.print_exc()
            raise e
    
    def predict_image(self, image_array):
        """Make prediction on an image array"""
        try:
            print(f"Input image shape: {image_array.shape}")
            print(f"Input image dtype: {image_array.dtype}")
            print(f"Input image range: {image_array.min()} to {image_array.max()}")
            
            # Preprocess the image (same as during training)
            # Assuming your model expects (128, 128, 3) images normalized to [0, 1]
            if image_array.max() > 1.0:
                print("Normalizing image from 0-255 to 0-1")
                image_array = image_array / 255.0
            
            # Check if the image has the right shape
            if image_array.shape != (128, 128, 3):
                print(f"Reshaping image from {image_array.shape} to (128, 128, 3)")
                # This shouldn't be necessary if you resized properly, but just in case
                from PIL import Image
                img = Image.fromarray((image_array * 255).astype(np.uint8) if image_array.max() <= 1.0 else image_array.astype(np.uint8))
                img = img.resize((128, 128))
                image_array = np.array(img) / 255.0
            
            # Add batch dimension
            image_batch = np.expand_dims(image_array, axis=0)
            print(f"Final input shape: {image_batch.shape}")
            
            # Make prediction
            print("Making prediction...")
            predictions = self.model.predict(image_batch)
            print(f"Raw predictions: {predictions}")
            
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(np.max(predictions[0]))
            predicted_class = self.class_labels[predicted_class_idx]
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            top_predictions = [
                {"class": self.class_labels[idx], "confidence": float(predictions[0][idx])}
                for idx in top_3_indices
            ]
            
            print(f"Prediction: {predicted_class} with {confidence*100:.2f}% confidence")
            
            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "all_predictions": top_predictions
            }
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            print("Full traceback:")
            traceback.print_exc()
            raise e

# Create a global instance
ecoscan_model = EcoScanModel()