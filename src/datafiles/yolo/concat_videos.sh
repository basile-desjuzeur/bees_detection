path_to_images="/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/BD_71"

for folder in $(ls $path_to_images)
do
    for file in $(ls $path_to_images/$folder)
    do
        echo "$file" >> "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/all_videos.csv"
        
    done
done

