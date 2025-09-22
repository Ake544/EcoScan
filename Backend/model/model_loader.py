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
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'garbage_classifier_final.h5')

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            self.model = tf.keras.models.load_model(model_path)
            
            labels_path = os.path.join(os.path.dirname(__file__), 'class_labels.json')
            
            if not os.path.exists(labels_path):
                raise FileNotFoundError(f"Class labels file not found: {labels_path}")
            
            with open(labels_path, 'r') as f:
                self.class_labels = json.load(f)
            
        except Exception as e:
            traceback.print_exc()
            raise e
    
    def predict_image(self, image_array):
        try:
            if image_array.max() > 1.0:
                image_array = image_array / 255.0
            
            if image_array.shape != (128, 128, 3):
                from PIL import Image
                img = Image.fromarray((image_array * 255).astype(np.uint8) if image_array.max() <= 1.0 else image_array.astype(np.uint8))
                img = img.resize((128, 128))
                image_array = np.array(img) / 255.0

            image_batch = np.expand_dims(image_array, axis=0)
            
            predictions = self.model.predict(image_batch)
            
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(np.max(predictions[0]))
            predicted_class = self.class_labels[predicted_class_idx]
            
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            top_predictions = [
                {"class": self.class_labels[idx], "confidence": float(predictions[0][idx])}
                for idx in top_3_indices
            ]
            
            
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

ecoscan_model = EcoScanModel()