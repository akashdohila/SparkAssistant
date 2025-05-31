"""
Spark AI Assistant - Data Synchronization Module

This module handles data synchronization between Windows and mobile devices.
It ensures consistent state across devices and handles conflict resolution.
"""

import logging
import json
import time
import os
import hashlib
from pathlib import Path

logger = logging.getLogger(__name__)

class DataSynchronizer:
    """
    Data synchronization class that manages consistent data state across devices.
    Handles efficient differential sync and conflict resolution.
    """
    
    def __init__(self, data_dir, communicator):
        """
        Initialize the data synchronizer.
        
        Args:
            data_dir: Directory for synchronized data
            communicator: DeviceCommunicator instance for inter-device communication
        """
        self.data_dir = Path(data_dir)
        self.communicator = communicator
        self.sync_state = {}
        self.last_sync_time = 0
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load sync state if exists
        self._load_sync_state()
        
        # Register message handlers
        self._register_handlers()
        
        logger.info(f"Data synchronizer initialized with data directory {data_dir}")
    
    def _load_sync_state(self):
        """Load synchronization state from file."""
        sync_state_file = self.data_dir / "sync_state.json"
        
        if sync_state_file.exists():
            try:
                with open(sync_state_file, 'r') as f:
                    self.sync_state = json.load(f)
                self.last_sync_time = self.sync_state.get("last_sync_time", 0)
                logger.info(f"Loaded sync state, last sync: {self.last_sync_time}")
            except Exception as e:
                logger.error(f"Error loading sync state: {e}")
                self.sync_state = {"files": {}, "last_sync_time": 0}
        else:
            self.sync_state = {"files": {}, "last_sync_time": 0}
    
    def _save_sync_state(self):
        """Save synchronization state to file."""
        sync_state_file = self.data_dir / "sync_state.json"
        
        try:
            self.sync_state["last_sync_time"] = self.last_sync_time
            with open(sync_state_file, 'w') as f:
                json.dump(self.sync_state, f, indent=2)
            logger.info("Saved sync state")
        except Exception as e:
            logger.error(f"Error saving sync state: {e}")
    
    def _register_handlers(self):
        """Register message handlers for synchronization messages."""
        self.communicator.register_handler("sync_request", self._handle_sync_request)
        self.communicator.register_handler("sync_data", self._handle_sync_data)
        self.communicator.register_handler("file_request", self._handle_file_request)
        self.communicator.register_handler("file_data", self._handle_file_data)
    
    def _handle_sync_request(self, sender_id, payload):
        """
        Handle a synchronization request from another device.
        
        Args:
            sender_id: Sender device ID
            payload: Request payload
        """
        logger.info(f"Received sync request from device {sender_id}")
        
        # Get their sync state
        their_sync_time = payload.get("last_sync_time", 0)
        their_files = payload.get("files", {})
        
        # Determine what needs to be synchronized
        files_to_send = {}
        
        # Check our files against their state
        for file_path, our_info in self.sync_state.get("files", {}).items():
            # If we have a newer version or they don't have it
            if file_path not in their_files or our_info["modified_time"] > their_files[file_path]["modified_time"]:
                files_to_send[file_path] = our_info
        
        # Send sync data response
        response = {
            "last_sync_time": self.last_sync_time,
            "files": files_to_send
        }
        
        self.communicator.send_message(sender_id, "sync_data", response)
        logger.info(f"Sent sync data to device {sender_id} with {len(files_to_send)} files")
    
    def _handle_sync_data(self, sender_id, payload):
        """
        Handle synchronization data from another device.
        
        Args:
            sender_id: Sender device ID
            payload: Sync data payload
        """
        logger.info(f"Received sync data from device {sender_id}")
        
        their_sync_time = payload.get("last_sync_time", 0)
        their_files = payload.get("files", {})
        
        # Request files that we need
        for file_path, their_info in their_files.items():
            our_info = self.sync_state.get("files", {}).get(file_path)
            
            # If we don't have the file or have an older version
            if not our_info or their_info["modified_time"] > our_info["modified_time"]:
                # Request the file
                self.communicator.send_message(sender_id, "file_request", {
                    "file_path": file_path
                })
                logger.info(f"Requested file {file_path} from device {sender_id}")
    
    def _handle_file_request(self, sender_id, payload):
        """
        Handle a file request from another device.
        
        Args:
            sender_id: Sender device ID
            payload: Request payload
        """
        file_path = payload.get("file_path")
        if not file_path:
            logger.error("Received file request without file_path")
            return
        
        logger.info(f"Received request for file {file_path} from device {sender_id}")
        
        # Check if we have the file
        full_path = self.data_dir / file_path
        if not full_path.exists():
            logger.warning(f"Requested file {file_path} not found")
            return
        
        try:
            # Read the file
            with open(full_path, 'r') as f:
                file_content = f.read()
            
            # Get file info
            file_info = self.sync_state.get("files", {}).get(file_path, {})
            
            # Send the file
            self.communicator.send_message(sender_id, "file_data", {
                "file_path": file_path,
                "content": file_content,
                "modified_time": file_info.get("modified_time", time.time()),
                "hash": file_info.get("hash", "")
            })
            
            logger.info(f"Sent file {file_path} to device {sender_id}")
            
        except Exception as e:
            logger.error(f"Error sending file {file_path}: {e}")
    
    def _handle_file_data(self, sender_id, payload):
        """
        Handle file data from another device.
        
        Args:
            sender_id: Sender device ID
            payload: File data payload
        """
        file_path = payload.get("file_path")
        content = payload.get("content")
        modified_time = payload.get("modified_time")
        file_hash = payload.get("hash")
        
        if not file_path or content is None:
            logger.error("Received file data without required fields")
            return
        
        logger.info(f"Received file {file_path} from device {sender_id}")
        
        try:
            # Ensure directory exists
            full_path = self.data_dir / file_path
            os.makedirs(full_path.parent, exist_ok=True)
            
            # Write the file
            with open(full_path, 'w') as f:
                f.write(content)
            
            # Update sync state
            if "files" not in self.sync_state:
                self.sync_state["files"] = {}
            
            self.sync_state["files"][file_path] = {
                "modified_time": modified_time,
                "hash": file_hash or self._calculate_hash(content)
            }
            
            # Save sync state
            self._save_sync_state()
            
            logger.info(f"Saved file {file_path} from device {sender_id}")
            
        except Exception as e:
            logger.error(f"Error saving file {file_path}: {e}")
    
    def _calculate_hash(self, content):
        """
        Calculate hash for file content.
        
        Args:
            content: File content
            
        Returns:
            str: Content hash
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        return hashlib.md5(content).hexdigest()
    
    def sync_with_device(self, device_id):
        """
        Initiate synchronization with another device.
        
        Args:
            device_id: Target device ID
            
        Returns:
            bool: True if sync initiated successfully, False otherwise
        """
        if device_id not in self.communicator.get_connected_devices():
            logger.warning(f"Cannot sync: device {device_id} not connected")
            return False
        
        logger.info(f"Initiating sync with device {device_id}")
        
        # Send sync request
        self.communicator.send_message(device_id, "sync_request", {
            "last_sync_time": self.last_sync_time,
            "files": self.sync_state.get("files", {})
        })
        
        return True
    
    def add_file(self, file_path, content):
        """
        Add or update a file for synchronization.
        
        Args:
            file_path: Relative path of the file
            content: File content
            
        Returns:
            bool: True if file added successfully, False otherwise
        """
        try:
            # Ensure directory exists
            full_path = self.data_dir / file_path
            os.makedirs(full_path.parent, exist_ok=True)
            
            # Write the file
            with open(full_path, 'w') as f:
                f.write(content)
            
            # Update sync state
            if "files" not in self.sync_state:
                self.sync_state["files"] = {}
            
            current_time = time.time()
            self.sync_state["files"][file_path] = {
                "modified_time": current_time,
                "hash": self._calculate_hash(content)
            }
            
            # Save sync state
            self._save_sync_state()
            
            logger.info(f"Added file {file_path} for synchronization")
            return True
            
        except Exception as e:
            logger.error(f"Error adding file {file_path}: {e}")
            return False
    
    def get_file(self, file_path):
        """
        Get a synchronized file.
        
        Args:
            file_path: Relative path of the file
            
        Returns:
            str: File content or None if not found
        """
        full_path = self.data_dir / file_path
        
        if not full_path.exists():
            logger.warning(f"File {file_path} not found")
            return None
        
        try:
            with open(full_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
