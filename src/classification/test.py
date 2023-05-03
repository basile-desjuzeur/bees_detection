from keras.utils import paths_and_labels_to_dataset
import pandas as pd

df_train = pd.read_csv('/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/datafiles/classification/inputs/VGG16/test.csv')



train_ds = paths_and_labels_to_dataset(
    image_paths = df_train['Paths'].values,
    image_size = (64,64),
    num_channels= 3,
    labels = df_train['Id'].values,
    label_mode = 'categorical',
    num_classes = df_train['Id'].nunique(),
    interpolation = 'bilinear',
    crop_to_aspect_ratio=False)

print(train_ds)