## Api Documentation
### latest_api_cli.md
## API and Command Lineï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
Veeam Kasten exposes an API based on Kubernetes Custom Resource Definitions (CRDs)
and Kubernetes API Aggregation.
The simplest way to use the API is through kubectl.
To understand the API better refer to the following:
© Copyright 2017-2024, Kasten, Inc.
### latest_api_transforms.md
## Transformsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Structure
Transform Commands
Transform Example
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
Transform Structure
Transform Commands
Transform Example
- Transform Structure
- Transform Commands
- Transform Example
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Transforms
Transforms enable modifications to Kubernetes resources on restore. Restore
actions may include transforms to modify resources prior to creation in
the target environment.
Transforms are loosely modeled on JSON Patch (RFC-6902) which structures patches into
patch documents containing patch operations. Transforms follow a
similar structure to JSON Patch, with transform documents containing
transform commands. Transforms deviates from JSON Patch in its
support for regular expressions and path globbing.
To take advantage of Kubernetes native RBAC or reuse transforms, they
can be aggregated into TransformSet custom resources. Follow
Transform Sets page to learn more.
Transforms Overview
- Transform Structure
Transform Validation Requirements
Paths
Regex and Value
Path Wildcards
- Transform Validation Requirements
- Paths
- Regex and Value
- Path Wildcards
- Transform Commands
Test
Add
Remove
Copy
Move
Replace
- Test
- Add
- Remove
- Copy
- Move
- Replace
### Transform Structureï
A transform document is composed of transformation commands to be performed
on a subject. Each transformation command within the document is
performed in sequence. Processing halts if a transform command results in
an error. If the error is the result of a test failure processing will
continue to the next document, otherwise the restore will fail.
The example below contains two transform documents that contains two commands.
The first command, test, checks for the presence of the
'metadata/labels/release' element within a deployment resource. The
copy command following the test will execute if the test succeeds.
The second document will be evaluated independent of the first document.
The second document replaces the "/metadata/labels/component" key value
with "webserver" only if the value is "nginx".
Transforms supports six command operations test, add, remove,
copy, move and replace:
- test checks that an element exists
(and equals the value / matches the regexp if specified).
- add inserts a new element to the resource definition.
- remove deletes an existing element from the resource definition.
- copy duplicates an element, overwriting the value in the new path
if it already exists.
- move relocates an element, overwriting the value in the new path
if it already exists.
- replace replaces an existing element with a new element.
The subject property, as used in the example above, is used to transform
a subset of resources on restore. Only those resources matching the
group, version, resource or name will be selected from the
restore-point. Any empty subject property will match all values. The
subject above matches all deployment resources with any name, for any
group or version.
Each command has an operation, op, and a path. op specifies the
command operation to perform, path references the element within the
resource to operate on.
copy and move operations contain two paths - from for the source
element of the operation and path for the destination element of the
operation.
value contains either an element for comparison or a new element for
inclusion. Similarly regex can be used for comparing string elements or
processing elements into new string elements.
### Transform Validation Requirementsï
To create a valid transform, it is required to match
the following requirements:
- Transform's name should not be empty
- Transform should contain the spec
- Transform should contain at least one operation
- Transform should have at least one resource specified
### Pathsï
Every command has at least one path that references element(s) to operate
on. path and from are the only command properties that contain paths.
Paths consist of keys delineated by slashes (/). Keys can be object
property names or array indexes. For example,
"/spec/template/spec/containers/0" references the first container,
nginx, within the Deployment resource in the
example below.
Note that every path should be absolute, starting with /.
When adding an element to an array, "-" can be used in the path to
add an element at the and of the array.
Per RFC-6901, paths may contain
character escapes that allow inclusion of / characters within path
keys. For example
"/metadata/annotations/k10~1injectGenericVolumeBackupSidecar" will
reference the k10/injectGenericVolumeBackupSidecar key on the
annotations object within the resource metadata.  ~ characters
may be included by using ~0.
### Regex and Valueï
The function of value and regex properties depend on the operation
performed:
- test with value compares the element at path to value
for an exact match.
- test with regex compares the string element at path to
the regular expression in regex
- copy and move that include a regex property operate only
on from string elements that match the regular expression in
regex.
- copy and move that include a regex and a value property
operate only on from string elements that match regex and replace
destination path elements with expanded value strings. Capturing
groups in value are replaced to produce new values from regex
expressions.
- replace that include a regex property operate only on path
string elements that match the regular expression in regex.
- replace that include a regex and a value property operate
only on path string elements that match regex and replace
destination elements with expanded value strings. Capturing groups
in value are replaced to produce new values from regex
expressions.
value and regex do not apply to the remove and add
operations. A test operation with both value and regex
properties will produce and error.
See re2 for the syntax accepted by regex.
Capturing groups are referenced in value with identifiers starting with
a dollar-sign, "$", followed by the index of the capturing group.
The following example copies the mountPath from the first
volumeMounts entry to the second using regex and value with
capturing group replacement. The example uses the
Deployment resource below. The parent
path, /etc/nginx from mountPath is preserved and copied into the
second volumeMounts as /etc/nginx/config.
### Path Wildcardsï
Path wildcards allow path or from to apply to sets of elements. A
wildcard can be used in place of a path key to refer to all keys of an
object or array. Valid wildcards are * and ** - * references
all keys within one element, ** references all keys across multiple
consecutive elements.
Using the deployment example below, all spec
app labels can be accessed with "spec/**/app", expanding to two
concrete paths:
In the example below, all metadata labels can
be accessed with the path "**/metadata/labels/*" expanding to the four
concrete paths below:
Reference groups can be used in the path property of the copy and
move operations to form new groups of destination paths. Reference
groups allow for constructing new destination paths from source paths
with wildcards. Reference groups have keys that start with $ followed by
a numeric index of the wildcard. The index refers the wildcard ordinal,
counting from one. During processing, the reference group will be replaced
with concrete values of the indexed wildcard.
The following copy command example copies all selector matchLabels to
the spec template metadata.
### Transform Commandsï
All of the available command forms are listed below. Examples apply to
the Deployment resource below.
### Testï
Test that element at path exists. path may contain wildcards. If a
test fails, the remainder of the current transform document will be skipped
and processing of the next transform document will begin.
Test that element at path equals element in value. Order of map
keys is not significant. Otherwise, set of map keys and values must
match exactly. Arrays must be the same size and elements are compared in
order. If path contains wildcards, all elements referenced by path
must equal value. If a test fails, the remaining commands in the current
transform document will be skipped and processing of the next transform
document will begin.
Test that string element at path exists and matches regular expression
in regex. path may contain wildcards. If a test fails, the remaining
commands in the current transform document will be skipped and processing of
the next transform document will begin.
### Addï
Add value at path. If path references a map, the key will be
added or replaced. If path references an array, a new value will
be inserted. value must be a value JSON/YAML element. path may
contain wildcards.
The transform will fail if the path does not exist. The last key of
the path may contain a new map key or an array index.
### Removeï
Remove element at path.  path may contain wildcards.
The transform will fail if path does not exist.
### Copyï
Copy element at from to path. If path references a map, element
will be added/replaced as in add above. If path references an array,
copy will insert element as in add above. If from contains wildcards,
path may contain wildcard variables. If from is a concrete path,
path may contain wildcards.
The transform will fail if from or path does not exist. The last key
of path may contain a new map key or an array index.
Copy string element at from to path. If path references a map,
node will be added/replaced as in add above. If path references is
array, copy will insert element as in add above. If from element
matches regular expression in regex, perform copy of element with
replacement of capturing groups in value. If from contains wildcards,
path may contain wildcard variables. If from is a concrete path,
path may contain wildcards.
The transform will fail if from element does not exist or is not a string.
The transform will fail if path does not exist. The last key of path
may contain a new map key or an array index.
### Moveï
Move element at from to path. If path references a map, element
will be added/replaced as in add above. If path references an array,
copy will insert element as in add above.
Move string element at from to path. If path references a map,
element will be added/replaced as in add above. If path references
an array, copy will insert element as in add above. If regular
expression in regex matches element at from, perform replacement
of capturing groups in value. If from contains wildcards, path
may contain wildcard variables. If from is a concrete path, path
may contain wildcards.
The transform will fail if from element does not exist or is not a
string. Transform will fail if path does not exist. The last key of
path may contain a new map key or an array index.
### Replaceï
Replace element at path with the element in value. path must
reference an existing element. path may contain wildcards.
The transform will fail if path element does not exist.
Replace element at path with string element in value. If path
references a map, node will be added/replaced as in add above. If
path references is array, the element referenced will be replaced. If
element at path matches regular expression in regex, replace element
at path with value. Any capturing groups in value will be expanded
value. path may contain wildcard variables.
The transform will fail if path element does not exist or is not a
string.
### Transform Exampleï
Transform to change the storage class on a persistent volume claim (pvc):
Resource to operate on:
Transformed resource:
© Copyright 2017-2024, Kasten, Inc.
### latest_api_dr.md
## KastenDRï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
KastenDRReview
KastenDRRestore
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
KastenDRReview
KastenDRRestore
- KastenDRReview
- KastenDRRestore
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- KastenDR
The DR API group consists of two resources used to initiate a
Veeam Kasten Disaster Recovery (KDR) restore operation:
### KastenDRReviewï
KastenDRReview is an API resource used to fetch a list of available
Veeam Kasten Disaster Recovery (KDR) restore points for a provided source
cluster, from a provided location profile.
This resource provides the ability to track the progress of the operation,
report on any errors encountered, and provide details regarding
each available KDR restore point. The output is used to determine the id
of a specific KDR restore point to be used in defining a KastenDRRestore
resource.
### Create a KastenDRReview Exampleï
The following example illustrates how to create a KastenDRReview resource.
This resource connects to the specified Veeam Kasten location profile and
fetches KDR restore point information for the specified source cluster UID.
Creating a KastenDRReview resource assumes the following prerequisites:
- The location profile containing KDR restore points has been configured
- The k10-dr-secret secret
has been configured in the install namespace
Note
To avoid accidental, concurrent requests, only a single instance
of a KastenDRReview is allowed to exist.
### List KastenDRReviews Exampleï
The following example illustrates listing all KastenDRReviews resources.
The status field provides information about the available
KDR restore points, operation progress and any errors.
### Delete KastenDRReview Exampleï
KastenDRReview API resources can be deleted.
Functionally, this only serves to clean up the
API representation; no restore point data will be deleted.
### KastenDRReview API Typeï
The following is a complete specification of the KastenDRReview resource.
### KastenDRRestoreï
KastenDRRestore is an API resource used to manage and track
Veeam Kasten Disaster Recovery (KDR) restore operations.
This resource allows users to:
- Initiate a KDR restore operation from the latest
KDR restore point
- Initiate a KDR restore operation from a specific
restore point provided by the KastenDRReview process.
- Specify which resources to skip during the
restore process (e.g., secrets, profiles).
- Monitor the status of the restore operation,
including error information, cause and
the phase of the operation.
### Create a KastenDRRestore Exampleï
The following examples illustrate how to create a KastenDRRestore resource.
Creating a KastenDRRestore resource assumes the following prerequisites:
- The k10-dr-secret Secret
has been configured in the install namespace
To avoid accidental, concurrent requests, only a single instance
of a KastenDRRestore is allowed to exist.
### Use Latest KDR Restore Pointï
The following example fetches all KDR restore points for the
referenced source cluster and restores the latest available
as of the specified point in time.
This method can be used without first creating a KastenDRReview.
The pointInTime parameter is optional and can only be used for
review and restore operations from an immutable location profile.
### Use Specific KDR Restore Pointï
The following example restores using a specific KDR restore point (id),
from an existing KastenDRReview resource (kastenDRReviewRef).
### List KastenDRRestore Exampleï
The following example illustrates listing all KastenDRRestore resources
in a namespace. The phase column indicates the various step through which
restore operation is progressing.
### Delete KastenDRRestore Exampleï
KastenDRRestore API resources can be deleted.
Functionally, this only serves to clean up the
API representation.
### KastenDRRestore API Typeï
The following is a complete specification of the KastenDRRestore resource.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_concepts.md
## API Conceptsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
Veeam Kasten exposes an API based on Kubernetes Custom Resource Definitions (CRDs).
This section helps you learn about the Veeam Kasten platform and the
abstractions that that are available through the API.
Currently the following Veeam Kasten objects are supported:
- Profile - abstracts a location (e.g. object store,
NFS file store) and a set of credentials for accessing it. The Profile
location is used to store and transfer application meta-data and, in
some cases, actual persistent data during Veeam Kasten data management
operations.
- Policy - represents a collection of data
management actions that are configured to occur on a periodic or event
driven basis. Policies would typically encode a set of business rules
and translate them to specific actions that Veeam Kasten will apply on the
applications it has discovered.
- PolicyPreset - is a predefined set of settings
that can easily be applied to a Policy. A PolicyPreset can represent
organizational SLAs requiring a user to specify only the application
details to be used in a Policy.
- Applications - abstracts an application
that has been automatically discovered on the cluster where Veeam Kasten
is running. The application object encapsulates information about all
stateful and stateless resources that comprise the application.
- Action - represents a data management operation
that Veeam Kasten perform. Actions can be initiated on demand or as part
of a policy. A number of different types of actions are supported.
- RestorePoint - created as a result of a backup
or import action, a RestorePoint represents a version-in-time of an
application that has been captured by Veeam Kasten and that can be restored
using a restore action.
- StorageRepository - a representation of
where and how Veeam Kasten stores its exported backup data. These objects
provide a mechanism of more precisely managing and monitoring low-level
data layout.
- KastenDR - Veeam Kasten Disaster Recovery (KDR)
enables the recovery of a Veeam Kasten instance in the event of
various disasters, including accidental deletion of Veeam Kasten resources,
failure of underlying cluster infrastructure, or malicious acts.
Its representation includes resources that fetch the list of available
KDR restore points and restore an instance from a KDR restore point.
- TransformSet - store a set of
Transforms as a custom resource. It provides more granular RBAC control,
and the possibility of repeated use for Transforms.
- BlueprintBinding - represents a selection of
resources in a cluster and a blueprint that Veeam Kasten will use for such
resources.
- StorageSecurityContext -
represents pod security context settings to access
target storage to execute backup and restore operations.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_restorepoints.md
## Restore Pointsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
RestorePoint
RestorePointContent
ClusterRestorePoint
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
RestorePoint
RestorePointContent
ClusterRestorePoint
- RestorePoint
- RestorePointContent
- ClusterRestorePoint
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Restore Points
### RestorePointï
A RestorePoint API resource is used to represent a
Application that is captured at a specific time as a result of a
BackupAction or a RestoreAction.
A RestorePoint resides in the namespace of the Application and
access to it can be controlled using Kubernetes RBAC role and binding
for the RestorePoint API.
### List RestorePoint Exampleï
The following example illustrates listing all RestorePoints for
a sample application.
### Get RestorePoint Details Exampleï
In addition to getting a RestorePoint, you can also query the details
associated with the restore point. You would use the details sub-resource
for that purpose.
### Delete RestorePoint Exampleï
For RestorePoints created by policy, RestorePoints will automatically be
deleted as part of the retention scheme that is specified.
A Veeam Kasten administrator may chose to not enable RBAC that allows deleting
RestorePoints directly in order to force such operations to happen through
policy retirement only.
Note
Currently, deleting a RestorePoint manually does not delete the underlying resources.
For all associated resources (e.g. persistent volumes, application-level artifacts, etc.) to be reclaimed,
see, Delete RestorePointContent Example
### Creating RestorePoint from RestorePointContent Exampleï
When an application which has previously been protected by Veeam Kasten
is deleted, the RestorePoints associated with the application are no
longer available, but the corresponding RestorePointContent resources
remain available. A Veeam Kasten administrator has the opportunity
re-create a RestorePoint that would be bound to the RestorePointContent.
The following example illustrates creating a RestorePoint in the mysql
namespace. The operation requires that the caller has read access to the
RestorePointContent resource.
### RestorePoint API Typeï
The following is a complete specification of the RestorePoint
resource.
### RestorePointContentï
A RestorePointContent API resource backs the content
of a RestorePoint.
When a RestorePoint exists for a given RestorePointContent, that
RestorePointContent resource is bound. If there is no corresponding
RestorePoint (e.g. application was deleted), then the resource is
unbound.
Deletion of a RestorePointContent resource frees up the artifacts
associated with the restore point content and deletes any bound
RestorePointContents.
Access to RestorePointContent is typically reserved for users with
Veeam Kasten administrative privileges through Kubernetes RBAC since
the resources are cluster-scoped.
### List RestorePointContent Exampleï
RestorePointContent resources can be listed similarly to RestorePoint
resources, but the operation is non-namespaced.
In addition, to get the RestorePointContent resources associated with
a specific Application, you can use a label selector to constrain your
query.
### Get RestorePointContent Details Exampleï
In addition to getting a RestorePointContent, you can also query the details
associated with the restore point content. You would use the details sub-resource for that purpose.
### Delete RestorePointContent Exampleï
In addition to policy-based deletion of RestorePoints and
RestorePointContents, you can explicitly delete a
RestorePointContent. Deleting a RestorePointContent will
cause its bound RestorePoints and all associated
resources (e.g. persistent volumes, application-level
artifacts, etc.) to be reclaimed.
Deleting a RestorePointContent resource creates a
RetireAction that can be examined to monitor
progress of the retirement.
Warning
Deletion of a RestorePointContent is permanent and overrides
retention by a Policy.
Some resources associated with the deleted restore point content
may be cleaned immediately, while others, such as backup data exported
to an object store, may take much longer to be completely removed. Data
references shared between restore points, aggregated data awaiting garbage
collection, version retention for immutable backups, and safety windows for
re-referencing data are among the reasons why retiring a restore point might
not immediately free up space in the underlying storage.
Additionally, due to data deduplication, some retirements may result
in minimal or no resource usage reclamation.
It is important to note that the increase in storage usage when creating
a restore point does not reflect the expected space reclamation once the
restore point is cleaned up.
The following example illustrates deleting a RestorePointContent.
The operation requires that the caller has delete access to the
RestorePointContent resource.
### RestorePointContent API Typeï
The following is a complete specification of the RestorePointContent
resource.
The RestorePointContent resource cannot be created directly.
### ClusterRestorePointï
A ClusterRestorePoint API resource is created by a
BackupClusterAction that captures cluster-scoped resources.
A RestoreClusterAction is used to restore cluster-scoped resources from
a ClusterRestorePoint.
Deleting a ClusterRestorePoint resource frees up the artifacts
associated with it.
Access to ClusterRestorePoint is typically reserved for users with
Veeam Kasten administrative privileges through Kubernetes RBAC since the
resources are cluster-scoped.
### List ClusterRestorePoint Exampleï
ClusterRestorePoint resources can be listed similarly to RestorePoint
resources, but the operation is non-namespaced.
### Delete ClusterRestorePoint Exampleï
In addition to policy-based deletion of ClusterRestorePoints,
a ClusterRestorePoint can be directly deleted.
Deleting a ClusterRestorePoint resource creates a
RetireAction that frees up the artifacts
associated with the ClusterRestorePoint and that can be
examined to monitor progress of the retirement.
Deletion of a ClusterRestorePoint is permanent and
overrides retention by a Policy.
The following example illustrates deleting a ClusterRestorePoint.
The operation requires that the caller has delete access to the
ClusterRestorePoint resource.
### ClusterRestorePoint API Typeï
The following is a complete specification of the ClusterRestorePoint
resource.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_k10apps.md
## Applicationsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Life Cycle and Namespaces
Application Operations
Veeam Kasten App API Type
Veeam Kasten App Details API Type
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
Life Cycle and Namespaces
Application Operations
Veeam Kasten App API Type
Veeam Kasten App Details API Type
- Life Cycle and Namespaces
- Application Operations
- Veeam Kasten App API Type
- Veeam Kasten App Details API Type
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Applications
Note
The Application resource is in developer
preview and a number of breaking changes to the resource API
schema may happen in subsequent releases.
An Application resource represents an application that
Veeam Kasten has been automatically discovered on the Kubernetes cluster.
The application encapsulates all stateless and stateful resources
that comprise it.
### Life Cycle and Namespacesï
Application resources are read-only and are automatically
instantiated by Veeam Kasten when it discovers applications that are
running on the Kubernetes cluster.
An Application resource is available in for each application
that is currently running in the cluster. This resource resides in the same
namespace as the application that it corresponds to.
When an application, for which Veeam Kasten has at least one existing
RestorePointContent from a previous backup,
is deleted from the cluster, a Application resource
representing the application is still available in the namespace where
Veeam Kasten is installed. The resource will be marked as a deleted
application, but it will be possible for an administrator to restore
the application.
Apps are also available to  track applications that have been
deleted from the Kubernetes cluster, but are available to be restored
based on an existing RestorePointContent
captured by Veeam Kasten.
### Application Operationsï
### List of Applicationsï
The Application API allows you to discover all applications
that are installed and currently present on the Kubernetes cluster.
### List of Deleted Applicationsï
The Application API allows you to discover applications
that Veeam Kasten can restore which have been previously deleted from
the cluster.
### Restore of Deleted Applicationsï
In addition to discovery of deleted applications, Veeam Kasten makes it
possible to restore an application that has been deleted but was
previously protected.
The procedure, which requires Veeam Kasten administrative privileges,
is as follows:
- Step 1: Find the RestorePointContent that corresponds to the desired
point-in-time.
- Step 2: Re-create the namespace where you would like to restore the
application.
- Step 3: Create a RestorePoint in the new namespace that is backed
by the RestorePointContent. See Creating RestorePoint from RestorePointContent Example for details.
- Step 4: Initiate a RestoreAction to restore the application from
the created RestorePoint. See RestoreAction for details.
### Get Application Componentsï
In addition to discovering the applications on the cluster, Veeam Kasten
also tracks all resources associated with the application. You can get a
summary of all resources (stateful and stateless) discovered in the context
of the application. This is done by querying a details sub-resource for the
particular application you are interested in.
### Initiate Backup for an Applicationï
Apps can be protected on a scheduled basis using a Policy or
in an ad hoc manner using a BackupAction.
For details see, Create a Backup Policy or
BackupAction.
### Veeam Kasten App API Typeï
The following is a complete specification of the Application resource.
The Application resource is read-only.
### Veeam Kasten App Details API Typeï
The following is a complete specification of the appDetails section
of the Application API. These fields are only available in the
Application API when the details sub-resource is used as shown in the
example above.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_storagesecuritycontexts.md
## StorageSecurityContextï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
StorageSecurityContextBinding
Example of StorageSecurityContext and StorageSecurityContextBindings Usage
StorageSecurityContext API Type
StorageSecurityContextBinding API Type
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
StorageSecurityContextBinding
Example of StorageSecurityContext and StorageSecurityContextBindings Usage
StorageSecurityContext API Type
StorageSecurityContextBinding API Type
- StorageSecurityContextBinding
- Example of StorageSecurityContext and StorageSecurityContextBindings Usage
- StorageSecurityContext API Type
- StorageSecurityContextBinding API Type
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
- Accessing Veeam Kasten
- API and Command Line
- StorageSecurityContext
A StorageSecurityContext custom resource (CR)
represents pod security context settings to access target storage
to execute backup and restore operations.
Once the StorageSecurityContext is created
and bound to specific storage using StorageSecurityContextBinding,
Veeam Kasten will use the parameters set in the StorageSecurityContext
for its internal pods, which access bound storage.
Note
### StorageSecurityContextBindingï
StorageSecurityContextBinding binds a StorageSecurityContext to a storage.
Warning
Bindings might be one of three types:
- Volume - binds StorageSecurityContext to a PV.
- StorageClass - binds StorageSecurityContext to a StorageClass.
- Provisioner - binds StorageSecurityContext to a Provisioner.
### Example of StorageSecurityContext and StorageSecurityContextBindings Usageï
- Create a StorageSecurityContext
- Create a StorageSecurityContextBinding
As an example, an NFS storage with the
filestore.csi.storage.gke.io StorageClass is used.
- NFS CSI driver should support VolumeSnapshots
- NFS CSI driver should support fsGroup
In this example, only UID and GID are set in the StorageSecurityContext.
However, if a target storage contains files or directories owned by
several different GIDs, SupplementalGroup should also be used to
enable Veeam Kasten to read all the data. Please note that after the restore,
the owner of files and directories will be set to the UID and GID
specified in the StorageSecurityContext.
### Create a StorageSecurityContextï
The following example illustrates how to create a StorageSecurityContext
for NFS storage:
For complete documentation of StorageSecurityContext CR,
please refer to StorageSecurityContext API Type.
When the StorageSecurityContext is applied, Veeam Kasten will start
a pod that reads the target storage with UID=1005 and GID=1006. If the target storage
contains files owned by other users,
which cannot be accessed
by the provided UID and GID, Veeam Kasten will fail
to complete the Export process.
### Create a StorageSecurityContextBindingï
The following example illustrates
how to create a StorageSecurityContextBinding to bind
the StorageSecurityContext named
"sample-storage-security-context" to all storages
created with filestore.csi.storage.gke.io Provisioner.
For complete documentation of StorageSecurityContextBinding CR,
please refer to StorageSecurityContextBinding API Type.
### StorageSecurityContext API Typeï
### StorageSecurityContextBinding API Typeï
© Copyright 2017-2024, Kasten, Inc.
### latest_api_reports.md
## Reportsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Report
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
Report
- Report
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Reports
Note
The Report resource is in developer preview and
a number of breaking changes to the resource API schema may happen
in subsequent releases.
### Reportï
A Report API resource captures information about the state
of the system at the time the report was generated as well
as select metrics collected from the Veeam Kasten Prometheus service.
A Report is produced by a
ReportAction when Veeam Kasten Reports are
enabled.
Enabling and viewing Reports in the Veeam Kasten dashboard or with
the API are discussed more fully in
Reporting.
### Report API Typeï
The following is a complete specification of the Report
resource.
### Retiring Reportsï
By default the reports are not retired. To set up a retention count,
update the policy spec to include the desired value:
© Copyright 2017-2024, Kasten, Inc.
### latest_api_repositories.md
## Repositoriesï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
StorageRepository
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
StorageRepository
- StorageRepository
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Repositories
### StorageRepositoryï
A StorageRepository API resource is used to represent how Veeam
Kasten backup data is stored at a particular location
(represented by a Profile<api_profile>).
Veeam Kasten will distribute backup data generated by a
Policy<api_policy> run into one or more repositories,
based on data type and deduplication domain.
The API gives the user an insight into the status of these
repositories, and provides a means of performing
maintenance and management actions on them.
### List StorageRepositories Exampleï
The following example illustrates listing all StorageRepositories
created by a policy backing up two applications, each
with PVCs.
### Get StorageRepositories Details Exampleï
In addition to getting a StorageRepository, you can also query the details
associated with the restore point. You would use the details
sub-resource for that purpose.
### Modify StorageRepository Background Maintenance Behaviorï
Veeam Kasten will periodically run maintenance on the
StorageRepositories it creates. Among other tasks, the maintenance
process tidies up unused data, detects inconsistent states, and
measures the overall storage usage over time. This behavior can be
disabled on a per-repository basis by modifying the spec.disableMaintenance
field. Additionally, the background operations performed on the
repository will, by default, have a 10-hour timeout. The timeout
can be customized as needed by setting the
spec.backgroundProcessTimeout field.
### Delete StorageRepository Exampleï
StorageRepository API resources can be deleted. Functionally, this only
serves to clean up the API representation; no backup data will be deleted,
and Veeam Kasten still tracks the associated repository data internally.
After deletion, if the repository is used again (e.g., by creating a new backup),
the StorageRepository API representation will be recreated.
### StorageRepository API Typeï
The following is a complete specification of the StorageRepository
resource.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_transformsets.md
## Transform Setsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Example TransformSet Operations
TransformSet API Type
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
Example TransformSet Operations
TransformSet API Type
- Example TransformSet Operations
- TransformSet API Type
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Transform Sets
A TransformSet custom resource (CR) is used to save and reuse the set of
Transforms to be used in
Restore Actions,
Restore Cluster Actions and
Policies.
### Example TransformSet Operationsï
- Create a TransformSet
- Update a TransformSet
- Using a TransformSet
- Delete a TransformSet
### Create a TransformSetï
The following example illustrates how to create a transform set that contains
two transforms, one of which changes the deadline parameter value to 300
seconds and another one scales deployments to 3 replicas.
### Update a TransformSetï
To update a TransformSet, edit the spec portion of a TransformSet CR
using your preferred method of submitting resource changes with kubectl.
Once the change is submitted, Veeam Kasten will re-validate the TransformSet
and update .status.validation accordingly.
Since Veeam Kasten processes API object changes asynchronously, to avoid
confusion with a previous TransformSet status, it is recommended as
convention that the status portion of the TransformSet is omitted
when submitting changes.
Warning
### Using a TransformSetï
The following example illustrates how to use a TransformSet
in a RestoreAction.
The TransformSet will be applied to the restored application.
### Delete a TransformSetï
A TransformSet can be deleted using the following command.
### TransformSet API Typeï
The following is a complete specification of a TransformSet CR.
To learn more about the transforms structure,
see Transforms.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_auditconfigs.md
## AuditConfigsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Creating an Audit Config
Updating an Audit Config
Deleting an Audit Config
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
Creating an Audit Config
Updating an Audit Config
Deleting an Audit Config
- Creating an Audit Config
- Updating an Audit Config
- Deleting an Audit Config
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- AuditConfigs
An AuditConfig custom resource (CR) is used to send Veeam Kasten
audit event logs to a cloud object store by using a reference to a
Location Profile.
### Creating an Audit Configï
When creating an AuditConfig, you first need to
create a Location Profile that points to a cloud
object store.
With a Location Profile already defined, you can now create an Audit Config
by executing the following commands:
The AuditConfig can assume four different statuses:
Status
Meaning
Pending
Created and waiting for Location
Profile
UpdateRequested
Audit Config or Location Profile has changed
DeleteRequested
Stop sending logs to this Location Profile
Success
Sending logs to this Location Profile
### Updating an Audit Configï
To update an AuditConfig, edit the spec portion using your preferred
method for submitting resource changes with kubectl.
Once the change is submitted, Veeam Kasten will re-validate the audit config
and update .status.validation accordingly.
This action will trigger the extended audit mechanism to update and send logs
to the updated Location Profile.
### Deleting an Audit Configï
You can delete an AuditConfig using the following command:
This action will trigger the extended audit mechanism to stop sending logs to
this Location Profile.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_blueprintbindings.md
## Blueprint Bindingsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Resource Selector
Example BlueprintBinding Operations
BlueprintBinding API Type
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
Resource Selector
Example BlueprintBinding Operations
BlueprintBinding API Type
- Resource Selector
- Example BlueprintBinding Operations
- BlueprintBinding API Type
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Blueprint Bindings
A BlueprintBinding custom resource (CR) is used to automate the assignment
of Kanister blueprints to applications. Once a BlueprintBinding is created,
Veeam Kasten will use it during snapshot, export and restore routines to
automatically run a desired blueprint for matching workloads including
workloads that are yet to be created in a cluster. You can learn more about
Kanister blueprints in this section.
A BlueprintBinding consists of two parts: a reference to a Kanister
blueprint and a resource selector. For resources that match the selector,
Veeam Kasten will automatically use the specified blueprint.
Warning
For complete documentation of the BlueprintBinding CR,
refer to BlueprintBinding API Type.
### Resource Selectorï
The resources portion of the blueprint binding spec indicates which
kind of resources this blueprint binding will apply to.
Note
For a resource to match the selector, it must meet all the requirements
from matchAll and at least one requirement from matchAny (if any).
A blueprint binding with no requirements is considered invalid.
Both matchAll and matchAny portions of resources represent a list
of resource requirements to meet. A single resource requirement can set
one of the following constraints:
- type: selects resources by group, version, resource and name (GVRN) values
- namespace: selects resources by namespace
- annotations: selects resources by annotations
- labels: selects resources by labels
### Example BlueprintBinding Operationsï
- Create a Blueprint Binding
- Update a Blueprint Binding
- Delete a Blueprint Binding
### Create a Blueprint Bindingï
The following example illustrates how to create a blueprint binding
which will automatically apply a blueprint to all statefulsets
in the group apps that has no custom blueprint annotations.
### Update a Blueprint Bindingï
To update a BlueprintBinding, edit the spec portion of a BlueprintBinding
CR using your preferred method of submitting resource changes with kubectl.
E.g. disabled: true can be added to the spec to
disable the blueprint binding.
Once the change is submitted, Veeam Kasten will re-validate the
BlueprintBinding and update .status.validation accordingly.
### Delete a Blueprint Bindingï
You can delete a BlueprintBinding using the following command.
### BlueprintBinding API Typeï
The following is a complete specification of the BlueprintBinding CR.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_policypresets.md
## Policy Presetsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Example PolicyPreset Operations
PolicyPreset API Type
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
Example PolicyPreset Operations
PolicyPreset API Type
- Example PolicyPreset Operations
- PolicyPreset API Type
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Policy Presets
A PolicyPreset custom resource (CR) is used to save and reuse
configuration of Veeam Kasten Policies. Follow this
page to learn more about using Veeam Kasten Policy Presets.
A PolicyPreset specifies schedule, retention, location and
infrastructure information, while Policy that uses a preset
is supposed to specify application specific information.
A detailed description of the schedule settings can be found
in the Policy Scheduling section.
For complete documentation of the PolicyPreset CR,
refer to PolicyPreset API Type.
### Example PolicyPreset Operationsï
- Create a PolicyPreset
- Update a PolicyPreset
- Delete a PolicyPreset
### Create a PolicyPresetï
The following example illustrates how to create a preset for policies
which execute hourly, retain 24 hourly and 7 daily snapshots and
export every daily snapshot with the same retention schedule
as for snapshots (i.e. retain 7 daily exported snapshots).
### Update a PolicyPresetï
To update a PolicyPreset, edit the spec portion of a PolicyPreset CR
using your preferred method of submitting resource changes with kubectl.
Once the change is submitted, Veeam Kasten will re-validate the PolicyPreset
and update .status.validation accordingly.
Since Veeam Kasten processes API object changes asynchronously, to avoid
confusion with a previous PolicyPreset status, it is recommended as
convention that the status portion of the PolicyPreset is omitted
when submitting changes.
Warning
### Delete a PolicyPresetï
You can delete a PolicyPreset using the following command.
All the policies that use the deleted preset will be
automatically marked as invalid.
### PolicyPreset API Typeï
The following is a complete specification of the PolicyPreset CR.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_profiles.md
## Profilesï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Example Profile Operations
Profile API Type
Profile Secret Types
Policies
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
Example Profile Operations
Profile API Type
Profile Secret Types
- Example Profile Operations
- Profile API Type
- Profile Secret Types
- Policies
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Profiles
Note
As of March 5, 2024, "Azure Active Directory" has been renamed as
"Microsoft Entra ID." Throughout this documentation, references to "Azure
Active Directory" will be updated to use both the new and old names. Both
names will be used for a while, after which the documentation will be updated
to use only the new name.
A Profile custom resource (CR) is used to perform operations on
Veeam Kasten Profiles. You can learn more about using Veeam Kasten Profiles
at Location Configuration.
### Example Profile Operationsï
- Create a Profile Secret
- Create an Object Store Location Profile
- Create an Infrastructure Profile
- Create a Veeam Repository Location Profile
- Update a Profile
- Delete a Profile
### Create a Profile Secretï
When creating a Profile, you first need to create a Kubernetes secret that
holds the credentials for the location associated with the profile. The
examples below use an S3 bucket and therefore requires a properly formatted
S3 secret.
For complete documentation of secret formats, refer to Profile Secret Types.
### Create an Object Store Location Profileï
With a secret already defined, you can now create an Object Store
Location Profile.
Object Store location profiles can be used for import as well as
export operations.
For complete documentation of the Profile CR, refer to Profile API Type.
### Create an Infrastructure Profileï
The example demonstrates how to create a AWS Infrastructure Profile, but
an analogous approach applies to creating an OpenStack Profile.
First, create a secret with the AWS credentials as described in
AWS S3 and S3 Compatible Bucket Secret.
### Create a Veeam Repository Location Profileï
A Veeam Repository Location Profile
is used to export or import vSphere CSI provisioned volume snapshot data
in a supported
vSphere cluster from a
Veeam Repository.
A Veeam Repository cannot be used to save restore points
so such a location profile is always used in conjunction with another
location profile that can be used to save restore point data.
This profile requires a secret whose creation is described in
Veeam Repository Secret.
Once the secret has been created the Veeam Repository
Location Profile is created as follows:
The repoName field specifies the name of the repository to use;
it should not be an immutable repository.
The serverPort and skipSSLVerify fields are optional.
For complete documentation of the Profile CR, refer to Profile API Type.
### Update a Profileï
To update a Profile edit the spec portion of a Profile CR using your
preferred method of submitting resource changes with kubectl.
Once the change is submitted, Veeam Kasten will re-validate the profile and
update .status.validation accordingly.
Since Veeam Kasten processes API object changes asynchronously, to avoid
confusion with a previous Profile status, it is recommended as convention
that the status portion of the Profile is omitted when submitting changes.
### Delete a Profileï
You can delete a Profile using the following command.
### Profile API Typeï
The following is a complete specification of the Profile CR.
### Profile Secret Typesï
The following are the different secret types and formats to be used with
profiles.
- AWS S3 and S3 Compatible Bucket Secret
- GCS Bucket Secret
- Azure Storage Bucket Secret
- OpenStack Account Secret
- Portworx Key Secret
- vSphere Key Secret
- Veeam Repository Secret
### AWS S3 and S3 Compatible Bucket Secretï
When a Profile is using an S3 or S3-compatible bucket location, the
credential secret must follow the format below. In order to use temporary
security credentials, you can generate an IAM role and provide it as a part
of the S3 secret as shown below. Veeam Kasten supports the generation of
temporary credentials to perform generic backups, export collections to
an object store, and for EBS/EFS snapshot operations.
Alternatively, the secret can be created using kubectl as follows.
### GCS Bucket Secretï
When a Profile is using a GCS Storage bucket location the credential secret
must follow the format below.
This example shows how to create a secret using a GCP service account JSON file
, assuming that the service account has the necessary permissions for accessing
your bucket and that the JSON file is located in your working directory.
This is an example that shows how to create a secret with a workload
identity federation credentials configurations file, assuming that the service
account the credentials will impersonate has the proper permissions for
accessing your bucket, and that the json file is in your working directory.
When using Google Workload Identity Federation with Kubernetes as the Identity
Provider, ensure that the credential configuration file is configured with the
format type (--credential-source-type) set to Text, and specify the OIDC
ID token path (--credential-source-file) as
/var/run/secrets/kasten.io/serviceaccount/GWIF/token.
### Azure Storage Bucket Secretï
When a Profile is using an Azure Storage bucket location the credential
secret must follow the format below.
### Microsoft Entra ID Secretï
When a Profile uses Microsoft Entra ID (formerly Azure Active Directory)
for authentication, the credential secret must follow the format below.
Please note that an Azure infrastructure profile using the default Managed
Identity does not need a secret.
### OpenStack Account Secretï
When an Infrastructure Profile is being configured for accessing storage
that supports the Open Stack Cinder interface, the credential secret must
follow the format below:
### Portworx Key Secretï
When an Infrastructure Profile is being configured for accessing storage
that supports the Portworx interface, the credential secret must follow
the format below.
### vSphere Key Secretï
When a vSphere Infrastructure Profile is being
configured the credential secret must follow the format below.
### Veeam Repository Secretï
A Veeam Repository Location Profile
requires a credential secret in the format below.
Alternatively, the secret can be created using kubectl as follows:
© Copyright 2017-2024, Kasten, Inc.
### latest_api_policies.md
## Policiesï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Example Policy Operations
Policy Scheduling
Advanced Backup Policy Examples
Policy API Type
Policy Presets
Actions
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
Example Policy Operations
Policy Scheduling
Advanced Backup Policy Examples
Policy API Type
- Example Policy Operations
- Policy Scheduling
- Advanced Backup Policy Examples
- Policy API Type
- Policy Presets
- Actions
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Policies
A Policy custom resource (CR) is used to perform operations on Veeam
Kasten Policies. Policies allow you to manage application
protection and migration at scale. You can learn more about using Veeam
Kasten Policies in the Veeam Kasten Protecting Applications
section.
### Example Policy Operationsï
- Create a Backup Policy
- Create a Backup Policy using a Policy Preset
- Create an Import Policy
- Update a Policy
- Delete a Policy
### Create a Backup Policyï
The following example illustrates how to create a backup policy which executes
hourly and retains 24 hourly and 7 daily snapshots. The policy covers an
application running in the namespace sampleApp.
For complete documentation of the Policy CR, refer to Policy API Type.
### Create a Backup Policy using a Policy Presetï
The following example illustrates how to create a backup policy which
uses a predefined policy preset sample-policy-preset and covers
an application running in the namespace sampleApp.
For more information about PolicyPreset CR,
refer to Policy Presets section.
### Create an Import Policyï
The following example illustrates how to create a policy which executes
hourly and imports an application that was previously exported to the
application-imports Profile.
### Update a Policyï
To update a Policy, edit the spec portion of a Policy CR using your
preferred method of submitting resource changes with kubectl.
Once the change is submitted, Veeam Kasten will re-validate the Policy and
update .status.validation accordingly.
Since Veeam Kasten processes API object changes asynchronously, to avoid
confusion with a previous Policy status, it is recommended as convention
that the status portion of the Policy is omitted when submitting changes.
### Delete a Policyï
You can delete a Policy using the following command.
### Policy Schedulingï
Within the Policy API Type, Veeam Kasten provides control of:
- How often the primary snapshot or import action should be performed
- How often snapshots should be exported into backups
- Which and how many snapshots and backups to retain
- When the primary snapshot or import action should be performed
### Frequencyï
The frequency portion of the policy spec indicates how often the primary
policy action should be performed. On demand policies run only when the
run once button is clicked or a RunAction is created.
The optional frequency portion of exportParameters indicates how often
snapshots should be exported into backups. If not specified, every snapshot is
to be exported.
### Retentionï
The retention portion of the policy spec indicates which and how many
snapshots to retain.
The optional retention portion of the export action allows exported backups
to be retained independently from snapshots. If not specified, exported backups
are retained with the same schedule as snapshots.
### BackupWindowï
The optional backupWindow portion of the policy spec indicates when in
the day the backup policy can be scheduled to run and by when any snapshot
action must complete.
The start and end times of the backupWindow are specified by
hour and minute. backupWindow length is limited to 24 hours.
If the end time specified is earlier than the start time,
this means backupWindow end time is in the next day.
The policy is scheduled to run once at the backupWindow start time.
If the policy has an hourly frequency and the duration of the
backupWindow exceeds 1 hour, the policy is also scheduled to run
every 60 minutes thereafter within the backupWindow.
The snapshot action of the policy will be forcibly cancelled if it does
not complete within the backup window. If the snapshot action completes
within the backup window, no time restrictions are imposed on further
actions such as snapshot export.
### Staggeringï
The optional enableStaggering portion of the policy spec indicates
whether Veeam Kasten may choose when within the backupWindow to schedule
the backup policy to run.
This allows Veeam Kasten the flexibility to stagger runs of multiple
policies and reduce the peak load on the overall system.
The backupWindow is required when enableStaggering is set. The number
of the scheduled policy runs within the backupWindow and the cancelling
of in-progress snapshot actions at the end of the backupWindow are not
affected by staggering.
### SubFrequencyï
By default:
- Policies run once within the period of the frequency.
- Hourly policies run at the top of the hour.
- Daily policies run at midnight UTC.
- Weekly policies run at midnight Sunday UTC.
- Monthly policies run at midnight on the 1st of the month UTC.
- Yearly policies run at midnight on the 1st of January UTC.
- Snapshots and backups at those times are retained by the corresponding
retention counts.
The optional subFrequency portion of the policy spec provides fine-grained
control of when to run a policy, how many times to run a policy within a
frequency, and which snapshots and backups are retained.
The frequency, subFrequency, backupWindow and retention
interact as follows:
- When backupWindow is set, the time of day setting from
subFrequency is not allowed
- backupWindow and subFrequency entries within the frequency indicate
when the policy is to run
e.g. the minutes and hours subFrequency entries indicate the minutes and
hours at which a policy with a daily frequency runs
e.g. backupWindow indicates the period of the day during which a policy
with an hourly frequency runs
e.g. backupWindow indicates the period of the day and subFrequency
indicates the certain days of the week during which a policy with
a weekly frequency runs
- e.g. the minutes and hours subFrequency entries indicate the minutes and
hours at which a policy with a daily frequency runs
- e.g. backupWindow indicates the period of the day during which a policy
with an hourly frequency runs
- e.g. backupWindow indicates the period of the day and subFrequency
indicates the certain days of the week during which a policy with
a weekly frequency runs
- subFrequency entries immediately within the frequency may have multiple
values to run multiple times within the frequency
e.g. multiple minutes may be specified for an hourly frequency
(without backupWindow being set)
e.g. multiple hours may be specified for a daily frequency
(without backupWindow being set)
e.g. multiple days may be specified for a monthly frequency
(while backupWindow can indicate the common period of the day)
- e.g. multiple minutes may be specified for an hourly frequency
(without backupWindow being set)
- e.g. multiple hours may be specified for a daily frequency
(without backupWindow being set)
- e.g. multiple days may be specified for a monthly frequency
(while backupWindow can indicate the common period of the day)
- subFrequency entries indicate which snapshots
and backups graduate to higher retention tiers
e.g. for a policy with an hourly frequency, the hours subFrequency entry
indicates the hour of day that will graduate and be retained as a daily
- e.g. for a policy with an hourly frequency, the hours subFrequency entry
indicates the hour of day that will graduate and be retained as a daily
- For subFrequency entries with multiple values, the first value
indicates the time of the snapshot or backup to be retained by higher
tiers
e.g. an hourly frequency with subFrequency minutes entry of [45, 15] will
run twice an hour at 15 and 45 minutes after the hour, will retain both
according to the hourly retention
count, and will graduate the hourly taken at 45 minutes after the
hour designated by the subFrequency hour entry
to the daily tier and higher
- e.g. an hourly frequency with subFrequency minutes entry of [45, 15] will
run twice an hour at 15 and 45 minutes after the hour, will retain both
according to the hourly retention
count, and will graduate the hourly taken at 45 minutes after the
hour designated by the subFrequency hour entry
to the daily tier and higher
- When backupWindow is used, the start value indicates the time of the snapshot
or backup to be retained by higher tiers
e.g. for a policy with an hourly frequency, the start of backupWindow
indicates the time of day that will graduate and be retained as a daily
- e.g. for a policy with an hourly frequency, the start of backupWindow
indicates the time of day that will graduate and be retained as a daily
backupWindow and subFrequency entries within the frequency indicate
when the policy is to run
subFrequency entries immediately within the frequency may have multiple
values to run multiple times within the frequency
subFrequency entries indicate which snapshots
and backups graduate to higher retention tiers
For subFrequency entries with multiple values, the first value
indicates the time of the snapshot or backup to be retained by higher
tiers
When backupWindow is used, the start value indicates the time of the snapshot
or backup to be retained by higher tiers
All time values in backupWindow and subFrequency entries
in the API are in UTC.
If a subFrequency entry is omitted, it defaults as above
(taking backupWindow into account, if set).
### Advanced Backup Policy Examplesï
- Scheduling frequency and retention
- Export snapshots to a Veeam Repository
### Scheduling frequency and retentionï
The following example illustrates how to use frequency, subFrequency,
backupWindow and retention to create a backup policy that
- creates snapshots every day between 22:30 and 07:00
- exports the snapshot created on the fifteenth of the month
including exporting snapshot data to create a durable and portable backup
- including exporting snapshot data to create a durable and portable backup
- retains 14 daily snapshots
- retains 4 weekly snapshots from 22:30 each Friday
- retains 6 monthly snapshots from 22:30 on the fifteenth of each month
- retains 12 exported monthly backups from 22:30 on the fifteenth of each month
- retains 5 exported yearly backups from 22:30 on the fifteenth of January each
year
exports the snapshot created on the fifteenth of the month
This policy covers an application running in the namespace sampleApp.
### Export snapshots to a Veeam Repositoryï
Snapshot data of vSphere CSI provisioned volumes
in supported vSphere clusters
can be exported to a
Veeam Repository
by adding a reference to a
Veeam Repository Location Profile
in the blockModeProfile field of the exportParameters.
Only snapshot data is saved in the Veeam Repository.
The remaining data associated with the restore point
is saved in the location profile identified by the profile
field of the exportParameters.
A block level copy of the snapshot is backed up to the specified
Veeam repository.
Configuring Change Tracking on the
vSphere cluster nodes
is not mandatory, but if configured it does
enable the use of more efficient incremental backups
of just the changes between snapshots when possible,
instead of full backups every time.
All of the persistent volumes of an application are
associated with a single restore point, per
invocation of the policy.
When an exported restore point is deleted, Veeam Kasten
will also delete the corresponding restore point for the
exported snapshots.
Veeam Kasten always converts each backup into a synthetic
full in order to support the policy retention functionality
that permits the deletion of restore points in any order.
The following YAML illustrates how to create a policy that exports
to a Veeam Repository:
The policy above maintains just 3 local restore points
(and hence VMware snapshots)
but uses a more sophisticated GFS retention policy for the exported
restore points.
### Policy API Typeï
The following is a complete specification of the Policy CR.
© Copyright 2017-2024, Kasten, Inc.
### latest_api_actions.md
## Actionsï
- Veeam Kasten Disaster Recovery
- API and Command Line
API Concepts
AuditConfigs
Profiles
Policies
Policy Presets
Actions
BackupAction
RestoreAction
BatchRestoreAction
ExportAction
ImportAction
BackupClusterAction
RestoreClusterAction
RunAction
RetireAction
CancelAction
ReportAction
UpgradeAction
Transforms
Transform Sets
Blueprint Bindings
Applications
Restore Points
Reports
Repositories
KastenDR
StorageSecurityContext
- API Concepts
- AuditConfigs
- Profiles
- Policies
- Policy Presets
- Actions
BackupAction
RestoreAction
BatchRestoreAction
ExportAction
ImportAction
BackupClusterAction
RestoreClusterAction
RunAction
RetireAction
CancelAction
ReportAction
UpgradeAction
- BackupAction
- RestoreAction
- BatchRestoreAction
- ExportAction
- ImportAction
- BackupClusterAction
- RestoreClusterAction
- RunAction
- RetireAction
- CancelAction
- ReportAction
- UpgradeAction
- Transforms
- Transform Sets
- Blueprint Bindings
- Applications
- Restore Points
- Reports
- Repositories
- KastenDR
- StorageSecurityContext
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
- Accessing Veeam Kasten
- API and Command Line
- Actions
An Action API resource is used to initiate Veeam Kasten data
management operations. The actions can either be associated with a
Policy or be stand-alone on-demand actions. Actions also allow for
tracking the execution status of the requested operations.
The Veeam Kasten Platform exposes a number of different action types.
You can find more information about each of the supported types.
### BackupActionï
Backup actions are used to initiate backup operations on applications.
A backup action can be submitted as part of a policy or as a standalone
action.
### Create BackupAction Exampleï
For an example of how to use a BackupAction in a policy see
Create Backup Policy.
The following example illustrates how to create an on-demand backup action
for an application called mysql which resides is in a namespace called
mysql.
### Check Status of BackupAction Exampleï
After creating a BackupAction, Veeam Kasten will validate the action and
will proceed with execution. The action can be used to verify the
execution status.
If the action has completed successfully, you can get the RestorePoint
that will be created.
### BackupAction Details Exampleï
In addition to checking the status of a BackupAction, you can also query
the details associated with the action. You would use the details
sub-resource for that purpose.
### BackupAction Delete Exampleï
Once a BackupAction is complete, successfully or otherwise, it is
possible to delete the action. For actions that have completed
successfully, the restore point created by the action will be preserved.
### BackupAction List Exampleï
The following example illustrates listing all BackupActions for
a sample namespace.
For listing BackupActions in all namespaces use the --all-namespaces option
### BackupAction API Typeï
The following is a complete specification of the BackupAction API.
### BackupAction Details API Typeï
The following is a complete specification of the actionDetails section
of the BackupAction API. These fields are only available in the
BackupAction API when the details sub-resource is used as shown in the
example above.
### RestoreActionï
Restore actions are used to restore applications to a known-good
state from a restore point.
### Create RestoreAction Exampleï
The following example illustrates how to initiate a restore
for an application called mysql which resides is in a namespace called
mysql.
### Check Status of RestoreAction Exampleï
After creating a RestoreAction, Veeam Kasten will validate the action
and will proceed with execution. The action can be used to verify the
execution status.
### RestoreAction Details Exampleï
In addition to checking the status of a RestoreAction, you can also query
the details associated with the action. You would use the details
sub-resource for that purpose.
### RestoreAction Delete Exampleï
Once a RestoreAction is complete, successfully or otherwise, it is
possible to delete the action. Deleting the action has no effect on the
underlying Restore Point that was used.
### RestoreAction List Exampleï
The following example illustrates listing all RestoreActions for
a sample namespace.
For listing RestoreActions in all namespaces use the --all-namespaces
option
### RestoreAction API Typeï
The following is a complete specification of the RestoreAction API.
### RestoreAction Details API Typeï
The specification for actionDetails for RestoreAction API is the
same as the actionDetails section of the BackupAction API.
### BatchRestoreActionï
Batch restore actions are used to restore multiple applications
to a known-good state from their restore points.
### Create BatchRestoreAction Exampleï
The following example illustrates how to initiate a batch restore
for multiple applications from their latest restore points.
Note
### Check Status of BatchRestoreAction Exampleï
After creating a BatchRestoreAction, Veeam Kasten will validate
the action and proceed with execution. The action can be used to
verify the execution status.
### Check Status of actions subordinate to BatchRestoreAction Exampleï
Once started, a BatchRestoreAction will attempt to create
a subordinate restore action for each specified subject.
These can be retrieved by filtering on the label
k10.kasten.io/batchRestoreActionName.
### BatchRestoreAction Details Exampleï
In addition to checking the status of a BatchRestoreAction,
it may be useful to query the details associated with the action.
For this purpose, use the details sub-resource, which
includes quantitative statistics on subordinate actions,
a list of successfully restored applications,
and a list of applications that failed to be restored.
### BatchRestoreAction List Exampleï
The following example illustrates listing all BatchRestoreActions.
### BatchRestoreAction Delete Exampleï
Once a BatchRestoreAction is complete, successfully or otherwise, it is
possible to delete the action. Deleting the action has no effect on the
underlying operations performed during the execution.
### BatchRestoreAction API Typeï
The following is a complete specification of the BatchRestoreAction API.
### BatchRestoreAction Details API Typeï
The following is a complete specification of the status.actionDetails
section of the BatchRestoreAction API. These fields are only available
in the BatchRestoreAction API when the details sub-resource is used,
as shown in the example above.
### ExportActionï
Export actions are used to initiate an export of an application
to a different cluster using an existing restore point.
The snapshot creation process completes without generating
output artifacts if all the resources are deselected. Attempting
to export the snapshot fails with the error message "No artifacts
provided." Therefore, for a successful export, including at least
one resource is crucial when creating a snapshot.
For scheduled operations, an export action will be included as
part of a policy following a BackupAction. It is still possible
to initiate an on-demand export.
### Create ExportAction Exampleï
The following example illustrates how to initiate an export
for an application called mysql which resides is in a namespace called
mysql.
On-demand export actions can only be initiated in by admin users who have
permissions to create an ExportAction in the namespace where
Veeam Kasten is installed.
Snapshot data from a volume provisioned by the vSphere CSI driver
in a supported vSphere cluster
can be exported to a
Veeam Repository
by adding a reference to a
Veeam Repository Location Profile
in the blockModeProfile field.
The remaining data associated with the restore point
is saved in the location profile identified by the profile field.
### Check Status of ExportAction Exampleï
After creating an ExportAction, Veeam Kasten will validate the
action and will proceed with execution. The action can be used to
verify the execution status.
### Get Export String of ExportAction Exampleï
In addition to checking the ExportAction status, you may need to retrieve
the receiveString that is generated to identify the export. This will be
used when initiating an import on the other cluster.
### ExportAction Details Exampleï
In addition to checking the status of an ExportAction, you can also query
the details associated with the action. You would use the details
sub-resource for that purpose.
### ExportAction Delete Exampleï
Once an ExportAction is complete, successfully or otherwise, it is
possible to delete the action. Deleting the action has no effect on the
application that was exported.
You will not be able to access the receiveString after deleting
the ExportAction so make sure to collect it before deleting.
### ExportAction API Typeï
The following is a complete specification of the ExportAction API.
### ExportAction Details API Typeï
The specification for actionDetails for ExportAction API is the
same as the actionDetails section of the BackupAction API.
### ImportActionï
Currently ImportAction can only be initiated as part of a policy.
See Create Import Policy for details.
You can still use ImportAction to check status, get details, and
delete completed actions the same way you would for any other action
type.
### ImportAction API Typeï
The following is a complete specification of the ImportAction API.
This can only be created by policy at this point.
### ImportAction Details API Typeï
The specification for actionDetails for ImportAction API is the
same as the actionDetails section of the BackupAction API.
### BackupClusterActionï
Backup cluster actions are used to initiate backup operations on
cluster-scoped resources.  A backup cluster action can be submitted
as part of a policy or as a standalone action.
Backup cluster actions are non-namespaced.
### BackupClusterAction List Exampleï
The following example illustrates listing all
BackupClusterActions.
### BackupClusterAction API Typeï
The following is a complete specification of the
BackupClusterAction API.
### RestoreClusterActionï
Restore cluster actions are used to restore cluster-scoped resources
from a ClusterRestorePoint.  A restore cluster action can be
submitted as part of a policy or as a standalone action.
Restore cluster actions are non-namespaced.
### RestoreClusterAction List Exampleï
The following example illustrates listing all
RestoreClusterActions.
### RestoreClusterAction API Typeï
The following is a complete specification of the
RestoreClusterAction API.
### RunActionï
RunActions are used for manual execution and monitoring of actions related to
policy runs.
Manual policy runs are not subject to Policy Retention
### Create RunAction Exampleï
The following example illustrates how to initiate a manual execution
of a policy called backup-policy``in namespace ``app-ns.
### Check Status of RunAction Exampleï
Any execution of a policy will create a RunAction.  After creating
a RunAction, Veeam Kasten will validate the action and will
proceed with execution of the subject policy actions. The action
can be used to verify the execution status.
### Check Status of actions subordinate to RunAction Exampleï
Once started, a RunAction will create subordinate actions to perform
the work outlined in the subject policy actions.  These can be retrieved
by filtering on the label k10.kasten.io/runActionName.
### RunAction Delete Exampleï
Once a RunAction is complete, successfully or otherwise, it is
possible to delete the action. Deleting the action has no effect on the
underlying operations performed by the policy execution
### RunAction List Exampleï
The following example illustrates listing all RunActions
### RunAction API Typeï
The following is a complete specification of the RunAction API.
### RetireActionï
Currently RetireAction can only be initiated by a policy,
Garbage Collector or
by the deletion of a RestorePointContent.
When a RestorePoint created by one or more policies is no longer retained by
at least one policy or when a RestorePointContent
is deleted using the API, a RetireAction is initiated.
See Create Backup Policy and
RestorePointContent for more details.
You can use the RetireAction to check status and
delete completed actions the same way you would for any other action
type.
Retire actions are non-namespaced.
### RetireAction List Exampleï
The following example illustrates listing all RetireActions
### Check Status of RetireAction Exampleï
The following example illustrates querying one of the RetireActions for its
current status.
### RetireAction Details Exampleï
The following example illustrates querying one of the RetireActions for
more details.
### RetireAction API Typeï
The following is a complete specification of the RetireAction API.
This can only be created by a policy's retire action or deletion of a restore point content
at this point.
### RetireAction Details API Typeï
The specification for actionDetails for the RetireAction API is the
same as the actionDetails section of the BackupAction API.
### CancelActionï
CancelActions are created to halt progress of another action and prevent any
remaining retries. Cancellation is best effort and not every phase of an Action
may be cancellable. When an action is cancelled, its state becomes Cancelled.
CancelActions are limited API Objects. Only the create method is
supported and CancelActions are not persisted. To see the effect
of a CancelAction, check the status of the target action.
### CancelAction API Typeï
The following is a complete specification of the CancelAction API.
### ReportActionï
A ReportAction resource is created to generate a Veeam Kasten Report
and provide insights into system performance and status. A successful
ReportAction produces a Veeam Kasten Report that
contains information gathered at the time of the ReportAction.
### ReportAction API Typeï
The following is a complete specification of the ReportAction API.
### UpgradeActionï
An UpgradeAction resource is created to upgrade the backup data and metadata
associated with a given Export Policy or
Repository.
### UpgradeAction API Typeï
The following is a complete specification for the UpgradeAction API.
© Copyright 2017-2024, Kasten, Inc.
