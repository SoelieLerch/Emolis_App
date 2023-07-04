from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import select
from class_metiers import class_emotion


class EmotionDAO:
	def __init__(self):
		self.id_emotion=0
		self.name=""
	def add_Emotion(self, name):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			emotion=Emotion(Name=name)
			session.add(emotion)
			session.commit()


class Base(DeclarativeBase):
	pass
class Emotion(Base):
	__tablename__ = "Emotion"
	id_emotion :Mapped[int] = mapped_column(primary_key=True)
	Name :Mapped[str] = mapped_column(String(10))
	def __repr__(self) -> str:
		return f"Emotion(id_emotion={self.id_emotion!r}, Name={self.Name!r}"


engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
with Session(engine) as session:
	session.query(Emotion).delete()
	session.commit()