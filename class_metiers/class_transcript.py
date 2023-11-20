class Transcript:
  def __init__(self, id_transcript, id_video, num_dialogue,text, begin_utterance, end_utterance):
    self.id_transcript=id_transcript
    self.id_video=id_video
    self.num_dialogue=num_dialogue
    self.text = text
    self.emotions=[]
    self.labels=[]
    self.begin_utterance=begin_utterance
    self.end_utterance=end_utterance
  def set_emotions(self, emotions):
  	self.emotions=emotions
  def set_labels(self, emotions):
    self.labels=emotions
  def get_num_dialogue():
    return self.num_dialogue
  def get_begin_utterance():
    return self.begin_utterance
  def get_end_utterance():
    return self.end_utterance


