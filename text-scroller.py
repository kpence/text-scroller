#!/usr/bin/python
import moviepy.editor as mpy
from mutagen.mp3 import MP3
from gtts import gTTS 
import textwrap
import string
import sys

language = 'en'
TEXT_FILE = './speech.txt' # Text file must be in ASCII format
BACKGROUND_COLOR = (255, 255, 255)
VIDEO_SIZE = (1028, 640)
TEXT_COLUMN_WIDTH = 50
FONT_FAMILY = 'Xolonium-Bold'
FONT_COLOR = 'black'
TEXT_ALIGN = 'West' # Options: West, Center, East
OUTPUT_FILE = 'video_with_python.webm'

# Open the text file    
f = open(TEXT_FILE,"r")
origin_txt = f.read()

# Wrap the text around
wrapper = textwrap.TextWrapper()
wrapper.width = TEXT_COLUMN_WIDTH
txt_height = -1
txt = ''
for pg in origin_txt.splitlines():
    pg_wrap = wrapper.wrap(pg)
    txt += "\n" + "\n".join(pg_wrap)
txt_height = txt.count('\n')
txt = 10*"\n" +txt + 10*"\n"

# Fix problems with ASCII code
printable = set(string.printable)
audio_txt = [filter(lambda x: x in printable, origin_txt)]

# Create audio and get audio duration
myobj = gTTS(text=audio_txt, lang=language, slow=False) 
myobj.save("audio.mp3")
audio.append(mpy.AudioFileClip("audio.mp3"))
duration = MP3("audio.mp3").info.length

# Create the Text clip
text = mpy.TextClip(txt,color=FONT_COLOR, align='West',fontsize=26,
                    font=FONT_FAMILY, method='label')

# Scroll the text at the right speed
line_height = 30
txt_speed = float(line_height) * float(txt_height) / float(duration)

fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+VIDEO_SIZE[1],:]
moving_txt= text.fl(fl, apply_to=['mask'])

# Create the video clip
clip = mpy.CompositeVideoClip(
    [
        moving_txt.set_position('center')
    ],
    size=VIDEO_SIZE).\
    on_color(
        color=BACKGROUND_COLOR
        col_opacity=1).set_duration(duration).set_audio(audio)

clip.write_videofile(OUTPUT_FILE, fps=10)
