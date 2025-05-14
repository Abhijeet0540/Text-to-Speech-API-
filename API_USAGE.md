# TTS API Usage Guide

This guide explains how to use the Text-to-Speech API in your projects.

## API Endpoint

Once deployed, your API will be available at:

```
https://your-vercel-url.vercel.app/api/stream-speech
```

## Making API Requests

### Request Format

Send a POST request with a JSON body containing:

```json
{
  "text": "The text you want to convert to speech",
  "language": "en",
  "slow": false,
  "emotion": "professional"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | The text to convert to speech |
| `language` | string | No | Language code (default: "en") |
| `slow` | boolean | No | Whether to speak slowly (default: false) |
| `emotion` | string | No | Emotion style: "neutral", "friendly", "professional", or "enthusiastic" (default: "neutral") |

### Available Languages

| Code | Language |
|------|----------|
| `en` | English (US) |
| `en-uk` | English (UK) |
| `en-au` | English (Australia) |
| `en-in` | English (India) |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `it` | Italian |
| `ja` | Japanese |
| `ko` | Korean |
| `zh-CN` | Chinese (Simplified) |

### Response

The API returns an audio stream with MIME type `audio/mpeg`.

## Integration Examples

### JavaScript/HTML

```javascript
async function speakText(text) {
  try {
    const response = await fetch('https://your-vercel-url.vercel.app/api/stream-speech', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        language: 'en',
        emotion: 'professional',
        slow: false
      }),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    
    // Play the audio
    audio.play();
    
    // Clean up the URL when done
    audio.onended = () => {
      URL.revokeObjectURL(audioUrl);
    };
  } catch (error) {
    console.error('Error:', error);
  }
}

// Example usage
document.getElementById('speak-button').addEventListener('click', () => {
  const text = document.getElementById('question-text').textContent;
  speakText(text);
});
```

### React

```jsx
import React, { useState } from 'react';

function TextToSpeech() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [text, setText] = useState('');
  
  const speakText = async () => {
    if (!text) return;
    
    setIsPlaying(true);
    
    try {
      const response = await fetch('https://your-vercel-url.vercel.app/api/stream-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          language: 'en',
          emotion: 'professional'
        }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      audio.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
      
      audio.play();
    } catch (error) {
      console.error('Error:', error);
      setIsPlaying(false);
    }
  };
  
  return (
    <div>
      <textarea 
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to speak"
        rows={4}
        cols={50}
      />
      <button 
        onClick={speakText}
        disabled={isPlaying || !text}
      >
        {isPlaying ? 'Speaking...' : 'Speak'}
      </button>
    </div>
  );
}

export default TextToSpeech;
```

### Python

```python
import requests
import io
from pydub import AudioSegment
from pydub.playback import play

def speak_text(text, language='en', emotion='neutral'):
    url = 'https://your-vercel-url.vercel.app/api/stream-speech'
    
    data = {
        'text': text,
        'language': language,
        'emotion': emotion
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        # Convert the response content to an audio segment
        audio_data = io.BytesIO(response.content)
        audio_segment = AudioSegment.from_mp3(audio_data)
        
        # Play the audio
        play(audio_segment)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Example usage
speak_text("Hello, this is a test of the TTS API.", emotion="friendly")
```

## Error Handling

The API may return the following error responses:

- **400 Bad Request**: Missing required parameters
- **500 Internal Server Error**: Server-side error

Always implement proper error handling in your code to handle these cases.

## Rate Limiting

Be aware that Vercel's free tier has certain limitations:
- 100 GB bandwidth per month
- 10 second execution timeout for serverless functions

For high-volume usage, consider upgrading to a paid plan or hosting the service on your own server.

## CORS Support

The API has CORS enabled, so you can call it from any domain. If you need to restrict access, modify the CORS settings in the `api/index.py` file.
