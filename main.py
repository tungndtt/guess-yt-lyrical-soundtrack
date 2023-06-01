import os
import json
import ffmpeg
import yt_dlp
import openai
import time
from googleapiclient.discovery import build


# clean up
def clean_up():
  print("cleaning up the audio files ...")
  for file in os.listdir("."):
    if file.endswith(".mp3"):
      os.remove(file)
  print("done")
  quit()


# download the audio from the video url
def download_audio(video_url):
  try:
    print(f"downloading audio from {video_url} ...")
    audio_file = "audio.mp3"
    with yt_dlp.YoutubeDL({"extract_audio": True, "format": "bestaudio", "outtmpl": audio_file, "quiet": True}) as video:
      video.download(video_url)
      return audio_file
  except Exception as error:
    print(f"[-] download_yt_audio: cannot extract audio from {video_url}: {error}")
    clean_up()


# cut the audio 
def trim_audio(audio_file, start, end):
  try:
    print(f"cutting audio from {start} to {end} ...")
    cut_audio_file = "cut_" + audio_file
    # load the audio file
    ffmpeg.input(audio_file, ss=start, to=end).output(cut_audio_file, acodec="libmp3lame", loglevel="panic").run()
    return cut_audio_file
  except Exception as error:
    print(f"[-] trim_audio: cannot cut audio from {audio_file}: {error}")
    clean_up()


# audio to text
def audio_to_text(cut_audio_file):
  try:
    print("detecting lyrics ...")
    with open(cut_audio_file, "rb") as audio_file:
      transcript = openai.Audio.transcribe("whisper-1", audio_file)
      lyrics = transcript["text"]
      return lyrics
  except Exception as error:
    print(f"[-] audio_to_text: cannot read audio from {cut_audio_file}: {error}")
    clean_up()


# ask chatgpt the song name
def make_guesses(lyric):
  print("making guess ...")
  question = f"What is name of the song with the following lyric? \n{lyric}"
  guesses = ""
  for _ in range(5):
    success = False
    while not success:
      try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "user", "content": question}],
          max_tokens=200,
        )
        guesses += "- " + response["choices"][0]["message"]["content"] + "\n"
        success = True
      except:
        time.sleep(4)
  return guesses


# find the song on youtube
def find_song(lyrics):
  print("looking up for song ...")
  api_key = os.environ.get("GOOGLE_API_KEY")
  if not api_key:
    print("[-] google api key is required to query youtube api")
    quit()
  youtube = build("youtube", "v3", developerKey=api_key)
  # Perform the search
  search_response = youtube.search().list(q=lyrics, part="snippet", type="video", maxResults=1).execute()
  # Process the search results
  results = search_response["items"]
  if len(results) == 0:
    return "cannot find the song with given lyrics"
  result = results[0]
  title = result["snippet"]["title"]
  link = "https://www.youtube.com/watch?v=" + result["id"]["videoId"]
  return f"song: {title}, link: {link}\n"


if __name__ == "__main__":
  with open("./info.json", "r") as f:
    # insert api key
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
      print("[-] You must have api key to access chatgpt api")
      quit()
    openai.api_key = openai_api_key

    # load information
    info = json.load(f)

    # download yt audio
    video_url = info["link"]
    audio_file = download_audio(video_url)

    # check whether cut timestamps are provided
    start, end = info["start"], info["end"]
    if start and end:
      # cut audio
      cut_audio_path = trim_audio(audio_file, start, end)

      # get the lyrics of the audio
      lyrics = audio_to_text(cut_audio_path)

      # make guesses for the song name
      guesses = make_guesses(lyrics)

      # look for the song
      song_info = find_song(lyrics)

      # return the lyrics and guesses 
      print(f"\n[Lyrics]:\n{lyrics}\n\n[Guesses]:\n{guesses}\n[Info]:\n{song_info}")
    else:
      print("[-] the start and end are required to cut the audio")

    # clean up
    clean_up()