class User:
  def __init__(self, id_user, login, age, genre):
  	self.id_user=id_user
  	self.login=login
  	self.age=age
  	self.genre=genre
  	self.video_notees={}
  def set_video_notee(video_ref, video_reco, note, rang):
  	self.video_notees[video_ref.title]=(video_reco.title, note, rang)




