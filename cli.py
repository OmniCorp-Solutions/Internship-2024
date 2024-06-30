import argparse
import pickle
from collections import Counter
from pathlib import Path
import face_recognition
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import random
import os
from src import simple_client, simple_server

PARENT_DIR = Path("data")
DEFAULT_ENCODINGS_PATH = Path(f"{PARENT_DIR}/Outputs/encodings.pkl")
BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"
NOT_FOUND = 0

# Create directories if they don't already exist
Path(f"{PARENT_DIR}/Training").mkdir(exist_ok=True)
Path(f"{PARENT_DIR}/Outputs").mkdir(exist_ok=True)
Path(f"{PARENT_DIR}/Validation").mkdir(exist_ok=True)

parser = argparse.ArgumentParser(description="Recognize faces in an image")
parser.add_argument("--train", action="store_true", help="Train on input data")
parser.add_argument("--validate", action="store_true", help="Validate trained model")
parser.add_argument("--test", action="store_true", help="Test the model with an unknown image")
parser.add_argument(
    "-m",
    action="store",
    default="hog",
    choices=["hog", "cnn"],
    help="Which model to use for training: hog (CPU), cnn (GPU)",
)
parser.add_argument("-f", action="store", help="Path to an image with an unknown face")
parser.add_argument("--addKey", action="store_true", help="Add key to server database")
parser.add_argument("--removeKey", action="store_true", help="Remove key to server database")
parser.add_argument("--printKey", action="store_true", help="Print keys to server database")
parser.add_argument("--server", action="store_true", help="Startup the facial recoginition server locally at :8080/api/facial_input")
parser.add_argument("--client", action="store_true", help="Run a client side program to test server recognition")
args = parser.parse_args()


def encode_known_faces(model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH) -> None:
    """
    Loads images in the training directory and builds a dictionary of their
    names and encodings.
    """
    names = []
    encodings = []

    for filepath in Path(f"{PARENT_DIR}/Training").glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)


def recognize_faces(
    image_location: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    Given an unknown image, get the locations and encodings of any faces and
    compares them against the known encodings to find potential matches.
    """
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)

    input_face_locations = face_recognition.face_locations(input_image, model=model)
    input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)

    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
            NOT_FOUND += 1
            print(f"Not found: {NOT_FOUND}          ", end="\n\r")
        else:
            print(f"Name: {name}          ", end="\r")
            _display_face(draw, bounding_box, name)

    del draw
    plt.imshow(np.asarray(pillow_image))
    plt.pause(1)


def _recognize_face(unknown_encoding, loaded_encodings):
    """
    Given an unknown encoding and all known encodings, find the known
    encoding with the most matches.
    """
    boolean_matches = face_recognition.compare_faces(loaded_encodings["encodings"], unknown_encoding)
    votes = Counter(name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match)
    if votes:
        return votes.most_common(1)[0][0]


def _display_face(draw, bounding_box, name):
    """
    Draws bounding boxes around faces, a caption area, and text captions.
    """
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox((left, bottom), name)
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill=BOUNDING_BOX_COLOR,
        outline=BOUNDING_BOX_COLOR,
    )
    draw.text(
        (text_left, text_top),
        name,
        fill=TEXT_COLOR,
    )


def validate(model: str = "hog"):
    """
    Runs recognize_faces on a set of images with known faces to validate
    known encodings.
    """
    files = []
    for filepath in Path(f"{PARENT_DIR}/Validation").rglob("*/*"):
        if filepath.is_file():
            files.append(filepath)

    random.shuffle(files)
    for filepath in files:
        recognize_faces(image_location=str(filepath.absolute()), model=model)


def addKey(newKey: str = ""):
    if newKey != "":
        if os.path.isfile("src/keys_db.pkl"):
            with open("src/keys_db.pkl", "rb") as f:
                keys_db = pickle.load(f)

            keys_db.update({**keys_db, **{newKey: True}})
        else:
            keys_db = {newKey: True}

        # Save the keys to a pickle file
        with open("src/keys_db.pkl", "wb") as f:
            pickle.dump(keys_db, f)

        print(f"Added the new key: {newKey}. Thank you")


def removeKey(key_string: str = ""):
    if key_string != "" and os.path.isfile("src/keys_db.pkl"):
        with open("src/keys_db.pkl", "rb") as f:
            keys_db = pickle.load(f)

        try:
            del keys_db[key_string]

            # Save the keys to a pickle file
            with open("keys_db.pkl", "wb") as f:
                pickle.dump(keys_db, f)

            print(f"Removed the key: {key_string}. Thank you")
        except:
            pass


def printKeys():  # s$8cyGN7KHjEU@DyTY7s4^NwNhp&e
    if os.path.isfile("src/keys_db.pkl"):
        with open("src/keys_db.pkl", "rb") as f:
            keys_db = pickle.load(f)

        for key, value in keys_db.items():
            print(key)
    else:
        print("No keys added yet")


def runServer():
    simple_server.start()


def runClient():
    simple_client.getData(image_path="data/Validation/Johnny Depp/086_f052c533.jpg", output_path="data/Outputs/client_return.png", key=input("Input API Key: "))


if __name__ == "__main__":
    if args.train:
        encode_known_faces(model=args.m)
    elif args.validate:
        validate(model=args.m)
    elif args.test:
        recognize_faces(image_location=args.f, model=args.m)
    elif args.addKey:
        addKey(input("Please input your new server authentication key: "))
    elif args.removeKey:
        removeKey(input("Please input key to remove: "))
    elif args.printKey:
        printKeys()
    elif args.server:
        runServer()
    elif args.client:
        runClient()
