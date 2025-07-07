# Operating Documentation

## Operating Dr

As Veeam Kasten is a stateful application running on the
  cluster, it must be responsible for backing up its own data to enable
  recovery in the event of disaster. This backup is enabled by the
  Veeam Kasten Disaster Recovery (KDR) policy. In particular, KDR
  provides the ability to recover the Veeam Kasten platform
  from a variety of disasters, such as the unintended deletion of
  Veeam Kasten or its restore points, the failure of the underlying
  storage used by Veeam Kasten, or even the accidental
  destruction of the Kubernetes cluster on which Veeam Kasten is deployed.

## Configuring Veeam Kasten Disaster Recovery Mode â

The KDR mode specifies how internal Veeam Kasten resources are protected. The
  mode must be set before enabling the KDR policy. Changes
  to the KDR mode only apply to future KDR policy runs.

Starting in Veeam Kasten v8.0.0, all installations default to Quick DR (Local Catalog Snapshot) mode.

Quick DR (Local Catalog Snapshot) mode should only be enabled if the storage provisioner
    used for Veeam Kasten PVCs supports both the creation of storage snapshots
    and the ability to restore the existing volume from a storage snapshot. See Comparing Available KDR Modes for details on alternate
    configuration options.

- To enable Legacy DR mode, install or upgrade Veeam Kasten with the --set kastenDisasterRecovery.quickMode.enabled=false Helm value.
- To enable Quick DR mode, install or upgrade Veeam Kasten with the --set kastenDisasterRecovery.quickMode.enabled=true Helm value.
- See Enabling Veeam Kasten Disaster Recovery via UI or Enabling Veeam Kasten Disaster Recovery via CLI for details on configuring catalog snapshot behavior for Quick DR mode.

## Comparing Available KDR Modes â

Refer to the details below to understand the key differences between
  each mode:

### Legacy DR â

Legacy DR mode has been deprecated and will be removed in a future release.
    All clusters should be migrated a supported Quick DR configuration.

Recommended Usage

- Supported for backwards-compatibility only

Actions Performed Per KDR Policy Run

- Exports a full copy of the catalog database

Resources Available to Recover

- Enables recovery of specified Veeam Kasten custom resources
- Enables recovery of local restore points, exported restore points, and action history on any cluster Note It is expected that local restore points will be non-restorable when a KDR recovery of the exported catalog snapshot is performed on a different cluster, as applicable storage snapshot references are typically unavailable.

Enables recovery of specified Veeam Kasten custom resources

Enables recovery of local restore points, exported
      restore points, and action history on any cluster

It is expected that local restore points will be non-restorable when a
        KDR recovery of the exported catalog snapshot is performed on a different cluster, as
        applicable storage snapshot references are typically unavailable.

### Quick DR (Local Catalog Snapshot) â

- Recommended when storage used for Veeam Kasten PVCs supports both the creation of storage snapshots and the ability to provision a volume using a storage snapshot

- Creates a local snapshot of the catalog PVC
- Incrementally exports minimally required data only from the catalog database

- Enables recovery of specified Veeam Kasten custom resources
- Enables recovery of exported restore points on any cluster
- Enables recovery of local restore points, exported restore points, and action history only where the local catalog snapshot is available for restore (i.e. in-place recovery on the original cluster)

Compared to Legacy DR

- Offers faster KDR policy runs by reducing amount of exported data
- Consumes less repository storage by reducing amount of exported data
- Offers faster KDR recovery when leveraging local storage snapshot
- Protects additional Veeam Kasten custom resource types

### Quick DR (Exported Catalog Snapshot) â

- Recommended when storage used for Veeam Kasten PVCs supports the creation of storage snapshots but cannot provision a volume using a storage snapshot
- Recommended when there is a need to reduce retention of local storage snapshots without impacting retention of exported backups
- This mode may be selected for any snapshot-capable storage in order to provide the highest level of resilience

- Creates a local snapshot of the catalog PVC
- Incrementally exports minimally required data only from the catalog database
- Performs an incremental export of the catalog PVC snapshot data

- Offers comparable KDR policy run completion times
- Consumes less repository storage by exporting incremental catalog data
- Offers faster KDR recovery when leveraging local storage snapshot
- Offers comparable KDR recovery when leveraging exported storage snapshot
- Protects additional Veeam Kasten resource types

### Quick DR (No Catalog Snapshot) â

- Recommended when no available cluster storage supports snapshot creation (i.e. only Generic Storage Backup is used)
- Alternatively, this mode may be selected if there is no requirement to recover local restore points or action history

- Incrementally exports minimally required data only from the catalog database

- Enables recovery of specified Veeam Kasten custom resources
- Enables recovery of exported restore points on any cluster

- Offers faster KDR policy runs by reducing amount of exported data
- Consumes less repository storage by reducing amount of exported data
- Offers faster KDR recovery by reducing amount of imported data
- Protects additional Veeam Kasten custom resource types
- Does not support recovery of local restore points and action history

### KDR Protected Resource Matrix â

| Veeam Kasten Resource | Quick DR | Legacy DR | Actions | Yes(1) | Yes |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Actions | Yes(1) | Yes |
| Local Restore Points | Yes(1) | Yes |
| Exported Restore Points | Yes | Yes |
| Policies | Yes | Yes |
| Basic User Policies | Yes | No |
| Profiles | Yes | Yes |
| Blueprints | Yes | Yes |
| Blueprint Bindings | Yes | No |
| Policy Presets | Yes | No |
| Transform Sets | Yes | No |
| Multi-Cluster Primary | Yes | No |
| Multi-Cluster Secondary | Yes | No |
| Reports | No | No |
| ActionPodSpecs | No | No |
| AuditConfig | No | No |
| StorageSecurityContext | Yes | No |
| StorageSecurityContextBinding | Yes | No |

For Quick DR, resources marked with (1) can only be
    restored if a local or exported catalog snapshot is available
    to be restored.

## Enabling Veeam Kasten Disaster Recovery via UI â

Enabling Veeam Kasten Disaster Recovery (KDR) creates a dedicated
  policy within Veeam Kasten to back up its resources and catalog data
  to an external location profile .

The Veeam Kasten Disaster Recovery settings are accessible via the Setup Kasten DR page under the Settings menu in the navigation
  sidebar.

- Specify a location profile to which KDR backups will be exported. It is strongly recommended to use a location profile that supports immutable backups to ensure restore point catalog data can be recovered in the event of incidents including ransomware and accidental deletion. Note Veeam Repository location profiles cannot be used as a destination for KDR backups.
- Select and configure the desired passphrase method that will be used to encrypt KDR backups: Passphrase warning It is critical that this unmanaged passphrase be stored securely outside of the cluster as it will be required to perform any future recoveries. HashiCorp Vault Note Using HashiCorp Vault requires that Veeam Kasten is configured to access Vault . AWS Secrets Manager Note Using AWS Secrets Manager requires that an AWS Infrastructure Profile exists with the required permissions
- If Quick DR mode is enabled, specify the desired catalog snapshot behavior. See comparison for details and recommendations. Note Updating the catalog snapshot configuration may be performed by disabling and re-enabling KDR.
- Select Enable Kasten DR . A confirmation with the configuration and cluster ID will be displayed when KDR is enabled. This ID is used as a prefix to the object or file storage location where Veeam Kasten saves its exported backup data. Tip The Cluster ID value for a given cluster can also be accessed using the following kubectl command: # Extract UUID of the `default` namespace kubectl get namespace default -o jsonpath = "{.metadata.uid}{' \n '}" warning After enabling KDR it is critical to retain the following to successfully recover Veeam Kasten from a disaster: The source Cluster ID The KDR passphrase (or external secret manager details) The KDR location profile details and credential Without this information, restore point catalog recovery will not be possible.

Specify a location profile to which KDR backups will be exported.

It is strongly recommended to use a location profile
      that supports immutable backups to ensure
      restore point catalog data can be recovered in the event of
      incidents including ransomware and accidental deletion.

Veeam Repository location profiles cannot be used as a destination for KDR backups.

Select and configure the desired passphrase method that will be used to encrypt KDR backups:

Passphrase

It is critical that this unmanaged passphrase be stored securely outside
        of the cluster as it will be required to perform any future recoveries.

HashiCorp Vault

Using HashiCorp Vault requires that Veeam Kasten is configured to access Vault .

AWS Secrets Manager

Using AWS Secrets Manager requires that an AWS Infrastructure Profile exists with the required permissions

If Quick DR mode is enabled, specify the desired catalog snapshot behavior. See comparison for details and recommendations.

Updating the catalog snapshot configuration may be performed by disabling and re-enabling KDR.

Select Enable Kasten DR .

A confirmation with the configuration and cluster ID will be displayed when KDR is enabled.
      This ID is used as a prefix to the object or file storage location where Veeam Kasten
      saves its exported backup data.

The Cluster ID value for a given cluster can also be accessed using the following kubectl command:

```
# Extract UUID of the `default` namespacekubectl get namespace default -o jsonpath="{.metadata.uid}{'\n'}"
```

After enabling KDR it is critical to retain the following to successfully recover Veeam Kasten
        from a disaster:

- The source Cluster ID
- The KDR passphrase (or external secret manager details)
- The KDR location profile details and credential

Without this information, restore point catalog recovery will not be possible.

## Enabling Veeam Kasten Disaster Recovery via CLI â

As KDR backups are performed via a Veeam Kasten policy, configuration
  of KDR may be automated via CLI or GitOps tools. Each of the following
  examples assume deployment to the kasten-io namespace and must be
  modified to reflect environment specific details including location
  profile name, frequency, and retention.

- Create the k10-dr-secret Secret with the passphrase to be used to encrypt KDR backups: kubectl create secret generic k10-dr-secret --namespace kasten-io --from-literal key = < PASSPHRASE >
- Modify and apply one of the following k10-disaster-recovery-policy Policy examples. See comparison for available mode details and recommendations. Quick DR (Local Catalog Snapshot) - Default apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io kdrSnapshotConfiguration : takeLocalCatalogSnapshot : true Quick DR (Exported Catalog Snapshot) apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io - action : export exportParameters : exportData : enabled : true profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io kdrSnapshotConfiguration : exportCatalogSnapshot : true takeLocalCatalogSnapshot : true Quick DR (No Catalog Snapshot) apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io kdrSnapshotConfiguration : { } Legacy DR (Full Catalog Export) apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io

Create the k10-dr-secret Secret with the passphrase to be used to encrypt KDR backups:

```
kubectl create secret generic k10-dr-secret  --namespace kasten-io  --from-literal key=<PASSPHRASE>
```

Modify and apply one of the following k10-disaster-recovery-policy Policy examples. See comparison for available mode details and recommendations.

Quick DR (Local Catalog Snapshot) - Default

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:      - key: k10.kasten.io/appNamespace        operator: In        values:          - kasten-io  kdrSnapshotConfiguration:    takeLocalCatalogSnapshot: true
```

Quick DR (Exported Catalog Snapshot)

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   - action: export    exportParameters:      exportData:        enabled: true      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io  frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:    - key: k10.kasten.io/appNamespace      operator: In      values:        - kasten-io  kdrSnapshotConfiguration:    exportCatalogSnapshot: true    takeLocalCatalogSnapshot: true
```

Quick DR (No Catalog Snapshot)

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:    - key: k10.kasten.io/appNamespace      operator: In      values:        - kasten-io  kdrSnapshotConfiguration: {}
```

Legacy DR (Full Catalog Export)

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:    - key: k10.kasten.io/appNamespace      operator: In      values:        - kasten-io
```

## Managing the Veeam Kasten Disaster Recovery Policy â

A policy named k10-disaster-recovery-policy that implements
  KDR functionality will automatically be created when
  KDR is enabled. This policy can be viewed through the Policies page in the navigation sidebar.

Click Run Once on the k10-disaster-recovery-policy to start a
  manual backup.

Click Edit to modify the frequency and retention settings. It is
  recommended that the KDR policy match the frequency of the lowest RPO
  policy on the cluster.

## Disabling Veeam Kasten Disaster Recovery â

Veeam Kasten Disaster Recovery can be disabled by clicking the Disable Kasten DR button on the Setup Kasten DR page, which is found
  under the Settings menu in the navigation sidebar.

It is not recommended to run Veeam Kasten without KDR enabled.

## Recovering Veeam Kasten from a Disaster via UI â

To recover from a KDR backup using the UI, follow these steps:

1. On a new cluster, install a fresh Veeam Kasten instance in the same namespace as the original Veeam Kasten instance.
2. On the new cluster, create a location profile by providing the bucket information and credentials for the object storage location or NFS/SMB file storage location where previous Veeam Kasten backups are stored.
3. On the new cluster, navigate to the Restore Kasten page under the Settings menu in the navigation sidebar.
4. In the Profile drop-down, select the location profile created in step 3.

1. For Cluster ID, provide the ID of the original cluster with Veeam Kasten Disaster Recovery enabled. This ID can be found on the Setup Kasten DR page of the original cluster that currently has Veeam Kasten Disaster Recovery enabled.

- Raw passphrase: Provide the passphrase used when enabling Disaster Recovery.

- HashiCorp Vault: Provide the Key Value Secrets Engine Version, Mount, Path, and Passphrase Key stored in a HashiCorp Vault secret.

- AWS Secrets Manager: Provide the secret name, its associated region, and the key.

For immutable location profiles, a previous point in time can be
    provided to filter out any restore points newer than the specified
    time in the next step. If no specific date is chosen, it will display
    all available restore points, with the most recent ones appearing
    first.

1. Click the Next button to start the validation process. If validation succeeds, a drop-down containing the available restore points will be displayed.

All times are displayed in the local timezone of the client's
    browser.

1. Select the desired restore point and click the Next button.
2. Review the summary and click the Start Restore button to begin the restore process.

1. Upon completion of a successful restoration, navigation to the dashboard and information about ownership and deletion of the configmap is displayed.

Following recovery of the Veeam Kasten restore point catalog,
  restore cluster-scoped resources and applications as required.

## Recovering Veeam Kasten from a Disaster via CLI â

In Veeam Kasten v7.5.0 and above, KDR recoveries can be performed via
  API or CLI using DR API Resources .
  Recovering from a KDR backup using CLI involves the following
  sequence of steps:

1. Create a Kubernetes Secret, k10-dr-secret , using the passphrase provided while enabling Disaster Recovery as described in Specifying a Disaster Recovery Passphrase .
2. Install a fresh Veeam Kasten instance in the same namespace as the above Secret.
3. Provide bucket information and credentials for the object storage location or NFS/SMB file storage location where previous Veeam Kasten backups are stored.
4. Create KastenDRReview resource providing the source cluster information.
5. Create KastenDRRestore resource referring to the KastenDRReview resource and choosing one of the restore points provided in the KastenDRReview status.
6. The steps 4 and 5 can be skipped and KastenDRRestore resource can be created directly with the source cluster information.
7. Delete the KastenDRReview and KastenDRRestore resources after restore completes. Following recovery of the Veeam Kasten restore point catalog, restore cluster-scoped resources and applications as required.

## Recovering Veeam Kasten From a Disaster via Helm â

The k10restore tool has has been deprecated and will be removed in a future release. See Recovering Veeam Kasten from a Disaster via UI and Recovering Veeam Kasten from a Disaster via CLI for
    supported recovery options.

Recovering from a KDR backup using k10restore involves the
  following sequence of actions:

1. Create a Kubernetes Secret, k10-dr-secret , using the passphrase provided while enabling Disaster Recovery
2. Install a fresh Veeam Kasten instance in the same namespace as the above Secret
3. Provide bucket information and credentials for the object storage location or NFS/SMB file storage location where previous Veeam Kasten backups are stored
4. Restoring the Veeam Kasten backup
5. Uninstalling the Veeam Kasten restore instance after recovery is recommended

If Kasten was previously installed in FIPS mode, ensure the fresh Veeam
    Kasten instance is also installed in FIPS mode.

If Veeam Kasten backup is stored using an NFS/SMB File Storage Location , it is important that the same NFS share is reachable from
    the recovery cluster and is mounted on all nodes where Veeam Kasten is
    installed.

### Specifying a Disaster Recovery Passphrase â

Currently, Veeam Kasten Disaster Recovery encrypts all artifacts via the
  use of the AES-256-GCM algorithm. The passphrase entered while enabling
  Disaster Recovery is used for this encryption. On the cluster used for
  Veeam Kasten recovery, the Secret k10-dr-secret needs to be therefore
  created using that same passphrase in the Veeam Kasten namespace
  (default kasten-io )

The passphrase can be provided as a raw string or reference a secret in
  HashiCorp Vault or AWS Secrets Manager.

Specifying the passphrase as a raw string:

```
$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal key=<passphrase>
```

Specifying the passphrase as a HashiCorp Vault secret:

```
$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=vault \   --from-literal vault-kv-version=<version-of-key-value-secrets-engine> \   --from-literal vault-mount-path=<path-where-key-value-engine-is-mounted> \   --from-literal vault-secret-path=<path-from-mount-to-passphrase-key> \   --from-literal key=<name-of-passphrase-key># Example$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=vault \   --from-literal vault-kv-version=KVv1 \   --from-literal vault-mount-path=secret \   --from-literal vault-secret-path=k10 \   --from-literal key=passphrase
```

The supported values for vault-kv-version are KVv1 and KVv2 .

Using a passphrase from HashiCorp Vault also requires enabling HashiCorp
    Vault authentication when installing the kasten/k10restore helm chart.
    Refer: Enabling HashiCorp Vault using Token Auth or Kubernetes Auth .

Specifying the passphrase as an AWS Secrets Manager secret:

```
$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=aws \   --from-literal aws-region=<aws-region-for-secret> \   --from-literal key=<aws-secret-name># Example$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=aws \   --from-literal aws-region=us-east-1 \   --from-literal key=k10/dr/passphrase
```

### Reinstalling Veeam Kasten â

When reinstalling Veeam Kasten on the same cluster, it is important to
    clean up the namespace in which Veeam Kasten was previously installed
    before the above passphrase creation.

```
# Delete the kasten-io namespace.$ kubectl delete namespace kasten-io
```

Veeam Kasten must be reinstalled before recovery. Please follow the
  instructions here .

### Configuring Location Profile â

Create a Location Profile with the object storage location or NFS/SMB file storage
  location where Veeam Kasten KDR backups are stored.

### Restoring Veeam Kasten with k10restore â

Requirements:

- Source cluster ID
- Name of Location Profile from the previous step

```
# Install the helm chart that creates the Kasten restore job and wait for completion of the `k10-restore` job# Assumes that Kasten is installed in the 'kasten-io' namespace.$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name>
```

If Veeam Kasten Quick Disaster Recovery is enabled, the Veeam Kasten
  restore helm chart should be installed with the following helm value:

```
--set quickMode.enabled=true \--set quickMode.overrideResources=true
```

The [overrideResources] flag must be set to true when using
    Quick Disaster Recovery. Since the Disaster Recovery operation involves
    creating or replacing resources, confirmation should be provided by
    setting this flag.

Veeam Kasten provides the ability to apply labels and annotations to all
  temporary worker pods created during Veeam Kasten recovery as part of
  its operation. The labels and annotations can be set through the podLabels and podAnnotations Helm flags, respectively. For example,
  if using a values.yaml file:

```
podLabels:   app.kubernetes.io/component: "database"   topology.kubernetes.io/region: "us-east-1"podAnnotations:   config.kubernetes.io/local-config: "true"   kubernetes.io/description: "Description"
```

Alternatively, the Helm parameters can be configured using the --set flag:

```
--set podLabels.labelKey1=value1 --set podLabels.labelKey2=value2 \--set podAnnotations.annotationKey1="Example annotation" --set podAnnotations.annotationKey2=value2
```

The restore job always restores the restore point catalog and artifact
  information. If the restore of other resources (options include
  profiles, policies, secrets) needs to be skipped, the skipResource flag can be used.

```
# e.g. to skip restore of profiles and policies, helm install command will be as follows:$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name> \    --set skipResource="profiles\,policies"
```

The timeout of the entire restore process can be configured by the helm
  field restore.timeout . The type of this field is int and the value
  is in minutes.

```
# e.g. to specify the restore timeout, helm install command will be as follows:$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name> \    --set restore.timeout=<timeout-in-minutes>
```

If the Disaster Recovery Location Profile was configured for Immutable Backups ,
  Veeam Kasten can be restored to an earlier point in time. The protection
  period chosen when creating the profile determines how far in the past
  the point-in-time can be. Set the pointInTime helm value to the
  desired time stamp.

```
# e.g. to restore Kasten to 15:04:05 UTC on Jan 2, 2022:$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name> \    --set pointInTime="2022-01-02T15:04:05Z"
```

See Immutable Backups Workflow for additional information.

### Restoring Veeam Kasten Backup with Iron Bank Kasten Images â

The general instructions found in Restoring Veeam Kasten with k10restore can be used for restoring Veeam Kasten using Iron Bank
  hardened images with a few changes.

Specific helm values are used to ensure that the Veeam Kasten
  restore helm chart only uses Iron Bank images.
  The values file must be downloaded by running:

```
$ curl -sO https://docs.kasten.io/ironbank/k10restore-ironbank-values.yaml
```

This file is protected and should not be modified. It is necessary
    to specify all other values using the corresponding helm flags, such as --set , --values , etc.

Credentials for Registry1 must be provided in order to successfully pull
  the images. These should already have been created as part of re-deploying a
  new Veeam Kasten instance; therefore, only the name of the secret should be
  used here.

The following set of flags should be added to the instructions found in Restoring Veeam Kasten with k10restore to use
  Iron Bank images for Veeam Kasten recovery:

```
...   --values=<PATH TO DOWNLOADED k10restore-ironbank-values.yaml> \   --set-json 'imagePullSecrets=[{"name": "k10-ecr"}]' \   ...
```

### Restoring Veeam Kasten Backup in FIPS Mode â

The general instructions found in Restoring Veeam Kasten with k10restore can be used for restoring Veeam Kasten in FIPS mode with a few changes.

To ensure that certified cryptographic modules are utilized, you must install
  the k10restore chart with additional Helm values that can be found here: FIPS values . These should be added to the
  instructions found in Restoring Veeam Kasten with k10restore for Veeam Kasten disaster recovery:

```
...   --values=https://docs.kasten.io/latest/fips/fips-restore-values.yaml   ...
```

### Restoring Veeam Kasten Backup in Air-Gapped environment â

In case of air-gapped installations, it's assumed that k10offline tool is used to push the images to a private container registry.
  Below command can be used to instruct k10restore to run in air-gapped mode.

```
# Install the helm chart that creates the Kasten restore job and wait for completion of the `k10-restore` job.# Assume that Kasten is installed in the 'kasten-io' namespace.$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set airgapped.repository=repo.example.com \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name>
```

### Restoring Veeam Kasten Backup with Google Workload Identity Federation â

Veeam Kasten can be restored from a Google Cloud Storage bucket using
  the Google Workload Identity Federation. Please follow the instructions
  provided here to
  restore Veeam Kasten with this option.

### Uninstalling k10restore â

The K10restore instance can be uninstalled with the helm uninstall command.

```
# e.g. to uninstall K10restore from the kasten-io namespace   $ helm uninstall k10-restore --namespace=kasten-io
```

#### Enabling HashiCorp Vault using Token Auth â

Create a Kubernetes secret with the Vault token.

```
kubectl create secret generic vault-creds \       --namespace kasten-io \       --from-literal vault_token=<vault-token>
```

This may cause the token to be stored in shell history.

Use these additional parameters when installing the kasten/k10restore helm chart.

```
--set vault.enabled=true \   --set vault.address=<vault-server-address> \   --set vault.secretName=<name-of-secret-with-vault-creds>
```

#### Enabling HashiCorp Vault using Kubernetes Auth â

Refer to Configuring Vault Server For Kubernetes Auth prior to installing the kasten/k10restore helm chart.

```
--set vault.enabled=true \    --set vault.address=<vault-server-address> \    --set vault.role=<vault-kubernetes-authentication-role_name> \    --set vault.serviceAccountTokenPath=<service-account-token-path> # optional
```

vault.role is the name of the Vault Kubernetes authentication role binding
  the Veeam Kasten service account and namespace to the Vault policy.

vault.serviceAccountTokenPath is optional and defaults to /var/run/secrets/kubernetes.io/serviceaccount/token .

## Recovering with the Operator â

If you have deployed Veeam Kasten via the OperatorHub on an OpenShift cluster,
  the k10restore tool can be deployed via the Operator as described below.
  However, it is recommended to use either the Recovering Veeam Kasten from a Disaster via UI or Recovering Veeam Kasten from a Disaster via CLI process.

Recovering from a Veeam Kasten backup involves the following sequence of
  actions:

1. Install a fresh Veeam Kasten instance.
2. Configure a Location Profile from where the Veeam Kasten backup will be restored.
3. Create a Kubernetes Secret named k10-dr-secret in the same namespace as the Veeam Kasten install, with the passphrase given when disaster recovery was enabled on the previous Veeam Kasten instance. The commands are detailed here .
4. Create a K10restore instance. The required values are Cluster ID - value given when disaster recovery was enabled on the previous Veeam Kasten instance. Profile name - name of the Location Profile configured in Step 2. and the optional values are Point in time - time (RFC3339) at which to evaluate restore data. Example "2022-01-02T15:04:05Z". Resources to skip - can be used to skip restore of specific resources. Example "profile,policies". After recovery, deleting the k10restore instance is recommended.

Install a fresh Veeam Kasten instance.

Configure a Location Profile from where the Veeam Kasten backup will be restored.

Create a Kubernetes Secret named k10-dr-secret in the same
      namespace as the Veeam Kasten install, with the passphrase given
      when disaster recovery was enabled on the previous Veeam Kasten
      instance. The commands are detailed here .

Create a K10restore instance. The required values are

- Cluster ID - value given when disaster recovery was enabled on the previous Veeam Kasten instance.
- Profile name - name of the Location Profile configured in Step 2.

and the optional values are

- Point in time - time (RFC3339) at which to evaluate restore data. Example "2022-01-02T15:04:05Z".
- Resources to skip - can be used to skip restore of specific resources. Example "profile,policies".

After recovery, deleting the k10restore instance is recommended.

Operator K10restore form view with Enable HashiCorp Vault set to False

Operator K10restore form view with Enable HashiCorp Vault set to True

## Using the Restored Veeam Kasten in Place of the Original â

The newly restored Veeam Kasten includes a safety mechanism to prevent
  it from performing critical background maintenance operations on backup
  data in storage. These operations are exclusive, meaning that there
  is only one Veeam Kasten instance should perform them one at a time.
  The DR-restored Veeam Kasten initially assumes that it does not have
  permission to perform these maintenance tasks. This assumption is
  made in case the original source, Veeam Kasten, is still running,
  especially during scenarios like testing the DR restore procedure in
  a secondary test cluster while the primary production Veeam Kasten is
  still active.

If no other Veeam Kasten instances are accessing the same sets of backup
  data (i.e., the original Veeam Kasten has been uninstalled and only the new
  DR-restored Veeam Kasten remains), it can be signaled that the new Veeam
  Kasten is now eligible to take over the maintenance duties by deleting
  the following resource:

```
# Delete the k10-dr-remove-to-get-ownership configmap in the Kasten namespace.$ kubectl delete configmap --namespace=kasten-io k10-dr-remove-to-get-ownership
```

It is critical that you delete this resource only when you are prepared
    to make the permanent cutover to the new DR-restored Veeam Kasten instance.
    Running multiple Veeam Kasten instances simultaneously, each assuming
    ownership, can corrupt backup data.

---

## Operating Dr

As Veeam Kasten is a stateful application running on the
  cluster, it must be responsible for backing up its own data to enable
  recovery in the event of disaster. This backup is enabled by the
  Veeam Kasten Disaster Recovery (KDR) policy. In particular, KDR
  provides the ability to recover the Veeam Kasten platform
  from a variety of disasters, such as the unintended deletion of
  Veeam Kasten or its restore points, the failure of the underlying
  storage used by Veeam Kasten, or even the accidental
  destruction of the Kubernetes cluster on which Veeam Kasten is deployed.

## Configuring Veeam Kasten Disaster Recovery Mode â

The KDR mode specifies how internal Veeam Kasten resources are protected. The
  mode must be set before enabling the KDR policy. Changes
  to the KDR mode only apply to future KDR policy runs.

Starting in Veeam Kasten v8.0.0, all installations default to Quick DR (Local Catalog Snapshot) mode.

Quick DR (Local Catalog Snapshot) mode should only be enabled if the storage provisioner
    used for Veeam Kasten PVCs supports both the creation of storage snapshots
    and the ability to restore the existing volume from a storage snapshot. See Comparing Available KDR Modes for details on alternate
    configuration options.

- To enable Legacy DR mode, install or upgrade Veeam Kasten with the --set kastenDisasterRecovery.quickMode.enabled=false Helm value.
- To enable Quick DR mode, install or upgrade Veeam Kasten with the --set kastenDisasterRecovery.quickMode.enabled=true Helm value.
- See Enabling Veeam Kasten Disaster Recovery via UI or Enabling Veeam Kasten Disaster Recovery via CLI for details on configuring catalog snapshot behavior for Quick DR mode.

## Comparing Available KDR Modes â

Refer to the details below to understand the key differences between
  each mode:

### Legacy DR â

Legacy DR mode has been deprecated and will be removed in a future release.
    All clusters should be migrated a supported Quick DR configuration.

Recommended Usage

- Supported for backwards-compatibility only

Actions Performed Per KDR Policy Run

- Exports a full copy of the catalog database

Resources Available to Recover

- Enables recovery of specified Veeam Kasten custom resources
- Enables recovery of local restore points, exported restore points, and action history on any cluster Note It is expected that local restore points will be non-restorable when a KDR recovery of the exported catalog snapshot is performed on a different cluster, as applicable storage snapshot references are typically unavailable.

Enables recovery of specified Veeam Kasten custom resources

Enables recovery of local restore points, exported
      restore points, and action history on any cluster

It is expected that local restore points will be non-restorable when a
        KDR recovery of the exported catalog snapshot is performed on a different cluster, as
        applicable storage snapshot references are typically unavailable.

### Quick DR (Local Catalog Snapshot) â

- Recommended when storage used for Veeam Kasten PVCs supports both the creation of storage snapshots and the ability to provision a volume using a storage snapshot

- Creates a local snapshot of the catalog PVC
- Incrementally exports minimally required data only from the catalog database

- Enables recovery of specified Veeam Kasten custom resources
- Enables recovery of exported restore points on any cluster
- Enables recovery of local restore points, exported restore points, and action history only where the local catalog snapshot is available for restore (i.e. in-place recovery on the original cluster)

Compared to Legacy DR

- Offers faster KDR policy runs by reducing amount of exported data
- Consumes less repository storage by reducing amount of exported data
- Offers faster KDR recovery when leveraging local storage snapshot
- Protects additional Veeam Kasten custom resource types

### Quick DR (Exported Catalog Snapshot) â

- Recommended when storage used for Veeam Kasten PVCs supports the creation of storage snapshots but cannot provision a volume using a storage snapshot
- Recommended when there is a need to reduce retention of local storage snapshots without impacting retention of exported backups
- This mode may be selected for any snapshot-capable storage in order to provide the highest level of resilience

- Creates a local snapshot of the catalog PVC
- Incrementally exports minimally required data only from the catalog database
- Performs an incremental export of the catalog PVC snapshot data

- Offers comparable KDR policy run completion times
- Consumes less repository storage by exporting incremental catalog data
- Offers faster KDR recovery when leveraging local storage snapshot
- Offers comparable KDR recovery when leveraging exported storage snapshot
- Protects additional Veeam Kasten resource types

### Quick DR (No Catalog Snapshot) â

- Recommended when no available cluster storage supports snapshot creation (i.e. only Generic Storage Backup is used)
- Alternatively, this mode may be selected if there is no requirement to recover local restore points or action history

- Incrementally exports minimally required data only from the catalog database

- Enables recovery of specified Veeam Kasten custom resources
- Enables recovery of exported restore points on any cluster

- Offers faster KDR policy runs by reducing amount of exported data
- Consumes less repository storage by reducing amount of exported data
- Offers faster KDR recovery by reducing amount of imported data
- Protects additional Veeam Kasten custom resource types
- Does not support recovery of local restore points and action history

### KDR Protected Resource Matrix â

| Veeam Kasten Resource | Quick DR | Legacy DR | Actions | Yes(1) | Yes |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Actions | Yes(1) | Yes |
| Local Restore Points | Yes(1) | Yes |
| Exported Restore Points | Yes | Yes |
| Policies | Yes | Yes |
| Basic User Policies | Yes | No |
| Profiles | Yes | Yes |
| Blueprints | Yes | Yes |
| Blueprint Bindings | Yes | No |
| Policy Presets | Yes | No |
| Transform Sets | Yes | No |
| Multi-Cluster Primary | Yes | No |
| Multi-Cluster Secondary | Yes | No |
| Reports | No | No |
| ActionPodSpecs | No | No |
| AuditConfig | No | No |
| StorageSecurityContext | Yes | No |
| StorageSecurityContextBinding | Yes | No |

For Quick DR, resources marked with (1) can only be
    restored if a local or exported catalog snapshot is available
    to be restored.

## Enabling Veeam Kasten Disaster Recovery via UI â

Enabling Veeam Kasten Disaster Recovery (KDR) creates a dedicated
  policy within Veeam Kasten to back up its resources and catalog data
  to an external location profile .

The Veeam Kasten Disaster Recovery settings are accessible via the Setup Kasten DR page under the Settings menu in the navigation
  sidebar.

- Specify a location profile to which KDR backups will be exported. It is strongly recommended to use a location profile that supports immutable backups to ensure restore point catalog data can be recovered in the event of incidents including ransomware and accidental deletion. Note Veeam Repository location profiles cannot be used as a destination for KDR backups.
- Select and configure the desired passphrase method that will be used to encrypt KDR backups: Passphrase warning It is critical that this unmanaged passphrase be stored securely outside of the cluster as it will be required to perform any future recoveries. HashiCorp Vault Note Using HashiCorp Vault requires that Veeam Kasten is configured to access Vault . AWS Secrets Manager Note Using AWS Secrets Manager requires that an AWS Infrastructure Profile exists with the required permissions
- If Quick DR mode is enabled, specify the desired catalog snapshot behavior. See comparison for details and recommendations. Note Updating the catalog snapshot configuration may be performed by disabling and re-enabling KDR.
- Select Enable Kasten DR . A confirmation with the configuration and cluster ID will be displayed when KDR is enabled. This ID is used as a prefix to the object or file storage location where Veeam Kasten saves its exported backup data. Tip The Cluster ID value for a given cluster can also be accessed using the following kubectl command: # Extract UUID of the `default` namespace kubectl get namespace default -o jsonpath = "{.metadata.uid}{' \n '}" warning After enabling KDR it is critical to retain the following to successfully recover Veeam Kasten from a disaster: The source Cluster ID The KDR passphrase (or external secret manager details) The KDR location profile details and credential Without this information, restore point catalog recovery will not be possible.

Specify a location profile to which KDR backups will be exported.

It is strongly recommended to use a location profile
      that supports immutable backups to ensure
      restore point catalog data can be recovered in the event of
      incidents including ransomware and accidental deletion.

Veeam Repository location profiles cannot be used as a destination for KDR backups.

Select and configure the desired passphrase method that will be used to encrypt KDR backups:

Passphrase

It is critical that this unmanaged passphrase be stored securely outside
        of the cluster as it will be required to perform any future recoveries.

HashiCorp Vault

Using HashiCorp Vault requires that Veeam Kasten is configured to access Vault .

AWS Secrets Manager

Using AWS Secrets Manager requires that an AWS Infrastructure Profile exists with the required permissions

If Quick DR mode is enabled, specify the desired catalog snapshot behavior. See comparison for details and recommendations.

Updating the catalog snapshot configuration may be performed by disabling and re-enabling KDR.

Select Enable Kasten DR .

A confirmation with the configuration and cluster ID will be displayed when KDR is enabled.
      This ID is used as a prefix to the object or file storage location where Veeam Kasten
      saves its exported backup data.

The Cluster ID value for a given cluster can also be accessed using the following kubectl command:

```
# Extract UUID of the `default` namespacekubectl get namespace default -o jsonpath="{.metadata.uid}{'\n'}"
```

After enabling KDR it is critical to retain the following to successfully recover Veeam Kasten
        from a disaster:

- The source Cluster ID
- The KDR passphrase (or external secret manager details)
- The KDR location profile details and credential

Without this information, restore point catalog recovery will not be possible.

## Enabling Veeam Kasten Disaster Recovery via CLI â

As KDR backups are performed via a Veeam Kasten policy, configuration
  of KDR may be automated via CLI or GitOps tools. Each of the following
  examples assume deployment to the kasten-io namespace and must be
  modified to reflect environment specific details including location
  profile name, frequency, and retention.

- Create the k10-dr-secret Secret with the passphrase to be used to encrypt KDR backups: kubectl create secret generic k10-dr-secret --namespace kasten-io --from-literal key = < PASSPHRASE >
- Modify and apply one of the following k10-disaster-recovery-policy Policy examples. See comparison for available mode details and recommendations. Quick DR (Local Catalog Snapshot) - Default apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io kdrSnapshotConfiguration : takeLocalCatalogSnapshot : true Quick DR (Exported Catalog Snapshot) apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io - action : export exportParameters : exportData : enabled : true profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io kdrSnapshotConfiguration : exportCatalogSnapshot : true takeLocalCatalogSnapshot : true Quick DR (No Catalog Snapshot) apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io kdrSnapshotConfiguration : { } Legacy DR (Full Catalog Export) apiVersion : config.kio.kasten.io/v1alpha1 kind : Policy metadata : name : k10 - disaster - recovery - policy namespace : kasten - io spec : actions : - action : backup backupParameters : filters : { } profile : name : <NAME OF LOCATION PROFILE > namespace : kasten - io frequency : '@hourly' retention : daily : 1 hourly : 4 monthly : 1 weekly : 1 yearly : 1 selector : matchExpressions : - key : k10.kasten.io/appNamespace operator : In values : - kasten - io

Create the k10-dr-secret Secret with the passphrase to be used to encrypt KDR backups:

```
kubectl create secret generic k10-dr-secret  --namespace kasten-io  --from-literal key=<PASSPHRASE>
```

Modify and apply one of the following k10-disaster-recovery-policy Policy examples. See comparison for available mode details and recommendations.

Quick DR (Local Catalog Snapshot) - Default

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:      - key: k10.kasten.io/appNamespace        operator: In        values:          - kasten-io  kdrSnapshotConfiguration:    takeLocalCatalogSnapshot: true
```

Quick DR (Exported Catalog Snapshot)

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   - action: export    exportParameters:      exportData:        enabled: true      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io  frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:    - key: k10.kasten.io/appNamespace      operator: In      values:        - kasten-io  kdrSnapshotConfiguration:    exportCatalogSnapshot: true    takeLocalCatalogSnapshot: true
```

Quick DR (No Catalog Snapshot)

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:    - key: k10.kasten.io/appNamespace      operator: In      values:        - kasten-io  kdrSnapshotConfiguration: {}
```

Legacy DR (Full Catalog Export)

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: k10-disaster-recovery-policy  namespace: kasten-iospec:  actions:  - action: backup    backupParameters:      filters: {}      profile:        name: <NAME OF LOCATION PROFILE>        namespace: kasten-io   frequency: '@hourly'  retention:    daily: 1    hourly: 4    monthly: 1    weekly: 1    yearly: 1  selector:    matchExpressions:    - key: k10.kasten.io/appNamespace      operator: In      values:        - kasten-io
```

## Managing the Veeam Kasten Disaster Recovery Policy â

A policy named k10-disaster-recovery-policy that implements
  KDR functionality will automatically be created when
  KDR is enabled. This policy can be viewed through the Policies page in the navigation sidebar.

Click Run Once on the k10-disaster-recovery-policy to start a
  manual backup.

Click Edit to modify the frequency and retention settings. It is
  recommended that the KDR policy match the frequency of the lowest RPO
  policy on the cluster.

## Disabling Veeam Kasten Disaster Recovery â

Veeam Kasten Disaster Recovery can be disabled by clicking the Disable Kasten DR button on the Setup Kasten DR page, which is found
  under the Settings menu in the navigation sidebar.

It is not recommended to run Veeam Kasten without KDR enabled.

## Recovering Veeam Kasten from a Disaster via UI â

To recover from a KDR backup using the UI, follow these steps:

1. On a new cluster, install a fresh Veeam Kasten instance in the same namespace as the original Veeam Kasten instance.
2. On the new cluster, create a location profile by providing the bucket information and credentials for the object storage location or NFS/SMB file storage location where previous Veeam Kasten backups are stored.
3. On the new cluster, navigate to the Restore Kasten page under the Settings menu in the navigation sidebar.
4. In the Profile drop-down, select the location profile created in step 3.

1. For Cluster ID, provide the ID of the original cluster with Veeam Kasten Disaster Recovery enabled. This ID can be found on the Setup Kasten DR page of the original cluster that currently has Veeam Kasten Disaster Recovery enabled.

- Raw passphrase: Provide the passphrase used when enabling Disaster Recovery.

- HashiCorp Vault: Provide the Key Value Secrets Engine Version, Mount, Path, and Passphrase Key stored in a HashiCorp Vault secret.

- AWS Secrets Manager: Provide the secret name, its associated region, and the key.

For immutable location profiles, a previous point in time can be
    provided to filter out any restore points newer than the specified
    time in the next step. If no specific date is chosen, it will display
    all available restore points, with the most recent ones appearing
    first.

1. Click the Next button to start the validation process. If validation succeeds, a drop-down containing the available restore points will be displayed.

All times are displayed in the local timezone of the client's
    browser.

1. Select the desired restore point and click the Next button.
2. Review the summary and click the Start Restore button to begin the restore process.

1. Upon completion of a successful restoration, navigation to the dashboard and information about ownership and deletion of the configmap is displayed.

Following recovery of the Veeam Kasten restore point catalog,
  restore cluster-scoped resources and applications as required.

## Recovering Veeam Kasten from a Disaster via CLI â

In Veeam Kasten v7.5.0 and above, KDR recoveries can be performed via
  API or CLI using DR API Resources .
  Recovering from a KDR backup using CLI involves the following
  sequence of steps:

1. Create a Kubernetes Secret, k10-dr-secret , using the passphrase provided while enabling Disaster Recovery as described in Specifying a Disaster Recovery Passphrase .
2. Install a fresh Veeam Kasten instance in the same namespace as the above Secret.
3. Provide bucket information and credentials for the object storage location or NFS/SMB file storage location where previous Veeam Kasten backups are stored.
4. Create KastenDRReview resource providing the source cluster information.
5. Create KastenDRRestore resource referring to the KastenDRReview resource and choosing one of the restore points provided in the KastenDRReview status.
6. The steps 4 and 5 can be skipped and KastenDRRestore resource can be created directly with the source cluster information.
7. Delete the KastenDRReview and KastenDRRestore resources after restore completes. Following recovery of the Veeam Kasten restore point catalog, restore cluster-scoped resources and applications as required.

## Recovering Veeam Kasten From a Disaster via Helm â

The k10restore tool has has been deprecated and will be removed in a future release. See Recovering Veeam Kasten from a Disaster via UI and Recovering Veeam Kasten from a Disaster via CLI for
    supported recovery options.

Recovering from a KDR backup using k10restore involves the
  following sequence of actions:

1. Create a Kubernetes Secret, k10-dr-secret , using the passphrase provided while enabling Disaster Recovery
2. Install a fresh Veeam Kasten instance in the same namespace as the above Secret
3. Provide bucket information and credentials for the object storage location or NFS/SMB file storage location where previous Veeam Kasten backups are stored
4. Restoring the Veeam Kasten backup
5. Uninstalling the Veeam Kasten restore instance after recovery is recommended

If Kasten was previously installed in FIPS mode, ensure the fresh Veeam
    Kasten instance is also installed in FIPS mode.

If Veeam Kasten backup is stored using an NFS/SMB File Storage Location , it is important that the same NFS share is reachable from
    the recovery cluster and is mounted on all nodes where Veeam Kasten is
    installed.

### Specifying a Disaster Recovery Passphrase â

Currently, Veeam Kasten Disaster Recovery encrypts all artifacts via the
  use of the AES-256-GCM algorithm. The passphrase entered while enabling
  Disaster Recovery is used for this encryption. On the cluster used for
  Veeam Kasten recovery, the Secret k10-dr-secret needs to be therefore
  created using that same passphrase in the Veeam Kasten namespace
  (default kasten-io )

The passphrase can be provided as a raw string or reference a secret in
  HashiCorp Vault or AWS Secrets Manager.

Specifying the passphrase as a raw string:

```
$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal key=<passphrase>
```

Specifying the passphrase as a HashiCorp Vault secret:

```
$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=vault \   --from-literal vault-kv-version=<version-of-key-value-secrets-engine> \   --from-literal vault-mount-path=<path-where-key-value-engine-is-mounted> \   --from-literal vault-secret-path=<path-from-mount-to-passphrase-key> \   --from-literal key=<name-of-passphrase-key># Example$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=vault \   --from-literal vault-kv-version=KVv1 \   --from-literal vault-mount-path=secret \   --from-literal vault-secret-path=k10 \   --from-literal key=passphrase
```

The supported values for vault-kv-version are KVv1 and KVv2 .

Using a passphrase from HashiCorp Vault also requires enabling HashiCorp
    Vault authentication when installing the kasten/k10restore helm chart.
    Refer: Enabling HashiCorp Vault using Token Auth or Kubernetes Auth .

Specifying the passphrase as an AWS Secrets Manager secret:

```
$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=aws \   --from-literal aws-region=<aws-region-for-secret> \   --from-literal key=<aws-secret-name># Example$ kubectl create secret generic k10-dr-secret \   --namespace kasten-io \   --from-literal source=aws \   --from-literal aws-region=us-east-1 \   --from-literal key=k10/dr/passphrase
```

### Reinstalling Veeam Kasten â

When reinstalling Veeam Kasten on the same cluster, it is important to
    clean up the namespace in which Veeam Kasten was previously installed
    before the above passphrase creation.

```
# Delete the kasten-io namespace.$ kubectl delete namespace kasten-io
```

Veeam Kasten must be reinstalled before recovery. Please follow the
  instructions here .

### Configuring Location Profile â

Create a Location Profile with the object storage location or NFS/SMB file storage
  location where Veeam Kasten KDR backups are stored.

### Restoring Veeam Kasten with k10restore â

Requirements:

- Source cluster ID
- Name of Location Profile from the previous step

```
# Install the helm chart that creates the Kasten restore job and wait for completion of the `k10-restore` job# Assumes that Kasten is installed in the 'kasten-io' namespace.$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name>
```

If Veeam Kasten Quick Disaster Recovery is enabled, the Veeam Kasten
  restore helm chart should be installed with the following helm value:

```
--set quickMode.enabled=true \--set quickMode.overrideResources=true
```

The [overrideResources] flag must be set to true when using
    Quick Disaster Recovery. Since the Disaster Recovery operation involves
    creating or replacing resources, confirmation should be provided by
    setting this flag.

Veeam Kasten provides the ability to apply labels and annotations to all
  temporary worker pods created during Veeam Kasten recovery as part of
  its operation. The labels and annotations can be set through the podLabels and podAnnotations Helm flags, respectively. For example,
  if using a values.yaml file:

```
podLabels:   app.kubernetes.io/component: "database"   topology.kubernetes.io/region: "us-east-1"podAnnotations:   config.kubernetes.io/local-config: "true"   kubernetes.io/description: "Description"
```

Alternatively, the Helm parameters can be configured using the --set flag:

```
--set podLabels.labelKey1=value1 --set podLabels.labelKey2=value2 \--set podAnnotations.annotationKey1="Example annotation" --set podAnnotations.annotationKey2=value2
```

The restore job always restores the restore point catalog and artifact
  information. If the restore of other resources (options include
  profiles, policies, secrets) needs to be skipped, the skipResource flag can be used.

```
# e.g. to skip restore of profiles and policies, helm install command will be as follows:$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name> \    --set skipResource="profiles\,policies"
```

The timeout of the entire restore process can be configured by the helm
  field restore.timeout . The type of this field is int and the value
  is in minutes.

```
# e.g. to specify the restore timeout, helm install command will be as follows:$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name> \    --set restore.timeout=<timeout-in-minutes>
```

If the Disaster Recovery Location Profile was configured for Immutable Backups ,
  Veeam Kasten can be restored to an earlier point in time. The protection
  period chosen when creating the profile determines how far in the past
  the point-in-time can be. Set the pointInTime helm value to the
  desired time stamp.

```
# e.g. to restore Kasten to 15:04:05 UTC on Jan 2, 2022:$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name> \    --set pointInTime="2022-01-02T15:04:05Z"
```

See Immutable Backups Workflow for additional information.

### Restoring Veeam Kasten Backup with Iron Bank Kasten Images â

The general instructions found in Restoring Veeam Kasten with k10restore can be used for restoring Veeam Kasten using Iron Bank
  hardened images with a few changes.

Specific helm values are used to ensure that the Veeam Kasten
  restore helm chart only uses Iron Bank images.
  The values file must be downloaded by running:

```
$ curl -sO https://docs.kasten.io/ironbank/k10restore-ironbank-values.yaml
```

This file is protected and should not be modified. It is necessary
    to specify all other values using the corresponding helm flags, such as --set , --values , etc.

Credentials for Registry1 must be provided in order to successfully pull
  the images. These should already have been created as part of re-deploying a
  new Veeam Kasten instance; therefore, only the name of the secret should be
  used here.

The following set of flags should be added to the instructions found in Restoring Veeam Kasten with k10restore to use
  Iron Bank images for Veeam Kasten recovery:

```
...   --values=<PATH TO DOWNLOADED k10restore-ironbank-values.yaml> \   --set-json 'imagePullSecrets=[{"name": "k10-ecr"}]' \   ...
```

### Restoring Veeam Kasten Backup in FIPS Mode â

The general instructions found in Restoring Veeam Kasten with k10restore can be used for restoring Veeam Kasten in FIPS mode with a few changes.

To ensure that certified cryptographic modules are utilized, you must install
  the k10restore chart with additional Helm values that can be found here: FIPS values . These should be added to the
  instructions found in Restoring Veeam Kasten with k10restore for Veeam Kasten disaster recovery:

```
...   --values=https://docs.kasten.io/latest/fips/fips-restore-values.yaml   ...
```

### Restoring Veeam Kasten Backup in Air-Gapped environment â

In case of air-gapped installations, it's assumed that k10offline tool is used to push the images to a private container registry.
  Below command can be used to instruct k10restore to run in air-gapped mode.

```
# Install the helm chart that creates the Kasten restore job and wait for completion of the `k10-restore` job.# Assume that Kasten is installed in the 'kasten-io' namespace.$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set airgapped.repository=repo.example.com \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name>
```

### Restoring Veeam Kasten Backup with Google Workload Identity Federation â

Veeam Kasten can be restored from a Google Cloud Storage bucket using
  the Google Workload Identity Federation. Please follow the instructions
  provided here to
  restore Veeam Kasten with this option.

### Uninstalling k10restore â

The K10restore instance can be uninstalled with the helm uninstall command.

```
# e.g. to uninstall K10restore from the kasten-io namespace   $ helm uninstall k10-restore --namespace=kasten-io
```

#### Enabling HashiCorp Vault using Token Auth â

Create a Kubernetes secret with the Vault token.

```
kubectl create secret generic vault-creds \       --namespace kasten-io \       --from-literal vault_token=<vault-token>
```

This may cause the token to be stored in shell history.

Use these additional parameters when installing the kasten/k10restore helm chart.

```
--set vault.enabled=true \   --set vault.address=<vault-server-address> \   --set vault.secretName=<name-of-secret-with-vault-creds>
```

#### Enabling HashiCorp Vault using Kubernetes Auth â

Refer to Configuring Vault Server For Kubernetes Auth prior to installing the kasten/k10restore helm chart.

```
--set vault.enabled=true \    --set vault.address=<vault-server-address> \    --set vault.role=<vault-kubernetes-authentication-role_name> \    --set vault.serviceAccountTokenPath=<service-account-token-path> # optional
```

vault.role is the name of the Vault Kubernetes authentication role binding
  the Veeam Kasten service account and namespace to the Vault policy.

vault.serviceAccountTokenPath is optional and defaults to /var/run/secrets/kubernetes.io/serviceaccount/token .

## Recovering with the Operator â

If you have deployed Veeam Kasten via the OperatorHub on an OpenShift cluster,
  the k10restore tool can be deployed via the Operator as described below.
  However, it is recommended to use either the Recovering Veeam Kasten from a Disaster via UI or Recovering Veeam Kasten from a Disaster via CLI process.

Recovering from a Veeam Kasten backup involves the following sequence of
  actions:

1. Install a fresh Veeam Kasten instance.
2. Configure a Location Profile from where the Veeam Kasten backup will be restored.
3. Create a Kubernetes Secret named k10-dr-secret in the same namespace as the Veeam Kasten install, with the passphrase given when disaster recovery was enabled on the previous Veeam Kasten instance. The commands are detailed here .
4. Create a K10restore instance. The required values are Cluster ID - value given when disaster recovery was enabled on the previous Veeam Kasten instance. Profile name - name of the Location Profile configured in Step 2. and the optional values are Point in time - time (RFC3339) at which to evaluate restore data. Example "2022-01-02T15:04:05Z". Resources to skip - can be used to skip restore of specific resources. Example "profile,policies". After recovery, deleting the k10restore instance is recommended.

Install a fresh Veeam Kasten instance.

Configure a Location Profile from where the Veeam Kasten backup will be restored.

Create a Kubernetes Secret named k10-dr-secret in the same
      namespace as the Veeam Kasten install, with the passphrase given
      when disaster recovery was enabled on the previous Veeam Kasten
      instance. The commands are detailed here .

Create a K10restore instance. The required values are

- Cluster ID - value given when disaster recovery was enabled on the previous Veeam Kasten instance.
- Profile name - name of the Location Profile configured in Step 2.

and the optional values are

- Point in time - time (RFC3339) at which to evaluate restore data. Example "2022-01-02T15:04:05Z".
- Resources to skip - can be used to skip restore of specific resources. Example "profile,policies".

After recovery, deleting the k10restore instance is recommended.

Operator K10restore form view with Enable HashiCorp Vault set to False

Operator K10restore form view with Enable HashiCorp Vault set to True

## Using the Restored Veeam Kasten in Place of the Original â

The newly restored Veeam Kasten includes a safety mechanism to prevent
  it from performing critical background maintenance operations on backup
  data in storage. These operations are exclusive, meaning that there
  is only one Veeam Kasten instance should perform them one at a time.
  The DR-restored Veeam Kasten initially assumes that it does not have
  permission to perform these maintenance tasks. This assumption is
  made in case the original source, Veeam Kasten, is still running,
  especially during scenarios like testing the DR restore procedure in
  a secondary test cluster while the primary production Veeam Kasten is
  still active.

If no other Veeam Kasten instances are accessing the same sets of backup
  data (i.e., the original Veeam Kasten has been uninstalled and only the new
  DR-restored Veeam Kasten remains), it can be signaled that the new Veeam
  Kasten is now eligible to take over the maintenance duties by deleting
  the following resource:

```
# Delete the k10-dr-remove-to-get-ownership configmap in the Kasten namespace.$ kubectl delete configmap --namespace=kasten-io k10-dr-remove-to-get-ownership
```

It is critical that you delete this resource only when you are prepared
    to make the permanent cutover to the new DR-restored Veeam Kasten instance.
    Running multiple Veeam Kasten instances simultaneously, each assuming
    ownership, can corrupt backup data.

---

## Operating External Tools Datadog

First off the Datadog agent needs to be installed in the Kubernetes
  cluster. Documentation for that is found in the Datadog
docs . Make
  sure to enable the [prometheusScrape] option documented in prometheus scrape
docs .

```
# datadog helm values.yaml# ...datadog:# ...  prometheusScrape:    enabled: true# ...
```

Finally, to collect the Veeam Kasten metrics in Datadog, apply the
  following values to either the Veeam Kasten install or upgrade (using
  Helm).

```
# Veeam Kasten values.yamlprometheus:  server:    podAnnotations:      ad.datadoghq.com/prometheus-server.check_names: |        ["openmetrics"]      ad.datadoghq.com/prometheus-server.init_configs: |        [{}]      ad.datadoghq.com/prometheus-server.instances: |        [{          "prometheus_url": "http://%%host%%:%%port%%/k10/prometheus/federate?match[]=%7Bjob%3D~%22.%2B%22%7D",          "namespace": "kasten-io",          "metrics": ["*"],          "type_overrides": {"*": "counter"}        }]
```

for example, given the above [values.yaml] file, if doing a
  helm install, the command would be:

```
helm install k10 kasten/k10 --create-namespace --namespace kasten-io --values values.yaml
```

If doing a helm upgrade to patch your install with the above values, run
  the following:

```
helm --namespace kasten-io get values k10 > values.yaml# note, if no values have been applied yet, then that file will be empty# add the values from the example file above and runhelm upgrade k10 kasten/k10 --namespace kasten-io --values values.yaml
```

To dive deeper into adding metrics to Datadog see the following
  documentation links:

- Kubernetes Prometheus and OpenMetrics metrics collection
- Prometheus Helm Values - Server Pod Annotations
- Using Veeam Kasten's Prometheus Endpoint

---

## Operating Garbagecollector

Veeam Kasten provides a way to collect and clean up the resources that
  are either orphaned or their expiration period has passed.

The following Helm options can be used to tune Garbage Collector
  behavior:

- garbagecollector.daemonPeriod - the length of time between two consecutive garbage collection events (in seconds)
- garbagecollector.keepMaxActions - how many finished actions to keep (if value is less than or equal to 0, no actions will be deleted)
- garbagecollector.actions.enabled - enables action collectors ( boolean )

## Supported Resource Types â

Garbage Collector daemon can currently clean up the following resource
  types:

- Actions: When the limit, as defined by garbagecollector.keepMaxActions , is exceeded, the oldest actions are removed until the limit is reached. Each action type is handled independently in this process.
- RestorePointContents - expired manual backups will be removed as determined by spec.expiresAt . This can be set via kubectl or on the manual snapshot page in the UI.
- CSISnapshot - temporary CSI snapshots created during restore operations.
- PersistentVolumes - temporary volumes created during restore operations.

---

## Operating K10Tools

The k10tools binary has commands that can help with validating if a cluster
  is setup correctly before installing Veeam Kasten and for debugging Veeam
  Kasten's micro services. The latest version of k10tools can be found here .

Binaries are available for the following operating systems and architectures:

| Operating System | x86_84 (amd64) | Arm (arm64/v8) | Power (ppc64le) | Linux | Yes | Yes | Yes |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Linux | Yes | Yes | Yes |
| MacOS | Yes | Yes | No |
| Windows | Yes | Yes | No |

## Authentication Service â

The k10tools debug auth sub command can be used to debug Veeam
  Kasten's Authentication service when it is setup with Active Directory
  or OpenShift based authentication. Provide -d openshift flag for
  OpenShift based authentication. It verifies connection to the OpenShift
  OAuth server and the OpenShift Service Account token. It also searches
  for any error events in Service Account.

```
./k10tools debug authDex:  OIDC Provider URL: https://api.test  Release name: k10  Dex well known URL:https://api.test/k10/dex/.well-known/openid-configuration  Trying to connect to Dex without TLS (insecureSkipVerify=false)  Connection succeeded  -  OK./k10tools debug auth -d openshiftVerify OpenShift OAuth Server Connection:  Openshift URL - https://api.test:6443/.well-known/oauth-authorization-server  Trying to connect to Openshift without TLS (insecureSkipVerify=false)  Connection failed, testing other options  Trying to connect to Openshift with TLS but verification disabled (insecureSkipVerify=true)  Connection succeeded  -  OKVerify OpenShift Service Account Token:  Initiating token verification  Fetched ConfigMap - k10-dex  Service Account for OpenShift authentication - k10-dex-sa  Service account fetched  Secret - k10-dex-sa-token-7fwm7 retrieved  Token retrieved from Service Account secrets  Token retrieved from ConfigMap  Token matched  -  OKGet Service Account Error Events:  Searching for events with error in Service Account - k10-dex-sa  Found event/s in service account with error  {"type":"Warning","from":"service-account-oauth-client-getter","reason":"NoSAOAuthRedirectURIs","object":"ServiceAccount/k10-dex-sa","message":"system:serviceaccount:kasten-io:k10-dex-sa has no redirectURIs; set serviceaccounts.openshift.io/oauth-redirecturi.<some-value>=<redirect> or create a dynamic URI using serviceaccounts.openshift.io/oauth-redirectreference.<some-value>=<reference>","timestamp":"2021-04-08 05:06:06 +0000 UTC"} ({"message":"service account event error","function":"kasten.io/k10/kio/tools/k10primer/k10debugger.(*OpenshiftDebugger).getServiceAccountErrEvents","linenumber":224})  -  Error
```

## Catalog Service â

The k10tools debug catalog size sub command can be used to obtain the
  size of K10's catalog and the disk usage of the volume where the
  catalog is stored.

```
% ./k10tools debug catalog size Catalog Size:   total 380K -rw------- 1 kio kio 512K Jan 26 23:57 model-store.db Catalog Volume Disk Usage:   Filesystem                                                                Size  Used Avail Use% Mounted on /dev/disk/by-id/scsi-0DO_Volume_pvc-4acee649-5c24-4a79-955f-9d8fdfb10ac7   20G   45M   19G   1% /mnt/k10state
```

## Backup Actions â

The k10tools debug backupactions sub command can be used to obtain the
  [backupactions] created in the respective cluster. Use the -o json flag to obtain more information in the JSON format.

```
% ./k10tools debug backupactionsName                    Namespace CreationTimestamp                   PolicyName      PolicyNamespacescheduled-6wbzw         default       2021-01-29 07:57:08 +0000 UTC     default-backup    kasten-ioscheduled-5thsg         default       2021-01-29 05:37:03 +0000 UTC     default-backup    kasten-io
```

## Kubernetes Nodes â

The k10tools debug node sub command can be used to obtain information
  about the Kubernetes nodes. Use the -o json flag to obtain more
  information in the JSON format.

```
% ./k10tools debug node  Name                 |OS Image  onkar-1-pool-1-3d1cf |Debian GNU/Linux 10 (buster)  onkar-1-pool-1-3d1cq |Debian GNU/Linux 10 (buster)  onkar-1-pool-1-3d1cy |Debian GNU/Linux 10 (buster)
```

## Application Information â

The k10tools debug applications sub command can be used to obtain
  information about the applications running in given namespace. Use the -o json flag to obtain more information in the JSON format (Note:
  Right now, JSON format support is only provided for PVCs). Use -n to
  provide the namespace. In case the namespace is not provided,
  application information will be fetched from the default namespace.
  e.g. -n kasten-io

```
% ./k10tools debug applications  Fetching information from namespace - kasten-io | resource - ingresses  Name        |Hosts |Address        |Ports |Age |  k10-ingress |*     |138.68.228.199 |80    |36d |  Fetching information from namespace - kasten-io | resource - daemonsets  Resources not found  PVC Information -  Name                |Volume                                     |Capacity  catalog-pv-claim    |pvc-4fc67966-aee7-493c-b2fd-c6251933875c   |20Gi  jobs-pv-claim       |pvc-cdda0458-6b63-48a6-8e7f-c1b947600c9f   |20Gi  logging-pv-claim    |pvc-36a92c5b-d018-4ce8-ba79-970d15554387   |20Gi  metering-pv-claim   |pvc-8c0c6477-216d-4227-a6af-9725ce2a3dc1   |2Gi  prometheus-server   |pvc-1b14f51c-5abf-45f5-8bd9-1a58d86d58ef   |8Gi
```

## Veeam Kasten Primer for Pre-Flight Checks â

The k10tools primer sub command can be used to run pre-flight checks
  before installing Veeam Kasten. Refer to the section about Pre-Flight Checks for more details.

The code block below shows an example of the output when executed on a
  Kubernetes cluster deployed in Digital Ocean.

```
% ./k10tools primerKubernetes Version Check:  Valid kubernetes version (v1.17.13)  -  OKRBAC Check:  Kubernetes RBAC is enabled  -  OKAggregated Layer Check:  The Kubernetes Aggregated Layer is enabled  -  OKCSI Capabilities Check:  Using CSI GroupVersion snapshot.storage.k8s.io/v1alpha1  -  OKValidating Provisioners:kube-rook-ceph.rbd.csi.ceph.com:  Is a CSI Provisioner  -  OK  Storage Classes:    rook-ceph-block      Valid Storage Class  -  OK  Volume Snapshot Classes:    csi-rbdplugin-snapclass      Has k10.kasten.io/is-snapshot-class annotation set to true  -  OK      Has deletionPolicy 'Retain'  -  OKdobs.csi.digitalocean.com:  Is a CSI Provisioner  -  OK  Storage Classes:    do-block-storage      Valid Storage Class  -  OK  Volume Snapshot Classes:    do-block-storage      Has k10.kasten.io/is-snapshot-class annotation set to true  -  OK      Missing deletionPolicy, using defaultValidate Generic Volume Snapshot:  Pod Created successfully  -  OK  GVS Backup command executed successfully  -  OK  Pod deleted successfully  -  OK
```

## Veeam Kasten Primer for Upgrades â

The k10tools primer upgrade sub command can be used to find the
  recommended upgrade path of your Veeam Kasten version and to check there
  is adequate space to perform the upgrades. It only provides commands for
  Helm deployments. See install_upgrade for additional details. This tool requires Internet access to http://gcr.io

```
% ./k10tools primer upgradeCatalog Volume Disk Usage:  Filesystem      Size  Used Avail Use% Mounted on/dev/sdf         20G  1.3G   19G   7% /mnt/k10stateCurrent K10 Version: 4.5.5Latest K10 Version: 4.5.6Helm Install: true* To upgrade successfully you must have at least 50% free in catalog storageRecommended upgrade path:  helm repo update && \    helm get values k10 --output yaml --namespace=kasten-io > k10_val.yaml && \    helm upgrade k10 kasten/k10 --namespace=kasten-io -f k10_val.yaml --version=4.5.6
```

## Veeam Kasten Primer for Storage Connectivity Checks â

Run k10tools primer storage connect --help command to observe all
    supported sub-commands.

The k10tools primer storage connect command family can be used to
  check a given storage provider accessibility.

Currently the following storage providers are supported for this group
  of checks:

- Azure
- Google Cloud Storage (GCS)
- Portworx (PWX)
- S3 Compatible Storage
- Veeam Backup Server (VBR)
- vSphere

Each sub-command corresponding to a particular storage provider accepts
  a configuration file with parameters required for making connection. The
  configuration file format can be observed by issuing config-yaml sub-command in the following way (example is for GCS):

```
% ./k10tools primer storage connect gcs config-yaml## The geography in which Google Cloud Storage buckets are located#region: <gcs_region> # Example: us-central1## Google Cloud Platform project IDproject_id: <gcs_project_id>## Google Cloud Platform service keyservice_key: <gcs_service_key>## Maximum number of buckets to collect during checking connectivity to Google Cloud Storage.#list_buckets_limit: 10 # Default is 0## Google Cloud Storage operations with required parameters to check (Optional).## Use the same parameters to run actions against the same objects.operations:  - action: PutObject    #container_name: <gcs_bucket_name> # Container name    #object_name: <gcs_object_name> # Object name    #content_string: <object_content> # Object content string  - action: ListObjects    #container_name: <gcs_bucket_name> # Container name    #limit: 100 # Maximum number of items to collect (Optional). Default is 0  - action: DeleteObject    #container_name: <gcs_bucket_name> # Container name    #object_name: <gcs_object_name> # Object name
```

The output below is an example of running GCS connectivity checker:

```
% ./k10tools primer storage connect gcs -f ./gcs_check.yamlUsing "./gcs_check.yaml " file content as config sourceConnecting to Google Cloud Storage (region: us-west1)-> Connect to Google Cloud Storage-> List Google Cloud Storage containers-> Put Google Cloud Storage object-> List Google Cloud Storage objects-> Delete Google Cloud Storage objectGoogle Cloud Storage Connection Checker:  Connected to Google Cloud Storage with provided credentials  -  OK  Listed Google Cloud Storage containers: [testbucket20221123 55-demo 66-demo 77-demo]  -  OK  Added Google Cloud Storage object testblob20221123 to container testbucket20221123  -  OK  Listed Google Cloud Storage container testbucket20221123 objects: [testblob20221123]  -  OK  Deleted Google Cloud Storage object testblob20221123 from container testbucket20221123  -  OK
```

## Veeam Kasten Primer for Storage Integration Checks â

Run k10tools primer storage check --help command to observe all
    supported sub-commands.

### CSI Capabilities Check â

The k10tools primer storage check csi sub-command can be used to check
  a specified CSI storage class is able to carry out snapshot and
  restoration activities or report configuration issues if not. It creates
  a temporary application to test this.

The command accepts a configuration file in the following format:

```
% cat ./csi_check.yaml#storage_class: standard-rwo # specifies the storage class#run_as_user: 1000           # specifies the user the pod runs as
```

The output below is an example of running CSI checker:

```
% ./k10tools primer storage check csi -f ./csi_check.yamlUsing "./csi_check.yaml" file content as config sourceStarting CSI Checker. Could take up to 5 minutesCreating application  -> Created pod (kubestr-csi-original-podr2rkz) and pvc (kubestr-csi-original-pvc2fx6s)Taking a snapshot  -> Created snapshot (kubestr-snapshot-20220608113008)Restoring application  -> Restored pod (kubestr-csi-cloned-podhgx57) and pvc (kubestr-csi-cloned-pvccfh8w)Cleaning up resourcesCSI Snapshot Walkthrough:  Using annotated VolumeSnapshotClass (my-snapshotclass)  Successfully tested snapshot restore functionality.  -  OK
```

### Direct Cloud Provider Integration Checks â

The k10tools primer storage check sub-command family allows checking
  snapshot/restore capabilities through native API integration of capable
  cloud storage providers via direct storage API invocations.

For now the following cloud providers are supported:

- Amazon Elastic Block Store (AWS EBS)
- Azure Persistent Disk
- Google Compute Engine Persistent Disk (GCE PD)

To run a desired check the k10tools primer storage check command
  should be appended with either awsebs , or azure , or gcepd suffix.
  Each of these sub-commands accepts parameters passed via configuration
  files to create a test application performing snapshot/restore via
  vendor specific storage APIs. The format of which sub-command can be
  observed by executing k10tools primer storage check <awsebs|azure|gcepd> config-yaml .

Example configuration file format for GCE PD checker:

```
% ./k10tools primer storage check gcepd config-yaml## GCP Project IDproject_id: <gcp_project_id>## GCP Service Keyservice_key: <gcp_service_key>## Size of a GCE PD volume (in mebibytes) to be created during the testvolume_size: 100
```

The output below is an example of running GCE PD provider check:

```
% ./k10tools primer storage check gcepd -f ./gcepd_check.yamlUsing "./gcepd_check.yaml" file content as config sourceChecking Backup/Restore capabilities of GCE PD storage provider-> Setup Provider-> Create Namespace-> Create Affinity Pod-> Create Volume-> Create Test Pod-> Write Data-> Create Snapshot-> Delete Test Pod-> Delete Volume-> Restore Volume-> Restore Test Pod-> Verify Data-> Delete Test Pod-> Delete Affinity Pod-> Delete Namespace-> Delete Snapshot-> Delete VolumeGCE PD Backup/Restore Checker:  Created storage provider  -  OK  Created namespace 'primer-test-ns-8q9cl'  -  OK  Created affinity pod 'primer-affinity-pod-9ctmj'  -  OK  Created volume 'vol-2d7d9b2a-7701-11ed-8664-6a5ef5ff8566'  -  OK  Created test pod 'primer-test-pod-v6nc8'  -  OK  Wrote data '2022-12-08 18:04:25.144008 +0400 +04 m=+30.117055584' to pod 'primer-test-pod-v6nc8'  -  OK  Created snapshot 'snap-39be78a0-7701-11ed-8664-6a5ef5ff8566' for volume 'vol-2d7d9b2a-7701-11ed-8664-6a5ef5ff8566'  -  OK  Deleted test pod 'primer-test-pod-v6nc8'  -  OK  Deleted volume 'vol-2d7d9b2a-7701-11ed-8664-6a5ef5ff8566'  -  OK  Restored volume 'vol-65f2d4c0-7701-11ed-8664-6a5ef5ff8566' from snapshot 'snap-39be78a0-7701-11ed-8664-6a5ef5ff8566'  -  OK  Created test pod 'primer-test-pod-k7knx'  -  OK  Verified restored data  -  OK  Deleted test pod 'primer-test-pod-k7knx'  -  OK  Deleted affinity pod 'primer-affinity-pod-9ctmj'  -  OK  Deleted namespace 'primer-test-ns-8q9cl'  -  OK  Deleted snapshot 'snap-39be78a0-7701-11ed-8664-6a5ef5ff8566'  -  OK  Deleted volume 'vol-65f2d4c0-7701-11ed-8664-6a5ef5ff8566'  -  OK
```

### vSphere First Class Disk Integration Check â

Due to limited functionality provided by vSphere CSI driver Veeam Kasten
  has to use both volume provisioning via CSI interface and manual calling
  vSphere API for doing snapshots and restores of volumes.

The k10tools primer storage check vsphere sub-command provisions a
  First Class Disk (FCD) volume using a CSI storage class and performs
  snapshot/restore via vSphere API.

The command accepts a configuration file in the following format (can be
  observed by running config-yaml command):

```
% cat ./vsphere_check.yaml#endpoint: test.endpoint.local     # The vSphere endpoint#username: *****                   # The vSphere username#password: *****                   # The vSphere password#storage_class: test-storage-class # vSphere CSI provisioner storage class name#volume_size: 100                  # Size of a vSphere volume (in mebibytes) to be created during the test
```

The output below is an example of running vSphere CSI checker:

```
% ./k10tools primer storage check vsphere -f ./vsphere_check.yamlUsing "./vsphere_check.yaml" file content as config source-> Setup Provider-> Create Namespace-> Create Volume-> Create Test Pod-> Write Data-> Create Snapshot-> Delete Test Pod-> Delete Volume   - Delete PVC 'primer-test-vsphere-pvc-b825l'-> Restore Volume   - Restore vSphere FCD   - Restore PV   - Restore PVC-> Restore Test Pod-> Verify Data-> Delete Test Pod-> Delete Snapshot-> Delete Volume   - Delete PVC 'primer-test-vsphere-pvc-9blfz'-> Delete NamespaceVSphere backup/restore checker:  Created storage provider  -  OK  Created namespace 'primer-test-ns-fwgfl'  -  OK  Created PVC 'primer-test-vsphere-pvc-b825l'  -  OK  Created test pod 'primer-test-pod-2frfw'  -  OK  Wrote data '2022-12-08 18:36:21.252404 +0400 +04 m=+29.712849501' to pod 'primer-test-pod-2frfw'  -  OK  Created snapshot '50cf961e-3e87-4cc0-8031-a09b6c6b6a2e:127c586c-5251-4a3d-976c-d728cd370926' for FCD '50cf961e-3e87-4cc0-8031-a09b6c6b6a2e' (PV 'pvc-ab60f6a8-d1b6-4861-9c95-b7404e1c1ea5')  -  OK  Deleted test pod 'primer-test-pod-2frfw'  -  OK  Deleted PVC 'primer-test-vsphere-pvc-b825l', PV 'pvc-ab60f6a8-d1b6-4861-9c95-b7404e1c1ea5' and FCD '50cf961e-3e87-4cc0-8031-a09b6c6b6a2e'  -  OK  Restored FCD '253cebc3-80cb-470c-90a8-e9e80a4f2188', PV 'primer-test-vsphere-pv-lqvmw' and PVC 'primer-test-vsphere-pvc-9blfz' from snapshot '50cf961e-3e87-4cc0-8031-a09b6c6b6a2e:127c586c-5251-4a3d-976c-d728cd370926'  -  OK  Created test pod 'primer-test-pod-5lk26'  -  OK  Verified restored data  -  OK  Deleted test pod 'primer-test-pod-5lk26'  -  OK  Deleted snapshot '50cf961e-3e87-4cc0-8031-a09b6c6b6a2e:127c586c-5251-4a3d-976c-d728cd370926'  -  OK  Deleted PVC 'primer-test-vsphere-pvc-9blfz', PV 'primer-test-vsphere-pv-lqvmw' and FCD '253cebc3-80cb-470c-90a8-e9e80a4f2188'  -  OK  Deleted namespace 'primer-test-ns-fwgfl'  -  OK
```

## Veeam Kasten Primer Block Mount Check â

The k10tools primer storage check blockmount sub-command is provided
  to test if the PersistentVolumes provisioned by a StorageClass can be
  supported in block mode by Veeam Kasten. If a StorageClass passes this test then see Block Mode Exports for how to indicate this fact to Veeam Kasten.

The checker performs two tests:

1. The kubestr block mount test is used to verify that the StorageClass volumes can be used with Block VolumeMounts.
2. If first test succeeds, then a second test is run to verify that Veeam Kasten can restore block data to such volumes. This step is performed only if Veeam Kasten does not use provisioner specific direct network APIs to restore data to a block volume during import.

Both tests independently allocate and release the Kubernetes resources
  they need, and it takes a few minutes for the test to complete.

The checker can be invoked by the k10primer.sh script in a manner
  similar to that described in the Pre-flight Checks :

```
% curl https://docs.kasten.io/downloads/8.0.3/tools/k10_primer.sh | bash /dev/stdin blockmount -s ${STORAGE_CLASS_NAME}
```

Alternatively, for more control over the invocation of the checker, use
  a local copy of the k10tools program to obtain a YAML configuration
  file as follows:

```
% ./k10tools primer storage check blockmount config-yaml## Storage class name (string)storage_class: <storage class being tested>## PVC size (Kubernetes Quantity string format)pvc_size: 1Gi## The user identifier for pods. (int64)run_as_user: 1000## Cleanup only (bool)cleanup_only: false## Mount test timeout seconds (uint32)mount_test_timeout_seconds: 60## Import test timeout seconds (uint32)import_test_timeout_seconds: 300## Disable the invocation of the kubestr blockmount test (bool)disable_mount_test: false## Disable the invocation of the import validation test (bool)disable_import_test: false
```

The YAML output should be saved to a file and edited to set the desired
  StorageClass. Only the storage_class property is required; other
  properties will default to the values displayed in the output if not
  explicitly set.

Then run the checker as follows:

```
% ./k10tools primer storage check blockmount -f ./blockmount.yaml
```

The test emits multiple messages as it progresses. On success, you will
  see a summary message like this at the end:

```
Block mount checker:StorageClass standard-rwo supports Block volume modeStorageClass standard-rwo is supported by K10 in Block volume mode
```

On failure, the summary message would look like this:

```
Block mount checker:StorageClass efs-sc does not support Block volume mode: had issues creating Pod: 0/4 nodes are available: 4 pod has unbound immediate PersistentVolumeClaims.  -  Error
```

The checker may produce spurious errors if the StorageClass specifies
  the Immediate VolumeBindingMode and the PersistentVolumes provisioned
  by the test have different node affinities. In such a case use a variant
  of the StorageClass that specifies the WaitForFirstConsumer VolumeBindingMode instead.

Use the -h flag to get all command usage options.

## Veeam Kasten Primer for Authentication Service Checks â

Run k10tools primer auth check --help command to observe all supported
    sub-commands.

The k10tools primer auth check sub-command family allows doing basic
  sanity checks for 3rd-party authentication services. Currently it
  supports checkers for ActiveDirectory/LDAP and OIDC.

Each service specific command accepts required parameters via a
  configuration file, format of which can be observed by running config-yaml sub-command (example is for OIDC checker):

```
% ./k10tools primer auth check oidc config-yaml## OIDC provider URL#provider_url: <provider_url> # Example: https://accounts.google.com
```

The output below is an example of running OIDC checker:

```
% ./k10tools primer auth check oidc -f ./oidc_check.yamlUsing "./oidc_check.yaml" file content as config sourceChecking the OIDC provider: https://accounts.google.comOIDC Provider Checker:  Successfully connected to the OIDC provider  -  OK
```

## Generic Volume Snapshot Capabilities Check â

The k10tools primer gvs-cluster-check command can be used to check if
  the cluster is compatible for Veeam Kasten Generic Volume Snapshot.
  Veeam Kasten Generic backup commands are executed on a pod running kanister-tools image and checked for appropriate output.

Use -n flag to provide namespace. By default, kasten-io namespace
  will be used.

Use -s flag to provide a storageclass for the checks to be run
  against. By default, no storage class will be used and the checks will
  be done using temporary storage from the node the pod runs on.

Use --service-account flag to specify the service account to be used
  by pods during GVS checks. By default, default service account will be
  used.

By default, the k10tools command will use the publicly available
    kanister-tools image at gcr.io/kasten-images/kanister-tools:<K10 version> . Since this image is
    not available in air-gapped environments, to override the default image,
    set the KANISTER_TOOLS environment variable to the kanister-tools
    image that is available in the air-gapped environment's local registry.

Example:

: export KANISTER_TOOLS=<your local registry>/<your local
    repository name>/kanister-tools:k10-<K10 version>

```
% ./k10tools primer gvs-cluster-check  Validate Generic Volume Snapshot:    Pod Created successfully  -  OK    GVS Backup command executed successfully  -  OK    Pod deleted successfully  -  OK
```

## Veeam Kasten Generic Storage Backup Sidecar Injection â

The k10tools k10genericbackup can be used to make Kubernetes workloads
  compatible for K10 Generic Storage Backup by injecting a Kanister
  sidecar and setting the [forcegenericbackup=true] annotation
  on the workloads.

```
### Usage ##% ./k10tools k10genericbackup --helpk10genericbackup makes Kubernetes workloads compatible for K10 Generic Storage Backup byinjecting a Kanister sidecar and setting the forcegenericbackup=true annotation on the workloads.To know more about K10 Generic Storage Backup, visit https://docs.kasten.io/latest/install/generic.htmlUsage:  k10tools k10genericbackup [command]Available Commands:  inject      Inject Kanister sidecar to workloads to enable K10 Generic Storage Backup  uninject    Uninject Kanister sidecar from workloads to disable K10 Generic Storage BackupFlags:      --all-namespaces         resources in all the namespaces  -h, --help                   help for k10genericbackup      --k10-namespace string   namespace where K10 services are deployed (default "kasten-io")  -n, --namespace string       namespace (default "default")Global Flags:  -o, --output string   Options(json)Use "k10tools k10genericbackup [command] --help" for more information about a command.### Example: Inject a Kanister sidecar to all the workloads in postgres namespace ##% ./k10tools k10genericbackup inject all -n postgresInject deployment:Inject statefulset:  Injecting sidecar to statefulset postgres/mysql  Updating statefulset postgres/mysql  Waiting for statefulset postgres/mysql to be ready  Sidecar injection successful on statefulset postgres/mysql!  -  OK  Injecting sidecar to statefulset postgres/postgres-postgresql  Updating statefulset postgres/postgres-postgresql  Waiting for statefulset postgres/postgres-postgresql to be ready  Sidecar injection successful on statefulset postgres/postgres-postgresql!  -  OKInject deploymentconfig:  Skipping. Env is not compatible for Kanister sidecar injection
```

## CA Certificate Check â

The k10tools debug ca-certificate command can be used to check if the
  CA certificate is installed properly in Veeam Kasten. The -n flag can
  be used to provide namespace and it defaults to kasten-io . More
  information on installation process.

Replace <custom-bundle-file> with the desired filename

```
% ./k10tools ca-certificate -k <custom-bundle-file>.pem  CA Certificate Checker:    Fetching configmap which contains CA Certificate information : custom-ca-bundle-store    Certificate exists in configmap  -  OK    Found container : aggregatedapis-svc to extract certificate    Certificate exists in container at /etc/ssl/certs/<custom-bundle-file>.pem    Certificates matched successfully  -  OK
```

## Installation of Veeam Kasten in OpenShift clusters â

The k10tools openshift prepare-install command can be used to prepare
  an OpenShift cluster for installation of Veeam Kasten. It extracts a CA
  Certificate from the cluster, installs it in the namespace where Veeam
  Kasten will be installed, and generates the helm command to be used for
  installing Veeam Kasten. The -n flag can be used to provide the
  namespace where Veeam Kasten will be installed. The default namespace is kasten-io . --recreate-resources flag recreates resources that may
  have been created by previous execution of this command. Set --insecure-ca flag to true if Certificate Issuing Authority is not
  trusted.

```
% ./k10tools openshift prepare-installOpenshift Prepare Install:  Certificate found in Namespace 'openshift-ingress-operator' in secret 'router-ca'  -  OK  Checking if namespace 'kasten-io' exists  Namespace 'kasten-io' exists  -  OK  Created configmap 'custom-ca-bundle-store' with custom certificate in it  -  OK  Searching for Apps Base Domain Name in Ingress Controller  Found Apps Base Domain 'apps.test.aws.kasten.io'  -  OK  Created Service Account 'k10-dex-sa' successfully  -  OKPlease use below helm command to start K10 installation-------------------------------------------------------------------- helm repo add kasten https://charts.kasten.io/ helm install k10 kasten/k10 --namespace=kasten-io \ --set scc.create=true \ --set route.enabled=true \ --set route.tls.enabled=true \ --set auth.openshift.enabled=true \ --set auth.openshift.serviceAccount=k10-dex-sa \ --set auth.openshift.clientSecret=<your key will be here automatically>\ --set auth.openshift.dashboardURL=https://k10-route-kasten-io.apps.test.aws.kasten.io/k10/ \ --set auth.openshift.openshiftURL=https://api.test.aws.kasten.io:6443 \ --set auth.openshift.insecureCA=false \ --set cacertconfigmap.name=custom-ca-bundle-store \ --set cacertconfigmap.key=custom-ca-bundle.pem
```

## Extracting OpenShift CA Certificates â

The k10tools openshift extract-certificates command is used to extract
  CA certificates from OpenShift clusters to the Veeam Kasten namespace.
  The following flags can be used to configure the command:

- --ca-cert-configmap-name . The name of the Kubernetes ConfigMap that contains all certificates required for Veeam Kasten. If no name is provided, the default name custom-ca-bundle-store will be used. If the ConfigMap with the used name does not exist, the command will generate a new ConfigMap. If the ConfigMap with the used name exists, the command will merge newly extracted certificates with the existing certificates in the ConfigMap without creating duplicates.
- --ca-cert-configmap-key . The key of the Kubernetes ConfigMap that contains certificates required for Veeam Kasten. If no key is provided, the default key custom-ca-bundle.pem will be used.
- --k10-namespace or -n . The Kubernetes namespace where Veeam Kasten is expected to be installed. The default value is kasten-io .
- --release-name . The K10 Release Name. The default value is k10 .

- If the ConfigMap with the used name does not exist, the command will generate a new ConfigMap.
- If the ConfigMap with the used name exists, the command will merge newly extracted certificates with the existing certificates in the ConfigMap without creating duplicates.

```
% ./k10tools openshift extract-certificates% kubectl get configmap custom-ca-bundle-store -n kasten-ioNAME                     DATA   AGEcustom-ca-bundle-store   1      46s
```

## Listing vSphere snapshots created by Veeam Kasten â

Veeam Kasten integrates with the vSphere clusters using direct
  integration. Veeam Kasten snapshots can be listed using k10tools .

```
export VSPHERE_ENDPOINT=<url of ESXi or vCenter instance to connect to>export VSPHERE_USERNAME=<vSphere username>export VSPHERE_PASSWORD=<vSphere password>k10tools provider-snapshots list -t FCD
```

Only snapshots created starting with version 5.0.7 will be listed by the
    current version of the tool. Earlier snapshots might be listed if they
    had been created using a vSphere infrastructure profile with the tagging
    option enabled (Deprecated since then). To list earlier snapshots,
    k10tools v6.5.0 should be used with an additional environment variable:

# category name can be found from the vSphere infrastructure profile,
    in the form of "k10:<UUID>"

export VSPHERE_SNAPSHOT_TAGGING_CATEGORY=$(kubectl -n kasten-io get profiles $(kubectl -n kasten-io get profiles -o=jsonpath='{.items[?(@.spec.infra.type=="VSphere")].metadata.name}') -o jsonpath='{.spec.infra.vsphere.categoryName}')

---

## Operating Monitoring

Veeam Kasten enables centralized monitoring of all its activity by
  integrating with Prometheus. In particular, it exposes a Prometheus
  endpoint from which a central system can extract data.

A Grafana instance can be installed in the same Kubernetes cluster
  where Veeam Kasten is installed to query and visualize the metrics
  from Veeam Kasten's prometheus instance. Steps to install a new Grafana
  instance and integrating that with Veeam Kasten's prometheus instance
  are documented here .

This section documents how to install and enable Prometheus,
  usage of the metrics currently exposed, generation of alerts and reports
  based on these metrics, and integration with external tools.

## Using Veeam Kasten's Prometheus Endpoint â

By default, Prometheus is configured with persistent storage size 8Gi
  and retention period of 30d. That can be changed with --set prometheus.server.persistentVolume.size=<size> and --set prometheus.server.retention=<days> .

Prometheus requires Kubernetes API access to discover Veeam Kasten pods
  to scrape their metrics. Thus, by default Role and RoleBinding entries are created in Veeam Kasten namespace. However, if you set prometheus.rbac.create=true , global ClusterRole and ClusterRoleBinding will be created instead.

The complete list of configurable parameters can be found at Advanced Install Options .

If for some reason you don't want helm to create RBAC for you
  automatically and you have both rbac.create=false and prometheus.rbac.create=false , you can create Role and RoleBinding manually:

```
kind: RoleapiVersion: rbac.authorization.k8s.io/v1metadata:  name: k10-prometheus-server  namespace: kasten-iorules:- apiGroups:  - ""  resources:  - nodes  - nodes/proxy  - nodes/metrics  - services  - endpoints  - pods  - ingresses  - configmaps  verbs:  - get  - list  - watch- apiGroups:  - extensions  - networking.k8s.io  resources:  - ingresses/status  - ingresses  verbs:  - get  - list  - watch---kind: RoleBindingapiVersion: rbac.authorization.k8s.io/v1metadata:  name: k10-prometheus-server  namespace: kasten-ioroleRef:  apiGroup: rbac.authorization.k8s.io  kind: Role  name:  k10-prometheus-serversubjects:  - kind: ServiceAccount    name: prometheus-server    namespace: kasten-io
```

An external Prometheus server can be configured to scrape Veeam
  Kasten's built-in server. The following scrape config is an example of
  how a Prometheus server hosted in the same cluster might be configured:

```
- job_name: k10  scrape_interval: 15s  honor_labels: true  scheme: http  metrics_path: '/<k10-release-name>/prometheus/federate'  params:    'match[]':      - '{__name__=~"jobs.*"}'  static_configs:    - targets:      - 'prometheus-server.kasten-io.svc.cluster.local'      labels:        app: "k10"
```

An additional NetworkPolicy may need to be applied in certain
    environments.

Although it's possible to disable Veeam Kasten's built-in Prometheus
  server enabled, it is recommended to leave it enabled. Disabling the
  server reduces functionality in various parts of the system such as
  usage data, reporting, and the multi-cluster dashboard. To disable the
  built-in server, set the prometheus.server.enabled value to false .

If the built-in server has previously been disabled, it can be
  re-enabled during a helm upgrade (see Upgrading Veeam Kasten ) with: --set prometheus.server.enabled=true .

## Veeam Kasten Metrics â

When using Veeam Kasten Multi-Cluster Manager (i.e., a
    cluster setup as a primary), to query metrics for the primary cluster
    from its Prometheus instance a cluster label with a blank value ( "" )
    is required.

### Veeam Kasten Action Metrics â

When Veeam Kasten performs various actions throughout the system, it
  collects metrics associated with these actions. It records counts for
  both cluster and application-specific actions.

These action metrics include labels that describe the context of the
  action. For actions specific to an application, the application name is
  included as app . For actions initiated by a policy, the policy name is
  included as policy . For ended actions, the final status is included as state (i.e., succeeded , failed , or cancelled ).

Separate metrics are collected for the number of times the action was
  started, ended, or skipped. This is indicated by the suffix of the
  metric (i.e., _started_count , _ended_count , or _skipped_count ).

An overall set of metrics is also collected that does not include the app or policy labels. These metrics end with _overall rather than _count . It is recommended to use the overall metrics unless specific
  application or policy information is required.

Metrics are collected for the following actions:

- backup and backup_cluster
- restore and restore_cluster
- export
- import
- report
- run

For example, to query the number of successful backups in the past 24
  hours:

```
sum(round(increase(action_backup_ended_overall{state="succeeded"}[24h])))
```

Or, to query the number of failed restores for the past hour:

```
sum(round(increase(action_restore_ended_overall{state="failed"}[1h])))
```

When querying metrics that are reported as counters, such as action
    metrics, the increase or rate functions must be used. See Prometheus query
functions for more information.

#### Examples of Action Metrics â

action_export_processed_bytes The overall bytes processed during the
  export. Labels: policy , app action_export_transferred_bytes The
  overall bytes transferred during the export. Labels: policy , app

See the Prometheus
docs for
  more information on how to query data from Prometheus.

### Veeam Kasten Artifact Metrics â

You can monitor both the rate of artifact creation and the current count
  within Veeam Kasten. Similar to the action counts mentioned above, there
  are also the following metrics, which track the number of artifacts
  backed up by Veeam Kasten within a defined time frame:

- action_artifact_count
- action_artifact_count_by_app
- action_artifact_count_by_policy

To see the number of artifacts protected by snapshots currently you can
  use the following metrics.

- artifact_sum
- artifact_sum_by_app
- artifact_sum_by_policy

If an artifact is protected by multiple snapshots then it will be
  counted multiple times.

### Veeam Kasten Compliance Metrics â

To track the number of applications that fall outside of compliance, you
  can use the compliance_count metric, which includes the following
  states of interest: [NotCompliant, Unmanaged] . If the cluster contains
  pre-existing namespaces, which are not subject to compliance concerns,
  you have the option to use the Helm flag excludedApps to exclude them.
  This action will remove both the application(s) from the dashboard and
  exclude them from the compliance_count . You can set this exclusion
  using the inline array ( excludedApps: ["app1", "app2"] ) or the
  multi-line array, specifying the applications to be excluded:

```
excludedApps:  - app1  - app2
```

If you prefer to set Helm values inline rather than through a YAML file,
  you can do this with the following:

```
--set excludedApps[0]="app1"--set excludedApps[1]="app2"
```

See the knowledge base article for more
  information.

### Veeam Kasten Execution Metrics â

#### Aggregating Job and Phase Runner Metrics â

Designed especially for measuring the parallelism usage:

| Name | Type | Description | Labels | exec_active_job_count | gauge | Number of active jobs at a time | *action- Action name (e.g.manualSnapshot,retire) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| exec_active_job_count | gauge | Number of active jobs at a time | *action- Action name (e.g.manualSnapshot,retire) |
| exec_started_job_count_total | counter | Total number of started jobs per executor instance | *action- Action name (e.g.manualSnapshot,retire) |
| exec_active_phase_count | gauge | Number of active phases for a given action and with a given name per executor instance | *action- Action name (e.g.manualSnapshot,retire)*phase- Phase name (e.g.copySnapshots,reportMetrics) |
| exec_started_phase_count_total | counter | Total number of started phases for a given action and with a given name per executor instance | *action- Action name (e.g.manualSnapshot,retire)*phase- Phase name (e.g.copySnapshots,reportMetrics) |
| exec_phase_error_count_total | counter | Total number of errors for a given action and phase per executor instance | *action- Action name (e.g.manualSnapshot,retire)*phase- Phase name (e.g.copySnapshots,reportMetrics) |

#### Rate Limiter Metrics â

These metrics might be useful for monitoring current pressure:

| Name | Type | Description | Labels | limiter_inflight_count | gauge | Number of in-flight operations | *operation- Operation name (e.g.csiSnapshot,genericCopy) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| limiter_inflight_count | gauge | Number of in-flight operations | *operation- Operation name (e.g.csiSnapshot,genericCopy) |
| limiter_pending_count | gauge | Number of pending operations | *operation- Operation name (e.g.csiSnapshot,genericCopy) |
| limiter_request_seconds | histogram | Duration in seconds of:* how long operation wait for the token (labelstage=wait)* how long operation hold the token (labelstage=hold) | *operation- Operation name (e.g.csiSnapshot,genericCopy)*stage- This label indicates the essence of the metric. Can bewaitorhold. See description for more details |

#### Jobs Metrics â

These metrics measure the time range between the creation of the job and
  its completion:

| Name | Type | Description | Labels | jobs_completed | gauge | Number of finished jobs (the job is considered to be finished if it has failed, skipped, or succeeded status) | *status- Status name (e.g.succeeded,failed) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| jobs_completed | gauge | Number of finished jobs (the job is considered to be finished if it has failed, skipped, or succeeded status) | *status- Status name (e.g.succeeded,failed) |
| jobs_duration | histogram | Duration in seconds of completed Veeam Kasten jobs. | *status- Status name (e.g.succeeded,failed)*policy_id- Policy ID (e.g.264aae0e-07ac-4aa5-a38f-aa131c053cbe,UNKNOWN) |

The jobs_duration metric is the easiest one for monitoring job status
  because it is already aggregated. This metric captures the running time
  of jobs that have completed, whether they succeed or fail.

### Veeam Kasten License Status â

Veeam Kasten exports the metering_license_compliance_status metric
  related to the cluster's license compliance. This metric contains
  information on when the cluster was out of license compliance.

The metering_license_compliance_status metric is a Prometheus gauge ,
  and has a value of 1 if the cluster's license status is compliant and 0
  otherwise. To see the timeline of when Veeam Kasten was out of license
  compliance, the metering_license_compliance_status metric can be
  queried and graphed.

It is possible to see the peak node usage for
  the last two months e.g. by querying node_usage_history{timePeriod="202210"} . The label format is YYYYMM .

### Veeam Kasten Status Metrics â

The state of profiles and policies can be monitored with profiles_count and policies_count respectively.

profiles_count{type="Location", status="Failed"} reporting a value
  greater than 0 would be grounds for further investigation as it would
  create issues for any related policies. type="Infra" is also available
  for Infrastructure profiles.

policies_count{action="backup", chained="export", status="Failed"} reports on policies involving both a backup and export that are in a
  failed state.

### Veeam Kasten Storage Metrics â

To check exported storage consumption (Object, NFS/SMB or Veeam Backup &
  Replication) there is export_storage_size_bytes with types [logical, physical] , e.g. export_storage_size_bytes{type="logical"} .
  The deduplication ratio is calculated by logical / physical .

snapshot_storage_size_bytes , also with logical and physical types,
  reports the local backup space utilization.

### Data Transfer Metrics â

Metrics are collected for individual snapshot upload and download
  operation steps within Veeam Kasten export and import actions<k10_action_metrics> . These metrics differ from those collected for Veeam Kasten
  actions because they are captured on a per-volume basis, whereas Veeam
  Kasten actions, in general, could involve multiple volume operations and
  other activities.

The following data operations metrics are recorded:

| Metric Name | Type | Description | data_operation_duration | Histogram | This metric captures the total time taken to complete an operation. |
| :---: | :---: | :---: | :---: | :---: | :---: |
| data_operation_duration | Histogram | This metric captures the total time taken to complete an operation. |
| data_operation_normalized_duration | Histogram | This metric captures thenormalized timetaken by an operation. The value is expressed in time/MiB. Normalized duration values allow comparisons between different time series, which is not possible for duration metric values due to the dependency on the amount of data transferred. |
| data_operation_bytes | Counter | This metric counts the bytes transferred by an operation, and is typically used to compute the data transfer rate. Note: This metric is not collected for Download operations involving the Filesystemexport mechanism. |
| data_operation_volume_count | Gauge | This metric counts the number of volumes involved in an operation. It is set to 1 at the beginning of an operation and changes to 0 upon completion. When aggregated, it displays the total number of volumes being transferred over time. |

The following labels are applied to the operation metrics:

| Label Name | Description | operation | The type of operation: one of Upload or Download |
| :---: | :---: | :---: | :---: |
| operation | The type of operation: one of Upload or Download |
| repo_type | The type ofLocationProfileobject that identifies the storage repository: one of ObjectStore, FileStore or VBR. |
| repo_name | The name of theLocationProfileobject that identifies the storage repository. |
| data_format | Theexport mechanismused: one of Filesystem or Block. |
| namespace | The namespace of the application involved. |
| pvc_name | The name of the PVC involved. |
| storage_class | The storage class of the PVC involved. |

Upload operation metrics do not include the time taken to
  snapshot the volumes or the time to upload the action's metadata.
  However, they do include the time taken to instantiate a
  PersistentVolume from a snapshot when needed. Similarly, Download operation metrics do not involve the allocation
  of the PersistentVolume or the node affinity enforcement steps.

Some query examples:

```
## average duration over 2-minute intervalssum by (data_format,operation,namespace,pvc_name) (rate(data_operation_duration_sum{}[2m]))/ sum by (data_format,operation,namespace,pvc_name) (rate(data_operation_duration_count{}[2m]))## average transfer rate over 2-minute intervalsavg by (data_format, operation, storage_class, repo_name) (rate(data_operation_bytes{}[2m]))## count of data transfer operations over 2-minute intervalssum (max_over_time(data_operation_volume_count{}[2m]))
```

When a Veeam Backup Repository is involved, additional metrics are recorded:

| Metric Name | Type | Description | data_upload_session_duration | Histogram | This metric captures the total time taken for an upload session. |
| :---: | :---: | :---: | :---: | :---: | :---: |
| data_upload_session_duration | Histogram | This metric captures the total time taken for an upload session. |
| data_upload_session_volume_count | Gauge | This metric counts the number of volumes in an upload session. When aggregated, it shows the total number of volumes across all upload sessions over time. |

The following labels are applied to the upload session metrics:

| Label Name | Description | repo_type | The type ofLocationProfileobject that identifies the storage repository: VBR. |
| :---: | :---: | :---: | :---: |
| repo_type | The type ofLocationProfileobject that identifies the storage repository: VBR. |
| repo_name | The name of theLocationProfileobject that identifies the storage repository. |
| namespace | The namespace of the application involved. |

A query example:

```
## count of volumes involved in VBR upload sessions over 2-minute intervalssum (max_over_time(data_upload_session_volume_count{repo_type="VBR"}[2m]))
```

## Veeam Kasten Multi-Cluster Metrics â

The Multi-Cluster primary instance exports the following metrics
  collected from all clusters within the multi-cluster system.

Use the cluster label with cluster name as the value to query metrics
  for an individual cluster.

For example, to query the number of successful actions in the past 24
  hours:

```
sum(round(increase(mc_action_ended_count{state="succeeded",cluster="<cluster-name>"}[24h])))
```

### Policy Metrics â

| Name | Type | Description | Labels | mc_policies_count | gauge | Number of policies in cluster | *cluster- Cluster name |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| mc_policies_count | gauge | Number of policies in cluster | *cluster- Cluster name |
| mc_compliance_count | gauge | Number of namespaces by compliance state. SeeVeeam Kasten Compliance Metricsabout exclusions | *cluster- Cluster name*state- Compliance state (e.g.Compliant,NotCompliant,Unmanaged) |

### Action Metrics â

| Name | Type | Description | Labels | mc_action_ended_count | counter | Number of actions that have ended | *cluster- Cluster name*state- Terminal state (e.g.cancelled,failed,succeeded) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| mc_action_ended_count | counter | Number of actions that have ended | *cluster- Cluster name*state- Terminal state (e.g.cancelled,failed,succeeded) |
| mc_action_skipped_count | counter | Number of actions that were skipped | *cluster- Cluster name |

### Storage Metrics â

| Name | Type | Description | Labels | mc_export_storage_physical_size_bytes | gauge | Exported storage consumption in bytes | *cluster- Cluster name |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| mc_export_storage_physical_size_bytes | gauge | Exported storage consumption in bytes | *cluster- Cluster name |
| mc_snapshot_storage_physical_size_bytes | gauge | Local backup space utilization in bytes | *cluster- Cluster name |

## Using Externally Installed Grafana â

This document can be followed to install a separate instance of Grafana and
  setup Veeam Kasten Grafana dashboard, alerts into that.

### Configuring Grafana's URL â

Once a separate instance of Grafana is installed on the Cluster, its URL can be
  configured, using the Helm field below, while installing Veeam Kasten to make
  it easier to access Grafana from Veeam Kasten's dashboard.

```
--set grafana.external.url=<grafan-url>
```

### Accessing Grafana from Veeam Kasten's dashboard â

Click on the "Data Usage" card on Veeam Kasten's dashboard.

Click on "More Charts and Alerts" to access the instance of Grafana
  installed with Veeam Kasten.

### Charts and Graphs â

The Grafana dashboard can be used to monitor how many application scoped
  or cluster scoped actions (backup, restore, export and import) have
  completed, failed or been skipped.

It shows the number of policy runs that have completed or been skipped.

The amount of disk space consumed and the percentage of free space
  available in Veeam Kasten's stateful services (catalog, jobs, and
  logging) are also shown.

The Data reduction section provides graphs which show the amount of data
  being transferred (e.g, when the new volume has been exported it will be
  close to 100%, as all data needs to be transferred, but with an
  unchanged volume it will be 0% since most of the data has already been
  exported):

The Veeam Kasten System Resource Usage section provides CPU/Memory usage
  graphs specific to Veeam Kasten and metrics that describe task execution
  performance:

The Data transfer operations section provides graphs on the transfer of
  data to and from storage repositories that are captured by the data transfer metrics described above.

The column on the left is organized by storage class, location profile,
  and the export mechanism used. The upper panel displays the normalized duration of
  transfer operations, while the lower panel shows the data transfer rate.
  (The normalized duration expresses the time taken to transfer one MiB of
  data, and hence is comparable between the different time series
  displayed in the panel).

The column on the right is organized by individual PVC and data format
  used, with the upper panel showing the actual duration of individual
  operations and the lower panel showing the transfer rate.

All panels have an overlay that displays the number of volume operations
  in progress. In addition, if VBR is used, the number of volumes involved
  in VBR upload sessions will be shown in a shaded area.

### Grafana Alerts â

Grafana can be used to create alerts to get notified moments after
  something unexpected happens in your system. An alert can be generated
  by specifying a condition or evaluation criteria and, these conditions
  can be configured using Alert rules. Each rule uses a query that fetches
  data from a data source. Each query involves a metric such as the Veeam
  Kasten metrics described in a previous section. More can be read about
  this by following the Grafana Alerting
documentation .

There are three main constructs that are involved while creating alerts
  in Grafana:

### Alert rules â

The condition on which the alerts should be fired can be configured
  using alert rules.

A new alert rule can be created by going to the dashboard's edit option
  and then clicking on the Alert tab at the bottom of the page. In this
  example, it's assumed that a dashboard panel named Dashboard Local is
  already created.

Once there, the Create alert rule from this panel button can be used
  to set the query and alert condition for this alert rule. Configure the
  datasource that should be used in this alert and the metric that should
  be queried.

In this example, datasource Prometheus and metric action_backup_ended_overall were used.

After setting the query and alert condition, the label of this alert
  rule can be configured by scrolling down the same page, until Notifications options.

Labels are useful to configure where these alerts are going to be sent.

In this example, the labels team:operations and resource:backup have
  been used.

Click on Save and Exit to save the dashboard with this alert rule and
  exit.

### Contact Points â

Contact points are used to configure the communication medium for the
  alerts that are going to be generated. For example, in some scenarios,
  it might be useful to get a slack message as soon as an alert is fired.
  In that case, slack must be configured as a contact point. To see a list
  of all the contact point types, refer to this Grafana
documentation .

A contact point can be configured by going to the Alerting dashboard and
  then clicking on New contact point under the Contact points tab. In
  the example below, slack has been chosen as the contact point type.

### Notification Policies â

Once the alerts rule and contact points have been configured, the
  relationship between these two configurations is established by creating
  a Notification policy.

A notification policy can be configured by going to the Alerting
  dashboard and then clicking on New specific policy under the Notification policies tab.

The example below uses the same labels specified while creating the
  alert rule in the previous step.

When an alert is generated based on the rule configured, notifications
  will be sent to the slack channel.

## Integrating External Prometheus with Veeam Kasten â

To integrate external Prometheus with Veeam Kasten, set the flags global.prometheus.external.host and global.prometheus.external.port .
  If external Prometheus is setup with a base URL, set the global.prometheus.external.baseURL flag. Make sure RBAC was enabled
  while setting up external Prometheus to enable target discovery.

It's also possible to disable kasten built-in prometheus by setting the
  flag prometheus.server.enabled: false

### Scrape Config â

Update the Prometheus scrape configuration by adding two additional
  targets.

```
- job_name: httpServiceDiscovery  http_sd_configs:    - url: http://metering-svc.kasten-io.svc.cluster.local:8000/v0/listScrapeTargets- job_name: k10-pods  scheme: http  metrics_path: /metrics  kubernetes_sd_configs:    - role: pod      namespaces:        own_namespace: true      selectors:        - role: pod          label: "component=executor"  relabel_configs:    - action: labelmap      regex: __meta_kubernetes_pod_label_(.+)    - source_labels: ___meta_kubernetes_pod_container_port_number_      action: keep      regex: 8\d{3}
```

It is possible to obtain those targets from Veeam Kasten's Prometheus'
  configuration, if Prometheus was installed with Veeam Kasten, you should
  skip job :prometheus . (Note. yq utility is needed to execute commands successfully)

```
## Get prometheus jobkubectl get cm k10-k10-prometheus-config -n kasten-io -o "jsonpath={.data['prometheus\.yml']}" | yq '.scrape_configs'## Update prometheus configmap with given output.
```

The targets will show up after adding the scrape config. Note that the
  targets will not be scraped until a network policy is added.

### Network Policy â

Once the scrape config is in place, the targets will be discovered but
  Prometheus won't be able to scrape them as Veeam Kasten has strict
  network policies for inter-service communication. To enable
  communication between external Prometheus and Veeam Kasten, a new
  network policy should be added as follows.

Add a label to the namespace where external Prometheus is installed
  - kubectl label namespace/prometheus app=prometheus and apply the
  following network policy to enable communication.

```
apiVersion: networking.k8s.io/v1kind: NetworkPolicymetadata:  labels:    app: k10    heritage: Helm    release: k10  name: allow-external-prometheusspec:  ingress:    - from:        - namespaceSelector:            matchLabels:              app: prometheus  podSelector:    matchLabels:      release: k10
```

Once the network policy enables communication, all the service targets
  will start coming up and the metrics will be scraped.

## Generating Reports â

Veeam Kasten Reporting provides regular insights into key performance
  and operational states of the system. It uses prometheus to obtain
  information about action runs and storage consumption. For more
  information about Veeam Kasten Reporting, see Reporting

## Integration with External Tools â

Exporting Metrics to Datadog

---

## Operating Reporting

Veeam Kasten Reporting provides regular insights into key performance
  and operational states of the system. When reporting is enabled, Veeam
  Kasten periodically collects information from the system and compiles it
  into a report. Generated reports include information such as license
  status, actions run, configured policies and profiles, compliance
  information, and service information.

## Enabling Veeam Kasten Reports â

Under Usage and Reports menu in the navigation sidebar, select Reports and then select Enable Reports .

When enabled, a policy is created to manage the generation of reports.
  Reports are generated according to the policy and then stored in the
  cluster. The policy is also be visible on the policies page.

## Viewing Generated Reports â

A generated report contains information about the state of the system at
  the time the report was generated as well as select metrics collected
  from the Veeam Kasten Prometheus service.

If some of the information is unavailable at the time the report is
    generated, it is omitted from the report. For example, if the Veeam
    Kasten Prometheus service is disabled or otherwise unavailable,
    metrics are omitted from the report.

### Viewing Reports With The Dashboard â

Recent reports can be viewed on the Usage & Reports page. The full
  details of a given report can be viewed by clicking on a report in the
  list.

### Viewing Reports With kubectl â

Reports can be listed and viewed using kubectl .

```
$ kubectl get -n kasten-io reports.reporting.kio.kasten.ioNAME                    LICENSE   DR         TIME                   AGEscheduled-45cfn-qwmcw   Valid     Disabled   2021-10-06T22:58:54Z   24hscheduled-568xd-s2qgh   Valid     Disabled   2021-10-07T22:57:49Z   16m
```

By default, kubectl get doesn't sort results, they're displayed in
    the same order they're received from the API server. This means
    reports may not be listed in the order they were generated.

The --sort-by=.spec.reportTimestamp option can be added to ensure
    the most recent reports are listed last.

An individual report can also be shown using the -o yaml option for kubectl get :

```
$ kubectl get -n kasten-io -o yaml reports.reporting.kio.kasten.io scheduled-568xd-s2qghapiVersion: reporting.kio.kasten.io/v1alpha1kind: Reportmetadata:  name: scheduled-568xd-s2qgh  namespace: kasten-ioresults:  ## â¦spec:  reportTimestamp: "2021-10-06T22:40:54Z"  statsIntervalDays: 1  statsIntervalEndTimestamp: "2021-10-06T22:40:54Z"  statsIntervalStartTimestamp: "2021-10-05T22:40:54Z"
```

---

## Operating Support

If you have questions or need support, please refer to Veeam Kasten
Community
Support or
  open a case via https://my.veeam.com .

## Supported Kubernetes Versions â

Veeam Kasten currently supports deployments running on the following
  certified Kubernetes distributions and respective OpenShift versions:

Veeam Kasten does not support distribution versions that
    are no longer actively supported by their respective
    vendor or community.

| Kubernetes | RedHat Openshift | Notes | 1.32 |  | Respective OpenShift version is not supported yet |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1.32 |  | Respective OpenShift version is not supported yet |
| 1.31 | 4.18 |  |
| 1.30 | 4.17 |  |
| 1.29 | 4.16 |  |
| 1.28 | 4.15 | Kubernetes version *only* supported when deployed as an OpenShift cluster |

## Gathering Debugging Information â

Admin users running 4.5.7 or later can get support logs from the System Information page under the [Settings] menu in the
  navigation sidebar.

Alternatively, if you run into problems with Veeam Kasten, please run
  these commands on your cluster as a first step to get information to
  support. The script assumes that your default kubectl context is
  pointed to the cluster you have installed Veeam Kasten on and that Veeam
  Kasten is installed in the kasten-io namespace.

```
$ curl -s https://docs.kasten.io/downloads/8.0.3/tools/k10_debug.sh | bash;
```

By default, the debug script will generate a compressed archive file k10_debug_logs.tar.gz which will have separate log files for Veeam
  Kasten services.

If you installed Veeam Kasten in a different namespace or want to log to
  a different file you can specify additional option flags to the script:

```
$ curl -s https://docs.kasten.io/downloads/8.0.3/tools/k10_debug.sh | \    bash -s -- -n <k10-namespace> -o <logfile-name>;
```

See the script usage message for additional help.

The debug script can optionally gather metrics from the Prometheus
  server installed by Veeam Kasten, by specifying the --prom-duration flag with a value indicating the desired duration (e.g. "1d",
  "3h25m"). The start time of the metric collection is implicitly
  assumed to be the current time less the specified duration, but can be
  adjusted with the --prom-start-time flag to specify a time in the
  past. The format is either the simple duration string that is accepted
  by the duration flag, or a string that is parsable with the date command, which could be a timestamp or a free form relative or absolute
  time specification. For example:

```
$ curl -s https://docs.kasten.io/downloads/8.0.3/tools/k10_debug.sh | \    bash -s -- --prom-duration 4h30m --prom-start-time "-2 days -3 hours"
```

would collect 270 minutes of metrics starting from 51 hours in the past.

Metrics capture only works with the Prometheus instance installed by
    Veeam Kasten. The specified duration directly impacts the size of the
    captured metrics data so constrain the duration accordingly. One can
    also consider using the --prom-metrics-only flag to separate the
    collection of metrics from the collection of the logs.

### Application Debug Information â

If you are having issues with a particular application, please also
  gather the following information.

```
## Get Application Information$ kubectl get pvc -oyaml --namespace <APP NAMESPACE>$ kubectl api-resources --verbs=list --namespaced -o name | \    xargs -n 1 kubectl get --show-kind --ignore-not-found --namespace <APP NAMESPACE>
```

Please also get the Helm status:

```
## If deployed via Helm$ helm status <RELEASE NAME> --namespace=<APP NAMESPACE>
```

## Veeam Kasten Tools â

The k10tools binary has commands that can help with validating if a cluster
  is setup correctly before installing Veeam Kasten and for debugging Veeam
  Kasten's micro services.

To learn more about this, see Veeam Kasten Tools .

## Storage Class Validation â

k10tools provides an option to validate storage classes via CSI Capabilities Check or Generic Volume Snapshot Capabilities Check commands. It is also possible for admin users to validate
  storage classes from the Veeam Kasten dashboard, under the System Information page of the Settings menu in the navigation
  sidebar. The state "Unknown" is shown until validation is run.

## Security Disclosures â

We value the critical role that the security community plays in helping
  us protect the confidentiality, integrity, and availability of our
  software, services, and information. If you have information about
  security vulnerabilities that affect Kasten software, services, or
  information, please report it via our vulnerability disclosure
program .

---

