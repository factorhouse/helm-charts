# Run Kpow for Apache Kafka with Kubernetes

[Kpow](https://factorhouse.io/kpow/) is the all-in-one toolkit to manage, monitor, and learn about your Kafka resources.

This Helm chart uses the [factorhouse/kpow](https://hub.docker.com/r/factorhouse/kpow) container from Dockerhub.

# Helm Charts

This repository contains a single Helm chart that uses the [factorhouse/kpow](https://hub.docker.com/r/factorhouse/kpow) container on Dockerhub.

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

- **License Details**: Start a [free 30-day trial](https://factorhouse.io/kpow/get-started/).
- **Kafka Bootstrap URL**

See the [Kpow Documentation](https://docs.factorhouse.io/kpow/getting-started) for a full list of configuration options.

## Kubernetes

You need to connect to a Kubernetes environment before you can install Kpow.

The following examples demonstrate installing Kpow in [Amazon EKS](https://aws.amazon.com/eks/).

### Configure Kubernetes/EKS

```bash
aws eks --region <your-aws-region> update-kubeconfig --name <your-eks-cluster-name>

Updated context arn:aws:eks:<your-aws-region>:123123123:cluster/<your-eks-cluster-name> in /your/.kube/config
```

#### Confirm Kubernetes Cluster Availability

```bash
kubectl get svc

NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   12.345.6.7   <none>        443/TCP   28h
```


## Run Kpow in Kubernetes

### Configure the Kpow Helm Repository

Add the Factor House Helm Repository in order to use the Kpow Helm Chart.

```
helm repo add factorhouse https://charts.factorhouse.io
```

Update Helm repositories to ensure you install the latest version of Kpow.

```
helm repo update
```


### Start a Kpow Instance

#### Start Kpow with config from '--set env.XYZ'

When using `helm install`, you can pass configuration with the `--set env.XYZ` flag. This requires careful formatting for certain values.

Some fields, particularly integers and strings containing quotation marks, require quoting. You may also need to escape special characters (like commas or nested quotes) with a backslash (`\`). For more details, see Helm's documentation on [The Format and Limitations of `--set`](https://helm.sh/docs/intro/using_helm/#the-format-and-limitations-of---set).

The following example shows how to install Kpow from the command line, highlighting how to handle escaped commas and quotes:

```bash
helm install kpow factorhouse/kpow \
  --set env.LICENSE_ID="00000000-0000-0000-0000-000000000001" \
  --set env.LICENSE_CODE="KPOW_CREDIT" \
  --set env.LICENSEE="Factor House\, Inc." \ # <-- note the escaped comma
  --set env.LICENSE_EXPIRY="2022-01-01" \
  --set env.LICENSE_SIGNATURE="638......A51" \
  --set env.BOOTSTRAP="127.0.0.1:9092\,127.0.0.1:9093\,127.0.0.1:9094" \ # <-- note the escaped commas
  --set env.SECURITY_PROTOCOL="SASL_PLAINTEXT" \
  --set env.SASL_MECHANISM="PLAIN" \
  --set env.SASL_JAAS_CONFIG="org.apache.kafka.common.security.plain.PlainLoginModule required username=\"user\" password=\"secret\";" \ # <-- note the escaped quotes
  --set env.LICENSE_CREDITS="7" \
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
helm install kpow factorhouse/kpow \
  --set envFromConfigMap=kpow-config \
  --create-namespace --namespace factorhouse
```

This approach requires a `ConfigMap` named `kpow-config` to already exist in the `factorhouse` namespace. To configure Kpow with a local ConfigMap template, see [Configuring with an Existing ConfigMap](#configuring-with-an-existing-configmap). You can also refer to [kpow-config.yaml.example](./kpow-config.yaml.example) for a sample ConfigMap manifest.

For general guidance, see the Kubernetes documentation on [configuring all key-value pairs in a ConfigMap as environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables).

### Manage a Kpow Instance

#### Set the $POD_NAME variable and test the Kpow UI

Follow the notes instructions to set the $POD_NAME variable and configure port forwarding to the Kpow UI.

```bash
export POD_NAME=$(kubectl get pods --namespace factorhouse -l "app.kubernetes.io/name=kpow,app.kubernetes.io/instance=kpow" -o jsonpath="{.items[0].metadata.name}")
echo "Visit http://127.0.0.1:3000 to use your application"
kubectl --namespace factorhouse port-forward $POD_NAME 3000:3000
```

Kpow is now available on [http://127.0.0.1:3000](http://127.0.0.1:3000).

#### Check the Kpow Pod

```bash
kubectl describe pods --namespace factorhouse

Name:         kpow-9988df6b6-vvf8z
Namespace:    factorhouse
Priority:     0
Node:         ip-172-31-33-42.ap-southeast-2.compute.internal/172.31.33.42
Start Time:   Mon, 31 May 2021 17:22:22 +1000
Labels:       app.kubernetes.io/instance=kpow
              app.kubernetes.io/name=kpow
              pod-template-hash=9988df6b6
Annotations:  kubernetes.io/psp: eks.privileged
Status:       Running
```

#### View the Kpow Pod Logs

```bash
kubectl logs $POD_NAME --namespace factorhouse

11:36:49.111 INFO  [main] kpow.system ? start Kpow
...
```

#### Remove Kpow

```bash
helm delete kpow --namespace factorhouse
```


### Start Kpow with Local Changes

You can run Kpow with local edits to these charts and provide local configuration when running Kpow.

#### Pull and Untar the Kpow Charts

```bash
helm pull factorhouse/kpow --untar --untardir .
```

#### Make Local Edits

Make any edits required to `kpow/Chart.yaml` or `kpow/values.yaml` (adding volume mounts, etc).

#### Run Local Charts

The command to run local charts is slightly different, see `./kpow` rather than `factorhouse/kpow`.

```bash
helm install kpow ./kpow \
  <.. --set configuration, etc ..> \
  --create-namespace -namespace factorhouse
```

#### Configuring with an Existing ConfigMap

This is the recommended method for managing configuration separately from the Helm chart.

**1. Prepare Your ConfigMap Manifest**

Copy the example file ([kpow-config.yaml.example](./kpow-config.yaml.example)), then edit it to set your desired `metadata.name` (e.g., `kpow-config`) and fill in your configuration under the `data` section.

```bash
cp ./kpow/kpow-config.yaml.example kpow-config.yaml
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
helm install kpow ./kpow \
  --set envFromConfigMap=kpow-config \
  --create-namespace --namespace factorhouse
```

The Kpow pod will now start using the environment variables from your externally managed `ConfigMap`.

See [kpow-config.yaml.example](./kpow-config.yaml.example) for an example ConfigMap file.

See the Kubernetes documentation on [configuring all key-value pairs in a config map as container environment variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables) for more information.

### Manage Sensitive Environment Variables

This helm chart accepts the name of a secret containing sensitive parameters, e.g.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kpow-secrets
data:
  SASL_JAAS_CONFIG: a3JnLmFwYWNoXS5rYWZrYS5jb21tb24uc2VjdXJpdHkucGxhaW4uUGxhaW5Mb2dpbk2vZHVsZSByZXF1aXJiZCB1c2VybmFtZT0iTFQ1V0ZaV1BRWUpHNzRJQyIgcGFzc3dvcmQ9IjlYUFVYS3BLYUQxYzVJdXVNRjRPKzZ2NxJ0a1E4aS9yWUp6YlppdlgvZnNiTG51eGY4SnlFT1dUeXMvTnJ1bTAiBwo=
  CONFLUENT_API_SECRET: NFJSejlReFNTTXlTcGhXdjNLMHNYY1F6UGNURmdadlNYT0ZXSXViWFJySmx2N3A2WStSenROQnVpYThvNG1NSRo=
```

```bash
kubectl apply -f ./kpow-secrets.yaml --namespace factorhouse
```

Then run the helm chart (this can be used in conjunction with `envFromConfigMap`)

See the Kubernetes documentation
on [configuring all key value pairs in a secret as environment variables](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#configure-all-key-value-pairs-in-a-secret-as-container-environment-variables)
for more information.


```bash
helm install kpow ./kpow \
  --set envFromSecret=kpow-secrets \
  --set envFromConfigMap=kpow-config \
  --create-namespace --namespace factorhouse
```

### Provide Files to the Kpow Pod

There are occasions where you must provide files to the Kpow Pod in order for Kpow to run correctly, such files include:

- RBAC configuration
- SSL Keystores
- SSL Truststores

How you provide these files is down to user preference, we are not able to provide any support or instruction in this
regard.

You may find the Kubernetes documentation on [injecting data into applications](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-a-volume) useful.


### Kpow Memory and CPU Requirements

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


Adjust these values from the command line like so:

```bash
helm install kpow factorhouse/kpow \
     --set resources.limits.cpu=1 \
     --set resources.limits.memory=2Gi \
     --set resources.requests.cpu=1 \
     --set resources.requests.memory=2Gi \
     --create-namespace --namespace factorhouse
```

We recommend always having limits and requests set to the same value, as this set Kpow in Guaranteed QoS and provides a much more reliable operation.

#### Snappy compression in read-only filesystem

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


---

### Get Help!

If you have any issues or errors, please contact support@factorhouse.io.

### Licensing and Modifications

This repository is Apache 2.0 licensed, you are welcome to clone and modify as required.

