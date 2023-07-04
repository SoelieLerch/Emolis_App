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
from class_metiers import class_user

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



