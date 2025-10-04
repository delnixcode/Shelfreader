#!/usr/bin/env python3
"""
Test script for YOLOv8 integration in P2-Enhanced-Desktop
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_yolo_import():
    """Test YOLOv8 import and basic functionality"""
    try:
        from ultralytics import YOLO
        print("✅ YOLOv8 import successful")

        # Try to create model without loading weights first
        print("🔄 Testing YOLO model creation...")
        model = YOLO()  # Create empty model
        print("✅ YOLO model creation successful")

        return True
    except Exception as e:
        print(f"❌ YOLOv8 test failed: {e}")
        return False

def test_dependencies():
    """Test other key dependencies"""
    try:
        import cv2
        import numpy as np
        import torch
        import redis
        import psutil

        print("✅ All dependencies imported successfully")
        print(f"   - OpenCV: {cv2.__version__}")
        print(f"   - NumPy: {np.__version__}")
        print(f"   - PyTorch: {torch.__version__}")
        print(f"   - Redis: {redis.__version__}")
        print(f"   - psutil: {psutil.__version__}")

        return True
    except Exception as e:
        print(f"❌ Dependencies test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing P2-Enhanced-Desktop dependencies...")
    print("=" * 50)

    deps_ok = test_dependencies()
    yolo_ok = test_yolo_import()

    print("=" * 50)
    if deps_ok and yolo_ok:
        print("🎉 All tests passed! Ready for P2 development.")
    else:
        print("⚠️  Some tests failed. Check dependencies.")