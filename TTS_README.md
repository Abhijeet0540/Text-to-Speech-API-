# Text-to-Speech Implementation

This repository contains a text-to-speech implementation using gTTS (Google Text-to-Speech) with enhanced natural-sounding voice capabilities.

## Features

- Text-to-speech conversion with natural-sounding voices
- Multiple language options
- Emotion selection (friendly, professional, enthusiastic)
- Natural pauses and speech enhancements
- No audio files saved on server (streaming option available)
- Easy to integrate with any website or application

## Implementation Options

This repository provides several implementation options:

1. **Simple CLI Tool** (`test_tts_cli.py`): Command-line interface for testing TTS functionality.
2. **Simple API** (`simple_tts_api.py`): Basic API for text-to-speech conversion.
3. **Web Interface** (`tts_web_interface.py`): Web interface for testing TTS functionality.
4. **Full API** (`test_gtts.py`): Complete API with web interface for text-to-speech conversion.

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

```bash
python test_tts_cli.py --text "Your text here" --emotion friendly --play
```

Options:
- `--text`: The text to convert to speech.
- `--output`: The output file path (default: output.mp3).
- `--language`: The language code (default: en).
- `--slow`: Whether to speak slowly.
- `--emotion`: The emotion to apply (neutral, friendly, professional, enthusiastic).
- `--play`: Whether to play the audio after generating it.

### Simple API

```python
from simple_tts_api import text_to_speech, text_to_speech_stream, text_to_speech_base64

# Convert text to speech and save to a file
text_to_speech("Your text here", output_file="output.mp3", emotion="friendly")

# Convert text to speech and get the audio data as bytes
audio_data = text_to_speech_stream("Your text here", emotion="professional")

# Convert text to speech and get the audio data as a base64-encoded string
base64_audio = text_to_speech_base64("Your text here", emotion="enthusiastic")
```

### Web Interface

```bash
python tts_web_interface.py
```

This will start a web server and open a browser window with a user interface for testing the TTS functionality.

### Full API

```bash
python test_gtts.py
```

This will start a web server with a complete API and web interface for text-to-speech conversion.

## API Endpoints

### `/api/stream-speech` (POST)

Convert text to speech and stream the audio.

Request body:
```json
{
  "text": "Your text here",
  "language": "en",
  "slow": false,
  "emotion": "friendly"
}
```

Response: Audio file (MP3)

## Emotion Types

The TTS implementation supports the following emotion types:

1. **Neutral**: No emotion applied.
2. **Friendly**: Adds friendly phrases and casual tone.
3. **Professional**: Makes language more formal and structured.
4. **Enthusiastic**: Adds emphasis and excitement.

## Language Support

The TTS implementation supports multiple languages, including:

- English (US, UK, Australia)
- Spanish
- French
- German
- Italian
- Japanese
- Korean
- Chinese (Mandarin)

## Integration with Other Projects

To integrate this TTS functionality with other projects:

1. Import the necessary functions from `simple_tts_api.py`.
2. Use the functions to convert text to speech.
3. Play the audio or save it to a file.

Example:

```python
from simple_tts_api import text_to_speech_stream

def speak_text(text, emotion="neutral"):
    audio_data = text_to_speech_stream(text, emotion=emotion)
    # Play the audio data
    # ...
```

## Future Improvements

- Add support for Coqui TTS for higher quality voices
- Add more emotion types
- Add more language support
- Add voice selection options
- Add pitch and speed control

## License

MIT
