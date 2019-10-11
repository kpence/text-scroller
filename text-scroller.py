import moviepy.editor as mpy
from mutagen.mp3 import MP3
from gtts import gTTS 
import textwrap
import string

language = 'en'
WHITE = (255, 255, 255)
VIDEO_SIZE = (1028, 640)

f = open("speech.txt","r")
origin_txt = f.read()

wrapper = textwrap.TextWrapper()
wrapper.width = 50
txt_height = -1
txt = ''
for pg in origin_txt.splitlines():
    pg_wrap = wrapper.wrap(pg)
    txt += "\n" + "\n".join(pg_wrap)
txt_height = txt.count('\n')
txt = 10*"\n" +txt + 10*"\n"

printable = set(string.printable)
audio_txt = [filter(lambda x: x in printable, origin_txt)]

audio_clips = []
duration = 0

for i in range(len(audio_txt)):
    myobj = gTTS(text=audio_txt[i], lang=language, slow=False) 
    myobj.save("audio"+str(i)+".mp3")
    audio_clips.append(mpy.AudioFileClip("audio"+str(i)+".mp3"))
    duration += MP3("audio"+str(i)+".mp3").info.length

audio = mpy.concatenate_audioclips(audio_clips)



text = mpy.TextClip(txt,color='black', align='West',fontsize=26,
                    font='Xolonium-Bold', method='label')


# duration per line
line_height = 30
txt_speed = float(line_height) * float(txt_height) / float(duration)
print(txt_speed)

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

print(txt_height)
print(txt)
clip.write_videofile('video_with_python.webm', fps=10)
