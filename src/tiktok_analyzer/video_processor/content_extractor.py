"""
Content extraction module for TikTok videos.

This module is responsible for extracting text content from videos,
including embedded text and speech-to-text conversion.
"""

import os
import tempfile
from pathlib import Path
import speech_recognition as sr
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import pytesseract
from PIL import Image
import numpy as np
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class ContentExtractor:
    """
    Extracts text content from videos.
    """
    
    def __init__(self):
        """Initialize the content extractor."""
        self.recognizer = sr.Recognizer()
    
    def extract_content(self, video_path):
        """
        Extract text content from a video.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Extracted text content
        """
        if not video_path or not os.path.exists(video_path):
            logger.warning(f"Video file not found: {video_path}")
            return ""
        
        logger.info(f"Extracting content from video: {video_path}")
        
        embedded_text = self._extract_embedded_text(video_path)
        
        speech_text = self._extract_speech(video_path)
        
        combined_text = ""
        
        if embedded_text:
            combined_text += "Embedded Text:\n" + embedded_text + "\n\n"
        
        if speech_text:
            combined_text += "Speech Content:\n" + speech_text
        
        if not combined_text:
            logger.warning(f"No text content extracted from video: {video_path}")
            return "No text content could be extracted from this video."
        
        return combined_text
    
    def _extract_embedded_text(self, video_path):
        """
        Extract embedded text from a video using OCR.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Extracted embedded text
        """
        try:
            logger.info(f"Extracting embedded text from video: {video_path}")
            
            video = VideoFileClip(video_path)
            
            duration = video.duration
            frame_count = min(10, int(duration))  # Sample up to 10 frames
            
            all_text = []
            
            for i in range(frame_count):
                position = duration * i / frame_count
                frame = video.get_frame(position)
                
                image = Image.fromarray(frame)
                
                text = pytesseract.image_to_string(image)
                
                if text.strip():
                    all_text.append(text.strip())
            
            video.close()
            
            combined_text = "\n".join(all_text)
            
            logger.info(f"Extracted embedded text: {len(combined_text)} characters")
            return combined_text
            
        except Exception as e:
            logger.error(f"Error extracting embedded text: {str(e)}")
            return ""
    
    def _extract_speech(self, video_path):
        """
        Extract speech from a video using speech recognition.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Extracted speech text
        """
        try:
            logger.info(f"Extracting speech from video: {video_path}")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = os.path.join(temp_dir, "audio.wav")
                self._extract_audio(video_path, audio_path)
                
                text = self._recognize_speech(audio_path)
                
                logger.info(f"Extracted speech text: {len(text)} characters")
                return text
                
        except Exception as e:
            logger.error(f"Error extracting speech: {str(e)}")
            return ""
    
    def _extract_audio(self, video_path, output_path):
        """
        Extract audio from a video file.
        
        Args:
            video_path: Path to the video file
            output_path: Path to save the extracted audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            video = VideoFileClip(video_path)
            
            audio = video.audio
            
            if audio is None:
                logger.warning(f"No audio track found in video: {video_path}")
                return False
            
            audio.write_audiofile(output_path, codec='pcm_s16le')
            
            video.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error extracting audio: {str(e)}")
            return False
    
    def _recognize_speech(self, audio_path):
        """
        Perform speech recognition on an audio file.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Recognized text
        """
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                
                text = self.recognizer.recognize_google(audio)
                
                return text
                
        except sr.UnknownValueError:
            logger.warning("Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from Speech Recognition service: {str(e)}")
            return ""
        except Exception as e:
            logger.error(f"Error in speech recognition: {str(e)}")
            return ""
