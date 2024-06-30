# Internship-2024


# This repo will serve as the project layout for Internship 2024

# Goal: Produce a ML algorithm (DNN, CNN, LLM, etc) from scratch containing all the neccesary different components, and documenting the entire process, links, and startups.

## Current - Facial Recognition using ML

Implement a generic ML algorithm that can infer from any vector dataset added to it, and use alignment models as necessary on the output to perform facial recognition.

Start with this [tutorial](https://realpython.com/face-recognition-with-python/) for facial recognition.


Changes needed:
- [x] create a simple http digest server to intake the photo in a json put/post and return a json object with the data recognition returned
- [ ] detector needs to use either proper object oriented pass by reference, or use python pass by dict method (each call, and/or pass by reference needs to be clear so as know which data is being used)
- [x] documentation of how much was manually scripted vs ai generated
- [x] requirements.txt or setup.py
- [x] documentation on methods used, process flow, and input/output black box description of functionality
- [x] documentation on the license for the model (what would be best to forward computer science, a company, or personal use...), the data, and the result
- [x] what license is the source code roots, and/or branches used?
- [ ] theoretical use cases each of the above categories taking all the considerations into account
- [ ] is this the best solution, what could be better, what is missing?
- [ ] stream line the execution of the workflow using a single command

## AI Assistance

This section is dedicated to outlining the use of LLM in the writing of code for this project and to what extent each module was developed using AI through chatlog outputs. All code has since been modified and licensed.

### Client

Client development chat log with ChatGPT found [here](https://chatgpt.com/share/daa07414-3c79-479b-9ba3-eba416780782).

### Base 64 Encoding Detector

Base 64 conversion chat log with ChatGPT found [here](https://chatgpt.com/share/699b3c44-75a6-4599-ae44-6e24acf0a2a9).

### Server

Server AI-derived code found in serverAI.py.

## Software Outline

This section focuses on the software itself: wht it does, how it does it, and and overview of how each module interacts with one another when being run.

### Methods

#### detector.py:

**Class: DataImport(string data_directory)**
On initialization, this class will grab all images from training directory in order to apply labels to the entire dataset, calling its method label_data().

- **label_data(self):** 
labels the images of all training images for class DataImport with the name of the associated actor. Directory must be in format ../data/training/actor_name/image_name.

- **encode_images(self, model: str = "hog", encodings_location: Path = Path("../data/Outputs/encodings.pkl")) -> None:** 
Creates an encoding of the image training set using the model set out in "model" (default HOG). encodings_location can be changed to the desired location of the encodings file.

- **recognize_faces(self,  image_unprocessed: str, encoded: bool = False, model: str = "hog", encodings_location: Path = Path("../data/Outputs/encodings.pkl")) -> None:** 
This method is used to recognize faces in unknown datasets based on the previous training data. The value image_unprocessed is a string that either contains an image file location or the base64 string of characters representing an image. The latter must be indicated by changing encoded to True in order to accept a base64 string. model is used in order to determine what form of facial recognition is used on the image, which must be reflective of the encodings created by the method encode_images(). Likewise, encodings_location must be to a file which contains encodings created by encode_images(). Returns a base64 string containing the image with bounding boxes over the faces detected.

- **Function: _recognize_face(unknown_encoding, loaded_encodings)** 
This function serves to compare two encodings and return the highest probable matching name for the unknown encoding using a counter of highest matches with the loaded_encodings, which are the encodings created by encode_images(). Serves to assist in recognize_faces().

- **Function: _display_face(draw, bounding_box, name, color: str = "blue", text_color: str = "white"):**
This function is used to draw a bounding box around any detected faces in an image as well as the predicted name that the face belongs to. The value draw holds an ImageDraw object, being the base image, while bounding_box holds location data relevant to the bounding box corners. Name contains the associated predicted name of the detected face as a string, while color and text_color are used for changing the aesthetics of the bounding box.

#### simple_server.py

- **Function: authenticator(keys):**
This function is used to check if an authentication key matches with the pickle database to allow connection to the server. Can be modified to change authentication steps. The value keys is the value being compared against the database.

- **Class: SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):**
This class is used to run the server and call all methods associated with the server object.

- **_set_response(self, status=200, content_type='application/json'):**
This method is used to set the response to a client and send back information related to the response using HTTP response codes (status). By default, the connection is accepted with a code 200 and uses a JSON object for data transfer.

- **do_POST(self):**
This method is used to intercept information from the client and decide whether to process the information or not. Checks the content type using a try block while also checking authentication keys before calling process_image() in order to deliver a response back to the client. If authenticator fails, a matching error message will be delivered, while if the try block fails, a message using error code 400 eill be returned. If the method is run while self.path is not equal to '/', then an error 404 will be returned to the client instead.

- **process_image(self, image):**
This method is used to send a base64 string, image, through to the DataImport() class in order to recognize any faces in the image, and returns a base64 string, processed_image, in order to be sent back in a JSON object to the client.

#### simple_client.py

- **Function: encode_image(image_path):**

- **Function: send_image(url, key, image_path, output_path):**

### Process Flow



### Use Cases



## Conclusion



## Licensing

This section outlines the licenses used by the various portions of this project and their applications.

### Code

The source code is licensed under [GNU General Public License v3](https://spdx.org/licenses/GPL-3.0-only#:~:text=The%20GNU%20General%20Public%20License,share%20and%20change%20the%20works.) as an open-source project. The model library used, [face_recognition.py](https://pypi.org/project/face-recognition/), and all models created, are licensed under [MIT license](https://choosealicense.com/licenses/mit/).

### Dataset

The hollywood actor dataset uses [CC0 1.0 Universal license: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) as outlined by the kaggle webpage hosting the images found [here](https://www.kaggle.com/datasets/bhaveshmittal/celebrity-face-recognition-dataset). All additional images used to train, validate, and test the code are also licensed under CC0.

### Results

All included output images of the source code are licensed under [CC0 1.0 Universal license: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/). 