import csv
import pandas as pd
from IPython.display import display
import cv2

#path

results_max = "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/comparate_results_videos/results_prediction.csv" #prédictions faites avec le modèle max
result_reelle = "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/comparate_results_videos/annotations.csv"

#on crée des dataframes à partir des csv

df_results_max = pd.read_csv(results_max, sep=",")
df_results_reelle = pd.read_csv(result_reelle, sep=",")


#comparaison

#on veut comparer les prédictions avec les vraies valeurs

videos_max = df_results_max['videos']
#on ne veut prendre que la dernière partie du nom de la vidéo
videos_max = videos_max.str.split('/').str[-1]

#df_results_max["videos"] = videos_max

especes_pred_max = df_results_max["prediction"]
clean_especes_pred_max = []
for predict in list(especes_pred_max):
    #on veut transformer la liste de string list(especes_pred_max) en liste de liste
    predict = predict.replace("[", "")
    predict = predict.replace("]", "")
    predict = predict.replace("'", "")
    predict = predict.split(", ")
    clean_especes_pred_max.append(predict)


#on prend le csv /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/comparate_results_videos/false_max_0.5.csv" et on sépare la colonne prediction en 4 colonnes espece1_predite, espece2_predite, espece3_predite, espece4_predite
#s'il n'y a pas 4 espèces prédites alors on met NaN

df_results_max["espece1_predite"] = [x[0] if len(x) > 0 else "NaN" for x in clean_especes_pred_max]
df_results_max["espece2_predite"] = [x[1] if len(x) > 1 else "NaN" for x in clean_especes_pred_max]
df_results_max["espece3_predite"] = [x[2] if len(x) > 2 else "NaN" for x in clean_especes_pred_max]
df_results_max["espece4_predite"] = [x[3] if len(x) > 3 else "NaN" for x in clean_especes_pred_max]
df_results_max.drop(columns=["prediction"], inplace=True)



#on veut transformer la liste de string list(especes_pred_max) en liste de liste
espece1 = df_results_reelle["espece1"]
espece2 = df_results_reelle["espece2"]
espece3 = df_results_reelle["espece3"]
espece4 = df_results_reelle["espece4"]


#on prend le csv /home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/comparate_results_videos/false_max_0.5.csv" et on sépare la colonne prediction en 4 colonnes espece1_predite, espece2_predite, espece3_predite, espece4_predite

df_results_reelle["espece1_reelle"] = [x for x in espece1]
df_results_reelle["espece2_reelle"] = [x for x in espece2]
df_results_reelle["espece3_reelle"] = [x for x in espece3]
df_results_reelle["espece4_reelle"] = [x for x in espece4]

        
df_results_reelle.drop(columns=["espece1"], inplace=True)
df_results_reelle.drop(columns=["espece2"], inplace=True)
df_results_reelle.drop(columns=["espece3"], inplace=True)
df_results_reelle.drop(columns=["espece4"], inplace=True)


df_results_max["espece1_reelle"] = df_results_reelle["espece1_reelle"]
df_results_max["espece2_reelle"] = df_results_reelle["espece2_reelle"]
df_results_max["espece3_reelle"] = df_results_reelle["espece3_reelle"]
df_results_max["espece4_reelle"] = df_results_reelle["espece4_reelle"]
df_results_max.drop(columns=["reelle"], inplace=True)

display(df_results_max)

#on rajoute une colonne qui indique si la prédiction est bonne

#on veut comparer les 4 colonnes de prédiction avec les 4 colonnes de vraies valeurs en le faisant ligne par ligne
df_results_max["bonne_prediction"] = [True for x in range(len(df_results_max))]
for i in range(len(df_results_max)):
    #on utilise string1.__eq__(string2)
    if not df_results_max["espece1_predite"][i].__eq__(df_results_max["espece1_reelle"][i]): #l'adresse est comparée ici car on utilise de spointeurs, pas le contenu
        df_results_max["bonne_prediction"][i] = False
    if not df_results_max["espece2_predite"][i].__eq__(df_results_max["espece2_reelle"][i]):
        df_results_max["bonne_prediction"][i] = False
    if not df_results_max["espece3_predite"][i].__eq__(df_results_max["espece3_reelle"][i]):
        df_results_max["bonne_prediction"][i] = False
    if not df_results_max["espece4_predite"][i].__eq__(df_results_max["espece4_reelle"][i]):
        df_results_max["bonne_prediction"][i] = False
        
display(df_results_max)


#on veut rajouter une colonnes qui donne le temps de passage de chaque espèce sur la vidéo en utilisant le fichier count_frames.csv

df_times = pd.read_csv("/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/count_frame.csv")

df_results_max["duree1"] = df_times["temps_de_passage1"]
df_results_max["duree2"] = df_times["temps_de_passage2"]
df_results_max["duree3"] = df_times["temps_de_passage3"]
df_results_max["duree4"] = df_times["temps_de_passage4"]    
df_results_max["duree5"] = df_times["temps_de_passage5"]   


# #on veut convertir ce dataframe en un csv

df_results_max.to_csv("/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/comparate_results_videos/comparaison.csv", index=False)

