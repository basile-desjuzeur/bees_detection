import pandas as pd
import os
import re

"""
This script aims to get the number of image per specie per dataset
The folders are structured differently :
- some are made hierarchically, there the label is the name of the last subfolder

    for almost all folders the structure is : name_of_folder/specie/observator/img
    for some it is , name_of_folder/specie/observator/subfolders/img 

- some are flat, there the label is contained in the name of the file , we use regex to get it

We dont take BD_71 as it is composed of pictures from all the other datasets
"""


path_to_dataset = "/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/whole_dataset_cropped"
dir_anthophila = 'Anthophila'
dir_new_justine = 'New_Justine'
dir_DG = 'DG'
dir_other = [dir_anthophila, dir_new_justine, dir_DG]
dir_hierarchical = [ 'HS', 'LMDI','inat_25_04']
dir_flat = ['iNaturalist', 'Spipoll']
dirs = dir_other + dir_hierarchical + dir_flat
path_csv = '/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/datafiles/final_datafiles/dataset_yolo_cropped_with_real_labels'
path_whole_dataset_csv = '/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/datafiles/final_datafiles/dataset_yolo_cropped_with_real_labels/whole_dataset.csv'
output_path = '/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/datafiles/final_datafiles/dataset_yolo_cropped_with_real_labels/number_of_images_per_specie_per_dataset.csv'


def clean_Anthophila_folder(path_to_dataset):
    """
    Structures a folder according to the following pattern : 

    folder/specie/observators/imgs

    Some are in this structure : folder/specie/observators/some_subfolders/img
    """

    # Check the number of sufolders to access the files
    for root, dirs, files in os.walk(path_to_dataset):

        for file in files:

            # Check the number of subfolders to access the files
            img_path = os.path.join(root, file)

            # a path would be like this : /home/basile/Documents/projet_bees_detection_basile/data_bees_detection/
            # whole_dataset/Anthophila_copy/Andrena leucolippa/Christophe.Philippe-Andrena leucolippa/
            # Christophe.Philippe-Andrena leucolippa Boutenac(11)  19 juin 2020/IMG_6270.JPG
            if len(img_path.split(os.path.sep)) > 1:

                # Get the parent folder and move the file in it
                parent_folder = os.path.sep.join(
                    img_path.split(os.path.sep)[:-2])
                os.system("mv '" + str(img_path) +
                          "' '" + str(parent_folder) + "'")

                # Remove the empty subfolder
                subfolder = os.path.sep.join(img_path.split(os.path.sep)[:-1])
                os.system("rm -r '" + subfolder + "'")

def get_number_of_image_Anthophila(path_to_dataset):
    """
    For folders hierarchically structured, label is the last folder

    param : path to dataset
    return : number of image per specie in this dataset as a dataframe
    """

    # Lists to store paths to img and real labels
    paths = []
    labels = []

    for root, dirs, files in os.walk(path_to_dataset):

        for file in files:

            img_path = os.path.join(root, file)
            paths.append(img_path)

            img_label = img_path.split(os.path.sep)[-3]
            labels.append(img_label)

    df_hierarchical_folder = pd.DataFrame(
        {'Paths': paths, 'Real labels': labels})

    return df_hierarchical_folder

def get_number_of_image_hierarchical(path_to_dataset):
    """
    For folders hierarchically structured, label is the last folder

    param : path to dataset
    return : number of image per specie in this dataset as a dataframe
    """

    # Lists to store paths to img and real labels
    paths = []
    labels = []

    for root, dirs, files in os.walk(path_to_dataset):

        for file in files:

            img_path = os.path.join(root, file)
            paths.append(img_path)

            img_label = img_path.split(os.path.sep)[-2]
            labels.append(img_label)

    df_hierarchical_folder = pd.DataFrame(
        {'Paths': paths, 'Real labels': labels})

    return df_hierarchical_folder

def get_number_of_image_flat(path_to_dataset):
    '''
    Images are stored like this :
    whole_dataset/iNaturalist/inaturalist_1/Aglaoapis tridentata44393.jpg
    '''

    # Lists to store paths to img and real labels
    paths = []
    labels = []

    for root, dirs, files in os.walk(path_to_dataset):

        for file in files:

            if file.endswith('.txt'):
                continue

            img_path = os.path.join(root, file)
            paths.append(img_path)

            img_label = re.findall(r"^[A-Za-z ]+?(?=\d+\.\w+)", file)[0]
            labels.append(img_label)

    df = pd.DataFrame({'Paths': paths, 'Real labels': labels})

    return df

def clean_DG_labels(path):
    """
    DG labels are like this :
    Lasioglossum (Evylaeus) corvinum
    We want to remove the parenthesis and the content inside
    """

    df = pd.read_csv(path)

    # Remove parenthesis and content inside, remove one space between the two words
    df['Real labels'] = df['Real labels'].apply( lambda x : re.sub(r"\(.*\)", "", x).replace("  ", " "))

    # Deletes the previous csv
    os.system("rm " + path)

    # Save the new csv
    df.to_csv(path, index=False)

    return

def merge_csv(paths=path_csv,dirs=dirs, path_whole_dataset=path_whole_dataset_csv):
    
    """
    Merge all the csv files in one
    """
    
    paths = [os.path.join(paths, dir + '.csv') for dir in dirs]


    # Merges all the csv files in one, one after the other
    dfs = [pd.read_csv(path) for path in paths]

    df = pd.concat(dfs, axis=0, ignore_index=True)

    df.to_csv(path_whole_dataset, index=False)

def get_nb_per_specie_per_dataset(paths=path_csv, dirs =dirs,  path_whole_dataset=path_whole_dataset_csv, output_path=output_path):
    """
    Get the number of images per specie per dataset
    Concatenate all the dataframes in one
    """

    # Read the whole dataset and set the index to the real labels    
    df = pd.read_csv(path_whole_dataset,usecols=['Paths', 'Real labels'])
    df = df.drop(columns=['Paths'])
    df = df['Real labels'].value_counts().reset_index()
    df.columns = ['Specie', 'Total']

    # list of paths to the csv files

    paths = [os.path.join(path_csv,dir +'.csv') for dir in dirs]

    # Get the number of images per specie per dataset

    for path in paths:

        dataset_name =  path.split('/')[-1].split('.')[0]

        df_temp = pd.read_csv(path,usecols=['Paths', 'Real labels'])
        df_temp = df_temp.drop(columns=['Paths'])
        df_temp = df_temp['Real labels'].value_counts().reset_index()
        df_temp.columns = ['Specie', dataset_name]
        df = pd.merge(df, df_temp, on='Specie', how='outer')

    # Fill NaN with 0
    df = df.fillna(0)

    # Converts the number of images per specie per dataset to int
    for col in df.columns[1:]:
        df[col] = df[col].astype(int)

    # Sort the dataframe by alphabetical order
    df = df.sort_values(by=['Specie'])
    
    # Save the new csv
    df.to_csv(output_path, index=False)
 
    return


if __name__ == '__main__': 

    path = os.path.join(path_to_dataset, dir_anthophila)

    #####  Antophila #####

    # clean_Anthophila_folder(path)

    df = get_number_of_image_Anthophila(path)

    # removes the " in the path
    df['Paths'] = df['Paths'].apply(lambda x : x.replace('"', ''))

    df.to_csv( os.path.join(path_csv,dir_anthophila+'.csv'), index=False)

    ##### NEW JUSTINE #####

    path = os.path.join(path_to_dataset, dir_new_justine)


    df = get_number_of_image_Anthophila(path)

    df.to_csv( os.path.join(path_csv,dir_new_justine+'.csv'), index=False)



    #####  Hierarchical folder #####

    for dir in  dir_hierarchical:

        path = os.path.join(path_to_dataset, dir)

        df = get_number_of_image_hierarchical(path)

        df.to_csv(os.path.join(path_csv,dir +'.csv'), index=False)

    #####  Flat folder #####

    for dir in  dir_flat:

        path = os.path.join(path_to_dataset, dir)

        df = get_number_of_image_flat(path)

        df.to_csv(os.path.join(path_csv,dir +'.csv'), index=False)

    #####  DG #####

    path = os.path.join(path_to_dataset, dir_DG)

    df = get_number_of_image_hierarchical(path)

    df.to_csv(os.path.join(path_csv,dir_DG+'.csv'), index=False)

    clean_DG_labels(os.path.join(path_csv,dir_DG+'.csv'))

    #####  Merge all the csv files #####

    merge_csv()

    #####  Get the number of images per specie per dataset #####

    get_nb_per_specie_per_dataset()
