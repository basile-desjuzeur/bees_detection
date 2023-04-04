import os 


"""
For some reasons, in some folders, picture's filename have no extension
"""

path='/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/Whole dataset/DG'

for root,dir,filenames in os.walk(path):

    for filename in filenames: 

        # the file has no extension in filename
        if '.' not in filename:
            # we add the extension
            os.rename(os.path.join(root,filename),os.path.join(root,filename+'.jpeg'))
