from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from class_DAO import class_video_DAO, class_emotion_DAO
from class_metiers import class_video, class_transcript, class_emotion
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String




class Transcript_DAO :
	def __init__(self):
		pass
	def add_Transcript_from_video(self, id_video, num_dialogue, text, begin_utterance, end_utterance):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		with Session(engine) as session:
			transcript=Transcript(id_video=id_video, Num_dialogue=num_dialogue, Text=text, begin_utterance=begin_utterance, end_utterance=end_utterance)
			session.add(transcript)
			session.commit()

	def find_all(self):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Transcript)
		transcripts=[]
		for transcript in session.scalars(stmt):
			transcript=class_transcript.Transcript(transcript.id_transcript,transcript.id_video, transcript.Num_dialogue, transcript.Text, transcript.begin_utterance, transcript.end_utterance)
			transcripts.append(transcript)
		return transcripts

	def get_emotions_from_transcript(self, id_transcript):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Transcript_emotion).where(Transcript_emotion.id_transcript==id_transcript)
		emotions=[]
		for transcript_emotion in session.scalars(stmt):
			stmt2=select(Emotion).where(Emotion.id_emotion==transcript_emotion.id_emotion)
			for emotion in session.scalars(stmt2):
				emotion=class_emotion.Emotion(emotion.id_emotion,emotion.Name)
				emotions.append(emotion)
		return emotions
	def get_labels_from_transcript(self, id_transcript):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Transcript_labels).where(Transcript_labels.id_transcript==id_transcript)
		emotions=[]
		for transcript_labels in session.scalars(stmt):
			stmt2=select(Emotion).where(Emotion.id_emotion==transcript_labels.id_labels)
			for emotion in session.scalars(stmt2):
				emotion=class_emotion.Emotion(emotion.id_emotion,emotion.Name)
				emotions.append(emotion)
		return emotions
	def add_emotions_to_transcript(self, id_video, num_dialogue, emotions, labels):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		i=0
		emotions_from_transcript=[]
		while(i<len(emotions)):
			stmt=select(Emotion).where(Emotion.Name==emotions[i])
			for emotion in session.scalars(stmt):
				emotion=class_emotion.Emotion(emotion.id_emotion, emotion.Name)
				emotions_from_transcript.append(emotion)
			i=i+1
		with Session(engine) as session:
			transcripts=select(Transcript).where(Transcript.id_video==id_video, Transcript.Num_dialogue==num_dialogue)
			for transcript in session.scalars(transcripts):
				i=0
				while(i<len(emotions_from_transcript)):
					emotion=Emotion(id_emotion=emotions_from_transcript[i].id_emotion,Name=emotions_from_transcript[i].name)
					transcript_emotion=Transcript_emotion(id_transcript=transcript.id_transcript, id_emotion=emotion.id_emotion)
					session.add(transcript_emotion)
					session.commit()
					i=i+1
				i=0
		labels_from_transcript=[]
		while(i<len(labels)):
			stmt=select(Emotion).where(Emotion.Name==labels[i])
			for emotion in session.scalars(stmt):
				emotion=class_emotion.Emotion(emotion.id_emotion, emotion.Name)
				labels_from_transcript.append(emotion)
			i=i+1
		with Session(engine) as session:
			transcripts=select(Transcript).where(Transcript.id_video==id_video, Transcript.Num_dialogue==num_dialogue)
			for transcript in session.scalars(transcripts):
				i=0
				while(i<len(labels_from_transcript)):
					emotion=Emotion(id_emotion=labels_from_transcript[i].id_emotion,Name=labels_from_transcript[i].name)
					transcript_labels=Transcript_labels(id_transcript=transcript.id_transcript, id_labels=emotion.id_emotion)
					session.add(transcript_labels)
					session.commit()
					i=i+1

				
class Base(DeclarativeBase):
	pass

class Transcript(Base):
	__tablename__ = "Transcript"
	id_transcript : Mapped[int] = mapped_column(primary_key=True)
	id_video: Mapped[int] = mapped_column(ForeignKey("Video.id_video"))
	Num_dialogue: Mapped[int] = mapped_column(Integer)
	Text :Mapped[str] = mapped_column(String(150))
	begin_utterance: Mapped[int]=mapped_column(Integer)
	end_utterance: Mapped[int]=mapped_column(Integer)
	def __repr__(self) -> str:
		return f"Transcript(id_transcript={self.id_transcript!r},id_video={self.id_video!r}, Num_dialogue={self.Num_dialogue!r},Text={self.Text!r})"
class Video(Base):
	__tablename__ = "Video"
	id_video :Mapped[int] = mapped_column(primary_key=True)
	Title : Mapped[str] = mapped_column(String(30))
	Path : Mapped[str] = mapped_column(String(150))
	def __repr__(self) -> str:
		return f"Video(id_video={self.id_video!r}, Title={self.Title!r}, Path={self.Path!r})"

class Emotion(Base):
	__tablename__ = "Emotion"
	id_emotion :Mapped[int] = mapped_column(primary_key=True)
	Name :Mapped[str] = mapped_column(String(10))
	def __repr__(self) -> str:
		return f"Emotion(id_emotion={self.id_emotion!r}, Name={self.Name!r}"

class Transcript_emotion(Base):
	__tablename__ = "Transcript_emotion"
	id_transcript: Mapped[int] = mapped_column(ForeignKey("Transcript.id_transcript"), primary_key=True)
	id_emotion: Mapped[int] = mapped_column(ForeignKey("Emotion.id_emotion"), primary_key=True)
	def __repr__(self) -> str:
		return f"Transcript_emotion(id_transcript={self.id_transcript!r},,id_emotion={self.id_emotion!r})"


class Transcript_labels(Base):
	__tablename__ = "Transcript_labels"
	id_transcript: Mapped[int] = mapped_column(ForeignKey("Transcript.id_transcript"), primary_key=True)
	id_labels: Mapped[int] = mapped_column(ForeignKey("Emotion.id_emotion"), primary_key=True)
	def __repr__(self) -> str:
		return f"Transcript_labels(id_transcript={self.id_transcript!r},,id_labels={self.id_labels!r})"

