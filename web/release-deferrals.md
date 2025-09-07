# Release Deferrals

<ReleaseDeferralTable />

## About Release Deferrals

Release deferrals allow organizations to delay the visibility of software updates to end users. This gives IT teams time to test updates before deployment while ensuring devices eventually receive critical security patches.

### Deferral Periods

- **14 Days**: Minimal testing period for critical updates
- **30 Days**: Standard testing period for most organizations  
- **60 Days**: Extended testing for complex environments
- **90 Days**: Maximum deferral for thorough validation

### Best Practices

1. **Test Early**: Begin testing as soon as updates are released
2. **Staged Rollout**: Deploy to pilot groups before organization-wide
3. **Monitor Deferrals**: Track upcoming expirations to avoid surprises
4. **Document Issues**: Keep records of compatibility problems found during testing

### MDM Configuration

Most MDM solutions support configuring deferral periods through:
- Configuration profiles (macOS)
- Restriction profiles (iOS/iPadOS)
- Software update policies

Refer to your MDM vendor's documentation for specific implementation details.