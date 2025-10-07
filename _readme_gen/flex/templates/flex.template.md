# Run Flex for Apache Flink in Kubernetes

[Flex](https://factorhouse.io/flex) is the all-in-one toolkit to manage, monitor, and learn about your Flink resources.

This Helm chart uses the [factorhouse/flex](https://hub.docker.com/r/factorhouse/flex) container from Dockerhub.

# Helm Charts

This repository contains a single Helm chart that uses the [factorhouse/flex](https://hub.docker.com/r/factorhouse/flex)
container on Dockerhub.

- [Prerequisites](#prerequisites)
- [Kubernetes](#kubernetes)
- [Run Flex in Kubernetes](#run-flex-in-kubernetes)
  - [Configure the Flex Helm Repository](#configure-the-flex-helm-repository)
  - [Start a Flex Instance](#start-a-flex-instance)
  - [Manage a Flex Instance](#manage-a-flex-instance)
  - [Start Flex with Local Changes](#start-flex-with-local-changes)
  - [Manage Sensitive Environment Variables](#manage-sensitive-environment-variables)
  - [Provide Files to the Flex Pod](#provide-files-to-the-flex-pod)
  - [Flex Memory and CPU Requirements](#flex-memory-and-cpu-requirements)

## Prerequisites

The minimum information Flex requires to operate is:

- **License Details**: Start a [free 30-day trial](https://factorhouse.io/flex/get-started/).
- **Flink REST URL**

See the [Flex Documentation](https://docs.factorhouse.io/flex/getting-started) for a full list of configuration options.

## Kubernetes

@@include(\_partials/\_configure-eks-environment.md)

## Run Flex in Kubernetes

### Configure the Flex Helm Repository

@@include(\_partials/\_configure-helm-flex.md)

### Start a Flex Instance

#### Start Flex with config from '--set env.XYZ'

When using `helm install`, you can pass configuration with the `--set env.XYZ` flag. This requires careful formatting for certain values.

Some fields, particularly integers and strings containing quotation marks, require quoting. You may also need to escape special characters (like commas or nested quotes) with a backslash (`\`). For more details, see Helm's documentation on [The Format and Limitations of `--set`](https://helm.sh/docs/intro/using_helm/#the-format-and-limitations-of---set).

The following example shows how to install Flex from the command line, highlighting how to handle escaped commas and quotes:

```bash
helm install flex factorhouse/flex \
  --set env.LICENSE_ID="00000000-0000-0000-0000-000000000001" \
  --set env.LICENSE_CODE="FLEX_CREDIT" \
  --set env.LICENSEE="Factor House\, Inc." \ # <-- note the escaped comma
  --set env.LICENSE_EXPIRY="2022-01-01" \
  --set env.LICENSE_SIGNATURE="638......A51" \
  --set env.FLINK_REST_URL="http://flink-dev.svc" \
  --create-namespace --namespace factorhouse

NAME: flex
LAST DEPLOYED: Mon May 31 17:22:21 2021
NAMESPACE: factorhouse
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace factorhouse -l "app.kubernetes.io/name=flex,app.kubernetes.io/instance=flex" -o jsonpath="{.items[0].metadata.name}")
  echo "Visit http://127.0.0.1:3000 to use your application"
  kubectl --namespace factorhouse port-forward $POD_NAME 3000:3000
```

#### Start Flex with Environment Variables from a ConfigMap

You can configure Flex with a ConfigMap of environment variables as follows:

```bash
helm install flex factorhouse/flex \
  --set envFromConfigMap=flex-config \
  --create-namespace --namespace factorhouse
```

This approach requires a `ConfigMap` named `flex-config` to already exist in the `factorhouse` namespace. To configure flex with a local ConfigMap template, see [Configuring with an Existing ConfigMap](#configuring-with-an-existing-configmap). You can also refer to [flex-config.yaml.example](./flex-config.yaml.example) for a sample ConfigMap manifest.

For general guidance, see the Kubernetes documentation on [configuring all key-value pairs in a ConfigMap as environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables).

### Manage a Flex Instance

@@include(\_partials/\_feature-manage-flex-instance.md)

### Start Flex with Local Changes

You can run Flex with local edits to these charts and provide local configuration when running Flex.

#### Pull and Untar the Flex Charts

```bash
helm pull factorhouse/flex --untar --untardir .
```

#### Make Local Edits

Make any edits required to `flex/Chart.yaml` or `flex/values.yaml` (adding volume mounts, etc).

#### Run Local Charts

The command to run local charts is slightly different, see `./flex` rather than `factorhouse/flex`.

```bash
helm install flex ./flex \
  <.. --set configuration, etc ..> \
  --create-namespace --namespace factorhouse
```

#### Configuring with an Existing ConfigMap

This is the recommended method for managing configuration separately from the Helm chart.

**1. Prepare Your ConfigMap Manifest**

Copy the example file ([flex-config.yaml.example](./kpow-config.yaml.example)), then edit it to set your desired `metadata.name` (e.g., `flex-config`) and fill in your configuration under the `data` section.

```bash
cp ./flex/flex-config.yaml.example flex-config.yaml
# now edit flex-config.yaml
```

**2. Create the ConfigMap in Kubernetes**

Before installing, use `kubectl` to create the `ConfigMap` object in your cluster from the file you just prepared.

```bash
kubectl apply -f flex-config.yaml --namespace factorhouse
```

**3. Install the Chart**

Install the Helm chart, using `--set` to reference the name of the `ConfigMap` you just created. The `--create-namespace` flag will ensure the target namespace exists.

```bash
helm install flex ./flex \
  --set envFromConfigMap=flex-config \
  --create-namespace --namespace factorhouse
```

The Flex pod will now start using the environment variables from your externally managed `ConfigMap`.

See [flex-config.yaml.example](./flex-config.yaml.example) for an example ConfigMap file.

See the Kubernetes documentation on [configuring all key-value pairs in a config map as container environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables) for more information.

### Manage Sensitive Environment Variables

@@include(\_partials/\_feature-manage-sensitive-env-vars.md)

```bash
helm install flex ./flex \
  --set envFromSecret=flex-secrets \
  --set envFromConfigMap=flex-config \
  --create-namespace --namespace factorhouse
```

### Provide Files to the Flex Pod

@@include(\_partials/\_feature-provide-files-to-flex-pod.md)

### Flex Memory and CPU Requirements

@@include(\_partials/\_feature-memory-cpu-requirements.md)

Adjust these values from the command line like so:

```bash
helm install flex factorhouse/flex \
     --set resources.limits.cpu=1 \
     --set resources.limits.memory=2Gi \
     --set resources.requests.cpu=1 \
     --set resources.requests.memory=2Gi \
     --create-namespace --namespace factorhouse
```

We recommend always having limits and requests set to the same value, as this set Flex in Guaranteed QoS and provides a
much more reliable operation.

---

@@include(\_partials/\_general-footer.md)
