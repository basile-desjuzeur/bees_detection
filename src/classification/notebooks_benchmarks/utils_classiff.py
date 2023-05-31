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

from keras.utils import Sequence
import cv2 as cv



def create_datasets_and_directories(path_to_csv,path_to_output,cap,nb_img_to_keep,only_species=True,image_size =128,nb_classes_to_keep ='all'):

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

    only_species : if True, only keeps the images labelled as species (i.e. real labels has more than 1 word)

    nb_classes_to_keep : number of classes to keep, if 'all' keeps all the classes

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


    if nb_classes_to_keep != 'all' :

        if nb_classes_to_keep < len(species) :

            # Get random species
            species_to_keep = species.sample(nb_classes_to_keep)

        else :
            print("nb_classes_to_keep must be less than the number of species with more than {} images, we kept all the species".format(cap))
            species_to_keep = species

            

    # Filter the dataset
    df_dataset = df_dataset[df_dataset["Labels"].isin(species_to_keep["Species"])]

    if nb_img_to_keep is not None : 
        
        dataset = df_dataset.groupby('Labels').head(nb_img_to_keep)

        
    print('\n SUM UP OF THE FILTERING PROCESS : \n')
    print('-'*50)


    print("Number of species with more than {} images : {}".format(cap, len(species)))

    nb_classes_to_keep = len(species) if nb_classes_to_keep == 'all' else int(nb_classes_to_keep)

    print("Number of species kept after filtering : {}".format(nb_classes_to_keep))

    print("Number of images in the filtered dataset : {}".format(len(df_dataset)))


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


def create_directories(path_to_csv,path_to_output,cap,nb_img_to_keep,only_species=True,image_size =128,nb_classes_to_keep ='all'):
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

    only_species : if True, only keeps the images labelled as species (i.e. real labels has more than 1 word)

    nb_classes_to_keep : number of classes to keep, if 'all' keeps all the classes

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



    if nb_classes_to_keep != 'all' :

        if nb_classes_to_keep < len(species) :

            # Get random species
            species_to_keep = species.sample(nb_classes_to_keep)

        else :
            print("nb_classes_to_keep must be less than the number of species with more than {} images, we kept all the species".format(cap))
            species_to_keep = species

            

    # Filter the dataset
    df_dataset = df_dataset[df_dataset["Labels"].isin(species_to_keep["Species"])]

    if nb_img_to_keep is not None : 
        
        dataset = df_dataset.groupby('Labels').head(nb_img_to_keep)

        
    print('\n SUM UP OF THE FILTERING PROCESS : \n')
    print('-'*50)


    print("Number of species with more than {} images : {}".format(cap, len(species)))

    nb_classes_to_keep = len(species) if nb_classes_to_keep == 'all' else int(nb_classes_to_keep)

    print("Number of species kept after filtering : {}".format(nb_classes_to_keep))



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


    ##### PRINT INFO #####

    print('_'*50)
    print("Number of species in the train dataset : {}".format(len(train_dataset["Labels"].unique())))
    print("Number of images in the train dataset : {}".format(len(train_dataset)))

    print('-'*50)
    print("Number of species in the validation dataset : {}".format(len(val_dataset["Labels"].unique())))
    print("Number of images in the validation dataset : {}".format(len(val_dataset)))

    print('-'*50)
    print("Number of species in the test dataset : {}".format(len(test_dataset["Labels"].unique())))
    print("Number of images in the test dataset : {}".format(len(test_dataset)))

    print('-'*50)

    print('Classes : ')
    classes = train_dataset['Labels'].unique()
    # convert to list
    classes = classes.tolist()
    print(classes)
    print('_'*50)

    X_train, y_train = train_dataset["Paths"], train_dataset["Labels"]
    X_val, y_val = val_dataset["Paths"], val_dataset["Labels"]
    X_test, y_test = test_dataset["Paths"], test_dataset["Labels"]

    return X_train, y_train, X_val, y_val, X_test, y_test, classes
    

def load_img(path, img_size,classes): 
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
    y = np.zeros((len(file_path),len(classes)),dtype=int)

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
        # convert to one hot encoding
        y[i][index] = 1


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

class AbeillesSequence(Sequence):
    #  Initialisation de la séquence avec différents paramètres
    def __init__(self, x_train, y_train, batch_size, class_names, image_size):
        self.x_train = x_train
        self.y_train = y_train
        self.classes = class_names
        self.batch_size = batch_size
        self.image_size = image_size
        self.indices1 = np.arange(len(x_train))

        np.random.shuffle(self.indices1)
        #  Les indices permettent d'accéder
        #  aux données et sont randomisés à chaque epoch pour varier la composition
        #  des batches au cours de l'entraînement

    #  Fonction calculant le nombre de pas de descente du gradient par epoch
    def __len__(self):
        return int(np.ceil(self.x_train.shape[0] / float(self.batch_size)))

    # Application de l'augmentation de données à chaque image du batch

    def apply_augmentation(self, bx, by):

        batch_x = np.zeros((bx.shape[0], self.image_size, self.image_size, 3))
        batch_y = by

        # Pour chaque image du batch
        for i in range(len(bx)):

            # Récupération du label de l'image
            class_labels = []
            class_id = np.argmax(by[i])
            class_labels.append(self.classes[class_id])

            # Read image
            img = cv.imread(bx[i])
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

            # resize
            img = self._resize_img_(img)

            batch_x[i] = img

        return batch_x, batch_y

    def _resize_img_(self, img):
        # resize img to image_size x image_size, add padding if necessary

        shape = img.shape

        # cas 1 : both dimensions are too small
        if shape[0] < self.image_size and shape[1] < self.image_size:

            # add padding
            img = cv.copyMakeBorder(
                img, 0, self.image_size - shape[0], 0, self.image_size - shape[1], cv.BORDER_CONSTANT, value=(0, 0, 0))

        # cas 2 : every other case
        else:

            # add padding to the smallest dimension to make it equal to the biggest one
            if shape[0] < shape[1]:
                img = cv.copyMakeBorder(
                    img, 0, shape[1] - shape[0], 0, 0, cv.BORDER_CONSTANT, value=0)
            else:
                img = cv.copyMakeBorder(
                    img, 0, 0, 0, shape[0] - shape[1], cv.BORDER_CONSTANT, value=0)

            # resize
            img = cv.resize(img, (self.image_size, self.image_size))

        return img

    #  Fonction appelée à chaque nouveau batch : sélection et augmentation des données
    # idx = position du batch (idx = 5 => on prend le 5ème batch)

    def __getitem__(self, idx):
        # Sélection des données : batch x correspond aux filepath
        batch_x = self.x_train[self.indices1[idx *
                                             self.batch_size:(idx + 1) * self.batch_size]]
        batch_y = self.y_train[self.indices1[idx *
                                             self.batch_size:(idx + 1) * self.batch_size]]

        #  Application de l'augmentation de données
        batch_x, batch_y = self.apply_augmentation(batch_x, batch_y)

        # Normalisation des données
        batch_x = color_preprocessing(batch_x)

        #### temp ####

        mean, std, min, max = np.mean(batch_x), np.std(
            batch_x), np.min(batch_x), np.max(batch_x)
        shp = batch_x.shape

        print('-'*50)
        print("mean : {}".format(mean), "std : {}".format(std),
              "min : {}".format(min), "max : {}".format(max))
        

        return batch_x, batch_y

    #  Fonction appelée à la fin d'un epoch ; on randomise les indices d'accès aux données
    def on_epoch_end(self):
        np.random.shuffle(self.indices1)


class BeeBatchGenerator(Sequence):

    def __init__(self, image_filenames, labels, batch_size, image_size, classes,cap):
        """
        Parameters
        ----------
        image_filenames : np.array of filepaths
        labels : np.array of labels as one-hot encoded vectors
        batch_size : int
        image_size : tuple of ints
        classes : list of strings
        cap : int, number of images to load per species in each batch
        """
        self.image_filenames, self.labels = image_filenames, labels
        self.batch_size = batch_size
        self.image_size = image_size
        self.classes = classes
        self.cap = cap

        # Set _indices_ list for the first epoch
        self.on_epoch_end()

    def __len__(self):
        """
        Number of batches per epoch, i.e. number of gradient steps per epoch
        """
        return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))
    

    def _process_batch_(self, _batch_x, _batch_y):
        """
        Converts a batch of paths to a batch of normalized np.arrays
        """
        batch_x = np.zeros((len(_batch_x), self.image_size, self.image_size, 3))
        batch_y = _batch_y

        # Iterates over the batch
        for i,_img_path in enumerate(_batch_x):

            # Read image
            img = Image.open(_img_path)

            # Resize
            img = img.resize(self.image_size,Image.ANTIALIAS)

            # Convert to array
            img = np.asarray(img)

            # Normalize
            img = img/255

            # Add to batch
            batch_x[i] = img


        return batch_x, batch_y
  

    def __getitem__(self, idx):
        """
        Returns one batch of data, idx refers to batch number
        """
        # Initialisation of the batch
        _batch_x = self.image_filenames[self.indices[idx *self.batch_size:(idx + 1) * self.batch_size]]
        _batch_y = self.labels[self.indices[idx *self.batch_size:(idx + 1) * self.batch_size]]

        # Processing of the batch
        batch_x, batch_y = self._process_batch_(_batch_x, _batch_y)

        return batch_x, batch_y


    def _on_epoch_end_(self):
        """
        Shuffle the data at the end of each epoch
        """
        np.random.shuffle(self.indices)


class BeeBatchGeneratorCapped(Sequence):

    def __init__(self, image_filenames, labels, batch_size, image_size, classes,cap):
        """
        Parameters
        ----------
        image_filenames : np.array of filepaths
        labels : np.array of labels as one-hot encoded vectors
        batch_size : int
        image_size : tuple of ints
        classes : list of strings
        cap : int, number of images to load per species in each batch
        """
        self.image_filenames, self.labels = image_filenames, labels
        self.batch_size = batch_size
        self.image_size = image_size
        self.classes = classes
        self.cap = cap

        # Get the nb of nb of images in the less represented class
        self.min_nb = np.min(np.sum(labels,axis=0))

        if self.cap > self.min_nb:
            self.cap = self.min_nb
            print("Warning : cap is higher than the number of images in the less represented class, cap is set to {}".format(self.cap))


        # First shuffle of the data
        self.indices = np.arange(len(image_filenames))
        self._indices_ = np.shuffle(self.indices)

    def __len__(self):
        """
        Number of batches per epoch, i.e. number of gradient steps per epoch
        """
        return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))
    

    def _process_batch_(self, _batch_x, _batch_y):
        """
        Converts a batch of paths to a batch of normalized np.arrays
        """
        batch_x = np.zeros((len(_batch_x), self.image_size, self.image_size, 3))
        batch_y = _batch_y

        # Iterates over the batch
        for i,_img_path in enumerate(_batch_x):

            # Read image
            img = Image.open(_img_path)

            # Resize
            img = img.resize(self.image_size,Image.ANTIALIAS)

            # Convert to array
            img = np.asarray(img)

            # Normalize
            img = img/255

            # Add to batch
            batch_x[i] = img


        return batch_x, batch_y
  

    def __getitem__(self, idx):
        """
        Returns one batch of data 
        """
        # Initialisation of the batch
        _batch_x = self.image_filenames[self._indices_[0 : self.batch_size]]
        _batch_y = self.labels[self._indices_[0 : self.batch_size]]

        # Processing of the batch
        batch_x, batch_y = self._process_batch_(_batch_x, _batch_y)

        return batch_x, batch_y
        

    def _on_epoch_end_(self):
        """
        Create a new _indices list at the end of each epoch, with the same distribution of classes
        (the list contains the indices of the images in the dataset, with "cap" images per class)
        """
        
        # initialisation of the new indices list
        self._indices_ = np.zeros((self.cap*len(self.classes),))

        # Iterates over the classes
        for i,_class in enumerate(self.classes):

            # Get the indices of the images of the class
            _indices = np.where(self.labels[:,i] == 1)[0]

            # Randomize the indices
            np.random.shuffle(_indices)

            # Add the first "cap" indices to the new indices list
            self._indices_[i*self.cap:(i+1)*self.cap] = _indices[:self.cap]

        # Shuffle the new indices list
        np.random.shuffle(self._indices_)



    