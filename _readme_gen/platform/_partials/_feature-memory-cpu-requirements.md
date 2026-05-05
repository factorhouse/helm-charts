The chart runs Factor Platform with Guaranteed QoS, having resource request and limit set to these values by default:

```yaml
resources:
  limits:
    cpu: 2
    memory: 8Gi
  requests:
    cpu: 2
    memory: 8Gi
```

These default resource settings are conservative and are intended for deployments of the Factor Platform that manage multiple Kafka and Flink clusters along with their associated resources.

If you're running the Factor Platform with a single Kafka and Flink cluster, you can experiment with reducing resource allocations down to our suggested minimum:

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
