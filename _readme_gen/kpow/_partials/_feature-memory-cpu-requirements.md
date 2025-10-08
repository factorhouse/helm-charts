The chart runs Kpow with Guaranteed QoS, having resource request and limit set to these values by default:

```yaml
resources:
  limits:
    cpu: 2
    memory: 8Gi
  requests:
    cpu: 2
    memory: 8Gi
```

These default resource settings are conservative, suited to a deployment of Kpow that manages multiple Kafka clusters and associated resources.

When running Kpow with a single Kafka cluster you can experiment with reducing those resources as far as our suggested minimum:

#### Minimum Resource Requirements

```yaml
resources:
  limits:
    cpu: 1
    memory: 2Gi
  requests:
    cpu: 1
    memory: 2Gi
```
