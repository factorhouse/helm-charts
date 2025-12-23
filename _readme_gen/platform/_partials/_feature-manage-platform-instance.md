#### Set the $POD_NAME variable and test the Factor Platform UI

Follow the notes instructions to set the $POD_NAME variable and configure port forwarding to the Factor Platform UI.

```bash
export POD_NAME=$(kubectl get pods --namespace factorhouse -l "app.kubernetes.io/name=factor-platform,app.kubernetes.io/instance=platform" -o jsonpath="{.items[0].metadata.name}")
echo "Visit http://127.0.0.1:3000 to use your application"
kubectl --namespace factorhouse port-forward $POD_NAME 3000:3000
```

Factor Platform is now available on [http://127.0.0.1:3000](http://127.0.0.1:3000).

#### Check the Factor Platform Pod

```bash
kubectl describe pod $POD_NAME --namespace factorhouse

Name:             platform-factor-platform-6976f96b95-g5ft7
Namespace:        factorhouse
Priority:         0
Service Account:  platform
Node:             ip-10-0-1-115.ec2.internal/10.0.1.115
Start Time:       Tue, 23 Dec 2025 10:04:29 +1100
Labels:           app.kubernetes.io/instance=platform
                  app.kubernetes.io/name=factor-platform
                  pod-template-hash=6976f96b95
Annotations:      <none>
Status:           Running
```

#### View the Factor Platform Pod Logs

```bash
kubectl logs $POD_NAME --namespace factorhouse

23:04:35.707 INFO  [main] factorhouse.platform – Initializing Factor Platform - Enterprise - 95.1
...
```

#### Remove Factor Platform

```bash
helm delete platform --namespace factorhouse
```
