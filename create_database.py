
import sqlalchemy
from sqlalchemy import create_engine
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy import Column


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)



class Base(DeclarativeBase):
	pass

class User(Base):
	__tablename__ = "User"
	id_user: Mapped[int] = mapped_column(primary_key=True)
	login: Mapped[str] = mapped_column(String(50))
	age: Mapped[int] = mapped_column(Integer)
	genre : Mapped[str] = mapped_column(String(50))
	videos_notees: Mapped[List["Video"]] = relationship(back_populates="Video")
	def __repr__(self) -> str:
		return f"User(id_user={self.id_user!r}, login={self.login!r}, age={self.age!r}, genre={self.genre!r})"




class Video(Base):
	__tablename__ = "Video"
	id_video :Mapped[int] = mapped_column(primary_key=True)
	Title : Mapped[str] = mapped_column(String(30))
	Dialogues: Mapped[List["Transcript"]] = relationship(back_populates="Video", cascade="all, delete-orphan")
	def __repr__(self) -> str:
		return f"Video(id_video={self.id_video!r}, Title={self.Title!r}"


association_table_transcript_emotion = Table(
    "Transcript_emotion",
    Base.metadata,
    Column("Transcript", ForeignKey("Transcript.id_transcript")),
    Column("Emotion", ForeignKey("Emotion.id_emotion")),
)


class videos_recommendation_user(Base):
    __tablename__ = "videos_recommendation_user"
    id_video_ref: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_video_reco: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id_user"), primary_key=True)
    Rank: Mapped[int] = mapped_column(Integer)
    note_recommendation: Mapped[int] = mapped_column(Integer)
    video: Mapped["Video"] = relationship()






class Transcript(Base):
	__tablename__ = "Transcript"
	id_transcript : Mapped[int] = mapped_column(primary_key=True)
	id_video: Mapped[int] = mapped_column(ForeignKey("Video.id_video"))
	Num_dialogue: Mapped[int] = mapped_column(Integer)
	Text :Mapped[str] = mapped_column(String(150))
	video: Mapped["Video"] = relationship(back_populates="Transcript")
	Emotions: Mapped[List["Emotion"]] = relationship(secondary=association_table_transcript_emotion)
	def __repr__(self) -> str:
		return f"Transcript(id_transcript={self.id_transcript!r}, Num_dialogue={self.Num_dialogue!r},Text={self.Text!r}"


class Emotion(Base):
	__tablename__ = "Emotion"
	id_emotion :Mapped[int] = mapped_column(primary_key=True)
	Name :Mapped[str] = mapped_column(String(10))
	def __repr__(self) -> str:
		return f"Emotion(id_emotion={self.id_emotion!r}, Name={self.Name!r}"








Base.metadata.create_all(engine)



