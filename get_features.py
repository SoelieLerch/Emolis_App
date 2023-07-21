import torch
import optuna
import model_prediction.TransformerSentenceEncoderLayer, model_prediction.TransformerMultiEncoderLayer
import torch.optim as optim
import model_prediction.PositionalEmbeddingMul
import pandas as pd
from transformers import RobertaTokenizer, RobertaModel
features=[]
import random
import torch.nn.functional as Func

class TextAudioClassificationModel(torch.nn.Module):
	def __init__(self, num_classes, hidden_size, dropout, seq_length):
		super().__init__()
		self.SE_embeddings_a = torch.nn.Embedding(1, 768, padding_idx=None)
		self.padding_idx_a=1
		self.embed_positions_a = model_prediction.PositionalEmbeddingMul.PositionalEmbeddingMul(
			499,
			768,
			padding_idx=1,
			learned=True)
		self.layers_a = torch.nn.ModuleList( 
			[
			model_prediction.TransformerSentenceEncoderLayer.TransformerSentenceEncoderLayer(
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
			model_prediction.TransformerMultiEncoderLayer.TransformerMultiEncoderLayer(
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
			model_prediction.TransformerMultiEncoderLayer.TransformerMultiEncoderLayer(
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
		return out, Final


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


def load_feats():
	train_file=pd.read_csv("transcription/train_emolis_meld.csv")
	dev_file=pd.read_csv("transcription/dev_emolis.csv")
	test_file=pd.read_csv("transcription/test_emolis.csv")
	bool_train_text=[]
	bool_train_audio=[]
	bool_dev_text=[]
	bool_dev_audio=[]
	bool_test_text=[]
	bool_test_audio=[]
	train_audio=[]
	dev_audio=[]
	test_audio=[]
	train_text=[]
	dev_text=[]
	test_text=[]
	y_train=[]
	y_dev=[]
	y_test=[]
	maxi_audio=0
	maxi_text=0
	train_names=[]
	dev_names=[]
	test_names=[]
	tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
	model = RobertaModel.from_pretrained("roberta-base")
	print(train_file)
	i=0
	while(i<len(train_file["Emotion"].values.tolist())):
		if i%100==0:
			print(i)
		name=train_file["Name"][i]
		if name[0:7]!="friends":
			name=name.split("_")
			name[-1]=str(train_file["Sr No."][i])
			name="_".join(name)
			try :
				inputs = tokenizer(train_file["Utterance"][i], return_tensors="pt")
				outputs = model(**inputs)
				last_hidden_states = outputs.last_hidden_state
				if last_hidden_states.shape[1]>maxi_text :
					maxi_text=last_hidden_states.shape[1]
				train_text.append(last_hidden_states[:, :, :].detach())
				train_names.append(name)
				y_train.append(train_file["Emotion"][i])
				bool_train_text.append(True)
				try :
					audio=torch.load("audio_feats/"+name+".pt")
					if audio.shape[1]>maxi_audio :
						maxi_audio=audio.shape[1]
					train_audio.append(audio)
					bool_train_audio.append(False)
				except :
					train_audio.append(torch.zeros((1,1, 768)))
					bool_train_audio.append(False)
			except :
				pass
		i=i+1
	i=0
	while(i<len(dev_file["Emotion"].values.tolist())):
		if i%100==0:
			print(i)
		name=dev_file["Name"][i]
		if name[0:7]!="friends":
			name=name.split("_")
			name[-1]=str(dev_file["Sr No."][i])
			name="_".join(name)
			try :
				inputs = tokenizer(dev_file["Utterance"][i], return_tensors="pt")
				outputs = model(**inputs)
				last_hidden_states = outputs.last_hidden_state
				if last_hidden_states.shape[1]>maxi_text :
					maxi_text=last_hidden_states.shape[1]
				dev_text.append(last_hidden_states[:, :, :].detach())
				dev_names.append(name)
				y_dev.append(dev_file["Emotion"][i])
				bool_dev_text.append(True)
				try :
					audio=torch.load("audio_feats/"+name+".pt")
					if audio.shape[1]>maxi_audio :
						maxi_audio=audio.shape[1]
					dev_audio.append(audio)
					bool_dev_audio.append(True)
				except :
					dev_audio.append(torch.zeros((1,1, 768)))
					bool_dev_audio.append(False)
			except :
				pass
		i=i+1
	i=0
	while(i<len(test_file["Emotion"].values.tolist())):
		if i%100==0:
			print(i)
		name=test_file["Name"][i]
		if name[0:7]!="friends":
			name=name.split("_")
			name[-1]=str(test_file["Sr No."][i])
			name="_".join(name)
			try :
				inputs = tokenizer(test_file["Utterance"][i], return_tensors="pt")
				outputs = model(**inputs)
				last_hidden_states = outputs.last_hidden_state
				if last_hidden_states.shape[1]>maxi_text :
					maxi_text=last_hidden_states.shape[1]
				test_text.append(last_hidden_states[:, :, :].detach())
				test_names.append(name)
				y_test.append(test_file["Emotion"][i])
				bool_test_text.append(True)
				try :
					audio=torch.load("audio_feats/"+name+".pt")
					if audio.shape[1]>maxi_audio :
						maxi_audio=audio.shape[1]
					test_audio.append(audio)
					bool_test_audio.append(True)
				except :
					test_audio.append(torch.zeros((1,1, 768)))
					bool_test_audio.append(False)
			except :
				pass
		i=i+1
	i=0
	while(i<len(train_text)):
		zeros=torch.zeros((1,maxi_audio-train_audio[i].shape[1],768))
		if  len(train_audio[i].shape)==2:
			train_audio[i]=torch.stack(train_audio[i])
		if train_audio[i].shape[-1]==1 :
			train_audio[i]=torch.zeros((1, maxi_audio, 768))
		
		else :
			train_audio[i]=torch.cat((train_audio[i], zeros), dim=1)
		zeros=torch.zeros((1,maxi_text-train_text[i].shape[1],768))
		train_text[i]=torch.cat((train_text[i], zeros), dim=1)
		zeros=torch.zeros((1,1, 768))
		train_text[i]=torch.cat((zeros, train_text[i]), dim=1)
		i=i+1

	i=0
	while(i<len(dev_text)):
		zeros=torch.zeros((1,maxi_audio-dev_audio[i].shape[1],768))
		if  len(dev_audio[i].shape)==2:
			dev_audio[i]=torch.stack(dev_audio[i])
		if dev_audio[i].shape[-1]==1 :
			dev_audio[i]=torch.zeros((1, maxi_audio, 768))
		else :
			dev_audio[i]=torch.cat((dev_audio[i], zeros), dim=1)
		zeros=torch.zeros((1,maxi_text-dev_text[i].shape[1],768))
		dev_text[i]=torch.cat((dev_text[i], zeros), dim=1)
		zeros=torch.zeros((1,1, 768))
		dev_text[i]=torch.cat((zeros, dev_text[i]), dim=1)
		i=i+1
	i=0
	while(i<len(test_text)):
		zeros=torch.zeros((1,maxi_audio-test_audio[i].shape[1],768))
		if  len(test_audio[i].shape)==2:
			test_audio[i]=torch.stack(test_audio[i])
		if test_audio[i].shape[-1]==1 :
			test_audio[i]=torch.zeros((1, maxi_audio, 768))
		else :
			test_audio[i]=torch.cat((test_audio[i], zeros), dim=1)
		zeros=torch.zeros((1,maxi_text-test_text[i].shape[1],768))
		test_text[i]=torch.cat((test_text[i], zeros), dim=1)
		zeros=torch.zeros((1,1, 768))
		test_text[i]=torch.cat((zeros, test_text[i]), dim=1)
		i=i+1
	y_train=structurelabel_binary(y_train)
	y_dev=structurelabel_binary(y_dev)
	y_test=structurelabel_binary(y_test)
	return train_audio, train_text, y_train, bool_train_text,bool_train_audio, train_names, dev_audio, dev_text, y_dev, bool_dev_text, bool_dev_audio, dev_names,test_audio, test_text, y_test,bool_test_text, bool_test_audio, test_names

def objective(trial):
	params={'num_classes': trial.suggest_categorical('num_classes', [6]),
	'learning_rate': trial.suggest_categorical('learning_rate', [1e-3]),
	'batch_size': trial.suggest_categorical('batch_size', [16]),
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
	train_audio, train_text, y_train, bool_train_text,bool_train_audio,train_names, dev_audio, dev_text, y_dev, bool_dev_text, bool_dev_audio,dev_names,test_audio, test_text, y_test, bool_test_text, bool_test_audio,test_names=load_feats()
	feats_audio=train_audio+dev_audio+test_audio
	print(len(feats_audio))
	feats_text=	train_text+dev_text+test_text
	y=y_train+y_dev+y_test
	bool_text=bool_train_text+bool_dev_text+bool_test_text
	bool_audio=bool_train_audio+bool_dev_audio+bool_test_audio
	names=train_names+dev_names+test_names
	print(len(names))
	feats_audio_true, feats_text_true, y_true,names_true, feats_audio_false, feats_text_false, y_false, names_false=get_data_bool(feats_audio, feats_text,bool_audio, bool_text,y, names)
	data=get_batches(feats_audio_true, feats_text_true, y_true,names_true,feats_audio_false, feats_text_false, y_false, names_false,params["batch_size"])
	i=0
	while(i<len(data)):
		print(i)
		scores_data, features=model(torch.cat(data[i]["features_text"], axis=0), torch.cat(data[i]["features_audio"], axis=0), data[i]["Text"], data[i]["Audio"])
		names=data[i]["name"]
		j=0
		while(j<features.shape[0]):
			torch.save(features[j], "total_features/"+names[j]+".pt")
			j=j+1

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

		print("ok")
		i=i+1
		
	print("fin")

study = optuna.create_study()
study.optimize(objective, n_trials=1)

