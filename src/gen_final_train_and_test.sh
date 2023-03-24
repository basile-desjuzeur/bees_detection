#paths

path_to_existing_train='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_train_iNat_trainset.csv' 
path_to_existing_validset='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_train_iNat_validset.csv'
path_to_existing_testset='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_test.csv'

path_to_empty_images_train='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_true_empty_train_trainset.csv'
path_to_empty_images_validset='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_true_empty_train_validset.csv'
path_to_empty_images_testset='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_true_empty_test.csv'

path_to_final_trainset='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_final_trainset.csv'
path_to_final_validset='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_final_validset.csv'
path_to_final_testset='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_final_testset.csv'

#mix full and empty images in new train and valid set

cat $path_to_empty_images_train $path_to_existing_train > $path_to_final_train_set


cat /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_train_iNat_validset.csv /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_true_empty_train_validset.csv  > /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_final_validset.csv



cat /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_test.csv /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_true_empty_test.csv  > /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/input_final_testset.csv