from sqlalchemy import delete
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
	pass
class videos_recommendation_user(Base):
    __tablename__ = "videos_recommendation_user"
    id_video_ref: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_video_reco: Mapped[int] = mapped_column(ForeignKey("Video.id_video"), primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id_user"), primary_key=True)
    Rank: Mapped[int] = mapped_column(Integer)
    note_recommendation: Mapped[int] = mapped_column(Integer)
engine = create_engine("sqlite+pysqlite:///emolis_database.sqlite", echo=True)
with Session(engine) as session:
	session.query(videos_recommendation_user).delete()
	session.commit()

