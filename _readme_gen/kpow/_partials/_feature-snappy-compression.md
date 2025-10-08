We preset an attribute for Snappy compression in read-only filesystems. It is disabled by default and can be enabled -
modify the volume configuration if necessary.

```yaml
ephemeralTmp:
  enabled: true
  volume:
    emptyDir:
      medium: Memory # Optional: for better performance
      sizeLimit: "100Mi" # Configurable size
```
