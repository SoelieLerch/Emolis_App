
import modele_client
from server import app

#apres avoir appuyer sur ok de la vue view_lgoin
def create_user(name, age, genre, physio_bool):
	#si données non remplies, renvoyer un message d'erreur

	response=modele_client.create_user(name, age, genre, physio_bool)
	return response
	"""
	if response.status_code==201 :
		#tout s'est bien passé
	else :
		#dire login déjà créé ou age non entier
	#physio : calcul pour l'utilisateur des rang pour la physiologie
	#Si pas de physio, renvoyer, ok mais pas de physio
	#vue, rafraichis-toi -> affichage videos
	"""


def login_user(name):
	response=modele_client.get_user(name)
	return response
	#si données non remplies, renvoyer un message d'erreur
	"""
	if response.status_code==200:
		#tout s'est bien passé
	else :
		#user doens't exist
	#physio : calcul pour l'utilisateur des rang pour la physiologie
	#Si pas de physio, renvoyer, ok mais pas de physio
	#vue, raffraichis-toi -> affichage videos
	"""
def find_all_videos(number, page):
	response=modele_client.find_all_videos(number, page)
	return response
def download_picture(name):
	response=modele_client.download_picture(name)
	return response

def download_movie(name):
	response=modele_client.download_movie(name)
	return response

def find_transcripts(id_video,number, page):
	response=modele_client.get_transcripts(id_video, number, page)
	return response

def get_emotions(id_transcript):
	response=modele_client.get_emotions_from_transcript(id_transcript)
	return response

def get_labels(id_transcript):
	response=modele_client.get_labels_from_transcript(id_transcript)
	return response

def get_first_ranks(id_video, id_user, seuil):
	response=modele_client.find_video_reco_first_ranks(id_video, id_user, seuil)
	return response

def note(note, id_user, id_video_ref, id_video_reco, rank):
	response=modele_client.note_video_recommendation(id_video_ref,id_video_reco, id_user,rank, note)
	return response
