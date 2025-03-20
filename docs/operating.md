## Operating Documentation
### latest_operating_operating.md
## Operating Veeam Kasten
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
There are a variety of ways to interact with the Veeam Kasten platform
ranging from command-line interaction to monitoring the status of policies and
jobs in the system. The following sections cover these topics in
depth.
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_reporting.md
## Reporting
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
Enabling Veeam Kasten Reports
Viewing Generated Reports
Viewing Reports With The Dashboard
Viewing Reports With kubectl
- Enabling Veeam Kasten Reports
- Viewing Generated Reports
Viewing Reports With The Dashboard
Viewing Reports With kubectl
- Viewing Reports With The Dashboard
- Viewing Reports With kubectl
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Reporting
Veeam Kasten Reporting provides regular insights into key performance and
operational states of the system. When reporting is enabled, Veeam Kasten
periodically collects information from the system and compiles it into a
report. Generated reports include information such as license status,
actions run, configured policies and profiles, compliance information,
and service information.
### Enabling Veeam Kasten Reports
Under Usage and Reports menu in the navigation sidebar, select Reports
and then select Enable Reports.
When enabled, a policy is created to manage the generation of reports. Reports
are generated according to the policy and then stored in the cluster. The
policy is also be visible on the policies page.
### Viewing Generated Reports
A generated report contains information about the state of the system at the
time the report was generated as well as select metrics collected from the
Veeam Kasten Prometheus service.
Note
If some of the information is unavailable at the time the report
is generated, it is omitted from the report. For example, if the Veeam
Kasten Prometheus service is disabled or otherwise unavailable, metrics
are omitted from the report.
### Viewing Reports With The Dashboard
Recent reports can be viewed on the Usage & Reports page. The full details of
a given report can be viewed by clicking on a report in the list.
### Viewing Reports With kubectl
Reports can be listed and viewed using kubectl.
Tip
By default, kubectl get doesn't sort results, they're displayed
in the same order they're received from the API server. This means
reports may not be listed in the order they were generated.
The --sort-by=.spec.reportTimestamp option can be added to ensure the
most recent reports are listed last.
An individual report can also be shown using the -o yaml option for
kubectl get:
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_garbagecollector.md
## Garbage Collector
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
Supported Resource Types
- Supported Resource Types
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Garbage Collector
Veeam Kasten provides a way to collect and clean up the resources that
are either orphaned or their expiration period has passed.
The following Helm options can be used to tune Garbage Collector behavior:
- garbagecollector.daemonPeriod - the length of time between
two consecutive garbage collection events (in seconds)
- garbagecollector.keepMaxActions - how many finished actions to keep
(if value is less than or equal to 0, no actions will be deleted)
- garbagecollector.actions.enabled - enables action
collectors (boolean)
### Supported Resource Types
Garbage Collector daemon can currently clean up the following resource types:
- Actions: When the limit, as defined by garbagecollector.keepMaxActions,
is exceeded, the oldest actions are removed until the limit is reached.
Each action type is handled independently in this process.
- RestorePointContents - expired manual backups will be removed
as determined by spec.expiresAt.
This can be set via kubectl or on the manual snapshot page in the UI.
- CSISnapshot - temporary CSI snapshots created during restore operations.
- PersistentVolumes - temporary volumes created during restore operations.
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_security_requirements.md
## Security Requirements
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
Permissions Requirements
runAsUser, runAsGroup
fsGroup
NFS Location Profile
- Permissions Requirements
- runAsUser, runAsGroup
- fsGroup
- NFS Location Profile
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Security Requirements
Veeam Kasten requires additional privileges to efficiently
backup and restore applications due to the nature of
backup, recovery, and migration operations.
This article contains descriptions and motivation
for all the privileges required by Veeam Kasten.
### Permissions Requirements
Veeam Kasten requires the following capabilities for both
the Veeam Kasten installation namespace (default: kasten-io)
and the target application's namespace:
- DAC_OVERRIDE: Allows to read the data on the volume
regardless of the permissions set.
Veeam Kasten needs this capability to read all the data from the volume.
- FOWNER: Allows to change owner (chown) of the files and directories.
This capability allows Veeam Kasten to correctly restore
the owner of the entity following the restore process.
- CHOWN: Allows to change permissions (chmod) of files and directories.
This capability allows Veeam Kasten to correctly restore access permissions
for the entity following the restore process.
See Linux Capabilities for a detailed description of the above capability requirements.
### runAsUser, runAsGroup
Veeam Kasten runs pods with UID = 1000 and GID = 1000,
which need to be permitted by the security policies.
Additionally, it might be required to allow
the default Prometheus UID\GID.
See Monitoring for
information about Grafana and Prometheus usage.
Note
### fsGroup
Value 1000 for fsGroup parameter
should be allowed by security policies.
During the restore phase, Veeam Kasten creates a volume for restoring data
and sets fsGroup = 1000 to the internal restore-data-*
pod's securityContext so that data can be written to that volume.
### NFS Location Profile
If the NFS location profile is used in rootless mode,
the security policies must allow the supplementalGroup
used by the profile.
See NFS Location Profile for details.
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_dr.md
## Veeam Kasten Disaster Recovery
- Veeam Kasten Disaster Recovery
Configuring Veeam Kasten Disaster Recovery Mode
Comparing Legacy DR and Quick DR
Enabling Veeam Kasten Disaster Recovery
Managing the Veeam Kasten Disaster Recovery Policy
Disabling Veeam Kasten Disaster Recovery
Recovering Veeam Kasten from a Disaster via UI
Recovering Veeam Kasten from a Disaster via CLI
Recovering Veeam Kasten From a Disaster via Helm
Specifying a Disaster Recovery Passphrase
Reinstalling Veeam Kasten
Configuring Location Profile
Restoring Veeam Kasten with k10restore
Restoring Veeam Kasten Backup with Iron Bank Kasten Images
Restoring Veeam Kasten Backup in FIPS Mode
Restoring Veeam Kasten Backup in Air-Gapped environment
Restoring Veeam Kasten Backup with Google Workload Identity Federation
Uninstalling k10restore
Recovering with the Operator
Using the Restored Veeam Kasten in Place of the Original
- Configuring Veeam Kasten Disaster Recovery Mode
Comparing Legacy DR and Quick DR
- Comparing Legacy DR and Quick DR
- Enabling Veeam Kasten Disaster Recovery
- Managing the Veeam Kasten Disaster Recovery Policy
- Disabling Veeam Kasten Disaster Recovery
- Recovering Veeam Kasten from a Disaster via UI
- Recovering Veeam Kasten from a Disaster via CLI
- Recovering Veeam Kasten From a Disaster via Helm
Specifying a Disaster Recovery Passphrase
Reinstalling Veeam Kasten
Configuring Location Profile
Restoring Veeam Kasten with k10restore
Restoring Veeam Kasten Backup with Iron Bank Kasten Images
Restoring Veeam Kasten Backup in FIPS Mode
Restoring Veeam Kasten Backup in Air-Gapped environment
Restoring Veeam Kasten Backup with Google Workload Identity Federation
Uninstalling k10restore
- Specifying a Disaster Recovery Passphrase
- Reinstalling Veeam Kasten
- Configuring Location Profile
- Restoring Veeam Kasten with k10restore
- Restoring Veeam Kasten Backup with Iron Bank Kasten Images
- Restoring Veeam Kasten Backup in FIPS Mode
- Restoring Veeam Kasten Backup in Air-Gapped environment
- Restoring Veeam Kasten Backup with Google Workload Identity Federation
- Uninstalling k10restore
- Recovering with the Operator
- Using the Restored Veeam Kasten in Place of the Original
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Veeam Kasten Disaster Recovery
As Veeam Kasten is a stateful application running on the
cluster, it must be responsible for backing up its own data to enable
recovery in the event of disaster - this is enabled by the
Veeam Kasten Disaster Recovery (KDR) policy. In particular, KDR
provides the ability to recover the Veeam Kasten platform
from a variety of disasters, such as the unintended deletion of
Veeam Kasten or its restore points, the failure of the underlying
storage used by Veeam Kasten, or even the accidental
destruction of the Kubernetes cluster on which Veeam Kasten is deployed.
### Configuring Veeam Kasten Disaster Recovery Mode
The KDR mode specifies how internal Veeam Kasten resources are protected. The
mode can be set either before or after enabling the KDR policy. Changes
to the KDR mode only apply to future KDR policy runs.
All installations default to Legacy DR mode. Quick DR mode is available
and recommended for installations using snapshot-capable storage.
Warning
Quick DR mode should only be enabled if the storage provisioner
used for Veeam Kasten PVCs supports both the creation of snapshots
and the ability to restore the existing volume from a snapshot.
- To enable Quick DR mode, install or upgrade Veeam Kasten
with the --set kastenDisasterRecovery.quickMode.enabled=true Helm value.
- To enable Legacy DR mode, install or upgrade Veeam Kasten
with the --set kastenDisasterRecovery.quickMode.enabled=false Helm value.
### Comparing Legacy DR and Quick DR
Refer to the details below to understand the key differences between
each mode.
Quick DR
- Snapshot-capable storage for Veeam Kasten PVCs required
- Incrementally exports only necessary data from the catalog database
and creates a local snapshot of the catalog PVC on each policy run
- Enables recovery of exported restore points on any cluster
- Enables recovery of local restore points, exported
restore points, and action history only where the local catalog
snapshot is available (i.e. in-place recovery on the
original cluster)
- Faster KDR backup and recovery versus Legacy DR
- Consumes less location profile storage versus Legacy DR
- Protects additional Veeam Kasten resource types versus Legacy DR
Legacy DR
- No dependency on snapshot-capable storage for Veeam
Kasten PVCs
- Exports a full dump of the catalog database
on each policy run
- Enables recovery of local restore points, exported
restore points, and action history
KDR Protected Resource Matrix
Veeam Kasten Resource
Actions
Yes(1)
Yes
Local Restore Points
Exported Restore Points
Policies
Basic User Policies
No
Profiles
Blueprints
Blueprint Bindings
Policy Presets
Transform Sets
Multi-Cluster Primary
Multi-Cluster Secondary
Reports
ActionPodSpecs
AuditConfig
StorageSecurityContext
StorageSecurityContextBinding
Note
For Quick DR, resources marked with (1) can only be
restored if a local KDR snapshot is available.
### Enabling Veeam Kasten Disaster Recovery
Enabling Veeam Kasten Disaster Recovery (KDR) creates a dedicated
policy within Veeam Kasten to back up its resources and catalog data
to an external location profile.
Veeam Repository location profiles cannot
be used as a destination for KDR backups.
It is strongly recommended to use a location profile
that supports immutable backups to ensure
restore point catalog data can be recovered in the event of
incidents including ransomware and accidental deletion.
The Veeam Kasten Disaster Recovery settings are accessible via the
Setup Kasten DR page under the Settings menu in the
navigation sidebar. For new installations, these settings are
also accessible using the link located within the alerts panel.
Select the Setup Kasten DR page under the Settings menu in the
navigation sidebar.
Enabling KDR requires selecting a Location
Profile for the exported KDR backups and providing
a passphrase to encrypt the data using AES-256-GCM.
The passphrase can be provided as a raw string
or as reference to a secret in HashiCorp Vault or AWS Secrets Manager.
Enable KDR by selecting a valid location profile and providing
either a raw passphrase or secret management credentials, then clicking
the Enable Kasten DR button.
If providing a raw passphrase,
save it securely outside the cluster.
Using HashiCorp Vault requires that
Kasten is configured to access Vault.
Using AWS Secrets Manager requires that an
AWS Infrastructure Profile exists
with the adequate permissions
A confirmation message with the cluster ID will be displayed
when KDR is enabled. This ID is used as a prefix to
the object storage or NFS file storage location where Veeam Kasten
saves its exported backup data.
After enabling Veeam Kasten Disaster Recovery, it is essential
to retain the following to successfully recover Veeam Kasten
from a disaster:
1. The source cluster ID
2. The KDR passphrase (or external secret manager details)
3. The KDR location profile details and credential
Without this information, restore point catalog recovery will not be possible.
The cluster ID value can also be accessed by using the
following kubectl command.
### Managing the Veeam Kasten Disaster Recovery Policy
A policy named k10-disaster-recovery-policy that implements
Veeam Kasten Disaster Recovery (KDR) will automatically be created when
KDR is enabled. This policy can be viewed through the Policies
page in the navigation sidebar.
Click Run Once on the k10-disaster-recovery-policy to start a
manual backup.
Click Edit to modify the frequency and retention settings. It is
recommended that the KDR policy match the frequency of the lowest RPO
policy on the cluster.
### Disabling Veeam Kasten Disaster Recovery
Veeam Kasten Disaster Recovery can be disabled by clicking
the Disable Kasten DR button on the Setup Kasten DR page,
which is found under the Settings menu in the navigation sidebar.
It is not recommended to run Veeam Kasten without KDR enabled.
### Recovering Veeam Kasten from a Disaster via UI
To recover from a KDR backup using the UI, follow these steps:
1. On a new cluster, install a fresh Veeam Kasten instance in the same
namespace as the original Veeam Kasten instance.
2. On the new cluster, create a location profile by providing the
bucket information and credentials for the object storage
location or NFS file storage location where previous Veeam
Kasten backups are stored.
3. On the new cluster, navigate to the Restore Kasten
page under the Settings menu in the navigation sidebar.
4. In the Profile drop-down, select the location profile created
in step 3.
1. For Cluster ID, provide the ID of the original cluster with
Veeam Kasten Disaster Recovery enabled. This ID can be found
on the Setup Kasten DR page of the original cluster that
currently has Veeam Kasten Disaster Recovery enabled.
- Raw passphrase: Provide the passphrase used when enabling
Disaster Recovery.
- HashiCorp Vault: Provide the Key Value Secrets Engine Version,
Mount, Path, and Passphrase Key stored in a HashiCorp Vault secret.
- AWS Secrets Manager: Provide the secret name, its associated region,
and the key.
For immutable location profiles, a previous
point in time can be provided to filter out any restore points
newer than the specified time in the next step. If no specific
date is chosen, it will display all available restore points,
with the most recent ones appearing first.
1. Click the Next button to start the validation process.
If validation succeeds, a drop-down containing the available
restore points will be displayed.
All times are displayed in the local timezone of the
client's browser.
1. Select the desired restore point and click the Next button.
2. Review the summary and click the Start Restore button to
begin the restore process.
1. Upon completion of a successful restoration, navigation to the
dashboard and information about ownership and deletion of
the configmap is displayed.
Following recovery of the Veeam Kasten restore point catalog,
restore cluster-scoped resources and
applications as required.
### Recovering Veeam Kasten from a Disaster via CLI
In Veeam Kasten v7.5.0 and above, KDR recoveries can be performed via
API or CLI using DR API Resources.
Recovering from a KDR backup using CLI involves the following
sequence of steps:
1. Create a Kubernetes Secret, k10-dr-secret, using the passphrase
provided while enabling Disaster Recovery as described in
Specifying a Disaster Recovery Passphrase.
2. Install a fresh Veeam Kasten instance in the same namespace as the above
Secret.
3. Provide bucket information and credentials for the object storage
location or NFS file storage location where previous Veeam Kasten backups
are stored.
4. Create KastenDRReview resource providing
the source cluster information.
5. Create KastenDRRestore resource
referring to the KastenDRReview resource and choosing one of the restore
points provided in the KastenDRReview status.
6. The steps 4 and 5 can be skipped and KastenDRRestore resource can be
created directly with the source cluster information.
7. Delete the KastenDRReview and KastenDRRestore resources after restore
completes.
### Recovering Veeam Kasten From a Disaster via Helm
The k10restore Helm chart is deprecated with Veeam Kasten v7.5.0
release and will be removed in a future release.
Recovering from a KDR backup using k10restore involves the
following sequence of actions:
1. Create a Kubernetes Secret, k10-dr-secret, using the passphrase
provided while enabling Disaster Recovery
2. Install a fresh Veeam Kasten instance in the same namespace as the above
Secret
3. Provide bucket information and credentials for the object storage
location or NFS file storage location where previous Veeam Kasten backups
are stored
4. Restoring the Veeam Kasten backup
5. Uninstalling the Veeam Kasten restore instance after recovery is
recommended
If Kasten was previously installed in FIPS mode, ensure the fresh
Veeam Kasten instance is also installed in FIPS mode.
If Veeam Kasten backup is stored using an
NFS File Storage Location, it is
important that the same NFS share is reachable from the recovery cluster
and is mounted on all nodes where Veeam Kasten is installed.
### Specifying a Disaster Recovery Passphrase
Currently, Veeam Kasten Disaster Recovery encrypts all artifacts via the
use of the AES-256-GCM algorithm. The passphrase entered while enabling
Disaster Recovery is used for this encryption. On the cluster used for
Veeam Kasten recovery, the Secret k10-dr-secret needs to be
therefore created using that same passphrase in the Veeam Kasten
namespace (default kasten-io)
The passphrase can be provided as a raw string or reference
a secret in HashiCorp Vault or AWS Secrets Manager.
Specifying the passphrase as a raw string:
Specifying the passphrase as a HashiCorp Vault secret:
The supported values for vault-kv-version are KVv1 and KVv2.
Using a passphrase from HashiCorp Vault also requires enabling
HashiCorp Vault authentication when installing the kasten/k10restore
helm chart. Refer: Enabling HashiCorp Vault using
Token Auth or
Kubernetes Auth.
Specifying the passphrase as an AWS Secrets Manager secret:
### Reinstalling Veeam Kasten
When reinstalling Veeam Kasten on the same cluster, it is
important to clean up the namespace in which Veeam Kasten was
previously installed before the above passphrase creation.
Veeam Kasten must be reinstalled before recovery. Please follow
the instructions here.
### Configuring Location Profile
Create a Location Profile with the object
storage location or NFS file storage location where Veeam Kasten
KDR backups are stored.
### Restoring Veeam Kasten with k10restore
Requirements:
- Source cluster ID
- Name of Location Profile from the previous step
If Veeam Kasten Quick Disaster Recovery is enabled, the Veeam Kasten restore
helm chart should be installed with the following helm value:
The overrideResources flag must be set to true when using
Quick Disaster Recovery. Since the Disaster Recovery operation involves
creating or replacing resources, confirmation should be provided
by setting this flag.
Veeam Kasten provides the ability to apply labels and annotations to all
temporary worker pods created during Veeam Kasten recovery as part of its
operation. The labels and annotations can be set through the podLabels and
podAnnotations Helm flags, respectively. For example, if using a
values.yaml file:
Alternatively, the Helm parameters can be configured using the --set flag:
The restore job always restores the restore point catalog and artifact
information. If the restore of other resources (options include profiles,
policies, secrets) needs to be skipped, the skipResource flag can be used.
The timeout of the entire restore process can be configured by the helm field
restore.timeout. The type of this field is int and the value is
in minutes.
If the Disaster Recovery Location Profile was configured for
Immutable Backups, Veeam Kasten can be
restored to an earlier point in time. The protection period chosen when
creating the profile determines how far in the past the point-in-time
can be. Set the pointInTime helm value to the desired time stamp.
See Immutable Backups Workflow for additional
information.
### Restoring Veeam Kasten Backup with Iron Bank Kasten Images
The general instructions found in
Restoring Veeam Kasten with k10restore
can be used for restoring Veeam Kasten using Iron Bank
hardened images with a few changes.
Specific helm values are used to ensure that the Veeam Kasten
restore helm chart only uses Iron Bank images.
The values file must be downloaded by running:
This file is protected and should not be modified. It is necessary
to specify all other values using the corresponding helm flags, such as
--set, --values, etc.
Credentials for Registry1 must be provided in order to successfully pull
the images. These should already have been created as part of re-deploying a
new Veeam Kasten instance; therefore, only the name of the secret should be
used here.
The following set of flags should be added to the instructions found in
Restoring Veeam Kasten with k10restore to use
Iron Bank images for Veeam Kasten recovery:
### Restoring Veeam Kasten Backup in FIPS Mode
The general instructions found in
Restoring Veeam Kasten with k10restore
can be used for restoring Veeam Kasten in FIPS mode with a few changes.
To ensure that certified cryptographic modules are utilized, you must install
the k10restore chart with additional Helm values that can be found here: FIPS
values. These should be added to the
instructions found in
Restoring Veeam Kasten with k10restore
for Veeam Kasten disaster recovery:
### Restoring Veeam Kasten Backup in Air-Gapped environment
In case of air-gapped installations, it's assumed that k10offline tool is
used to push the images to a private container registry.
Below command can be used to instruct k10restore to run in air-gapped mode.
### Restoring Veeam Kasten Backup with Google Workload Identity Federation
Veeam Kasten can be restored from a Google Cloud Storage bucket using the
Google Workload Identity Federation. Please follow the instructions
provided here to restore Veeam Kasten with
this option.
### Uninstalling k10restore
The K10restore instance can be uninstalled with the helm uninstall command.
### Enabling HashiCorp Vault using Token Auth
Create a Kubernetes secret with the Vault token.
This may cause the token to be stored in shell history.
Use these additional parameters when installing the kasten/k10restore
helm chart.
### Enabling HashiCorp Vault using Kubernetes Auth
Refer to Configuring Vault Server For Kubernetes Auth prior to installing the kasten/k10restore helm chart.
Use these additional parameters when installing the
kasten/k10restore helm chart.
vault.role is the name of the Vault Kubernetes authentication role binding
the Veeam Kasten service account and namespace to the Vault policy.
vault.serviceAccountTokenPath is optional and defaults to
/var/run/secrets/kubernetes.io/serviceaccount/token.
### Recovering with the Operator
If you have deployed Veeam Kasten via the OperatorHub on an OpenShift cluster,
the k10restore tool can be deployed via the Operator as described below.
However, it is recommended to use either the
Recovering Veeam Kasten from a Disaster via UI or
Recovering Veeam Kasten from a Disaster via CLI
process.
Recovering from a Veeam Kasten backup involves the following sequence of
actions:
1. Install a fresh Veeam Kasten instance.
2. Configure a Location Profile from
where the Veeam Kasten backup will be restored.
3. Create a Kubernetes Secret named k10-dr-secret in the same namespace
as the Veeam Kasten install, with the passphrase given when disaster
recovery    was enabled on the previous Veeam Kasten instance.
The commands are detailed here.
4. Create a K10restore instance. The required values are
Cluster ID - value given when disaster recovery was enabled
on the previous Veeam Kasten instance.
Profile name - name of the Location Profile configured in Step 2.
and the optional values are
Point in time - time (RFC3339) at which to evaluate restore data.
Example "2022-01-02T15:04:05Z".
Resources to skip - can be used to skip restore of specific resources.
Example "profile,policies".
After recovery, deleting the k10restore instance is recommended.
5. Cluster ID - value given when disaster recovery was enabled
on the previous Veeam Kasten instance.
6. Profile name - name of the Location Profile configured in Step 2.
7. Point in time - time (RFC3339) at which to evaluate restore data.
Example "2022-01-02T15:04:05Z".
8. Resources to skip - can be used to skip restore of specific resources.
Example "profile,policies".
Create a K10restore instance. The required values are
and the optional values are
After recovery, deleting the k10restore instance is recommended.
Operator K10restore form view with Enable HashiCorp Vault set to False
Operator K10restore form view with Enable HashiCorp Vault set to True
### Using the Restored Veeam Kasten in Place of the Original
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
It is critical that you delete this resource only when you are prepared
to make the permanent cutover to the new DR-restored Veeam Kasten instance.
Running multiple Veeam Kasten instances simultaneously, each assuming
ownership, can corrupt backup data.
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_support.md
## Support and Troubleshooting
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
Supported Kubernetes Versions
Gathering Debugging Information
Application Debug Information
Veeam Kasten Tools
Storage Class Validation
Security Disclosures
- Supported Kubernetes Versions
- Gathering Debugging Information
Application Debug Information
- Application Debug Information
- Veeam Kasten Tools
- Storage Class Validation
- Security Disclosures
- Uninstalling Veeam Kasten
-
- Operating Veeam Kasten
- Support and Troubleshooting
If you have questions or need support, please refer to
Veeam Kasten Community Support
or open a case via https://my.veeam.com.
### Supported Kubernetes Versions
Veeam Kasten currently supports deployments running on the following certified
Kubernetes distributions and respective OpenShift versions:
Note: Veeam Kasten also does not support distributions/versions that have
been declared 'End of Life' status as defined by their respective
entity/community/vendor (in other words, distributions/versions for which
maintenance is not provided anymore by their supporting
entity/community/vendor).
Kubernetes
RedHat Openshift
Notes
1.31
Respective OpenShift version is not supported yet
1.30
4.17
1.29
4.16
1.28
4.15
1.27
4.14
Kubernetes version only supported when deployed as an OpenShift cluster
1.26
4.13
1.25
4.12
### Gathering Debugging Information
Admin users running 4.5.7 or later can get support logs from the
System Information page under the Settings menu in the
navigation sidebar.
Alternatively, if you run into problems with Veeam Kasten, please run
these commands on your cluster as a first step to get information to
support. The script assumes that your default kubectl context is
pointed to the cluster you have installed Veeam Kasten on and that
Veeam Kasten is installed in the kasten-io namespace.
By default, the debug script will generate a compressed archive file
k10_debug_logs.tar.gz which will have separate log files
for Veeam Kasten services.
If you installed Veeam Kasten in a different namespace or want to log to
a different file you can specify additional option flags to the script:
See the script usage message for additional help.
The debug script can optionally gather metrics from the Prometheus
server installed by Veeam Kasten,
by specifying the --prom-duration flag with a value indicating
the desired duration (e.g. "1d", "3h25m").
The start time of the metric collection is implicitly assumed to
be the current time less the specified duration, but can be adjusted
with the --prom-start-time flag to specify a time in the past.
The format is either the simple duration string that is accepted by
the duration flag,
or a string that is parsable with the date command, which could
be a timestamp or a free form relative or absolute time specification.
For example:
would collect 270 minutes of metrics starting from 51 hours in the past.
Note
Metrics capture only works with the Prometheus instance installed
by Veeam Kasten.
The specified duration directly impacts the size of the captured
metrics data so constrain the duration accordingly.
One can also consider using the --prom-metrics-only flag to
separate the collection of metrics from the collection of the logs.
### Application Debug Information
If you are having issues with a particular application, please also
gather the following information.
Please also get the Helm status:
### Veeam Kasten Tools
The k10tools binary has commands that can help with validating if a cluster
is setup correctly before installing Veeam Kasten and for debugging Veeam
Kasten's micro services.
To learn more about this, see Veeam Kasten Tools.
### Storage Class Validation
k10tools provides an option to validate
storage classes via CSI Capabilities Check or
Generic Volume Snapshot Capabilities Check commands.
It is also possible for admin users to validate storage classes from the
Veeam Kasten dashboard, under the System Information page of the
Settings menu in the navigation sidebar. The state "Unknown" is shown
until validation is run.
### Security Disclosures
We value the critical role that the security community plays in helping
us protect the confidentiality, integrity, and availability of our software,
services, and information. If you have information about security
vulnerabilities that affect Kasten software, services, or information, please
report it via our vulnerability disclosure program.
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_siem.md
## Integrating Security Information and Event Management (SIEM) Systems
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
Detecting Veeam Kasten SIEM Scenarios
Enabling Agent-based Veeam Kasten Event Capture
Enabling Agent-less Veeam Kasten Event Capture
Datadog Cloud SIEM
Configuring Ingest
Adding Detection Rules
Microsoft Sentinel
Configuring Ingest
Importing Analytics Rules
- Detecting Veeam Kasten SIEM Scenarios
- Enabling Agent-based Veeam Kasten Event Capture
- Enabling Agent-less Veeam Kasten Event Capture
- Datadog Cloud SIEM
Configuring Ingest
Adding Detection Rules
- Configuring Ingest
- Adding Detection Rules
- Microsoft Sentinel
Configuring Ingest
Importing Analytics Rules
- Importing Analytics Rules
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
Inhibiting data protection software and deleting backup data are examples
of actions that may be taken by a malicious actor before proceeding to the
next stage of an attack, such as file encryption. Prompt notification of such
potentially malicious behavior can help mitigate the impact of an attack.
To provide activity correlation and analysis, Veeam Kasten can integrate
with SIEM solutions. SIEMs ingest and aggregate data from an environment,
including logs, alerts, and events, for the purpose of providing real-time
threat detection and analysis, and assisting in investigations.
As an application built upon Kubernetes CRDs and API Aggregation, Veeam
Kasten events (e.g., creating a Location Profile resource) can be captured
through the Kubernetes audit log.
These events can then be ingested by a SIEM system. However, there are
situations where you may not have direct control over the Kubernetes audit
policy configuration for a cluster (or the kube-apiserver), especially when
using a cloud-hosted managed Kubernetes service. This limitation can impact the
detail available in Kubernetes API server responses that can be collected for
audit events and the customization of log transmission.
For this reason, Veeam Kasten provides an extended audit mechanism to
enable direct ingestion of Veeam Kasten events into a SIEM system,
independently of Kubernetes cluster audit policy configurations.
Furthermore, this extended mechanism allows more fine-tuned control
over how to store these logs, including options like file-based and
cloud-based storage.
The audit policy applied to Veeam Kasten's aggregated-apiserver is the
following:
This section provides documentation on configuring each of these mechanisms
and includes example rules that a SIEM system can enable. Sample
integrations are provided for Datadog Cloud SIEM and Microsoft Sentinel, though
similar detection rules can be adapted to any SIEM platform capable of
ingesting Kubernetes audit and container logs.
### Detecting Veeam Kasten SIEM Scenarios
Below are multiple scenarios which could be used to drive SIEM detection and
alerts based on Veeam Kasten user activity:
Resource
Action
RestorePoints
Excessive Deletion
RestorePointContents
ClusterRestorePoints
CancelAction
Excessive Create
RetireAction
Passkeys
Excessive Update/Delete/Get
### Enabling Agent-based Veeam Kasten Event Capture
By default, Veeam Kasten is deployed to write these new audit event logs to
stdout (standard output) from the aggregatedapis-svc pod. These logs
can be ingested using an agent installed in the cluster. Examples for
Datadog Cloud SIEM and
Microsoft Sentinel are provided below.
To disable, configure the Veeam Kasten deployment with
--set siem.logging.cluster.enabled=false.
### Enabling Agent-less Veeam Kasten Event Capture
Many SIEM solutions support ingestion of stdout log data from Kubernetes
applications using an agent deployed to the cluster. If an agent-based
approach is not available or not preferred, Veeam Kasten offers the
option to send these audit events to a Location Profile. SIEM-specific
tools can then be used to ingest the log data from the object store.
Note
Currently, only AWS S3 Location Profiles are supported as a target for
Veeam Kasten audit events.
By default, Veeam Kasten is deployed with the ability to send these new
audit event logs to available cloud object stores. However, enabling this
feature is just the first step. The action of sending the logs depends on
the creation or update of an applicable
K10 AuditConfig that points to a
valid Location Profile. An example for Datadog is shown
below.
To disable the sending of these logs to AWS S3, you can configure the
Veeam Kasten deployment with the following command:
--set siem.logging.cloud.awsS3.enabled=false.
To begin, you should first determine the name of your target Location
Profile.
Next, define and apply an AuditConfig manifest to your Veeam Kasten
namespace. In the example below, make sure to replace the target values
for spec.profile.name and spec.profile.namespace before applying.
If the spec.profile.namespace is left blank, the default value
will be the namespace of the AuditConfig.
Veeam Kasten event logs will now be sent to the target Location Profile bucket
under the k10audit/ directory. If you wish to change the destination path
of the logs within the bucket, configure the Veeam Kasten deployment with
--set siem.logging.cloud.path=<DIRECTORY PATH WITHIN BUCKET>.
### Datadog Cloud SIEM
Veeam Kasten integrates with Datadog Cloud SIEM to provide high-fidelity signal
data that can be used to detect suspicious activity and support security operators.
### Configuring Ingest
Review each of the sections below to understand how Veeam Kasten event data can
be sent to Datadog. Both methods can be configured per cluster.
### Setting up the Datadog Agent on a Kubernetes Cluster
The Datadog Agent can be installed on the Kubernetes cluster and used to
collect application logs, metrics, and traces.
Refer to Datadog Kubernetes
documentation for complete instructions on installing the Agent on the
cluster.
For Datadog to ingest Veeam Kasten event logs, the Agent must be configured
with log collection enabled
and an include_at_match global processing rule to match the Veeam Kasten
specific pattern, (?i).*K10Event.*.
Here is an example of a values.yaml file for installing the Datadog Agent
using Helm:
Refer to the Datadog
processing rules
documentation for instructions on alternative methods for configuring
processing rules.
### Setting up the Datadog Forwarder with AWS
The Datadog Forwarder is an AWS Lambda function used to ingest Veeam
Kasten event logs sent to an AWS S3 bucket.
Refer to the Datadog
cloudformation
documentation to install the Forwarder in the same AWS region as the target S3
bucket.
After deploying the Forwarder, follow the to Datadog
S3 trigger
documentation to add an S3 Trigger using the settings below:
Field
Value
Bucket
<TARGET S3 BUCKET>
Event type
Object Created (All)
Prefix
<TARGET S3 BUCKET PREFIX> (defaults to k10audit/)
Suffix
<BLANK>
### Adding Detection Rules
Detection Rules define how Datadog analyzes ingested data and when to
generate a signal. Using these rules, Veeam Kasten event data can be
used to alert organizations to specific activity that could indicate
an ongoing security breach. This section provides the details required
to add example Veeam Kasten rules to Datadog Cloud SIEM.
Open the Datadog Cloud SIEM user
interface and select Detection Rules from the toolbar.
At the top right corner of the page, click the New Rule button.
Complete the form using the details below for each rule.
Each rule should be configured to notify the appropriate services
and/or users. Since the specific configurations are unique to each
environment, they are not covered in the examples provided below.
### Veeam Kasten RestorePoints Manually Deleted
The purpose of this rule is to detect deletions of Veeam Kasten
RestorePoint resources initiated by a user.
Typically, the removal of this type of resource would be the result of backup
data no longer being needed based on a policy's retention schedule and
performed directly by Veeam Kasten.
Removal of a Kubernetes namespace containing RestorePoints may also
trigger this signal.
Rule Name
Kasten RestorePoints Manually Deleted
Rule Type
Log Detection
Detection Method
Threshold
Query
Trigger
deleted_k10_rps > 0
Severity
Low
Tags
tactic:TA0040-impact
Use the following notification body to provide an informative alert:
### Kasten RestorePointContents Manually Deleted
The purpose of this rule is to detect deletions of Veeam Kasten
RestorePointContent resources initiated by a
user. The removal of this type of resource should only be the result of backup
data no longer being needed based on a policy's retention schedule and
performed directly by Veeam Kasten.
Kasten RestorePointContents Manually Deleted
deleted_k10_rpcs > 0
High/Critical
tactic:TA0040-impact,
technique:T1490-inhibit-system-recovery
Use of the cluster-name tag in both the query and notification
body requires capturing Veeam Kasten event logs via Datadog Agent.
### Veeam Kasten ClusterRestorePoints Manually Deleted
The purpose of this rule is to detect deletions of Veeam Kasten
ClusterRestorePoint resources initiated by a
user. The removal of this type of resource should only be the result of backup
data no longer being needed based on a policy's retention schedule and
performed directly by Veeam Kasten.
Kasten ClusterRestorePoints Manually Deleted
deleted_k10_crps > 0
### Microsoft Sentinel
Veeam Kasten integrates with Microsoft Sentinel to provide high-fidelity
signal data that can be used to detect suspicious activity and support
security operators.
### Configuring Ingest
The Azure Monitor agent can be installed on Azure Kubernetes Service (AKS) and
Azure Arc-managed Kubernetes clusters for collecting logs and metrics.
Refer to the Azure Monitor documentation for instructions on enabling Container Insights. Container Insights
must be configured to send container logs to the Log Analytics
workspace associated with Sentinel.
To minimize the cost associated with log collection, individual namespaces
may be excluded from Azure Monitor using a ConfigMap as documented here.
### Importing Analytics Rules
Analytics Rules define how Sentinel analyzes ingested data and when to
generate an alert. Using these rules, Veeam Kasten event data can be
used to alert organizations to specific activity that could indicate an
ongoing security breach. This section provides the details required to
add example Veeam Kasten rules to Sentinel.
Download the provided rules:
kasten_sentinel_rules.json
1. Open a Sentinel instance from the Azure Portal user interface.
2. Select Analytics from the sidebar.
1. Select Import from the toolbar.
2. Choose the previously downloaded file named kasten_sentinel_rules.jsonto import the rules.
to import the rules.
### Kasten RestorePoint Resources Manually Deleted
The purpose of this rule is to detect deletions of Veeam Kasten
RestorePoint, RestorePointContents, ClusterRestorePoint,
and ClusterRestorePointContents resources initiated by a user.
The removal of these resource types should only occur as a
result of backup data no longer being needed based on a policy's
retention schedule and performed directly by Veeam Kasten.
Each rule should be configured to notify the appropriate services
and/or users. Since each environment has its own configurations, these are not covered in the examples provided below. See
the  Sentinel documentation
for details on creating automation rules to manage notifications and
responses.
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_audit.md
## Auditing Veeam Kasten
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
Authentication Mode
Request Attribution
- Authentication Mode
- Request Attribution
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Auditing Veeam Kasten
Independent of whether the dashboard, CLI, or API is used to access
Veeam Kasten, the usage translates into native Kubernetes API calls.
Veeam Kasten usage can therefore be transparently audited using the
Kubernetes Auditing
feature without requiring any additional changes.
Note
Managed Kubernetes providers like EKS, GKE, and AKS do not allow any
modifications to the kube-apiserver flags,  thereby lacking control
over the passed-in audit policy. Typically, these providers log the audit
events at the metadata level, resulting in the loss of important
information within the request and response bodies.
This approach is not applicable if you want to send these logs to
different cloud object stores or use NFS for storing the logs.
Since the Kubernetes Auditing feature only has access to Kubernetes API calls,
any internal Veeam Kasten event that does not use this API will not get logged.
The ongoing work with integrating Veeam Kasten more closely with
Security Information and Event Management (SIEM) platforms,
such as with Datadog, will allow for a more robust auditing of Veeam Kasten.
When viewing audit logs, consider the following:
### Authentication Mode
For correct user attribution, we depend on Veeam Kasten to be set up with OIDC
or token-based authentication.
- OIDC: When OIDC is enabled, Kubernetes user impersonation will
be used based on the email address extracted from the provided OIDC
token.
- Token-based Authentication: When token-based authentication is
enabled, the token is used directly for making API calls.
### Request Attribution
Note that there are two callers of Veeam Kasten and Kubernetes APIs in the
Veeam Kasten system. Actions triggered by the dashboard, CLI, or API will be
attributed to the user that initiated them. Other system actions
(e.g., validation of a Profile or Policy) will be attributed to the
Veeam Kasten Service Account (SA).
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_uninstall.md
## Uninstalling Veeam Kasten
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
It is important to uninstall Veeam Kasten with the Helm command to
ensure that all non-namespaced resources are cleaned up. Simply
deleting the namespace Veeam Kasten is installed in might cause
issues with stale services. Assuming Veeam Kasten was installed
with the release name k10 and in the kasten-io namespace,
run the following command to uninstall:
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_monitoring.md
## Monitoring
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
Using Veeam Kasten's Prometheus Endpoint
Veeam Kasten Metrics
Veeam Kasten Action Metrics
Veeam Kasten Artifact Metrics
Veeam Kasten Compliance Metrics
Veeam Kasten Execution Metrics
Veeam Kasten License Status
Veeam Kasten Status Metrics
Veeam Kasten Storage Metrics
Data Transfer Metrics
Veeam Kasten Multi-Cluster Metrics
Policy Metrics
Action Metrics
Storage Metrics
Using Externally Installed Grafana
Configuring Grafana's URL
Accessing Grafana from Veeam Kasten's dashboard
Charts and Graphs
Grafana Alerts
Alert rules
Contact Points
Notification Policies
Integrating External Prometheus with Veeam Kasten
Scrape Config
Network Policy
Generating Reports
Integration with External Tools
Exporting Metrics to Datadog
- Using Veeam Kasten's Prometheus Endpoint
- Veeam Kasten Metrics
Veeam Kasten Action Metrics
Veeam Kasten Artifact Metrics
Veeam Kasten Compliance Metrics
Veeam Kasten Execution Metrics
Veeam Kasten License Status
Veeam Kasten Status Metrics
Veeam Kasten Storage Metrics
Data Transfer Metrics
- Veeam Kasten Action Metrics
- Veeam Kasten Artifact Metrics
- Veeam Kasten Compliance Metrics
- Veeam Kasten Execution Metrics
- Veeam Kasten License Status
- Veeam Kasten Status Metrics
- Veeam Kasten Storage Metrics
- Data Transfer Metrics
- Veeam Kasten Multi-Cluster Metrics
Policy Metrics
Action Metrics
Storage Metrics
- Policy Metrics
- Action Metrics
- Storage Metrics
- Using Externally Installed Grafana
Configuring Grafana's URL
Accessing Grafana from Veeam Kasten's dashboard
Charts and Graphs
Grafana Alerts
Alert rules
Contact Points
Notification Policies
- Configuring Grafana's URL
- Accessing Grafana from Veeam Kasten's dashboard
- Charts and Graphs
- Grafana Alerts
- Alert rules
- Contact Points
- Notification Policies
- Integrating External Prometheus with Veeam Kasten
Scrape Config
Network Policy
- Scrape Config
- Network Policy
- Generating Reports
- Integration with External Tools
Exporting Metrics to Datadog
- Exporting Metrics to Datadog
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Monitoring
Veeam Kasten enables centralized monitoring of all its activity by integrating
with Prometheus. In particular, it exposes a Prometheus endpoint from
which a central system can extract data.
A Grafana instance can be installed in the same Kubernetes cluster
where Veeam Kasten is installed to query and visualize the metrics
from Veeam Kasten's prometheus instance. Steps to install a new Grafana
instance and integrating that with Veeam Kasten's prometheus instance
are documented here.
This section documents how to install and enable Prometheus, usage
of the metrics currently exposed, generation of alerts and reports based on
these metrics, and integration with external tools.
### Using Veeam Kasten's Prometheus Endpoint
By default, Prometheus is configured with persistent storage size 8Gi and
retention period of 30d. That can be changed with --set
prometheus.server.persistentVolume.size=<size> and --set
prometheus.server.retention=<days>.
Prometheus requires Kubernetes API access to discover Veeam Kasten pods
to scrape their metrics. Thus, by default Role and RoleBinding
entries are created in Veeam Kasten namespace. However, if you set
prometheus.rbac.create=true, global ClusterRole and
ClusterRoleBinding will be created instead.
The complete list of configurable parameters can be found at
Advanced Install Options.
If for some reason you don't want helm to create RBAC for you automatically
and you have both rbac.create=false and prometheus.rbac.create=false,
you can create Role and RoleBinding manually:
An external Prometheus server can be configured to scrape Veeam Kasten's
built-in server. The following scrape config is an example of how a
Prometheus server hosted in the same cluster might be configured:
Note
An additional NetworkPolicy may need to be applied in certain
environments.
Although it's possible to disable Veeam Kasten's built-in Prometheus server
enabled, it is recommended to leave it enabled. Disabling the server reduces
functionality in various parts of the system such as usage data, reporting, and
the multi-cluster dashboard. To disable the built-in server, set the
prometheus.server.enabled value to false.
If the built-in server has previously been disabled, it can be re-enabled
during a helm upgrade (see Upgrading Veeam Kasten) with: --set
prometheus.server.enabled=true.
### Veeam Kasten Metrics
Tip
When using Veeam Kasten Multi-Cluster Manager
(i.e., a cluster setup as a primary),
to query metrics for the primary cluster from its Prometheus instance
a cluster label with a blank value ("") is required.
### Veeam Kasten Action Metrics
When Veeam Kasten performs various actions throughout the system,
it collects metrics associated with these actions.
It records counts for both cluster and application-specific actions.
These action metrics include labels that describe the context of the action.
For actions specific to an application, the application name is included as
app. For actions initiated by a policy, the policy name is included as
policy. For ended actions, the final status is included as state
(i.e., succeeded, failed, or cancelled).
Separate metrics are collected for the number of times the action was started,
ended, or skipped. This is indicated by the suffix of the metric
(i.e., _started_count, _ended_count, or _skipped_count).
An overall set of metrics is also collected that does not include the app
or policy labels.
These metrics end with _overall rather than _count.
It is recommended to use the overall metrics unless specific application
or policy information is required.
Metrics are collected for the following actions:
- backup and backup_cluster
- restore and restore_cluster
- export
- import
- report
- run
For example, to query the number of successful backups in the past 24 hours:
Or, to query the number of failed restores for the past hour:
Important
When querying metrics that are reported as counters,
such as action metrics,
the increase or rate functions must be used.
See Prometheus query functions for
more information.
### Examples of Action Metrics
action_export_processed_bytes
The overall bytes processed during the export.
Labels: policy, app
action_export_transferred_bytes
The overall bytes transferred during the export.
Labels: policy, app
See the Prometheus docs
for more information on how to query data from Prometheus.
### Veeam Kasten Artifact Metrics
You can monitor both the rate of artifact creation and the current
count within Veeam Kasten.
Similar to the action counts mentioned above,
there are also the following metrics,
which track the number of artifacts backed up by Veeam Kasten within
a defined time frame:
- action_artifact_count
- action_artifact_count_by_app
- action_artifact_count_by_policy
To see the number of artifacts protected by snapshots currently you can use
the following metrics.
- artifact_sum
- artifact_sum_by_app
- artifact_sum_by_policy
If an artifact is protected by multiple snapshots then
it will be counted multiple times.
### Veeam Kasten Compliance Metrics
To track the number of applications that fall outside of compliance,
you can use the compliance_count metric,
which includes the following states of interest: [NotCompliant, Unmanaged].
If the cluster contains pre-existing namespaces,
which are not subject to compliance concerns,
you have the option to use the Helm flag excludedApps to exclude them.
This action will remove both the application(s) from the dashboard
and exclude them from the compliance_count.
You can set this exclusion using the inline array
(excludedApps: ["app1", "app2"]) or the multi-line array,
specifying the applications to be excluded:
If you prefer to set Helm values inline rather than through a YAML file,
you can do this with the following:
See the knowledge base article
for more information.
### Veeam Kasten Execution Metrics
### Aggregating Job and Phase Runner Metrics
Designed especially for measuring the parallelism usage:
Name
Type
Description
Labels
exec_active_job_count
gauge
Number of active jobs at a time
- action - Action name (e.g. manualSnapshot, retire)
exec_started_job_count_total
counter
Total number of started jobs per executor instance
exec_active_phase_count
Number of active phases for a given action and with
a given name per executor instance
- phase - Phase name (e.g. copySnapshots, reportMetrics)
exec_started_phase_count_total
Total number of started phases for a given action and with
a given name per executor instance
exec_phase_error_count_total
Total number of errors for a given action and phase
per executor instance
### Rate Limiter Metrics
These metrics might be useful for monitoring current pressure:
limiter_inflight_count
Number of in-flight operations
- operation - Operation name (e.g. csiSnapshot, genericCopy)
limiter_pending_count
Number of pending operations
limiter_request_seconds
histogram
Duration in seconds of:
- how long operation wait for the token (label stage = wait)
- how long operation hold the token (label stage = hold)
- stage - This label indicates the essence of the metric.
Can be wait or hold. See description for more details
### Jobs Metrics
These metrics measure the time range
between the creation of the job and its completion:
jobs_completed
Number of finished jobs (the job is considered to be
finished if it has failed, skipped, or succeeded status)
- status - Status name (e.g. succeeded, failed)
jobs_duration
Duration in seconds of completed Veeam Kasten jobs.
- policy_id - Policy ID (e.g. 264aae0e-07ac-4aa5-a38f-aa131c053cbe, UNKNOWN)
The jobs_duration metric is the easiest one for monitoring job status
because it is already aggregated.
This metric captures the running time of jobs that have completed, whether
they succeed or fail.
### Veeam Kasten License Status
Veeam Kasten exports the metering_license_compliance_status metric related
to the cluster's license compliance. This metric contains information on
when the cluster was out of license compliance.
The metering_license_compliance_status metric is a Prometheus gauge,
and has a value of 1 if the cluster's license status is compliant and 0
otherwise. To see the timeline of when Veeam Kasten was out of license
compliance, the metering_license_compliance_status metric can be
queried and graphed.
It is possible to see the peak node usage for the
last two months e.g. by querying node_usage_history{timePeriod="202210"}.
The label format is YYYYMM.
### Veeam Kasten Status Metrics
The state of profiles and policies can be monitored with profiles_count
and policies_count respectively.
profiles_count{type="Location", status="Failed"} reporting a value greater
than 0 would be grounds for further investigation as it would create issues
for any related policies. type="Infra" is also available for Infrastructure
profiles.
policies_count{action="backup", chained="export", status="Failed"} reports
on policies involving both a backup and export that are in a failed state.
### Veeam Kasten Storage Metrics
To check exported storage consumption (Object, NFS or Veeam
Backup & Replication) there is export_storage_size_bytes with types
[logical, physical],
e.g. export_storage_size_bytes{type="logical"}.
The deduplication ratio is calculated by logical / physical.
snapshot_storage_size_bytes, also with logical and physical types,
reports the local backup space utilization.
### Data Transfer Metrics
Metrics are collected for individual snapshot upload and download operation
steps within Veeam Kasten export and import actions.
These metrics differ from those collected for Veeam Kasten actions
because they are captured on a per-volume basis,
whereas Veeam Kasten actions, in general, could involve multiple volume
operations and other activities.
The following data operations metrics are recorded:
Metric Name
data_operation_duration
Histogram
This metric captures the total time taken to complete an operation.
data_operation_normalized_duration
This metric captures the normalized time taken by an operation.
The value is expressed in time/MiB.
Normalized duration values allow comparisons between different
time series, which is not possible for duration metric values
due to the dependency on the amount of data transferred.
data_operation_bytes
Counter
This metric counts the bytes transferred by an operation, and is
typically used to compute the data transfer rate.
Note: This metric is not collected for Download operations involving
the Filesystem export mechanism.
data_operation_volume_count
Gauge
This metric counts the number of volumes involved in an operation.
It is set to 1 at the beginning of an operation and changes to 0
upon completion.
When aggregated, it displays the total number of volumes being
transferred over time.
The following labels are applied to the operation metrics:
Label Name
operation
The type of operation: one of Upload or Download
repo_type
The type of LocationProfile
object that identifies the storage repository:
one of ObjectStore, FileStore or VBR.
repo_name
The name of the LocationProfile
object that identifies the storage repository.
data_format
The export mechanism used:
one of Filesystem or Block.
namespace
The namespace of the application involved.
pvc_name
The name of the PVC involved.
storage_class
The storage class of the PVC involved.
Upload operation metrics do not include the time taken
to snapshot the volumes or the time to upload the action's metadata.
However, they do include the time taken to instantiate a
PersistentVolume from a snapshot when needed.
Similarly, Download operation metrics do not involve the allocation
of the PersistentVolume or the node affinity enforcement steps.
Some query examples:
When a Veeam Backup Repository is involved,
additional metrics are recorded:
data_upload_session_duration
This metric captures the total time taken for an upload session.
data_upload_session_volume_count
This metric counts the number of volumes in an upload session.
When aggregated, it shows the total number of volumes across
all upload sessions over time.
The following labels are applied to the upload session metrics:
The type of LocationProfile
object that identifies the storage repository: VBR.
A query example:
### Veeam Kasten Multi-Cluster Metrics
The Multi-Cluster primary instance exports the following metrics
collected from all clusters within the multi-cluster system.
Use the cluster label with cluster name as the value to query metrics
for an individual cluster.
For example, to query the number of successful actions in the past 24 hours:
### Policy Metrics
mc_policies_count
Number of policies in cluster
- cluster - Cluster name
mc_compliance_count
Number of namespaces by compliance state.
See Veeam Kasten Compliance Metrics about exclusions
- state - Compliance state (e.g. Compliant, NotCompliant, Unmanaged)
### Action Metrics
mc_action_ended_count
Number of actions that have ended
- state - Terminal state (e.g. cancelled, failed, succeeded)
mc_action_skipped_count
Number of actions that were skipped
### Storage Metrics
mc_export_storage_physical_size_bytes
Exported storage consumption in bytes
mc_snapshot_storage_physical_size_bytes
Local backup space utilization in bytes
### Using Externally Installed Grafana
This document can be followed to install a separate instance of Grafana and
setup Veeam Kasten Grafana dashboard, alerts into that.
### Configuring Grafana's URL
Once a separate instance of Grafana is installed on the Cluster, its URL can be
configured, using the Helm field below, while installing Veeam Kasten to make
it easier to access Grafana from Veeam Kasten's dashboard.
### Accessing Grafana from Veeam Kasten's dashboard
Click on the "Data Usage" card on Veeam Kasten's dashboard.
Click on "More Charts and Alerts" to access the instance of Grafana installed
with Veeam Kasten.
### Charts and Graphs
The Grafana dashboard can be used to monitor how many application scoped or
cluster scoped actions (backup, restore, export and import)
have completed, failed or been skipped.
It shows the number of policy runs that have completed or been skipped.
The amount of disk space consumed and the percentage of free space
available in Veeam Kasten's stateful services (catalog, jobs, and logging)
are also shown.
The Data reduction section provides graphs which show the amount
of data being transferred
(e.g, when the new volume has been exported it will be close to 100%,
as all data needs to be transferred,
but with an unchanged volume it will be 0%
since most of the data has already been exported):
The Veeam Kasten System Resource Usage section
provides CPU/Memory usage graphs specific to Veeam Kasten and metrics
that describe task execution performance:
The Data transfer operations section provides graphs on
the transfer of data to and from storage repositories
that are captured by the
data transfer metrics
described above.
The column on the left is organized by storage class,
location profile, and the
export mechanism used.
The upper panel displays the normalized duration
of transfer operations, while the lower panel shows
the data transfer rate.
(The normalized duration expresses the time taken to
transfer one MiB of data, and hence is comparable between
the different time series displayed in the panel).
The column on the right is organized by individual
PVC and data format used, with the upper panel
showing the actual duration of individual operations
and the lower panel showing the transfer rate.
All panels have an overlay that displays the number of volume
operations in progress.
In addition, if VBR is used, the number of volumes
involved in VBR upload sessions will be shown
in a shaded area.
### Grafana Alerts
Grafana can be used to create alerts to get notified moments after
something unexpected happens in your system. An alert can be generated by
specifying a condition or evaluation criteria and, these conditions
can be configured using Alert rules.
Each rule uses a query that fetches data from a data source.
Each query involves a metric such as the Veeam Kasten metrics described
in a previous section.
More can be read about this by following the
Grafana Alerting documentation.
There are three main constructs that are involved while creating alerts
in Grafana:
### Alert rules
The condition on which the alerts should be fired can be configured using alert
rules.
A new alert rule can be created by going to the dashboard's edit option and
then clicking on the Alert tab at the bottom of the page. In this
example, it's assumed that a dashboard panel named Dashboard Local
is already created.
Once there, the Create alert rule from this panel button can be used
to set the query and alert condition for this alert rule. Configure the
datasource that should be used in this alert and the metric that should
be queried.
In this example, datasource Prometheus and metric
action_backup_ended_overall were used.
After setting the query and alert condition, the label of this alert
rule can be configured by scrolling down the same page, until Notifications
options.
Labels are useful to configure where these alerts are going to be sent.
In this example, the labels team:operations and
resource:backup have been used.
Click on Save and Exit to save the dashboard with this alert rule and
exit.
### Contact Points
Contact points are used to configure the communication medium for the
alerts that are going to be generated. For example, in some scenarios,
it might be useful to get a slack message as soon as an alert is fired.
In that case, slack must be configured as a contact point. To see a list
of all the contact point types, refer to this
Grafana documentation.
A contact point can be configured by going to the Alerting dashboard and
then clicking on New contact point under the Contact points tab.
In the example below, slack has been chosen as the contact point type.
### Notification Policies
Once the alerts rule and contact points have been configured, the
relationship between these two configurations is established by
creating a Notification policy.
A notification policy can be configured by going to the Alerting
dashboard and then clicking on New specific policy under the
Notification policies tab.
The example below uses the same labels specified while creating
the alert rule in the previous step.
When an alert is generated based on the rule configured,
notifications will be sent to the slack channel.
### Integrating External Prometheus with Veeam Kasten
To integrate external Prometheus with Veeam Kasten, set the flags
global.prometheus.external.host and global.prometheus.external.port.
If external Prometheus is setup with a base URL, set the
global.prometheus.external.baseURL flag. Make sure RBAC was enabled
while setting up external Prometheus to enable target discovery.
It's also possible to disable kasten built-in prometheus by setting the flag
prometheus.server.enabled: false
### Scrape Config
Update the Prometheus scrape configuration by adding two additional targets.
It is possible to obtain those targets from Veeam Kasten's Prometheus'
configuration, if Prometheus was installed with Veeam Kasten, you should
skip job:prometheus. (Note. yq utility is needed
to execute commands successfully)
The targets will show up after adding the scrape config. Note that the targets
will not be scraped until a network policy is added.
### Network Policy
Once the scrape config is in place, the targets will be discovered
but Prometheus won't be able to scrape them as Veeam Kasten has strict
network policies for inter-service communication. To enable communication
between external Prometheus and Veeam Kasten, a new network policy should
be added as follows.
Add a label to the namespace where external Prometheus is installed -
kubectl label namespace/prometheus app=prometheus and apply
the following network policy to enable communication.
Once the network policy enables communication, all the service targets will
start coming up and the metrics will be scraped.
### Generating Reports
Veeam Kasten Reporting provides regular insights into key performance and
operational states of the system. It uses prometheus to obtain information
about action runs and storage consumption. For more information about
Veeam Kasten Reporting, see Reporting
### Integration with External Tools
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_footprint.md
## Resource Requirements
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
Requirement Types
Requirement Guidelines
Configuring Veeam Kasten Resource Usage for Core Pods
Prometheus Pod's Resources
Configuring Veeam Kasten Resource Usage for Worker Pods
Configuring Cluster-Wide Worker Pod Resource Usage
Configuring Granular Worker Pod Resource Usage
Worker Pod Resource Usage Configuration Priority
Configuring Metric Sidecar Resource Usage for Worker Pods
- Requirement Types
- Requirement Guidelines
- Configuring Veeam Kasten Resource Usage for Core Pods
Prometheus Pod's Resources
- Prometheus Pod's Resources
- Configuring Veeam Kasten Resource Usage for Worker Pods
Configuring Cluster-Wide Worker Pod Resource Usage
Configuring Granular Worker Pod Resource Usage
Worker Pod Resource Usage Configuration Priority
Configuring Metric Sidecar Resource Usage for Worker Pods
- Configuring Cluster-Wide Worker Pod Resource Usage
- Configuring Granular Worker Pod Resource Usage
- Worker Pod Resource Usage Configuration Priority
- Configuring Metric Sidecar Resource Usage for Worker Pods
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Resource Requirements
Veeam Kasten's resource requirements are almost always related to
the number of applications in your Kubernetes cluster and the kind
of data management operations being performed (e.g., snapshots
vs. backups).
Some of the resource requirements are static (base resource
requirements) while other resources are only required when certain
work is done (dynamic resource requirements). The auto-scaling nature
of Veeam Kasten ensures that resources consumed by dynamic
requirements will always scale down to zero when no work is being
performed.
While the below recommendations for both requests and limits should be
applicable to most clusters, it is important to note that the final
requirement will be a function of your cluster and application scale,
total amount of data, file size distribution, and data churn rate. You
can always use Prometheus or Kubernetes Vertical Pod Autoscaling (VPA)
with updates disabled to check your particular requirements.
### Requirement Types
- Base Requirements: These are the core resources needed for Veeam
Kasten's internal scheduling and cleanup services, which are
mostly driven by monitoring and catalog scale requirements.
The resource footprint for these base requirements is usually
static and generally does not noticeably grow with either a
growth in catalog size (number of   Kubernetes resources protected)
or number of applications protected.
- Disaster Recovery: These are the resources needed to perform a
DR of the Veeam Kasten install and are predominantly used to compress,
deduplicate, encrypt, and transfer the Veeam Kasten catalog to object
storage. Providing additional resources can also speed up the DR
operation. The DR resource footprint is dynamic and scales down to
zero when a DR is not being performed.
- Backup Requirements: Resources for backup are required when data
is transferred from volume snapshots to object storage or NFS file storage.
While the backup requirements depend on your data, churn rate, and
file system layout, the requirements are not unbounded and can easily
fit in   a relatively narrow band. Providing additional resources can also
speed up backup operations. To prevent unbounded parallelism when
protecting a large number of workloads, Veeam Kasten bounds the number of
simultaneous backup jobs (default 9). The backup resource footprint
is dynamic and scales down to zero when a backup is not being
performed.
### Requirement Guidelines
The below table lists the resource requirements for a Veeam Kasten install
protecting 100 applications or namespaces.
It should be noted that DR jobs are also included in the maximum
parallelism limit (N) and therefore you can only have N
simultaneous backup jobs or N-1 simultaneous backup jobs
concurrently with 1 DR job.
Type
Requested CPU (Cores)
Limit CPU (Cores)
Requested Memory (GB)
Limit Memory (GB)
Base
1
2
4
DR
0.3
Dynamic (per parallel job)
0.4
Total
3
1.8
4.8
Note
Kasten temporarily consumes approximately
3GB of ephemeral storage on a worker node for each
concurrent volume export or restore operation.
Default worker node storage configuration can
vary based on distribution. Configuring worker nodes
with 100GB of storage is recommended to
prevent interruptions to Kasten operations.
### Configuring Veeam Kasten Resource Usage for Core Pods
Using Helm values, resource requests and limits can be set for
the core Pods that make up Veeam Kasten's base requirements. Kubernetes
resource management is at the container level, so in order
to set resource values, you will need to provide both the deployment
and container names. Custom resource usage can be set through
Helm in two ways:
- Providing the path to one or more YAML files during
helm install or helm upgrade with the --values flag:
resources:
  <deployment-name>:
    <container-name>:
      requests:
        memory: <value>
        cpu: <value>
      limits:
        memory: <value>
        cpu: <value>
Note
See Resource units in Kubernetes
for details on how to specify valid memory and CPU values.
For example, this file will modify the settings for the
catalog-svc container, upgrade-init init container, and kanister-sidecar sidecar container,
which runs in the pod created by the catalog-svc deployment:
resources:
  catalog-svc:
    catalog-svc:
      requests:
        memory: "1.5Gi"
        cpu: "300m"
      limits:
        memory: "3Gi"
        cpu: "1"
    upgrade-init:
      requests:
        memory: "120Mi"
        cpu: "100m"
      limits:
        memory: "360Mi"
        cpu: "300m"
    kanister-sidecar:
      requests:
        memory: "800Mi"
        cpu: "250m"
      limits:
        memory: "950Mi"
        cpu: "900m"
- Modifying the resource values one at a time with the
--set flag during helm install or helm upgrade:
--set=resources.<deployment-name>.<container-name>.[requests|limits].[memory|cpu]=<value>
For the equivalent behavior of the example above, the following values
can be provided:
--set=resources.catalog-svc.catalog-svc.requests.memory=1.5Gi \
--set=resources.catalog-svc.catalog-svc.requests.cpu=300m \
--set=resources.catalog-svc.catalog-svc.limits.memory=3Gi \
--set=resources.catalog-svc.catalog-svc.limits.cpu=1 \
--set=resources.catalog-svc.upgrade-init.requests.memory=120Mi \
--set=resources.catalog-svc.upgrade-init.requests.cpu=100m \
--set=resources.catalog-svc.upgrade-init.limits.memory=360Mi \
--set=resources.catalog-svc.upgrade-init.limits.cpu=300m \
--set=resources.catalog-svc.kanister-sidecar.requests.memory=800Mi \
--set=resources.catalog-svc.kanister-sidecar.requests.cpu=250m \
--set=resources.catalog-svc.kanister-sidecar.limits.memory=950Mi \
--set=resources.catalog-svc.kanister-sidecar.limits.cpu=900m
Providing the path to one or more YAML files during
helm install or helm upgrade with the --values flag:
See Resource units in Kubernetes
for details on how to specify valid memory and CPU values.
For example, this file will modify the settings for the
catalog-svc container, upgrade-init init container, and kanister-sidecar sidecar container,
which runs in the pod created by the catalog-svc deployment:
Modifying the resource values one at a time with the
--set flag during helm install or helm upgrade:
For the equivalent behavior of the example above, the following values
can be provided:
When adjusting a container's resource limits or requests, if any setting
is left empty, the Helm chart will assume it should be unspecified. Likewise,
providing empty settings for a container will result in no limits/requests
being applied.
For example, the following Helm values file will yield no specified resource
requests or limits for the kanister-sidecar container and only a CPU
limit for the jobs-svc container, which runs in the pod
created by the jobs-svc deployment:
### Prometheus Pod's Resources
Resource requests and limits can be added to the Prometheus
pod through Prometheus child Helm charts values.
Custom resource usage can be set through Helm in two ways:
- Providing the path to one or more YAML files during
helm install or helm upgrade with the --values flag:
prometheus:
  server:
    resources:
      requests:
        memory: <value>
        cpu: <value>
      limits:
        memory: <value>
        cpu: <value>
  configmapReload:
    prometheus:
      resources:
        requests:
          memory: <value>
          cpu: <value>
        limits:
          memory: <value>
          cpu: <value>
- Modifying the resource values one at a time with the
--set flag during helm install or helm upgrade:
--set=prometheus.server.resources.[requests|limits].[memory|cpu]=<value> \
--set=prometheus.configmapReload.prometheus.resources.[requests|limits].[memory|cpu]=<value>
### Configuring Veeam Kasten Resource Usage for Worker Pods
By default, Veeam Kasten does not assign resource requests or limits
to temporary worker Pods. This allows Pods responsible for data
movement during backup or restore operations to scale up as needed
to ensure timely completion. If explicit resource settings are required
in the environment, see the available methods below.
### Configuring Cluster-Wide Worker Pod Resource Usage
Using Helm values, resource requests and limits can be set for the
temporary worker Pods created by Veeam Kasten to perform operations.
This method will set the same requests and limits for all injected
Kanister sidecar containers used for Generic Volume Backup,
as well as all other temporary worker Pods provisioned by Veeam Kasten.
As it may be undesirable to configure the same requests and limits for
all temporary worker Pods across all applications, a granular alternative is
described in the following section.
Veeam Kasten affinity-pvc-group- Pods have fixed
resource requests and limits that cannot be modified. These Pods
are used only for PVC/node placement prior to data restore and
do not require customization based on workload.
If namespace level resource limitations have been configured
using LimitRange or ResourceQuota, the values below may be prevented
from being applied or result in failure of the operation. Make sure
resources are specified taking those restrictions into consideration.
Cluster-wide resource requests and limits for Veeam Kasten worker Pods
can be applied through Helm in two ways:
- Providing the path to one or more YAML files during
helm install or helm upgrade with the --values flag:
genericVolumeSnapshot:
  resources:
    requests:
      memory: <value>
      cpu: <value>
    limits:
      memory: <value>
      cpu: <value>
- Modifying the resource values one at a time with the
--set flag during helm install or helm upgrade:
--set=genericVolumeSnapshot.resources.[requests|limits].[memory|cpu]=<value>
### Configuring Granular Worker Pod Resource Usage
The following approach allows for specifying granular resource requests
and limits for different types of Veeam Kasten worker Pods, as well as
allowing configuration on a per application basis. The purpose is to
accommodate "right-sizing" across different application profiles within
a single cluster, rather than sizing all worker Pods based on the
data mover requirements of the largest applications.
Granular resource configuration uses the Veeam Kasten-specific custom
resources, ActionPodSpec and ActionPodSpecBinding. An ActionPodSpec
specifies the Pod categories and their associated request and limit values.
An ActionPodSpec resource may be applied to a specific namespace using
an ActionPodSpecBinding, or may be applied via reference within a policy.
An ActionPodSpec can be created in any namespace and
may be cross referenced from other namespaces.
An ActionPodSpecBinding must be created in application namespace to
which the referenced ActionPodSpec is being applied.
To enable granular resource control,
set the Helm flag workerPodCRDs.enabled to true.
You can also define a default ActionPodSpec during installation.
This will have the lowest priority and will be used if there
is no ActionPodSpec defined for the namespace or action.
### Examples
An ActionPodSpec with an explicit resource configuration
for the export-volume-to-repository Pod type and a default
configuration for all other temporary worker Pods:
An ActionPodSpecBinding applying an ActionPodSpec to
the temporary worker Pods within a specific namespace:
Alternatively, a Policy referencing an ActionPodSpec to
affect temporary worker Pod resources provisioned as part of the
backup action:
### Action Pod Types
This list contains Pod types that are affected by the specified settings.
Typically, Pod types are associated with specific operations;
however, on rare occasions,
a single Pod type may be used for several similar operations.
Pod type can also be found in the k10.kasten.io/actionPodType
annotation on worker Pods.
Pod Type Value
Pod Type Description
*
Wildcard value to configure any worker Pods types not explicitly specified
check-repository
Performs checks on a repository during the export process
create-repository
Initializes a backup repository in an export location
delete-block-data-from-repository
Deletes backup data exported using block mode
delete-collection
Deletes the application manifest data associated with a backup
delete-data-from-repository
Deletes backup data exported using the default filesystem mode
export-block-volume-to-repository
Exports a snapshot using block mode
export-volume-to-repository
Exports a snapshot using the default filesystem mode
image-copy
Exports and restores container images from ImageStreams
kanister-job
Created by Blueprint actions to perform custom operations
list-data-from-repository
Lists data in the repository when retiring backups
repository-operations
Performs background operations such as repository scans and maintenance
repository-server
API server used for multiple operations including export, restore, and import
restore-block-volume-from-repository
Restores a volume exported using block mode
restore-data-dr
Restores Veeam Kasten from a Disaster Recovery backup
restore-data-from-repository
Restores a volume exported using the default filesystem mode
upgrade-repository
Upgrades the repository
validate-repository
Validates a remote repository when restoring a Disaster Recovery backup
### Worker Pod Resource Usage Configuration Priority
The cluster-wide genericVolumeSnapshot Helm setting holds the
lowest priority and will be overridden by any applied ActionPodSpec.
ActionPodSpec resources that are bound to a namespace using an
ActionPodSpecBinding hold a lower priority than an ActionPodSpec
explicitly specified as part of a policy. ActionPodSpec
configurations from multiple sources are not merged;
therefore, it is not possible to apply namespace-bound
resources to one type of Pod and policy-specific resources to another.
It is possible to override resources of worker pods globally through the
Kanister Pod Override,
but this approach is not recommended.
### Configuring Metric Sidecar Resource Usage for Worker Pods
By default, Veeam Kasten provisions a sidecar container on temporary
worker Pods used to collect metrics to monitor resource utilization.
Using Helm, resource requests and limits can be added to the metric sidecar
container added to worker Pods. This setting is independent of either
method previously detailed for configuring worker Pod resources.
Custom resource requests and limits can be set through Helm in two ways:
- Providing the path to one or more YAML files during
helm install or helm upgrade with the --values flag:
workerPodMetricSidecar:
  resources:
    requests:
      memory: <value>
      cpu: <value>
    limits:
      memory: <value>
      cpu: <value>
- Modifying the resource values one at a time with the
--set flag during helm install or helm upgrade:
--set=workerPodMetricSidecar.resources.[requests|limits].[memory|cpu]=<value>
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_k10tools.md
## Veeam Kasten Tools
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
Authentication Service
Catalog Service
Backup Actions
Kubernetes Nodes
Application Information
Veeam Kasten Primer for Pre-Flight Checks
Veeam Kasten Primer for Upgrades
Veeam Kasten Primer for Storage Connectivity Checks
Veeam Kasten Primer for Storage Integration Checks
CSI Capabilities Check
Direct Cloud Provider Integration Checks
vSphere First Class Disk Integration Check
Veeam Kasten Primer Block Mount Check
Veeam Kasten Primer for Authentication Service Checks
Generic Volume Snapshot Capabilities Check
Veeam Kasten Generic Storage Backup Sidecar Injection
CA Certificate Check
Installation of Veeam Kasten in OpenShift clusters
Extracting OpenShift CA Certificates
Listing vSphere snapshots created by Veeam Kasten
- Authentication Service
- Catalog Service
- Backup Actions
- Kubernetes Nodes
- Application Information
- Veeam Kasten Primer for Pre-Flight Checks
- Veeam Kasten Primer for Upgrades
- Veeam Kasten Primer for Storage Connectivity Checks
- Veeam Kasten Primer for Storage Integration Checks
CSI Capabilities Check
Direct Cloud Provider Integration Checks
vSphere First Class Disk Integration Check
- CSI Capabilities Check
- Direct Cloud Provider Integration Checks
- vSphere First Class Disk Integration Check
- Veeam Kasten Primer Block Mount Check
- Veeam Kasten Primer for Authentication Service Checks
- Generic Volume Snapshot Capabilities Check
- Veeam Kasten Generic Storage Backup Sidecar Injection
- CA Certificate Check
- Installation of Veeam Kasten in OpenShift clusters
- Extracting OpenShift CA Certificates
- Listing vSphere snapshots created by Veeam Kasten
-
- Operating Veeam Kasten
- Veeam Kasten Tools
The k10tools binary has commands that can help with validating if a cluster
is setup correctly before installing Veeam Kasten and for debugging Veeam
Kasten's micro services. The latest version of k10tools can be found here.
Binaries are available for the following operating systems and architectures:
Operating System
x86_84 (amd64)
Arm (arm64/v8)
Power (ppc64le)
Linux
Yes
MacOS
No
Windows
### Authentication Service
The k10tools debug auth sub command can be used to debug
Veeam Kasten's Authentication service when it is setup with Active
Directory or OpenShift based authentication. Provide -d openshift
flag for OpenShift based authentication. It verifies connection to the
OpenShift OAuth server and the OpenShift Service Account token. It
also searches for any error events in Service Account.
### Catalog Service
The k10tools debug catalog size sub command can be used to obtain
the size of K10's catalog and the disk usage of the volume
where the catalog is stored.
### Backup Actions
The k10tools debug backupactions sub command can be used to obtain
the backupactions created in the respective cluster. Use the -o json
flag to obtain more information in the JSON format.
### Kubernetes Nodes
The k10tools debug node sub command can be used to obtain information
about the Kubernetes nodes. Use the -o json flag to obtain more
information in the JSON format.
### Application Information
The k10tools debug applications sub command can be used
to obtain information
about the applications running in given namespace.
Use the -o json flag to obtain more
information in the JSON format
(Note: Right now, JSON format support is only provided for PVCs).
Use -n to provide the namespace.
In case the namespace is not provided, application information
will be
fetched from the default namespace.
e.g. -n kasten-io
### Veeam Kasten Primer for Pre-Flight Checks
The k10tools primer sub command can be used to run pre-flight checks
before installing Veeam Kasten. Refer to the section about
Pre-Flight Checks for more details.
The code block below shows an example of the output when executed on a
Kubernetes cluster deployed in Digital Ocean.
### Veeam Kasten Primer for Upgrades
The k10tools primer upgrade sub command can be used to find the recommended
upgrade path of your Veeam Kasten version and to check there is adequate space to
perform the upgrades. It only provides commands for Helm deployments.
See Upgrading Veeam Kasten for additional details.
This tool requires Internet access to http://gcr.io
### Veeam Kasten Primer for Storage Connectivity Checks
Note
Run k10tools primer storage connect --help command to observe
all supported sub-commands.
The k10tools primer storage connect command family can be used
to check a given storage provider accessibility.
Currently the following storage providers are supported for this
group of checks:
- Azure
- Google Cloud Storage (GCS)
- Portworx (PWX)
- S3 Compatible Storage
- Veeam Backup Server (VBR)
- vSphere
Each sub-command corresponding to a particular storage provider accepts
a configuration file with parameters required for making connection. The
configuration file format can be observed by issuing config-yaml
sub-command in the following way (example is for GCS):
The output below is an example of running GCS connectivity checker:
### Veeam Kasten Primer for Storage Integration Checks
Run k10tools primer storage check --help command to observe
all supported sub-commands.
### CSI Capabilities Check
The k10tools primer storage check csi sub-command can be used to check
a specified CSI storage class is able to carry out snapshot and restoration
activities or report configuration issues if not. It creates a temporary
application to test this.
The command accepts a configuration file in the following format:
The output below is an example of running CSI checker:
### Direct Cloud Provider Integration Checks
The k10tools primer storage check sub-command family allows
checking snapshot/restore capabilities through native API integration
of capable cloud storage providers via direct storage API invocations.
For now the following cloud providers are supported:
- Amazon Elastic Block Store (AWS EBS)
- Azure Persistent Disk
- Google Compute Engine Persistent Disk (GCE PD)
To run a desired check the k10tools primer storage check command
should be appended with either awsebs, or azure, or gcepd
suffix. Each of these sub-commands accepts parameters passed via
configuration files to create a test application performing
snapshot/restore via vendor specific storage APIs. The format of which
sub-command can be observed by executing
k10tools primer storage check <awsebs|azure|gcepd> config-yaml.
Example configuration file format for GCE PD checker:
The output below is an example of running GCE PD provider check:
### vSphere First Class Disk Integration Check
Due to limited functionality provided by vSphere CSI driver Veeam
Kasten has to use both volume provisioning via CSI interface and
manual calling vSphere API for doing snapshots and restores of volumes.
The k10tools primer storage check vsphere sub-command provisions
a First Class Disk (FCD) volume using a CSI storage class and performs
snapshot/restore via vSphere API.
The command accepts a configuration file in the following format
(can be observed by running config-yaml command):
The output below is an example of running vSphere CSI checker:
### Veeam Kasten Primer Block Mount Check
The k10tools primer storage check blockmount sub-command is
provided to test if the PersistentVolumes provisioned by
a StorageClass can be supported in block mode
by Veeam Kasten.
If a StorageClass passes this test then see
Block Mode Exports for how to indicate
this fact to Veeam Kasten.
The checker performs two tests:
1. The kubestr block mount test is used to
verify that the StorageClass volumes can be used with Block
VolumeMounts.
2. If first test succeeds, then a second test is
run to verify that Veeam Kasten can restore block data to such volumes.
This step is performed only if Veeam Kasten does not use provisioner
specific direct network APIs to restore data to a block volume
during import.
Both tests independently allocate and release the Kubernetes resources
they need, and it takes a few minutes for the test to complete.
The checker can be invoked by the k10primer.sh script in a
manner similar to that described in the
Pre-flight Checks:
Alternatively, for more control over the invocation of the checker,
use a local copy of the k10tools program to obtain a
YAML configuration file as follows:
The YAML output should be saved to a file and edited to set the
desired StorageClass. Only the storage_class property is
required; other properties will default to the values displayed
in the output if not explicitly set.
Then run the checker as follows:
The test emits multiple messages as it progresses.
On success, you will see a summary message like this at the end:
On failure, the summary message would look like this:
The checker may produce spurious errors if the StorageClass specifies
the Immediate VolumeBindingMode and the PersistentVolumes
provisioned by the test have different node affinities.
In such a case use a variant of the StorageClass that specifies
the WaitForFirstConsumer VolumeBindingMode instead.
Use the -h flag to get all command usage options.
### Veeam Kasten Primer for Authentication Service Checks
Run k10tools primer auth check --help command
to observe all supported sub-commands.
The k10tools primer auth check sub-command family allows doing
basic sanity checks for 3rd-party authentication services. Currently
it supports checkers for ActiveDirectory/LDAP and OIDC.
Each service specific command accepts required parameters via
a configuration file, format of which can be observed by running
config-yaml sub-command (example is for OIDC checker):
The output below is an example of running OIDC checker:
### Generic Volume Snapshot Capabilities Check
The k10tools primer gvs-cluster-check command can be used to check
if the cluster is compatible for Veeam Kasten Generic Volume Snapshot.
Veeam Kasten Generic backup commands are executed on a pod running
kanister-tools image and checked for appropriate output.
Use -n flag to provide namespace.
By default, kasten-io namespace will be used.
Use -s flag to provide a storageclass for the checks to be run against.
By default, no storage class will be used and the checks will be done using
temporary storage from the node the pod runs on.
Use --service-account flag to specify the service account to be used
by pods during GVS checks. By default, default service
account will be used.
By default, the k10tools command will use the publicly available
kanister-tools image at gcr.io/kasten-images/kanister-tools:<K10 version>.
Since this image is not available in air-gapped environments, to
override the default image, set the KANISTER_TOOLS environment variable
to the kanister-tools image that is available in the air-gapped
environment's local registry.
export KANISTER_TOOLS=<your local registry>/<your local repository name>/kanister-tools:k10-<K10 version>
### Veeam Kasten Generic Storage Backup Sidecar Injection
The k10tools k10genericbackup can be used to make Kubernetes
workloads compatible for K10 Generic Storage Backup by injecting a
Kanister sidecar and setting the forcegenericbackup=true annotation
on the workloads.
### CA Certificate Check
The k10tools debug ca-certificate command can be used to check
if the CA certificate is installed properly in Veeam Kasten.
The -n flag can be used to provide namespace and it
defaults to kasten-io.
More information on
installation
process.
### Installation of Veeam Kasten in OpenShift clusters
The k10tools openshift prepare-install command can be used to
prepare an OpenShift cluster for installation of Veeam Kasten.
It extracts a CA Certificate from the cluster, installs it in
the namespace where Veeam Kasten will be installed, and generates
the helm command to be used for installing Veeam Kasten.
The -n flag can be used to provide the namespace where Veeam
Kasten will be installed. The default namespace is kasten-io.
--recreate-resources flag recreates resources that
may have been created by previous execution of this command.
Set --insecure-ca flag to true if Certificate Issuing
Authority is not trusted.
### Extracting OpenShift CA Certificates
The k10tools openshift extract-certificates command is used to extract
CA certificates from OpenShift clusters to the Veeam Kasten namespace.
The following flags can be used to configure the command:
- --ca-cert-configmap-name. The name of the Kubernetes ConfigMap that
contains all certificates required for Veeam Kasten. If no name is provided,
the default name custom-ca-bundle-store will be used.
If the ConfigMap with the used name does not exist, the command will
generate a new ConfigMap.
If the ConfigMap with the used name exists, the command will merge
newly extracted certificates with the existing certificates
in the ConfigMap without creating duplicates.
- If the ConfigMap with the used name does not exist, the command will
generate a new ConfigMap.
- If the ConfigMap with the used name exists, the command will merge
newly extracted certificates with the existing certificates
in the ConfigMap without creating duplicates.
- --k10-namespace or -n. The Kubernetes namespace where Veeam Kasten
is expected to be installed. The default value is kasten-io.
- --release-name. The K10 Release Name. The default value is k10.
--ca-cert-configmap-name. The name of the Kubernetes ConfigMap that
contains all certificates required for Veeam Kasten. If no name is provided,
the default name custom-ca-bundle-store will be used.
### Listing vSphere snapshots created by Veeam Kasten
Veeam Kasten integrates with the vSphere clusters using direct integration.
Veeam Kasten snapshots can be listed using k10tools.
Only snapshots created starting with version 5.0.7 will be listed
by the current version of the tool.
Earlier snapshots might be listed if they had been created
using a vSphere infrastructure profile with the tagging option enabled
(Deprecated since then).
To list earlier snapshots, k10tools v6.5.0
should be used with an additional environment variable:
## category name can be found from the vSphere infrastructure profile, in the form of "k10:<UUID>"
export VSPHERE_SNAPSHOT_TAGGING_CATEGORY=$(kubectl -n kasten-io get profiles $(kubectl -n kasten-io get profiles -o=jsonpath='{.items[?(@.spec.infra.type=="VSphere")].metadata.name}') -o jsonpath='{.spec.infra.vsphere.categoryName}')
© Copyright 2017-2024, Kasten, Inc.
### latest_operating_external_tools_datadog.md
## Exporting Metrics to Datadog
- Veeam Kasten Disaster Recovery
- API and Command Line
- Monitoring
Using Veeam Kasten's Prometheus Endpoint
Veeam Kasten Metrics
Veeam Kasten Multi-Cluster Metrics
Using Externally Installed Grafana
Integrating External Prometheus with Veeam Kasten
Generating Reports
Integration with External Tools
Exporting Metrics to Datadog
- Using Veeam Kasten's Prometheus Endpoint
- Veeam Kasten Metrics
- Veeam Kasten Multi-Cluster Metrics
- Using Externally Installed Grafana
- Integrating External Prometheus with Veeam Kasten
- Generating Reports
- Integration with External Tools
Exporting Metrics to Datadog
- Exporting Metrics to Datadog
- Auditing Veeam Kasten
- Integrating Security Information and Event Management (SIEM) Systems
- Reporting
- Garbage Collector
- Resource Requirements
- Security Requirements
- Support and Troubleshooting
- Uninstalling Veeam Kasten
- Veeam Kasten Tools
-
- Operating Veeam Kasten
- Monitoring
First off the Datadog agent needs to be installed in the Kubernetes cluster.
Documentation for that is found in the Datadog docs. Make sure to enable
the prometheusScrape option documented in prometheus scrape docs.
Finally, to collect the Veeam Kasten metrics in Datadog, apply the following
values to either the Veeam Kasten install or upgrade (using Helm).
for example, given the above values.yaml file, if doing a helm install,
the command would be:
If doing a helm upgrade to patch your install with the above values,
run the following:
To dive deeper into adding metrics to Datadog see the following documentation
links:
- Kubernetes Prometheus and OpenMetrics metrics collection
- Prometheus Helm Values - Server Pod Annotations
© Copyright 2017-2024, Kasten, Inc.
