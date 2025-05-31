# Spark AI Assistant Deployment Guide

## Overview

This document provides instructions for deploying and using the Spark AI Assistant on both Windows laptop and mobile devices. Follow these steps to set up and configure the assistant for optimal performance.

## System Requirements

### Windows Requirements
- Windows 10 or 11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Microphone for voice input
- Speakers for voice output
- Python 3.9 or higher
- Administrator privileges for installation

### Mobile Requirements
- Android 8.0+ or iOS 13.0+
- 2GB RAM minimum
- 500MB free storage
- Permissions for microphone, calls, messages, and notifications

## Windows Installation

### Step 1: Install Python Dependencies
1. Ensure Python 3.9+ is installed on your system
2. Open Command Prompt as Administrator
3. Navigate to the Spark Assistant directory
4. Create a virtual environment:
   ```
   python -m venv venv
   ```
5. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
6. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Step 2: Install System Dependencies
1. Install PyAudio for microphone access:
   ```
   pip install pyaudio
   ```
2. Install Tesseract OCR for text recognition:
   ```
   # Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   ```
3. Install required Windows components:
   ```
   pip install pywin32
   ```

### Step 3: Configure the Assistant
1. Open the configuration file at `data/config.json`
2. Adjust settings as needed:
   - Set preferred wake word sensitivity
   - Configure voice settings
   - Set startup preferences
   - Adjust privacy settings

### Step 4: Set Up Autostart (Optional)
1. Create a shortcut to `run_assistant.bat` in the Spark Assistant directory
2. Press Win+R, type `shell:startup` and press Enter
3. Copy the shortcut to the Startup folder

## Mobile Installation

### Step 1: Install the Companion App
1. Download the Spark Assistant companion app:
   - Android: [Google Play Store link]
   - iOS: [App Store link]
2. Install the app on your mobile device

### Step 2: Configure the App
1. Open the Spark Assistant companion app
2. Grant requested permissions:
   - Microphone access
   - Call management
   - Message access
   - Notification access
   - Location services (optional)
3. Adjust settings as needed:
   - Notification preferences
   - Battery optimization exceptions
   - Data synchronization options

## Device Pairing

### Step 1: Ensure Network Connectivity
1. Connect both Windows laptop and mobile device to the same Wi-Fi network
2. Ensure no firewall is blocking communication on port 8765

### Step 2: Pair Devices
1. Start the Spark Assistant on Windows
2. Open the companion app on your mobile device
3. On Windows, select "Pair New Device" from the tray icon menu
4. On mobile, tap "Connect to Windows Device"
5. Confirm the pairing code displayed on both devices

## Using Spark Assistant

### Basic Commands
- Wake the assistant by saying "Spark"
- Wait for the acknowledgment response
- Speak your command clearly
- Examples:
  - "What time is it?"
  - "Open Chrome"
  - "Turn up the volume"
  - "Send a message to John"

### Windows-Specific Features
- **Application Control**: "Open/close [application name]"
- **File Management**: "Find files containing [text]"
- **System Control**: "Turn on/off Wi-Fi", "Increase volume"
- **Screen Capture**: "Take a screenshot"

### Mobile-Specific Features
- **Call Management**: "Call [contact name]"
- **Messaging**: "Send a message to [contact]"
- **Notifications**: "Read my notifications"
- **Location**: "Where am I?"

### Cross-Device Features
- **Synchronization**: "Sync my devices"
- **Remote Control**: "Send a message from my phone to [contact]"
- **Media Transfer**: "Show photos from my phone"

## Troubleshooting

### Windows Issues
- **Wake word not detected**: Adjust microphone settings and sensitivity
- **Commands not recognized**: Retrain speech model in settings
- **Application control fails**: Ensure app paths are correctly configured
- **System crashes**: Check log files in `logs/` directory

### Mobile Issues
- **Connection problems**: Verify both devices are on same network
- **Permission errors**: Review app permissions in system settings
- **Battery drain**: Adjust background service settings
- **Notification issues**: Ensure notification access is granted

### Cross-Device Issues
- **Pairing fails**: Check network connectivity and firewall settings
- **Sync problems**: Try manual sync from settings menu
- **Command routing errors**: Verify device status in the dashboard

## Security and Privacy

### Data Storage
- All personal data is stored locally on your devices
- No data is sent to external servers without permission
- Encryption can be enabled in privacy settings

### Network Communication
- Device-to-device communication is encrypted
- No persistent connections to external servers
- All internet access requires explicit permission

### Permissions
- Review and adjust permissions in settings
- Disable features you don't need
- Clear stored data through the privacy menu

## Updating

### Windows Updates
1. Close the Spark Assistant
2. Pull latest code or download update package
3. Run update script:
   ```
   update_assistant.bat
   ```
4. Restart the assistant

### Mobile Updates
1. Update through app store when available
2. Follow in-app update prompts
3. Verify settings after update

## Uninstallation

### Windows Uninstallation
1. Run `uninstall.bat` from the Spark Assistant directory
2. Remove the program directory
3. Remove startup entries if configured

### Mobile Uninstallation
1. Uninstall the app through system settings
2. Clear app data if prompted

## Support and Feedback

For assistance or to provide feedback:
- Check the documentation in the `docs/` directory
- Visit the support website at [support link]
- Submit issues through the feedback form in settings
- Contact support at [email address]
