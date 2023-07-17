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
		pass
	def find_all(self, number,page):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Video).where(Video.id_video>=number*page, Video.id_video<=number*(page+1))
		videos=[]
		for video in session.scalars(stmt):
			video=class_video.Video(video.id_video,video.Title, video.Path)
			videos.append(video)
		return videos
	def add_Video(self, title, path):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		with Session(engine) as session:
			video=Video(Title=title, Path=path)
			session.add(video)
			session.commit()
	def find_video_from_title(self, title):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Video).where(Video.Title==title)
		video=None
		for video in session.scalars(stmt):
			video=class_video.Video(video.id_video,video.Title, video.Path)
		return video
	def find_video_from_id(self, id_video):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Video).where(Video.id_video==id_video)
		video=None
		for video in session.scalars(stmt):
			video=class_video.Video(video.id_video,video.Title, video.Path)
		return video

	def find_video_from_path(self, path):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Video).where(Video.Path==path)
		video=None
		for video in session.scalars(stmt):
			video=class_video.Video(video.id_video,video.Title, video.Path)
		return video
	def find_transcripts(self,id_video, number, page):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		stmt = select(Transcript).where(Transcript.id_video==id_video, Transcript.id_transcript>=number*page, Transcript.id_transcript<=number*(page+1))
		transcripts=[]
		for transcript in session.scalars(stmt):
			transcript=class_transcript.Transcript(transcript.id_transcript,transcript.id_video, transcript.Num_dialogue, transcript.Text, transcript.begin_utterance, transcript.end_utterance)
			transcripts.append(transcript)
		return transcripts	
	def find_noted_videos(self, id_video_ref, page, number):
		engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
		session = Session(engine)
		notes_reco=[]
		stmt=select(videos_recommendation_user).where(videos_recommendation_user.id_video_ref==id_video_ref and videos_recommendation_user.id_video_reco>=page*number and videos_recommendation_user.id_video_reco<=number*(page+1) and videos_recommendation_user.note_recommendation!=-1)
		for noted_video in session.scalars(stmt) :
			video_ref=select(Video).where(Video.id_video==noted_video.id_video_ref)
			video_reco=select(Video).where(Video.id_video==noted_video.id_video_reco)
			rank=noted_video.Rank
			note=noted_video.note_recommendation
			for v in session.scalars(video_ref):
				video_ref=v
			for v in session.scalars(video_reco):
				video_reco=v
			note_reco=(video_ref, video_reco, rank, note)
			notes_reco.append(note_reco)
		return notes_reco



class Base(DeclarativeBase):
	pass
class Video(Base):
	__tablename__ = "Video"
	id_video :Mapped[int] = mapped_column(primary_key=True)
	Title : Mapped[str] = mapped_column(String(30))
	Path:Mapped[str] = mapped_column(String(150))
	def __repr__(self) -> str:
		return f"Video(id_video={self.id_video!r}, Title={self.Title!r}, Path={self.Path!r}"
class Transcript(Base):
	__tablename__ = "Transcript"
	id_transcript : Mapped[int] = mapped_column(primary_key=True)
	id_video: Mapped[int] = mapped_column(ForeignKey("Video.id_video"))
	Num_dialogue: Mapped[int] = mapped_column(Integer)
	Text :Mapped[str] = mapped_column(String(150))
	begin_utterance :Mapped[int] = mapped_column(Integer)
	end_utterance :Mapped[int] = mapped_column(Integer)
	def __repr__(self) -> str:
		return f"Transcript(id_transcript={self.id_transcript!r}, Num_dialogue={self.Num_dialogue!r},Text={self.Text!r})"
class videos_recommendation_user(Base):
    __tablename__ = "videos_recommendation_user"
    id_video_ref: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_video_reco: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id_user"), primary_key=True)
    Rank: Mapped[int] = mapped_column(Integer)
    note_recommendation: Mapped[int] = mapped_column(Integer)

