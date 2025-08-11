# Usage Documentation

## Usage App Scoped Policies 

Users who are not administrators can create Veeam Kasten policies in an
  application's namespace for protecting only that specific application.
  The image below shows the dashboard as viewed by a non-admin user who
  has access to policies.

For information about setting up RBAC for users of application-scoped
  policies, refer to this page.

## Creating the Policy â

A user who does not have administrator privileges will see a different
  policy creation form compared to an admin user. The main difference is
  in the ability to select the applications that can be protected by such
  a policy. The image below shows that the user is allowed to only select
  a single application.

A Veeam Kasten Policy resource is created in the application's
  namespace.

```
kind: PolicyapiVersion: config.kio.kasten.io/v1alpha1metadata:  name: k10-basic-user-ns-1-pol1  namespace: k10-basic-user-ns-1spec:  frequency: "@hourly"  subFrequency:    minutes:      - 0      - 30      - 55    hours:      - 0    weekdays:      - 0    days:      - 1    months:      - 1  retention:    hourly: 24    daily: 7    weekly: 4    monthly: 12    yearly: 7  selector:    matchExpressions:    - key: k10.kasten.io/appNamespace        operator: In        values:        - k10-basic-user-ns-1  actions:    - action: backup    - action: export    exportParameters:      frequency: "@hourly"      receiveString: exampleReceiveString      profile:        name: profile1        namespace: kasten-io      migrationToken:        name: k10-basic-user-ns-1-pol1-migration-token-n74p8        namespace: kasten-io      exportData:        enabled: true    retention: {}
```

## Profiles â

The users of application-scoped policies require read-only access to
  location profiles. They depend on the administrator for creation of
  profiles. The image below shows the profiles page as seen by such a
  user. The user can list/view the profiles that they have been given
  access to. But they cannot create, edit or delete them. Refer to this page for
  setting up RBAC to provide access to profiles in Veeam Kasten's
  namespace for non-admin users.

## Backups â

When the policy runs, the BackupActions and Restore Points will be
  created in the application's namespace. The image below shows a
  BackupAction. The originating policy indicates that the policy named k10-basic-user-ns-1-pol1 in the namespace named k10-basic-user-ns-1 created this BackupAction.

## Exports â

If the policy is configured to export Restore Points to object storage,
  the ExportAction will be created in the application's namespace. The
  image below shows an ExportAction. The originating policy indicates that
  the policy named tl-pol in the namespace named timelogger created
  this ExportAction.

It is possible to monitor the number of processed volumes and the data
  processed while the export is running via the Action Details view.

- Processed - How much data was checked for changes since the last backup. Data known to be unchanged since the last backup will not be read from disk but will still count as being processed.
- Read - How much data was read from the PVCs of the application.
- Transferred - How much data has been exported after deduplication and compression have been applied.

## Restores â

The non-admin user can restore the application using one of the Restore
  Points created by the application-scoped policy. This image below shows
  an exported Restore Point whose originating policy is an
  application-scoped policy.

In the Optional Restore Settings section of the restore form, the user
  can select Kanister blueprint actions that will run after a successful
  restore. The users of application-scoped policies require read-only
  access to such blueprints. They depend on the administrator for creation
  of blueprints. Refer to this page
  for setting up RBAC to provide access to blueprints in Veeam Kasten's namespace
  for non-admin users.

## Imports â

To ensure Imports function correctly for non-admin users, the Kubernetes
    ValidatingAdmissionPolicy must be enabled in the cluster.
    For more information, visit the Kasten Policy Permissions VAP documentation.

A non-admin user can create a policy using the 'Import and Restore' policy form,
  which automatically restores after import and does not allow restoring
  cluster-scoped resources. The policy must include both an Import action to bring
  in RestorePointContents (RPCs) of an application and a Restore action to
  immediately restore from them, as RPCs are cluster-wide resources that non-admin
  users cannot restore directly.

The image below shows how the 'Create Policy' form will appear for a non-admin
  user, with the 'Import and Restore' option expanded.

The user does not have the ability to specify in-line transforms, but can
  reference existing transform sets to which they have access, as shown in the
  image below.

On creating the policy, its validation occurs in the application namespace and
  can be viewed in the Policies page. In the image below, the Import and Restore
  policy named test-import succeeded validation.

When the policy runs, the Import and Restore Actions will be created in the
  application's namespace and they can be viewed both in the Actions dashboard
  as well as in the Action Details page on expanding on the action. In the
  following image, the status of the completed Import and Restore policy can be
  seen in the non-admin user's view of the Kasten dashboard.

The image below shows how the 'Create Policy' form will appear for a non-admin
  user if the VAP Helm Value has been disabled. The 'Import' option will not be
  expanded to display a form and a tooltip showing 'Insufficient permissions to
  perform imports' will be displayed on hovering over the option.

---

## Usage App Scoped Policies Vap

Kasten introduces support for Kubernetes ValidatingAdmissionPolicies (VAP) to
  deliver more robust user permission controls and secure data operations across
  clusters. This new feature helps minimize administrative overhead, empowers
  namespace and application owners, and maintains strict compliance with
  organizational standards. The result is a more secure, flexible, and efficient
  workflow that aligns with modern Kubernetes best practices. For more details,
  visit the Kubernetes VAP documentation .

By implementing VAP, Kasten enables namespace owners and application-scoped
  users to securely manage critical workflows such as disaster recovery (DR),
  development/testing, and general data migrations. VAPs are configurable using
  the Helm values under the vap section of the Kasten Helm Chart .

Validating admission policies use Common Expression Language (CEL) to declare
  the validation rules of a policy.

## Common Expression Language (CEL) â

The spec.validations[i].expression in the VAP represents the expression that
  will be evaluated by CEL. For more details on CEL syntax, refer to the
  Kubernetes documentation on Validation Expressions.

## Prerequisites and Restrictions â

### Kubernetes 1.31 â

Full GA support for VAP without additional configuration.

## Kasten VAPs â

It is not recommended to modify the existing CEL rules in the VAPs installed
    by Kasten. Modifying the rules will change the security posture of Kasten.

### Kasten Policy Permissions VAP â

The kasten.policy.permissions VAP evaluates permissions for a non-admin user
  while creating a Kasten policy. This prevents unauthorized access to sensitive
  resources and maintains a high level of security compliance across all
  Kasten-driven data operations.

The kasten.policy.permissions.binding VAP binding narrows the scope of the
  VAP to non-admin users who are creating policies outside of the kasten-io namespace.

To enable installation of the VAP and VAP binding, set the vap.kastenPolicyPermissions.enabled value in the Kasten Helm chart to true .

The VAP ensures that the following requirements are maintained for any policy
  created by such a user:

1. The user has access to every Kasten resource (e.g. blueprints, location profiles, transform sets, etc) referenced in any policy.
2. The policy has no in-line transforms.
3. The Import and Restore policy restores only to the application namespace where it is run.
4. The Import and Restore policy does not set the flag to restore cluster resources.

For more information on Import and Restore application-scoped policies created
  by non-admin users, refer to the Imports section under Application-Scoped Policies.

To view the complete set of the CELs in the VAP and the referenced resources
  which they protect, admin users can run the following command:

```
kubectl describe validatingadmissionpolicy kasten.policy.permissions
```

Similarly, to view the logic for the VAP binding, run the following command:

```
kubectl describe validatingadmissionpolicybinding kasten.policy.permissions.binding
```

---

## Usage Clusterscoped

Cluster-scoped resources are Kubernetes resources that are not
  namespaced. Cluster-scoped resources may be part of the Kubernetes
  cluster configuration or may be part of one or more applications. Veeam
  Kasten can protect and restore cluster-scoped resources together with or
  separately from applications.

When Veeam Kasten protects cluster-scoped resources, by default all
  instances of StorageClasses, CustomResourceDefinitions, ClusterRoles,
  and ClusterRoleBindings are captured in a cluster restore point.
  Resource filtering can be used to restrict which cluster-scoped resource
  instances are captured or restored.

## Protecting Cluster-Scoped Resources â

Veeam Kasten protects cluster-scoped resources in the same way that it
  protects applications, with snapshot policies, backups, and manual
  snapshots.

This section demonstrates specifically how to use these to protect
  cluster-scoped resources. Refer to Protecting Applications for
  common policy details such as scheduling, retention, exceptions, and
  resource filtering.

### Snapshot Policies for Cluster-Scoped Resources â

To create a policy that protects only cluster-scoped resources, click Create New Policy on the Policies card, select Snapshot action, None for applications, and toggle Snapshot Cluster-Scoped Resources .

Choose All Cluster-Scoped Resources to snapshot all instances of
  StorageClasses, CustomResourceDefinitions, ClusterRoles, and
  ClusterRoleBindings. Choose Filter Cluster-Scoped Resources to select
  resources to be captured using include and exclude filters.

When this policy runs, it will create a cluster restore point with
  artifacts that capture the state of the cluster-scoped resources.

### Snapshot Policies for Application and Cluster-Scoped Resources â

Some applications have cluster-scoped resources such as StorageClasses
  or CustomResourceDefinitions as well as namespaced components such as
  StatefulSets. To create a policy that protects the entire application,
  create a policy that protects both the application and its associated
  cluster-scoped resources.

When this policy runs, it will create both a restore point for the my-app application and a cluster restore point with artifacts that
  capture the application's cluster-scoped resources.

If the policy sets Enable backups by exporting snapshots , any restore
  points and the cluster restore point will be exported.

### Manual Snapshots of Cluster-Scoped Resources â

Cluster-scoped resources are accessible from the Options menu on the Applications page. A manual snapshot of cluster-scoped
  resources is initiated by clicking on `Snapshot cluster-scoped
  resources`:

This brings up the Snapshot Cluster Resources dialog with options that
  include whether to apply filters. By default all instances of
  StorageClasses, CustomResourceDefinitions, ClusterRoles, and
  ClusterRoleBindings are captured.

## Restoring Cluster-Scoped Resources â

Once cluster-scoped resources have been protected via a policy or a
  manual action, it is possible to restore them from a cluster restore
  point.

To restore cluster-scoped resources from a cluster, select the [Restore
  cluster-scoped resources] in the Options menu.

At this point, one has the option to pick a cluster restore point. As
  seen above, this view distinguishes manually generated restore points
  from automated policy-generated ones.

It also distinguishes between snapshots and backups. When both are
  present, a layered box is shown to indicate more than one kind of
  cluster restore point is present for the same data. Clicking on the
  layered cluster restore point will present an option to select between
  the local snapshot and exported backup.

While the UI uses the Export term for backups, no Import policy is
    needed to restore from a backup. Import policies are only needed when
    you want to restore the application into a different cluster.

Selecting a cluster restore point will bring up a side-panel containing
  more details for you to preview, if needed, before you initiate a
  restore. You may select or deselect artifacts to be restored
  individually or by type. Click Restore to recover the selected
  cluster-scoped resources.

## Import Policies and Cluster-Scoped Resources â

Import polices that import from a location containing a cluster restore
  point will import the cluster restore point as well as any restore
  points in the location. Cluster-scoped resources can be restored
  manually from an imported cluster restore point.

An import policy with the Restore After Import option will import both
  cluster restore points and restore points. The policy will only
  automatically restore cluster-scoped resources if the Restore cluster-scoped resources option is explicitly selected.

---

## Usage Configuration

Veeam Kasten can usually invoke protection operations such as snapshots
  within a cluster without requiring additional credentials. While this
  might be sufficient if Veeam Kasten is running in some of (but not all)
  the major public clouds and if actions are limited to a single cluster,
  it is not sufficient for essential operations such as performing
  real backups, enabling cross-cluster and cross-cloud application
  migration, and enabling DR of the Veeam Kasten system itself.

To enable these actions that span the lifetime of any one cluster, Veeam
  Kasten needs to be configured with access to external object storage or
  external NFS/SMB file storage. This is accomplished via the creation of Location Profiles.

Location Profile creation can be accessed from the Location page of
  the Profiles menu in the navigation sidebar or via the CRD-based Profiles API .

## Location Profiles â

Location profiles are used to create backups from snapshots, move
  applications and their data across clusters and potentially across
  different clouds, and to subsequently import these backups or exports
  into another cluster. To create a location profile, click Create New Profile on the profiles page.

### Object Storage Location â

Support is available for the following object storage providers:

- Amazon S3 or S3 Compatible Storage
- Azure Storage
- Google Cloud Storage
- Veeam Data Cloud Vault

Veeam Kasten creates Kopia repositories in object
  store locations. Veeam Kasten uses Kopia as a data
  mover which implicitly provides support to deduplicate, encrypt and
  compress data at rest. Veeam Kasten performs periodic maintenance on
  these repositories to recover released storage.

#### Amazon S3 or S3 Compatible Storage â

Enter the access key and secret, select the region and enter the bucket
  name. The bucket must be in the region specified. If the bucket has
  object locking enabled then set the Enable Immutable Backups toggle
  (see Immutable Backups for details). If the bucket is using S3 Intelligent-Tiering , only Standard-IA , One Zone-IA and Glacier Instant Retrieval storage classes are supported by Veeam
  Kasten.

An IAM role may be specified for an Amazon S3 location profile by
  selecting the Execute Operations Using an AWS IAM Role button.

If an S3-compatible object storage system is used that is not hosted by
  one of the supported cloud providers, an S3 endpoint URL will need to be
  specified and optionally, SSL verification might need to be disabled.
  Disabling SSL verification is only recommended for test setups.

When a location profile is created, the config profile will be created,
  and a profile similar to the following will appear:

The minimum supported version for NetApp ONTAP S3 is 9.12.1.

#### Azure Storage â

To use an Azure storage location, you are required to pick an Azure Storage Account , a Cloud Enviornment and a Container .

The Container must be created beforehand.

##### Azure Federated Identity â

Veeam Kasten supports authenticating Azure location profiles
  with Azure Federated Identity credentials. An Azure Storage Access Key is not required.
  When using Azure Federated Identity all Azure location profiles will authenticate
  with Federated Identity credentials.

Learn more about installing Openshift on Azure .

#### Google Cloud Storage â

In addition to authenticating with Google Service Account credentials,
  Veeam Kasten also supports authentication with Google Workload Identity
Federation with Kubernetes as the Identity
Provider .

In order to use Google Workload Identity Federation, some additional
  Helm settings are necessary. Please refer to Installing Veeam Kasten with Google Workload Identity Federation for details on how to install Veeam Kasten with these
  settings.

Enter the project identifier and the appropriate credentials, i.e., the
  service key for the Google Service Account or the credential
  configuration file for Google Workload Identity Federation. Credentials
  should be in JSON or PKCS12 format. Then, select the region and enter a
  bucket name. The bucket must be in the specified location.

When using Google Workload Identity Federation with Kubernetes as the
    Identity Provider, ensure that the credential configuration file is
    configured with the format type ( --credential-source-type ) set to Text , and specify the OIDC ID token path ( --credential-source-file )
    as /var/run/secrets/kasten.io/serviceaccount/GWIF/token .

#### Veeam Data Cloud Vault â

A Veeam Data Cloud Vault Repository may be used as the destination for persistent
  volume snapshot data in compatible environments.

Prior to creating a Veeam Data Cloud Vault location profile within Veeam Kasten, a Kasten instance must
  first be registered with Veeam Data Cloud. Visit Settings > Registration to start that process. See Veeam Data Cloud Vault Integration Guide for additional details.

To create a Veeam Data Cloud Vault location profile, select Create New Profile and specify Veeam Data Cloud Vault as the provider type.

Select one of the storage vaults assigned to this Veeam Kasten Backup Server . If you haven't yet
  assigned a storage vault to this registered cluster, you'll have to visit My Account to configure that.
  For more information on that process please visit the Veeam Data Cloud Vault user guide

Upon clicking Submit , the dialog will validate the input data.

If registration has occurred recently, there is a possibility it may take 30
    minutes to propagate. Please wait or come back and try again later if location
    profile validation fails and you've recently configured the registration or
    vault assignment steps.

All Veeam Vault locations are configured as immutable; follow these instructions to
  learn more about configuration within Veeam Kasten.

##### Considerations   â

The following limitations should be considered when exporting
  data from Veeam Kasten to Veeam Vault:

- Veeam Vault is a generic object storage repository
- All Veeam Vault exports are immutable.
- Data captured in Veeam Vault remains (and continues to incur charges) until the retention period expires, even if the location profile is removed from a Kasten installation.
- While Veeam Vault can be used to protect kubernetes data from any on-premises or cloud environment, when running in Azure Veeam highly recommends the Kasten cluster be located in the same Azure region as the Veeam Vault storage account to limit possible ingress and egress data charges
- Removing the Veeam Vault location profile will not remove any data from Veeam Vault and prevents Kasten from running future cleanup actions.

### File Storage Location â

You can use either NFS or SMB file storage as a location profile. The setup process for each is described below.

To avoid issues on NFS/SMB servers with limited storage, new exports are prevented from starting when storage is 95% full. Veeam Kasten automatically recovers storage as it cleans up expired snapshots, but reaching this state may signal a need to update retention settings or expand storage.

#### NFS File Storage â

Requirements:

- An NFS server reachable from all nodes where Veeam Kasten is installed.
- An exported NFS share, mountable on all nodes.
- A PersistentVolume (PV) and PersistentVolumeClaim (PVC) in the Veeam Kasten namespace.

Steps:

Specification details will vary based on environment. Consult Kubernetes distribution documentation for additional details on configuring NFS connections.

1. Create a PersistentVolume for the NFS share: apiVersion : v1 kind : PersistentVolume metadata : name : nfs - pv spec : capacity : storage : 10Gi volumeMode : Filesystem accessModes : - ReadWriteMany persistentVolumeReclaimPolicy : Retain storageClassName : "" mountOptions : - hard - nfsvers=4.1 nfs : path : / server : 172.17.0.2
2. Create a PersistentVolumeClaim in the Veeam Kasten namespace: apiVersion : v1 kind : PersistentVolumeClaim metadata : name : test - pvc namespace : kasten - io spec : storageClassName : "" volumeName : nfs - pv accessModes : - ReadWriteMany resources : requests : storage : 10Gi
3. Create an NFS/SMB Location Profile referencing the previously created PVC:

Create a PersistentVolume for the NFS share:

```
apiVersion: v1kind: PersistentVolumemetadata:   name: nfs-pvspec:   capacity:      storage: 10Gi   volumeMode: Filesystem   accessModes:      - ReadWriteMany   persistentVolumeReclaimPolicy: Retain   storageClassName: ""   mountOptions:      - hard      - nfsvers=4.1   nfs:      path: /      server: 172.17.0.2
```

Create a PersistentVolumeClaim in the Veeam Kasten namespace:

```
apiVersion: v1kind: PersistentVolumeClaimmetadata:   name: test-pvc   namespace: kasten-iospec:   storageClassName: ""   volumeName: nfs-pv   accessModes:      - ReadWriteMany   resources:      requests:         storage: 10Gi
```

Create an NFS/SMB Location Profile referencing the previously created PVC:

By default, Veeam Kasten uses the root user to access the NFS location profile. To use a different user, set the Supplemental Group and Path fields. The Path must refer to a directory within the PVC, and the group must have read, write, and execute access.

#### SMB File Storage â

- An SMB server reachable from all nodes where Veeam Kasten is installed.
- An exported SMB share, mountable on all nodes.
- A PersistentVolume (PV) and PersistentVolumeClaim (PVC) in the Veeam Kasten namespace (default: kasten-io ).

The following example is specific to Red Hat OpenShift and the smb.csi.k8s.io storage provisioner. For other Kubernetes distributions or provisioners, consult the appropriate documentation.

1. Create a PersistentVolume for the SMB share: apiVersion : v1 kind : PersistentVolume metadata : annotations : pv.kubernetes.io/provisioned-by : smb.csi.k8s.io name : smb - pv spec : capacity : storage : 100Gi accessModes : - ReadWriteMany persistentVolumeReclaimPolicy : Retain storageClassName : "" mountOptions : - dir_mode=0777 - file_mode=0777 csi : driver : smb.csi.k8s.io volumeHandle : smb - server.default.svc.cluster.local/share # volumeAttributes : source : //<hostname > /<shares > nodeStageSecretRef : name : smbcreds namespace : samba - server
2. Create a Secret for SMB credentials: apiVersion : v1 kind : Secret metadata : name : smbcreds namespace : samba - server stringData : username : <username > password : <password > volumeHandle : Unique identifier for the volume. volumeAttributes.source : UNC path to the SMB share. nodeStageSecretRef : References the Secret with SMB credentials.
3. Create a PersistentVolumeClaim in the Veeam Kasten namespace: apiVersion : v1 kind : PersistentVolumeClaim metadata : name : test - pvc namespace : kasten - io spec : storageClassName : "" volumeName : smb - pv accessModes : - ReadWriteMany resources : requests : storage : 10Gi
4. Create an NFS/SMB Location Profile referencing the previously created PVC:

Create a PersistentVolume for the SMB share:

```
apiVersion: v1kind: PersistentVolumemetadata:  annotations:    pv.kubernetes.io/provisioned-by: smb.csi.k8s.io  name: smb-pvspec:  capacity:    storage: 100Gi  accessModes:    - ReadWriteMany  persistentVolumeReclaimPolicy: Retain  storageClassName: ""  mountOptions:    - dir_mode=0777    - file_mode=0777  csi:    driver: smb.csi.k8s.io    volumeHandle: smb-server.default.svc.cluster.local/share#    volumeAttributes:      source: //<hostname>/<shares>    nodeStageSecretRef:      name: smbcreds      namespace: samba-server
```

Create a Secret for SMB credentials:

```
apiVersion: v1kind: Secretmetadata:  name: smbcreds  namespace: samba-serverstringData:  username: <username>  password: <password>
```

- volumeHandle : Unique identifier for the volume.
- volumeAttributes.source : UNC path to the SMB share.
- nodeStageSecretRef : References the Secret with SMB credentials.

```
apiVersion: v1kind: PersistentVolumeClaimmetadata:   name: test-pvc   namespace: kasten-iospec:   storageClassName: ""   volumeName: smb-pv   accessModes:      - ReadWriteMany   resources:      requests:         storage: 10Gi
```

By default, Veeam Kasten uses the root user to access the SMB location. To use a different user, set the Supplemental Group and Path fields. The Path must refer to a directory within the PVC, and the group must have read, write, and execute access.

### Veeam Repository Location â

A Veeam Repository may be used as the destination for persistent
  volume snapshot data in compatible environments. See Storage Integration for additional details.

Prior to creating a Veeam Repository location profile within
  Veeam Kasten, a Kasten instance must first be configured on the
  target VBR backup server. See Veeam Kasten Integration Guide for additional details.

To create a Veeam Repository location profile, select Create New Profile and specify Veeam Repository as the
  provider type.

Provide the DNS name or the IP address of the Veeam backup server in the Veeam Backup Server field. The Veeam Backup Server API Port field is
  pre-configured with the installation default value and may be changed if
  necessary. Specify the name of a backup repository on this server in the Backup Repository field.

Using more than one unique VBR backup server per Veeam Kasten instance
    is not supported and may cause synchronization issues between
    Veeam Kasten and VBR. Creating multiple location profiles connecting
    to different instances of VBR will produce a warning and should only
    be performed during temporary reconfiguration of an environment.

Provide access credentials in the Username and Password fields.

Ensure Access Permissions are granted within VBR for the specified
    account (or related security group) and backup repository. See Veeam Kasten
Integration Guide for details.

Upon clicking Submit , the dialog will validate the input data.
  Communication with the server uses SSL and requires that the server's
  certificate be trusted by Veeam Kasten. Alternatively, enabling the Skip certificate chain and hostname verification option disables
  certificate validation.

If using an immutable Veeam Repository, follow these instructions to
  ensure proper configuration within Veeam Kasten.

## Location Settings for Migration â

If the location profile is used for exporting an application for
  cross-cluster migration, it will be used to store application restore
  point metadata and, when moving across infrastructure providers, bulk
  data too. Similarly, location profiles are also used for importing
  applications into a cluster that is different than the source cluster
  where the application was captured.

In case of NFS/SMB File Storage Location, the exported NFS/SMB share must be
    reachable from the destination cluster and mounted on all the nodes
    where Veeam Kasten is installed.

## Read-Only Location Profile â

Veeam Kasten supports read-only location profiles for import and restore operations. These profiles require no write permissions, as the system performs only read operations during these phases.

Read-only profiles can only be used for import and restore operations. Attempting to use them for backup or export operations will result in an error.

This configuration is particularly useful when:

- Working with immutable backups
- Implementing strict security policies
- Accessing shared backup repositories

## Immutable Backups â

The frequency of ransomware attacks on enterprise customers is
  increasing. Backups are essential for recovering from these attacks,
  acting as a first line of defense for recovering critical data.
  Attackers are now targeting backups as well, to make more difficult, if
  not impossible for their victims to recover.

Veeam Kasten can leverage object-locking and immutability features
  available in many object store providers to ensure its exported backups
  are protected from tampering. When exporting to a locked bucket, the
  restore point data cannot be deleted or modified within a set period,
  even with administrator privileges. If an attacker obtains privileged
  object store credentials and attempts to disrupt the backups stored
  there, Veeam Kasten can restore the protected application by reading
  back the original, immutable and unadulterated restore point.

Immutable backups are supported for AWS S3 and other S3 compatible
  object stores. Additionally, they are supported for Azure and Google .

More information on the full Immutable Backups Workflow .

The generic storage and shareable volume backup and restore workflows are not compatible with the protections
    afforded by immutable backups. Use of a location profile enabled for
    immutable backups can be used for backup and restore, but the protection
    period is ignored, and the profile is treated as a
    non-immutability-enabled location. Please note that using an
    object-locking bucket for such use cases can amplify storage usage
    without any additional benefit. Please contact support for any inquiries.

### S3 Locked Bucket Setup â

To prepare Veeam Kasten to export immutable backups, a bucket must be
  prepared in advance.

- The bucket must be created on AWS S3 or an S3 compatible object store.
- The bucket must be created with object locking enabled. Note: On some S3-compatible implementations, the object locking property of a bucket can only be enabled/configured at bucket creation time.

A sample Minio CLI mc script that will set up an
  immutable-backup-eligible locked bucket in AWS S3:

```
## Set up the following variables:BUCKET_NAME=<choose a unique bucket name>REGION=<pick the region for the bucket>AWS_ACCESS_KEY_ID=<access key ID>AWS_SECRET_ACCESS_KEY=<secret access key>## Alias the s3 account credentialsmc alias set s3 https://s3.amazonaws.com ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY}## Make the bucket with locking enabledmc mb --region=${REGION} s3/${BUCKET_NAME} --with-lock
```

For more information on setting up object-locking: * Using S3 Object
Lock

### Profile Creation â

Once a bucket has been prepared with each of these requirements met, a
  profile can be created from the Veeam Kasten dashboard to point to it.

Follow the steps for setting up a profile as normal. Enter a profile
  name, object store credentials, region, and bucket name.

It is recommended that the credentials provided to access the locked
  bucket are granted minimal permissions only:

- List objects
- List object versions
- Determine if bucket exists
- Get object lock configuration
- Get bucket versioning state
- Get/Put object retention
- Get/Put/Remove object
- Get object metadata

See Using Veeam Kasten with AWS S3 for a list of required permissions.

After selecting the checkbox labeled "Enable Immutable Backups" a new
  button labeled "Validate Bucket <bucket-name>" will appear. Click
  the Validate Bucket button to initiate a series of checks against the
  bucket, verifying the bucket can be reached and meets all of the
  requirements denoted above. All conditions must be met for the check to
  succeed and for the profile form to be submitted.

If the provided bucket meets all of the conditions, a Protection Period
  slider will appear. The protection period is a user-selectable time
  period that Veeam Kasten will use when maintaining an ongoing immutable
  retention period for each exported restore point. A longer protection
  period means a longer window in which to detect, and safely recover
  from, an attack; backup data remains immutable and unadulterated for
  longer. The trade-off is increased storage costs, as potentially stale
  data cannot be removed until the object's immutable retention expires.

Veeam Kasten limits the maximum protection period that can be selected
  to 90 days. A safety buffer is added to the desired protection period.
  This is to ensure Veeam Kasten can always find and maintain ongoing
  protection of any new objects written to the bucket before their
  retention lapses. The minimum protection period is 1 day.

Click the "Submit" button. The profile will be submitted to Veeam
  Kasten and appear in the Location Profiles list. The dedicated view page
  will reflect the object immutability status of the referenced bucket, as
  well as the selected protection period.

### Protecting applications with Immutable Backups â

Selecting the locked bucket profile as the Export Location Profile in
  the Backups procedure will
  render all application data immutable for the duration of the protection
  period. Additionally, to ensure Veeam Kasten can restore that
  application data, Veeam Kasten should also be protected with an
  immutable locked-bucket Disaster Recovery (DR) profile.

In a situation where the cluster and/or object store has been corrupted,
  attacked, or otherwise tampered with, Veeam Kasten might be just as
  susceptible to being compromised as any other application. Protecting
  both (apps and Veeam Kasten) with immutable locked-bucket profiles will
  ensure the data is intact, and that Veeam Kasten knows how to restore
  it. Therefore, if one or more locked bucket location profiles are being
  used to back up and protect vital applications, it is highly recommended
  that a locked bucket profile should also be used with Veeam Kasten DR.

When setting up a location profile for Veeam Kasten DR, one should
  choose a protection period that is AT LEAST as long as the longest
  protection period in use for application backups. For example if one
  application is being backed up using a profile with a 1 week protection
  period, and another using a 1 year protection period, the protection
  period for the Veeam Kasten DR backup profile should be at least 1 year
  to ensure the latter application can always be recovered by Veeam Kasten
  in the required 1-year time window.

See Restoring Veeam Kasten Backup for instructions on how to restore Veeam Kasten to a
  point-in-time.

### Azure Immutability Setup â

To set up immutability in Azure take into account the following requirements:

- Ensure that the container exists and is reachable with the credentials provided in the profile form.
- Enable versioning on the related storage account.
- Ensure support for version-level immutability on the container or related storage account.

Since Veeam Kasten ignores retention policies, it is not necessary to
  set one on the container. As an alternative, choose the desired
  protection period, and the files will be initially protected for that
  amount plus a safety buffer to ensure protection compliance.

### Google Immutability Setup â

To set up immutability in Google take into account the following requirements:

- Ensure that the bucket exists and is reachable with the credentials provided in the profile form.
- Enable object versioning on the bucket.
- Enable object retention lock on the bucket.
- If using minimal permissions with the credentials, storage.objects.setRetention permission is also required.

### Veeam Data Cloud Vault Immutability â

There are no special setup requirements to configure Veeam Vault immutability. See Setting up Immutability for Veeam Vault for more details.

## Location Profiles page â

The Location Profiles page can be accessed by clicking on Location under the
  the Profiles menu in the navigation sidebar.

### Filtering â

The Location Profiles page supports filtering based on the following properties:

- Name : The name assigned to the location profile.
- Target : The destination for exported snapshots: bucket name (Amazon S3, GCP), container name (Azure), or persistent volume claim name (NFS/SMB).
- Validation : The current validation status of the location profile.
- Storage Provider : The third-party storage provider associated with the profile.
- Immutability : Indicates whether immutability is enabled for the profile.

---

## Usage Failover

Moving applications across clusters can be used for performing
  production failovers.

Production application failover is a process by which a standby
  production cluster assumes operations when a primary cluster fails or
  primary operations are abnormally terminated.

A cluster running Veeam Kasten along with a production application can
  use workflows provided by Veeam Kasten to organize an orchestrated
  failover to another cluster.

The following section provides an example of actions (i.e. Failover
  Action) that can be performed to failover an application between
  clusters. Actual actions should be adapted per application and cluster
  configuration.

In addition, most industries have requirements to test their DR plans at
  regular intervals. With this in mind, this page contains another example
  set of actions (Failover and FailoverTest Actions) to help with building
  your own DR procedure.

## Failover Action â

Failover Action is a set of recommended steps to make a production
  application DR ready. It is assumed that the customer's cloud
  infrastructure is able to do production DNS name switchover between
  clusters in case of production outage. In general, failover of
  components other than the application running on a Kubernetes cluster is
  out of scope for this document.

### Step 1: Clusters preparation â

To organize DR infrastructure at least one standby Kubernetes cluster
  equipped with Veeam Kasten is required. Depending on production needs a
  standby cluster can live in the same cloud environment or in a different
  one.

This document assumes that an application to be failed over is installed
  in a primary cluster and that it has a working DNS configuration.

See Installing Veeam Kasten for details about installation options.

### Step 2: Selection of an external storage â

To store application backups, primary and standby clusters must have
  network connectivity to at least one external storage location (S3,
  Google Cloud, Azure, etc).

In order to allow access to an external storage location, a
  corresponding location profile must be configured both on the primary
  and standby clusters.

See Location Configuration for details about location profiles.

### Step 3: Backup configuration â

To backup a production application and store it in an external storage
  location, a backup policy with exports enabled must be configured on the
  primary cluster.

Depending on needs, the backup policy can also retain periodic local
  snapshots on the primary cluster for faster local restore, at the
  expense of some local resources.

Refer to Application-Scoped Policies for details about backup + export policy configuration.

### Step 4: Restore configuration â

In order to restore an application on the standby side, an import policy
  must be configured on the standby cluster. Depending on whether a
  standby cluster is deployed in the same environment or in another the
  import policy may require applying transformations to some application
  resources (like Ingress) that might require different configurations
  between environments.

An import policy can be configured with scheduled runs or can also be
  ran on demand, for example in the event of an outage, or to test that
  the import + restore process is working.

Refer to Migrating Applications for details about import + restore configuration. More
    information about transforms can be found at Transforms page.

### Step 5: Triggering failover â

When an outage on the primary cluster happens, an import policy on the
  standby side should be invoked to download and restore an exported
  backup of the application and restore it.

After any external resources required by the application have also been
  failed over (such as external DNS entries), a copy of the production
  application should be up and running instead on the standby cluster.

## FailoverTest Action â

FailoverTest Action contains a guided example of steps required to build
  a demonstration of the procedure described in the previous section.

It is assumed that a production cluster is up and running and Veeam
  Kasten has been installed properly.

For demonstration purposes, a sample Kubernetes application based on the gcr.io/google_containers/echoserver:1.10 image has been deployed:

```
$ kubectl create namespace echoserver$ kubectl create deployment echoserver --image=gcr.io/google_containers/echoserver:1.10 --namespace echoserver$ kubectl expose deployment echoserver --type=NodePort --port=8080 --namespace echoserver
```

To provide external access to the application an Ingress resource which
  uses the NGINX ingress controller has been configured:

```
$ kubectl apply --namespace=echoserver --filename=- <<EOF---apiVersion: networking.k8s.io/v1kind: Ingressmetadata:  name: echoserver-ingress  namespace: echoserver  annotations:    kubernetes.io/ingress.class: nginxspec:  rules:    - http:        paths:          - path: /            pathType: ImplementationSpecific            backend:              service:                name: echoserver                port:                  number: 8080EOF
```

To make sure that the application is accessible via it's external IP
  address, the following command has been executed:

```
$ kubectl get ingress echoserver-ingress --namespace echoserverNAME                 CLASS    HOSTS   ADDRESS         PORTS   AGEechoserver-ingress   <none>   *       34.83.228.252   80      41s
```

### Step 1: Deploying a standby cluster â

For this step a standby Kubernetes cluster with Veeam Kasten installed
  is required. It is used as the target for the failover operation.

For this demonstration, another Kubernetes cluster has been provisioned
  and Traefik has been used as the
  default ingress controller.

### Step 2: Location profile configuration â

At this step an external storage should be prepared for exporting
  application backups.

For the purpose of this example, an AWS S3 bucket has been used and
  location profiles have been created for it both on primary and standby
  instances of Veeam Kasten:

For the purpose of this demonstration, a Snapshot + Export policy has been
  configured on the primary cluster.

For the purpose of this demonstration, the "on-demand" frequency has
    been used and the policy has been run on demand.

This step requires an Import + Restore policy to be configured on the
  standby cluster.

For the purpose of this demonstration, an Import + Restore policy has
  been configured without a schedule, and has been run on demand.

Since both clusters have different ingress controllers, Ingress
  resources need to be reconfigured on the standby cluster to use Traefik
  ingress controller instead of NGINX. To achieve this the following
  transforms have been added to the import + restore policy on the standby
  cluster to remove NGINX Ingress annotations and add Traefik related
  settings:

### Step 5: Run-once backup â

An initial Snapshot + Export has to be successfully performed on the
  primary cluster.

This can be achieved via clicking the Run Once menu option on the Policies page:

Before moving to the next step it's required to ensure that a
  corresponding policy run is completed:

### Step 6: Run-once restore â

After a backup is completed on the primary cluster a restore on the
  standby cluster should be initiated by clicking the Run Once menu option on
  the import policy previously created.

An import policy run should be completed before moving to the next step:

### Step 7: Checking an application copy â

After an import and restore are completed it's required to ensure
  whether an application is up and running on the standby cluster and that
  it is accessible externally.

In this case, the Ingress resource got restored with a Traefik ingress
  class annotation and the application is now accessible via Traefik load
  balancer's IP address:

> $ kubectl get ingress echoserver-ingress --namespace echoserver -o yaml
> apiVersion: networking.k8s.io/v1
> kind: Ingress
> metadata:
> annotations:
> kubernetes.io/ingress.class: traefik
> creationTimestamp: "2023-01-12T06:46:51Z"
> generation: 1
> name: echoserver-ingress
> namespace: echoserver
> resourceVersion: "778114"
> uid: de70a1eb-b90b-4167-bd37-c7d233ce58a7
> spec:
> rules:
> - http:
> paths:
> - backend:
> service:
> name: echoserver
> port:
> number: 8080
> path: /
> pathType: ImplementationSpecific
> status:
> loadBalancer: {}
> $ kubectl get service traefik --namespace traefik
> NAME      TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)                      AGE
> traefik   LoadBalancer   10.95.252.188   34.168.126.252   80:32340/TCP,443:32305/TCP   22m

```
$ kubectl get ingress echoserver-ingress --namespace echoserver -o yamlapiVersion: networking.k8s.io/v1kind: Ingressmetadata:  annotations:    kubernetes.io/ingress.class: traefik  creationTimestamp: "2023-01-12T06:46:51Z"  generation: 1  name: echoserver-ingress  namespace: echoserver  resourceVersion: "778114"  uid: de70a1eb-b90b-4167-bd37-c7d233ce58a7spec:  rules:  - http:      paths:      - backend:          service:            name: echoserver            port:              number: 8080        path: /        pathType: ImplementationSpecificstatus:  loadBalancer: {}$ kubectl get service traefik --namespace traefikNAME      TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)                      AGEtraefik   LoadBalancer   10.95.252.188   34.168.126.252   80:32340/TCP,443:32305/TCP   22m
```

---

## Usage Immutable

Veeam Kasten can leverage the object-locking capability available in
  object stores to make backups immutable. This guards against
  catastrophic disaster scenarios such as ransomware attacks and allows
  recovering the backups in those situations.

This feature is currently available for use with Azure, AWS S3 and any
  S3-compatible object store that supports object locking.

The generic storage and shareable volume backup and restore workflows are not compatible with the protections
    afforded by immutable backups. Use of a location profile enabled for
    immutable backups can be used for backup and restore, but the protection
    period is ignored, and the profile is treated as a
    non-immutability-enabled location. Please note that using an
    object-locking bucket for such use cases can amplify storage usage
    without any additional benefit. Please contact support for any inquiries.

## Disaster Scenarios â

Vulnerabilities can arise from many sources, such as lack of privilege
  separation due to credentials with permissive access, or from
  sophisticated attacks.

Consider a comprehensive breach of all secured systems in a Kubernetes
  cluster and ancillary infrastructure. Assume that a malicious agent has
  compromised all of the following:

- the Kubernetes cluster - can inspect and control applications running in all namespaces, read secrets, manipulate snapshots, and locate backups.
- the object store - can tamper with or destroy application backup data that had been exported by Veeam Kasten.
- the Veeam Kasten deployment - can force retirement of Veeam Kasten snapshots and backups, compelling Veeam Kasten to delete the associated data and metadata, including application backups and Veeam Kasten Disaster Recovery self-backups.
- the production application - can tamper with or encrypt vital data, demanding a ransom in exchange for resumed access.

In such a sophisticated scenario, an attacker might attempt to render
  restores from backups useless, before encrypting live application data
  and demanding a ransom.

## Veeam Kasten Immutable Backups â

In the face of such a comprehensive attack, Veeam Kasten has the ability
  to turn back the clock.

Veeam Kasten is capable of exporting backups to object store containers
  with object locking enabled. Doing so renders the data written there
  immutable. Even users with administrative privileges are prevented from
  deleting or tampering with the backup data. Each repository blob is
  immutable and secure for an extendable period of time.

Veeam Kasten uses these immutable blobs to go back in time, and retrieve
  the backups as they were prior to the time of an attack.

### Protection Period â

How far back in time Veeam Kasten can see is a tunable parameter called
  the protection period . The protection period is chosen by the user
  when creating a profile with immutable backups enabled.

The protection period represents the estimated amount of time required
  by your organization to recover following impact . Recovery must begin
  within that protection period window in order to guarantee a successful
  restoration from immutable backups. The longer the protection period,
  the more time can be afforded for the recovery from an impact event like
  ransomware.

The protection period can be any length of time greater than or equal to
  1 day, with a granularity of days. Longer protection periods may have
  increased storage costs associated with them, as object versions must be
  kept around longer.

### Active Monitoring â

Veeam Kasten has a background service that monitors repositories
  containing immutable backups. Each time a restore point is exported to a
  repository in a locked bucket, some new blobs may be written, and some
  blobs may be reused. Therefore the retain-until date applied to each
  blob (the property that renders it immutable) may need to be refreshed,
  or pushed out to a later date, as time passes. This is because Veeam
  Kasten's backup solution makes use of incremental backups.

Once an immutable backups repository is created, Veeam Kasten will begin
  periodically querying its data blobs in the background. The frequency of
  this operation is determined by the chosen protection period; a longer
  protection period doesn't require checking as frequently, because the
  retain-until date can be pushed out further when needed. That said, the
  longest the service will wait without performing a refresh check is 2
  days. This will only run on the cluster which made the original export;
  if a restore point is imported into another cluster, that cluster will
  not extend the protection period on the imported restore points.

In order for this background operation to run smoothly, you must
  maintain a profile referencing the location containing that repository.
  Additionally that profile must follow the criteria perscribed for an
immutable backups profile .

An alert notification will appear in the upper right corner of the Veeam
  Kasten dashboard when any of the following conditions are encountered:

- the profile no longer meets these criteria
- the background monitoring service has trouble connecting to the store
- the background monitoring service is otherwise unable to perform the refresh procedure

the profile no longer meets these criteria

the background monitoring service has trouble connecting to the
      store

the background monitoring service is otherwise unable to perform the
      refresh procedure

Clicking the alert icon will open a side-pane containing a list of
  outstanding errors and warnings, each with a description of what went
  wrong. If you are unable to determine the appropriate fix from the
  information provided, please refer to Kasten Veeam Kasten Community
Support or
  open a case via https://my.veeam.com .

## Comprehensive Protection â

Individual applications can be protected with immutable backups by
  exporting to a location with object locking enabled. This ensures those
  application restore points are unable to be tampered with, and that
  Veeam Kasten knows how to access them at the appropriate points in time.

However if the cluster has been completely compromised, Veeam Kasten may
  also be susceptible to tampering. For example if an attacker manually
  retires all restore points, from Veeam Kasten's perspective, those
  backups no longer exist.

To comprehensively secure an application's backups even in the face of
  an attack on Veeam Kasten, it is necessary to activate a Veeam Kasten
  Disaster Recovery policy that also makes use of immutable backups .
  This means that all backups of Veeam Kasten itself are also stored
  immutably in an object-locked object store location.

By combining immutable backup policy runs for an application with a
  subsequent immutable Disaster Recovery policy run for Veeam Kasten, you
  preserve both the application's data and the ability to restore it.

Each time the Disaster Recovery policy runs, it will "lock in" the
  ability to recover from any of the active restore points at that point
  in time. Multiple applications may be simultaneously protected by
  different policies with differing scheduling frequencies. Therefore it
  is recommended to schedule the Disaster Recovery policy to run at
least as frequently, if not more so, than the most frequent policy
  schedule that performs immutable backups. Additionally, the protection
  period chosen for the Disaster Recovery profile should be at least as
  long as the longest protection period in use by an immutable backups
  policy.

### Setting Up Immutable Backup Protection for S3 â

Begin by setting up one or more location profiles , each
  pointing to an object store destination with object-locking enabled .

The selected object store destination must meet certain criteria:

- Must be a bucket on AWS S3 or an S3-compatible object store.
- Must be reachable with the credentials provided in the profile form.
- Must already exist.
- The region provided on the profile form must match the region in which the bucket resides.
- Must have object locking enabled. Note: On some S3-compatible implementations, the object locking property of a bucket can only be enabled/configured at bucket creation time.

Select the checkbox for "Enable Immutable Backups".

Click the "Validate Bucket" button. This will initiate a pre-flight
  check of the above criteria.

If all of the checks succeed, a slider bar will appear for selecting the
  desired protection period . The bounds of this bar are from 1 day to
  an upper value of 90 days.

Click the "Save Profile" button to submit this profile configuration.

Enabling immutability protection for an existing profile will only be effective if the backups have not been compromised prior to activation.

Profiles that reference object-locked object store locations and have
  immutable backups enabled will display this on its respective profile
  card: a field indicating "Object Immutability" is "enabled", and the
  chosen protection period.

Next follow the standard Backups workflow, selecting one of the immutable backup profiles for
  each policy. This will protect each covered application with immutable
  backups for all policy runs.

Finally follow the Veeam Kasten Disaster Recovery workflow, selecting the desired immutable backup profile for
  the "Cloud Location Profile" in the DR form.

### Setting Up Immutable Backup Protection for Azure â

To set up immutability in Azure take into account the following requirements:

- Ensure that the container exists and is reachable with the credentials provided in the profile form.
- Enable versioning on the related storage account.
- Ensure support for version-level immutability on the container or related storage account.

Since Veeam Kasten ignores retention policies, it is not necessary to
  set one on the container. As an alternative, choose the desired
  protection period, and the files will be initially protected for that
  amount plus a safety buffer to ensure protection compliance.

### Setting Up Immutable Backup Protection for Google â

To set up immutability in Google take into account the following requirements:

- Ensure that the bucket exists and is reachable with the credentials provided in the profile form.
- Enable object versioning on the bucket.
- Enable object retention lock on the bucket.
- If using minimal permissions with the credentials, storage.objects.setRetention permission is also required.

### Setting Up Immutable Backup Protection Using Veeam Repository â

To use the Veeam Kasten backup immutability feature with VBR, make sure
  that immutability settings are configured consistently as follows:

- Set up the immutability window length in VBR for the desired immutability period.
- Configure a proper protected period in Veeam Kasten. This period must be less than or equal to the immutability window in VBR.
- Adjust Veeam Kasten backup frequency and retention settings to prevent the deletion restore points inside the VBR immutability window. Failure to do so may lead to orphaned restore points that will not be automatically retired.

The integrity of restore points outside the immutability window in VBR
    is not guaranteed. It is recommended to set up the retention policy to
    automatically delete such restore points when they are outside the
    immutability window.

This approach allows you to keep only the N last backups according to
  the chosen backup frequency. If you need to keep, for example, N daily
  backups and M yearly backups, create several policies with different
  backup frequencies and retention settings.

#### Example â

A customer wants to guarantee the immutability for 30 days for their
  daily backups:

- The immutability period for VBR must be set to 30 days
- The protection period for Veeam Kasten must be set to 30 days (or lower)

The configuration of the S3 bucket is beyond the scope of this example.
  We assume that it has already been properly configured.

#### Setting up the Immutability Window Length in VBR â

To set up the immutability window length in VBR, open the Repository
  settings and enter the desired value in the "Make recent backups
  immutable for" field:

Allowed value for immutability window in VBR is 7 to 9999 days.

Here, we set it to 30 days because the customer wants to guarantee
  immutability for this period.

Additional information about immutable repositories can be found in the VBR
documentation .

#### Setting up the Immutability Window Length in Veeam Kasten â

The Veeam Kasten protection period should be set to any value up to and
  including 30 days, but not more, to align with the specified
  requirements.

The Protection period set in Veeam Kasten should not exceed the
    immutability window set in VBR. If the protection period is configured
    incorrectly, the Policy validation will display the following error (as
    shown in the figure):

Please check, Setting Up Immutable Backup Protection for details about immutable profile creation.

### Setting Up Immutable Backup Protection Using Veeam Data Cloud Vault â

To use the Veeam Kasten backup immutability feature with Veeam Vault, make sure
  to configure the desired retention period in Kasten as this setting is required.

The default value is 30 days but it may be configured as low as 1 day.

It is recommended to set up the retention policy in Kasten to automatically delete
    restore points when they are no longer required and to prevent unnecessary costs.

If you need to keep, for example, N daily backups and M yearly backups, create
  several policies with different backup frequencies and retention settings.

#### Creating an Immutable Policy â

Create a policy with a daily snapshot (one snapshot per day) and set
  the exported snapshot retention as shown in the figure:

Weekly, monthly and yearly snapshots are intentionally set to 0.

If a user needs another backup frequency, it can be done via another
  (separate) policy with separate S3 and VBR repositories, with
  corresponding immutability settings.

### Recovering from a Worst-Case Scenario Attack â

#### Stage 1: Recover Veeam Kasten â

In many disaster circumstances, it may be safer to assume that Veeam
  Kasten has been compromised if an attack has been detected. If so, Veeam
  Kasten may need to be recovered to a point-in-time prior to the attack.
  If it is absolutely certain that Veeam Kasten has not been affected,
  directly restoring the application from Veeam Kasten's current known
  restore points is still possible, in which case skip directly to Stage 2 .
  When in doubt, discuss with your CISO if it makes sense to restore Veeam
  Kasten to a time before the attack.

Restoring Veeam Kasten is straightforward. Follow the standard Recovering Veeam Kasten From a Disaster workflow:

1. Reinstall Veeam Kasten , deleting the Veeam Kasten namespace if reinstalling on the same cluster.
2. Create a secret to contain the DR passphrase .
3. Provide the external storage configuration by adding a location profile referencing the object store location where backups are stored. This should resemble the profile that was created when Setting Up Immutable Backup Protection , but it is not necessary to create it with "Immutable Backups" enabled.
4. Ascertain when the disaster was likely to have occurred. Pick a timestamp corresponding to a point-in-time prior to the disaster event. The time chosen should be no earlier than the protection period (associated with the Veeam Kasten Disaster Recovery immutable profile) in the past.
5. Install the helm chart that creates the Veeam Kasten restore job. Provide the source cluster ID, the name of the location profile just created, and the point-in-time chosen in the previous step, formatted as a RFC3339 time stamp.

```
## e.g. to restore Veeam Kasten to 15:04:05 UTC on Jan 2, 2022:$ helm install k10-restore kasten/k10restore --namespace=kasten-io \    --set sourceClusterID=<source-clusterID> \    --set profile.name=<location-profile-name> \    --set pointInTime="2022-01-02T15:04:05Z"
```

Upon successful recovery, Veeam Kasten will now be in the same state as
  it was at the last time the Disaster Recovery policy had been run prior to the chosen point-in-time. This includes references to restore
  points that had since been retired, even if that retirement happened as
  part of routine policy retention management.

Restore points referring to snapshots or non-immutable backups may or
  may not be recoverable in this state; local storage snapshots or
  non-immutable exported backup data may have been permanently deleted,
  either during an attack, or as part of routine operation. However any
  restore points corresponding to immutable backups should still be fully
  recoverable.

#### Stage 2: Restore Applications â

The process for restoring applications from immutable backups is
  identical to the standard restoration workflow . Make sure
  to select the Exported restore point instance, referring to the backup
  residing in the object store locked bucket.

Veeam Kasten will do all point-in-time management based on its knowledge
  of the time the backup took place. Initiating a restore is as simple as
  selecting the desired backup (exported) restore point and clicking
  "Restore".

The point-in-time chosen for the restore will be different for each PVC,
    and is a function of the time when the data upload completed for each.
    The upload completion time can be viewed for each data artifact by
    querying the RestorePointContent Details . Veeam Kasten will use a point-in-time 30 seconds after the uploadEndTime timestamp for the restore.

When the restore action completes, the application will be running in
  the same state, with the same persistent data, as it was at the time the
  backup took place.

---

## Usage Migration 

## Introduction â

The ability to move an application across clusters is an extremely
  powerful feature that enables a variety of use cases including Disaster
  Recovery (DR), Test/Dev with realistic data sets, and performance
  testing in isolated environments.

In particular, the Veeam Kasten platform is built to support application
  migration and mobility in a variety of different and overlapping
  contexts:

- Cross-Namespace : The entire application stack can be migrated across different namespaces in the same cluster (covered in restoring applications ).
- Cross-Cluster : The application stack is migrated across non-federated Kubernetes clusters.
- Cross-Account : Mobility can additionally be enabled across clusters running in different accounts (e.g., AWS accounts) or projects (e.g., Google Cloud projects).
- Cross-Region : Mobility can further be enabled across different regions of the same cloud provider (e.g., US-East to US-West).
- Cross-Cloud : Finally, mobility can be enabled across different cloud providers (e.g., AWS to Azure).

## Mobility Configuration â

Some additional infrastructure configuration is needed before migration
  between two clusters can be enabled.

- Required : Object storage or NFS/SMB file storage configuration
- Use-Case Specific : Cross-account and Kanister configuration

### External Storage Configuration â

For two clusters to share data, Veeam Kasten needs access to an object
  storage bucket (e.g., k10-migrate ) or an NFS/SMB file storage location
  that will be used to store data about the application restore points
  that have been selected for migration between clusters. If a Veeam Repository is used to export snapshot data then it too needs to be accessible in
  the destination cluster. The source cluster needs to have write
  permissions to these locations, and the destination cluster needs to
  have read permissions. The appropriate credentials can be configured
  using Location profiles.

### Cross-Cloud Configuration â

When migrating applications across different cloud providers, including
  hybrid environments, Veeam Kasten should have support for storage system
  snapshots on the originating side.

#### Orchestrated Application Failover â

Moving applications across clusters can be used for performing
  production failovers. More info about preparing an application to
  cross-cloud failover can be found here .

### Cloud-Provider Configuration â

The following per-cloud provider configuration is required when
  cross-account/project/subscription migration within the same
  cloud-provider is needed.

#### AWS â

To use IAM roles, there are two options: first, if Veeam Kasten was
  installed with an IAM role, that can be used by selecting the Authenticate With AWS IAM Role option. Alternatively, if an IAM role
  needs to be specified at profile creation time, the Execute Operations Using an AWS IAM Role option should be selected. As
  a result, Veeam Kasten will generate and use temporary security
  credentials for executing operations.

If cross-account and/or cross-region volume migration is desired, select
  the Advanced Export Settings option while creating or editing the
  location policy for entering additional destination information:

In an AWS environment, if the destination cluster is in a different
  region, specify the destination region here, and Veeam Kasten will make
  a cross-region copy of the underlying EBS snapshots.

If a different target account at the destination is desired, specify it
  here. Veeam Kasten needs an IAM user created within the destination
  account (e.g., k10migrate ). The destination AWS account
ID is also needed. During the creation of the export policy, the username
  should be specified as <AWS Account ID>/<User Name>

Both the native provider and the CSI provider are supported.

#### Google Cloud â

Currently, due to underlying provider limitations, optimized migration
  is only supported among different clusters in the same project. For
  migration across clusters running within different accounts, please
  follow the documentation for cross-cloud migration.

#### Microsoft Azure â

In an Azure environment, a destination region that is different from
  source can be specified in the export policy in the same way as
  mentioned for AWS above for a cross-region copy of the underlying
  snapshots.

A destination resource group may also be specified. This is particularly
  useful when migrating CSI provisioned volumes.

All the objects created for an AKS cluster belong to a resource group
    created specifically for it. When a CSI driver takes snapshots, these
    also belong to this resource group. In order for other clusters to use
    these snapshots, their service principals must have the [Disk Snapshot
    Contributor] role on that resource group.

az role assignment create --assignee <service principal ID> --role 'Disk Snapshot Contributor' --resource-group <resource group>

Optimized migration across different Azure subscriptions will be
  available in the near future. If migration across clusters running
  within different subscriptions is needed, please follow the
  documentation for cross-cloud migration for the current release.

## Exporting Applications â

### Policy-Based Exports â

The workflow for exporting applications into another cluster is very
  similar to the workflow followed for protecting applications . When a policy is created to
  capture an application, simply also select the Enable Backups via Snapshot Exports option shown above.

If selected, one ExportAction is created for each BackupAction when the
  export schedule is triggered. Once all the ExportActions finish for that
  scheduled time, the metadata is uploaded to the location specified by
  the Profile. After this is uploaded, these backups are available for
  import.

The Export Snapshot Data option stores the exported data and metadata
  to the store configured above, but the Export Snapshot References Only option stores only metadata about the application restore points. Below
  these options, the Advanced Export Settings button opens up additional
  options for specifying storage classes that override the Snapshot Data or Snapshot References Only setting.

For example, if there is a cluster where multiple storage providers are
  in use, and all of the storage classes in this cluster can be exported
  by reference, then the Export Snapshot References Only option is all
  that is needed; but if one of the storage classes in this cluster is
  only visible inside the cluster (e.g., a Rook Ceph setup with a
  StorageClass named rc1 ), the Export Snapshot References Only option
  can still be used, but that one particular StorageClass ( rc1 ) needs to
  be listed as an exception to the portability setting, because its data
  needs to be exported. The image above shows the settings for this
  example.

If migration is desired across Kubernetes clusters in different clouds
  or between on-premises and public cloud environments, you need to enable
  the Export Snapshot Data option in order to migrate both the
  application data and metadata. Without it, the application data will not
  be exported and the subsequent import will fail.

When Export Snapshot Data is selected then the Export Location
Profile specifies a Location Profile where the exported data and metadata will be stored. This
  profile contains the location of an object storage bucket (e.g., using
  AWS S3, Google Cloud Storage, Azure blob, or any other S3-compliant
  object store) or an NFS/SMB file storage location to export the needed data.
  The default is to export snapshot data to this location in filesystem mode ,
  but with some cluster infrastructures snapshot data can alternatively be
  exported in block mode , by enabling the Export snapshot data in block mode option
  and selecting an appropriate destination location profile from the Location Profile Supporting Block Mode list.

Within Advanced Export Settings , additional options become available
  when the source and destination clusters are in different regions of a
  public cloud provider that supports cross-region snapshot copies (e.g.,
  AWS and Azure). Follow the instructions here to enter the
  destination information.

When this application is imported into another cluster, as described
  below, initial handshake configuration will be required. This can be
  obtained from the policy by clicking Show import details and will
  result in the below encoded configuration being displayed.

### Manual Exports â

Apart from policy-driven exports, it is also possible to manually create
  a one-off application export. From the Applications page, simply click
  on the Export icon.

After a restore point is selected, you will be presented with
  information about the application snapshot being migrated (e.g., time,
  originating policy, artifacts) and, more importantly, the option to
  configure the destination by selecting a mobility profile.

The option to select export portability and other Advanced Export Settings follows. Refer back to the above section for information relating to these options.

Finally, click on Export . After confirming the export, the encoded
  import configuration required by the destination cluster will be
  presented.

## Importing Applications â

Import policies are only supported for importing applications into a
    cluster that is different than where the application was captured from.
    The protecting
applications section has more
    details.

The Applications with block mode exports section contains additional details and constraints for when
    such applications are involved.

Importing an application snapshot is again very similar to the policy
  creation workflow for protecting applications . From
  the Policies page, simply select Create New Policy .

To import applications, you need to select Import for the action.
  While you need to also specify a frequency for the import, this simply
  controls how often to check the shared object storage or NFS/SMB file
  storage location. If data within the store is not refreshed at the same
  frequency, no duplicate work will be performed, and multiple restore
  points may be imported by a single action if there is any catching-up to
  do.

Care should be taken when auto-restoring the application during import.
    In particular, ensure that the newly restored application does not
    conflict with the application running in the source cluster. Examples of
    potential conflicts include accidental credential reuse, access to and
    use of external services, and services conflicting for exclusive
    ownership of shared resources.

It is also possible to select Restore after Import to bring the
  application up in this cluster after the metadata import is complete.

You will also need to paste the text block displayed by the source
  cluster's export policy (or shown during a manual export) to allow
  Veeam Kasten to create the data export/import relationship for this
  application across the clusters. Finally, similar to the export
  workflow, a location profile also needs to be selected. The destination
  cluster usually only needs read and list permissions on all the data in
  the shared storage system.

When selecting a location profile in the Profile for Import section,
  the list of location profiles will show a "Matching Profile". This is
  the original export location, which should contain the exported restore
  points. A list of "Other Profiles" is also shown. Selecting a profile
  from the "Other Profiles" section can be useful if, for example, a
  restore point has been cloned or moved from its original export
  location.

A Veeam Repository Location used for exported snapshot data should not be specified as
    the Profile for Import as restore point data was not sent to the Veeam
    Repository. However, the importing cluster must have a Veeam Repository Location Profile with the identical name as the one in the original
    cluster. The restore will fail if this location profile is not present.

After the Create Policy button is clicked, the system will start
  scheduling jobs based on the policy definition. If new data is detected,
  its metadata will be imported into the cluster, automatically associated
  with the application stack already running, and be made available as a
  restore point. Note that unless Restore after Import is selected, only
  metadata is brought into the cluster. If the data volumes reside in an
  object store or NFS/SMB file store (e.g., after a cross-cloud migration),
  they will not be converted into native volumes until a restore operation
  is initiated.

The normal workflow for restoring applications can be
  followed and, when given the choice, simply select a restore point that
  is tagged with the import policy name.

Running an import policy keeps the list of local restore points in-sync
  with the retention settings of the originating policy. If a restore
  point is marked for retirement by the source cluster, it will be cleaned
  up; exported data and metadata will be deleted. Accordingly, the next
  time the import policy runs, that retired restore point will be removed
  from the destination cluster, reflecting the fact that it can no longer
  be used to restore the application.

### Transforming restored resources â

By default, Veeam Kasten restores Kubernetes resources as they exist in
  the restore point. However, there are times when the restore target does
  not match the environment of the backup. For these situations, Veeam
  Kasten allows Kubernetes resource artifacts to be transformed on
  restore.

For example, if a restore point was created in one cloud provider and it
  should be restored into a cluster in a different cloud provider, it
  might be necessary to use a transform that updates the container image
  URLs in some resources, or one that changes storage class settings.

To apply transforms to the restored application, enable Apply transforms to restored resources under Restore After Import .

#### Add new custom transform â

The complete API specification for transforms can be found here .

Clicking the Add new transform will open a form for creating a new
  transform.

On the form, name the transform, select which resources the transform
  will be applied to, and then create one or more operations.

Each operation will have its own panel allowing customization and
  testing of the selected operation.

Operations can be tested against any resources to verify the outcome of
  the operations. The ability to apply transforms will provide flexibility
  in migration workflows between environments where more than just a like
  for like recovery is needed.

#### Add transforms using transform sets â

A complete guide of how to setup a transform set can be found here .

Clicking the Add a reference to an existing transform set will open a
  form for selecting a transform set.

Type the name of the transform set and click Add reference .

A reference to the transform set will then be added to the form. The SET label helps identify transforms which are stored and referenced
  rather than those that are created inline via Add new transform .

#### Extract transforms as transform set to reuse them â

To make a transform set from a sequence of transforms already defined
  click Extract this list as new transform set .

Type the name of new transform set and [optionally] its description.

Click Create transform set . After successful creation all transforms
  will be replaced with the reference of the created transform set.

## Migration Considerations â

While migrating applications across clusters, regions, and clouds is
  significantly simpler with Veeam Kasten, there are still other
  considerations to be aware of that might impact a migration workflow.
  The sections below cover these considerations in detail for a smoother
  migration process.

### Non-Application Resources â

While the Veeam Kasten platform will protect all resources that are
  discovered in the application namespace, it intentionally does not
  gather resources that are not part of an application namespace but only
  found at the cluster level. Examples of such resources include Custom
  Resource Definitions or CRDS (but not the actual Custom Resources or
  CRs), Storage Classes, or Cluster Role Bindings. Veeam Kasten assumes
  that these resources will be deployed as a part of cluster creation by
  the administrator or the cluster deployment process. This is of
  particular importance when migrating applications to a new cluster as
  the absence of these resources could cause application restore failures.

Related to the issue of cluster-wide resources, there are Kubernetes
  resources that are only found in a namespace but have a resource
  conflict with other applications in the same cluster. While generally
  discouraged for production usage, a commonly observed resource that
  falls in this category is the NodePort
service .
  Once claimed by an application, a subsequent request for the same
  NodePort will conflict and be disallowed. Whenever possible, Veeam
  Kasten attempts to work around such limitations by resetting such
  settings on restore to a cluster-provided non-conflicting value. For
  example, with NodePort, Veeam Kasten will allow Kubernetes to pick a
  port from the default port range allocated to the NodePort service.

Finally, applications sometimes will have dependencies that are external
  to the cluster (e.g., DNS entries) that might not be visible to
  Kubernetes or Veeam Kasten. However, it is possible to work with such
  external resources through the use of post-restore hooks available in
  Veeam Kasten and Kanister blueprints.

### Availability and Failure Zones â

For migrations across Kubernetes clusters that are spread across
  different availability (or failure) zones, Veeam Kasten, for stateful
  applications in the destination cluster, tries to maintain the same
  fault independence as the source cluster. However, this can be hard or
  not possible when either the destination cluster has fewer availability
  zones than the source cluster or does not have nodes deployed in all
  availability zones.

To help work around these issues, Veeam Kasten adopts a number of
  techniques to simplify the redeployment process. As far as possible,
  Veeam Kasten will attempt to only place volumes in availability zones
  where it has already discovered worker nodes belonging to the
  destination cluster.

In the case of migration in the same region, Veeam Kasten will attempt
  to first place volumes in the same zones that the source cluster had
  selected. If that is not possible, it will assign volumes to other
  availability zones where it has found worker nodes.

For cross-region migration, Veeam Kasten will first attempt to map
  availability zones between the source and destination regions and,
  assuming the worker nodes are found in those zones, provision volumes
  according to that mapping. If a mapping is not possible (e.g., the
  source cluster used more available zones than the destination cluster
  has available), it will provision volumes into one of the other
  discovered zones in the destination cluster.

In the unlikely case that Veeam Kasten is unable to either find worker
  nodes or discover zones, it will fallback to assigning volumes to zones
  that it knows exist in that region.

Finally, note that the above approach can potentially run into
  scheduling issues where the destination cluster might have either
  insufficient or no compute resources in a given zone. If you run into
  this issue, the simplest solution is to provision more worker nodes
  across your desired available zones.

### Applications with Block mode exports â

Migrating an application whose snapshot data was exported in block mode format can
  be done across clusters that have storage classes with PersistentVolumes
  that can be exported by Veeam Kasten in this manner. See Block Mode Exports for details on how to identify such storage classes to Veeam Kasten.

If the source cluster type is different from the destination cluster
  type, then a resource transformation will be required to change the storage class initially
  configured for the application in the source cluster to one that is
  available in the target cluster. The selected storage class in the
  target cluster must support Dynamic Volume
Provisioning and Block Volume
Mode ,
  and must be identified to Veeam Kasten in the manner described in Block Mode Exports .

Veeam Kasten will use available infrastructure specific network APIs to
  write data to the volume directly if possible (for example, in vSphere clusters); otherwise, Veeam Kasten will mount the volume in Block mode
  and directly write the data to the raw device. After the volume data is
  restored, Veeam Kasten will ensure that the volume is mounted in the
  application with whatever volume mode was configured initially.

In the particular case of migrating snapshot data from a Veeam Repository Location , an identically named location profile as used as the export
    block mode destination must exist in the importing cluster.

---

## Usage Overview

The Veeam Kasten dashboard is broken up into a number of different
  sections. A brief description about each is provided below.

It is also possible to perform an interactive walkthrough of the Veeam
  Kasten dashboard via a Guided Tour. The tour is available when the Veeam
  Kasten dashboard is accessed for the first time or via the Interface page of the Settings menu
  in the navigation sidebar.

## System Overview â

The top of the Veeam Kasten dashboard displays a list of applications
  (currently mapped to namespaces), any policies that might exist in the
  system, and a summary of the cluster's backup data footprint.

After filtering to only include applications that have stateful services
  (defined as containing a persistent volume), the above screen breaks
  down each section into three categories:

- Unmanaged : There are no protection policies that cover this object
- Non-compliant : A policy applies to this object but the actions associated with the policy are failing (e.g., due to underlying storage slowness, configuration problems, etc.) or the actions haven't been invoked yet (e.g., right after policy creation)
- Compliant : Objects that both policies apply to and the policy SLAs are being respected
- Removed : Objects that are removed.

## Applications, Namespaces, and Workloads â

The Veeam Kasten platform by default equates namespaces to applications
  for ease of use and consistency with Kubernetes best practices, use of
  RBAC, and to mirror the most common application deployment pattern.
  However, as shown later, policies can be defined to operate on more than
  one namespace or only operate on a subset of an application residing in
  a single namespace.

Assuming you have already installed applications, clicking on the
  Applications card on the dashboard will take you to the following view.
  Choosing one of the Compliant/Non-Compliant/Unmanaged/Removed
  buttons, it would automatically filter the applications.
  The cluster-scoped Options lists down the options that can be performed on the cluster scoped resources.

Veeam Kasten classifies Pods, VirtualMachines, StatefulSets, Deployments and DeploymentConfigs as workloads.

An application, in turn, is made up of multiple Kubernetes resources and
  workloads. In the above diagram, the GitLab card shows that the
  application is composed of four volumes, seven network resources, three
  workloads, and two other pieces of application configuration. You can
  get more information about the application by clicking on the details
  icon.

## Restore Points â

The Veeam Kasten UI has a centralized view for listing all the restore points created or imported by the cluster.
  It is accessed by clicking on the Restore Points item in the left side menu.

Clicking on a specific restore point will provide additional details. From there, the Application can be
  restored by clicking on the Restore button:

Additionally, local restore points can be exported by clicking on the Export option in the dropdown menu:

Exported restore points can be validated by selecting the Validate option in the dropdown menu:

Restore points can be deleted, either in bulk by selecting them first, or individually by using the
  action dropdown menu:

The Restore Points page provides rich filtering capabilities. They can be filtered based on the Application,
  the originating Policy, the Profile used for import/export and the creation date/time. Under the Application filter,
  the cluster-scoped option can be selected to view Restore Points that include cluster-scoped resources.
  Additionally, the Restore Points can be filtered by their type - Snapshot, Exported or Imported.
  Selecting Include manual runs only will only list the restore points that were created
  by manually snapshotting or exporting an application, or by manually executing a policy.
  Selecting No expiration will only list the restore points that do not have an expiration,
  allowing for simple identification and removal of orphaned backup data.

## Policies â

Within Veeam Kasten, policies define a selection of Kubernetes resources and one or more data management actions that are configured to occur on a periodic or event-driven basis.

On the main dashboard, the Policies card provides an overview of configured policy types. Selecting via the sidebar or the Policies card navigates to the Policies page, which lists all policies that have been created in the system. At the time of installation, no policies are created by default.

A policy can be created on the Policies page by clicking the Create New Policy button, or by navigating to the Applications page and selecting the menu option to Create a Policy for a specific application.

## Settings â

Accessible via the navigation sidebar, the Settings menu is where you
  can access and configure:

- System Information (Logs download, upgrade status, etc.)
- Licenses (Veeam Kasten product licenses)
- Veeam Kasten Disaster Recovery
- Interface (Light/Dark Mode, Guided Tour)

## Support â

Located at the bottom of the navigation sidebar Get Support is where you can
  find links to open a Support case, this documentation, and the Knowledge
  Base articles.

## Activity â

Below the policy management section of the dashboard, you will find
  activity data. This consists of a graph that shows all activity in the
  system. As there are no default policies, you will not see any activity
  after the initial install but, once policies are defined, the graph will
  start displaying activity. Mousing over the graph will display action
  information such as status, action duration, action start time, and
  action completion time.

Some of the same activity information can also be viewed in tabular form
  under the graph. In particular, the dashboard first displays a summary
  of activity in the system including total actions, average action
  duration, number of data artifacts, the size of those artifacts, etc.

Following the activity and artifact summary, information on recent
  actions is displayed. This includes the Policy that generated the action
  which may include the number of child actions, the number of
  applications included in the Policy run, and start and completion times.
  The display for manual actions, such as manual snapshots, will be
  slightly different listing the phases and number of artifacts included
  in the action. You can also filter the displayed actions by the
  originating Policy, type of action, failed actions, and completed
  actions.

Actions listed as "Policy Run" can be expanded by clicking on the row,
  bringing up the policy run page for that action. This page states the
  number of actions included in the policy run along the the names of the
  applications.

Actions in the running state can be cancelled. Click the running action
  in the actions list and look for the "Cancel Action" button on the
  action details panel. Cancellation is best-effort and may not take
  effect until the next cancellation checkpoint, typically between phases.
  See API Cancellation for more details.

## Manual Actions â

Apart from policies, it is also possible to manually create a one-off
  application snapshot or export. From the Applications page, simply click
  on the quick action menu button.

With manual snapshots it is possible to set an expiration date for the
  snapshot. If this is not set then the snapshot will exist until it is
  manually deleted from the underlying system. Via the API this is done
  by setting spec.expiresAt .

---

## Usage Protect

Protecting an application with Veeam Kasten, usually accomplished by
  creating a policy, requires the understanding and use of three concepts:

- Snapshots and Exports : Depending on the environment and requirements, one or both of these data capture mechanisms will be used
- Scheduling : Specification of application capture frequency and snapshot/backup retention objectives
- Selection : This defines not just which applications are protected by a policy but, whenever finer-grained control is needed, resource filtering can be used to select what is captured on a per-application basis

This section demonstrates how to use these concepts in the context of a
  Veeam Kasten policy to protect applications. Today, an application for
  Veeam Kasten is defined as a collection of namespaced Kubernetes
  resources (e.g., ConfigMaps, Secrets), relevant non-namespaced resources
  used by the application (e.g., StorageClasses), Kubernetes workloads
  (i.e., Deployments, StatefulSets, OpenShift DeploymentConfigs, and
  standalone Pods), deployment and release information available from Helm
  v3, and all persistent storage resources (e.g., PersistentVolumeClaims
  and PersistentVolumes) associated with the workloads.

Creating a new policy may be performed via either the Policies or Applications page. Initiating policy creation from the Applications page will pre-populate fields for policy name and namespace selection.

First, go to the Applications page by clicking on the Applications card on the main dashboard or using the Applications navigation link the sidebar.

Next, find any unmanaged application in the Application table and select the Create a Policy menu option to navigate to the policy creation form, where the auto-populated policy name will be provided and can be modified as needed.

## Snapshots and Exports â

All policies center around the execution of actions and, for
  protecting applications, you start by selecting the snapshot action with
  an optional export action to produce a durable backup.

### Snapshots â

Snapshots are the basis of persistent data capture in Veeam Kasten. They
  are usually used in the context of disk volumes (PVC/PVs) used by the
  application but can also apply to application-level data capture (e.g.,
  with Kanister ).

Snapshots, in most storage systems, are very efficient in terms of
  having a very low performance impact on the primary workload, requiring
  no downtime, supporting fast restore times, and implementing incremental
  data capture.

However, storage snapshots usually also suffer from constraints such as
  having relatively low limits on the maximum number of snapshots per
  volume or per storage array. Most importantly , snapshots are not
  always durable. First, catastrophic storage system failure will destroy
  your snapshots along with your primary data. Further, in a number of
  storage systems, a snapshot's lifecycle is tied to the source volume.
  So, if the volume is deleted, all related snapshots might automatically
  be garbage collected at the same time. It is therefore highly
  recommended that durable backups be created by exporting data.

A number of public cloud providers (e.g., AWS, Azure, Google Cloud)
    actually store snapshots in object storage and they are retained
    independent of the lifecycle of the primary volume. However, this is not
    true of all public clouds (e.g., IBM Cloud) and you might also need to
    enable exports in public clouds for safety. Please check with your cloud
    provider's documentation for more information.

### Exports â

Given the limitations of snapshots, it is often advisable to set up
  backups of your application stack. However, even if your snapshots are
  durable, backups might still be useful in a variety of use cases
  including lowering costs with Veeam Kasten's data deduplication or
  backing your snapshots up in a different infrastructure provider for
  cross-cloud resiliency.

Backup operations convert application and volume snapshots into backups
  by transforming them into an infrastructure-independent format and then
  storing them in a target location.

The resulting exported data is organized into
    storage repositories that are exclusively controlled and maintained by
    the Veeam Kasten instance. Independently using, interacting, connecting, modifying,
    copying, upgrading, or in any way accessing/manipulating a Veeam Kasten
    storage repository is unsupported and might cause data corruption/loss
    to some or all of the restore points. Users must never attempt to
    perform any such action themselves unless under constant, active
    supervision by a member of Veeam support or engineering teams.

To convert snapshots into
  backups, select Enable Backups via Snapshot Exports during policy
  creation. Additional settings for the destination location and control
  over the export of snapshot data versus just a reference will also be
  visible here. These are primarily used for migrating applications across
  clusters and more information on them can be found in the Exporting Applications section. These settings are available when creating a
  policy, and when manually exporting a restore point.

The backup produced by an export action consists of metadata of the
  application and snapshot data for the application volumes. The
  destination for the metadata export is an Object Storage Location or an NFS/SMB File Storage Location that is specified in the Export Location Profile field.

There are two options by which Veeam Kasten exports snapshot data: Filesystem Mode Export or Block Mode Export .

Each mechanism defines the process of uploading,
  downloading, and managing snapshot data in a specific destination
  location. The default export mechanism is selected automatically on a
per-volume basis , based on the Volume
Mode used to mount the volume in a Pod:

- The Filesystem Mode Export mechanism is used to export snapshot data of volumes with a Filesystem volume mode .
- The Block Mode Export mechanism is used to export snapshot data of volumes with a Block volume mode .

Additionally, there are scenarios in which Filesystem mode volumes may be exported
  using the Block Mode Export mechanism. See Block Mode Export for details.

The two export mechanisms are described below:

#### Filesystem Mode Export â

This is the default mode of export for a volume mounted in Filesystem volume mode. Such volumes are attached via the volumeMounts property of a Pod container specification.

A filesystem mode export assumes that the format of the data on the
  application disk is a filesystem. During upload, this export
  mechanism creates a clone of the source PersistentVolume from the volume snapshot produced by the Veeam Kasten policy. This volume is then mounted in a temporary Pod
  which deduplicates, compresses, encrypts, and uploads the data to the repository.
  During restore operations the
  target volume is similarly mounted in a temporary Pod using filesystem volume mode
  and the exported data is restored.

#### Block Mode Export â

This is the default mode of export for a volume mounted in Block volume mode. Such volumes are attached via the volumeDevices property
  of a Pod container specification.

A block mode export accesses the content of the disk snapshot at the
  block level. If changed block tracking (CBT) data is available
  for the volume and is supported in Veeam Kasten for the
  provisioner concerned, Veeam Kasten will export the
  incremental changes to the repository without needing to perform
  client-side fingerprinting and deduplication. If CBT is
  unavailable, Veeam Kasten will read the entire source volume
  upon export in order to produce an incremental backup.

During the export process, the temporary datamover Pod will use
  provisioner-specific network data transfer APIs to read
  volume snapshot data, if available and
  supported by Veeam Kasten. Alternatively, if these APIs are not
  available, a clone of the source PersistentVolume will be created from the volume snapshot produced by the Veeam Kasten policy. This
  volume is then mounted in the temporary Pod using Block volume mode,
  and the data will be read from the raw volume.

Similarly, during the restore process, the mechanism will use
  storage provisioner specific network data transfer APIs if
  available and supported by Veeam Kasten, to directly write the data
  to the target volume. Alternatively, if these APIs are not available, the target
  volume will be mounted in the temporary Pod using Block volume mode
  and the data will be written to the raw volume.

When block mode export is used, the organization of
  exported data is based on the type of location profile
  configured in the policy:

- When the destination is an Object Storage Location or an NFS/SMB File Storage Location , snapshot data will be uploaded in a Veeam Kasten specific format which provides deduplication, compression and encryption support in the specified destination. Automatic compaction will be performed periodically on volume data, to ensure that the chain of incremental backups that follows a full backup will not grow too long. Compaction synthesizes a full backup by applying the chain of incremental backups to the base full backup and saving the result as a new full backup; no block data is uploaded during compaction as only references to data blocks are manipulated by the operation. Metadata will also be sent to the same destination location, though it is stored separately from the snapshot data.
- When the destination is a Veeam Repository Location then snapshot data is uploaded to a Veeam Repository in its specific format. A Veeam Repository Location does not provide metadata storage, which must be specified separately within the policy.

When the destination is an Object Storage Location or an NFS/SMB File Storage Location , snapshot data will be uploaded in a Veeam Kasten
      specific format which provides deduplication, compression and
      encryption support in the specified destination.

Automatic compaction will be performed periodically on volume
      data, to ensure that the chain of incremental backups that follows
      a full backup will not grow too long. Compaction synthesizes a
full backup by applying the chain of incremental backups to the
      base full backup and saving the result as a new full backup; no
      block data is uploaded during compaction as only references to
      data blocks are manipulated by the operation.

Metadata will also be sent to the same destination location,
      though it is stored separately from the snapshot data.

When the destination is a Veeam Repository Location then snapshot data is uploaded to a Veeam Repository in its specific format.

A Veeam Repository Location does not provide metadata storage, which must be
      specified separately within the policy.

#### Enabling Block Mode Export â

To enable block mode exports and restores, first use the Veeam Kasten Primer Block Mount Check to validate the storage provisioner is compatible with block mode.

Next, apply the following annotation to the StorageClass
  of any compatible provisioner where block mode export will be required:

```
$ kubectl annotate storageclass ${STORAGE_CLASS_NAME} k10.kasten.io/sc-supports-block-mode-exports=true
```

The annotation above is not required for StorageClasses using
    the csi.vsphere.vmware.com provisioner.

#### Exporting Filesystem Volumes in Block Mode â

A Filesystem volume normally exported in filesystem mode may be exported in
  block mode if desired, provided its StorageClass meets the
  requirements and is annotated as described in Enabling Block Mode Export . To enable this behavior, it is necessary to
  request it on a per-volume basis by setting one of the following
  annotations on its PersistentVolumeClaim:

```
$ kubectl annotate pvc -n ${NAMESPACE} ${PVC_NAME} k10.kasten.io/pvc-export-volume-in-block-mode=preferred$ kubectl annotate pvc -n ${NAMESPACE} ${PVC_NAME} k10.kasten.io/pvc-export-volume-in-block-mode=force
```

When the annotation value is set to preferred , it gives priority to
  block mode export but has the flexibility to fallback to filesystem mode
  export if block mode export cannot be performed. If the annotation value is set to force , an error will be raised if block mode cannot be
  performed.

#### Configuring Block Mode Export Storage API Use â

By default, Veeam Kasten uses provisioner-specific network data
  transfer APIs for both block mode data upload and download, if
  available. If there is a need for more precise control over the use of
  these APIs, you can add one of the following annotations to a
  volume's StorageClass:

```
$ kubectl annotate storageclass ${STORAGE_CLASS_NAME} k10.kasten.io/block-mode-uses-storage-api=disable$ kubectl annotate storageclass ${STORAGE_CLASS_NAME} k10.kasten.io/block-mode-uses-storage-api=download-only$ kubectl annotate storageclass ${STORAGE_CLASS_NAME} k10.kasten.io/block-mode-uses-storage-api=enable$ kubectl annotate storageclass ${STORAGE_CLASS_NAME} k10.kasten.io/block-mode-uses-storage-api=upload-only
```

The annotation above is ignored for StorageClasses using
    the csi.vsphere.vmware.com provisioner and network data transfer
    APIs are always used.

#### Configuring Block Mode Export in VMware vSphere â

When exporting data
  in VMware vSphere environments it is possible to optionally enable the use
  of the Block Mode Export mechanism for all of the volume
  snapshots created by a policy, regardless of the Volume
Mode of each persistent volume.This is the preferred way to export snapshot data
  in a cluster with volumes provisioned by the csi.vsphere.vmware.com provisioner.
  Additionally, when exporting volume data to a Veeam Repository Location ,
  Block Mode Export must be enabled for all volume snapshots associated with the policy.

Using the Block Mode Export mechanism for all volume snapshots
  is enabled by explicitly selecting the Export snapshot data in block mode option in the export properties
  of the policy and then
  selecting an Object Storage Location , an NFS/SMB File Storage or a Veeam Repository Location profile as the destination for snapshot data in the Location Profile Supporting Block Mode field.

The location for metadata is specified by the Export Location Profile field, a required field in the dialog. When
  the Location Profile Supporting Block Mode field is an Object Storage Location or an NFS/SMB File Storage Location , then both values are required to be the same to
  ensure that both metadata and snapshot data are sent to the same
  location.

#### Configuring Block Mode Export to VBR â

To export snapshot data to a Veeam Repository Location from a compatible cluster it is required to use
  the Block Mode Export mechanism for all of the volume
  snapshots created by a policy, regardless of the Volume
Mode of each persistent volume.

First, ensure any required StorageClasses have enabled Block Mode Export .

Using the Block Mode Export mechanism for all volume snapshots
  is enabled by explicitly selecting the Export volume snapshot data to VBR option in the export properties
  of the policy and then
  selecting an available Veeam Repository Location profile as the destination.

The location for metadata is specified by the Export Location Profile field, which requires the selection of a separate Object Storage Location or an NFS/SMB File Storage Location .

## Scheduling â

There are four components to scheduling:

- How frequently the primary snapshot action should be performed
- How often snapshots should be exported into backups
- Retention schedule of snapshots and backups
- When the primary snapshot action should be performed

### Action Frequency â

Actions can be set to execute at an hourly, daily, weekly, monthly, or
  yearly granularity, or on demand. By default, actions set to hourly will
  execute at the top of the hour and other actions will execute at
  midnight UTC.

It is also possible to select the time at which scheduled actions will
  execute and sub-frequencies that execute multiple actions per frequency.
  See Advanced Schedule Options below.

Sub-hourly actions are useful when you are protecting mostly Kubernetes
  objects or small data sets. Care should be taken with more
  general-purpose workloads because of the risk of stressing underlying
  storage infrastructure or running into storage API rate limits. Further,
  sub-frequencies will also interact with retention (described below). For
  example, retaining 24 hourly snapshots at 15-minute intervals would only
  retain 6 hours of snapshots.

### Snapshot Exports to Backups â

Backups performed via exports, by default, will be set up to export
  every snapshot into a backup. However, it is also possible to select a
  subset of snapshots for exports (e.g., only convert every daily snapshot
  into a backup).

To maintain backup recovery points, once the policy is saved the export
    location profile can only be changed to a compatible location profile.
    The UI will enforce compatibility when editing a policy, but no
    compatibility enforcement is performed when editing the policy CR
    directly.

### Retention Schedules â

A powerful scheduling feature in Veeam Kasten is the ability to use a GFS retention
scheme for cost savings and compliance reasons. With this backup rotation
  scheme, hourly snapshots and backups are rotated on an hourly basis with
  one graduating to daily every day and so on. It is possible to set the
  number of hourly, daily, weekly, monthly, and yearly copies that need to
  be retained and Veeam Kasten will take care of both cleanup at every
  retention tier as well as graduation to the next one. For on demand
  policies it is not possible to set a retention schedule.

By default, backup retention schedules will be set to be the same as
  snapshot retention schedules but these can be set to independent
  schedules if needed. This allows users to create policies where a
  limited number of snapshots are retained for fast recovery from
  accidental outages while a larger number of backups will be stored for
  long-term recovery needs. This separate retention schedule is also
  valuable when limited number of snapshots are supported on the volume
  but a larger backup retention count is needed for compliance reasons.

The retention schedule for a policy does not apply to snapshots and
  backups produced by manual policy runs .
  Any artifacts created by a manual policy run will need to be manually
  cleaned up.

Restore points created by failed policy runs do not count towards
  retiring older restore points and are retained until there are enough
  newer restore points from successful policy runs to satisfy the
  retention counts. This situation can arise when policy runs are
  partially successful, such as when a policy run successfully backs up
  one app but fails on another or when export fails after successfully
  creating a local restore point. This outcome can lead to more restore
  points than expected, as failed policy runs may create restore points
  until the policy stops failing. If desired, restore points from failed
  runs can be manually deleted before reaching the point where there are
  sufficient new successful policy runs to meet the retention counts.

When restore points are retired, whether done manually or through a
    policy retention schedule, Veeam Kasten takes care of cleaning up the
    associated resources. The cleanup process is not immediate for all
    resources; some are removed right away, while others, such as backup
    data stored in an object store, may take a significant amount of time to
    be completely removed. Data references shared between restore points,
    aggregated data awaiting garbage collection, version retention for
    immutable backups, and safety windows for re-referencing data are among
    the reasons why retiring a restore point might not immediately free up
    space in the underlying storage.

Additionally, due to data deduplication, some retirements may result in
    minimal or no resource usage reclamation. It is important to note that
    the increase in storage usage when creating a restore point does not
    reflect the expected space reclamation once the restore point is cleaned
    up.

### Advanced Schedule Options â

By default, actions set to hourly will execute at the top of the hour
  and other actions will execute at midnight UTC.

The Advanced Options settings enable picking how many times and when
  actions are executed within the interval of the frequency. For example,
  for a daily frequency, what hour or hours within each day and what
  minute within each hour can be set.

The retention schedule for the policy can be customized to select which
  snapshots and backups will graduate and be retained according to the
  longer period retention counts.

By default, hourly retention counts apply to the hourly at the top of
  the hour, daily retention counts apply to the action at midnight, weekly
  retention counts refer to midnight Sunday, monthly retention counts
  refer to midnight on the 1st of each month, and yearly retention counts
  refer to midnight on the 1st of January (all UTC).

When using sub-frequencies with multiple actions per period, all of the
  actions are retained according to the retention count for that
  frequency.

The Advanced Options settings allows a user to display and enter times
  in either local time or UTC. All times are converted to UTC and Veeam
  Kasten policy schedules do not change for daylight savings time.

### Backup Window â

The Backup Window settings allow a user to select a time interval
  within which the policy will run. The policy is scheduled to run once at
  the Backup Window start time. If the selected time interval is too
  short, the policy run will not finish and will be canceled.

If the policy has an hourly frequency and the duration of the Backup
  Window exceeds 1 hour, the policy is also scheduled to run every 60
  minutes thereafter within the Backup Window.

Advanced Frequency Options can be used with Backup Window but with
  some limitations. The Backup Window settings override time settings
  (hours and minutes) selected in the Advanced Frequency Options. Advanced
  Frequency Options are not available for Hourly and Daily frequencies and
  only partially available for the other frequency options.

#### Staggering â

With staggering enabled, Veeam Kasten will automatically find an optimal
  start time and run the policy within the selected interval. Staggering
  allows Veeam Kasten the flexibility to stagger runs of multiple policies
  and reduce the peak load on the overall system.

## Application Selection and Exceptions â

This section describes how policies can be bound to applications, how
  namespaces can be excluded from policies, how policies can protect
  cluster-scoped resources, and how exceptions can be handled.

### Application Selection â

You can select applications by two specific methods:

- Application Names
- Labels

#### Selecting By Application Name â

The most straightforward way to apply a policy to an application is to
  use its name (which is derived from the namespace name). Note that you
  can select multiple application names in the same policy.

#### Selecting By Application Name Wildcard â

For policies that need to span similar applications, you can select
  applications by an application name wildcard. Wildcard selection will
  match all application that start with the wildcard specified.

For policies that need to span all applications, you can select all
  applications with a * wildcard.

#### Selecting No Applications â

For policies that protect only cluster-scoped resources and do not
  target any applications, you can select "None". For more information
  about protecting cluster-scoped resources, see Cluster-Scoped Resources .

#### Selecting By Labels â

For policies that need to span multiple applications (e.g., protect all
  applications that use MongoDB or applications that have been annotated
  with the gold label), you can select applications by label. Any
  application (namespace) that has a matching label as defined in the
  policy will be selected. Matching occurs on labels applied to
  namespaces, deployments, and statefulsets. If multiple labels are
  selected, a union (logical OR) will be performed when deciding to which
  applications the policy will be applied. All applications with at least
  one matching label will be selected.

Note that label-based selection can be used to create forward-looking
  policies as the policy will automatically apply to any future
  application that has the matching label. For example, using the heritage: Tiller (Helm v2) or heritage: Helm (Helm v3) selector will
  apply the policy you are creating to any new Helm -deployed
  applications as the Helm package manager automatically adds that label
  to any Kubernetes workload it creates.

### Namespace Exclusion â

Even if a namespace is covered by a policy, it is possible to have the
  namespace be ignored by the policy. You can add the k10.kasten.io/ignorebackuppolicy annotation to the namespace(s) you
  want to be ignored. Namespaces that are tagged with the k10.kasten.io/ignorebackuppolicy annotation will be skipped during
  scheduled backup operations.

### Exceptions â

Normally Veeam Kasten retries when errors occur and then fails the
  action or policy run if errors persist. In some circumstances it is
  desirable to treat errors as exceptions and continue the action if
  possible.

Examples of when Veeam Kasten does this automatically include:

- When a Snapshot policy selects multiple applications by label and creates durable backups by exporting snapshots, Veeam Kasten treats failures across applications independently. If the snapshot for an application fails after all retries, that application is not exported. If snapshots for some applications succeed and snapshots for other applications fail, the failures are reported as exceptions in the policy run. If snapshots for all applications fail, the policy run fails and the export is skipped. If the export of a snapshot for an application fails after retries, that application is not exported. If the export of snapshots for some applications succeed and others fail, the failures are reported as exceptions in the export action and policy run. If no application is successfully exported, the export action and policy run fail.

- If the snapshot for an application fails after all retries, that application is not exported. If snapshots for some applications succeed and snapshots for other applications fail, the failures are reported as exceptions in the policy run. If snapshots for all applications fail, the policy run fails and the export is skipped.
- If the export of a snapshot for an application fails after retries, that application is not exported. If the export of snapshots for some applications succeed and others fail, the failures are reported as exceptions in the export action and policy run. If no application is successfully exported, the export action and policy run fail.

In some cases, treating errors as exceptions is optional:

- Veeam Kasten normally waits for workloads (e.g., Deployments or StatefulSets) to become ready before taking snapshots and fails the action if a workload does not become ready after retries. In some cases the desired path for a backup action or policy might be to ignore such timeouts and to proceed to capture whatever it can in a best-effort manner and store that as a restore point.

When an exception occurs, the job will be completed with exception(s):

Details of the exceptions can be seen with job details:

Any exception(s) ignored when creating a restore point are noted in the
  restore point:

## Resource Filtering â

This section describes how specific application resources can either be
  included or excluded from capture or restoration.

Filters should be used with care. It is easy to accidentally define a
    policy that might leave out essential components of your application.

Resource filtering is supported for both backup and restore operations,
  whether performed through policies or manual actions. Separate resource
  filters can be specified for namespaced application resources and
  cluster-scoped resources. The recommended best practice is to create
  backup policies that capture all resources to future-proof restores and
  to use filters to limit what is restored.

In Veeam Kasten, filters describe which Kubernetes resources should be
  included or excluded in the backup. Backup operations without filters
  capture the default sets of API resources. Restore operations without
  filters restore all artifacts from the restore point or cluster restore
  point.

In an include filter, an entry that specifies only resource names or
  labels will match the resource types that are included by default. In an
  exclude filter, such entries apply to all resources selected by the
  include filter or by default.

### Filtering Resources by GVRN â

Resource types are identified by group, version, and resource type
  names, or GVR (e.g., networking.k8s.io/v1/networkpolicies ). Individual resources are
  identified by their resource type and resource name, or GVRN.

In a filter, an empty or omitted group, version, resource type or
  resource name matches any value. For example, if you set Group: apps and Resource: deployments , it will capture all Deployments no matter
  the API Version (e.g., v1 or v1beta1 ). Core Kubernetes types do not
  have a group name and are identified by just a version and resource type
  name (e.g., v1/configmaps ). The sentinel value core can be used in
  the group field of a filter to match the empty group and not all group
  values.

Filters reduce the resources in the backup by first selectively
  including and then excluding resources:

- If no include or exclude filters are specified, the default API resources belonging to an application are included in the set of resources to be backed up
- If only include filters are specified, resources matching any GVRN entry in the include filter are included in the set of resources to be backed up
- If only exclude filters are specified, resources matching any GVRN entry in the exclude filter are excluded from the default set of resources to be backed up
- If both include and exclude filters are specified, the include filters are applied first and then exclude filters will be applied only on the GVRN resources selected by the include filter

For a full list of API resources in your cluster, run kubectl api-resources .

### Filtering Resources by Labels â

Veeam Kasten also supports filtering resources by labels when taking a
  backup. This is particularly useful when there are multiple apps running
  in a single namespace. By leveraging label filters, it is possible to
  selectively choose which application to backup.

The snapshot creation process completes without generating output
    artifacts if all the resources are deselected. Attempting to export the
    snapshot fails with the error message "No artifacts provided." For
    instance, if no resources are selected during label-based filtering, the
    snapshot process will complete successfully without generating any
    artifacts. However, the export process will fail. Therefore, for a
    successful export, including at least one resource is crucial when
    creating a snapshot.

The rules from the previous section describing the use of include and
  exclude filters apply to label filters as well.

Multiple labels can be provided as part of the same filter if they are
  intended to be applied together. Conversely, multiple filters, each with
  their own label, can be provided together, signifying that any of the
  labels should match.

This filter includes resources with either app:mysql2 or app:mysql1 label

A filter can specify both GVRN and labels. Such filters match resources
  that satisfy both the GVRN and the specified labels.

### Filter Defaults â

Veeam Kasten implements useful defaults for resources included without
  filters, along with the ability to override and extend those defaults.
  There are different defaults for namespaced and cluster-scoped
  resources.

Veeam Kasten considers a Kubernetes namespace similarly to a namespaced
    object. By default, Veeam Kasten creates a namespace artifact as part of
    the application backup, and the namespace artifact is stored in a
    restore point, not a cluster restore point. Filters for application
    backup and restore can include or exclude the namespace artifact. This
    differs from namepace exclusion .

The default for backing up namespaced Kubernetes resources is to
  include:

- In-tree Kubernetes resources relating to the deployment of applications. For example, this includes, but is not limited to, specs for namespaces , workloads ( deployments , statefulsets , standalone pods ), services , configmaps , secrets , PVCs , serviceaccounts , and more. This excludes dynamically-created and low-level resources relating to the running of applications. Resources such as endpoints , events , replicasets , metrics , horizontalpodautoscalers , and volumesnapshots are not included by default.
- Specific OpenShift resource types: deploymentconfigs , buildconfigs , imagestreams , imagestreamtags , routes , and templates .
- Other custom resource types defined by installed customresourcedefinitions .

- For example, this includes, but is not limited to, specs for namespaces , workloads ( deployments , statefulsets , standalone pods ), services , configmaps , secrets , PVCs , serviceaccounts , and more.
- This excludes dynamically-created and low-level resources relating to the running of applications. Resources such as endpoints , events , replicasets , metrics , horizontalpodautoscalers , and volumesnapshots are not included by default.

The default for backing up cluster-scoped Kubernetes resources is to
  include:

- storageclasses from group storage.k8s.io
- customresourcedefinitions from group apiextensions.k8s.io
- clusterroles from group rbac.authorization.k8s.io
- clusterrolebindings from group rbac.authorization.k8s.io

Resource types that are not backed up by default can be included by
  adding them to a GVRN entry in the include filter. Once an include
  filter is specified, only resources that match a GVRN entry in the
  include filter are included in the set of resources to be backed up. To
  include additional resource types plus default resource types,
  include a GVRN entry for the defaults resource in the group actions.kio.kasten.io .

### Safe Backup â

For safety, Veeam Kasten automatically includes resources such as
  associated volumes (PVCs and PVs) when a StatefulSet, Deployment,
  DeploymentConfig, Pod, or Virtual Machine workload is included by
  filters. Such auto-included resources can be omitted by specifying an
  exclude filter.

### Filter Examples â

This table illustrates the use of filters when backing up an
  application:

| Include Filter | Exclude Filter | Captured in Restore Point | none | none | All default resources |
| :---: | :---: | :---: | :---: | :---: | :---: |
| none | none | All default resources |
| {Group: core, Resource: configmaps} | {Label: app:otherapp} | All configmaps except for any with labelapp:otherapp |
| {Label: app:my-app} | none | All default resources with the labelapp:my-app |
| {Group: "", Resource: deployments, Name: my-app} | none | my-appdeployment and its PVCs and volume snapshots, if any (Safe Backup) |
| {Group: "", Resource: deployment, Name: my-app} | {Resource: persistentvolumeclaims} | my-appdeployment spec only, no PVCs or volume snapshots |
| {Group: autoscaling, Resource: horizontalpodautoscalers} | none | Any horizontalpodautoscalers (not included by default) |
| {Group: autoscaling, Resource: horizontalpodautoscalers},{Group: actions.kio.kasten.io, Resource: defaults} | none | All default resources plus any horizontalpodautoscalers |

This table illustrates the use of filters when backing up cluster-scoped
  resources:

| Include Filter | Exclude Filter | Captured in Cluster Restore Point | none | none | All default cluster-scoped resources (storageclasses, customresourcedefinitions, clusterroles, clusterrolebindings) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| none | none | All default cluster-scoped resources (storageclasses, customresourcedefinitions, clusterroles, clusterrolebindings) |
| {Group: storage.k8s.io, Resource: storageclasses} | none | All storageclasses |
| none | {Resource: clusterrolebindings} | All default cluster-scoped resources except clusterrolebindings |
| {Group: admissionregistration, Resource: mutatingwebhookconfigurations},{Group: actions.kio.kasten.io, Resource: defaults} | none | All default cluster-scoped resources plus any mutatingwebhookconfigurations in cluster |

## Working With Policies â

### Using Policy Presets â

Operations teams can define multiple protection policy presets that
  specify parameters such as schedule, retention, location and
  infrastructure. A catalog of organizational policy presets and SLAs can
  be provided to the development teams with an intimate knowledge of
  application requirements, without disclosing credential and storage
  infrastructure implementation. This ensures separations of concerns
  while scaling operations in a cloud-native environment.

To create a policy preset, navigate to the Presets page under the Policies menu in the navigation sidebar. Then simply click Create New Preset and, as shown below, the policy preset creation
  section will be shown.

As can be seen, the workflow of the policy preset creation is quite
  similar to the policy creation. The major difference here is that the
  policy preset does not contain any application specific settings, which
  must be specified directly in the policy.

While creating (or editing) a policy the user can opt in to "Use a
  Preset". Users without list permissions on policy presets can manually
  enter the name of the policy preset to use, if they have been given that
  information.

Each policy created using a preset does not copy its configuration but
    refers to it. This means that every preset change also entails a change
    in the corresponding policies.

### Viewing Policy Activity â

After creating a policy and navigating back to the dashboard, the application status is updated from Unmanaged to Non-Compliant , indicating a policy exists but has not successfully run within the specified frequency. This status will change to Compliant upon successful completion of a scheduled or manual run of the policy. The page will now look similar to this:

Scrolling down on the page provides visibility into individual action activity. More detailed information can be obtained by clicking on the
  in-progress or completed jobs.

### Manual Policy Runs â

It is possible to manually run a policy by going to the Policies page and clicking the Run Once menu option on the desired policy. Note that
  unless an expiration time is specified, any artifacts created by this action will not be eligible for automatic retirement and will need to be manually removed.

It is also possible to run a policy manually on the Policy View page. First, navigate to the Policy View page by clicking on the policy row or clicking the View menu option on the desired policy. Then, click the Run Once button on the Policy View page.

### Pausing Policies â

It is possible to pause new scheduled runs of a policy by going to the Policies page
  and clicking the Pause menu option on the desired policy.

Once a policy is paused, it can be resumed by clicking the Resume menu option on the desired policy. Resuming a policy will allow begin running on it's scheduled frequency again.

Policies can also be paused and resumed from the Policy View page. First, navigate to the Policy View page by clicking on the policy row or clicking the View menu option on the desired policy. Then, click the Pause or Resume button on the Policy View page.

Paused policies do not generate skipped jobs and are ignored for the
    purposes of compliance. Applications that are only protected by paused
    policies are marked as unmanaged.

### Revalidating Policies â

Revalidation is useful when a Policy becomes invalid. Policies that are
  invalid will not run and can result in a breach of compliance. To revalidate a policy, go to the Policies page and click the Revalidate menu option on the desired policy.

### Editing Policies â

Editing a policy is possible from the Policies page using the Edit menu option, or from the Policy View page by clicking the Edit button. This opens a dialog to modify the schedule, retention, and other configuration details.

Policies, a Kubernetes Custom Resource (CR), can also be edited directly
  by manually modifying the CR's YAML through the dashboard or command
  line.

Changes made to the policy (e.g., new labels added or resource filtering
  applied) will take effect during the next scheduled policy run.

Careful attention should be paid to changing a policy's retention
  schedule as that action will automatically retire and delete restore
  points that no longer fall under the new retention scheme.

Editing retention counts can change the number of restore points
  retained at each tier during the next scheduled policy run. The
  retention counts at the start of a policy run apply to all restore
  points created by the policy, including those created when the policy
  had different retention counts. Editing Advanced Schedule Options can change when a policy runs in the future and which
  restore points created by future policy runs will graduate and be
  retained by which retention tiers.

Restore points graduate to higher retention tiers according to the
  retention schedule in effect when the restore point is created. This
  protects previous restore points when the retention schedule changes.

For example, consider a policy that runs hourly at 20 minutes after the
  hour and retains 1 hourly and 7 daily snapshots with the daily coming at
  22:20. At steady state that policy will have 7 or 8 restore points. If
  that policy is edited to run at 30 minutes after the hour and retain the
  23:30 snapshot as a daily, when the policy next runs at 23:30 it will
  retain the newly created snapshot as both an hourly and a daily. The 6
  most recent snapshots created at 22:20 will be retained, and the oldest
  snapshot from 22:20 will be retired.

When editing the export location profile on a policy, the updated
    location profile should only be changed to a profile that references the
    same file or object store as the previous location profile. Failing to
    do so will result in the previously exported backups being inaccessible
    by Veeam Kasten.

#### Disabling Backup Exports In A Policy â

Care should be taken when disabling backup/exports from a policy. If no
  independent export retention schedule existed, no new exports will be
  created and the prior exports will be retired as before. The exported
  artifacts will be retired in the future at the same time as the snapshot
  artifacts from each policy run.

If an independent retention schedule existed for export, editing the
  policy to remove exports will remove the independent export retention
  counts from the policy. Upon the next successful policy run, the
  snapshot retirement schedule will determine which previous artifacts to
  retain and which to retire based upon the policy's retention table.
  Retiring a policy run will retire both snapshot and export artifacts.
  Either snapshot or export artifacts for a retiring policy run may
  already have been retired if the prior export retention values were
  higher or lower than the policy retention values.

### Deleting A Policy â

A policy may be deleted from the Policies page, Policy View page, or through the API. However, for safety, deleting a policy does not remove the restore points it generated. Restore points from deleted policies must be manually deleted from the Application restore point view or via the API.

### Upgrading a Policy â

Periodic releases of Veeam Kasten include enhancements to improve backup data robustness and performance. In order to prepare the repository to take advantage of these enhancements, an upgrade may be required via each policy.

An eligible policy may be upgraded through the Upgrade menu option on the Policies page or by using the UpgradeAction API. Upgrading a Policy automatically upgrades all associated StorageRepositories .

Depending on the specific Veeam Kasten release and the amount of data
  protected through a policy, an upgrade workflow may take anywhere from a
  few minutes to several hours to complete. Users are advised to plan
  downtime when scheduling upgrades. Upgrading a policy requires exclusive
  access to the underlying backup data and metadata. Currently, Veeam
  Kasten requires that no import or export actions be performed on a given
  policy while an upgrade is in progress. If a user attempts to upgrade an
  export policy while the policy is running or its restore points are
  being imported elsewhere, that operation will be interrupted. During a
  policy upgrade, imports and exports of restore points created by the
  same policy will be put on hold until the upgrade is complete.

In the event that a policy or repository upgrade is interrupted or fails
    unpredictably (for example, due to a network failure), the user should
    wait until all pending actions against the policy have completed.
    Afterward, the user may retry the upgrade. If the upgrade continues to
    fail unpredictably, please contact Kasten support.

---

## Usage Restore

Once applications have been protected via a policy or a manual action,
  it is possible to restore them in-place or clone them into a different
  namespace.

Restore can take a few minutes as this depends on the amount of data
    captured by the restore point. The restore time is usually dependent on
    the speed of the underlying storage infrastructure as times are
    dominated by how long it takes to rehydrate captured data followed by
    recreating the application containers.

To speed up the Restore process and account for failures during the
    first or second attempt (maximum of 3 attempts), all successfully
    restored volumes will be retained for the next attempt. Only volumes
    that have been partially restored will be recreated.

## Restoring Existing Applications â

Restoring an application is accomplished via the Applications page. One
  needs to simply click the Restore option in the dropdown.

Alternatively, the Restore Points Page can be used to find a
  specific Restore Points and initiate the Restore using it:

While the UI uses the Export term for backups, no Import policy is
    needed to restore from a backup. Import policies are only needed when
    you want to restore the application into a different cluster.

At this point, one has the option to pick a restore point, a grouped
  collection of data artifacts belonging to the application, to restore
  from. As seen above, this view distinguishes manually generated restore
  points from automated policy-generated ones.

It also distinguishes between snapshots and backups. When both are
  present, as seen above, a layered box is shown to indicate more than one
  kind of restore point is present for the same data. If you want to
  restore a version of the application stack, clicking on the layered
  restore point will present the below option to select between the local
  snapshot and exported backup.

Selecting a restore point will bring up a side-panel containing more
  details on the restore point for you to preview, if needed, before you
  initiate an application restore.

Once you click Restore , the system will automatically recreate the
  entire application stack into the selected namespace. This not only
  includes the data associated with the original application but also the
  versioned container images. After the restore completes, you will be
  able to go back to your application and verify that the state was
  restored to what existed at the time the restore point was obtained.

A resource that doesn't currently exist in the namespace is always
  restored. The treatment of namespaced resources which already exist when
  the restore is invoked depends on the type of resource and the overwriteExisting flag.

Workloads are always
  restored, regardless of whether the overwriteExisting flag is used.

ServiceAccounts & non-namespaced resources (e.g. storage class) are only
  restored when missing from namespace/cluster, regardless of whether the overwriteExisting flag is used.

For other resources, existing objects are not restored and instead
  maintain their current state unless the overwriteExisting flag is
  used. When the flag is used, Immutable Secrets and ConfigMaps are also
  restored to the restore point version by re-creating the resources.

If desired, use restore_filtering to
  selectively control the namespaced objects that are restored.

## Restoring Deleted Applications â

The process of restoring a deleted application is nearly identical to
  the above process. The only difference is that, by default, removed
  applications are not shown on the Applications page. To discover them,
  you simply need to filter and select Removed .

Once the filter is in effect, you will see applications that Veeam
  Kasten has previously protected but no longer exist. These can now be
  restored using the normal restore workflow.

Alternatively, applications that were imported can be filtered by
  selecting Imported from the dropdown. In addition, imported
  applications will appear in the list of removed applications.

## Restoring Multiple Applications â

To initiate the restore of multiple applications, simply select them in
  the table:

It is possible to quickly identify and manage all applications selected
    by using the Selected filter:

Once one or more applications are selected, the [Restore
  selected] option is available in the Options menu:

Select restore points for each application. By default, the most recent
  restore point available will be preselected. Applications can also be
  excluded from the restore operation, for example, if no valid restore
  point exists that satisfies the needs of this restore operation.

You can specify a date range, such as during a ransomware attack, in
  order to choose the latest restore point containing unencrypted data,
  even if there are more recent restore points (potentially containing
  corrupted data). When a date range is selected, the most recent restore
  point within that range will be automatically selected for each
  application.

It is also possible to restore cluster-scoped resources along with
  selected applications:

When a valid restore point has been picked up for each selected
  application, click the "Next" button to proceed to the next step, Restore Configuration . This step contains modified options
  from the single application restore workflow. For instance, it is
  possible to add a prefix/suffix to the target namespace or filter
  resources.

Finally, the Summary screen provides a comprehensive
  overview of the upcoming operations, the relevant applications, and all
  the options enabled throughout the process.

After multiple restore is submitted a page of batch restore action will
  appear.

There will be also an action card in Action section on the Dashboard
    page.

## Limitations â

- Currently, Veeam Kasten only supports Allowed Topologies consisting of a single zone. If more than one zone is provided, Veeam Kasten will choose the first one.
- Changing the size of a PersistentVolumeClaim resource ( PVC ) on restore via transform is not supported.
- A resource's owner references will not be preserved if a transform changes the name of the resource to an auto-generated name ( generatedName ).

## Restore Filtering â

By default, a restore will bring back all artifacts and data captured
  during the backup process. However, there are times where only a subset
  of these artifacts are required and, to support that use case, the
  restore workflow supports two distinct filtering options.

- Artifact Filtering : Full-control over what artifacts and data to restore
- Data-Only Restore : Data-only restore (usually for a running application)
- Volume-Clones Restore : Volume-Clones restore (for restoring volumes only)

### Artifact Filtering â

As seen in the above diagram, it is possible to selectively bring back
  restore point artifacts (including volume snapshots). This is useful for
  scenarios such as single PVC restore or rolling back configuration
  updates. By default, all artifacts are selected for restore.

To preserve owner references, both the resource and its owners must be
    included by the filters.

### Data-Only Restore â

As seen in the above sections, it is also possible to select a Data-Only Restore . While, at the surface level, this is similar to
  just selecting all volume snapshots and no Kubernetes specs, there are a
  number of safety guardrails for successful data-only restores. The
  important differences to be aware of include:

- The Kubernetes workloads (Deployments, StatefulSets, etc.) captured in the restore point must exist in the namespace the application is being restored in
- The running Kubernetes workloads must have the same number of replicas as captured in the restore point
- The Kubernetes workloads must also have same volumes as were gathered in the restore point (number of volumes, names of the volumes)

These guardrails are in place as data-only restore is frequently used to
  bring older versions of data into a newer version of application code.
  In those scenarios, these checks are essential to ensure that a
  successful restore can be completed.

Data-Only Restore follows delete and restore from backup approach for
    the PVCs to maintain data integrity.

### Volume-Clones Restore â

The Volume-Clones restore feature enables the restoration of individual
  volumes into the existing application namespace without disrupting its
  operation or workloads.

This method is particularly beneficial when specific files need to be
  recovered from a backup without causing any disruption to the ongoing
  workload, and restoring the volume to an alternative namespace is not
  permitted or desirable.

The important differences from Data-Only Restore to be aware of
  include:

- The Kubernetes workloads (Deployments, StatefulSets, etc.) captured in the restore point can exist in the namespace where the application is being restored without being affected.
- The restored PVCs follow a predefined naming convention that includes the original PVC name with the Restore Point's creation timestamp appended to denote that they are clones.
- Volume-Clones restore does not automatically mount volumes to any Pods. The responsibility for mounting these volumes to the appropriate Pods lies with the user, providing flexibility in managing workload dependencies.
- Each cloned PVC has label k10.kasten.io/cloned: "true" to identify it as a clone. This label can be utilized as a policy exclusion to prevent the cloned volumes from being accidentally included in the backup policy.
- Once the cloned PVCs have served their intended purpose, it is recommended to remove them from the namespace. This ensures their exclusion from future backups, maintaining a clean environment, and preventing unnecessary data duplication.

### Instant Recovery â

Instant Recovery will get an exported restore point up and running much
  faster than a regular restore. This feature requires vSphere 7.0.3+ and
  a Veeam Backup server version V12 or higher. This is not supported on
  vSphere with Tanzu clusters at this time. Before using Instant Recovery,
  you should ensure that all Storage Classes in your Kubernetes clusters
  are configured to avoid placing new volumes in the Instant Recovery
  datastore. Please see this Knowledge Base
article for recommendations on Storage
  Classes for use with Instant Recovery. After an Instant Recovery has
  been completed, the migration step will start automatically. The
  migration occurs in the background while the recovered application runs
  from the network volume. Please see the Instant Recovery section for more details on how Instant Recovery works.

Currently Instant Recovery is only supported for Restore Actions , not
  Restore Policies. To use Instant Recovery, select the Enable Instant
  Recovery checkbox (this will only appear if all compatibility criteria
  are met) and set the target datastore name on vSphere to migrate the
  volume to. It is possible to use either the datastore name or datastore
  id from VBR. Alternatively set the InstantRestore and TargetDatastorage
  properties in the RestoreAction spec.

All restore features are supported with Instant Recovery.

### Resource Transformation â

By default, Veeam Kasten restores Kubernetes resources as they exist in
  the restore point. However, there are times when the restore target does
  not match the environment of the backup. For these situations, Veeam
  Kasten allows Kubernetes resource artifacts to be transformed on
  restore.

For example, if a restore point was created in one cloud provider and it
  should be restored into a cluster in a different cloud provider, it
  might be necessary to use a transform that updates the container image
  URLs in some resources, or one that changes storage class settings.

To apply transforms to the restored application, enable Apply transforms to restored resources under Restore After Import .

#### Add transforms using transform sets â

A complete guide of how to setup a transform set can be found here .

Clicking the Add a reference to an existing transform set will open a
  form for selecting a transform set.

Type the name of the transform set and click Add reference .

A reference to the transform set will then be added to the form. The SET label helps identify transforms which are stored and referenced
  rather than those that are created inline via Add new transform .

#### Add new custom transform â

A complete specification of how transforms can be configured can be
  found here .

Clicking the Add new transform will open a form for creating a new
  transform.

On the form, name the transform, select which resources the transform
  will be applied to, and then create one or more operations.

Each operation will have its own panel allowing customization and
  testing of the selected operation.

Operations can be tested against any resources to verify the outcome of
  the operations. The ability to apply transforms will provide flexibility
  in migration workflows between environments where more than just a like
  for like recovery is needed.

#### Extract transforms as transform set to reuse them â

To make a transform set from a sequence of transforms already defined
  click Extract this list as new transform set .

Type the name of new transform set and, optionally, its description.

Click Create transform set . After successful creation all transforms
  will be replaced with the reference of the created transform set.

## Cloning Applications â

By default, Veeam Kasten restores applications into the original
  namespace the restore point was created from. However, as the above
  image shows, the target namespace can be changed and new namespaces can
  be created at this point. In particular, this functionality can be used
  to extract only a few files or subset of the originally gathered data
  with requiring a complete rollback of the primary application. Other use
  cases include debugging and test/dev purposes or for cloning.

## PVC Renames â

During restores it is possible to rename PVCs depending on how the workload has been configured.
  While preparing the restore, transformation(s) targeting the relevant PVC(s) and specifying the new name(s) should be
  created.

For it to restore successfully to a new PVC, all references to the PVCs
  in other resources must also be transformed. For example, in a
  deployment that specifies a PVC claim name, this must also be updated
  e.g. replacing /spec/template/spec/volumes/0/persistentVolumeClaim/claimName with "new-name" in the example above. The same path can also be found in
  some StatefulSets and DeploymentConfigs setups and should also be
  updated in such cases.

If the StatefulSet makes use of volumeClaimTemplates then PVCs can
  partially be renamed by changing
  (/spec/volumeClaimTemplates/0/metadata/name ) as well as the reference in the volume mounts (e.g. /spec/template/spec/containers/0/volumeMounts/0/name ) along with renaming each PVC, assuming the replicas have separate PVCs. It is currently only possible to rename PVCs of a StatefulSet that uses volumeClaimTemplates` into a new namespace.

Renaming PVCs related to VirtualMachines involves renaming the PVCs and
  related DataVolumes (to have matching names), as well as transforming
  DataVolume references in the VirtualMachine resource. This also includes
  transforming the ownerReferences on the PVC(s) to reference the new
  DataVolume name. VirtualMachines can only be restored into a new
  namespace.

## Using an Alternate Location Profile â

An exported restore point can be selected to restore an application from
  a location outside the cluster. By default, it is assumed that the
  restore point exists at the location it was originally exported to.
  However, the "Alternate Location Profile" option can be used to select
  a different location profile to restore from. This can be useful if, for
  example, restore points have been copied or moved to a different
  location.

---

## Usage Transformsets

The Transform Sets page can be used to manage sets of transformations
  for later usage in policies and restores.

## Create transform set â

To create a new transform set, click the Add new button. A page with a
  form will be opened. Once all necessary fields are set, click the Create transform set button. The transform set will be validated and
  saved if the validation has passed.

## Import transforms from another transform set â

Import function is dedicated to reusability of already configured
  transform sets.

1. To import transforms from an existing transform set, click Import from transform set .

2. Select a transform set to import. Then select the desired transforms
  and click the Import selected .

1. Selected transforms will be added to the list.

## Transform set overview â

- Edit is the primary way to edit the content of the transform set.
- Duplicate will open the Create form prefilled with a particular transform set's content (Excluding name).
- YAML will show the YAML representation of the transform set.
- Delete will completely remove the transform set after confirmation.

## Transform setup â

Please see documentation about transforms to find out more about how to setup a transform.

## Testing of operation â

This is a simple example of using the Remove operation on one of the
  transform set objects to remove the metadata/labels path from the
  resource.

1. Click the Test operation .

1. Paste the YAML of the resource.

3. Click the arrow button in between Original and Transformed windows. In the current example, the operation will remove the whole
  metadata branch of the object. Thus it can be assumed the operation will
  work as intended.

All operations could be tested in bulk in a similar way by clicking the Test all operations button.

## Using preconfigured examples â

Under the Examples page of the Transform Sets menu, there is a
  collection of predefined examples for common use-cases.

Click Duplicate to create a transform set based on an example.

Examples cannot be removed, edited or used in policies or restore
    points.

---

## Usage Usage

The following sections provide an overview of how to perform common
  tasks using the Veeam Kasten dashboard. The equivalent actions can also
  be performed via a Kubernetes-native API and are documented in the API and Command Line section.

---

