from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from class_DAO import class_video_DAO
from class_metiers import class_video, class_transcript
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String




class TranscriptDAO :
	def __init__(self):
		self.id_transcript=0
		self.id_video=0
		self.text=""
		self.emotions=[]
	def add_Transcript_from_video(self, id_video, num_dialogue, text):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			transcript=Transcript(id_video=video.id_video, Num_dialogue=num_dialogue, Text=text)
			session.add(transcript)
			session.commit()

class Base(DeclarativeBase):
	pass

class Transcript(Base):
	__tablename__ = "Transcript"
	id_transcript : Mapped[int] = mapped_column(primary_key=True)
	id_video: Mapped[int] = mapped_column(ForeignKey("Video.id_video"))
	Num_dialogue: Mapped[int] = mapped_column(Integer)
	Text :Mapped[str] = mapped_column(String(150))
	def __repr__(self) -> str:
		return f"Transcript(id_transcript={self.id_transcript!r},id_video={self.id_video!r}, Num_dialogue={self.Num_dialogue!r},Text={self.Text!r})"
class Video(Base):
	__tablename__ = "Video"
	id_video :Mapped[int] = mapped_column(primary_key=True)
	Title : Mapped[str] = mapped_column(String(30))
	def __repr__(self) -> str:
		return f"Video(id_video={self.id_video!r}, Title={self.Title!r})"





