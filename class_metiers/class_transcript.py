class Transcript:
  def __init__(self, id_transcript, id_video, num_dialogue,text):
  	self.id_transcript=id_transcript
  	self.id_video=id_video
  	self.num_dialogue=num_dialogue
  	self.text = text
  	self.emotions=[]
  def set_emotions(self, emotions):
  	self.emotions=emotions

