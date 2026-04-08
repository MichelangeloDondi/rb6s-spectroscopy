import yaml
from pathlib import Path
import sys

def load_config():
    """
    Dynamically locates the 'config' directory and merges all YAML files
    inside it into a single configuration dictionary.
    """
    current_dir = Path.cwd()
    root_path = None
    
    # 1. Look for the 'config' folder walking up the directory tree
    for directory in [current_dir] + list(current_dir.parents):
        if (directory / "config").is_dir():
            root_path = directory
            break
            
    if not root_path:
        print(f"❌ Critical Error: Could not find 'config' directory in {current_dir} or its parents.", file=sys.stderr)
        sys.exit(1)
        
    config_dir = root_path / "config"
    merged_config = {}
    
    # 2. Find and merge all .yaml files
    yaml_files = list(config_dir.glob("*.yaml"))
    
    if not yaml_files:
        print(f"⚠️ Warning: 'config' directory found at {config_dir}, but it contains no .yaml files.")
        return merged_config

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, "r") as f:
                data = yaml.safe_load(f)
                # Ensure the file isn't empty before merging
                if data: 
                    merged_config.update(data)
        except Exception as e:
            print(f"❌ Error loading {yaml_file.name}: {e}", file=sys.stderr)
            sys.exit(1)
            
    return merged_config

# Quick test if you run this file directly
if __name__ == "__main__":
    config = load_config()
    print("✅ Configuration successfully merged and loaded:")
    print(f"   Available top-level keys: {list(config.keys())}")