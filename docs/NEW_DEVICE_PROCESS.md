# Adding New Apple Hardware to SOFA

When Apple ships new hardware, SOFA needs to know about it so feeds, DMS consumers, and Nudge enforcement work correctly.

## How it works

Three data sources combine to resolve and validate devices:

- **GDMF** (`gdmf.apple.com/v2/pmv`) — Apple's signing server. Lists board IDs per OS version. Refreshed by `sofa-gather gdmf`.
- **Overrides** (`config/model_overrides.json`) — Hand-maintained fallback for devices AppleDB doesn't cover (VMs, Intel Macs, brand-new unreleased hardware).
- **AppleDB** (`github.com/littlebyteorg/appledb`) — For cross  validated we use a community-maintained device database. This helps map board IDs to marketing names, identifiers, SoC info.


## Quick reference: which files do what

| File | Source | Purpose |
|------|--------|---------|
| `config/model_overrides.json` | Manual | Device corrections and additions not in AppleDB |
| `data/models/model_identifier_*.json` | Generated | Per-OS device lists consumed by feed builders |
| `data/models/macos_devices.json` | Generated | Upstream SOFA format with all macOS devices |
| `data/models/mac_models_mapping.json` | Generated | Board ID → marketing name lookup for macOS |
| `data/models/device_identifiers.json` | Generated | All-platform identifier → marketing name lookup |
| `data/models/supported_devices_v1.json` | Generated | V1 feed format device lists |
| `data/resources/gdmf_device_baseline.json` | Generated + accumulated | Per-version device counts for Nudge compatibility |

## When Apple ships new Mac hardware

### 1. Pull latest AppleDB fro validation and chcek board ID mapping

```bash
cd /path/to/appledb
git pull
```

Check for new device files appear in `deviceFiles/` (e.g., `deviceFiles/Macbook Pro/Mac18,1.json`).

### 2. Gather fresh GDMF

```bash
bin/sofa-gather gdmf
```

New board IDs appear in `data/resources/gdmf_cached.json`.

### 3. (Re-)Generate model data

```bash
bin/sofa-models generate \
  --repo-path /path/to/appledb \
  --strict \
  --diff-previous \
  --compare https://raw.githubusercontent.com/macadmins/sofa/main/data/models/sources/macos_devices.json
```

This will:
- Scan AppleDB for the new device
- Cross-reference with GDMF for OS version support
- Show what changed (`--diff-previous`)
- Compare against the public SOFA data (`--compare`)
- Fail if any GDMF board ID can't be resolved (`--strict`)

### 4. If `--strict` fails

In case a new board ID appeared in GDMF that AppleDB doesn't have yet (as happened in MacBook Neo release). Add it to overrides:

```bash
# Edit config/model_overrides.json
# Add entry keyed by board ID:
{
  "J900AP": {
    "identifier": "Mac18,1",
    "name": "MacBook Pro (16-inch, M6, 2027)",
    "type": "MacBook Pro",
    "soc": "M6",
    "board": "J900AP",
    "arch": "arm64e"
  }
}
```

Then re-run `sofa-models generate --strict`.

### 5. Validate

```bash
# Compare device counts against production
bin/sofa-models generate \
  --repo-path /path/to/appledb \
  --compare https://raw.githubusercontent.com/macadmins/sofa/main/data/models/sources/macos_devices.json

# Build feeds and verify
bin/sofa-build all

# Check per-version device counts match expectations
python3 -c "
import json
with open('data/feeds/v2/macos_data_feed.json') as f:
    d = json.load(f)
for ov in d['OSVersions']:
    latest = ov['Latest']
    print(f'{ov[\"OSVersion\"]}: {latest[\"ProductVersion\"]} — {len(latest.get(\"SupportedDevices\",[]))} devices')
"
```

### 6. Copy updated files

```bash
# Model identifier files
cp data/models/model_identifier_*.json /path/to/sofa/data/models/legacy/

# Supported devices (v1 format)
cp data/models/supported_devices_v1.json /path/to/sofa/data/models/legacy/supported_devices.json

# Upstream source format
cp data/models/macos_devices.json /path/to/sofa/data/models/sources/

# Overrides (if changed)
cp config/model_overrides.json /path/to/sofa/config/
```

## When a new non-Mac device ships (iPhone, iPad, Watch, Vision Pro)

Non-Mac devices use their identifier directly (iPhone17,1, iPad16,3) not board IDs. Again AppleDB has them usually listed, we keep a flat copy here in our repo.

### 1. Regenerate device_identifiers.json

```bash
python3 -c "
import json, glob

lookup = {}
for f in glob.glob('/path/to/appledb/deviceFiles/**/*.json', recursive=True):
    try:
        with open(f) as fh:
            d = json.load(fh)
        ident = d.get('identifier', '')
        name = d.get('name', '')
        if ident and name:
            if isinstance(ident, list):
                for i in ident:
                    lookup[i] = name
            else:
                lookup[ident] = name
    except:
        pass

with open('data/models/device_identifiers.json', 'w') as f:
    json.dump(lookup, f, indent=2)
print(f'Wrote {len(lookup)} device identifiers')
"
```

### 2. Copy to sofa

```bash
cp data/models/device_identifiers.json /path/to/sofa/data/models/
```

### 3. Rebuild feeds

```bash
bin/sofa-build all
```

The DMS consumer feed (`dms_consumers.json`) will resolve the new device automatically.

## CI/CD safety net

The automated pipeline uses `--strict --min-version 12` to catch new hardware:

```bash
sofa-models generate \
  --repo-path ../appledb \
  --strict \
  --min-version 12 \
  --diff-previous
```

- New Mac board ID in GDMF (macOS 12+) that can't be resolved → pipeline fails → update overrides or pull AppleDB
- Old Big Sur (macOS 11) board IDs are ignored (`--min-version 12`)

## Device baseline (Nudge compatibility)

`data/resources/gdmf_device_baseline.json` stores per-version device counts seeded from production. This ensures older OS versions don't get inflated with hardware that didn't exist when they shipped. The baseline updates automatically on each build — new GDMF data merges in, counts only grow forward within a major version.

If the baseline seems wrong, re-seed from production:

```bash
python3 -c "
import json, subprocess
result = subprocess.run(['curl', '-s', 'https://sofafeed.macadmins.io/v2/macos_data_feed.json'],
                       capture_output=True, text=True, timeout=30)
prod = json.loads(result.stdout)
baseline = {}
for ov in prod['OSVersions']:
    baseline[ov['Latest']['ProductVersion']] = sorted(ov['Latest'].get('SupportedDevices', []))
    for sr in ov.get('SecurityReleases', []):
        baseline[sr['ProductVersion']] = sorted(sr.get('SupportedDevices', []))
with open('data/resources/gdmf_device_baseline.json', 'w') as f:
    json.dump(baseline, f, indent=2)
print(f'Seeded {len(baseline)} version baselines from prod')
"
```
