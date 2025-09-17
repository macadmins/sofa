#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "tomli>=2.0.1",
# ]
# ///
"""
Transform essential_links.toml into the JSON format expected by the web components.
"""

import json
import tomli
from pathlib import Path
from typing import Dict, List, Any


def transform_essential_links() -> Dict[str, Any]:
    """Transform TOML essential_links into JSON format expected by components"""
    
    # Read the TOML file
    toml_path = Path("config/essential_links.toml")
    if not toml_path.exists():
        print(f"❌ Essential links TOML not found at {toml_path}")
        return {}
    
    with open(toml_path, "rb") as f:
        toml_data = tomli.load(f)
    
    # Create the JSON structure expected by LatestFeatures.vue
    json_structure = {}
    
    # Process macOS versions
    if "macOS" in toml_data:
        json_structure["macOS"] = {
            "general": {},
            "versions": {}
        }
        
        for os_name, links in toml_data["macOS"].items():
            # Map OS names to version entries
            version_key = os_name  # e.g., "Sequoia", "Sonoma", etc.
            json_structure["macOS"]["versions"][version_key] = links
    
    # Process iOS versions
    if "iOS" in toml_data:
        json_structure["iOS"] = {
            "general": {},
            "versions": {}
        }
        
        for version, links in toml_data["iOS"].items():
            # Convert version numbers to the expected format
            version_key = f"iOS {version}"
            json_structure["iOS"]["versions"][version_key] = links
        
        # Add general iOS links from Common section
        if "Common" in toml_data:
            json_structure["iOS"]["general"] = {
                "Developer Release Notes": "https://developer.apple.com/documentation/ios-ipados-release-notes"
            }
    
    # Process iPadOS (same as iOS structure)
    if "iOS" in toml_data:
        json_structure["iPadOS"] = {
            "general": {},
            "versions": {}
        }
        
        for version, links in toml_data["iOS"].items():
            # Convert version numbers to the expected format
            version_key = f"iPadOS {version}"
            json_structure["iPadOS"]["versions"][version_key] = links
        
        # Add general iPadOS links from Common section
        if "Common" in toml_data:
            json_structure["iPadOS"]["general"] = {
                "Developer Release Notes": "https://developer.apple.com/documentation/ios-ipados-release-notes"
            }
    
    # Process other platforms (Safari, tvOS, watchOS, visionOS) if they exist
    platform_mappings = {
        "Safari": "Safari",
        "tvOS": "tvOS", 
        "watchOS": "watchOS",
        "visionOS": "visionOS"
    }
    
    for toml_key, json_key in platform_mappings.items():
        if toml_key in toml_data:
            json_structure[json_key] = {
                "general": {},
                "versions": {}
            }
            
            for version, links in toml_data[toml_key].items():
                version_key = f"{json_key} {version}"
                json_structure[json_key]["versions"][version_key] = links
    
    # Add common/general resources from various sections
    general_resources = []
    
    # Add resources from Common section
    if "Common" in toml_data:
        for title, url in toml_data["Common"].items():
            general_resources.append({"title": title, "url": url, "platform": "general"})
    
    # Add resources from Apple Guides
    if "Apple Guides" in toml_data and "links" in toml_data["Apple Guides"]:
        for title, url in toml_data["Apple Guides"]["links"].items():
            general_resources.append({"title": title, "url": url, "platform": "general"})
    
    # Add resources from Apple Training
    if "Apple Training" in toml_data and "links" in toml_data["Apple Training"]:
        for title, url in toml_data["Apple Training"]["links"].items():
            general_resources.append({"title": title, "url": url, "platform": "general"})
    
    # Add resources from Apple Developer
    if "Apple Developer" in toml_data:
        for key, value in toml_data["Apple Developer"].items():
            if key not in ["context", "description"] and isinstance(value, str):
                general_resources.append({"title": key, "url": value, "platform": "general"})
    
    # Add resources from Security section  
    if "Security" in toml_data:
        for key, value in toml_data["Security"].items():
            if key not in ["context", "description"] and isinstance(value, str):
                title = "macOS Security Compliance Project" if key == "mSCP" else "MITRE ATT&CK for macOS" if key == "Mitre" else key
                general_resources.append({"title": title, "url": value, "platform": "general"})
    
    # Add general resources to the structure
    if general_resources:
        json_structure["_general_resources"] = general_resources
    
    return json_structure


def main():
    """Main function to run the transformation"""
    print("🔄 Transforming essential_links.toml to JSON...")
    
    # Ensure we're in the right directory
    if not Path("config/essential_links.toml").exists():
        print("❌ Must run from repo root (config/essential_links.toml not found)")
        return 1
    
    # Transform the data
    json_data = transform_essential_links()
    
    if not json_data:
        print("❌ No data to transform")
        return 1
    
    # Ensure output directory exists
    output_dir = Path("data/resources")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the JSON file
    output_path = output_dir / "essential_links.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Essential links transformed and saved to {output_path}")
    
    # Show summary
    platforms = [key for key in json_data.keys() if not key.startswith("_")]
    general_count = len(json_data.get("_general_resources", []))
    
    print(f"   📱 Platforms: {', '.join(platforms)}")
    print(f"   🔗 General resources: {general_count}")
    
    return 0


if __name__ == "__main__":
    exit(main())