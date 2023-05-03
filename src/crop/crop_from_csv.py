import os 
import pandas as pd
from tqdm import tqdm
from PIL import Image



#### INPUTS ####

# path to the csv file containing the predictions
path_csv = '/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/datafiles/crop/predict_csv/other/whole_datast_predicted_latest.csv'

# path to the folder were the cropped images are stored
path_folder = '/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/whole_dataset_cropped'


#### SCRIPT ####


def crop_image(img_path, x, y, w, h):
    '''
    Crop image from x, y, w, h coordinates
    '''
    img = Image.open(img_path)
    img = img.crop((x, y, x+w, y+h))
    
    return img 





# Read the csv file
df = pd.read_csv(path_csv, header=None)

# Create all the folders
df_folders = df.iloc[:,0].apply(lambda x: x.split('/')[:-1])
df_folders = df_folders.apply(lambda x: '/'.join(x))
df_folders = df_folders.apply(lambda x: x.replace('whole_dataset', 'whole_dataset_cropped'))
df_folders = df_folders.drop_duplicates()

for folder in tqdm(df_folders):
    if not os.path.exists(folder):
        os.makedirs(folder)


# Crop the images
for index, row in tqdm(df.iterrows()):

    # Get the image path
    img_path = row[0]
    new_img_path = img_path.replace('whole_dataset', 'whole_dataset_cropped')
    # img_path = img_path.replace(' ', '\ ')

    # Get the coordinates
    x = row[1]
    y = row[2]
    w = row[3]
    h = row[4]

    # Crop the image
    img = crop_image(img_path, x, y, w, h)

    # Save the image
    img.save(new_img_path)

