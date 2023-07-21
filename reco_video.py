import pandas as pd
import torch
import copy
import math
import os
import wandb
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import ndcg_score, dcg_score
import modele_client

df=pd.read_csv("transcription/train_emolis_meld.csv")
df2=pd.read_csv("transcription/dev_emolis.csv")
df3=pd.read_csv("transcription/test_emolis.csv")
df=pd.concat([df, df2, df3], ignore_index=True)
emotions=[]
features=[]
i=0
dicti_scenes={}
dicti_names={}
names=[]
cpt=0
names=[]
while(i<len(df["Emotion"])):
	name=df["Name"][i]
	if name[0:7]!="friends":
		name=name.split("_")
		name[-1]=str(df["Sr No."][i])
		if name[0]+"_"+name[1]not in names :
			dicti_scenes[name[0]+"_"+name[1]]=[]
			dicti_names[name[0]+"_"+name[1]]=[]
			names.append(name[0]+"_"+name[1])
		dicti_names[name[0]+"_"+name[1]].append(int(name[-1]))
		name="_".join(name)
		try :
			features.append(torch.load("total_features/"+name+".pt"))
			#features[-1]=features[-1][0:features[-1].shape[0]//2]
			dicti_scenes[name.split("_")[0]+"_"+name.split("_")[1]].append(features[-1])
		except:
			del dicti_names[name.split("_")[0]+"_"+name.split("_")[1]][-1]
	i=i+1



i=0
dicti_scenes2={}
dicti_names2={}
while(i<len(dicti_scenes.keys())):
	keys=list(dicti_scenes.keys())[i]
	dicti_scenes2[keys]=[]
	dicti_names2[keys]=[]
	j=0
	k=0
	while(j<=max(dicti_names[keys])):
		k=0
		while(k<len(dicti_names[keys])):
			if j ==dicti_names[keys][k] :
				dicti_scenes2[keys].append(dicti_scenes[keys][k])
				dicti_names2[keys].append(dicti_names[keys][k])
			k=k+1
		if j not in dicti_names[keys]:
			dicti_scenes2[keys].append(None)
			dicti_names2[keys].append(j)
		j=j+1
	i=i+1

i=0
while(i<len(dicti_scenes2.keys())):
	keys=list(dicti_scenes2.keys())[i]
	j=0
	booleen=False
	while(j<len(dicti_scenes2[keys])):
		if dicti_scenes2[keys][j] ==None :
			if j==0:
				k=0
				while(dicti_scenes2[keys][k]==None):
					k=k+1
				while(j<k):
					dicti_scenes2[keys][j]=dicti_scenes2[keys][k]
					j=j+1
				j=j-1
			else :
				k=j
				while(dicti_scenes2[keys][k]==None):
					k=k-1
				temp=dicti_scenes2[keys][k]
				k=j
				while(dicti_scenes2[keys][k]==None):
					k=k+1
				temp=torch.add(temp, dicti_scenes2[keys][k])
				temp=torch.divide(temp, 2)
				while(j<k):
					dicti_scenes2[keys][j]=temp
					j=j+1
				j=j-1
		j=j+1
	i=i+1

data_reco=dicti_scenes2

#requete scenes critere
data_requete=data_reco

#order
dict1={}
i=0
print("data_requete")
print(len(data_requete))
keys=list(data_requete.keys())
while(i<len(data_requete)):
	print(i)
	dict1[keys[i]]=[]
	j=0
	while(j<len(data_reco)):
		value=0
		mini=min(len(data_requete[keys[i]]), len(data_reco[keys[j]]))
		k=0
		while(k<mini):
			l=0
			while(l<len(data_requete[keys[i]][k])):
				value=value+(data_requete[keys[i]][k][l]-data_reco[keys[j]][k][l])**2
				l=l+1
			k=k+1
		dict1[keys[i]].append(math.sqrt(value))
		j=j+1
	i=i+1

dicti_names={}
dicti_order={}
keys=list(data_requete.keys())
print(dict1)
order_video={}
i=0
while(i<len(keys)):
	j=0
	order_video[keys[i]]=[]
	dicti_names[keys[i]]=[]
	dist2=copy.deepcopy(dict1[keys[i]])
	while(len(dict1[keys[i]])!=len(order_video[keys[i]])):
		mini=min(dist2)
		order_video[keys[i]].append(dict1[keys[i]].index(mini))
		dicti_names[keys[i]].append(keys[dict1[keys[i]].index(mini)])
		dict1[keys[i]][dict1[keys[i]].index(mini)]=1000
		del dist2[dist2.index(mini)]
		j=j+1
	i=i+1
i=0

videos=modele_client.find_all_videos(100, 0)
videos=videos.json()
i=0
while(i<len(videos)):
	if '_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1])=="La_reine_des_neiges":
		if int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==3 or int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==5 or int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==7:
			videos[i]["Path"]="Frozen"+"_video"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
		else : 
			videos[i]["Path"]="Frozen"+"_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
	elif '_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1])=="La_planete_au_tresor":
		if int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==2 or int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==5:
			videos[i]["Path"]="planete_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
		else :
			videos[i]["Path"]="planete_video"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
	elif '_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1])=="Mulan":
		if int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==8 or int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==9:
			videos[i]["Path"]="mulan_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
		else :
			videos[i]["Path"]="mulan_video"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
	elif '_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1])=="Pocahontas" :
		if int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==6:
			videos[i]["Path"]="pocahontas_video"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
		elif int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==7:
			videos[i]["Path"]="pocahontas_scene30"
		else :
			videos[i]["Path"]="pocahontas_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
	elif '_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1])=="Rebelle" :
		if int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==6 or int(videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0])==5:
			videos[i]["Path"]="rebelle_scene3"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]		
		else :
			videos[i]["Path"]="rebelle_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]		
	elif  '_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1])=="Vaiana" :
		videos[i]["Path"]="vaiana_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
	elif  '_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1])=="ViceVersa": 
		videos[i]["Path"]="viceversa_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
		print(videos[i]["Path"])
	else :	
		print('_'.join(videos[i]["Path"].split("/")[-1].split("_")[0:-1]))
		videos[i]["Path"]="zootopie_scene"+videos[i]["Path"].split("/")[-1].split("_")[-1].split(".")[0]
		print(videos[i]["Path"])
	i=i+1


user=modele_client.get_user("lambda")
user=user.json()
i=0
while(i<len(keys)):
	list_orders=dicti_names[keys[i]]
	j=0
	data=[]
	while(j<len(list_orders)):
		if list_orders[j]!=keys[i]:
			k=0
			while(k<len(videos)):
				if videos[k]["Path"]==list_orders[j]:
					v_reco=videos[k]
				if videos[k]["Path"]==keys[i]:
					v_ref=videos[k]
				k=k+1
			modele_client.init_reco_video(v_ref["id_video"],v_reco["id_video"],user["id_user"], j, 0)
		j=j+1
	i=i+1
print(len(data))
#['Frozen_scene1', 'vaiana_scene5', 'mulan_scene9', 'vaiana_scene3', 'pocahontas_video6', 'mulan_video3', 'zootopie_scene8', 'vaiana_scene1', 'mulan_video2', 'viceversa_scene6', 'rebelle_scene36', 'planete_video4', 'viceversa_scene8', 'viceversa_scene3', 'vaiana_scene4', 'vaiana_scene7', 'zootopie_scene9', 'zootopie_scene3', 'zootopie_scene7', 'planete_scene2', 'vaiana_scene6', 'mulan_video4', 'mulan_video7', 'mulan_scene8', 'pocahontas_scene5', 'viceversa_scene2', 'rebelle_scene7', 'mulan_video1', 'pocahontas_scene2', 'viceversa_scene4', 'pocahontas_scene4', 'planete_video6', 'vaiana_scene2', 'planete_video1', 'Frozen_video5', 'zootopie_scene5', 'zootopie_scene4', 'zootopie_scene1', 'planete_video3', 'mulan_video5', 'zootopie_scene2', 'rebelle_scene3', 'vaiana_scene8', 'pocahontas_scene3', 'rebelle_scene4', 'planete_video7', 'rebelle_scene1', 'Frozen_scene2', 'mulan_video6', 'rebelle_scene2', 'viceversa_scene7', 'planete_scene5', 'Frozen_scene6', 'zootopie_scene6', 'Frozen_video7', 'Frozen_video3', 'viceversa_scene1', 'pocahontas_scene30', 'Frozen_scene4', 'rebelle_scene35', 'pocahontas_scene1', 'viceversa_scene5']
#vaiana_scene5, rang 1
#mulan_scene9, rang 2
#vaiana_scene3, rang 3

