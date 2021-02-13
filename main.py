from pytube import YouTube
import srt
import datetime
from moviepy.editor import VideoFileClip


myVideo = YouTube('https://www.youtube.com/watch?v=_L3gNaAVjQ4&ab_channel=LexFridman')
print(myVideo)

caption=myVideo.captions.get_by_language_code('en')
caption.xml_captions
print(caption.generate_srt_captions())

#Create a file with subtitles

with open("caption.srt",'w')as f:
    f.write(caption.generate_srt_captions())
print("File Created!")

cp = srt.parse(caption.generate_srt_captions())
captionCC = list(cp)

CCPointList = []
for i in range(len(captionCC)):

    if captionCC[i].content.startswith("what") or captionCC[i].content.startswith("george"):
        CCPointList.append(i)
        print(captionCC[i].content)
        print(captionCC[i].start)

print(CCPointList)

filename = "Podcast1.mp4"
n = 0
for j in range(len(CCPointList)):
    lastNumber = CCPointList[-1]
    n += 1
    if CCPointList[j] >= 0 and CCPointList[j] != lastNumber:
        starttime = srt.timedelta_to_srt_timestamp(captionCC[CCPointList[j]].start)
        endtime = srt.timedelta_to_srt_timestamp(captionCC[CCPointList[j + 1]].start)
        clip = VideoFileClip(filename).subclip(starttime, endtime)
        clip.write_videofile(f"clip{n}.mp4")
        clip.close()

    elif CCPointList[j] == CCPointList[-1]:
        starttime = srt.timedelta_to_srt_timestamp(captionCC[CCPointList[j]].start)
        endtime = srt.timedelta_to_srt_timestamp(captionCC[-1].end)
        clip1 = VideoFileClip(filename).subclip(starttime, endtime)
        clip1.write_videofile(f"clip{n}.mp4")
        clip1.close()
