## Kanister Documentation
### latest_kanister_kanister.md
## Extending Veeam Kasten with Kanisterï
- Kanister-Enabled Applications
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
Kanister, an extensible open-source framework used by Kasten's Veeam Kasten
platform, can be used for application-level data management on Kubernetes. It
allows domain experts to capture application specific data management tasks in
blueprints which can be easily shared and extended. The framework takes care of
the tedious details around execution on Kubernetes and presents a homogeneous
operational experience across applications at scale. Further, it gives you a
natural mechanism to extend the Veeam Kasten platform by adding your own code
to modify any desired step performed for data lifecycle management.
Below you can find useful resources about the project as well as
helpful information for testing Veeam Kasten with Kanister-enabled
applications.
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Execution Hooks
Configuring Security Context for Kanister Execution Hooks
- Configuring Security Context for Kanister Execution Hooks
- Kanister Pod Override
Configuring custom labels and annotations
- Configuring custom labels and annotations
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_resources.md
## Kanister Project Resourcesï
- Kanister-Enabled Applications
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
The Kanister project is completely open and developed under the Apache
License, Version 2.0. We encourage you to check out the following
useful resources.
- The Kanister Website
- Kanister Documentation
- The source code on GitHub
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_testing.md
## Kanister-Enabled Applicationsï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
Veeam Kasten defaults to volume snapshot operations when capturing data, but
there are situations where customization is required. For example, the best
way to protect your application's data may be to take a logical dump of the
database. This requires using tools specific to that database.
Kanister uses Blueprints to define these database-specific workflows and
open-source Blueprints are available for several popular applications. It's
also simple to customize existing Blueprints or add new ones.
When configured to do so, Veeam Kasten will automatically use Kanister
Blueprints and manage the resulting application-level Kanister artifacts.
### Configuring a Profileï
The Kanister Blueprints provided use object storage or NFS file storage to
manage data artifacts.
To make this storage accessible to Kanister Blueprints,
configure a Location Profile via the Location page of the Profiles
menu in the navigation sidebar or via the
CRD-based Profiles API. Specifying a Location Profile is
required when executing actions or defining policies for applications protected
with Kanister.
Note
Make sure that the credentials specified in the Location
Profile have sufficient permissions to perform LIST, PUT, GET, and DELETE for
the object storage location.
To learn more about configuring an NFS file storage location profile, refer to
this section.
### Installing Applications and Blueprintsï
Blueprints typically require no modifications to the application and most
Blueprints are written to work with respective standard Helm charts. The
Kanister GitHub repository contains several Blueprints that work with
respective Helm Charts.
### Logical Backupsï
If backups are required where data is captured completely at the data
service layer without requiring volume snapshots, the following
examples are available today:
- Logical Elasticsearch Backup
- Logical MongoDB Backup
- Logical MySQL Backup
- Logical PostgreSQL Backup
- Logical MySQL Backup for OpenShift
- Logical MongoDB Backup on OpenShift clusters
- Logical PostgreSQL Backup on OpenShift Clusters
- Logical Microsoft SQL Server Backup
### Managed Services Backupsï
Backups can be performed on Managed Services like Amazon RDS
by using the snapshot APIs of the service provider or by extracting
data directly from the service through logical dumps.
Following examples are available today:
### Amazon RDSï
- RDS PostgreSQL Backup
- RDS Aurora Backup
### Application-Consistent Backupsï
Application-consistent backups can be enabled if the data
service needs to be quiesced before a volume snapshot is initiated.
To obtain an application-consistent backup, a quiescing function,
as defined in the application blueprint, is first invoked and is
followed by a volume snapshot. To shorten the time spent while
the application is quiesced, it is unquiesced based on the blueprint
definition as soon as the storage system has indicated that a
point-in-time copy of the underlying volume has been started. The
backup will complete asynchronously in the background when the volume
snapshot is complete, or in other words after unquiescing the
application, Veeam Kasten waits for the snapshot to complete.
An advantage of this approach is that the database is not locked for
the entire duration of the volume snapshot process.
The following examples for application-consistent backups are
available today:
- Application-Consistent MongoDB Backup
- Application Consistent PostgreSQL Backup
- Application Consistent PostgreSQL HA Backup and Restore
### etcd Backup and Restoreï
If a backup of all cluster state stored in etcd is required, the etcd
cluster can be backed up and restored in case of catastrophic failure.
- etcd Backup (Kubeadm)
- etcd Backup (OpenShift Container Platform)
### Kafka Backup and Restoreï
For some types of data services, the best approach to data protection
may be for the service to stream data directly to object storage.
Kanister Blueprints are still used to initiate the stream and
to recover data, even though Kanister may not be in the data path.
Kafka, a data streaming platform, is an example of a data server
where using a Blueprint to initiate a backup stream may be the
preferred data protection strategy.
- Kafka Backup and restore
### K8ssandra Backup and Restoreï
K8ssandra is a cloud native distribution of Apache CassandraÂ® (Cassandra)
designed to run on Kubernetes. K8ssandra follows the K8s operator
pattern to automate operational tasks. This includes metric,
data anti-entropy services, and backup/restore tooling.
More details can be found here.
K8ssandra operator uses Medusa to backup and restore Cassandra data.
Veeam Kasten platform integrates with Medusa operator to perform backup and
restore of Cassandra data.
- K8ssandra Logical Backup
### Crunchy Data Postgres Operator Backup and Restoreï
The Postgres Operator (PGO) developed by Crunchy Data automates and
simplifies deploying and managing open source PostgreSQL clusters on
Kubernetes.
PGO provides some out of the box features like high availability, disaster
recovery, and monitoring, all over secure TLS communications.
More details can be found
here.
PGO uses open source pgBackRest to backup and
restore Postgres data. Veeam Kasten platform integrates with PGO to perform
backup and restore Postgres data using the operator APIs.
- Crunchy Data Postgres Operator Logical Backup and Restore
### Logical Backups to NFS File Storage Locationï
Kanister Blueprints that use kando to write and read data can
use NFS file storage locations. The following are some examples:
### Specifying a Kanister Blueprint for Your Applicationï
To request Veeam Kasten to use a custom Kanister Blueprint to manage a
workload (e.g., Deployment or StatefulSet), please (a) create the Blueprint in
the Veeam Kasten namespace (default kasten-io) and (b) annotate the
workload with the name of the created blueprint as follows:
Finally, note that the Blueprint used must have a backup and
restore action defined and ideally a delete action for
retirement too.
It is important to note that when a Kanister blueprint includes a
Backup action, it supersedes all other backup configurations and
settings. In the absence of a Kanister blueprint, Veeam Kasten will
automatically decide the most suitable backup mode (CSI, in-tree storage,
or GSB) for each PVC based on the PVC's specific attributes and
environmental conditions.
To take advantage of automated blueprint assignment by Veeam Kasten
without the need of manual annotating, please refer to
Blueprint Bindings.
### Use Case Testingï
Once you have installed your application, you will be able to use the
Veeam Kasten Dashboard to bring the application in compliance
and protect it by creating one or more policies. You can also subsequently
restore the application and its data to a previous version.
You can find more detailed instructions in the
Protecting Applications and
Restoring Applications sections of this documentation.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_hooks.md
## Kanister Execution Hooksï
- Kanister-Enabled Applications
- Kanister Project Resources
- Kanister Execution Hooks
Configuring Security Context for Kanister Execution Hooks
- Configuring Security Context for Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister Execution Hooks
Kanister Blueprints can be used to execute arbitrary functionality
before or after Veeam Kasten Actions.
To use a Blueprint to define an execution hook, create the Blueprint
in the Veeam Kasten namespace and add a reference to one of the Blueprint's
actions in a Policy or Action.
1. For snapshot/export actions, these execution hooks operate on
namespaces and can be set independently. The namespace is the source
namespace where the application being snapshotted/exported
is deployed. A hook blueprint can use this namespace via
template parameters like {{ .Namespace.Name }}
2. For restore actions, the execution hooks can operate on other Kubernetes
resources as well. The resource on which the hook would operate can be
selected on the dashboard as shown in the image below.
For example, if a StatefulSet is selected as the target resource,
a hook blueprint can access it via template parameters like
{{ .StatefulSet.Name }}. Only the resources created in the target
namespace can be selected as a subject. If no target resource is
selected, namespace would be the target resource.
Policies that apply to multiple namespaces will invoke hooks on each namespace.
Execution hooks do not require location profiles and hook Blueprint
actions cannot use template parameters and helpers such as
{{ .Profile.Location.Bucket }} or kando location.
For example, the following Blueprint defines a hook which updates a
label on the namespace that was snapshotted.
The following Blueprint defines a hook which checks if a
particular pod is ready after restore.
A hook reference may include preHook, onSuccess, or onFailure:
- A preHook action is executed before the Veeam Kasten Action (after
any Veeam Kasten setup steps have succeeded).
- An onSuccess action is executed after the Veeam Kasten Action has
succeeded.
- An onFailure action is executed when there is a
failure in an earlier step and Veeam Kasten has reached its retry limit.
Once successful, hook actions are not retried. If a preHook or
onSuccess action fails, it may be retried by Veeam Kasten. If an onFailure
action fails, Veeam Kasten will not retry. Execution hooks may or may not be
invoked when a Veeam Kasten Action is cancelled asynchronously.
Kanister artifacts returned as outputArtifacts by the hook
Blueprint action for preHook are passed as inputArtifacts to
any hook Blueprint action for onSuccess or onFailure.
For example, the following hook reference specifies an execution
hook for before a Restore Action and the error and non-error cases:
Look here to see how to embed hook references in
API objects.
Note, using VBR as a profile for blueprint based backups is currently
unsupported.
### Configuring Security Context for Kanister Execution Hooksï
By default, Pods provisioned as part of a Kanister Execution Hook action
run with root privileges.
If certain conditions are met, it is possible to change this behavior
(e.g., to configure Kanister Hooks in a rootless manner).
Note
The Kanister Pod Override
ConfigMap holds the highest priority.
If the pod's security context is defined in this ConfigMap,
it will override any other configuration.
Setting the forceRootInBlueprintActions flag to false
provides more flexibility for configuring the security context
for the Kanister Execution Hooks but should be done cautiously.
Once the flag is set to false, Veeam Kasten will use the security context
specified in the Kanister Blueprint's phase. If no security context is set for
the phase, Veeam Kasten will default to using an empty security context.
The security context can be set in the args.podOverride
section of any phase in the Kanister Blueprint for all functions
that deploy temporary Pods.
See the Kanister documentation
for a complete list of functions that support args.podOverride.
For example, the following section should be added to the phase's
args section to make it run as the user 1000:
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_override.md
## Kanister Pod Overrideï
- Kanister-Enabled Applications
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
Configuring custom labels and annotations
- Configuring custom labels and annotations
-
- Extending Veeam Kasten with Kanister
- Kanister Pod Override
In some cases, there can be a requirement to override Kanister
jobs pods specifications with custom values, such as tolerations for
taints, nodeSelector, or serviceAccountName. This can serve a
use-case when the pods need to be scheduled on a particular node, or use a
ServiceAccount which provides limited access. Changing these values
manually for Kanister Job pods will not be feasible.
To handle specifying the custom pod override for all Kanister Pods,
a ConfigMap named pod-spec-override must be created in the kasten-io
namespace. Veeam Kasten will merge the specifications configured in
pod-spec-override with other specifications set through Helm (such as
Root CA) and apply the merged configuration to all Kanister Job Pods.
Note
imagePullSecrets and securityContext should not be set via
pod-spec-override. If these configurations are set in this manner,
Veeam Kasten will ignore them.
When the helm option for providing a Root CA to Veeam Kasten
(i.e., cacertconfigmap.name) is enabled, the Kanister Backup/Restore workflow will
create a new ConfigMap, in the application namespace to
provide the Root CA to the sidecar. This ConfigMap in the application
namespace would be a copy of the Root CA ConfigMap residing in the Veeam Kasten
namespace, which would be deleted at the end of the workflow. To override this,
the Root CA ConfigMap can be created in the application namespace and the
respective Volume and VolumeMounts in the pod-spec-override in
kasten-io namespace.
For example, the following ConfigMap defines a Pod Specification, which
contains tolerations to node taints, and a nodeSelector.
This ConfigMap now would be merged with all Kanister job Pod
specifications. The Kanister restore job Pods would look like:
### Configuring custom labels and annotationsï
Kanister pods launched during Veeam Kasten operations can be configured with
additional custom labels and annotations through Helm Values.
Custom labels can be configured through Helm in following ways:
- Providing the path to one or more YAML files during
helm install or helm upgrade with the --values flag:
kanisterPodCustomLabels: "key1=value1,key2=value2"
kanisterPodCustomAnnotations: "key1=value1,key2=value2"
- Modifying the resource values one at a time with the
--set flag during helm install or helm upgrade:
--set=kanisterPodCustomLabels="key1=value1,key2=value2"
--set=kanisterPodCustomAnnotations="key1=value1,key2=value2"
Providing the path to one or more YAML files during
helm install or helm upgrade with the --values flag:
Modifying the resource values one at a time with the
--set flag during helm install or helm upgrade:
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_kafka_k8s_install.md
## Kafka Backup and restoreï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Kafka Backup and restore
To backup and restore Kafka topic data, Adobe S3 Kafka connector is used which periodically
polls data from Kafka and in turn, uploads it to S3. Each chunk of data is
represented as an S3 object. More details about the connector
can be found here.
During Restore, topic messages are purged before the restore
operation is performed. This is done to make sure that topic
configuration remains the same after restoration.
### Assumptionsï
- A ConfigMap containing the parameters for the connector is
present in the cluster.
- Topics should be present in the Kafka cluster before taking the backup.
- No consumer should be consuming messages from the topic during restore.
### Setup Kafka Clusterï
If it hasn't been done already, the strimzi Helm repository needs
to be added to your local configuration:
Install the Strimzi Cluster Operator from the strimzi Helm repository:
Setup Kafka Cluster with one ZooKeeper and one Kafka broker instance:
Add some data to the Kafka topic blogs using Kafka image
strimzi/kafka:0.20.0-kafka-2.6.0 provided by strimzi:
Note
To take backup of multiple topics, add comma separated
topic names in adobe-s3-sink.properties
### Create ConfigMapï
A config map with the following configuration should be provided
to the Kafka Connector:
- Details of the S3 bucket and Kafka broker address
- adobe-s3-sink.properties file containing properties related
to s3 sink Connector
- adobe-s3-source.properties file containing properties related
to s3 source Connector
- kafkaConfiguration.properties containing properties related to
Kafka server
### Create Blueprintï
To create the Blueprint resource that will be used by Veeam Kasten to
backup Kafka, run the command below:
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint gets created, annotate the ConfigMap with
the below annotations to instruct Veeam Kasten to use this Blueprint while
performing backup and restore operations on the Kafka instance.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_elasticsearch_install_logical.md
## Logical Elasticsearch Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical Elasticsearch Backup
If it hasn't been done already, the elastic Helm repository needs
to be added to your local configuration:
Install the Elasticsearch chart from the elastic Helm repository:
Once Elasticsearch is installed, create an index and
insert some documents in the Elasticsearch cluster by following
the commands mentioned
here.
To create a Blueprint resource, please run the command below:
Note
The Elasticsearch backup example provided above serves as a
blueprint template for logical backups. Please note that these examples
may need to be modified for specific production environments and setups.
As a result, it is highly recommended to carefully review and modify
the blueprints as needed before deploying them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, the StatefulSets will need to be
annotated to instruct Veeam Kasten to use the Blueprint while performing
backup operations on this Elasticsearch instance. The following example
demonstrates how to annotate the Elasticsearch StatefulSet with the
elasticsearch-blueprint.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_postgresql_install_logical_os.md
## Logical PostgreSQL Backup on OpenShift Clustersï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical PostgreSQL Backup on OpenShift Clusters
To demonstrate data protection for PostgreSQL provided and deployed
with OpenShift, the install should be performed according to the
documentation provided here.
Note
The secret that gets created after installation of PostgreSQL doesn't
have the ADMIN password that we have just specified and this password
is used by the Blueprint to connect to the PostgreSQL instance and
perform the data management operations.
To address the above issue, a secret should be created that will have this
ADMIN password with the key postgresql_admin_password.
A Blueprint resource should be created via the following command:
For PostgreSQL App Versions 14.x or older, Kanister tools version 0.85.0 is
required.
The PostgreSQL backup example provided above serves as a blueprint
template for logical backups on OpenShift clusters. Please note that these
examples may need to be modified for specific production environments
and setups on OpenShift. As a result, it is highly recommended to
carefully review and modify the blueprints as needed before deploying
them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, annotate the DeploymentConfig with
the below annotations to instruct Veeam Kasten to use this Blueprint while
performing data management operations on the PostgreSQL instance.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_postgresql-ha_install_app_cons.md
## Application Consistent PostgreSQL HA Backup and Restoreï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Application Consistent PostgreSQL HA Backup and Restore
If it hasn't been done already, the bitnami Helm repository
needs to be added to your local configuration:
Install the PostgreSQL HA chart from the bitnami Helm repository:
Use Veeam Kasten to backup and restore the application.
### Using Post Restore Hook Blueprintï
Note
The provided example in this section serves as a blueprint
template for achieving application-consistent PostgreSQL HA backup and
restore workflows. Please note that these examples may need to be
modified for specific production environments and setups. As a result,
it is highly recommended to carefully review and modify the blueprints
as needed before deploying them for production use.
If the PostgreSQL HA application is being restored into a different namespace,
the secondary instance pod postgresql-postgresql-ha-postgresql-1 will
go into CrashLoopBackOff since the connection info for the
primary/secondary nodes in the repmgr database points to the source
namespace. The following additional steps are needed to solve this issue:
1. Create a snapshot for the PostgreSQL HA application using Veeam Kasten.
2. Create a blueprint in the kasten-io namespace. This blueprint will
operate as a post restore hook
1. During restore, create a different namespace - postgresql-2
and select it as the target namespace
2. Under the Pre and Post-Restore Action Hooks section, select the
check box After - On Success and select the blueprint created
in step 2 as the action hook with action as postRestoreHook.
Select the checkbox Don't wait for workloads to be ready
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_postgresql_install_app_cons.md
## Application Consistent PostgreSQL Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Application Consistent PostgreSQL Backup
If it hasn't been done already, the bitnami Helm repository
needs to be added to your local configuration:
Install the PostgreSQL chart from the bitnami Helm repository:
Note
This is an example workflow that has been validated with PostgreSQL chart version 11.9.13.
For different versions of PostgreSQL and other requirements, modify the postgresql-hooks.yaml blueprint below as required.
Next create a file postgresql-hooks.yaml with the following contents
And then apply the file using:
Finally add the following annotation to the PostgreSQL StatefulSets to
instruct Veeam Kasten to use the above hooks when performing operations
on this PostgreSQL instance.
The PostgreSQL backup example provided above serves as a blueprint
template for achieving application-consistent backups. Please note that
these examples may need to be modified for specific production environments
and setups. As a result, it is highly recommended to carefully review and
modify the blueprints as needed before deploying them for production use.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_etcd_k8s_install.md
## etcd Backup (Kubeadm)ï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- etcd Backup (Kubeadm)
Assuming the Kubernetes cluster is set up through Kubeadm,
the etcd pods will be running in the kube-system namespace.
Before taking a backup of the etcd cluster, a Secret needs to
be created in a temporary new or an existing namespace,
containing details about the authentication mechanism used by
etcd. In the case of kubeadm, it is likely that etcd will
have been deployed using TLS-based authentication. A temporary
namespace and a Secret to access etcd can be created by running
the following command:
Note
If the correct path of the server keys and certificate is not provided,
backups will fail. These paths can be discovered from the command that
gets run inside the etcd pod, by describing the pod or looking into the
static pod manifests. The value for the flags etcdns and labels
should be the namespace where etcd pods are running and etcd pods' labels
respectively.
To avoid any other workloads from etcd-backup namespace being backed
up, Secret etcd-details can be labeled to make sure only this Secret
is included in the backup. The below command can be executed to label the
Secret:
### Backupï
To create the Blueprint resource that will be used by Veeam Kasten to backup
etcd, run the below command:
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, the Secret that was created
above needs to be annotated to instruct Veeam Kasten to use the Blueprint
to perform backups on the etcd pod.
The following command demonstrates how to annotate the Secret with
the name of the Blueprint that was created earlier.
Once the Secret is annotated, use Veeam Kasten to backup etcd using the
new namespace. If the Secret is labeled, as mentioned in one of the previous
steps, while creating the policy just that Secret can be included in the
backup by adding resource filters like below:
The backup location of etcd can be found by looking at the Kanister artifact
of the created restore point.
### Restoreï
To restore the etcd backup, log in to the host (most likely the Kubernetes
control plane nodes) where the etcd pod is running. Obtain the restore path
by looking into the artifact details of the backup action on the Veeam Kasten
dashboard, and download the snapshot to a specific location on the etcd pod
host machine (e.g., /tmp/etcd-snapshot.db). Downloading the snapshot is
going to be dependent on the backup storage target in use. For example, if
AWS S3 was used as object storage, the AWS CLI will be needed to obtain
the backup.
Once the snapshot is downloaded from the backup target, use the etcdctl CLI
tool to restore that snapshot to a specific location, for example
/var/lib/etcd-from-backup on the host. The below command can be used to
restore the etcd backup:
All the values that are provided for the above flags can be discovered from the
etcd pod manifest (static pod). The two important flags are
--data-dir and --initial-cluster-token. --data-dir is the
directory where etcd stores its data into and --initial-cluster-token
is the flag that defines the token for new members to join this etcd cluster.
Once the backup is restored into a new directory
(e.g., /var/lib/etcd-from-backup), the etcd manifest (static pod)
needs to be updated to point its data directory to this new directory
and the --initial-cluster-token=etcd-cluster-1 needs to be
specified in the etcd command argument. Apart from that the volumes
and volumeMounts fields should also be changed to point to new data-dir
that we restored the backup to.
### Multi-Member etcd Clusterï
In the cases when the cluster is running a multi-member etcd cluster, the same
steps that we followed earlier can be followed to restore the cluster with some
minor changes. As mentioned in the official etcd documentation
all the members of etcd can be restored from the same snapshot.
Among the leader nodes, choose one that will be used as a restore node and stop
the static pods on all other leader nodes. After making sure that the static
pods have been stopped on the other leader nodes, the previous step should be
followed on those nodes sequentially.
The below command, used to restore the etcd backup, needs to be changed from
the previous example before running it on other leader nodes:
The name of the host for the flags --initial-cluster and --name
should be changed based on the host (leader) on which the command is being run.
To explore more about how etcd backup and restore work, this
Kubernetes documentation
can be followed.
In reaction to the change in the static pod manifest, the kubelet will
automatically recreate the etcd pod with the cluster state that was backed up
when the etcd backup was performed.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_pgo_logical.md
## Crunchy Data Postgres Operator Logical Backup and Restoreï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Crunchy Data Postgres Operator Logical Backup and Restore
Crunchy Data Postgres Operator (PGO) uses the open-source pgBackRest
tool to backup and restore PostgreSQL data. The Veeam Kasten
platform integrates with PGO to perform backup and restore
PostgreSQL data using the operator APIs.
You can find the steps for installing PGO and PostgresCluster
here.
Before you begin, make sure you understand the known limitations
of the current integration.
Note
By default, Veeam Kasten utilizes built-in Kanister Blueprints for managing data
services like PGO and K8ssandra. If you wish to disable this feature, you
can use the kanister.managedDataServicesBlueprintsEnabled=false Helm flag
during the installation of Veeam Kasten.
### Known Limitationsï
Veeam Kasten uses PGO APIs to perform Backup and Restore of PostgreSQL data.
Since PGO uses the pgBackRest tool for managing backups,
please take a note of the following limitations:
- As of now, Veeam Kasten supports only in-place restoration. That means the
PostgresCluster backed up needs to be present to run restore.
- Restoring to a different namespace or migration is not supported as of now.
This can be done manually by cloning the PostgresCluster by following
the official documentation.
- PGO must be running before performing PostgresCluster restore.
- PGO performs PITR
to restore data. PostgreSQL PITR runs recovery till the next
commit it finds after the specified timestamp. Hence while restoring the
latest restore point, please make sure that there exists a commit after the
timestamp. If there is no database commit after the restore timestamp, the
restore job may get stuck with the error
recovery ended before configured recovery target was reached.
To recover from this situation, try to restore to an older restore point.
- PGO does not support an API for deleting the pgBackRest restore point.
Due to this reason, Veeam Kasten cannot delete PostgresCluster restore point
as per the Veeam Kasten Policy's retention configuration. It is recommended
to set the correct retention configuration in the PostgresCluster spec.
The details about managing PGO backup retention can be found
here.
Also, note that the PGO repository can be different from the Veeam Kasten
Location Profiles.
### PGO Backup with Veeam Kastenï
### Enable Manual Backups on PostgresClusterï
To allow Veeam Kasten to perform on-demand backup, manual backups
need to be enabled on the PostgresCluster. This can be done by applying the
following patch to the PostgresCluster CR
Where, REPO-NAME is the backup repository configured for PGO.
The complete list of supported backup repositories can be found
here.
Once PostgresCluster CR is patched to enable manual backups, a Veeam
Kasten Policy can be created to perform backups of the PGO application.
### PGO Restore with Veeam Kastenï
### Restore PostgresClusterï
PostgresCluster components are managed by the PGO.
The StatefulSet workloads are created by the operator when a
PostgresCluster Custom Resource is created. For this reason, the
StatefulSet objects do not need to be restored as they are managed by the
operator.
Follow the steps below to restore PostgresCluster without conflicting
with the functioning of the operator.
1. Select the Restore Point that needs to be restored.
2. Deselect all the artifacts under the Artifacts section.
3. Now, under Spec Artifacts, select only artifact(s) of type
postgresclusters.
4. Click Restore to perform the restore of PostgresCluster and data.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_mysql_install.md
## Logical MySQL Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical MySQL Backup
If it hasn't been done already, the bitnami Helm repository
needs to be added to your local configuration:
Install the MySQL chart from the bitnami Helm repository:
The following command can be used create the MySQL Blueprint in the
Veeam Kasten namespace.
Note
The MySQL backup example provided above serves as a blueprint
template for logical backups. Please note that these examples may need
to be modified for specific production environments and setups. As a
result, it is highly recommended to carefully review and modify the
blueprints as needed before deploying them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, add an annotation on the MySQL Deployment
to instruct Veeam Kasten to use the Blueprint when performing operations on
this MySQL instance.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_mysql_install_logical_os.md
## Logical MySQL Backup for OpenShiftï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical MySQL Backup for OpenShift
To demonstrate data protection for MySQL provided and deployed
with OpenShift, the install should be performed according to the
documentation provided here.
A Blueprint resource should be created via the following command:
Note
The MySQL backup example provided above serves as a blueprint
template for logical backups in an OpenShift environment. Please note
that these examples may need to be modified for specific production
environments and setups. As a result, it is highly recommended to
carefully review and modify the blueprints as needed before deploying
them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, annotate the DeploymentConfig with
the below annotations to instruct Veeam Kasten to use this Blueprint while
performing data management operations on the MySQL instance.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_mongodb_install_app_cons.md
## Application-Consistent MongoDB Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Application-Consistent MongoDB Backup
To obtain an application-consistent MongoDB backup where MongoDB is
first quiesced and then a snapshot of the underlying volume belong to
only the primary replica is performed, start by installing the
MongoDB chart from the bitnami Helm repository:
Note
Due to certain quirks in the MongoDB chart, you must use
mongodb, the name of the chart, in the Helm release name
below. Otherwise, the below test blueprint will be unable to find
the right MongoDB secret required for authentication.
The example workflow has been validated with the latest version of the MongoDB
helm chart. For other versions, modify the mongodb_hooks.yaml blueprint below
as required.
If it hasn't been done already, the bitnami Helm repository needs
to be added to your local configuration:
Next, create a file mongodb_hooks.yaml with the following contents:
And then apply the file using:
If MongoDB chart is installed specifying existing secret by setting
parameter --set auth.existingSecret=<mongo-secret-name>, secret name in the
blueprint mongodb_hooks.yaml needs to be modified at
following places:
actions.backupPrehook.phases[0].objects.mongoDbSecret.name:
<mongo-secret-name>
actions.backupPosthook.phases[0].objects.mongoDbSecret.name:
<mongo-secret-name>
Finally add the following annotation to the MongoDB Deployments to instruct
Veeam Kasten to use the above hooks when performing operations on this MongoDB
instance.
The MongoDB backup example provided above serves as a blueprint
template for achieving application-consistent backups. Please note that
these examples may need to be modified for specific production environments
and setups. As a result, it is highly recommended to carefully review and
modify the blueprints as needed before deploying them for production use.
Note that certain quirks in the MongoDB chart are addressed in the provided
instructions, but additional modifications may be required for different
MongoDB versions or custom setups.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_k8ssandra_policy.md
## K8ssandra Logical Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- K8ssandra Logical Backup
K8ssandra operator uses Medusa to backup and restore Cassandra data.
Steps for installing the K8ssandra operator with Medusa can be found
here.
Note
By default, Veeam Kasten uses built-in Kanister Blueprints for managing data
services such as PGO and K8ssandra. If you wish to disable this feature, you
can use the kanister.managedDataServicesBlueprintsEnabled=false Helm flag
during the installation of Veeam Kasten.
### Create K8ssandra Backup Policyï
K8ssandra components are managed by the K8ssandra operator. The StatefulSet
workloads are created by the operator when a Cassandra Custom Resource is
created. For this reason, the StatefulSet objects do not need to be backed up
as they are recreated by the operator. Medusa uses CassandraDatacenter
resource to backup and restore Cassandra data. To backup Cassandra
data with Veeam Kasten, create a policy with Include Filters to include
only the CassandraDatacenters needed to be backed up.
To create a policy with Include Filters -
1. Open the Veeam Kasten dashboard, go to Policies and click on
Create New Policy.
2. Specify a name of your choice (e.g. k8ssandra-backup) for the policy,
set backup frequency, and select the application by name.
3. To add filters, click on Select Application Resources ->
Filter Resources.
4. In the Include Filters section, click on Add a filter.
Check Resources box and add cassandradatacenters resource name.
Finally, click Add Filter and create the policy.
Once the policy is created, the backup operation can be performed on the
application by clicking Run Once action.
### Known Limitationsï
Veeam Kasten relies on Medusa operator deployed with K8ssandra
to perform backup and restore operations. Therefore,
the following limitations exist:
- The K8ssandra operator must be running before
performing restores
- Only in-place restores are possible
- The MedusaRestoreJob custom resource must be present
in the same namespace during restore operations
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_rds_postgres_install.md
## RDS PostgreSQL Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- RDS PostgreSQL Backup
RDS PostgreSQL backup can be performed by taking RDS snapshot of the running DB
instance.
### Prerequisitesï
The access credentials associated with the location profile should have
these permissions to perform RDS operations.
### Create Secret and ConfigMapï
To facilitate Veeam Kasten to connect to the RDS instance, Veeam Kasten
needs RDS instance details and the username, password
to login to the database created in RDS.
This information is provided by creating ConfigMap and Secret
Kubernetes resources.
Create a Kubernetes secret to store PostgreSQL credentials into
rds-app namespace. If there are other RDS instances,
multiple ConfigMap/Secret pairs can be created to have the details
of those RDS instances.
Create a ConfigMap in rds-app namespace which contains
information to connect to the RDS DB instance
### Annotate the ConfigMapï
The ConfigMap containing connection info will need to be annotated with
an annotation of form kanister.kasten.io/rds: rds-postgres to instruct
Veeam Kasten to perform backup and restore operations on this RDS PostgreSQL
DB instance. The following example demonstrates how to annotate
the dbconfig ConfigMap with the RDS Annotation.
Finally, use Veeam Kasten to backup and restore the RDS instance.
Warning
Here, RDS snapshots are created to
perform backups. These operations are prone to fail if Manual snapshots quota
is reached (which is 100 by default).
Make sure that correct retention policies are set to
avoid getting into this issue.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_mongodb_install_logical.md
## Logical MongoDB Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical MongoDB Backup
If it hasn't been done already, the bitnami Helm repository needs
to be added to your local configuration:
Install the MongoDB chart from the bitnami Helm repository:
To create a Blueprint resource, please run the command below:
Note
The MongoDB backup example above serves as a blueprint template
for logical backups. Please note that these examples may need to be
modified for specific production environments and setups. As a result,
it is highly recommended to carefully review and modify the blueprints
as needed before deploying them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
If MongoDB chart is installed specifying existing secret by setting
parameter --set auth.existingSecret=<mongo-secret-name>, secret name in the
blueprint mongo-blueprint.yaml needs to be modified at
following places:
actions.backup.phases[0].objects.mongosecret.name:
<mongo-secret-name>
actions.restore.phases[0].objects.mongosecret.name:
<mongo-secret-name>
Once the Blueprint is created, we will have to annotate the StatefulSet with
the correct annotation to instruct Veeam Kasten to use the Blueprint while
performing operations on this MongoDB instance.
The following example demonstrates how to annotate the MongoDB StatefulSet with
the mongodb-logical Blueprint.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_rds_aurora_install.md
## RDS Aurora Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- RDS Aurora Backup
Aurora DB cluster backup can be performed by taking RDS snapshot of
the running DB cluster.
### Prerequisitesï
The access credentials associated with the location profile should have
these permissions to perform RDS operations.
### Create ConfigMapï
To facilitate Veeam Kasten to connect to the Aurora DB cluster, a ConfigMap
Kubernetes resource can be created with the details of the DB cluster.
Create aurora-app namespace, if required.
Create a ConfigMap in aurora-app namespace to store the Aurora DB cluster
details.
### Create Blueprintï
A Blueprint resource should be created via the following command:
Alternatively, use the Blueprints page on the Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, annotate the ConfigMap with
the below annotations to instruct Veeam Kasten to use this Blueprint while
performing data management operations on the RDS Aurora DB cluster.
Finally, use Veeam Kasten to backup and restore the RDS Aurora DB cluster.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_postgresql_install_logical.md
## Logical PostgreSQL Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical PostgreSQL Backup
If it hasn't been done already, the bitnami Helm repository
needs to be added to your local configuration:
Install the PostgreSQL chart from the bitnami Helm repository:
The following command can be used to create the PostgreSQL Blueprint in the
Veeam Kasten namespace:
For PostgreSQL App Versions 14.x or older, Kanister tools version 0.85.0 is
required.
Note
The PostgreSQL backup example provided above serve as a blueprint
template for logical backups. Please note that these examples may need
to be modified for specific production environments and setups. As a
result, it is highly recommended to carefully review and modify the
blueprints as needed before deploying them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, add an annotation on the PostgreSQL Deployment
to instruct Veeam Kasten to use the Blueprint when performing operations on
this PostgreSQL instance.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_mssql_install.md
## Logical Microsoft SQL Server Backupï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical Microsoft SQL Server Backup
MS SQL Server is a relational database developed by Microsoft.
The example below covers SQL Server instances running natively
on Kubernetes. Use the following commands to deploy the SQL Server
using Kubernetes manifests.
The following command can be used to create the MS SQL Server Blueprint in the
Veeam Kasten namespace.
Note
The provided Microsoft SQL Server backup example serves as a blueprint
template for logical backups on Kubernetes. Please note that these
examples may need to be modified for specific production environments
and setups. As a result, it is highly recommended to carefully review and
modify the blueprints as needed before deploying them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, add an annotation to the SQL Server Deployment
to instruct Veeam Kasten to use the Blueprint when performing operations on
this instance.
Finally, use Veeam Kasten to backup and restore the application.
### Known Limitationsï
Currently, the backup process in the Kanister Blueprint creates
the temporary database backup files in the same volume as the
database. Due to this, it is necessary to use a PVC at least
twice the size of the database.
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_etcd_ocp_install.md
## etcd Backup (OpenShift Container Platform)ï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- etcd Backup (OpenShift Container Platform)
Assuming the Kubernetes cluster is set up through OpenShift Container Platform,
the etcd pods will be running in the openshift-etcd namespace.
Before taking a backup of the etcd cluster, a Secret needs to be created
in a temporary new or an existing namespace, containing details about
the etcd cluster endpoint, etcd pod labels and namespace in which the etcd pods
are running. In the case of OCP, it is likely that etcd pods have
labels app=etcd,etcd=true and are running in the namespace
openshift-etcd.
A temporary namespace, and a Secret to access the etcd member can be created by
running the following commands:
Note
Make sure that the provided endpoints, labels and etcdns values
are correct. Veeam Kasten uses the labels provided above to identify a member
of the etcd cluster and then takes backup of the running etcd cluster.
To figure out the value for endpoints flag, the below command can be used:
To avoid any other workloads from etcd-backup namespace being backed
up, Secret etcd-details can be labeled to make sure only this Secret
is included in the backup. The below command can be executed to label the
Secret:
### Backupï
To create the Blueprint resource that will be used by Veeam Kasten to
backup etcd, run the below command:
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
Once the Blueprint is created, the Secret that was created above
needs to be annotated to instruct Veeam Kasten to use this Secret with the
provided Blueprint to perform backups on the etcd pod.
The following command demonstrates how to annotate the Secret with
the name of the Blueprint that was created earlier.
Once the Secret is annotated, use Veeam Kasten to backup etcd using the new
namespace. If the Secret is labeled, as mentioned in one of the previous steps,
while creating the policy, just that Secret can be included in the backup by
adding resource filters like below:
The backup location of etcd can be found by looking at the Kanister artifact
of the created restore point.
### Restoreï
To restore the etcd cluster, the same mechanism that is documented by
OpenShift
can be followed with minor modifications. The OpenShift documentation provides
a cluster restore script (cluster-restore.sh), and that restore script
requires minor modifications as it expects the backup of static pod
manifests as well which is not taken in this case. The modified version of
the restore script can be found on here.
Before starting the restore process, make sure these prerequisites are met:
1. Create a namespace (for example etcd-restore) where Veeam Kasten restore
would be executed:
$ oc create namespace etcd-restore
2. Create a Persistent Volume and Persistent Volume Claim in the namespace
etcd-restore created in the above step. These resources are needed
to copy backed-up etcd data to the leader node to perform restore operation
$ oc --namespace etcd-restore apply -f \
     https://raw.githubusercontent.com/kanisterio/kanister/0.113.0/examples/etcd/etcd-in-cluster/ocp/blueprint-v2/pv-etcd-backup.yaml
$ oc --namespace etcd-restore apply -f \
     https://raw.githubusercontent.com/kanisterio/kanister/0.113.0/examples/etcd/etcd-in-cluster/ocp/blueprint-v2/pvc-etcd-backup.yaml
3. SSH connectivity to all the leader nodes
Create a namespace (for example etcd-restore) where Veeam Kasten restore
would be executed:
Create a Persistent Volume and Persistent Volume Claim in the namespace
etcd-restore created in the above step. These resources are needed
to copy backed-up etcd data to the leader node to perform restore operation
Among all the leader nodes, choose one node to be the restore node.
Perform the steps below to download the etcd backup file to the chosen
restore node:
1. Add a label etcd-restore to the node that has been chosen as the restore
node
$ oc label node <your-leader-node-name> etcd-restore=true
2. Perform the restore action on Veeam Kasten by selecting the target namespace
as etcd-restore. The Veeam Kasten restore action in this step only
downloads the backup file from the external storage to the restore node
Add a label etcd-restore to the node that has been chosen as the restore
node
The below steps should be followed to restore the etcd cluster:
1. Check if the the backup file is downloaded and available at
/mnt/data location on the restore node
2. Stop static pods from all other leader nodes by moving them outside of
staticPodPath directory (i.e., /etc/kubernetes/manifests):
## Move etcd pod manifest
$ sudo mv /etc/kubernetes/manifests/etcd-pod.yaml /tmp
## Make sure etcd pod has been stopped. The output of this
## command should be empty. If it is not empty, wait a few
## minutes and check again.
$ sudo crictl ps | grep etcd | grep -v operator
## Move api server pod manifest
$ sudo mv /etc/kubernetes/manifests/kube-apiserver-pod.yaml /tmp
## Verify that the Kubernetes API server pods are stopped. The output of
## this command should be empty. If it is not empty, wait a few minutes
## and check again.
$ sudo crictl ps | grep kube-apiserver | grep -v operator
3. Move the etcd data directory to a different location, on all leader nodes
that are not the restore nodes:
$ sudo mv /var/lib/etcd/ /tmp
4. Run the modified cluster-ocp-restore.sh script with the location
of etcd backup:
$ sudo ./cluster-ocp-restore.sh /mnt/data
5. Check the nodes to ensure they are in the Ready state.
$ oc get nodes -w
  NAME                STATUS  ROLES          AGE     VERSION
  host-172-25-75-28   Ready   master         3d20h   v1.23.3+e419edf
  host-172-25-75-38   Ready   worker         3d20h   v1.23.3+e419edf
  host-172-25-75-40   Ready   master         3d20h   v1.23.3+e419edf
  host-172-25-75-65   Ready   master         3d20h   v1.23.3+e419edf
  host-172-25-75-74   Ready   worker         3d20h   v1.23.3+e419edf
  host-172-25-75-79   Ready   worker         3d20h   v1.23.3+e419edf
  host-172-25-75-86   Ready   worker         3d20h   v1.23.3+e419edf
  host-172-25-75-98   Ready   worker         3d20h   v1.23.3+e419edf
6. If any nodes are in the NotReady state, log in to the nodes and remove
all of the PEM files from the /var/lib/kubelet/pki directory on each
node.
7. Restart the Kubelet service on all of the leader nodes:
$ sudo systemctl restart kubelet.service
8. Approve the pending CSRs (If there are no CSRs, skip this step)
## Check for any pending CSRs
$ oc get csr
## Review the details of a CSR to verify that it is valid
$ oc describe csr <csr_name>
## Approve all the pending CSRs
$ oc adm certificate approve <csr_name>
9. On the restore node, verify that the etcd container is running
$ sudo crictl ps | grep etcd | grep -v operator
10. Verify that the single etcd node has been started by executing
following command from a host which can access the cluster
$ oc get pods -n openshift-etcd | grep -v etcd-quorum-guard | grep etcd
  NAME                                             READY   STATUS      RESTARTS   AGE
  etcd-ip-10-0-143-125.ec2.internal                1/1     Running     1          2m47s
11. Delete and recreate other lost leader machines, one by one.
After these machines are recreated, a new revision is forced and
etcd scales up automatically. If you are running installer-provisioned
infrastructure, or you used the Machine API to create your machines,
follow these steps. Otherwise, you must create the new control plane
node using the same method that was used to originally create it.
Note
Do not delete and recreate the machine for the recovery(restore node) host
$ oc get machines -n openshift-machine-api -o wide
  NAME                                        PHASE     TYPE        REGION      ZONE         AGE     NODE                           PROVIDERID                              STATE
  clustername-8qw5l-master-0                  Running   m4.xlarge   us-east-1   us-east-1a   3h37m   ip-10-0-131-183.ec2.internal   aws:///us-east-1a/i-0ec2782f8287dfb7e   stopped
  clustername-8qw5l-master-1                  Running   m4.xlarge   us-east-1   us-east-1b   3h37m   ip-10-0-143-125.ec2.internal   aws:///us-east-1b/i-096c349b700a19631   running
  clustername-8qw5l-master-2                  Running   m4.xlarge   us-east-1   us-east-1c   3h37m   ip-10-0-154-194.ec2.internal   aws:///us-east-1c/i-02626f1dba9ed5bba   running
  clustername-8qw5l-worker-us-east-1a-wbtgd   Running   m4.large    us-east-1   us-east-1a   3h28m   ip-10-0-129-226.ec2.internal   aws:///us-east-1a/i-010ef6279b4662ced   running
  clustername-8qw5l-worker-us-east-1b-lrdxb   Running   m4.large    us-east-1   us-east-1b   3h28m   ip-10-0-144-248.ec2.internal   aws:///us-east-1b/i-0cb45ac45a166173b   running
  clustername-8qw5l-worker-us-east-1c-pkg26   Running   m4.large    us-east-1   us-east-1c   3h28m   ip-10-0-170-181.ec2.internal   aws:///us-east-1c/i-06861c00007751b0a   running
## Save the machine configuration of lost control plane node to a file
## on your file system
$ oc get machine clustername-8qw5l-master-0 -n openshift-machine-api \
  -o yaml > new-master-machine.yaml
## Edit the new-master-machine.yaml file that was created in the previous step
## to assign a new name and remove unnecessary field
  1. Remove the entire status section
  2. Change the metadata.name field to a new name
  3. Remove the spec.providerID field
  4. Remove the metadata.annotations and metadata.generation fields
  5. Remove the metadata.resourceVersion and metadata.uid fields
## Delete the machine of the lost control plane host
$ oc delete machine -n openshift-machine-api clustername-8qw5l-master-0
## Verify that the machine was deleted
$ oc get machines -n openshift-machine-api -o wide
## Create the new machine using the new-master-machine.yaml file
$ oc apply -f new-master-machine.yaml
## Verify that the new machine has been created.
## The new machine will be ready after phase changes from Provisioning to Running
$ oc get machines -n openshift-machine-api -o wide
12. Force etcd deployment, by running the below command:
$ oc patch etcd cluster -p='{"spec": {"forceRedeploymentReason": "recovery-'"$( date --rfc-3339=ns )"'"}}' --type=merge
## Verify all nodes are updated to latest version
$ oc get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type=="NodeInstallerProgressing")]}{.reason}{"\n"}{.message}{"\n"}'
## To make sure all etcd nodes are on the latest version wait for a message like below
AllNodesAtLatestRevision
3 nodes are at revision 3
13. Force rollout for the API Server control plane component:
## API Server
$ oc patch kubeapiserver cluster -p='{"spec": {"forceRedeploymentReason": "recovery-'"$( date --rfc-3339=ns )"'"}}' --type=merge
14. Wait for all API server pods to get to the latest revision:
$ oc get kubeapiserver -o=jsonpath='{range .items[0].status.conditions[?(@.type=="NodeInstallerProgressing")]}{.reason}{"\n"}{.message}{"\n"}'
15. Force rollout for the Controller Manager control plane component:
$ oc patch kubecontrollermanager cluster -p='{"spec": {"forceRedeploymentReason": "recovery-'"$( date --rfc-3339=ns )"'"}}' --type=merge
16. Wait for all Controller manager pods to get to the latest revision:
$ oc get kubecontrollermanager -o=jsonpath='{range .items[0].status.conditions[?(@.type=="NodeInstallerProgressing")]}{.reason}{"\n"}{.message}{"\n"}'
17. Force rollout for the Scheduler control plane component:
$ oc patch kubescheduler cluster -p='{"spec": {"forceRedeploymentReason": "recovery-'"$( date --rfc-3339=ns )"'"}}' --type=merge
18. Wait for all Scheduler pods to get to the latest revision:
$ oc get kubescheduler -o=jsonpath='{range .items[0].status.conditions[?(@.type=="NodeInstallerProgressing")]}{.reason}{"\n"}{.message}{"\n"}'
Stop static pods from all other leader nodes by moving them outside of
staticPodPath directory (i.e., /etc/kubernetes/manifests):
Move the etcd data directory to a different location, on all leader nodes
that are not the restore nodes:
Run the modified cluster-ocp-restore.sh script with the location
of etcd backup:
Check the nodes to ensure they are in the Ready state.
Restart the Kubelet service on all of the leader nodes:
Approve the pending CSRs (If there are no CSRs, skip this step)
On the restore node, verify that the etcd container is running
Verify that the single etcd node has been started by executing
following command from a host which can access the cluster
Delete and recreate other lost leader machines, one by one.
After these machines are recreated, a new revision is forced and
etcd scales up automatically. If you are running installer-provisioned
infrastructure, or you used the Machine API to create your machines,
follow these steps. Otherwise, you must create the new control plane
node using the same method that was used to originally create it.
Do not delete and recreate the machine for the recovery(restore node) host
Force etcd deployment, by running the below command:
Force rollout for the API Server control plane component:
Wait for all API server pods to get to the latest revision:
Force rollout for the Controller Manager control plane component:
Wait for all Controller manager pods to get to the latest revision:
Force rollout for the Scheduler control plane component:
Wait for all Scheduler pods to get to the latest revision:
Verify that all the etcd pods are in the running state. If successful,
the etcd cluster has been restored successfully
© Copyright 2017-2024, Kasten, Inc.
### latest_kanister_mongodb_install_logical_os.md
## Logical MongoDB Backup on OpenShift clustersï
- Kanister-Enabled Applications
Configuring a Profile
Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
Specifying a Kanister Blueprint for Your Application
Use Case Testing
- Configuring a Profile
- Installing Applications and Blueprints
Logical Backups
Managed Services Backups
Application-Consistent Backups
etcd Backup and Restore
Kafka Backup and Restore
K8ssandra Backup and Restore
Crunchy Data Postgres Operator Backup and Restore
Logical Backups to NFS File Storage Location
- Logical Backups
- Managed Services Backups
- Application-Consistent Backups
- etcd Backup and Restore
- Kafka Backup and Restore
- K8ssandra Backup and Restore
- Crunchy Data Postgres Operator Backup and Restore
- Logical Backups to NFS File Storage Location
- Specifying a Kanister Blueprint for Your Application
- Use Case Testing
- Kanister Project Resources
- Kanister Execution Hooks
- Kanister Pod Override
-
- Extending Veeam Kasten with Kanister
- Kanister-Enabled Applications
- Logical MongoDB Backup on OpenShift clusters
To demonstrate data protection for MongoDB provided and deployed
with OpenShift, the install should be performed according to the
documentation provided here.
A Blueprint resource should be created via the following command:
Note
The MongoDB backup example provided above serves as a blueprint
for logical backups on OpenShift clusters. Please note that these
examples may need to be modified for specific production environments
and setups on OpenShift. As a result, it is highly recommended to
carefully review and modify the blueprints as needed before deploying
them for production use.
Alternatively, use the Blueprints page on Veeam Kasten
Dashboard to create the Blueprint resource.
If MongoDB chart is installed specifying existing secret by setting
parameter --set auth.existingSecret=<mongo-secret-name>, secret name in the
blueprint mongo-dep-config-blueprint.yaml needs to be modified at
following places:
actions.backup.phases[0].objects.mongosecret.name:
<mongo-secret-name>
actions.restore.phases[0].objects.mongosecret.name:
<mongo-secret-name>
Once the Blueprint is created, annotate the DeploymentConfig with
the below annotations to instruct Veeam Kasten to use this Blueprint while
performing data management operations on the MongoDB instance.
Finally, use Veeam Kasten to backup and restore the application.
© Copyright 2017-2024, Kasten, Inc.
