# ShelfReader P1 - Book Detection Scripts

## detect_books.py

**Usage:**
```bash
python scripts/detect_books.py <image_path>
```

**Examples:**
```bash
# From p1-MVP-Desktop directory
python scripts/detect_books.py ../data/test_images/programming-books.jpg

# From Shelfreader root directory
python p1-MVP-Desktop/scripts/detect_books.py data/test_images/programming-books.jpg
```

**What it does:**
- Takes an image path as argument
- Runs OCR detection on the image
- Displays detected book titles with confidence scores
- Shows formatted results with emojis for easy reading

**Features:**
- ✅ Automatic path resolution (works from any directory)
- ✅ Error handling for missing files
- ✅ Beautiful formatted output
- ✅ Confidence scoring
- ✅ Optimized for book spine detection (no preprocessing)