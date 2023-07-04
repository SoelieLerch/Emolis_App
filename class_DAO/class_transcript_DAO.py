from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from class_DAO import class_video_DAO

class TranscriptDAO :
	def __init__(self):
		self.id_transcript=0
		self.id_video=0
		self.text=""
		self.emotions=[]
	def add_Transcript_from_video(video, text):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			transcript=Transcript(video.id_video, text)
			session.add(transcript)
			session.commit()


transcriptDAO=TranscriptDAO()
videoDAO=class_video_DAO.Video_DAO()
videoDAO.add_video("Frozen_1")
video=videoDAO.find_video_from_title("Frozen_1")
transcriptDAO.add_Transcript_from_video(video, "Hello, I love you")
video.dialogues=videoDAO.find_transcripts(video)
print(video.dialogues[0].transcripts)



