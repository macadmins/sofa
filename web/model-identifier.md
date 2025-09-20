# Mac Model Identifiers

<ModelIdentifierTable />

## About Model Identifiers

Model identifiers are unique codes that macOS uses to identify specific Mac hardware configurations. These identifiers are essential for:

- **System Management**: MDM and deployment tools use these to target specific hardware
- **Compatibility Checks**: Determining which macOS versions support specific models
- **Asset Management**: Tracking and inventorying Mac fleets
- **Support Documentation**: Finding model-specific troubleshooting guides

## Understanding the Format

### Identifier Structure
Model identifiers follow patterns like:
- `MacBookPro18,3` - MacBook Pro with M1 Pro chip
- `iMac21,1` - 24-inch iMac with M1 chip
- `Mac15,12` - MacBook Air with M3 chip

The numbers generally indicate:
- **First number**: Generation or major revision
- **Second number**: Specific configuration within that generation

### Chip Architecture
- **Apple Silicon** (M1, M2, M3): Latest Mac models with ARM-based processors
- **Intel**: Previous generation Macs with x86 processors

## How to Find Your Model Identifier

### Using Terminal
```bash
system_profiler SPHardwareDataType | grep "Model Identifier"
```

### Using System Information
1. Hold Option and click Apple menu
2. Select "System Information"
3. Look for "Model Identifier" under Hardware

### Using About This Mac
1. Click Apple menu > About This Mac
2. Click "System Report"
3. Find "Model Identifier" in the Hardware Overview

## Using This Information

### For IT Administrators
- Deploy OS-specific configurations based on hardware
- Create smart groups in MDM solutions
- Plan hardware refresh cycles
- Verify compatibility before upgrades

### For Developers
- Test app compatibility across hardware
- Optimize for specific chip architectures
- Debug hardware-specific issues

## Related Resources

- [Apple Support - Identify your Mac model](https://support.apple.com/en-us/HT201581)
- [EveryMac - Mac Model Lookup](https://everymac.com/ultimate-mac-lookup/)
- [macOS Compatibility Checker](https://support.apple.com/en-us/HT211238)