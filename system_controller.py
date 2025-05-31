"""
Spark AI Assistant - System Controller Module

This module handles system integration and control functions.
It provides interfaces to control applications, system settings, and hardware.
"""

import logging
import subprocess
import os
import time
import platform
import psutil

# In a real implementation, we would import platform-specific libraries
# such as pywin32 for Windows integration
# For this prototype, we'll simulate system control functions

logger = logging.getLogger(__name__)

class SystemController:
    """
    System controller class that provides interfaces to control the operating system,
    applications, and hardware settings.
    """
    
    def __init__(self):
        """Initialize the system controller."""
        logger.info("System controller initialized")
        
        # Cache for running applications
        self.running_apps = {}
        
        # Map of common application names to executables
        self.app_map = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "file explorer": "explorer.exe",
            "settings": "ms-settings:",
            "spotify": "spotify.exe",
            "vlc": "vlc.exe",
            "zoom": "zoom.exe",
            "teams": "teams.exe",
            "skype": "skype.exe",
            "whatsapp": "whatsapp.exe",
            "telegram": "telegram.exe"
        }
    
    def handle_command(self, entities):
        """
        Handle system control commands based on entities.
        
        Args:
            entities: Dictionary of command entities
            
        Returns:
            str: Response message
        """
        action = entities.get("action", "unknown")
        target = entities.get("target", "unknown")
        
        logger.info(f"Handling system command: action={action}, target={target}")
        
        # Handle different system control actions
        if target in ["wifi", "bluetooth", "airplane mode"]:
            return self._handle_connectivity(action, target)
        
        elif target in ["volume", "brightness"]:
            return self._handle_settings(action, target)
        
        elif action in ["shutdown", "restart", "lock", "sleep"]:
            return self._handle_power(action)
        
        else:
            return f"I'm not sure how to {action} {target}."
    
    def _handle_connectivity(self, action, target):
        """
        Handle connectivity-related commands.
        
        Args:
            action: Action to perform
            target: Target connectivity feature
            
        Returns:
            str: Response message
        """
        # In a real implementation, this would use platform-specific APIs
        # to control WiFi, Bluetooth, etc.
        
        if action == "turn_on":
            logger.info(f"Turning on {target}")
            return f"Turning on {target}."
        
        elif action == "turn_off":
            logger.info(f"Turning off {target}")
            return f"Turning off {target}."
        
        else:
            return f"I'm not sure how to {action} {target}."
    
    def _handle_settings(self, action, target):
        """
        Handle settings-related commands.
        
        Args:
            action: Action to perform
            target: Target setting
            
        Returns:
            str: Response message
        """
        # In a real implementation, this would use platform-specific APIs
        # to control volume, brightness, etc.
        
        if action in ["increase", "raise"]:
            logger.info(f"Increasing {target}")
            return f"Increasing {target}."
        
        elif action in ["decrease", "lower"]:
            logger.info(f"Decreasing {target}")
            return f"Decreasing {target}."
        
        elif action == "mute":
            logger.info(f"Muting {target}")
            return f"Muting {target}."
        
        elif action == "unmute":
            logger.info(f"Unmuting {target}")
            return f"Unmuting {target}."
        
        else:
            return f"I'm not sure how to {action} {target}."
    
    def _handle_power(self, action):
        """
        Handle power-related commands.
        
        Args:
            action: Action to perform
            
        Returns:
            str: Response message
        """
        # In a real implementation, this would use platform-specific APIs
        # to control system power state
        
        logger.info(f"Handling power command: {action}")
        
        if action == "shutdown":
            return "Preparing to shut down the system. Please save your work."
        
        elif action == "restart":
            return "Preparing to restart the system. Please save your work."
        
        elif action == "lock":
            return "Locking the system."
        
        elif action == "sleep":
            return "Putting the system to sleep."
        
        else:
            return f"I'm not sure how to {action} the system."
    
    def control_application(self, app_name, action="open"):
        """
        Control an application (open or close).
        
        Args:
            app_name: Name of the application
            action: Action to perform (open or close)
            
        Returns:
            str: Response message
        """
        if not app_name:
            return "Please specify an application name."
        
        # Normalize app name
        app_name = app_name.lower().strip()
        
        # Find executable name
        executable = self._get_executable_for_app(app_name)
        
        logger.info(f"Controlling application: {app_name} ({executable}), action: {action}")
        
        if action == "open":
            return self._open_application(app_name, executable)
        elif action == "close":
            return self._close_application(app_name, executable)
        else:
            return f"I'm not sure how to {action} {app_name}."
    
    def _get_executable_for_app(self, app_name):
        """
        Get executable name for an application.
        
        Args:
            app_name: Application name
            
        Returns:
            str: Executable name
        """
        # Check if app name is in our map
        for key, value in self.app_map.items():
            if key in app_name or app_name in key:
                return value
        
        # If not found, use app name as executable
        return app_name + ".exe"
    
    def _open_application(self, app_name, executable):
        """
        Open an application.
        
        Args:
            app_name: Application name
            executable: Executable name
            
        Returns:
            str: Response message
        """
        # In a real implementation, this would use platform-specific APIs
        # to launch applications
        
        logger.info(f"Opening application: {app_name} ({executable})")
        
        # Simulate opening the application
        self.running_apps[app_name] = {
            "executable": executable,
            "pid": 12345  # Simulated process ID
        }
        
        return f"Opening {app_name}."
    
    def _close_application(self, app_name, executable):
        """
        Close an application.
        
        Args:
            app_name: Application name
            executable: Executable name
            
        Returns:
            str: Response message
        """
        # In a real implementation, this would use platform-specific APIs
        # to close applications
        
        logger.info(f"Closing application: {app_name} ({executable})")
        
        # Check if app is in our running apps cache
        if app_name in self.running_apps:
            del self.running_apps[app_name]
            return f"Closing {app_name}."
        else:
            return f"I don't see {app_name} running."
    
    def take_screenshot(self, save_path=None):
        """
        Take a screenshot.
        
        Args:
            save_path: Path to save the screenshot
            
        Returns:
            str: Path to saved screenshot or error message
        """
        # In a real implementation, this would use platform-specific APIs
        # to take screenshots
        
        logger.info(f"Taking screenshot, save path: {save_path}")
        
        # Generate default save path if not provided
        if not save_path:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(os.path.expanduser("~"), "Pictures", f"Screenshot_{timestamp}.png")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Simulate taking screenshot
        # In a real implementation, this would be:
        # import pyautogui
        # screenshot = pyautogui.screenshot()
        # screenshot.save(save_path)
        
        # Simulate file creation
        with open(save_path, "w") as f:
            f.write("Simulated screenshot content")
        
        logger.info(f"Screenshot saved to: {save_path}")
        return f"Screenshot saved to {save_path}"
    
    def get_system_info(self):
        """
        Get system information.
        
        Returns:
            dict: System information
        """
        info = {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free
            }
        }
        
        # Add battery info if available
        if hasattr(psutil, "sensors_battery") and psutil.sensors_battery():
            battery = psutil.sensors_battery()
            info["battery"] = {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "secsleft": battery.secsleft
            }
        
        logger.info("Retrieved system information")
        return info
    
    def get_running_processes(self, limit=10):
        """
        Get list of running processes.
        
        Args:
            limit: Maximum number of processes to return
            
        Returns:
            list: Running processes
        """
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'memory_percent': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort by memory usage
        processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        
        logger.info(f"Retrieved {len(processes[:limit])} running processes")
        return processes[:limit]
