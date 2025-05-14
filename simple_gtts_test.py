"""
Simple test script for gTTS (Google Text-to-Speech).
This script demonstrates how to use gTTS to convert text to speech.
"""

from gtts import gTTS
import os

def text_to_speech(text, output_file="output.mp3", language="en", slow=False):
    """
    Convert text to speech using gTTS.
    
    Args:
        text (str): The text to convert to speech.
        output_file (str): The output file path.
        language (str): The language code.
        slow (bool): Whether to speak slowly.
    """
    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang=language, slow=slow)
        
        # Save the audio file
        tts.save(output_file)
        
        print(f"Audio saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Test text
    test_text = "Hello, this is a test of the Google Text-to-Speech API."
    
    # Convert text to speech
    success = text_to_speech(test_text)
    
    if success:
        # Play the audio file (Windows)
        os.system(f"start output.mp3")
