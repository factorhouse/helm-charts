# Run Kpow Annual for Apache Kafka on AWS Marketplace with Kubernetes

[Kpow](https://factorhouse.io/kpow/) is the all-in-one toolkit to manage, monitor, and learn about your Kafka resources.

This Helm chart is designed for the [Kpow Annual](https://aws.amazon.com/marketplace/pp/prodview-vgghgqdsplhvc) listing on AWS Marketplace. It uses a custom AWS Marketplace container that integrates with AWS to verify subscriptions and manage entitlements. The container is automatically licensed to the subscribing AWS account, which is billed directly for the subscription. There is no need to arrange a separate license with us if you subscribe to a Kpow product through the AWS Marketplace.

# Helm Charts

This Helm chart is for the [Kpow Annual](https://aws.amazon.com/marketplace/pp/prodview-5jvke6codhrsm) offering on AWS Marketplace.

- [Prerequisites](#prerequisites)
- [Kubernetes (EKS)](#kubernetes)
- [Run Kpow in Kubernetes (EKS)](#run-kpow-in-kubernetes)
  - [Download the Kpow Annual Helm chart](#download-the-kpow-annual-helm-chart)
  - [Start a Kpow Instance](#start-a-kpow-instance)
  - [Manage a Kpow Instance](#manage-a-kpow-instance)
  - [Start Kpow with Local Changes](#start-kpow-with-local-changes)
  - [Manage Sensitive Environment Variables](#manage-sensitive-environment-variables)
  - [Provide Files to the Kpow Pod](#provide-files-to-the-kpow-pod)
  - [Kpow Memory and CPU Requirements](#kpow-memory-and-cpu-requirements)
  - [Snappy compression in read-only filesystem](#snappy-compression-in-read-only-filesystem)
- [Run Kpow in EKS Anywhere](#run-kpow-in-eks-anywhere)

## Prerequisites

- **License Details**: No license required—billing is handled automatically through your AWS account.
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

### Download the Kpow Annual Helm chart

Download the Helm Repository in order to use the Kpow Helm Chart.

```bash
export HELM_EXPERIMENTAL_OCI=1
aws ecr get-login-password \
    --region us-east-1 | helm registry login \
    --username AWS \
    --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com

mkdir awsmp-chart && cd awsmp-chart
helm pull oci://709825985650.dkr.ecr.us-east-1.amazonaws.com/factor-house/kpow-annual-chart \
  --version <VERSION_NUMBER>
tar xf $(pwd)/* && find $(pwd) -maxdepth 1 -type f -delete
```

### Start a Kpow Instance

#### Start Kpow with config from '--set env.XYZ'

When using `helm install`, you can pass configuration with the `--set env.XYZ` flag. This requires careful formatting for certain values.

Some fields, particularly integers and strings containing quotation marks, require quoting. You may also need to escape special characters (like commas or nested quotes) with a backslash (`\`). For more details, see Helm's documentation on [The Format and Limitations of `--set`](https://helm.sh/docs/intro/using_helm/#the-format-and-limitations-of---set).

The following example shows how to install Kpow from the command line, highlighting how to handle escaped commas and quotes:

```bash
helm install kpow ./kpow-aws-annual/ \
  --set serviceAccount.create=false \
  --set serviceAccount.name=kpow \
  --set env.BOOTSTRAP="b-1.<cluster-name>.<cluster-identifier>.c8.kafka.us-east-1.amazonaws.com:9096" \
  --set env.SECURITY_PROTOCOL="SASL_PLAINTEXT" \
  --set env.SASL_MECHANISM="PLAIN" \
  --set env.SASL_JAAS_CONFIG="org.apache.kafka.common.security.plain.PlainLoginModule required username=\"user\" password=\"secret\";" \ # <-- note the escaped quotes
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
helm install kpow ./kpow-aws-annual/ \
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

You can run Kpow with local edits to chart files to provide custom configuration.

#### Make Local Edits

Make any edits required to `kpow-aws-annual/Chart.yaml` or `kpow-aws-annual/values.yaml` (adding volume mounts, etc).

#### Configuring with an Existing ConfigMap

This is the recommended method for managing configuration separately from the Helm chart.

**1. Prepare Your ConfigMap Manifest**

Copy the example file ([kpow-config.yaml.example](./kpow-config.yaml.example)), then edit it to set your desired `metadata.name` (e.g., `kpow-config`) and fill in your configuration under the `data` section.

```bash
cp ./kpow-aws-annual/kpow-config.yaml.example kpow-config.yaml
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
helm install kpow ./kpow-aws-annual \
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
helm install kpow ./kpow-aws-annual/ \
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
helm install kpow ./kpow-aws-annual/ \
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

## Run Kpow in EKS Anywhere

This Helm chart includes extra resources required for the token-based IAM authentication used by **EKS Anywhere**.

### Step 1: Create Token & IAM Role

- In the AWS Marketplace console, create a **license token** and an associated IAM role for the Kpow subscription.
- This token is used to access AWS License Manager APIs for license validation.
- A button to generate these is available after you subscribe to the product.

### Step 2: Configure Kubernetes Secrets and Service Account

**1. Create the namespace and a dedicated service account**

```bash
kubectl create namespace factorhouse
kubectl create serviceaccount kpow --namespace factorhouse
```

**2. Create the license secret with the values from Step 1**

```bash
# IMPORTANT: Replace the placeholder values below with your actual token and role ARN.
AWSMP_TOKEN="<YOUR_LICENSE_TOKEN_HERE>"
AWSMP_ROLE_ARN="<YOUR_IAM_ROLE_ARN_HERE>"

kubectl create secret generic awsmp-license-token-secret \
  --from-literal=license_token=$AWSMP_TOKEN \
  --from-literal=iam_role=$AWSMP_ROLE_ARN \
  --namespace factorhouse
```

**3. Create an ECR image pull secret using the license token**

```bash
AWSMP_ACCESS_TOKEN=$(aws license-manager get-access-token \
    --output text --query '*' --token $AWSMP_TOKEN --region us-east-1)

AWSMP_ROLE_CREDENTIALS=$(aws sts assume-role-with-web-identity \
    --region 'us-east-1' \
    --role-arn $AWSMP_ROLE_ARN \
    --role-session-name 'AWSMP-guided-deployment-session' \
    --web-identity-token $AWSMP_ACCESS_TOKEN \
    --query 'Credentials' \
    --output text)

export AWS_ACCESS_KEY_ID=$(echo $AWSMP_ROLE_CREDENTIALS | awk '{print $1}' | xargs)
export AWS_SECRET_ACCESS_KEY=$(echo $AWSMP_ROLE_CREDENTIALS | awk '{print $3}' | xargs)
export AWS_SESSION_TOKEN=$(echo $AWSMP_ROLE_CREDENTIALS | awk '{print $4}' | xargs)

kubectl create secret docker-registry awsmp-image-pull-secret \
  --docker-server=709825985650.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region us-east-1) \
  --namespace factorhouse
```

**4. Link the image pull secret to the service account**

```bash
kubectl patch serviceaccount kpow \
  --namespace factorhouse \
  -p '{"imagePullSecrets": [{"name": "awsmp-image-pull-secret"}]}'
```

### Step 3: Launch Kpow Annual Chart

Download the Helm Repository in order to use the Kpow Helm Chart.

```bash
export HELM_EXPERIMENTAL_OCI=1
aws ecr get-login-password \
    --region us-east-1 | helm registry login \
    --username AWS \
    --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com

mkdir awsmp-chart && cd awsmp-chart
helm pull oci://709825985650.dkr.ecr.us-east-1.amazonaws.com/factor-house/kpow-annual-chart \
  --version <VERSION_NUMBER>
tar xf $(pwd)/* && find $(pwd) -maxdepth 1 -type f -delete
```

Install Kpow, referencing the Kubernetes resources you created above.

```bash
helm install kpow ./kpow-aws-annual/ \
  --set serviceAccount.create=false \
  --set serviceAccount.name=kpow \
  --set aws.licenseConfigSecretName=awsmp-license-token-secret \
  --create-namespace --namespace factorhouse
```

---

### Get Help!

If you have any issues or errors, please contact support@factorhouse.io.

### Licensing and Modifications

This repository is Apache 2.0 licensed, you are welcome to clone and modify as required.
