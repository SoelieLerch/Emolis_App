from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from class_metiers import class_video, class_transcript

class Video_DAO():
	def __init__(self):
		self.id_video=0
		self.Title=""
		self.dialogues=[]
	def find_all(self, number,page):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Video).where(Video.id_video>=number*page, Video.id_video<=number*(page+1))
		videos=[]
		for video in session.scalars(stmt):
			video=class_video.Video(video.id_video,video.Title)
			video.dialogues=find_transcripts(video)
			videos.append(video)
		return videos
	def add_Video(self, title):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			video=Video(Title=title)
			session.add(video)
			session.commit()
	def find_video_from_title(self, title):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Video).where(Video.Title==title)
		for video in session.scalars(stmt):
			video=class_video.Video(video.id_video,video.Title)
		return video
	def find_transcripts(self,id_video):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Transcript).where(Transcript.id_video==id_video)
		transcripts=[]
		for transcript in session.scalars(stmt):
			transcript=class_transcript.Transcript(transcript.id_transcript,transcript.id_video, transcript.id_transcript, transcript.Text)
			transcripts.append(transcript)
		return transcripts	




class Base(DeclarativeBase):
	pass
class Video(Base):
	__tablename__ = "Video"
	id_video :Mapped[int] = mapped_column(primary_key=True)
	Title : Mapped[str] = mapped_column(String(30))
	def __repr__(self) -> str:
		return f"Video(id_video={self.id_video!r}, Title={self.Title!r}"
class Transcript(Base):
	__tablename__ = "Transcript"
	id_transcript : Mapped[int] = mapped_column(primary_key=True)
	id_video: Mapped[int] = mapped_column(ForeignKey("Video.id_video"))
	Num_dialogue: Mapped[int] = mapped_column(Integer)
	Text :Mapped[str] = mapped_column(String(150))
	def __repr__(self) -> str:
		return f"Transcript(id_transcript={self.id_transcript!r}, Num_dialogue={self.Num_dialogue!r},Text={self.Text!r})"

