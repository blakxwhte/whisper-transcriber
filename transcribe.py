import whisper
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from pytube import YouTube
import tempfile

def load_whisper_model(model_size="base"):
    """Load the Whisper model."""
    print("Loading the Whisper model...")
    try:
        model = whisper.load_model(model_size)
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Failed to load the model: {e}")
        return None

def get_audio_file_path():
    """Prompt the user for the audio file path or YouTube link."""
    path_completer = PathCompleter()
    while True:
        user_input = prompt("Enter the path to the audio file or a YouTube link: ", completer=path_completer)
        if user_input.startswith(("http://", "https://")):
            # Assume it's a YouTube link
            return user_input
        elif os.path.isfile(user_input):
            # Assume it's a local file path
            return user_input
        else:
            print(f"Invalid input: '{user_input}'. Please try again.")

def download_youtube_audio(youtube_url):
    """Download the audio from a YouTube video and return the file path."""
    try:
        print("Downloading audio from YouTube...")
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            print("No audio stream found for this video.")
            return None

        # Save the audio to a temporary file
        temp_dir = tempfile.mkdtemp()
        audio_path = audio_stream.download(output_path=temp_dir, filename="youtube_audio")
        print(f"Audio downloaded to: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"Failed to download YouTube audio: {e}")
        return None

def transcribe_audio(audio_path, model):
    """Transcribe the audio file."""
    print(f"Starting transcription for '{audio_path}'...")
    result = model.transcribe(audio_path)
    return result["text"]

def format_transcription(transcription):
    """Format the transcription with line breaks after sentences."""
    return "\n".join(transcription.split(". "))

def save_transcription(transcription, file_path="transcription.txt"):
    """Save the formatted transcription to a text file."""
    try:
        with open(file_path, "w") as file:
            file.write(transcription)
        print(f"Formatted transcription saved to '{file_path}'.")
    except Exception as e:
        print(f"Failed to save transcription: {e}")

def main():
    # Load the Whisper model
    model = load_whisper_model("base")
    if not model:
        return

    # Get the audio file path or YouTube link
    user_input = get_audio_file_path()

    # Handle YouTube links
    if user_input.startswith(("http://", "https://")):
        audio_path = download_youtube_audio(user_input)
        if not audio_path:
            return
    else:
        audio_path = user_input

    # Transcribe the audio file
    transcription = transcribe_audio(audio_path, model)

    # Format the transcription
    formatted_transcription = format_transcription(transcription)

    # Print the formatted transcription
    print("\nFormatted Transcription:")
    print(formatted_transcription)

    # Save the formatted transcription to a text file
    save_transcription(formatted_transcription)

if __name__ == "__main__":
    main()