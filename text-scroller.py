import moviepy.editor as mpy
from mutagen.mp3 import MP3
from gtts import gTTS 
import textwrap

language = 'en'
BLUE = (59/255, 89/255, 152/255)
WHITE = (255, 255, 255)
VIDEO_SIZE = (640, 480)

f = open("speech.txt","r")
audio_txt = f.read()

txt = "\n".join(textwrap.wrap(audio_txt,10))
# Add blanks
txt = 10*"\n" +txt + 10*"\n"


# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=audio_txt, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  
myobj.save("audio.mp3") 
audio = mpy.AudioFileClip("audio.mp3")
duration = MP3("audio.mp3").info.length


#text = mpy.VideoClip(render_text, duration=10)
text = mpy.TextClip(txt,color='black', align='West',fontsize=25,
                    font='Xolonium-Bold', method='label')


txt_speed = 27
fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+VIDEO_SIZE[1],:]
moving_txt= text.fl(fl, apply_to=['mask'])


clip = mpy.CompositeVideoClip(
    [
        moving_txt.set_position('center')
    ],
    size=VIDEO_SIZE).\
    on_color(
        color=WHITE,
        col_opacity=1).set_duration(duration).set_audio(audio)

clip.write_videofile('video_with_python.webm', fps=10)
