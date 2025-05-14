"""
Serverless version of the streaming TTS server for Vercel deployment.
"""

from flask import Flask, request, jsonify, Response
import io
import re
from gtts import gTTS
from flask_cors import CORS

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

# For local development
if __name__ == '__main__':
    app.run(debug=True)
