import os
import cv2
import numpy as np
import easyocr
from pythainlp.spell import correct
from googletrans import Translator
import csv

def process_menu_images(image_dir):
    # Initialize EasyOCR reader for Thai language
    reader = easyocr.Reader(['th'])
    
    # Initialize Google Translator
    translator = Translator()
    
    # Initialize an empty list to store the results
    results = []
    
    # Loop through each image file in the directory
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Read the image and crop the borders
            image_path = os.path.join(image_dir, filename)
            image = cv2.imread(image_path)
            h, w = image.shape[:2]
            crop_img = image[int(0.35*h):int(0.95*h), int(0.05*w):int(0.95*w)]
            
            # Perform OCR to extract Thai text
            try:
                thai_text = reader.readtext(crop_img, detail=0, paragraph=True)[0]
            except:
                thai_text = ""
            
            # Check and correct spelling using PyThaiNLP
            try:
                corrected_text = correct(thai_text)
            except:
                corrected_text = ""
            
            # Translate the corrected text to English
            try:
                translated_text = translator.translate(corrected_text, dest='en').text
            except:
                translated_text = ""
            
            # Extract the numeric id from the image filename
            id_num = int(os.path.splitext(filename)[0])
            
            # Append the result to the list
            results.append((id_num, translated_text))
    
    # Sort the results based on the numeric id
    results.sort(key=lambda x: x[0])
    
    # Save the results in a CSV file
    with open("submission.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "menu"])
        writer.writerows(results)
    
    return "Processing completed. Results saved in submission.csv"

# Example usage
image_directory = "./IMG_Data"
process_menu_images(image_directory)