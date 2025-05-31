"""
Spark AI Assistant - Intent Processing Module

This module handles natural language understanding and intent detection.
It processes user commands and extracts intents and entities for action execution.
"""

import logging
import re
import json
from pathlib import Path

# In a real implementation, we would import NLP libraries
# such as spaCy, Hugging Face Transformers, or custom NLP models
# For this prototype, we'll simulate intent processing with rule-based approaches

logger = logging.getLogger(__name__)

class IntentProcessor:
    """
    Intent processing class that analyzes text to determine user intent and extract entities.
    Supports both English and Hinglish language processing.
    """
    
    def __init__(self, language="en-US", enable_hinglish=True):
        """
        Initialize the intent processor.
        
        Args:
            language: Primary language for processing
            enable_hinglish: Whether to enable Hinglish processing
        """
        self.language = language
        self.enable_hinglish = enable_hinglish
        
        logger.info(f"Intent processor initialized with language {language}, Hinglish: {enable_hinglish}")
        
        # Load intent patterns and entity definitions
        self._load_intent_definitions()
    
    def _load_intent_definitions(self):
        """Load intent patterns and entity definitions."""
        # In a real implementation, this would load from files or models
        # For demonstration, we'll define them inline
        
        # Define basic intent patterns
        self.intent_patterns = {
            "greeting": [
                r"^(hello|hi|hey|namaste|greetings)[\s!]*$",
                r"^(good\s(morning|afternoon|evening))[\s!]*$",
                r"^(hii|hiii|hiiii|hola)[\s!]*$"
            ],
            "farewell": [
                r"^(goodbye|bye|see\syou|talk\sto\syou\slater)[\s!]*$",
                r"^(alvida|phir\smilenge)[\s!]*$"
            ],
            "gratitude": [
                r"^(thanks|thank\syou|shukriya|dhanyavaad)[\s!]*$"
            ],
            "system_control": [
                r"(turn|switch)\s(on|off)\s(wifi|bluetooth|airplane\smode)",
                r"(increase|decrease|raise|lower|turn\sup|turn\sdown)\s(volume|brightness)",
                r"(mute|unmute)\s(volume|system)",
                r"(shutdown|restart|lock|sleep)\s(system|computer|laptop)",
                r"(wifi|bluetooth|volume|brightness)\s(on|off|badha|kam|badhao|kamao)"
            ],
            "app_control": [
                r"(open|launch|start|run|close|exit)\s([a-zA-Z0-9\s]+)",
                r"([a-zA-Z0-9\s]+)\s(kholo|band\skaro)"
            ],
            "query_time": [
                r"what\stime\sis\sit",
                r"current\stime",
                r"time\sbatao",
                r"abhi\skitne\sbaje\shain"
            ],
            "query_date": [
                r"what\s(date|day)\sis\s(it|today)",
                r"aaj\skya\s(din|tareekh|date)\shai"
            ],
            "query_weather": [
                r"(what's|what\sis|how's|how\sis)\sthe\sweather",
                r"weather\s(report|forecast)",
                r"mausam\skaisa\shai"
            ],
            "take_screenshot": [
                r"take\s(a\s)?(screenshot|screen\sshot|screen\scapture)",
                r"capture\s(the\s)?screen",
                r"screenshot\s(lo|lena)"
            ],
            "send_message": [
                r"send\s(a\s)?message\sto\s([a-zA-Z0-9\s]+)",
                r"message\s([a-zA-Z0-9\s]+)",
                r"([a-zA-Z0-9\s]+)\sko\smessage\s(bhejo|karo)"
            ],
            "make_call": [
                r"call\s([a-zA-Z0-9\s]+)",
                r"dial\s([a-zA-Z0-9\s]+)",
                r"([a-zA-Z0-9\s]+)\sko\scall\s(karo|lagao)"
            ]
        }
        
        # Compile regex patterns
        for intent, patterns in self.intent_patterns.items():
            self.intent_patterns[intent] = [re.compile(p, re.IGNORECASE) for p in patterns]
        
        logger.info(f"Loaded {len(self.intent_patterns)} intent definitions")
    
    def process(self, text):
        """
        Process text to determine intent and extract entities.
        
        Args:
            text: Text to process
            
        Returns:
            tuple: (intent, entities) where intent is a string and entities is a dict
        """
        if not text:
            return "unknown", {}
        
        logger.info(f"Processing text: '{text}'")
        
        # Normalize text
        normalized_text = text.lower().strip()
        
        # Match against intent patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = pattern.search(normalized_text)
                if match:
                    # Extract entities based on intent
                    entities = self._extract_entities(intent, normalized_text, match)
                    logger.info(f"Matched intent: {intent}, entities: {entities}")
                    return intent, entities
        
        # If no match, try to handle as a general query
        if any(q in normalized_text for q in ["what", "who", "when", "where", "why", "how", "is", "are", "can", "kya", "kaun", "kab", "kahan", "kyun", "kaise"]):
            return "query", {"query_text": text}
        
        # Default to unknown intent
        logger.info("No intent matched, defaulting to unknown")
        return "unknown", {}
    
    def _extract_entities(self, intent, text, match):
        """
        Extract entities based on intent and regex match.
        
        Args:
            intent: Detected intent
            text: Original text
            match: Regex match object
            
        Returns:
            dict: Extracted entities
        """
        entities = {}
        
        if intent == "system_control":
            # Extract action and target
            action_words = ["turn", "switch", "increase", "decrease", "raise", "lower", "mute", "unmute", "shutdown", "restart", "lock", "sleep"]
            target_words = ["wifi", "bluetooth", "airplane mode", "volume", "brightness", "system", "computer", "laptop"]
            
            # Extract action
            for action in action_words:
                if action in text:
                    if action in ["turn", "switch"]:
                        if "on" in text:
                            entities["action"] = "turn_on"
                        elif "off" in text:
                            entities["action"] = "turn_off"
                    else:
                        entities["action"] = action
                    break
            
            # Extract target
            for target in target_words:
                if target in text:
                    entities["target"] = target
                    break
            
            # Handle Hinglish
            if "badha" in text or "badhao" in text:
                entities["action"] = "increase"
            elif "kam" in text or "kamao" in text:
                entities["action"] = "decrease"
        
        elif intent == "app_control":
            # Extract action and app name
            action_words = ["open", "launch", "start", "run", "close", "exit", "kholo", "band karo"]
            
            # Extract action
            for action in action_words:
                if action in text:
                    if action in ["open", "launch", "start", "run", "kholo"]:
                        entities["action"] = "open"
                    else:
                        entities["action"] = "close"
                    
                    # Remove action word to get app name
                    app_text = text.replace(action, "").strip()
                    entities["app_name"] = app_text
                    break
            
            # If no action found but intent matched, assume open
            if "action" not in entities:
                entities["action"] = "open"
                entities["app_name"] = text
        
        elif intent == "send_message":
            # Extract recipient
            if "to" in text:
                recipient = text.split("to")[1].strip()
                entities["recipient"] = recipient
            elif "ko" in text:
                recipient = text.split("ko")[0].strip()
                entities["recipient"] = recipient
        
        elif intent == "make_call":
            # Extract recipient
            if "call" in text:
                recipient = text.split("call")[1].strip()
                entities["recipient"] = recipient
            elif "ko call" in text:
                recipient = text.split("ko call")[0].strip()
                entities["recipient"] = recipient
        
        return entities
    
    def get_response_for_intent(self, intent, entities):
        """
        Generate a response based on intent and entities.
        
        Args:
            intent: Detected intent
            entities: Extracted entities
            
        Returns:
            str: Response text
        """
        # This is a simple response generator
        # In a real implementation, this would be more sophisticated
        
        if intent == "greeting":
            return "Hello! How can I help you today?"
        
        elif intent == "farewell":
            return "Goodbye! Have a great day!"
        
        elif intent == "gratitude":
            return "You're welcome!"
        
        elif intent == "system_control":
            action = entities.get("action", "unknown")
            target = entities.get("target", "unknown")
            
            if action == "turn_on":
                return f"Turning on {target}."
            elif action == "turn_off":
                return f"Turning off {target}."
            elif action in ["increase", "raise"]:
                return f"Increasing {target}."
            elif action in ["decrease", "lower"]:
                return f"Decreasing {target}."
            else:
                return f"Performing {action} on {target}."
        
        elif intent == "app_control":
            action = entities.get("action", "open")
            app_name = entities.get("app_name", "unknown")
            
            if action == "open":
                return f"Opening {app_name}."
            else:
                return f"Closing {app_name}."
        
        elif intent == "query_time":
            import datetime
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        elif intent == "query_date":
            import datetime
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}."
        
        elif intent == "query_weather":
            # In a real implementation, this would check weather data
            return "I'm sorry, I don't have access to weather information in offline mode."
        
        elif intent == "take_screenshot":
            return "Taking a screenshot now."
        
        elif intent == "send_message":
            recipient = entities.get("recipient", "unknown")
            return f"What message would you like to send to {recipient}?"
        
        elif intent == "make_call":
            recipient = entities.get("recipient", "unknown")
            return f"Calling {recipient} now."
        
        elif intent == "query":
            query_text = entities.get("query_text", "")
            return f"I'll try to find information about '{query_text}', but I'm limited in offline mode."
        
        else:
            return "I'm not sure how to help with that yet."
