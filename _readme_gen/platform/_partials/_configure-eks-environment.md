### Configure Kubernetes/EKS

You need to connect to a Kubernetes environment before you can install Kpow.

The following examples demonstrate installing Kpow in [Amazon EKS](https://aws.amazon.com/eks/).

```bash
aws eks --region <your-aws-region> update-kubeconfig --name <your-eks-cluster-name>

Updated context arn:aws:eks:<your-aws-region>:123123123:cluster/<your-eks-cluster-name> in /your/.kube/config
```

#### Confirm Kubernetes Cluster Availability

```bash
kubectl get nodes

NAME                              STATUS   ROLES    AGE     VERSION
ip-192-168-...-21.ec2.internal   Ready    <none>   2m15s    v1.32.9-eks-113cf36
...
```
