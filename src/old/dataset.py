import pandas as pd 

path='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/bees_detection_dataset.csv'
# n_path='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/bees_detection_dataset_reduced.csv'

df=pd.read_csv(path)

# # df.iloc[:,0]=df.iloc[:,0].map(lambda row : row.split('/',1)[1])
# df.to_csv(n_path,index=False)

df=df.iloc[:,1:]
df.iloc[:,0]=df.iloc[:,0].map(lambda row : row.split('/',1)[1])
df.iloc[:,-3]='Anthophila'
df.to_csv(path,header=False,index=False)