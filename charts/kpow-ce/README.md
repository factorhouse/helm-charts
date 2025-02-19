# Run Kpow Community Edition for Apache Kafka in Kubernetes

[Kpow Community Edition](https://kpow.io) is a free, developer focused toolkit for Apache Kafka clusters, schema
registries, and connect installations.

Starting today, individuals can use Kpow CE for free, even at work. Organisations can install Kpow CE in up to three
non-production environments.

Each installation of Kpow CE can manage one Kafka Cluster, one Schema Registry, and one Connect cluster. See
our [feature matrix](https://factorhouse.io/blog/articles/kpow-community-edition/) for more information.

This Helm chart uses the [factorhouse/kpow-ce](https://hub.docker.com/r/factorhouse/kpow-ce) container from Dockerhub.

## Get Repo Info

```bash 
helm repo add factorhouse https://charts.factorhouse.io
helm repo update
```

## Installing the Chart

To install the chart with the release name `my-kpow-ce`:

```bash 
helm install my-kpow-ce factorhouse/kpow-ce
```

## Uninstalling the Chart

To uninstall/delete the `my-kpow-ce` deployment:

```bash 
helm delete my-kpow-ce
```

The command removes all the Kubernetes components associated with the chart and deletes the release
