import os 
from pathlib import Path
import pandas as pd 
import json 
from PIL import Image


path_to_json='/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/BD_71_Annotations/JSON'
path_to_images='/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/BD_71'
taxon_detection='Anthophila'
path_to_output_csv='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/bees_detection_dataset.csv'


master_dict=[]      # dict to be converted in csv
minor_dict=[]       # dict with the corrupted files


# Create a dataframe with the info of every pictures

for file in os.listdir(path=path_to_json):

    with open(file=os.path.join(path_to_json,file)) as file:

        json_file=json.load(file)
        json_file_verified=[picture for picture in json_file if picture['visited']==1] #only takes verified pic
        
        for picture in json_file_verified:
            for box in picture['boxes']:

                file_path=picture['file_path'] 
                xmin=box['xmin']
                xmax=box['xmax']
                ymin=box['ymin']
                ymax=box['ymax']
                taxon=picture['specie']


                # getting the image size 
                # in the json the path is "./BD_71/Amegilla quadrifasciata/Amegilla quadrifasciata51495.jpg"
                path_to_img=str(file_path)[7:]
                path_to_img=Path(path_to_images + path_to_img)

                try:
                    img=Image.open(path_to_img) 
                    w,h= img.size
                    box_info=[file_path,xmin,ymin,xmax,ymax,taxon,w,h,]
                    master_dict.append(box_info)
                
                except Exception:

                    minor_dict.append(path_to_img)

df_ok=pd.DataFrame(master_dict,columns=['file_path','xmin','ymin','xmax','ymax','taxon','w','h'])


# Cleans the dataframe so that it can be processed by gen_anchors.py

df_ok['xmin']=df_ok['xmin']*df_ok['w']       # xmin,.. stored as relative values in json
df_ok['xmax']=df_ok['xmax']*df_ok['w']       # need to be converted to absolute values
df_ok['ymin']=df_ok['ymin']*df_ok['h']       # for gen_anchors    
df_ok['ymax']=df_ok['ymax']*df_ok['h']

df_ok['taxon']=taxon_detection                   # we only need one discrimination
df_ok.iloc[:,0]=df_ok.iloc[:,0].map(lambda row : row.split('/',1)[1])

df_missing=pd.DataFrame(minor_dict)

# Dataframe to csv
# df_missing allows you to check if there is no corrupted pictures                 
df_ok.to_csv('/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/BD_71_Annotations/bees_detection_dataset.csv',index=False,header=False)     
df_missing.to_csv('/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/BD_71_Annotations/missing_bees_detection_dataset.csv',index=False,header=False)     
