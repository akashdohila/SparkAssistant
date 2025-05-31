"""
Spark AI Assistant Configuration Module

This module contains configuration settings for the Spark AI Assistant.
"""

import os
import json
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "assistant": {
        "name": "Spark",
        "wake_word": "Spark",
        "language": "en-US",
        "voice_id": "default",
        "response_style": "respectful",
        "enable_hinglish": True
    },
    "speech": {
        "recognition_engine": "whisper",
        "tts_engine": "pyttsx3",
        "wake_word_sensitivity": 0.5,
        "volume": 1.0,
        "rate": 200,
        "offline_mode": True
    },
    "system": {
        "startup_with_windows": True,
        "minimize_to_tray": True,
        "lock_screen_access": True,
        "enable_logging": True,
        "log_level": "INFO"
    },
    "privacy": {
        "offline_only_mode": True,
        "data_collection": "minimal",
        "require_permission_for_online": True,
        "encryption_enabled": False
    },
    "features": {
        "enable_camera_mode": True,
        "enable_file_management": True,
        "enable_system_control": True,
        "enable_clipboard_access": True,
        "enable_screen_capture": True
    },
    "mobile": {
        "enable_sync": True,
        "sync_interval": 300,  # seconds
        "connection_method": "local_network"
    },
    "responses": [
        "Ji sir!",
        "Yes boss!",
        "Bataiye sir.",
        "Yes sir ji!",
        "Main hoon Spark, kya hukm hai?",
        "Haanji boliye!",
        "Command received, boss!",
        "Always at your service!",
        "Sun raha hoon sir, boliye!",
        "Yes captain!",
        "Orders, sir?"
    ]
}

CONFIG_FILE = DATA_DIR / "config.json"

def load_config():
    """Load configuration from file or create default if not exists."""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

# Global configuration object
CONFIG = load_config()

def get_config(section=None, key=None):
    """Get configuration value."""
    if section is None:
        return CONFIG
    
    if key is None:
        return CONFIG.get(section, {})
    
    return CONFIG.get(section, {}).get(key)

def update_config(section, key, value):
    """Update configuration value and save."""
    if section not in CONFIG:
        CONFIG[section] = {}
    
    CONFIG[section][key] = value
    return save_config(CONFIG)
