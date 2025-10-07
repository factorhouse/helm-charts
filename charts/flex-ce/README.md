# Run Flex Community Edition for Apache Flink in Kubernetes

[Flex](https://factorhouse.io/flex) is the all-in-one toolkit to manage, monitor, and learn about your Flink resources.

This Helm chart uses the [factorhouse/flex-ce](https://hub.docker.com/r/factorhouse/flex-ce) container from Dockerhub.

# Helm Charts

This repository contains a single Helm chart that uses the [factorhouse/flex-ce](https://hub.docker.com/r/factorhouse/flex-ce) container on Dockerhub.

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

The minimum information Kpow requires to operate is:

- **License Details**: Request a [community license](https://factorhouse.io/flex/community/).
- **Flink REST URL**

See the [Kpow Documentation](https://docs.factorhouse.io/kpow/getting-started) for a full list of configuration options.

## Kubernetes

readme_gen/kpow/\_partials/\_configure-eks-environment.md

### Start a Flex Instance

The minimum information Kpow requires to operate is:

- **License Details**: Request a [community license](https://factorhouse.io/flex/community/).
- **Flink REST URL**

See the [Flex Documentation](https://docs.factorhouse.io/flex/getting-started) for a full list of configuration options.

#### Start Flex with config from '--set env.XYZ'

When using `helm install`, you can pass configuration with the `--set env.XYZ` flag. This requires careful formatting for certain values.

Some fields, particularly integers and strings containing quotation marks, require quoting. You may also need to escape special characters (like commas or nested quotes) with a backslash (`\`). For more details, see Helm's documentation on [The Format and Limitations of `--set`](https://helm.sh/docs/intro/using_helm/#the-format-and-limitations-of---set).

The following example shows how to install Flex from the command line, highlighting how to handle escaped commas and quotes:

```bash
helm install flex factorhouse/flex-ce \
  --set env.LICENSE_ID="00000000-0000-0000-0000-000000000001" \
  --set env.LICENSE_CODE="FLEX_COMMUNITY" \
  --set env.LICENSEE="John\, doe" \ # <-- note the escaped comma
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
helm install flex factorhouse/flex-ce \
  --set envFromConfigMap=flex-config \
  --create-namespace --namespace factorhouse
```

This approach requires a `ConfigMap` named `flex-config` to already exist in the `factorhouse` namespace. To configure Kpow with a local ConfigMap template, see [Start Flex with Local Changes](#start-flex-with-local-changes). You can also refer to [flex-config.yaml.example](./flex-config.yaml.example) for a sample ConfigMap manifest.

For general guidance, see the Kubernetes documentation on [configuring all key-value pairs in a ConfigMap as environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables).

### Manage a Flex Instance

#### Set the $POD_NAME variable and test the Flex UI

Follow the notes instructions to set the $POD_NAME variable and configure port forwarding to the Flex UI.

```bash
export POD_NAME=$(kubectl get pods --namespace factorhouse -l "app.kubernetes.io/name=flex,app.kubernetes.io/instance=flex" -o jsonpath="{.items[0].metadata.name}")
echo "Visit http://127.0.0.1:3000 to use your application"
kubectl --namespace factorhouse port-forward $POD_NAME 3000:3000
```

Flex is now available on [http://127.0.0.1:3000](http://127.0.0.1:3000).

#### Check the Flex Pod

```bash
kubectl describe pods --namespace factorhouse

Name:         flex-9988df6b6-vvf8z
Namespace:    factorhouse
Priority:     0
Node:         ip-172-31-33-42.ap-southeast-2.compute.internal/172.31.33.42
Start Time:   Mon, 31 May 2021 17:22:22 +1000
Labels:       app.kubernetes.io/instance=flex
              app.kubernetes.io/name=flex
              pod-template-hash=9988df6b6
Annotations:  kubernetes.io/psp: eks.privileged
Status:       Running
```

#### View the Flex Pod Logs

```bash
kubectl logs --namespace factorhouse $POD_NAME

11:36:49.111 INFO  [main] flex.system ? start Flex
...
```

#### Remove Flex

```bash
helm delete --namespace factorhouse flex
```


### Start Flex with Local Changes

You can run Flex with local edits to these charts and provide local configuration when running Flex.

#### Pull and Untar the Flex Charts

```bash
helm pull factorhouse/flex-ce --untar --untardir .
```

#### Make Local Edits

Make any edits required to `flex-ce/Chart.yaml` or `flex-ce/values.yaml` (adding volume mounts, etc).

#### Run Local Charts

The command to run local charts is slightly different, see `./flex-ce` rather than `factorhouse/flex-ce`.

```bash
helm install flex ./flex-ce \
  <.. --set configuration, etc ..> \
  --create-namespace --namespace factorhouse
```

#### Run with Local ConfigMap Configuration

This method bundles your configuration into the Helm chart itself. When you run `helm install`, Helm will create the `ConfigMap` resource in Kubernetes and then configure the Kpow pod to use it.

1.  **Create your `ConfigMap` manifest file.** The `metadata.name` inside this file must match the name you specify in the `--set` flag. For example, `flex-config`. See [flex-config.yaml.example](./flex-config.yaml.example) for a template.
2.  **Place the manifest file** in the `./flex-ce/templates/` directory.
3.  **Install the chart**, referencing the `ConfigMap` name.

```bash
helm install flex ./flex-ce \
  --set envFromConfigMap=flex-config \
  --create-namespace  --namespace factorhouse
```

See [flex-config.yaml.example](./flex-config.yaml.example) for an example ConfigMap file.

See the Kubernetes documentation
on [configuring all key value pairs in a config map as environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables)
for more information.

### Manage Sensitive Environment Variables

This helm chart accepts the name of a secret containing sensitive parameters, e.g.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: flex-secrets
data:
  SASL_JAAS_CONFIG: a3JnLmFwYWNoXS5rYWZrYS5jb21tb24uc2VjdXJpdHkucGxhaW4uUGxhaW5Mb2dpbk2vZHVsZSByZXF1aXJiZCB1c2VybmFtZT0iTFQ1V0ZaV1BRWUpHNzRJQyIgcGFzc3dvcmQ9IjlYUFVYS3BLYUQxYzVJdXVNRjRPKzZ2NxJ0a1E4aS9yWUp6YlppdlgvZnNiTG51eGY4SnlFT1dUeXMvTnJ1bTAiBwo=
  CONFLUENT_API_SECRET: NFJSejlReFNTTXlTcGhXdjNLMHNYY1F6UGNURmdadlNYT0ZXSXViWFJySmx2N3A2WStSenROQnVpYThvNG1NSRo=
```

```bash
kubectl apply -f ./flex-secrets.yaml --namespace factorhouse
```

Then run the helm chart (this can be used in conjunction with `envFromConfigMap`)

See the Kubernetes documentation
on [configuring all key value pairs in a secret as environment variables](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#configure-all-key-value-pairs-in-a-secret-as-container-environment-variables)
for more information.


```bash
helm install flex ./flex-ce \
  --set envFromSecret=flex-secrets \
  --set envFromConfigMap=flex-config \
  --create-namespace --namespace factorhouse
```

### Provide Files to the Flex Pod

There are occasions where you must provide files to the Flex Pod in order for Flex to run correctly, such files include:

- RBAC configuration
- SSL Keystores
- SSL Truststores

How you provide these files is down to user preference, we are not able to provide any support or instruction in this
regard.

You may find the Kubernetes documentation
on [injecting data into applications](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-a-volume)
useful.


### Flex Memory and CPU Requirements

The chart runs Flex with Guaranteed QoS, having resource request and limit set to these values by default:

```yaml
resources:
  limits:
    cpu: 2
    memory: 8Gi
  requests:
    cpu: 2
    memory: 8Gi
```

These default resource settings are conservative, suited to a deployment of Flex that manages multiple Flink clusters
and associated resources.

When running Flex with a single Flink cluster you can experiment with reducing those resources as far as our suggested
minimum:

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


Adjust these values from the command line like so:

```bash
helm install flex factorhouse/flex-ce \
     --set resources.limits.cpu=1 \
     --set resources.limits.memory=2Gi \
     --set resources.requests.cpu=1 \
     --set resources.requests.memory=2Gi \
     --create-namespace --namespace factorhouse
```

We recommend always having limits and requests set to the same value, as this set Flex in Guaranteed QoS and provides a
much more reliable operation.

---

### Get Help!

If you have any issues or errors, please contact support@factorhouse.io.

### Licensing and Modifications

This repository is Apache 2.0 licensed, you are welcome to clone and modify as required.

