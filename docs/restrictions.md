# Restrictions Documentation

## Restrictions

Here is a list of known limitations in the current Veeam Kasten release.
  A number of them will be addressed in upcoming releases.

## On-Premises Storage Providers â

Currently, on-premises Veeam Kasten deployments are only supported
  if storage is provisioned via the Container Storage Interface (CSI).

With this in mind, the following limitations exist if you have an
  unsupported storage provider:

- Applications for which a Kanister blueprint (or a blueprint binding) is available but does not use volume-snapshots will be fully supported.
- Any deployments and stateful sets that use a persistent volume that are not associated with a Kanister blueprint (or a blueprint binding) will fail on snapshots unless you are using the Generic Storage Backup and Restore Kanister approach with sidecar containers.

Please refer to Kanister for
  more details.

## Cloning Applications â

When cloning applications, one needs to be aware of both external
  dependencies outside of the application namespace as well as
  namespace-dependent configuration. For example, if there is a duplicated
  ingress setup, they will conflict and the results might be
  non-deterministic.

## Restore â

Please refer to Limitations for restore limitations.

## Migration Restrictions â

- Multi and hybrid-cloud volume migration is fully supported as long as Veeam Kasten has support for snapshots on the source side. For unsupported storage providers, please use Kanister for now.
- When migrating Kanister-enabled applications across clusters, the destination cluster also needs access to all buckets where Kanister artifacts are stored. This restriction will be removed in an upcoming release where Kanister artifacts will be copied into the migration bucket.

## GitOps Managed Applications â

When restoring applications that are managed by external controllers,
  one needs to be aware of the following conditions.

- An external controller can interrupt Veeam Kasten operations that may lead to restore failures. Ensure that there is no external controller handling the resource lifecycle during the restore by disabling the auto-sync mechanism in the GitOps tools used, or scaling down the controller, etc.
- To avoid conflict with external controller after the restore has taken place, it is recommended that you perform a data-only restore. Please refer to Data-Only Restore for more details.

## TLS Version Compatibility â

Kasten currently supports TLS version 1.2 and 1.3, but it has
  limitations on the cipher suites, elliptic curves, and signature
  algorithms it allows.

| Cipher Suites | TLS Version | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 1.2 |
| :---: | :---: | :---: | :---: |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 1.2 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 1.2 |
| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | 1.2 |
| TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 | 1.2 |
| TLS_AES_128_GCM_SHA256 | 1.3 |
| TLS_AES_256_GCM_SHA384 | 1.3 |

| Curves | P-256 |
| :---: | :---: |
| P-256 |
| P-384 |
| P-522 |

For the following signature algorithms, the ECDSA implementations are
  constrained to specific curves in TLS 1.3.

| Signature Algorithms | Hash | RSASSA-PSS | SHA256 |
| :---: | :---: | :---: | :---: |
| RSASSA-PSS | SHA256 |
| RSASSA-PSS | SHA384 |
| RSASSA-PSS | SHA512 |
| RSASSA-PKCS1 | SHA256 |
| RSASSA-PKCS1 | SHA384 |
| RSASSA-PKCS1 | SHA512 |
| ECDSA with P-256 | SHA256 |
| ECDSA with P-384 | SHA384 |
| ECDSA with P-512 | SHA512 |

## Limitations in FIPS mode â

Enabling FIPS mode may result in certain features that are unavailable
  due to non-compliance with the algorithms used. For more information
  regarding the distinct features and their installation limitations,
  please see the FIPS section.

It is important to note that importing non-FIPS compliant data into a
  FIPS compliant version of Kasten will not be possible.

## Running without a cluster-admin ClusterRole â

Veeam Kasten configures some of its ServiceAccount to be bound with the
  kubernetes ClusterRole cluster-admin so that Kasten can properly backup and
  restore resources within your cluster.

Installing Veeam Kasten without the cluster-admin ClusterRole bound to a
  provided ServiceAccount is not supported .

---

