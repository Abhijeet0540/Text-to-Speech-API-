# Text-to-Speech API

This project provides a serverless API for text-to-speech conversion with human-like voice enhancements. It supports both gTTS (Google Text-to-Speech) and Coqui TTS (an open-source TTS system), designed to be deployed to Vercel or run locally, and can be easily integrated across multiple projects.

## Features

- Text-to-speech conversion with natural-sounding voices
- Multiple language options
- Emotion selection (friendly, professional, enthusiastic)
- Natural pauses and speech enhancements
- No audio files saved on server (streaming only)
- Easy to integrate with any website or application
- Option to use Coqui TTS for higher quality voices and offline usage

## How It Works

The API uses Flask to create a lightweight web server that processes text-to-speech requests. When you send text to the `/api/stream-speech` endpoint, the service:

### gTTS Implementation
1. Enhances the text with natural pauses
2. Applies emotional tone adjustments based on your selection
3. Converts the text to speech using gTTS
4. Streams the audio directly to your application without storing files

### Coqui TTS Implementation
1. Enhances the text with natural pauses
2. Applies emotional tone adjustments based on your selection
3. Converts the text to speech using Coqui TTS models
4. Streams the audio directly to your application without storing files
5. Provides higher quality, more natural-sounding voices

## API Usage

See [API_USAGE.md](API_USAGE.md) for detailed instructions on how to use the API in your projects.

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions on how to deploy this API to Vercel.

## Quick Start

1. Clone this repository
2. Deploy to Vercel
3. Use the API in your projects:

```javascript
async function speakText(text) {
  const response = await fetch('https://your-vercel-url.vercel.app/api/stream-speech', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      language: 'en',
      emotion: 'professional'
    }),
  });

  const audioBlob = await response.blob();
  const audioUrl = URL.createObjectURL(audioBlob);
  const audio = new Audio(audioUrl);
  audio.play();
}
```

## Local Development

### gTTS Implementation

To run the gTTS API locally:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```
   python test_tts_api.py
   ```

   Alternatively, on Windows, you can use the provided batch file:
   ```
   run_tts_api.bat
   ```

3. The API will be available at `http://localhost:5000`

### Coqui TTS Implementation

To run the Coqui TTS API locally:

1. Create and activate a virtual environment:
   ```
   python -m venv coqui_env
   # On Windows:
   coqui_env\Scripts\activate
   # On macOS/Linux:
   source coqui_env/bin/activate
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Coqui TTS:
   ```
   pip install TTS
   ```

   If you encounter build errors, try using pre-built wheels:
   ```
   # For Windows with Python 3.9
   pip install https://github.com/coqui-ai/TTS/releases/download/v0.8.0/TTS-0.8.0-py3-none-any.whl
   ```

   Or use Docker:
   ```
   docker pull ghcr.io/coqui-ai/tts
   docker run -it --rm -p 5002:5002 ghcr.io/coqui-ai/tts --model_name tts_models/en/ljspeech/tacotron2-DDC
   ```

4. Run the Coqui TTS server:
   ```
   python coqui_tts_alternative.py
   ```

5. The API will be available at `http://localhost:5000`

## License

MIT

