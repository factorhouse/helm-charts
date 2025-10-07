### Download the Kpow Hourly Helm chart

Add the Helm Repository in order to use the Kpow Helm Chart.

```bash
export HELM_EXPERIMENTAL_OCI=1
aws ecr get-login-password \
    --region us-east-1 | helm registry login \
    --username AWS \
    --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com

mkdir awsmp-chart && cd awsmp-chart
helm pull oci://709825985650.dkr.ecr.us-east-1.amazonaws.com/factor-house/kpow-aws-hourly \
  --version <VERSION_NUMBER>
tar xf $(pwd)/* && find $(pwd) -maxdepth 1 -type f -delete
```
