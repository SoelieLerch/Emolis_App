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
from class_metiers import class_user, class_video
from class_DAO import class_video_DAO
from sqlalchemy import update

class User_DAO():
	def __init__(self):
		self.id_user=0
		self.login=""
		self.age=0
		self.genre=""
	def add_user(self, login, age, genre):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			user=User(login=login, age=age, genre=genre)
			session.add(user)
			session.commit()
	def find_user_from_name(self, login):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(User).where(User.login==login)
		for user in session.scalars(stmt):
			user=class_user.User(user.id_user, user.login, user.age, user.genre)
		return user
	def init_reco_video(self, id_video_ref, id_video_reco, id_user, rank):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			video_reco=videos_recommendation_user(id_video_ref=id_video_ref, id_video_reco=id_video_reco, id_user=id_user, Rank=rank, note_recommendation=-1)
			session.add(video_reco)
			session.commit()
	def note_reco_video(self, id_video_ref, id_video_reco, id_user, note):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			session.execute(update(videos_recommendation_user).where(videos_recommendation_user.id_video_ref==id_video_ref, videos_recommendation_user.id_video_reco==id_video_reco, videos_recommendation_user.id_user==id_user).values(note_recommendation=note))
			session.commit()

	def find_video_reco_from_rank(self, id_video_ref, id_user, rank):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(videos_recommendation_user).where(videos_recommendation_user.id_user==id_user, videos_recommendation_user.id_video_ref==id_video_ref, videos_recommendation_user.Rank==rank)
		for video_reco in session.scalars(stmt):
			video_reco = select(Video).where(Video.id_video==video_reco.id_video_reco)
			for video_reco in session.scalars(video_reco):
				video_reco=class_video.Video(video_reco.id_video, video_reco.Title)
		return video_reco
	def find_note_reco_from_user(self, id_video_ref, id_video_reco, id_user):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(videos_recommendation_user).where(videos_recommendation_user.id_user==id_user, videos_recommendation_user.id_video_ref==id_video_ref, videos_recommendation_user.id_video_reco==id_video_reco)
		for video_reco in session.scalars(stmt):
			note=video_reco.note_recommendation
		return note		



class Base(DeclarativeBase):
	pass
class User(Base):
	__tablename__ = "User"
	id_user: Mapped[int] = mapped_column(primary_key=True)
	login: Mapped[str] = mapped_column(String(50))
	age: Mapped[int] = mapped_column(Integer)
	genre : Mapped[str] = mapped_column(String(50))
	def __repr__(self) -> str:
		return f"User(id_user={self.id_user!r}, login={self.login!r}, age={self.age!r}, genre={self.genre!r})"

class Video(Base):
	__tablename__ = "Video"
	id_video :Mapped[int] = mapped_column(primary_key=True)
	Title : Mapped[str] = mapped_column(String(30))
	def __repr__(self) -> str:
		return f"Video(id_video={self.id_video!r}, Title={self.Title!r}"


class videos_recommendation_user(Base):
    __tablename__ = "videos_recommendation_user"
    id_video_ref: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_video_reco: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id_user"), primary_key=True)
    Rank: Mapped[int] = mapped_column(Integer)
    note_recommendation: Mapped[int] = mapped_column(Integer)

