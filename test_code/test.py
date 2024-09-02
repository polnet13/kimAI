from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_wav(r'C:\Users\prude\kimAI\rsc\sound\toong.wav')
play(sound)