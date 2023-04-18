import pandas as pd
import numpy as np
from numpy.ma.core import transpose
from keras import backend as K
import math
import tensorflow as tf


"""
Initally from https://github.com/fabiopereira59/abeilles-cap500/blob/main/Notebooks/AnalyseAccuracyHierarchie.ipynb
"""

###### INPUTS ######

# path to the csv file with all the hierarchy
# csv format is : species, genus, subfamily, family

path_hierarchie = '/home/basile/Documents/projet_bees_detection_basile/classification/data/hierarchy.csv'

# path to the csv file with all the species and the number of images
# csv format is : species, number of images

path_data = '/home/basile/Documents/projet_bees_detection_basile/classification/data/liste_classes_71.csv'


###### SETTING UP THE VARIABLES ######

hierarchie = pd.read_csv(path_hierarchie)

species = hierarchie["species"].unique()
nb_species = len(species)

genus = list(hierarchie["genus"].unique())
nb_genus = len(genus)

family = list(hierarchie["family"].unique())
nb_family = len(family)

subfamily = list(hierarchie["subfamily"].unique())
nb_subfamily = len(subfamily)

# hierarchie.set_index("species", inplace=True)
data = pd.read_csv(path_data)
# data.set_index("species", inplace=True)

species_to_genus = np.zeros((nb_genus, nb_species))
genus_to_subfamily = np.zeros((nb_subfamily, nb_genus))
subfamily_to_family = np.zeros((nb_family, nb_subfamily))


for i in range(nb_species):

    nb_images = data.at[i, "0"]

    # species -> genus
    genus_species = hierarchie.at[i, "genus"]
    ind_genus = genus.index(genus_species)
    species_to_genus[ind_genus, i] = 1

    # genus -> subfamily
    subfamily_species = hierarchie.at[i, "subfamily"]
    ind_subfamily = subfamily.index(subfamily_species)
    genus_to_subfamily[ind_subfamily, ind_genus] = 1

    # subfamily -> family
    family_species = hierarchie.at[i, "family"]
    ind_family = family.index(family_species)
    subfamily_to_family[ind_family, ind_subfamily] = 1


###### DEFINING THE HIERARCHICAL LOSS (SPECIE LEVEL) ######

def Hierarchicaloss(species_to_genus, genus_to_subfamily, subfamily_to_family, batch_size, alpha=0.1):

    # Penalizes the loss of the higher levels of the hierarchy (family)
    # more than the lower levels (species)
    def weight(height=1):
        return math.exp(-alpha * height)

    def species_loss(y_true, y_pred):
        height = 0
        return weight(height) * K.categorical_crossentropy(y_true, y_pred)

    def species_to_genus_loss(y_true, y_pred):
        height = 1
        y_true_genus = K.transpose(tf.raw_ops.MatMul(
            a=species_to_genus, b=tf.cast(y_true, tf.float64), transpose_b=True))
        y_pred_genus = K.transpose(tf.raw_ops.MatMul(
            a=species_to_genus, b=tf.cast(y_pred, tf.float64), transpose_b=True))
        return weight(height) * K.categorical_crossentropy(y_true_genus, y_pred_genus), y_true_genus, y_pred_genus

    def genus_to_subfamily_loss(y_true, y_pred):
        height = 2
        y_true_subfamily = K.transpose(tf.raw_ops.MatMul(
            a=genus_to_subfamily, b=y_true, transpose_b=True))
        y_pred_subfamily = K.transpose(tf.raw_ops.MatMul(
            a=genus_to_subfamily, b=y_pred, transpose_b=True))
        return weight(height) * K.categorical_crossentropy(y_true_subfamily, y_pred_subfamily), y_true_subfamily, y_pred_subfamily

    def subfamily_to_family_loss(y_true, y_pred):
        height = 3
        y_true_family = K.transpose(tf.raw_ops.MatMul(
            a=subfamily_to_family, b=y_true, transpose_b=True))
        y_pred_family = K.transpose(tf.raw_ops.MatMul(
            a=subfamily_to_family, b=y_pred, transpose_b=True))
        return weight(height) * K.categorical_crossentropy(y_true_family, y_pred_family)

    def HIERARCHICAL_loss(y_true, y_pred):
        loss_species = tf.cast(species_loss(y_true, y_pred), tf.float64)
        loss_genus, y_true_genus, y_pred_genus = species_to_genus_loss(
            y_true, y_pred)
        loss_subfamily, y_true_subfamily, y_pred_subfamily = genus_to_subfamily_loss(
            y_true_genus, y_pred_genus)
        loss_family = subfamily_to_family_loss(
            y_true_subfamily, y_pred_subfamily)
        return (loss_species + loss_genus + loss_subfamily + loss_family)/batch_size

    # Return a function
    return HIERARCHICAL_loss


###### DEFINING THE HIERARCHICAL LOSS FOR GENUS ######

def Hierarchicaloss_genus(species_to_genus, genus_to_subfamily, subfamily_to_family, batch_size, alpha=0.1):

    # Penalizes the loss of the higher levels of the hierarchy (family)
    # more than the lower levels (species)
    def weight(height=1):
        return math.exp(-alpha * height)

    def species_loss(y_true, y_pred):
        height = 0
        return weight(height) * K.categorical_crossentropy(y_true, y_pred)

    def species_to_genus_loss(y_true, y_pred):
        height = 1
        y_true_genus = K.transpose(tf.raw_ops.MatMul(
            a=species_to_genus, b=tf.cast(y_true, tf.float64), transpose_b=True))
        y_pred_genus = K.transpose(tf.raw_ops.MatMul(
            a=species_to_genus, b=tf.cast(y_pred, tf.float64), transpose_b=True))
        return weight(height) * K.categorical_crossentropy(y_true_genus, y_pred_genus), y_true_genus, y_pred_genus

    def genus_to_subfamily_loss(y_true, y_pred):
        height = 2
        y_true_subfamily = K.transpose(tf.raw_ops.MatMul(
            a=genus_to_subfamily, b=y_true, transpose_b=True))
        y_pred_subfamily = K.transpose(tf.raw_ops.MatMul(
            a=genus_to_subfamily, b=y_pred, transpose_b=True))
        return weight(height) * K.categorical_crossentropy(y_true_subfamily, y_pred_subfamily), y_true_subfamily, y_pred_subfamily

    def subfamily_to_family_loss(y_true, y_pred):
        height = 3
        y_true_family = K.transpose(tf.raw_ops.MatMul(
            a=subfamily_to_family, b=y_true, transpose_b=True))
        y_pred_family = K.transpose(tf.raw_ops.MatMul(
            a=subfamily_to_family, b=y_pred, transpose_b=True))
        return weight(height) * K.categorical_crossentropy(y_true_family, y_pred_family)

    def HIERARCHICAL_loss(y_true, y_pred):
        loss_genus, y_true_genus, y_pred_genus = species_to_genus_loss(
            y_true, y_pred)
        loss_subfamily, y_true_subfamily, y_pred_subfamily = genus_to_subfamily_loss(
            y_true_genus, y_pred_genus)
        loss_family = subfamily_to_family_loss(
            y_true_subfamily, y_pred_subfamily)

        return (loss_genus + loss_subfamily + loss_family)/batch_size
    
    return HIERARCHICAL_loss