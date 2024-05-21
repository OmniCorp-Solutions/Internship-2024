#credit to SHORYA22 on Kaggle for code to be restructured into this class
#can be found here: https://www.kaggle.com/code/shorya22/hollywood-celebrity-facial-recognition/notebook 

#data folder directory
#data_directory can be found at '../data/training' or '../data/validation'

import numpy as np
import pandas as pd
import os
import glob
import cv2
import matplotlib.pyplot as plt

class DataImport:
    def __init__(self, data_directory):
        self.images_path = glob.glob(data_directory + '/**/*.jpg', recursive = True, root_dir = data_directory) #grab all of the 1700 images
        self.labels = self.label_data()
        self.image_array = self.import_images()
        self.image_labels = np.array(self.labels)


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

    def import_images(self):
        images = []

        #resize image to 128 x 128 and gather image information 
        for file in self.images_path:
            img = cv2.imread(file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (128, 128))
            img = img / 255

            images.append(img)

        image_array = np.array(images)
        return image_array

    def reveal_imagelabels(self, repetition):
        #method for randomly showing images in the dataset for observation
        plt.figure(figsize = (8, 8))
        random_indices = np.random.choice(len(self.image_array), size = repetition, replace = False) #choose multiple random indices without replacement

        for i, index in enumerate(random_indices):
            plt.subplot(3, 4, i+1)
            plt.imshow(self.image_array[index], cmap = 'gray')
            plt.title(self.labels[index])
            plt.axis('off')

        plt.tight_layout()
        plt.show()
