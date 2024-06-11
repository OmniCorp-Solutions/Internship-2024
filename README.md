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
- [ ] documentation on methods used, process flow, and input/output black box description of functionality
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

Server AI-derived code found in serverAI.txt.

## Software Outline

This section focuses on the software itself: wht it does, how it does it, and and overview of how each module interacts with one another when being run.

### Methods

### Inputs/Outputs

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