
import assemblyai as aai

audio_url = "https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3"


aai.settings.api_key = "625058c65a9c4255af2179587a57e19a"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe(audio_url)
text = transcript.text
print(text)
print(transcript.word_search(words=["knee"])) # Timestamps are in MilliSeconds, 