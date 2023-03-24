path_to_images='/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/BD_71'
path_to_all_images='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/bees_detection_dataset.csv'
# Generate new data

for file in $(find $path_to_images | grep -v 'detected\|iNat')
do 
if [ -d $file ]
then
    continue
else
#echo $file
a=${file##*raw_data/}
echo $a>>$path_to_all_images
fi
done