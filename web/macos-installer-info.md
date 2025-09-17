# macOS Installers

<ReleaseInstallerTable />

## Installation Methods

### IPSW Files (Apple Silicon)
IPSW files are firmware restore images designed for Apple Silicon Macs (M1, M2, M3, and newer). These files:
- Can be used with Apple Configurator 2 for restoration
- Support DFU (Device Firmware Update) mode recovery
- Include the complete macOS system and recovery partition
- Are approximately 13-15 GB in size

### PKG Files (Universal)
PKG installer packages work on all Mac models and contain the full macOS installer application. These files:
- Can be deployed via MDM solutions
- Support command-line installation with `installer`
- Create a bootable installer when extracted
- Work on both Intel and Apple Silicon Macs

## Creating Bootable Media

### Using Terminal
```bash
sudo /Applications/Install\ macOS\ Sequoia.app/Contents/Resources/createinstallmedia \
  --volume /Volumes/MyVolume
```

### Requirements
- USB drive with at least 16 GB capacity
- Administrator privileges
- Full macOS installer application

## Deployment Best Practices

### Enterprise Deployment
1. **Test thoroughly** before mass deployment
2. **Stage rollouts** to pilot groups first
3. **Maintain backups** before major upgrades
4. **Document compatibility** issues with critical software

### MDM Integration
Most MDM solutions support:
- Caching content locally
- Scheduling installation windows
- Enforcing minimum OS versions
- Deferring updates as needed

## Useful Resources

- [Apple Support - Create bootable installer](https://support.apple.com/guide/mac-help/create-a-bootable-installer-mh27903/mac)
- [Apple Developer - Installation](https://developer.apple.com/documentation/installation)
- [Mr. Macintosh - IPSW Database](https://mrmacintosh.com/)

## Compatibility Notes

### System Requirements
Always verify hardware compatibility before upgrading:
- Check minimum RAM requirements (typically 8 GB)
- Ensure adequate storage space (35-45 GB free)
- Verify Mac model compatibility on Apple's website

### Known Issues
Consult release notes and community forums for:
- Third-party software compatibility
- Driver updates for peripherals
- Network configuration changes
- Security software updates