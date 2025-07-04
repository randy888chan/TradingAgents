import tradingagents.default_config as default_config
from typing import Dict, Optional
import os

# Use default config but allow it to be overridden
_config: Optional[Dict] = None
DATA_DIR: Optional[str] = None


def initialize_config():
    """Initialize the configuration with default values."""
    global _config, DATA_DIR
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()
        DATA_DIR = _config["data_dir"]
        
        # Create necessary directories
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(_config["results_dir"], exist_ok=True)
        os.makedirs(_config["data_cache_dir"], exist_ok=True)


def set_config(config: Dict):
    """Update the configuration with custom values."""
    global _config, DATA_DIR
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()
    _config.update(config)
    DATA_DIR = _config["data_dir"]
    
    # Create necessary directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(_config["results_dir"], exist_ok=True)
    os.makedirs(_config["data_cache_dir"], exist_ok=True)


def get_config() -> Dict:
    """Get the current configuration."""
    if _config is None:
        initialize_config()
    return _config.copy()


# Initialize with default config
initialize_config()
