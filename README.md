# Factor House Helm Charts

[![Release Charts](https://github.com/factorhouse/helm-charts/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/factorhouse/helm-charts/actions/workflows/release.yml)

Official Helm Charts for Factor House products. Currently supported:

* [Kpow](charts/kpow/README.md) (`factorhouse/kpow`)
* [Kpow Community Edition](charts/kpow-ce/README.md) (`factorhouse/kpow-ce`)
* [Flex](charts/flex/README.md) (`factorhouse/flex`)
* [Flex Community Edition](charts/flex-ce/README.md) (`factorhouse/flex-ce`)

# How to use Factor House Helm repository 

You need to add this repository to your Helm repositories:

```bash
helm repo add datadog https://charts.factorhouse.com
helm repo update
```

# Usage

Please refer to each individual products README for instructions on how to get up and running.

For a quick reference, check out our [examples/](examples/) directory to see common configurations.
