# Run Kpow Community Edition for Apache Kafka with Kubernetes

[Kpow](https://factorhouse.io/kpow/) is the all-in-one toolkit to manage, monitor, and learn about your Kafka resources.

This Helm chart uses the [factorhouse/kpow-ce](https://hub.docker.com/r/factorhouse/kpow-ce) container from Dockerhub.

# Helm Charts

This repository contains a single Helm chart that uses the [factorhouse/kpow-ce](https://hub.docker.com/r/factorhouse/kpow-ce) container on Dockerhub.

- [Prerequisites](#prerequisites)
- [Kubernetes](#kubernetes)
- [Run Kpow in Kubernetes](#run-kpow-in-kubernetes)
  - [Configure the Kpow Helm Repository](#configure-the-kpow-helm-repository)
  - [Start a Kpow Instance](#start-a-kpow-instance)
  - [Manage a Kpow Instance](#manage-a-kpow-instance)
  - [Start Kpow with Local Changes](#start-kpow-with-local-changes)
  - [Manage Sensitive Environment Variables](#manage-sensitive-environment-variables)
  - [Provide Files to the Kpow Pod](#provide-files-to-the-kpow-pod)
  - [Kpow Memory and CPU Requirements](#kpow-memory-and-cpu-requirements)
  - [Snappy compression in read-only filesystem](#snappy-compression-in-read-only-filesystem)

## Prerequisites

The minimum information Kpow requires to operate is:

- **License Details**: Request a [community license](https://factorhouse.io/kpow/community/).
- **Kafka Bootstrap URL**

See the [Kpow Documentation](https://docs.factorhouse.io/kpow/getting-started) for a full list of configuration options.

## Kubernetes

@@include(\_partials/\_configure-eks-environment.md)

## Run Kpow in Kubernetes

### Configure the Kpow Helm Repository

@@include(\_partials/\_configure-helm-kpow.md)

### Start a Kpow Instance

#### Start Kpow with config from '--set env.XYZ'

##### Quotation

When using `helm install`, you can pass configuration with the `--set env.XYZ` flag. This requires careful formatting for certain values.

Some fields, particularly integers and strings containing quotation marks, require quoting. You may also need to escape special characters (like commas or nested quotes) with a backslash (`\`). For more details, see Helm's documentation on [The Format and Limitations of `--set`](https://helm.sh/docs/intro/using_helm/#the-format-and-limitations-of---set).

The following example shows how to install Kpow from the command line, highlighting how to handle escaped commas and quotes:

```bash
helm install kpow factorhouse/kpow-ce \
  --set env.LICENSE_ID="00000000-0000-0000-0000-000000000001" \
  --set env.LICENSE_CODE="KPOW_COMMUNITY" \
  --set env.LICENSEE="Doe\, Jane" \ # <-- note the escaped comma
  --set env.LICENSE_EXPIRY="2022-01-01" \
  --set env.LICENSE_SIGNATURE="638......A51" \
  --set env.BOOTSTRAP="127.0.0.1:9092\,127.0.0.1:9093\,127.0.0.1:9094" # <-- note the escaped commas
  --create-namespace --namespace factorhouse

NAME: kpow
LAST DEPLOYED: Mon May 31 17:22:21 2021
NAMESPACE: factorhouse
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace factorhouse -l "app.kubernetes.io/name=kpow,app.kubernetes.io/instance=kpow" -o jsonpath="{.items[0].metadata.name}")
  echo "Visit http://127.0.0.1:3000 to use your application"
  kubectl --namespace factorhouse port-forward $POD_NAME 3000:3000
```

#### Start Kpow with Environment Variables from a ConfigMap

You can configure Kpow with a ConfigMap of environment variables as follows:

```bash
helm install kpow factorhouse/kpow-ce \
  --set envFromConfigMap=kpow-config \
  --create-namespace --namespace factorhouse
```

This approach requires a `ConfigMap` named `kpow-config` to already exist in the `factorhouse` namespace. To configure Kpow with a local ConfigMap template, see [Configuring with an Existing ConfigMap](#configuring-with-an-existing-configmap). You can also refer to [kpow-config.yaml.example](./kpow-config.yaml.example) for a sample ConfigMap manifest.

For general guidance, see the Kubernetes documentation on [configuring all key-value pairs in a ConfigMap as environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables).

### Manage a Kpow Instance

@@include(\_partials/\_feature-manage-kpow-instance.md)

### Start Kpow with Local Changes

You can run Kpow with local edits to these charts and provide local configuration when running Kpow.

#### Pull and Untar the Kpow Charts

```bash
helm pull factorhouse/kpow-ce --untar --untardir .
```

#### Make Local Edits

Make any edits required to `kpow-ce/Chart.yaml` or `kpow-ce/values.yaml` (adding volume mounts, etc).

#### Run Local Charts

The command to run local charts is slightly different, see `./kpow-ce` rather than `factorhouse/kpow-ce`.

```bash
helm install kpow ./kpow-ce \
  <.. --set configuration, etc ..> \
  --create-namespace -namespace factorhouse
```

#### Configuring with an Existing ConfigMap

This is the recommended method for managing configuration separately from the Helm chart.

**1. Prepare Your ConfigMap Manifest**

Copy the example file ([kpow-config.yaml.example](./kpow-config.yaml.example)), then edit it to set your desired `metadata.name` (e.g., `kpow-config`) and fill in your configuration under the `data` section.

```bash
cp ./kpow-ce/kpow-config.yaml.example kpow-config.yaml
# now edit kpow-config.yaml
```

**2. Create the ConfigMap in Kubernetes**

Before installing, use `kubectl` to create the `ConfigMap` object in your cluster from the file you just prepared.

```bash
kubectl apply -f kpow-config.yaml --namespace factorhouse
```

**3. Install the Chart**

Install the Helm chart, using `--set` to reference the name of the `ConfigMap` you just created. The `--create-namespace` flag will ensure the target namespace exists.

```bash
helm install kpow ./kpow-ce \
  --set envFromConfigMap=kpow-config \
  --create-namespace --namespace factorhouse
```

The Kpow pod will now start using the environment variables from your externally managed `ConfigMap`.

See [kpow-config.yaml.example](./kpow-config.yaml.example) for an example ConfigMap file.

See the Kubernetes documentation on [configuring all key-value pairs in a config map as container environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables) for more information.

### Manage Sensitive Environment Variables

@@include(\_partials/\_feature-manage-sensitive-env-vars.md)

```bash
helm install kpow ./kpow-ce \
  --set envFromSecret=kpow-secrets \
  --set envFromConfigMap=kpow-config \
  --create-namespace --namespace factorhouse
```

### Provide Files to the Kpow Pod

@@include(\_partials/\_feature-provide-files-to-kpow-pod.md)

### Kpow Memory and CPU Requirements

@@include(\_partials/\_feature-memory-cpu-requirements.md)

Adjust these values from the command line like so:

```bash
helm install kpow factorhouse/kpow-ce \
     --set resources.limits.cpu=1 \
     --set resources.limits.memory=2Gi \
     --set resources.requests.cpu=1 \
     --set resources.requests.memory=2Gi \
     --create-namespace --namespace factorhouse
```

We recommend always having limits and requests set to the same value, as this set Kpow in Guaranteed QoS and provides a much more reliable operation.

#### Snappy compression in read-only filesystem

@@include(\_partials/\_feature-snappy-compression.md)

---

@@include(\_partials/\_general-footer.md)
