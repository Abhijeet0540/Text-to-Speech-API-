"""
Simple test script for gTTS (Google Text-to-Speech).
This script demonstrates how to use gTTS to convert text to speech.
"""

from flask import Flask, request, jsonify, Response
import io
import re
from gtts import gTTS
from flask_cors import CORS
import webbrowser
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def add_natural_pauses(text):
    """
    Enhance text with natural pauses to make speech sound more human-like.
    """
    # Add slight pauses after punctuation
    text = re.sub(r'([.!?])', r'\1 ', text)
    
    # Add commas for natural phrasing if there aren't enough already
    if text.count(',') < len(text) / 50:  # Roughly one comma per 50 chars
        # Add commas before conjunctions if not already present
        text = re.sub(r'([^\s,])(\s+)(and|but|or|because|however|therefore)(\s+)', r'\1,\2\3\4', text)
    
    # Add pauses for long sentences
    sentences = re.split(r'([.!?])', text)
    enhanced_sentences = []
    
    for i in range(0, len(sentences), 2):
        if i+1 < len(sentences):
            sentence = sentences[i] + sentences[i+1]
            # If sentence is long, add a pause in the middle
            if len(sentence) > 100:
                words = sentence.split()
                mid = len(words) // 2
                first_half = ' '.join(words[:mid])
                second_half = ' '.join(words[mid:])
                enhanced_sentences.append(f"{first_half}, {second_half}")
            else:
                enhanced_sentences.append(sentence)
        elif sentences[i].strip():
            enhanced_sentences.append(sentences[i])
    
    return ' '.join(enhanced_sentences)

def apply_emotion(text, emotion):
    """
    Modify text to convey different emotions through speech patterns.
    """
    if emotion == 'neutral':
        return text
        
    elif emotion == 'friendly':
        # Add friendly phrases and more casual tone
        greetings = ["Hi there! ", "Hello! ", "Great to meet you! "]
        endings = [" That's all for now!", " Thanks for listening!", " Hope that helps!"]
        
        # Add a greeting if the text doesn't already have one
        if not re.match(r'^(hi|hello|hey|greetings)', text.lower()):
            text = greetings[len(text) % len(greetings)] + text
            
        # Add an ending if the text doesn't already have one
        if not re.search(r'(thanks|thank you|cheers|goodbye|bye)[\s.!?]*$', text.lower()):
            text = text + endings[len(text) % len(endings)]
            
        # Add emphasis on positive words
        text = re.sub(r'\b(great|good|excellent|amazing|wonderful|fantastic)\b', r'really \1', text, flags=re.IGNORECASE)
        
        return text
        
    elif emotion == 'professional':
        # Make language more formal and structured
        # Replace casual phrases with more formal ones
        replacements = [
            (r'\bkind of\b', 'somewhat'),
            (r'\ba lot\b', 'significantly'),
            (r'\bget\b', 'obtain'),
            (r'\buse\b', 'utilize'),
            (r'\bstart\b', 'commence'),
            (r'\bend\b', 'conclude'),
            (r'\bfind out\b', 'determine'),
            (r'\blook at\b', 'examine'),
            (r'\btalk about\b', 'discuss')
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            
        return text
        
    elif emotion == 'enthusiastic':
        # Add emphasis and excitement
        # Add exclamation points to sentences that don't have them
        text = re.sub(r'([.]) ', r'! ', text)
        
        # Add emphasis words
        emphasis = [
            (r'\b(good|great)\b', r'fantastic'),
            (r'\b(like|enjoy)\b', r'love'),
            (r'\b(interesting)\b', r'fascinating'),
            (r'\b(important)\b', r'crucial')
        ]
        
        for pattern, replacement in emphasis:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            
        # Add enthusiastic interjections
        if len(text) > 100 and '!' not in text[:50]:
            interjections = ["Wow! ", "Amazing! ", "Incredible! ", "Excellent! "]
            text = interjections[len(text) % len(interjections)] + text
            
        return text
        
    # Default case
    return text

@app.route('/')
def index():
    """Return API information."""
    return jsonify({
        'name': 'TTS API',
        'version': '1.0',
        'description': 'Text-to-Speech API with natural voice enhancements',
        'endpoints': {
            '/api/stream-speech': 'POST - Convert text to speech audio'
        }
    })

@app.route('/api/stream-speech', methods=['POST'])
def stream_speech():
    """Generate speech from text and stream it directly without saving files."""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    language = data.get('language', 'en')
    slow = data.get('slow', False)
    emotion = data.get('emotion', 'neutral')
    
    try:
        # Create an in-memory bytes buffer
        mp3_fp = io.BytesIO()
        
        # Add natural pauses with punctuation and apply emotion
        enhanced_text = add_natural_pauses(text)
        enhanced_text = apply_emotion(enhanced_text, emotion)
        
        # Generate speech to the buffer
        tts = gTTS(text=enhanced_text, lang=language, slow=slow)
        tts.write_to_fp(mp3_fp)
        
        # Reset buffer position to the beginning
        mp3_fp.seek(0)
        
        # Stream the audio data
        return Response(
            mp3_fp, 
            mimetype='audio/mpeg',
            headers={
                'Content-Disposition': 'inline',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test_page():
    """Serve a simple test page."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TTS API Test</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .container {
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                padding: 8px 15px;
                margin-right: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            select, textarea {
                padding: 8px;
                margin-bottom: 10px;
                width: 100%;
                border-radius: 4px;
                border: 1px solid #ddd;
            }
            .loading {
                display: none;
                margin-left: 10px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>TTS API Test</h1>
        
        <div class="container">
            <h2>Test the API</h2>
            
            <div>
                <label for="text">Text to speak:</label>
                <textarea id="text" rows="4">Hello, this is a test of the text to speech API with human-like voice enhancements.</textarea>
            </div>
            
            <div>
                <label for="language">Language:</label>
                <select id="language">
                    <option value="en" selected>English (US)</option>
                    <option value="en-uk">English (UK)</option>
                    <option value="en-au">English (Australia)</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                </select>
            </div>
            
            <div>
                <label for="emotion">Emotion:</label>
                <select id="emotion">
                    <option value="neutral" selected>Neutral</option>
                    <option value="friendly">Friendly</option>
                    <option value="professional">Professional</option>
                    <option value="enthusiastic">Enthusiastic</option>
                </select>
            </div>
            
            <div>
                <label for="slow">Slow speech:</label>
                <input type="checkbox" id="slow">
            </div>
            
            <button onclick="speakText()">Speak Text</button>
            <span id="loading" class="loading">Generating audio...</span>
        </div>
        
        <script>
            // Audio element for playing streamed audio
            let audioPlayer = new Audio();
            
            async function speakText() {
                // Get the text and options
                const text = document.getElementById('text').value;
                const language = document.getElementById('language').value;
                const emotion = document.getElementById('emotion').value;
                const slow = document.getElementById('slow').checked;
                
                if (!text) {
                    alert('Please enter some text to speak');
                    return;
                }
                
                // Show loading indicator
                const loadingElement = document.getElementById('loading');
                loadingElement.style.display = 'inline-block';
                
                // Stop any currently playing audio
                audioPlayer.pause();
                
                try {
                    // Send request to API
                    const response = await fetch('/api/stream-speech', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            text: text,
                            language: language,
                            emotion: emotion,
                            slow: slow
                        }),
                    });
                    
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    
                    // Get audio blob
                    const audioBlob = await response.blob();
                    
                    // Hide loading indicator
                    loadingElement.style.display = 'none';
                    
                    // Create a URL for the audio blob
                    const audioUrl = URL.createObjectURL(audioBlob);
                    
                    // Set the audio source and play
                    audioPlayer.src = audioUrl;
                    
                    // Add event listeners
                    audioPlayer.onended = () => {
                        // Revoke the blob URL to free up memory
                        URL.revokeObjectURL(audioUrl);
                    };
                    
                    audioPlayer.onerror = () => {
                        // Handle audio error
                        loadingElement.textContent = 'Error playing audio';
                        loadingElement.style.display = 'inline-block';
                        URL.revokeObjectURL(audioUrl);
                    };
                    
                    // Play the audio
                    audioPlayer.play();
                } catch (error) {
                    // Show error
                    loadingElement.textContent = 'Error: ' + error.message;
                    loadingElement.style.display = 'inline-block';
                }
            }
        </script>
    </body>
    </html>
    """
    return html

def open_browser():
    """Open the browser after a short delay."""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000/test')

if __name__ == '__main__':
    # Open browser automatically
    threading.Thread(target=open_browser).start()
    
    # Run the Flask app
    print("Starting TTS API server...")
    print("A browser window should open automatically.")
    print("If not, go to http://127.0.0.1:5000/test")
    app.run(debug=True)
