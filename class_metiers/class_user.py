class User:
  def __init__(self, id_user, login, age, genre):
  	self.id_user=id_user
  	self.login=login
  	self.age=age
  	self.genre=genre
  	self.video_notees={}
  def set_video_notee(video_ref, video_reco, note, rank):
  	self.video_notees[video_ref.title]={}
  	self.video_notees[video_ref.title][video_reco.title]=(note, rank)
  def get_note_of_one_recommendation(video_ref, video_reco):
  	return self.video_notees[video_ref.title][video_reco.title][0]




