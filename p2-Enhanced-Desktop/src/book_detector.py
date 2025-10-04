#!/usr/bin/env python3
"""
Book Detector using YOLOv8 for precise book spine detection
P2-Enhanced-Desktop component
"""

import os
import cv2
import numpy as np
from typing import List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BookDetector:
    """
    YOLOv8-based book detector for precise spine detection.

    This class provides automatic detection of book spines in shelf images
    using YOLOv8 object detection model.
    """

    def __init__(self, model_path: str = "yolov8n.pt", conf_threshold: float = 0.5):
        """
        Initialize the book detector.

        Args:
            model_path: Path to YOLOv8 model weights
            conf_threshold: Confidence threshold for detections (0.0-1.0)
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load YOLOv8 model with error handling for PyTorch 2.6+"""
        try:
            # Import YOLOv8
            from ultralytics import YOLO

            # Try to load model with safe globals for PyTorch 2.6+
            import torch
            with torch.serialization.safe_globals([YOLO]):
                self.model = YOLO(self.model_path)
                logger.info(f"✅ YOLOv8 model loaded from {self.model_path}")

        except Exception as e:
            logger.warning(f"⚠️  Could not load YOLOv8 model: {e}")
            logger.info("🔄 Falling back to alternative detection method")
            self.model = None

    def detect_books(self, image: np.ndarray) -> List[Tuple[int, int, int, int, float]]:
        """
        Detect books in the given image.

        Args:
            image: Input image as numpy array (BGR format)

        Returns:
            List of tuples (x, y, w, h, confidence) for detected books
        """
        if self.model is None:
            logger.warning("No YOLO model available, using fallback detection")
            return self._fallback_detection(image)

        try:
            # Run YOLOv8 inference
            results = self.model(image, conf=self.conf_threshold, verbose=False)

            # Extract bounding boxes
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get box coordinates (x1, y1, x2, y2)
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = box.conf[0].cpu().numpy()

                        # Convert to (x, y, w, h) format
                        x, y = int(x1), int(y1)
                        w, h = int(x2 - x1), int(y2 - y1)

                        detections.append((x, y, w, h, float(conf)))

            # Sort by x-coordinate (left to right)
            detections.sort(key=lambda x: x[0])

            logger.info(f"📚 Detected {len(detections)} books with YOLOv8")
            return detections

        except Exception as e:
            logger.error(f"❌ YOLOv8 detection failed: {e}")
            return self._fallback_detection(image)

    def _fallback_detection(self, image: np.ndarray) -> List[Tuple[int, int, int, int, float]]:
        """
        Fallback detection method when YOLOv8 is not available.

        Uses simple image processing to detect potential book regions.
        This is a basic implementation - not as accurate as YOLOv8.
        """
        logger.info("🔄 Using fallback book detection method")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        height, width = image.shape[:2]

        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)

            # Filter contours that might be books
            # Books are typically vertical rectangles
            if w > h * 0.3 and h > height * 0.1 and w < width * 0.3:
                # Calculate confidence based on rectangle properties
                aspect_ratio = h / w
                size_ratio = (w * h) / (width * height)

                # Simple confidence score
                confidence = min(0.8, aspect_ratio * 0.5 + size_ratio * 2)

                if confidence > 0.3:  # Minimum confidence threshold
                    detections.append((x, y, w, h, confidence))

        # Sort by x-coordinate
        detections.sort(key=lambda x: x[0])

        logger.info(f"📚 Fallback detection found {len(detections)} potential books")
        return detections

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better book detection.

        Args:
            image: Input image

        Returns:
            Preprocessed image
        """
        # Convert to RGB if needed (YOLOv8 expects RGB)
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Assume BGR to RGB conversion
            processed = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            processed = image

        return processed

    def visualize_detections(self, image: np.ndarray, detections: List[Tuple]) -> np.ndarray:
        """
        Draw bounding boxes on image for visualization.

        Args:
            image: Input image
            detections: List of (x, y, w, h, conf) tuples

        Returns:
            Image with bounding boxes drawn
        """
        vis_image = image.copy()

        for i, (x, y, w, h, conf) in enumerate(detections):
            # Draw rectangle
            cv2.rectangle(vis_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw label
            label = f"Book {i+1}: {conf:.2f}"
            cv2.putText(vis_image, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return vis_image


def test_detector():
    """Test function for the book detector"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'p1-MVP-Desktop', 'src'))

    try:
        from PIL import Image
        import numpy as np

        # Create detector
        detector = BookDetector()

        # Try to load a test image
        test_image_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_images', 'bookshelf.jpg')

        if os.path.exists(test_image_path):
            print(f"🔍 Testing with image: {test_image_path}")

            # Load image
            pil_image = Image.open(test_image_path)
            image_array = np.array(pil_image)

            # Detect books
            detections = detector.detect_books(image_array)

            print(f"📚 Found {len(detections)} books")
            for i, (x, y, w, h, conf) in enumerate(detections):
                print(f"  Book {i+1}: pos=({x},{y}) size=({w}x{h}) conf={conf:.2f}")

        else:
            print(f"⚠️  Test image not found: {test_image_path}")
            print("🔄 Testing with synthetic image...")

            # Create synthetic test image
            test_image = np.zeros((600, 800, 3), dtype=np.uint8)
            test_image[:, :] = [200, 200, 200]  # Light gray background

            # Add some fake book rectangles
            cv2.rectangle(test_image, (50, 100), (120, 500), (139, 69, 19), -1)   # Brown book
            cv2.rectangle(test_image, (150, 80), (220, 520), (25, 25, 112), -1)   # Dark blue book
            cv2.rectangle(test_image, (250, 120), (320, 480), (34, 139, 34), -1)  # Green book

            detections = detector.detect_books(test_image)
            print(f"📚 Found {len(detections)} books in synthetic image")

    except ImportError as e:
        print(f"⚠️  Could not import test dependencies: {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    print("🧪 Testing BookDetector...")
    test_detector()