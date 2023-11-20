import torch
import optuna
from model_prediction import TransformerSentenceEncoderLayer, TransformerMultiEncoderLayer
import torch.optim as optim
from model_prediction import PositionalEmbeddingMul
import pandas as pd
from transformers import RobertaTokenizer, RobertaModel
features=[]
import random
import torch.nn.functional as Func
import modele_client

class TextAudioClassificationModel(torch.nn.Module):
	def __init__(self, num_classes, hidden_size, dropout, seq_length):
		super().__init__()
		self.SE_embeddings_a = torch.nn.Embedding(1, 768, padding_idx=None)
		self.padding_idx_a=1
		self.embed_positions_a = PositionalEmbeddingMul.PositionalEmbeddingMul(
			499,
			768,
			padding_idx=1,
			learned=True)
		self.layers_a = torch.nn.ModuleList( 
			[
			TransformerSentenceEncoderLayer.TransformerSentenceEncoderLayer(
				embedding_dim=768,
				ffn_embedding_dim=3072,
				num_attention_heads=8,
				dropout=0.1,
				attention_dropout=0.1,
				activation_dropout=0.1,
				activation_fn="relu",
				add_bias_kv=False,
				add_zero_attn=False,
				export=False,) for _ in range(6)
			]
		)
		self.layers_ta = torch.nn.ModuleList(
			[
			TransformerMultiEncoderLayer.TransformerMultiEncoderLayer(
				embedding_dim=768,
				qdim=768,
				kdim=768,
				vdim=768,
				self_attention=False,
				encoder_decoder_attention=True,
				ffn_embedding_dim=3072,
				num_attention_heads=8,
				dropout=0.1,
				attention_dropout=0.1,
				activation_dropout=0.1,
				activation_fn="relu",
				add_bias_kv=False,
				add_zero_attn=False,
				export=False,) for _ in range(6)
			]
		)
		self.layers_at = torch.nn.ModuleList(
			[
			TransformerMultiEncoderLayer.TransformerMultiEncoderLayer(
				embedding_dim=768,
				qdim=768,
				kdim=768,
				vdim=768,
				self_attention=False,
				encoder_decoder_attention=True,
				ffn_embedding_dim=3072,
				num_attention_heads=8,
				dropout=0.1,
				attention_dropout=0.1,
				activation_dropout=0.1,
				activation_fn="relu",
				add_bias_kv=False,
				add_zero_attn=False,
				export=False,) for _ in range(6)
			]
		)
		self.lstm = torch.nn.LSTM(input_size=1536, hidden_size=50, batch_first=True, bidirectional=True) 
		self.linear=torch.nn.Linear(1536,512)
		self.relu=torch.nn.ReLU()
		self.linear2=torch.nn.Linear(512,170)
		self.linear3=torch.nn.Linear(170,6)
	def forward(self, features_text, features_audio, bool_t, bool_a):
		x_a=features_audio
		x_t=features_text
		seq_rep={}
		if bool_a:
			x_a = Func.dropout(x_a, p=0.1, training=self.training)
			x_a = x_a.transpose(0, 1)
			for layer_a in self.layers_a:  #mask should be the key
				x_a,_=layer_a(x_a)
			j_aud_n=x_a[0, :, :]
			seq_rep.update({'j_aud' : j_aud_n})
		if bool_t :
			j_text=x_t[:, 0, :] #text embeddigs
			seq_rep.update({'j_text' : j_text})
		if (bool_a and bool_t):
			x_ta=x_t
			x_at=x_a
			x_ta=x_ta.transpose(0,1)
			for layer_ta in self.layers_ta:  #mask should be the key
				x_ta,_=layer_ta(x_ta,x_a,x_a)
			x_t=x_t.transpose(0,1)
			for layer_at in self.layers_at:
				x_at,_=layer_at(x_at,x_t,x_t)
			x_ta = x_ta.transpose(0, 1)
			x_at = x_at.transpose(0, 1)
			ta_rep = x_ta[:, 0, :]
			at_rep = x_at[:, 0, :]
			seq_rep.update({'t2a_r' : ta_rep})
			seq_rep.update({'a2t_r' : at_rep})
		if bool_t:
			cls_text=seq_rep['j_text']
			Final=cls_text
		if bool_t and bool_a :
			T_A=seq_rep['t2a_r']
			A_T=seq_rep['a2t_r']
			Final=torch.cat((T_A,A_T),dim=1)
		zeros=torch.zeros((Final.shape[0],1536-Final.shape[1]))
		Final=torch.cat((Final, zeros), dim=1)
		global features
		features=Final
		#out=self.lstm(Final)[0]
		out=self.linear(Final)
		out=self.relu(out)
		out=self.linear2(out)
		out=self.relu(out)
		out=self.linear3(out)
		return Final
def get_data_bool(audio, text,bool_a, bool_t, y, name):
	i=0
	audio_true=[]
	text_true=[]
	y_true=[]
	name_true=[]
	audio_false=[]
	text_false=[]
	y_false=[]
	name_false=[]
	while(i<len(audio)):
		if bool_a[i]==True :
			audio_true.append(audio[i])
			text_true.append(text[i])
			y_true.append(y[i])
			name_true.append(name[i])
		else :
			audio_false.append(audio[i])
			text_false.append(text[i])
			y_false.append(y[i])
			name_false.append(name[i])
		i=i+1
	return audio_true, text_true, y_true, name_true,audio_false, text_false, y_false, name_false
def get_batches(audio_true, text_true, y_true,name_true,audio_false, text_false, y_false,name_false, batch_size):	
	batches_true=[]
	batches_false=[]
	batch_size_true=batch_size
	batch_size_false=batch_size
	while len(audio_true)!=0:
		if batch_size_true>len(audio_true):
			batch_size_true=len(audio_true)
		j=0
		batch={}
		batch["features_audio"]=[]
		batch["features_text"]=[]
		batch["y"]=[]
		batch["name"]=[]
		batch["Audio"]=True
		batch["Text"]=True
		while(j<batch_size_true):
			rand=random.randint(0, len(audio_true)-1)
			batch["features_audio"].append(audio_true[rand])
			batch["features_text"].append(text_true[rand])
			batch["y"].append(y_true[rand])
			batch["name"].append(name_true[rand])
			del audio_true[rand]
			del text_true[rand]
			del y_true[rand]
			del name_true[rand]
			j=j+1
		batches_true.append(batch)
	while len(audio_false)!=0:
		if batch_size_false>len(audio_false):
			batch_size_false=len(audio_false)
		j=0
		batch={}
		batch["features_audio"]=[]
		batch["features_text"]=[]
		batch["y"]=[]
		batch["Audio"]=False
		batch["name"]=[]
		batch["Text"]=True
		while(j<batch_size_false):
			rand=random.randint(0, len(audio_false)-1)
			batch["features_audio"].append(audio_false[rand])
			batch["features_text"].append(text_false[rand])
			batch["y"].append(y_false[rand])
			batch["name"].append(name_false[rand])
			del audio_false[rand]
			del text_false[rand]
			del y_false[rand]
			del name_false[rand]
			j=j+1
		batches_false.append(batch)
	batches=[]
	i=0
	while(i<max(len(batches_true), len(batches_false))):
		if i<len(batches_true):
			batches.append(batches_true[i])
		if i<len(batches_false):
			batches.append(batches_false[i])
		i=i+1
	print("batches", len(batches))
	return batches

def structurelabel_binary(train):
	i=0
	y=[]
	cpt=[0,0,0,0,0,0]
	while(i<len(train)):
		em=train[i].split(", ")
		j=0
		y_em=[0,0,0,0,0,0]
		while(j<len(em)):
			if em[j]=="Joy" or em[j]=="joy":
				y_em[1]=1
				cpt[1]=cpt[1]+1
			elif em[j]=="Anger" or em[j]=="anger":
				y_em[0]=1
				cpt[0]=cpt[0]+1
			elif em[j]=="Sadness" or em[j]=="sadness":
				y_em[2]=1
				cpt[2]=cpt[2]+1
			elif em[j]=="Disgust" or em[j]=="disgust":
				y_em[3]=1
				cpt[3]=cpt[3]+1
			elif em[j]=="Fear" or em[j]=="fear":
				y_em[4]=1
				cpt[4]=cpt[4]+1
			elif em[j]=="Surprise" or em[j]=="surprise":
				y_em[5]=1
				cpt[5]=cpt[5]+1
			j=j+1
		y.append(y_em)
		i=i+1
	print("emotion",cpt)
	return y


def load_feats(video_file_name):
	file=pd.read_csv("transcription/emolis/"+video_file_name)
	
	bool_text=[]
	bool_audio=[]
	audio=[]
	text=[]
	y=[]
	maxi_audio=499
	maxi_text=120
	names=[]
	tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
	model = RobertaModel.from_pretrained("roberta-base")
	i=0
	while(i<len(file["Emotion"].values.tolist())):
		if i%100==0:
			print(i)
		name=video_file_name.split(".")[0]
		name=name.split("_")
		del name[0]
		name='_'.join(name)

		name=name+"_"+str(file["sr No."][i])
		print("ok utterance")
		print(file["Utterance"][i])
		try :
			inputs = tokenizer(file["Utterance"][i], return_tensors="pt")
			try :
				audio_temp=torch.load("audio_feats/"+name+".pt")
				audio.append(audio_temp)
				bool_audio.append(True)
			except :
				audio.append(torch.zeros((1,1, 768)))
				bool_audio.append(False)
			bool_text.append(True)
		except:
			inputs = tokenizer("", return_tensors="pt")
			bool_text.append(False)
			audio.append(torch.zeros((1,1, 768)))
			bool_audio.append(False)
		outputs = model(**inputs)
		last_hidden_states = outputs.last_hidden_state
		text.append(last_hidden_states[:, :, :].detach())
		names.append(name)
		y.append(file["Emotion"][i])
		

		
		i=i+1
	i=0
	print(len(text))
	print(len(audio))
	while(i<len(text)):
		zeros=torch.zeros((1,maxi_audio-audio[i].shape[1],768))
		if  len(audio[i].shape)==2:
			audio[i]=torch.stack(audio[i])
		if audio[i].shape[-1]==1 :
			audio[i]=torch.zeros((1, maxi_audio, 768))
		
		else :
			audio[i]=torch.cat((audio[i], zeros), dim=1)
		zeros=torch.zeros((1,maxi_text-text[i].shape[1],768))
		text[i]=torch.cat((text[i], zeros), dim=1)
		zeros=torch.zeros((1,1, 768))
		audio[i]=torch.cat((zeros, audio[i]), dim=1)
		i=i+1

	y=structurelabel_binary(y)
	return audio, text, y, bool_text,bool_audio, names
def objective(trial):
	params={'num_classes': trial.suggest_categorical('num_classes', [6]),
	'learning_rate': trial.suggest_categorical('learning_rate', [1e-3]),
	'batch_size': trial.suggest_categorical('batch_size', [8]),
	'epoch': trial.suggest_categorical('epoch', [300]),
	'hidden_size':trial.suggest_categorical('hidden_size', [60]),
	'dropout':trial.suggest_categorical('dropout', [0.2]),
	'seuil':trial.suggest_categorical('seuil', [0.5]),
	'seq_length':trial.suggest_categorical('seq_length', [120]),
	}


	model=TextAudioClassificationModel(params['num_classes'], params["hidden_size"], params["dropout"], params["seq_length"])
	optimizer = optim.Adam(model.parameters())
	checkpoint=torch.load("model_audio_text_3l.pt")
	model.load_state_dict(checkpoint['model_state_dict'], strict="False")
	optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
	epoch = checkpoint['epoch']
	loss = checkpoint['loss']
	model.eval()
	video_file="test_zootopie_scene6.csv"
	feats_audio, feats_text, y, bool_text,bool_audio,names=load_feats(video_file)
	feats_audio_true, feats_text_true, y_true,names_true, feats_audio_false, feats_text_false, y_false, names_false=get_data_bool(feats_audio, feats_text,bool_audio, bool_text,y, names)
	data=get_batches(feats_audio_true, feats_text_true, y_true,names_true,feats_audio_false, feats_text_false, y_false, names_false,params["batch_size"])
	i=0
	emo_scores=[]
	names_scores=[]
	labels_emotion_temp=[]
	while(i<len(data)):
		print(i)
		labels_emotion_temp.append(data[i]["y"])
		scores_data=model(torch.cat(data[i]["features_text"], axis=0), torch.cat(data[i]["features_audio"], axis=0), data[i]["Text"], data[i]["Audio"])
		if data[i]["Text"]==False and data[i]["Audio"]==False:
			scores_data=torch.FloatTensor(torch.FloatTensor([0,0,0,0,0,0]), torch.FloatTensor([0,0,0,0,0,0]), torch.FloatTensor([0,0,0,0,0,0]), torch.FloatTensor([0,0,0,0,0,0]), torch.FloatTensor([0,0,0,0,0,0]), torch.FloatTensor([0,0,0,0,0,0]), torch.FloatTensor([0,0,0,0,0,0]), torch.FloatTensor([0,0,0,0,0,0]))
		names=data[i]["name"]
		sigmoid=torch.nn.Sigmoid()
		scores_data=sigmoid(scores_data)
		j=0
		while(j<scores_data.shape[0]):
			k=0
			while(k<scores_data.shape[1]):
				if scores_data[j][k]>0.5:
					scores_data[j][k]=1
				else :
					scores_data[j][k]=0
				k=k+1
			j=j+1
		print(names)
		print(scores_data)
		emo_scores.append(scores_data)
		names_scores.append(names)
		i=i+1
		print("ok")
		
	print("fin")
	i=0
	emo_scores_total=[]
	emo_names_total=[]
	labels_emotion=[]
	while(i<len(names_scores)*params["batch_size"]):
		j=0
		while(j<len(emo_scores)):
			k=0
			while(k<emo_scores[j].shape[0]):
				if names_scores[j][k].split("_")[-1]==str(i):
					emo_scores_total.append(emo_scores[j][k])
					emo_names_total.append(names_scores[j][k])
					labels_emotion.append(labels_emotion_temp[j][k])
					break
				k=k+1
			j=j+1
		i=i+1
	i=0
	while(i<len(emo_names_total)):
		em=[]
		if emo_scores_total[i][0]==1:
			em.append("Colère")
		if emo_scores_total[i][1]==1:
			em.append("Joie")
		if emo_scores_total[i][2]==1:
			em.append("Tristesse")
		if emo_scores_total[i][3]==1:
			em.append("Dégoût")
		if emo_scores_total[i][4]==1:
			em.append("Peur")
		if emo_scores_total[i][5]==1:
			em.append("Surprise")
		if em==[]:
			em.append("Neutre")
		emo_scores_total[i]=em
		em=[]
		if labels_emotion[i][0]==1:
			em.append("Colère")
		if labels_emotion[i][1]==1:
			em.append("Joie")
		if labels_emotion[i][2]==1:
			em.append("Tristesse")
		if labels_emotion[i][3]==1:
			em.append("Dégoût")
		if labels_emotion[i][4]==1:
			em.append("Peur")
		if labels_emotion[i][5]==1:
			em.append("Surprise")
		if em==[]:
			em.append("Neutre")
		labels_emotion[i]=em
		print(emo_scores_total[i])
		print(labels_emotion[i])
		i=i+1
	"""
	modele_client.create_emotion("Colère")
	modele_client.create_emotion("Joie")
	modele_client.create_emotion("Tristesse")
	modele_client.create_emotion("Dégoût")
	modele_client.create_emotion("Peur")
	modele_client.create_emotion("Surprise")
	modele_client.create_emotion("Neutre")
	"""
	title="Zootopie - Retour à l'état sauvage !"
	modele_client.create_video(title,"video/Zootopie_6.mp4")
	dialogues=pd.read_csv("transcription/emolis/"+video_file)
	i=0
	while(i<len(emo_scores_total)):
		begin=int(dialogues["StartTime"][i].split(":")[0])*3600+int(dialogues["StartTime"][i].split(":")[1])*60+int(dialogues["StartTime"][i].split(":")[2].split(",")[0])
		end=int(dialogues["EndTime"][i].split(":")[0])*3600+int(dialogues["EndTime"][i].split(":")[1])*60+int(dialogues["EndTime"][i].split(":")[2].split(",")[0])
		modele_client.create_transcript(title, str(i),dialogues["Utterance"][i],begin,end, emo_scores_total[i], labels_emotion[i])
		if begin>end :
			print("error")
			print(begin)
			print(end)
		i=i+1
	return 0

study = optuna.create_study()
study.optimize(objective, n_trials=1)
