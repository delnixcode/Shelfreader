class BookOCR:
    def __init__(self, languages, confidence_threshold):
        # Initialiser easyocr.Reader avec les langues
        # Stocker le seuil de confiance
    
    def preprocess_image(self,image):
        # Convertir en gris : cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Égaliser histogramme : cv2.equalizeHist(gray)
        # Retourner l'image traitée

    def extract_text_from_pil(self, pil_image, preprocess=True):
        # Convertir PIL → numpy array : np.array(pil_image)
        # Convertir RGB → BGR : cv2.cvtColor(..., cv2.COLOR_RGB2BGR)
        # Appliquer preprocess si demandé
        # Appeler self.reader.readtext(image)
        # Filtrer par confidence_threshold
        # Combiner tous les textes détectés
        # Retourner (texte_complet, confiance_moyenne)