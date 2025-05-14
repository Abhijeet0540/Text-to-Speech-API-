# Text-to-Speech API 

This project provides a serverless API for text-to-speech conversion with human-like voice enhancements. It's designed to be deployed to Vercel and used across multiple projects.

## Features

- Text-to-speech conversion with natural-sounding voices
- Multiple language options
- Emotion selection (friendly, professional, enthusiastic)
- No audio files saved on server (streaming only)
- Easy to integrate with any website or application

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

## License

MIT
