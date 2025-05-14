"""
Simple test script for Coqui TTS.
This script demonstrates how to use Coqui TTS to convert text to speech.
"""

import os
import sys

# Check if TTS is installed
try:
    from TTS.utils.manage import ModelManager
    from TTS.utils.synthesizer import Synthesizer
    import torch
    import numpy as np
    from scipy.io.wavfile import write as write_wav
except ImportError:
    print("Error: TTS is not installed. Please install it with 'pip install TTS'.")
    print("If you encounter build errors, you can try using a pre-built wheel or Docker.")
    sys.exit(1)

def text_to_speech(text, output_file="output.wav", model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_name=None):
    """
    Convert text to speech using Coqui TTS.
    
    Args:
        text (str): The text to convert to speech.
        output_file (str): The output file path.
        model_name (str): The TTS model name.
        vocoder_name (str): The vocoder model name.
    """
    try:
        # Create model manager
        model_manager = ModelManager(models_file=None)
        
        # Get model info
        model_path, config_path, model_item = model_manager.download_model(model_name)
        vocoder_path, vocoder_config_path, _ = model_manager.download_model(vocoder_name) if vocoder_name else (None, None, None)
        
        # Initialize synthesizer
        synthesizer = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            vocoder_checkpoint=vocoder_path,
            vocoder_config=vocoder_config_path,
            use_cuda=torch.cuda.is_available()
        )
        
        # Generate speech
        wav = synthesizer.tts(text)
        
        # Save the audio file
        write_wav(output_file, synthesizer.output_sample_rate, wav)
        
        print(f"Audio saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Test text
    test_text = "Hello, this is a test of the Coqui Text-to-Speech system."
    
    print("Initializing Coqui TTS (this may take a moment)...")
    
    # Convert text to speech
    success = text_to_speech(test_text)
    
    if success:
        # Play the audio file (Windows)
        os.system(f"start output.wav")
