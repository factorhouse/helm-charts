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
