#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich>=13.7.0",
#     "typer>=0.9.0",
# ]
# ///
"""
SOFA Device Manager - One Script for All Device Maintenance
Simple flags for the 3 core maintenance scenarios
"""

import json
import typer
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()
app = typer.Typer(help="SOFA Device Manager - Simple device maintenance")

# Add missing constants and function
SOURCES_DIR = Path("data/models/sources") 
OUTPUT_DIR = Path("data/resources")

# Smart defaults for guided device entry
DEVICE_PATTERNS = {
    "macos": {
        "processors": {
            "M4": ["tahoe", "sequoia"],
            "M3": ["tahoe", "sequoia", "sonoma"],
            "M2": ["tahoe", "sequoia", "sonoma", "ventura"],
            "M1": ["tahoe", "sequoia", "sonoma", "ventura", "monterey"],
        },
        "urls": {
            "MacBook Air": "https://support.apple.com/en-ca/HT201862",
            "MacBook Pro": "https://support.apple.com/en-ca/HT201300",
            "iMac": "https://support.apple.com/en-ca/HT201634",
            "Mac mini": "https://support.apple.com/en-ca/HT201894",
            "Mac Studio": "https://support.apple.com/en-ca/HT213073",
            "Mac Pro": "https://support.apple.com/en-ca/HT202888"
        }
    },
    "ios": {
        "processors": {"A18": ["18", "17", "16"], "A17": ["18", "17", "16"], "A16": ["18", "17", "16"], "A15": ["18", "17", "16"]},
        "url": "https://support.apple.com/en-ca/108044"
    },
    "ipados": {
        "processors": {"M4": ["18", "17", "16"], "M2": ["18", "17", "16"], "M1": ["18", "17", "16"], "A15": ["18", "17", "16"]},
        "url": "https://support.apple.com/en-ca/108043"
    },
    "watchos": {
        "processors": {"S10": ["11", "10"], "S9": ["11", "10", "9"], "S8": ["11", "10", "9"], "S7": ["11", "10", "9"]},
        "url": "https://support.apple.com/en-ca/108042"
    },
    "tvos": {
        "processors": {"A15": ["18", "17", "16"], "A12": ["18", "17", "16"], "A10X": ["18", "17", "16"]},
        "url": "https://support.apple.com/apple-tv"
    }
}

def _matches_filter(device_info, filter_str):
    """Check if device matches filter criteria"""
    filter_lower = filter_str.lower()
    for field in ["processorFamily", "processorType", "support_status", "marketingName"]:
        value = str(device_info.get(field, "")).lower()
        if filter_lower in value:
            return True
    return False

def rebuild_database():
    """Rebuild unified database from platform sources with hierarchical sorting"""
    console.print("🔨 Rebuilding unified database...", style="cyan")
    
    # Platform order: macOS first, then iPads, iOS, tvOS, watchOS  
    platform_order = ["macos", "ipados", "ios", "tvos", "watchos"]
    
    all_devices = {}
    platform_count = 0
    
    # Build devices in hierarchical order
    for platform in platform_order:
        platform_file = SOURCES_DIR / f"{platform}_devices.json"
        if platform_file.exists():
            with open(platform_file) as f:
                data = json.load(f)
                
                devices = data.get("devices", {})
                
                # Update metadata device_count to match actual count
                actual_count = len(devices)
                if data.get("metadata", {}).get("device_count", 0) != actual_count:
                    data["metadata"]["device_count"] = actual_count
                    # Write back corrected metadata
                    with open(platform_file, "w") as f_write:
                        json.dump(data, f_write, indent=2)
                
                # Preserve existing order from source files - no sorting
                # Only new devices added via add-device get placed at top of their platform file
                for device_id, device_data in devices.items():
                    all_devices[device_id] = device_data
                    
                platform_count += 1
    
    # Add any remaining platforms not in our order
    for source_file in SOURCES_DIR.glob("*_devices.json"):
        platform = source_file.stem.replace("_devices", "")
        if platform not in platform_order:
            with open(source_file) as f:
                data = json.load(f)
                devices = data.get("devices", {})
                
                # Update metadata device_count to match actual count
                actual_count = len(devices)
                if data.get("metadata", {}).get("device_count", 0) != actual_count:
                    data["metadata"]["device_count"] = actual_count
                    # Write back corrected metadata
                    with open(source_file, "w") as f_write:
                        json.dump(data, f_write, indent=2)
                
                # Preserve existing order from source files
                for device_id, device_data in devices.items():
                    all_devices[device_id] = device_data
                    
                platform_count += 1
    
    # Add metadata
    unified_db = {
        "_metadata": {
            "generated_at": datetime.now().isoformat(),
            "schema_version": "1.0",
            "total_devices": len(all_devices),
            "platforms_loaded": platform_count,
            "platform_order": platform_order,
            "source": "device_manager_script"
        }
    }
    
    # Add all devices in hierarchical order
    unified_db.update(all_devices)
    
    # Write unified JSON file - use OUTPUT_DIR constant
    output_file = OUTPUT_DIR / "all_devices_enhanced.json"
    with open(output_file, "w") as f:
        json.dump(unified_db, f, indent=2)
    
    # Write NDJSON file (one device per line)
    ndjson_file = OUTPUT_DIR / "all_devices_enhanced.ndjson"
    with open(ndjson_file, "w") as f:
        # Write metadata as first line
        f.write(json.dumps(unified_db["_metadata"]) + "\n")
        
        # Write each device as separate line
        for device_id, device_data in all_devices.items():
            device_record = {"device_id": device_id, **device_data}
            f.write(json.dumps(device_record) + "\n")
    
    json_size = f"{output_file.stat().st_size // 1024}KB"
    ndjson_size = f"{ndjson_file.stat().st_size // 1024}KB"
    
    console.print("✅ Database rebuilt successfully", style="green")
    console.print(f"   📊 {len(all_devices)} devices from {platform_count} platforms")
    console.print(f"   📄 JSON: {json_size} | NDJSON: {ndjson_size}")

@app.command()
def add_device(
    platform: str = typer.Argument(help="Platform: macos, ios, ipados, watchos, tvos"),
    device_id: str = typer.Argument(help="Device ID: Mac17,1, iPhone18,1, etc."),
    name: str = typer.Argument(help="Marketing name: 'iPhone 17 Pro', 'Mac Studio M4'"),
    processor: str = typer.Argument(help="Processor: 'M4 Max', 'A19 Pro', 'S10'"),
    os_version: str = typer.Option("", help="First OS version: '16.0', '19.0'")
):
    """Add new device (Scenario 1: New hardware ships)"""
    
    console.print(f"🆕 Adding new {platform} device: {device_id}", style="cyan")
    
    # Load platform file
    platform_file = Path(f"data/models/sources/{platform}_devices.json")
    
    if not platform_file.exists():
        console.print(f"❌ Platform file not found: {platform_file}", style="red")
        return
    
    with open(platform_file) as f:
        data = json.load(f)
    
    # Determine URLs and types
    url_mapping = {
        "macos": {
            "MacBook Air": "https://support.apple.com/en-ca/HT201862",
            "MacBook Pro": "https://support.apple.com/en-ca/HT201300", 
            "iMac": "https://support.apple.com/en-ca/HT201634",
            "Mac mini": "https://support.apple.com/en-ca/HT201894",
            "Mac Studio": "https://support.apple.com/en-ca/HT213073",
            "Mac Pro": "https://support.apple.com/en-ca/HT202888"
        },
        "ios": {"iPhone": "https://support.apple.com/iphone"},
        "ipados": {"iPad": "https://support.apple.com/ipad"},
        "watchos": {"Apple Watch": "https://support.apple.com/watch"},
        "tvos": {"Apple TV": "https://support.apple.com/apple-tv"}
    }
    
    # Determine device model from name
    model = "Unknown"
    url = "https://support.apple.com"
    device_type = "Unknown"
    
    if platform == "macos":
        for model_name in url_mapping["macos"].keys():
            if model_name.lower() in name.lower():
                model = model_name
                url = url_mapping["macos"][model_name] 
                device_type = "Desktop" if model_name in ["iMac", "Mac mini", "Mac Studio", "Mac Pro"] else "Laptop"
                break
    else:
        model_map = {"ios": "iPhone", "ipados": "iPad", "watchos": "Apple Watch", "tvos": "Apple TV"}
        model = model_map.get(platform, "Unknown")
        url = url_mapping.get(platform, {}).get(model, "https://support.apple.com")
        device_type_map = {"ios": "Phone", "ipados": "Tablet", "watchos": "Wearable", "tvos": "Set-Top Box"}
        device_type = device_type_map.get(platform, "Unknown")
    
    # Create new device entry
    new_device = {
        "Model": model,
        "URL": url,
        "deviceType": device_type,
        "processorFamily": processor,
        "processorType": "Apple Silicon" if any(x in processor for x in ["M1", "M2", "M3", "M4", "M5", "A15", "A16", "A17", "A18", "A19", "S8", "S9", "S10"]) else "Unknown",
        "marketingName": name,
        "support_status": "current",
        "DeviceID": device_id
    }
    
    if os_version:
        new_device["systemFirstRelease"] = os_version
    
    # Check for duplicate device ID
    devices = data.get("devices", {})
    if device_id in devices:
        console.print(f"❌ Device {device_id} already exists in {platform}", style="red")
        console.print(f"   Existing: {devices[device_id].get('marketingName', 'Unknown')}")
        console.print(f"💡 Use 'fix-device {device_id} <field> <value>' to update existing device")
        return
    
    # Add to devices (at the beginning for newest-first sorting)
    new_devices = {device_id: new_device}
    new_devices.update(devices)
    data["devices"] = new_devices
    
    # Update metadata
    data["metadata"]["device_count"] = len(new_devices)
    data["metadata"]["last_updated"] = "2025-09-07"
    
    # Write updated file
    with open(platform_file, "w") as f:
        json.dump(data, f, indent=2)
    
    console.print(f"✅ Added {device_id} to {platform_file.name}", style="green")
    console.print(f"   {name} ({processor})")
    
    # Rebuild database
    rebuild_database()

@app.command()
def add_guided():
    """Guided device creation with smart defaults and proper supportedMajor"""
    
    console.print("🤖 Guided Device Entry", style="bold blue")
    console.print("Smart defaults for proper SOFA device creation\n")
    
    # Platform selection
    platform = Prompt.ask(
        "📱 Platform", 
        choices=["macos", "ios", "ipados", "watchos", "tvos"],
        default="macos"
    )
    
    # Device ID
    device_id = Prompt.ask("🆔 Device ID (e.g., Mac17,1, iPhone19,1)")
    
    # Marketing Name 
    name = Prompt.ask("📛 Marketing Name (e.g., 'iPhone 18 Pro', 'MacBook Air M5')")
    
    # Show processor suggestions
    processors = list(DEVICE_PATTERNS.get(platform, {}).get("processors", {}).keys())
    if processors:
        console.print(f"💡 Suggested processors: {', '.join(processors)}")
    
    processor = Prompt.ask("⚡ Processor Family (e.g., M4, A18 Pro, S10)")
    
    # Smart supportedMajor suggestion
    patterns = DEVICE_PATTERNS.get(platform, {}).get("processors", {})
    suggested_os = None
    for proc_pattern, versions in patterns.items():
        if proc_pattern in processor:
            suggested_os = versions
            break
    
    if suggested_os:
        console.print(f"💡 Suggested supportedMajor: {suggested_os}")
        use_suggested = Confirm.ask("Use suggested OS versions?", default=True)
        if use_suggested:
            supported_major = suggested_os
        else:
            os_input = Prompt.ask("📟 Supported OS versions (comma-separated)")
            supported_major = [v.strip() for v in os_input.split(",")]
    else:
        os_input = Prompt.ask("📟 Supported OS versions (comma-separated)")
        supported_major = [v.strip() for v in os_input.split(",")]
    
    # Show preview and confirm
    console.print(f"\n📋 Preview: {device_id} - {name} ({processor})", style="bold cyan")
    console.print(f"📟 OS Support: {', '.join(supported_major)}")
    
    if Confirm.ask("\n✅ Add this device?", default=True):
        # Use existing add_device logic but with the collected data
        import subprocess
        import sys
        
        # Call the regular add-device command
        result = subprocess.run([
            sys.executable, "scripts/device_manager.py", "add-device", 
            platform, device_id, name, processor
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Now fix the supportedMajor to use our smart suggestion
            subprocess.run([
                sys.executable, "scripts/device_manager.py", "fix-device",
                device_id, "supportedMajor", json.dumps(supported_major)
            ], capture_output=True)
            
            console.print(f"✅ Added {device_id} with guided settings!", style="green")
            console.print(f"📟 OS Support: {', '.join(supported_major)}")
            
            # Post-processing validation
            console.print("\n🔍 Post-processing validation...", style="cyan")
            
            # Run check to ensure device was added correctly
            validation_result = subprocess.run([
                sys.executable, "scripts/device_manager.py", "check", 
                "--platform", platform
            ], capture_output=True, text=True)
            
            if "All devices have essential SOFA fields!" in validation_result.stdout:
                console.print("✅ Device validation passed", style="green")
            else:
                console.print("⚠️  Device may need additional fixes", style="yellow")
                if validation_result.stdout:
                    console.print(validation_result.stdout)
            
            # Show final status
            console.print("📊 Final database status:", style="dim")
            subprocess.run([sys.executable, "scripts/device_manager.py", "status"])
            
        else:
            console.print("❌ Failed to add device", style="red")
    else:
        console.print("❌ Cancelled", style="red")

@app.command() 
def drop_support(
    platform: str = typer.Argument(help="Platform: macos, ios, ipados, watchos"),
    processor_filter: str = typer.Argument(help="Processor to drop: 'Intel', 'A12', 'S4'"),
    final_version: str = typer.Argument(help="Final OS version: '15.7.2', '18.8.1'"),
    description: str = typer.Option("OS drops processor support", help="Description of change")
):
    """Drop OS support for processors (Scenario 2: OS drops devices)"""
    
    console.print(f"📱 Dropping {platform} support for {processor_filter}", style="yellow")
    
    # Load platform file
    platform_file = Path(f"data/models/sources/{platform}_devices.json")
    
    if not platform_file.exists():
        console.print(f"❌ Platform file not found: {platform_file}", style="red")
        return
    
    with open(platform_file) as f:
        data = json.load(f)
    
    devices = data.get("devices", {})
    updated_devices = []
    
    # Find and update matching devices
    for device_id, device_info in devices.items():
        # Use the helper function instead of manual matching
        matches = _matches_filter(device_info, processor_filter)
        
        # Only update current devices to vintage
        if matches and device_info.get("support_status") == "current":
            device_info["support_status"] = "vintage"
            device_info["systemLastRelease"] = final_version
            updated_devices.append((device_id, device_info.get("marketingName", "")))
    
    # Write updated file
    with open(platform_file, "w") as f:
        json.dump(data, f, indent=2)
    
    if updated_devices:
        console.print(f"✅ Updated {len(updated_devices)} devices to vintage:", style="green")
        for device_id, name in updated_devices[:5]:
            console.print(f"   • {device_id}: {name}")
        if len(updated_devices) > 5:
            console.print(f"   • ... and {len(updated_devices) - 5} more")
    else:
        console.print("ℹ️  No devices matched the filter", style="blue")
    
    # Rebuild database
    rebuild_database()

@app.command()
def fix_device(
    device_id: str = typer.Argument(help="Device ID to fix: Mac15,4, iPhone17,1"),
    field: str = typer.Argument(help="Field to fix: processorFamily, marketingName, etc."),
    value: str = typer.Argument(help="New value for the field")
):
    """Fix device information (Scenario 3: Fix mistakes)"""
    
    console.print(f"🔧 Fixing {device_id}: {field} = {value}", style="yellow")
    
    # Find which platform file contains the device
    sources_dir = Path("data/models/sources")
    device_found = False
    
    for platform_file in sources_dir.glob("*_devices.json"):
        with open(platform_file) as f:
            data = json.load(f)
        
        devices = data.get("devices", {})
        
        if device_id in devices:
            # Update the field - handle JSON arrays properly
            if field == "supportedMajor":
                try:
                    # Try to parse as JSON array
                    import json as json_module
                    devices[device_id][field] = json_module.loads(value)
                except json_module.JSONDecodeError:
                    # If not valid JSON, treat as string
                    devices[device_id][field] = value
            else:
                devices[device_id][field] = value
            
            # Write updated file
            with open(platform_file, "w") as f:
                json.dump(data, f, indent=2)
            
            console.print(f"✅ Fixed {device_id} in {platform_file.name}", style="green")
            console.print(f"   {field}: {value}")
            device_found = True
            break
    
    if not device_found:
        console.print(f"❌ Device {device_id} not found in any platform file", style="red")
        return
    
    # Rebuild database
    rebuild_database()

@app.command()
def search(
    query: str = typer.Argument(help="Search term: device ID, name, or processor"),
    platform: str = typer.Option("", help="Filter by platform: macos, ios, etc.")
):
    """Search for devices"""
    
    console.print(f"🔍 Searching devices for: '{query}'", style="cyan")
    
    found_devices = []
    
    for platform_file in SOURCES_DIR.glob("*_devices.json"):
        if platform and platform not in platform_file.stem:
            continue
            
        with open(platform_file) as f:
            data = json.load(f)
        
        devices = data.get("devices", {})
        platform_name = platform_file.stem.replace("_devices", "")
        
        for device_id, device_info in devices.items():
            # Search in device_id, name, processor
            searchable_text = f"{device_id} {device_info.get('marketingName', '')} {device_info.get('processorFamily', '')}".lower()
            
            if query.lower() in searchable_text:
                found_devices.append((platform_name, device_id, device_info))
    
    if found_devices:
        table = Table(title=f"Search Results for '{query}'")
        table.add_column("Platform", style="cyan")
        table.add_column("Device ID", style="yellow")
        table.add_column("Name", style="green") 
        table.add_column("Processor", style="blue")
        table.add_column("Status", style="magenta")
        
        for platform_name, device_id, device_info in found_devices:  # Show all results
            table.add_row(
                platform_name,
                device_id,
                device_info.get("marketingName", "")[:40],  # Truncate long names
                device_info.get("processorFamily", "")[:15],
                device_info.get("support_status", "")
            )
        
        console.print(table)
    else:
        console.print("❌ No devices found matching query", style="red")

@app.command()
def list_platform(
    platform: str = typer.Argument(help="Platform: macos, ios, ipados, watchos, tvos"),
    status: str = typer.Option("", help="Filter by status: current, vintage, obsolete"),
    processor: str = typer.Option("", help="Filter by processor: M3, A18, Intel")
):
    """List devices in a platform with optional filters"""
    
    console.print(f"📱 Listing {platform} devices", style="cyan")
    
    platform_file = SOURCES_DIR / f"{platform}_devices.json"
    
    if not platform_file.exists():
        console.print(f"❌ Platform file not found: {platform_file}", style="red")
        return
    
    with open(platform_file) as f:
        data = json.load(f)
    
    devices = data.get("devices", {})
    filtered_devices = []
    
    for device_id, device_info in devices.items():
        # Apply filters
        if status and device_info.get("support_status", "") != status:
            continue
        if processor and processor.lower() not in device_info.get("processorFamily", "").lower():
            continue
            
        filtered_devices.append((device_id, device_info))
    
    if filtered_devices:
        table = Table(title=f"{platform.title()} Devices")
        table.add_column("Device ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Processor", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("OS Versions", style="magenta")
        
        for device_id, device_info in filtered_devices:  # Show all devices
            supported_major = device_info.get("supportedMajor", [])
            os_versions = ", ".join(supported_major[:3]) + ("..." if len(supported_major) > 3 else "")
            
            table.add_row(
                device_id,
                device_info.get("marketingName", "")[:40],  # Slightly shorter for OS column
                device_info.get("processorFamily", "")[:15],
                device_info.get("support_status", ""),
                os_versions
            )
        
        console.print(table)
        console.print(f"\n📊 Found {len(filtered_devices)} devices")
    else:
        console.print("❌ No devices found with specified filters", style="red")

@app.command() 
def validate():
    """Validate device database for consistency"""
    
    console.print("🔍 Validating device database...", style="cyan")
    console.print(f"📂 Sources: {SOURCES_DIR}")
    
    issues = []
    total_devices = 0
    
    for platform_file in SOURCES_DIR.glob("*_devices.json"):
        platform = platform_file.stem.replace("_devices", "")
        
        with open(platform_file) as f:
            data = json.load(f)
        
        devices = data.get("devices", {})
        actual_count = len(devices)
        metadata_count = data.get("metadata", {}).get("device_count", 0)
        total_devices += actual_count
        
        # Check device count consistency
        if actual_count != metadata_count:
            issues.append(f"{platform}: device_count mismatch (metadata: {metadata_count}, actual: {actual_count})")
        
        for device_id, device_info in devices.items():
            # Check required fields
            required_fields = ["Model", "URL", "marketingName", "support_status", "DeviceID"]
            for field in required_fields:
                if not device_info.get(field):
                    issues.append(f"{platform}:{device_id} missing {field}")
            
            # Check device ID consistency
            if device_info.get("DeviceID") != device_id:
                issues.append(f"{platform}:{device_id} DeviceID mismatch")
            
            # Check support status values
            valid_statuses = ["current", "vintage", "obsolete"]
            if device_info.get("support_status") not in valid_statuses:
                issues.append(f"{platform}:{device_id} invalid support_status")
    
    if issues:
        console.print(f"⚠️  Found {len(issues)} validation issues:", style="yellow")
        for issue in issues[:10]:  # Show first 10 issues
            console.print(f"   • {issue}", style="red")
        if len(issues) > 10:
            console.print(f"   • ... and {len(issues) - 10} more issues")
    else:
        console.print(f"✅ Database validation passed", style="green")
        console.print(f"   📊 {total_devices} devices across {len(list(SOURCES_DIR.glob('*_devices.json')))} platforms")

@app.command()
def status():
    """Show device database status"""
    
    console.print("📊 SOFA Device Database Status", style="bold blue")
    console.print(f"📂 Sources: {SOURCES_DIR}")
    console.print(f"📁 Output: {OUTPUT_DIR}\n")
    
    # Check platform files
    if SOURCES_DIR.exists():
        table = Table(title="Platform Files")
        table.add_column("Platform", style="cyan")
        table.add_column("Devices", style="yellow") 
        table.add_column("Current", style="green")
        table.add_column("Vintage", style="orange3")
        table.add_column("File Size", style="blue")
        
        total_devices = 0
        total_current = 0
        total_vintage = 0
        
        for platform_file in SOURCES_DIR.glob("*_devices.json"):
            try:
                with open(platform_file) as f:
                    data = json.load(f)
                
                devices = data.get("devices", {})
                device_count = len(devices)
                current_count = sum(1 for d in devices.values() if d.get("support_status") == "current")
                vintage_count = sum(1 for d in devices.values() if d.get("support_status") == "vintage")
                file_size = f"{platform_file.stat().st_size // 1024}KB"
                platform = platform_file.stem.replace("_devices", "")
                
                table.add_row(platform, str(device_count), str(current_count), str(vintage_count), file_size)
                total_devices += device_count
                total_current += current_count
                total_vintage += vintage_count
            except:
                table.add_row(platform_file.stem, "Error", "Error", "Error", "Error")
        
        console.print(table)
        
        # Show totals
        console.print(f"\n📊 Totals: {total_devices} devices ({total_current} current, {total_vintage} vintage)")
        
        # Check unified database files
        json_file = OUTPUT_DIR / "all_devices_enhanced.json"
        ndjson_file = OUTPUT_DIR / "all_devices_enhanced.ndjson"
        
        if json_file.exists() and ndjson_file.exists():
            json_size = f"{json_file.stat().st_size // 1024}KB"
            ndjson_size = f"{ndjson_file.stat().st_size // 1024}KB"
            console.print(f"✅ Unified Files: JSON ({json_size}) | NDJSON ({ndjson_size})")
        else:
            console.print("❌ Unified database files missing")
    else:
        console.print("❌ Sources directory not found", style="red")

@app.command()
def rebuild():
    """Rebuild unified database from platform sources"""
    console.print("🔨 Rebuilding from sources...", style="bold cyan")
    console.print(f"📂 Sources: {SOURCES_DIR}")
    console.print(f"📁 Output: {OUTPUT_DIR}")
    rebuild_database()

def _check_essential_fields(device_info):
    """Check if device has essential SOFA fields"""
    issues = []
    
    # Essential fields for SOFA
    essential_fields = {
        "processorFamily": "Add processor (e.g., 'M4', 'A18', 'S9')",
        "marketingName": "Add marketing name", 
        "supportedMajor": "Add supported OS versions",
        "DeviceID": "Add device ID"
    }
    
    for field, suggestion in essential_fields.items():
        value = device_info.get(field, [])
        if not value or value == [] or value == "":
            issues.append(f"Missing {field} - {suggestion}")
    
    # Check for placeholder values
    supported_major = device_info.get("supportedMajor", [])
    if supported_major == ["current"]:
        issues.append("Invalid supportedMajor: ['current'] - use specific versions")
    
    return issues

@app.command()
def check(
    platform: str = typer.Option("", help="Check specific platform only"),
    fix_suggestions: bool = typer.Option(True, help="Show fix suggestions")
):
    """Check device database for essential SOFA fields"""
    
    console.print("🔍 Checking device database for essential fields...", style="cyan")
    
    total_devices = 0
    total_issues = 0
    platform_issues = {}
    
    platforms_to_check = [platform] if platform else ["macos", "ios", "ipados", "watchos", "tvos", "visionos"]
    
    for platform_name in platforms_to_check:
        platform_file = SOURCES_DIR / f"{platform_name}_devices.json"
        
        if not platform_file.exists():
            if platform:  # Only warn if specific platform requested
                console.print(f"⚠️  Platform file not found: {platform_name}", style="yellow")
            continue
            
        with open(platform_file) as f:
            data = json.load(f)
        
        devices = data.get("devices", {})
        problem_devices = {}
        
        for device_id, device_info in devices.items():
            total_devices += 1
            
            # Check essential SOFA fields
            field_issues = _check_essential_fields(device_info)
            if field_issues:
                problem_devices[device_id] = {
                    "device_info": device_info,
                    "issues": field_issues
                }
                total_issues += len(field_issues)
        
        if problem_devices:
            platform_issues[platform_name] = problem_devices
    
    # Display results
    if total_issues == 0:
        console.print("✅ All devices have essential SOFA fields!", style="green")
        console.print(f"   📊 Checked {total_devices} devices - all complete")
        return
        
    console.print(f"⚠️  Found {total_issues} missing fields across {len(platform_issues)} platforms", style="yellow")
    
    for platform_name, problem_devices in platform_issues.items():
        console.print(f"\n📱 {platform_name.upper()} Issues:", style="bold magenta")
        
        for device_id, device_data in problem_devices.items():
            device_info = device_data["device_info"]
            issues = device_data["issues"]
            
            console.print(f"  • {device_id} ({device_info.get('marketingName', 'Unknown')})", style="cyan")
            
            for issue in issues:
                console.print(f"    ❌ {issue}", style="red")
    
    # Simple summary
    console.print(f"\n💡 Use guided entry: uv run scripts/device_manager.py add-guided", style="dim")


@app.command()
def cleanup_vintage(
    platform: str = typer.Option("", help="Platform to clean (or all)"),
    dry_run: bool = typer.Option(True, help="Show what would be removed without removing")
):
    """Remove vintage and obsolete devices from sources to reduce maintenance burden"""
    
    console.print("🧹 Cleaning vintage devices from sources...", style="cyan")
    
    if dry_run:
        console.print("🔍 DRY RUN - Showing what would be removed", style="yellow")
    
    platforms_to_clean = [platform] if platform else ["macos", "ios", "ipados", "watchos", "tvos", "visionos"]
    
    total_removed = 0
    
    for platform_name in platforms_to_clean:
        platform_file = SOURCES_DIR / f"{platform_name}_devices.json"
        
        if not platform_file.exists():
            continue
            
        with open(platform_file) as f:
            data = json.load(f)
        
        devices = data.get("devices", {})
        original_count = len(devices)
        
        # Find vintage/obsolete devices
        to_remove = []
        for device_id, device_info in devices.items():
            status = device_info.get("support_status", "")
            if status in ["vintage", "obsolete"]:
                to_remove.append((device_id, device_info.get("marketingName", "Unknown")))
        
        if to_remove:
            console.print(f"\n📱 {platform_name.upper()} - Removing {len(to_remove)} vintage/obsolete devices:", style="bold magenta")
            
            for device_id, name in to_remove[:10]:  # Show first 10
                console.print(f"  🗑️  {device_id}: {name[:50]}", style="red")
            
            if len(to_remove) > 10:
                console.print(f"  ... and {len(to_remove) - 10} more devices", style="dim")
            
            if not dry_run:
                # Actually remove them
                for device_id, _ in to_remove:
                    del devices[device_id]
                
                # Update metadata
                data["metadata"]["device_count"] = len(devices)
                data["metadata"]["last_updated"] = "2025-09-07"
                
                # Write back
                with open(platform_file, "w") as f:
                    json.dump(data, f, indent=2)
                
                console.print(f"  ✅ Cleaned {platform_file.name}: {original_count} → {len(devices)} devices", style="green")
            
            total_removed += len(to_remove)
        else:
            console.print(f"\n📱 {platform_name.upper()}: No vintage/obsolete devices found", style="green")
    
    if dry_run:
        console.print(f"\n🔍 Would remove {total_removed} vintage/obsolete devices", style="yellow")
        console.print("💡 Run with --no-dry-run to actually remove them", style="dim")
    else:
        console.print(f"\n✅ Removed {total_removed} vintage/obsolete devices", style="green")
        console.print("🔨 Rebuilding unified database...", style="cyan")
        rebuild_database()

if __name__ == "__main__":
    app()
