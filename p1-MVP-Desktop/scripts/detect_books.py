#!/usr/bin/env python3
"""
ShelfReader P1 - Book Detection Script
Usage: python detect_books.py <image_path>
"""

import sys
import os
from pathlib import Path

# Add src directory to path so we can import our modules
script_dir = Path(__file__).parent
src_dir = script_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from ocr_processor import BookOCR
from PIL import Image

def main():
    if len(sys.argv) != 2:
        print("Usage: python detect_books.py <image_path>")
        print("Example: python detect_books.py ../../data/test_images/programming-books.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        sys.exit(1)

    try:
        # Initialize OCR processor
        print("🔍 Initializing OCR processor...")
        processor = BookOCR(['en'], 0.2)  # English, confidence threshold 0.2

        # Load image
        print(f"📖 Loading image: {image_path}")
        pil_image = Image.open(image_path)

        # Process the image (without preprocessing for best results)
        print("⚡ Running OCR detection...")
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)
        boxes = processor.get_boxes(pil_image, preprocess=False)

        # Display results
        print("\n" + "="*50)
        print("📚 SHELFREADER P1 - BOOK DETECTION RESULTS")
        print("="*50)
        print(f"🖼️  Image: {os.path.basename(image_path)}")
        print(f"📊 Books detected: {len(boxes)}")
        print(f"🎯 Confidence: {confidence:.2f}")
        print(f"📝 Combined text: {text[:100]}{'...' if len(text) > 100 else ''}")

        if boxes:
            print("\n📖 Detected book titles:")
            print("-" * 30)
            for i, box in enumerate(boxes, 1):
                title = box['text'].strip()
                if title:  # Only show non-empty titles
                    print(f"{i:2d}. {title}")
        else:
            print("\n❌ No books detected in this image.")

        print("\n✅ Detection complete!")

    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()