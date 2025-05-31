"""
Spark AI Assistant - Main Application Entry Point

This module serves as the entry point for the Spark AI Assistant Windows application.
It initializes all core components and manages the application lifecycle.
"""

import sys
import threading
import logging
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# Core imports
from src.windows.core.config import get_config, CONFIG
from src.windows.speech.wake_word import WakeWordDetector
from src.windows.speech.recognition import SpeechRecognizer
from src.windows.speech.synthesis import TextToSpeech
from src.windows.nlp.intent_processor import IntentProcessor
from src.windows.system_integration.system_controller import SystemController
from src.windows.ui.tray_app import TrayApplication

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(CONFIG['system'].get('log_file', 'spark_assistant.log'))),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SparkAssistant:
    """Main Spark AI Assistant class that coordinates all components."""
    
    def __init__(self):
        """Initialize the Spark AI Assistant."""
        logger.info("Initializing Spark AI Assistant")
        
        # Initialize components
        self.tts = TextToSpeech()
        self.recognizer = SpeechRecognizer()
        self.intent_processor = IntentProcessor()
        self.system_controller = SystemController()
        
        # Initialize wake word detector
        self.wake_word_detector = WakeWordDetector(
            callback=self.on_wake_word_detected,
            sensitivity=get_config('speech', 'wake_word_sensitivity')
        )
        
        # State variables
        self.is_listening = False
        self.is_speaking = False
        self.is_processing = False
        
        logger.info("Spark AI Assistant initialized")
    
    def on_wake_word_detected(self):
        """Callback when wake word is detected."""
        if self.is_listening or self.is_speaking:
            return
        
        logger.info("Wake word detected")
        self.is_listening = True
        
        # Play acknowledgment sound or speak response
        self.speak_random_response()
        
        # Start listening for command in a separate thread
        threading.Thread(target=self.listen_for_command).start()
    
    def speak_random_response(self):
        """Speak a random response from the configured list."""
        import random
        responses = get_config('responses')
        if responses:
            response = random.choice(responses)
            self.speak(response)
    
    def speak(self, text):
        """Speak the given text."""
        self.is_speaking = True
        self.tts.speak(text)
        self.is_speaking = False
    
    def listen_for_command(self):
        """Listen for a command and process it."""
        try:
            # Listen for command with timeout
            text = self.recognizer.recognize(timeout=5)
            if text:
                logger.info(f"Recognized: {text}")
                self.process_command(text)
            else:
                logger.info("No speech detected")
        except Exception as e:
            logger.error(f"Error in listen_for_command: {e}")
        finally:
            self.is_listening = False
    
    def process_command(self, text):
        """Process the recognized command."""
        self.is_processing = True
        try:
            # Process intent
            intent, entities = self.intent_processor.process(text)
            logger.info(f"Intent: {intent}, Entities: {entities}")
            
            # Execute command based on intent
            response = self.execute_command(intent, entities)
            
            # Speak response
            if response:
                self.speak(response)
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.speak("I'm sorry, I couldn't process that command.")
        finally:
            self.is_processing = False
    
    def execute_command(self, intent, entities):
        """Execute a command based on intent and entities."""
        # This is a placeholder for the actual command execution logic
        # In a real implementation, this would dispatch to various handlers
        
        if intent == "greeting":
            return "Hello! How can I help you today?"
        
        elif intent == "system_control":
            return self.system_controller.handle_command(entities)
        
        elif intent == "app_control":
            app_name = entities.get("app_name")
            action = entities.get("action", "open")
            return self.system_controller.control_application(app_name, action)
        
        elif intent == "query":
            # This would connect to a knowledge base or search function
            return "I'm still learning how to answer questions."
        
        else:
            return "I'm not sure how to help with that yet."
    
    def start(self):
        """Start the assistant."""
        logger.info("Starting Spark AI Assistant")
        self.wake_word_detector.start()
        
        # Initial greeting
        if get_config('system', 'startup_greeting'):
            self.speak("Spark AI Assistant is ready.")
    
    def stop(self):
        """Stop the assistant."""
        logger.info("Stopping Spark AI Assistant")
        self.wake_word_detector.stop()


def main():
    """Main entry point for the application."""
    # Create and start the assistant
    assistant = SparkAssistant()
    
    # Create and start the UI
    app = TrayApplication(assistant)
    
    # Start the assistant
    assistant.start()
    
    # Start the UI event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
