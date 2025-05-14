"""
Command-line interface for testing TTS functionality.
This script provides a command-line interface for testing TTS functionality.
"""

import argparse
import os
from gtts import gTTS
import re

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

def text_to_speech(text, output_file="output.mp3", language="en", slow=False, emotion="neutral"):
    """
    Convert text to speech using gTTS.
    
    Args:
        text (str): The text to convert to speech.
        output_file (str): The output file path.
        language (str): The language code.
        slow (bool): Whether to speak slowly.
        emotion (str): The emotion to apply (neutral, friendly, professional, enthusiastic).
    """
    try:
        # Add natural pauses with punctuation and apply emotion
        enhanced_text = add_natural_pauses(text)
        enhanced_text = apply_emotion(enhanced_text, emotion)
        
        print(f"Original text: {text}")
        print(f"Enhanced text: {enhanced_text}")
        
        # Generate speech
        tts = gTTS(text=enhanced_text, lang=language, slow=slow)
        
        # Save the audio file
        tts.save(output_file)
        
        print(f"Audio saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert text to speech using gTTS.')
    parser.add_argument('--text', type=str, help='The text to convert to speech.', default="Hello, this is a test of the text to speech API with human-like voice enhancements.")
    parser.add_argument('--output', type=str, help='The output file path.', default="output.mp3")
    parser.add_argument('--language', type=str, help='The language code.', default="en")
    parser.add_argument('--slow', action='store_true', help='Whether to speak slowly.')
    parser.add_argument('--emotion', type=str, help='The emotion to apply (neutral, friendly, professional, enthusiastic).', default="neutral")
    parser.add_argument('--play', action='store_true', help='Whether to play the audio after generating it.')
    
    args = parser.parse_args()
    
    success = text_to_speech(args.text, args.output, args.language, args.slow, args.emotion)
    
    if success and args.play:
        # Play the audio file (Windows)
        os.system(f"start {args.output}")

if __name__ == "__main__":
    main()
