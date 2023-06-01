## Guess Song From Lyrical Soundtrack
This is a fun script for guessing the lyrical soundtrack from Youtube

### Story
Watching a Youtube video and a soundtrack catches your mood by chance. However, you dont understand the language, cant get the lyrics and unable to look up for the song

### Requirements
You need to have the google api key and openai api key. Detail instructions can be found [how to get google api key](https://blog.hubspot.com/website/how-to-get-youtube-api-key) and [how to get openai api key](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)

### Installation & Run
- Installation: `pip install -r requirements.txt`
- Run: `python main.py`

### Configuration
You have to configure the file `info.json`, in which:
- `link`: link of the Youtube video, in which you hear the soundtrack
- `start`: starting timestamp of the soundtrack
- `end`: ending timestamp of the soundtrack

### Demo
For the following information
```
{
  "link": "https://www.youtube.com/watch?v=CjxugyZCfuw",
  "start": "0:00",
  "end": "0:21"
}
```

Result
```
[Lyrics]:
I am not a stranger to the dark. Hide away, they say. Cause we don't want your broken parts. I learned to be ashamed of all I saw.

[Guesses]:
- The song is called "This Is Me" from the movie The Greatest Showman.
- The name of the song is "This Is Me" from the musical film "The Greatest Showman".
- The song is "This Is Me" from the movie The Greatest Showman.
- The name of the song is "This Is Me" from the movie The Greatest Showman.
- The song is "This Is Me" from the musical film The Greatest Showman.

[Info]:
song: This Is Me - The Greatest Showman {LYRICS}, link: https://www.youtube.com/watch?v=5J29YsEfYlo
```
