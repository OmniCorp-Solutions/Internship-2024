#credit to SHORYA22 on Kaggle for code to be restructured into this class
#can be found here: https://www.kaggle.com/code/shorya22/hollywood-celebrity-facial-recognition/notebook

#credit to Kyle Stratis at Real Python for additional code for encoding and training
#can be found here: https://realpython.com/face-recognition-with-python/#step-5-validate-your-model

#data folder directory
#data_directory can be found at '../data/training'

import numpy as np
import pandas as pd
import os
import glob
from io import BytesIO
import matplotlib.pyplot as plt
from pathlib import Path
import face_recognition
import pickle
from collections import Counter
from PIL import Image, ImageDraw
import base64

# Class DataImport()
# The purpose of this class is to load training data into memory, encode images,
# and display results for testing. Different datasets can be loaded into memory by
# changing data_directory

class DataImport:
    def __init__(self, data_directory: str = "../data/training"):
        self.images_path = glob.glob(data_directory + '/**/*.jpg', recursive = True, root_dir = data_directory) #grab all of the 1700 images
        self.labels = self.label_data()
        self.image_labels = np.array(self.labels)
        self.data_directory = data_directory

    def label_data(self):
        #First establish the labels for the pictures
        labels = []
        for image in self.images_path:
            lab = os.path.dirname(image)
            labels.append(lab)

        #next, label each image using the labels set aside prior 
        image_labels = []
        for lbl in labels:
            lab = lbl.split('\\')[-1]
            image_labels.append(lab)

        return image_labels

    def encode_images(self, model: str = "hog", encodings_location: Path = Path("../data/Outputs/encodings.pkl")) -> None:
        names = []
        encodings = []
        for filepath in Path(self.data_directory).glob("*/*"):
            #Grab the folder name (person name) and load the image file
            name = filepath.parent.name
            image = face_recognition.load_image_file(filepath)

            #Place list of locations of images into encoding method, and place in seperate list
            face_locations = face_recognition.face_locations(image, model = model)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            #append each encoding into names and encodings local list so face_encodings can be reassigned
            for encoding in face_encodings:
                names.append(name)
                encodings.append(encoding)

        #Place lists in dictionary to dump into output file
        name_encodings = {"names": names, "encodings": encodings}
        with encodings_location.open(mode = "wb") as f:
            pickle.dump(name_encodings, f)

    def recognize_faces(self, image_unprocessed: str, encoded: bool = False, model: str = "hog", encodings_location: Path = Path("../data/Outputs/encodings.pkl")) -> None:
        #This method is to recognize unlabelled faces in an image location
        with encodings_location.open(mode = "rb") as f:
            loaded_encodings = pickle.load(f)

        #load the input image to be identified,
        #if encoded is False, image_unprocessed should
        #be a file path, otherwise it should be a Base64
        #encoded string
        if (encoded == False):
            input_image = face_recognition.load_image_file(image_unprocessed)
        else:
            image_decoded = base64.b64decode(image_unprocessed)
            image = Image.open(BytesIO(image_decoded))
            input_image = np.array(image)
        
        #Use the model in order to identify faces on the input image
        input_face_locations = face_recognition.face_locations(input_image, model = model)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

        #draw the image with faces
        pillow_image = Image.fromarray(input_image)
        draw = ImageDraw.Draw(pillow_image)

        #Recognize faces on the image, if not found set to "unknown"
        for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
            name = _recognize_face(unknown_encoding, loaded_encodings)
            if not name:
                name = "Unknown"
            #print(name, bounding_box)
            #Removed print for pillow observations
            _display_face(draw, bounding_box, name)

        #remove the draw object and display
        del draw
        pillow_image.show()

        #convert to base64
        buffered = io.BytesIO()
        pillow_image.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_processed = base64.b64encode(img_bytes).decode('utf-8')

        return img_processed


def _recognize_face(unknown_encoding, loaded_encodings):
    #This helper function recognizes faces in an image
    #compare the encodings of the unknown and loaded
    boolean_matches = face_recognition.compare_faces(loaded_encodings["encodings"], unknown_encoding)

    #Keep track of each possible match, and push the name with the highest votes/True values
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def _display_face(draw, bounding_box, name, color: str = "blue", text_color: str = "white"):
    #This helper function draws squares around recognized faces
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline = color)
    text_left, text_top, text_right, text_bottom = draw.textbbox((left, bottom), name)

    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill = color,
        outline = color,
    )
    draw.text(
        (text_left, text_top),
        name,
        fill = text_color,
    )
