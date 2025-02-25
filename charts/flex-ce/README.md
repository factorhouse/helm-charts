# Run Flex Community Edition for Apache Flink in Kubernetes

[Flex Community Edition](https://factorhouse.io/flex) is a free, developer focused toolkit for Apache Flink.

Starting now, individuals can use Flex CE for free, even at work. Organisations can install Flex CE in up to three
non-production environments.

Each installation of Flex CE can manage one Flink Cluster. See
our [feature matrix](https://factorhouse.io/flex/features/) for more information.

This Helm chart uses the [factorhouse/flex-ce](https://hub.docker.com/r/factorhouse/flex-ce) container from Dockerhub.

## Get Repo Info

```bash
helm repo add factorhouse https://charts.factorhouse.io
helm repo update
```

## Installing the Chart

To install the chart with the release name `my-flex-ce`:

```bash
helm install my-flex-ce factorhouse/flex-ce
```

## Uninstalling the Chart

To uninstall/delete the `my-flex-ce` deployment:

```bash
helm delete my-flex-ce
```

The command removes all the Kubernetes components associated with the chart and deletes the release
