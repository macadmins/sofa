---
title: macOS Installer Information
platform: macOS
layout: doc
---

# macOS Installer Information <Badge type="info" text="Latest Updates" />

::: info Latest macOS Installer Information
This page provides information and links to the latest macOS installers, the Unified Mac Assistant (UMA), and macOS IPSW.
:::

### macOS Restore IPSW (latest macOS)

Apple Silicon Macs can be restored using the IPSW restore file with Apple Configurator 2.

### Unified Mac Assistant (UMA) - InstallAssistant.pkg 

The only update or upgrade installation Apple supports on a running computer (besides from System Settings -> General -> Software Update) is via a package referred to as the Unified Mac Assistant or UMA. Once downloaded, installing the package places the `Install macOS <Version Name>` application bundle in the Applications folder. This would be the same as a full installation app you'd get from the (Mac) App Store. 


<script setup>
import ReleaseInfoTable from './components/ReleaseInstallerTable.vue';
</script>

## Release Information Table

The table below shows the latest macOS releases and provides download links for the UMA and IPSW installation files.

More IPSW files are available here [Apple DB an database of Apple software and devices](https://appledb.dev/firmware.html)

<ReleaseInfoTable />
