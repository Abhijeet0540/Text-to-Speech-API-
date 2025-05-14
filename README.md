# Text-to-Speech API 

This project provides a serverless API for text-to-speech conversion with human-like voice enhancements. It's built with Flask and gTTS (Google Text-to-Speech), designed to be deployed to Vercel, and can be easily integrated across multiple projects.

## Features

- Text-to-speech conversion with natural-sounding voices
- Multiple language options
- Emotion selection (friendly, professional, enthusiastic)
- Natural pauses and speech enhancements
- No audio files saved on server (streaming only)
- Easy to integrate with any website or application

## How It Works

The API uses Flask to create a lightweight web server that processes text-to-speech requests. When you send text to the `/api/stream-speech` endpoint, the service:

1. Enhances the text with natural pauses
2. Applies emotional tone adjustments based on your selection
3. Converts the text to speech using gTTS
4. Streams the audio directly to your application without storing files

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

To run the API locally:

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

## License

MIT

