#!/usr/bin/python
import moviepy.editor as mpy
import moviepy.video.fx.all as vfx
from mutagen.mp3 import MP3
from gtts import gTTS 
import textwrap
import string
import sys

language = 'en'
VIDEO_SIZE = (1028, 640)
TEXT_FILE = './speech.txt' # Text file must be in ASCII format
BACKGROUND_IMAGE = 'epicurus.jpg' # Leave as '', if you want to have solid color background
BACKGROUND_IMAGE_POSITION = ('center','top') # Options: (See TEXT_POSITION. It's the same options)
BACKGROUND_IMAGE_RESIZE = (VIDEO_SIZE[0],VIDEO_SIZE[1]) # Examples: (460,720) <- New resolution, 0.6 <- width and heigth multiplied by 0.6
BACKGROUND_COLOR = (255, 255, 255)

TEXT_POSITION = ('center','center') # Options, for the x and y axes: <Integer for position in x or y axis>, 'center', 'top', 'bottom', 'left', 'right'
TEXT_COLUMN_WIDTH = 50
TEXT_ALIGN = 'West' # Options: West, Center, East
FONT_FAMILY = 'Xolonium-Bold'
FONT_COLOR = 'red'

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
audio_txt = filter(lambda x: x in printable, origin_txt)

# Create audio and get audio duration
myobj = gTTS(text=audio_txt, lang=language, slow=False) 
myobj.save("audio.mp3")
audio = mpy.AudioFileClip("audio.mp3")
duration = MP3("audio.mp3").info.length

# Create the Text clip
text = mpy.TextClip(txt,color=FONT_COLOR, align='West',fontsize=26,
                    font=FONT_FAMILY, method='label')

if len(BACKGROUND_IMAGE) > 0:
    bg = mpy.ImageClip(BACKGROUND_IMAGE)

# Scroll the text at the right speed
line_height = 30
txt_speed = float(line_height) * float(txt_height) / float(duration)

fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+VIDEO_SIZE[1],:]
moving_txt= text.fl(fl, apply_to=['mask'])

# Create the video clip
clip = mpy.CompositeVideoClip(
    [
        vfx.resize(bg.set_position(BACKGROUND_IMAGE_POSITION), BACKGROUND_IMAGE_RESIZE),
        moving_txt.set_position(TEXT_POSITION)
    ]
    if len(BACKGROUND_IMAGE) > 0 else
    [
        moving_txt.set_position(TEXT_POSITION)
    ],
    size=VIDEO_SIZE).\
    on_color(
        color=BACKGROUND_COLOR,
        col_opacity=1).set_duration(duration).set_audio(audio)

clip.write_videofile(OUTPUT_FILE, fps=10)
    #use_bgclip=True if len(BACKGROUND_IMAGE) > 0 else False,
