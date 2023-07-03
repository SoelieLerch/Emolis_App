from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import select
from class_metiers import class_video

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
			videos.append(video)
		return videos
	def add_Video(self, title):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			video=Video(Title=title)
			session.add(video)
			session.commit()


class Base(DeclarativeBase):
	pass
class Video(Base):
	__tablename__ = "Video"
	id_video :Mapped[int] = mapped_column(primary_key=True)
	Title : Mapped[str] = mapped_column(String(30))
	def __repr__(self) -> str:
		return f"Video(id_video={self.id_video!r}, Title={self.Title!r}"


