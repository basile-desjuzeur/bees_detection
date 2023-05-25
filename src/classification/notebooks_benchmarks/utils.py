import pandas as pd
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import shutil

from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import image_dataset_from_directory
from PIL import Image



def create_datasets_and_directories(path_to_csv,path_to_output,cap,nb_img_to_keep,only_species=True,image_size=128):

    """
    Given a dataset of cropped images, create the train, validation and test folders.
    Only keeps the images with more than cap images in the dataset, keeps only nb_img_to_keep images per class.
    Split for train, validation and test is 80/10/10.
    
    args : 

    path_to_csv : path to the csv file containing the dataset
                    # paths , # labels 
    path_to_output : path to the output folder were folders will be created
                     in this format : 
                        output_folder
                            - train
                            - validation
                            - test
                            - train_dataset.csv
                            - validation_dataset.csv
                            - test_dataset.csv
                            - weights.h5
    cap : minimum number of images per class, if None no cap
    nb_img_to_keep : number of images to keep per class, if None keep all images
    only_species : if True, only keeps the images labelled as species (i.e. real labels has more than 1 word) 
                     if False, keeps all the images
    image_size : size of the images to resize to
    TODO : integrate the only_species = False
    
    Returns : 
        train_dataset, validation_dataset, test_dataset : Dataset objects
    """

    ###### FILTER THE DATASET ######

    # read the csv file
    df_dataset = pd.read_csv(path_to_csv)
    
    # Take only the images labelled as species (i.e. real labels has more than 1 word)
    if only_species:
        df_dataset = df_dataset[df_dataset["Labels"].str.contains(" ")]
  
    # Get the number of species that have more than cap images
    if cap is not None : 
        species = df_dataset['Labels'].value_counts()[df_dataset['Labels'].value_counts() > cap]

        # Convert the series to a dataframe
        species = species.to_frame()

        # Reset the index
        species.reset_index(inplace=True)

        # Rename the columns
        species.columns = ['Species', 'Number of images']

        # Filter the dataset
        df_dataset = df_dataset[df_dataset["Labels"].isin(species["Species"])]

        print("Number of species with more than {} images : {}".format(cap, len(species)))
        print("Number of images in the filtered dataset : {}".format(len(df_dataset)))

        print('-'*50)

        print(df_dataset['Labels'].value_counts())

    if nb_img_to_keep is not None : 
        
        dataset = df_dataset.groupby('Labels').head(nb_img_to_keep)

    #### SPLITS THE DATASET #####


    # Get the paths and the labels
    X = dataset["Paths"]
    y = dataset["Labels"]

    
    X_train, X_test_val, y_train, y_test_val = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
    X_test, X_val, y_test, y_val = train_test_split(X_test_val, y_test_val, test_size=0.5, stratify=y_test_val, random_state=42)

    # Create the train, validation and test datasets

    train_dataset = pd.concat([X_train, y_train], axis=1)
    val_dataset = pd.concat([X_val, y_val], axis=1)
    test_dataset = pd.concat([X_test, y_test], axis=1)



    ###### CREATE THE FOLDER STRUCTURE ######

    if os.path.exists(path_to_output):
        shutil.rmtree(path_to_output)

    os.makedirs(path_to_output)

    os.makedirs(path_to_output + "/train")
    os.makedirs(path_to_output + "/validation")
    os.makedirs(path_to_output + "/test")

    ###### COPY THE IMAGES TO THE FOLDERS ######

    for index, row in train_dataset.iterrows():

        # Create the folder if it does not exist
        if not os.path.exists(path_to_output + "/train/" + row["Labels"]):
            os.makedirs(path_to_output + "/train/" + row["Labels"])

        # Copy the image
        shutil.copy(row["Paths"], path_to_output + "/train/" + row["Labels"])

    for index, row in val_dataset.iterrows():
            
            # Create the folder if it does not exist
            if not os.path.exists(path_to_output + "/validation/" + row["Labels"]):
                os.makedirs(path_to_output + "/validation/" + row["Labels"])
    
            # Copy the image
            shutil.copy(row["Paths"], path_to_output + "/validation/" + row["Labels"])

    for index, row in test_dataset.iterrows():

        # Create the folder if it does not exist
        if not os.path.exists(path_to_output + "/test/" + row["Labels"]):
            os.makedirs(path_to_output + "/test/" + row["Labels"])

        # Copy the image
        shutil.copy(row["Paths"], path_to_output + "/test/" + row["Labels"])

    ###### CREATE THE CSV FILES ######

    train_dataset.to_csv(path_to_output + "/train_dataset.csv", index=False)
    val_dataset.to_csv(path_to_output + "/validation_dataset.csv", index=False)
    test_dataset.to_csv(path_to_output + "/test_dataset.csv", index=False)


    ##### MAKE THE DATASET OBJECTS #####

    train_dataset = image_dataset_from_directory(os.path.join(path_to_output,"train"), shuffle=True, batch_size=32, image_size=(image_size,image_size),labels = 'inferred',label_mode= 'categorical')
    test_dataset = image_dataset_from_directory(os.path.join(path_to_output,"test"), shuffle=True, batch_size=32, image_size=(image_size,image_size),labels = 'inferred',label_mode= 'categorical')
    val_dataset = image_dataset_from_directory(os.path.join(path_to_output,"validation" ),shuffle=True, batch_size=32, image_size=(image_size,image_size),labels = 'inferred',label_mode= 'categorical')

    ##### PRINT INFO #####

    print('-'*50)
    print('-'*50)

    print("Number of species in the train dataset : {}".format(len(train_dataset.class_names)))
    print("Number of images in the train dataset : {}".format(len(train_dataset.file_paths)))

    print('-'*50)
    print("Number of species in the validation dataset : {}".format(len(val_dataset.class_names)))
    print("Number of images in the validation dataset : {}".format(len(val_dataset.file_paths)))
    
    print('-'*50)
    print("Number of species in the test dataset : {}".format(len(test_dataset.class_names)))
    print("Number of images in the test dataset : {}".format(len(test_dataset.file_paths)))

    print('-'*50)
    print('-'*50)


    
    return train_dataset, val_dataset, test_dataset


def load_img(path, img_size = 128,classes = ['Apis mellifera', 'Bombus terrestris']): 
    """
    Load image from a folder named after the species

    Parameters
    ----------
    path : str
        Path to the folder containing the images, folder name is the species name
    img_size : int
        Size of the image
    classes : list
        List of the species to load

    Returns
    -------
        x,y : arrays
    """

    # Get the list of all the files in directory
    file_path = []

    for root, dirs, files in os.walk(path):

        for f in files:
            fullpath = os.path.join(root, f)
            file_path.append(fullpath)


    # initialize the arrays
    x = np.zeros((len(file_path),img_size,img_size, 3))
    y = np.zeros((len(file_path),1))

    # loop over the input images
    for i, file in enumerate(file_path):

        # load the image, pre-process it, and store it in the data list
        image = cv2.imread(file)
        image = cv2.resize(image, (img_size,img_size),Image.ANTIALIAS)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image =np.asarray(image)
        x[i] = image

        # extract the class label from the image path and update the
        # labels list
        label = file.split(os.path.sep)[-2]
        # returns 0 or 1
        index  = classes.index(label)
        # convert to numpy array
        y[i] = int(index)

    return x,y


def plot_random_imgs_from_train(x_train,y_train,CLASSES):

    """
    Plot 9 random images from the train dataset

    Parameters
    ----------
    x_train : array
        Array of the train images
    y_train : array
        Array of the train labels
    CLASSES : list

    Returns
    -------
        None
    """

    # Randomisation des indices et affichage de 9 images alétoires de la base d'apprentissage
    indices = np.arange(x_train.shape[0])
    np.random.shuffle(indices)
    plt.figure(figsize=(12, 12))
    for i in range(0, 9):
        plt.subplot(3, 3, i+1)
        plt.title(CLASSES[int(y_train[i])])
        plt.imshow(x_train[i])
    plt.tight_layout()
    plt.show()


def plot_history(history,metric): 

    plt.plot(history.history[metric])
    plt.plot(history.history['val_'+metric])
    plt.title('model '+metric)
    plt.ylabel(metric)
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()