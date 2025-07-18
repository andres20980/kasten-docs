# Api Documentation

## Api Actions

An Action API resource is used to initiate Veeam Kasten data
  management operations. The actions can either be associated with a Policy or be stand-alone on-demand actions. Actions also allow for
  tracking the execution status of the requested operations.

The Veeam Kasten Platform exposes a number of different action types.
  You can find more information about each of the supported types.

## BackupAction â

Backup actions are used to initiate backup operations on applications. A
  backup action can be submitted as part of a policy or as a standalone
  action.

### Create BackupAction Example â

For an example of how to use a BackupAction in a policy see Create Backup Policy .

The following example illustrates how to create an on-demand backup
  action for an application called mysql which resides is in a namespace
  called mysql .

```
$ cat > sample-backup-action.yaml <<EOFapiVersion: actions.kio.kasten.io/v1alpha1kind: BackupActionmetadata:  generateName: backup-mysql-  namespace: mysql  labels:    # These labels are required for on-demand actions so that    # actions can be filtered.    # Label presence is validated.    k10.kasten.io/appName: "mysql"    k10.kasten.io/appNamespace: "mysql"spec:  subject:    # Reference to the K10App CR for the application    name: mysql    namespace: mysqlEOF$ kubectl create -f sample-backup-action.yamlactions.kio.kasten.io/backup-mysql-ax34rt created
```

### Check Status of BackupAction Example â

After creating a BackupAction , Veeam Kasten will validate the action
  and will proceed with execution. The action can be used to verify the
  execution status.

```
$ kubectl get backupactions.actions.kio.kasten.io backup-mysql-ax34rt -ojsonpath="{.status.state}{'\n'}"Running
```

If the action has completed successfully, you can get the RestorePoint that will be created.

```
$ kubectl get backupactions.actions.kio.kasten.io backup-mysql-ax34rt -ojsonpath="{.status.restorePoint.name}{'\n'}"backup-mysql-ax34rt-restore-point-02-10-2019-09-00
```

### BackupAction Details Example â

In addition to checking the status of a BackupAction , you can also
  query the details associated with the action. You would use the
  [details] sub-resource for that purpose.

```
# get the details for action 'backup-mysql-ax34rt' created in 'mysql' namespace# yq only used for readability$ kubectl get --raw /apis/actions.kio.kasten.io/v1alpha1/namespaces/mysql/backupactions/backup-mysql-ax34rt/details | yq -y .status.actionDetailsphases:- name: Application configuration  state: succeeded  attempt: 1  startTime: '2019-02-11T03:03:47Z'  endTime: '2019-02-11T03:03:48Z'  updatedTime: '2019-02-11T03:03:48Z'- name: Stateful component mysql  state: failed  attempt: 2  startTime: '2019-02-11T03:03:47Z'  endTime:  updatedTime: '2019-02-11T03:04:51Z'  errors:  - message: No profile foundartifacts:  ...
```

### BackupAction Delete Example â

Once a BackupAction is complete, successfully or otherwise, it is
  possible to delete the action. For actions that have completed
  successfully, the restore point created by the action will be preserved.

```
$ kubectl delete backupactions.actions.kio.kasten.io backup-mysql-ax34rtactions.kio.kasten.io/backup-mysql-ax34rt deleted
```

### BackupAction List Example â

The following example illustrates listing all BackupActions for a
  sample namespace.

```
# list backup actions in namespace 'sample-app'$ kubectl get backupactions.actions.kio.kasten.io --namespace sample-appNAME                              AGEsample-app-backup-mysql-ax34rt    1hsample-app-backup-mysql-bg54st    2h
```

For listing BackupActions in all namespaces use the
  [--all-namespaces] option

```
## list backup actions in all namespaces$ kubectl get backupactions.actions.kio.kasten.io --all-namespacesNAMESPACE         NAME                              AGEsample-app        sample-app-backup-mysql-ax34rt    1hsample-app        sample-app-backup-mysql-bg54st    2h
```

### BackupAction API Type â

The following is a complete specification of the BackupAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: BackupActionmetadata:  ## Kubernetes labels.  ## The following labels will be auto-populated upon creation.  ## These labels can be used for filtering when getting actions.  ## Any additional custom labels can be specified if desired.  labels:    ## Populated for policy initiated BackupAction only.    k10.kasten.io/policyName: "sample-originating-policy"    k10.kasten.io/policyNamespace: "namespace-of-policy"    ## Populated for on-demand and policy initiated actions    k10.kasten.io/appName: "sample-app"    k10.kasten.io/appNamespace: "sample-app"    ## Populated for on-demand RunActions and policy initiated actions    k10.kasten.io/runActionName: "run-lhr7n6j8dw"    k10.kasten.io/runActionNamespace: "namespace-of-policy"  ## BackupAction name. May be any valid Kubernetes object name. Required.  ## BackupAction name is not mutable once created.  name: backup-action-example  ## BackupAction names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation  generateName: backup-action-  ## BackupAction namespace. Required.  ## Must be namespace of the application being backed up. Should match subject.  namespace: mysql## BackupAction spec. Required.spec:  ## Expiration timestamp in ``RFC3339`` format. Optional.  ## Garbage collector will automatically retire expired backups.  expiresAt: "2002-10-02T15:00:00Z"  ## Target application to be backed up. Required.  subject:    ## Name of the K10App resource. Required.    name: sample-app    ## Namespace of the application. Required.    namespace: sample-app  ## Scheduled time of action when initiated by policy. Optional.  scheduledTime: "2019-02-11T05:10:45Z"  ## Filters describe which Kubernetes resources should be included or excluded  ## in the backup. If no filters are specified, all the API resources in a  ## namespace are captured by the BackupAction.  #  ## Resource types are identified by group, version, and resource type names,  ## or GVR, e.g. networking.k8s.io/v1/networkpolicies. Core Kubernetes types  ## do not have a group name and are identified by just a version and resource  ## type name, e.g. v1/configmaps.  #  ## Individual resources are identified by their resource type and resource  ## name, or GVRN. In a filter, an empty or omitted group, version, resource  ## type or resource name matches any value.  #  ## Filters reduce the resources in the backup by selectively including and  ## then excluding resources.  ## - If includeResources is not specified, all the API resources in a  ##   namespace are included in the set of resources to be backed up.  ## - If includeResources is specified, resources matching any GVRN entry in  ##   includeResources are included in the set of resources to be backed up.  ## - If excludeResources is specified, resources matching any GVRN entry in  ##   excludeResources are excluded from the set of resources to be backed up.  #  ## For RestorePoint usefulness after the BackupAction, Veeam Kasten automatically  ## includes associated PVCs and PVs when a statefulset, deployment, or  ## deploymentconfig is included by includeResources unless the PVC is  ## excluded by excludeResources.  filters:    ## Include only resources that match any of the following NGVRs    includeResources:      ## Include individual resource    - name: <resource1 resource name>      group: <resource1 group>      version: <resource1 version>      resource: <resource1 type name>      ## Include resource type    - group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>    ## Exclude resources that match any of the following NGVRs    excludeResources:      ## Exclude specific instance of resource2 type    - name: <resource2 resource name>      group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>  ## Optional: Ignore exceptions and continue if possible.  ## Snapshots with exceptions will be flagged as potentially flawed.  ## Default: false  ignoreExceptions: false  ## Optional: Hooks are Kanister actions executed first or last in a BackupAction.  ## A Kanister ActionSet is created with the application namespace as its subject.  ## The Blueprint must be in the Veeam Kasten namespace. Hooks do not use Location Profile.  hooks:    ## The Kanister action referenced by preHook will be executed before    ## other phases of the BackupAction. Optional.    preHook:      blueprint: backup-hook-blueprint      actionName: before-backup    ## The Kanister action referenced by onSuccess will be executed once all    ## other phases in the BackupAction have completed successfully. Optional.    onSuccess:      blueprint: backup-hook-blueprint      actionName: on-success    ## The Kanister action referenced by onFailure will be executed only    ## when the BackupAction fails and exhausts all retries. Optional.    onFailure:      blueprint: backup-hook-blueprint      actionName: on-failure## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Action execution progress represented as an integer percentage value in range between 0 and 100. Optional.  progress: 88  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## RestorePoint created by a successful action.  ## Always present when the action succeeds.  restorePoint:    ## Name of the restore point.    name: backup-action-example-restorepoint    ## Namespace of the restore point. Will be the same as action name space    namespace: mysql  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

### BackupAction Details API Type â

The following is a complete specification of the
  [actionDetails] section of the BackupAction API. These
  fields are only available in the BackupAction API when the
  [details] sub-resource is used as shown in the example
  above.

```
apiVersion: actions.kio.kasten.io/v1alpha1kind: BackupAction...spec:...status:  ...  ## Details section of the action resource.  ## Included when the details sub-resource is queried.  actionDetails:    ## List of phases associated with the action. Always present.    phases:        ## Name of the phase.      - name: "Application configuration"        ## State of the phase.        state: "succeeded"        ## Number of attempts for the phase.        attempt: 1        ## Start time of the phase.        startTime: "2019-02-11T03:03:47Z"        ## End time of the phase. 'null' if still running.        endTime: "2019-02-11T03:03:48Z"        ## Last updated time of the phase.        updatedTime: "2019-02-11T03:03:48Z"        ## List of errors associated with the phase attempts.        ## Only included attempt > 1 (phase has failed at lease once).        errors:          - message: "Sample error message"
```

## RestoreAction â

Restore actions are used to restore applications to a known-good state
  from a restore point.

### Create RestoreAction Example â

The following example illustrates how to initiate a restore for an
  application called mysql which resides is in a namespace called mysql .

```
$ cat > sample-restore-action.yaml <<EOFapiVersion: actions.kio.kasten.io/v1alpha1kind: RestoreActionmetadata:  generateName: restore-mysql-  namespace: mysqlspec:  subject:    kind: RestorePoint    name: mysql-restore-point-02-11-2019-09-00PST    namespace: mysql  targetNamespace: mysqlEOF$ kubectl create -f sample-restore-action.yamlactions.kio.kasten.io/restore-mysql-afr823 created
```

### Check Status of RestoreAction Example â

After creating a RestoreAction , Veeam Kasten will validate the action
  and will proceed with execution. The action can be used to verify the
  execution status.

```
## get the state of action 'restore-mysql-afr823' created in the 'mysql' namespace$ kubectl get -n mysql restoreaction restore-mysql-afr823 -ojsonpath="{.status.state}{'\n'}"Running
```

### RestoreAction Details Example â

In addition to checking the status of a RestoreAction , you can also
  query the details associated with the action. You would use the
  [details] sub-resource for that purpose.

```
## get the details for action 'restore-mysql-afr823' created in the 'mysql' namespace## yq only used for readability$ kubectl get --raw /apis/actions.kio.kasten.io/v1alpha1/namespaces/mysql/restoreactions/restore-mysql-afr823/details | yq -y .status.actionDetails## output is analogous to that for BackupAction with the addition of the volume operation details in the 'actionDetails.phases' sectionphases:  - attempt: 1    endTime: '2024-05-28T22:01:35Z'    name: Restoring Application Components    startTime: '2024-05-28T21:59:42Z'    state: succeeded    updatedTime: '2024-05-28T22:01:35Z'    volumeOperations:      - namespace: mysql        pvcName: pvc0        operation: Download        dataFormat: Block        driver: openshift-storage.rbd.csi.ceph.com        storageClass: ocs-storagecluster-ceph-rbd        storageType: CSI
```

### RestoreAction Delete Example â

Once a RestoreAction is complete, successfully or otherwise, it is
  possible to delete the action. Deleting the action has no effect on the
  underlying Restore Point that was used.

```
$ kubectl delete restoreactions.actions.kio.kasten.io restore-mysql-afr823actions.kio.kasten.io/restore-mysql-afr823 deleted
```

### RestoreAction List Example â

The following example illustrates listing all RestoreActions for a
  sample namespace.

```
## list restore actions in namespace 'sample-app'$ kubectl get restoreactions.actions.kio.kasten.io --namespace sample-appNAME                              AGErestore-mysql-afr823              1hrestore-mysql-fth675              2h
```

For listing RestoreActions in all namespaces use the
  [--all-namespaces] option

```
## list restore actions in all namespaces$ kubectl get restoreactions.actions.kio.kasten.io --all-namespacesNAMESPACE         NAME                              AGEsample-app        restore-mysql-afr823              1hsample-app        restore-mysql-fth675              2h
```

### RestoreAction API Type â

The following is a complete specification of the RestoreAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: RestoreActionmetadata:  ## Kubernetes labels.  ## The following labels will be auto-populated upon creation.  ## These labels can be used for filtering when getting actions.  ## Any additional custom labels can be specified if desired.  labels:    ## Populated for policy initiated RestoreAction only.    k10.kasten.io/policyName: "sample-originating-policy"    k10.kasten.io/policyNamespace: "namespace-of-policy"    ## Populated for on-demand and policy initiated actions    k10.kasten.io/appName: "sample-app"    k10.kasten.io/appNamespace: "sample-app"  ## RestoreAction name. May be any valid Kubernetes object name. Required.  ## RestoreAction name is not mutable once created.  name: restore-action-example  ## RestoreAction names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation  generateName: restore-action-  ## RestoreAction namespace. Required.  ## The target namespace where the application is being restored.  namespace: mysql## RestoreAction spec. Required.spec:  ## Target RestorePoint to be used. Required.  ## The caller needs to have read permission for the RestorePoint API  ## in the namespace below.  subject:    ## Standard Kubernetes kind declaration. Required.    ## Must be 'RestorePoint'    kind: RestorePoint    ## Name of the restore point to use. Required.    name: sample-restore-point    ## Namespace of the restore point. Required.    namespace: sample-app  ## Optional: set to true to overwrite existing resources to their  ## state in the restore point.  ## Default: false  overwriteExisting: false  ## Optional: set to true to only restore the application data to its original location  ## by overwriting existing PVC and re-scaling workloads.  ## Must be false if filters are specified.  ## Default: false  dataOnly: false  ## Optional: set to true to only restore the application data as a cloned volume  ## without overwriting existing PVC and re-scaling workloads.  ## Can be true if filters are specified.  ## Default: false  volumeClones: false  ## Optional: Request for Instant Recovery process. The restored application  ## will run from network volumes. Available only for block mode exports  ## in VBR 11+ when using a supported vSphere CSI driver.  ## The operation will fail if these requirements are not met.  instantRecovery: false  ## Optional for normal RestoreActions but required if 'instantRecovery'  ## is set to 'true'. Defines the name or Id of a datastore where the FCD  ## volumes will be migrated after a successful Instant Recovery process.  targetVsphereStorage:  ## Optional: Filters describe which Kubernetes resources should be restored  ## from the RestorePoint.  If no filters are specified, all the artifacts  ## in the RestorePoint are restored.  #  ## Filters reduce the resources restored by selectively including and then  ## excluding resources.  ## - If includeResources is not specified, all resources in the RestorePoint  ##   are included in the set of resources to be restored.  ## - If includeResources is specified, resources matching any GVRN entry in  ##   includeResources are included in the set of resources to be restored.  ## - If excludeResources is specified, resources matching any GVRN entry in  ##   excludeResources are excluded from the set of resources to be restored.  ## - In a filter, an empty or omitted group, version, resource type or  ##   resource name matches any value.  #  ## For precise control of RestoreAction, Veeam Kasten only restores resources that  ## are explicitly included by includeResources. For RestoreAction, when a  ## statefulset,deployment, or deploymentconfig is included by includeResources,  ## Veeam Kasten does not restore associated PVCs unless the PVC is included by  ## includeResources.  filters:    ## Include only resources that match any of the following NGVRs or labels    includeResources:      ## Include individual resource    - name: <resource1 resource name>      group: <resource1 group>      version: <resource1 version>      resource: <resource1 type name>      ## Include resource type    - group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>    - matchLabels:        <label key>: <label value>    ## Exclude resources that match any of the following NGVRs or labels    excludeResources:      ## Exclude specific instance of resource2 type    - name: <resource2 resource name>      group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>    - matchLabels:        <label key>: <label value>  ## Namespace where the application is to be restored.  ## This field will be REMOVED shortly as this will be controlled  ## by the namespace in which the RestoreAction resource is created  targetNamespace: mysql  ## The list of transforms. Optional.  ## Each transform can be defined inline or in a referenced transform set.  transforms:    ## Specifies which resource artifacts to apply this transform to. Required.    ## At least one filter should be set.  - subject:      ## Resource group. Optional.      group: apps      ## Resource version. Optional.      version: v1      ## Resource type. Optional.      resource: deployments      ## Resource name. Optional.      name: my-app    ## The name of the transform. Optional.    name: 'copyRelease'    ## An array of RFC-6902 JSON patch-like operations. Required.    ## It can be an empty array if the transform references a transform set.    json:      ## Operation name. Required.      ## Transforms support six command operations:      ##   ## 'test' - checks that an element exists (and equals the value / matches the regexp if specified)      ##   ## 'add' - inserts a new element to the resource definition      ##   ## 'remove' - deletes an existing element from the resource definition      ##   ## 'copy' - duplicates an element, overwriting the value in the new path if it already exists      ##   ## 'move' - relocates an element, overwriting the value in the new path if it already exists      ##   ## 'replace' - replaces an existing element with a new element    - op: copy      ## Source reference for operation. Optional.      ## Required and valid only for 'move' and 'copy' operations.      from: '/metadata/labels/release'      ## Target reference for operation. Required for every operation.      path: '/spec/template/metadata/labels/release'      ## Regex to match expression. Optional.      ## When used with 'copy', 'move' or 'replace' operation,      ## the transform will match the target text against the `regex`      ## and substitute regex capturing groups with `value`.      ## When used with 'test' operation,      ## the transform will match the target text against the `regex`.      regex: 'prod-v.*'      ## Value is any valid JSON. Optional.      ## Required for 'add' and 'replace' operations.      ## Required for 'copy' and 'move' operations only when used along with `regex`.      ## 'test' operation can use either `regex` or `value`.      value: 'prod'    ## Transform set to be used instead of in-place JSON specification. Optional.    transformSetRef:      name: copy-release-transformset      namespace: kasten-io  ## Only used with Kanister blueprints that support point-in-time restore  ## Value is the desired timestamp. Optional.  pointInTime: "2019-02-11T05:13:10Z"  ## Optional: Specifies whether the restore action should wait for all  ## workloads (Deployments, StatefulSets or DeploymentConfigs)  ## to be ready before completing.  skipWaitForWorkloadReady: false  ## Optional: Specify an alternate profile to restore from. Use if restore  ## points have been copied or moved from their original export location.  artifactOverrideProfile:    name: <profile name>  ## Optional: Hooks are Kanister actions executed first or last in a RestoreAction.  ## A Kanister ActionSet is created with the target namespace as its subject.  ## The Blueprint must be in the Veeam Kasten namespace. Hooks do not use Location Profile.  hooks:    ## The Kanister action referenced by preHook will be executed before    ## other phases of the RestoreAction. Optional.    preHook:      blueprint: restore-hook-blueprint      actionName: before-restore    ## The Kanister action referenced by onSuccess will be executed once all    ## other phases in the RestoreAction have completed successfully. Optional.    onSuccess:      blueprint: restore-hook-blueprint      actionName: on-success    ## The Kanister action referenced by onFailure will be executed only    ## when the RestoreAction fails and exhausts all retries. Optional.    onFailure:      blueprint: restore-hook-blueprint      actionName: on-failure## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

### RestoreAction Details API Type â

The specification for [actionDetails] for RestoreAction API is the same as the [actionDetails] section of the BackupAction API.

## BatchRestoreAction â

Batch restore actions are used to restore multiple applications to a
  known-good state from their restore points.

### Create BatchRestoreAction Example â

The following example illustrates how to initiate a batch restore for
  multiple applications from their latest restore points.

Batch restore actions can be created only in the namespace where
    Veeam Kasten is installed.

```
$ cat > sample-batch-restore-action.yaml <<EOFapiVersion: actions.kio.kasten.io/v1alpha1kind: BatchRestoreActionmetadata:  generateName: batchrestore-  namespace: kasten-iospec:  subjects:    - namespace: mysql    - namespace: nginx    - namespace: sample-appEOF$ kubectl create -f sample-batch-restore-action.yamlbatchrestoreactions.actions.kio.kasten.io/batchrestore-z82gt created
```

### Check Status of BatchRestoreAction Example â

After creating a BatchRestoreAction , Veeam Kasten will validate the
  action and proceed with execution. The action can be used to verify the
  execution status.

```
$ kubectl get batchrestoreactions.actions.kio.kasten.io batchrestore-z82gt --namespace kasten-io -o jsonpath="{.status.state}{'\n'}"Running
```

### Check Status of actions subordinate to BatchRestoreAction Example â

Once started, a BatchRestoreAction will attempt to create a
  subordinate restore action for each specified subject. These can be
  retrieved by filtering on the label
  [k10.kasten.io/batchRestoreActionName].

```
$ kubectl get restoreactions.actions.kio.kasten.io -l 'k10.kasten.io/batchRestoreActionName=batchrestore-z82gt' -o jsonpath="{range .items[*]}{.metadata.name}:{.metadata.namespace} {.status.state}{'\n'}{end}"scheduled-lsj8x:mysql Runningscheduled-ir29k:nginx Completescheduled-p9ako:sample-app Failed
```

### BatchRestoreAction Details Example â

In addition to checking the status of a BatchRestoreAction , it may be
  useful to query the details associated with the action. For this
  purpose, use the [details] sub-resource, which includes
  quantitative statistics on subordinate actions, a list of successfully
  restored applications, and a list of applications that failed to be
  restored.

```
## get the details for action 'batchrestore-z82gt'## yq only used for readability$ kubectl get --raw /apis/actions.kio.kasten.io/v1alpha1/namespaces/kasten-io/batchrestoreactions/batchrestore-z82gt/details | yq -y .status.actionDetailsactions:  total: 3  cancelled: 0  running: 1  failed: 1  skipped: 0  completed: 1  pending: 0subjectsCount: 3restoredApplications:  - nginxfailedApplications:  - sample-app
```

### BatchRestoreAction List Example â

The following example illustrates listing all BatchRestoreActions .

```
$ kubectl get batchrestoreactions.actions.kio.kasten.io --all-namespacesNAMESPACE   NAME                 CREATED AT              STATE      PCT    SUBJECTSkasten-io   batchrestore-z82gt   2023-10-03T18:33:42Z    Complete   100    3kasten-io   batchrestore-jtjwg   2023-10-03T16:21:37Z    Complete   100    7
```

### BatchRestoreAction Delete Example â

Once a BatchRestoreAction is complete, successfully or otherwise, it
  is possible to delete the action. Deleting the action has no effect on
  the underlying operations performed during the execution.

```
$ kubectl delete batchrestoreactions.actions.kio.kasten.io batchrestore-z82gt --namespace kasten-iobatchrestoreactions.kio.kasten.io/batchrestore-z82gt deleted
```

### BatchRestoreAction API Type â

The following is a complete specification of the BatchRestoreAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: BatchRestoreActionmetadata:  ## BatchRestoreAction name. May be any valid Kubernetes object name.  ## Required if generateName (below) is not specified.  ## BatchRestoreAction name is not mutable once created.  name: batchrestore-example  ## BatchRestoreAction names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation.  generateName: batchrestore-  ## BatchRestoreAction namespace. Required.  ## Must be the namespace where Veeam Kasten is installed.  namespace: kasten-io## BatchRestoreAction spec. Required.spec:  ## Prefix to be added to the namespace  ## where the application is to be restored. Optional.  ## If used and the target namespace does not yet exist,  ## the user creating the resource will need to have  ## create permission on namespaces.  targetNamespacePrefix: copy-  ## Suffix to be added to the namespace  ## where the application is to be restored. Optional.  ## If used and the target namespace does not yet exist,  ## the user creating the resource will need to have  ## create permission on namespaces.  targetNamespaceSuffix: -1  ## List of applications to be restored. Required.  subjects:      ## Namespace of the application. Required.      ## The user creating the resource needs to have create permission      ## for the RestoreAction API in the target namespace.      ## To restore cluster-scoped resources, use a special value `kasten-io-cluster`.    - namespace: mysql      ## Name of the restore point to use. Optional.      ## If used, the user creating the resource will need to have      ## get permission on this restore point.      ## If not provided, Veeam Kasten will use the latest restore point available      ## for the specified namespace and the user will need to have list      ## permission on RestorePoint API in the specified namespace.      restorePointName: scheduled-m8zkn      ## Name of the restore point content to use. Optional.      ## Useful when restoring a deleted application for which      ## a restore point was once created and then deleted      ## along with the application namespace.      ## If used, the user creating the resource will need to have      ## get permission on this restore point content.      ## If the specified restore point content is in an `Unbound` state      ## (references a restore point that does not exist),      ## the user creating the resource will also need to have      ## create permission on RestorePoint API in the target namespace.      ## If not provided and the namespace being restored does not exist,      ## the user will need to have list permission on RestorePointContent API.      restorePointContentName: mysql-scheduled-m8zkn  ## Date range in which Veeam Kasten will search for the latest restore point  ## (or restore point content) for subjects that specify  ## neither restore point name nor restore point content name. Optional.  restorePointsDiscoveryRange:    ## Start of the date range. Optional.    - start: "2023-10-01T08:00:00Z"    ## End of the date range. Optional.    - end: "2023-10-02T11:00:00Z"  ## Set to true to overwrite existing resources to their  ## state in the restore point. Optional.  ## Default: false.  overwriteExisting: false  ## Optional: set to true to only restore the application data to its original location  ## by overwriting existing PVC and re-scaling workloads.  ## Must be false if filters are specified.  ## Default: false.  dataOnly: false  ## Optional: set to true to only restore the application data as a cloned volume  ## without overwriting existing PVC and re-scaling workloads.  ## Can be true if filters are specified.  ## Default: false.  volumeClones: false  ## Filters describe which Kubernetes resources should be restored  ## from the RestorePoint. If no filters are specified, all the artifacts  ## in the RestorePoint are restored. Optional.  ## Check RestoreAction API Type for more details.  #  ## Filters reduce the resources restored by selectively including and then  ## excluding resources.  ## - If includeResources is not specified, all resources in the RestorePoint  ##   are included in the set of resources to be restored.  ## - If includeResources is specified, resources matching any GVRN entry in  ##   includeResources are included in the set of resources to be restored.  ## - If excludeResources is specified, resources matching any GVRN entry in  ##   excludeResources are excluded from the set of resources to be restored.  ## - In a filter, an empty or omitted group, version, resource type or  ##   resource name matches any value.  #  ## For precise control of RestoreAction, Veeam Kasten only restores resources that  ## are explicitly included by includeResources. For RestoreAction, when a  ## statefulset, deployment, or deploymentconfig is included by includeResources,  ## Veeam Kasten does not restore associated PVCs unless the PVC is included by  ## includeResources.  filters:    ## Include only resources that match any of the following GVRNs or labels.    includeResources:      ## Include individual resource.    - name: <resource1 resource name>      group: <resource1 group>      version: <resource1 version>      resource: <resource1 type name>      ## Include resource type.    - group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>    - matchLabels:        <label key>: <label value>    ## Exclude resources that match any of the following GVRNs or labels.    excludeResources:      ## Exclude specific instance of resource2 type.    - name: <resource2 resource name>      group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>    - matchLabels:        <label key>: <label value>  ## The list of transforms. Optional.  ## Each transform can be defined inline or in a referenced transform set.  transforms:    ## Specifies which resource artifacts to apply this transform to. Required.    ## At least one filter should be set.  - subject:      ## Resource group. Optional.      group: apps      ## Resource version. Optional.      version: v1      ## Resource type. Optional.      resource: deployments      ## Resource name. Optional.      name: my-app    ## The name of the transform. Optional.    name: 'copyRelease'    ## An array of RFC-6902 JSON patch-like operations. Required.    ## It can be an empty array if the transform references a transform set.    json:      ## Operation name. Required.      ## Transforms support six command operations:      ##   ## 'test' - checks that an element exists (and equals the value / matches the regexp if specified)      ##   ## 'add' - inserts a new element to the resource definition      ##   ## 'remove' - deletes an existing element from the resource definition      ##   ## 'copy' - duplicates an element, overwriting the value in the new path if it already exists      ##   ## 'move' - relocates an element, overwriting the value in the new path if it already exists      ##   ## 'replace' - replaces an existing element with a new element    - op: copy      ## Source reference for operation. Optional.      ## Required and valid only for 'move' and 'copy' operations.      from: '/metadata/labels/release'      ## Target reference for operation. Required for every operation.      path: '/spec/template/metadata/labels/release'      ## Regex to match expression. Optional.      ## When used with 'copy', 'move' or 'replace' operation,      ## the transform will match the target text against the `regex`      ## and substitute regex capturing groups with `value`.      ## When used with 'test' operation,      ## the transform will match the target text against the `regex`.      regex: 'prod-v.*'      ## Value is any valid JSON. Optional.      ## Required for 'add' and 'replace' operations.      ## Required for 'copy' and 'move' operations only when used along with `regex`.      ## 'test' operation can use either `regex` or `value`.      value: 'prod'    ## Transform set to be used instead of in-place JSON specification. Optional.    transformSetRef:      name: copy-release-transformset      namespace: kasten-io  ## Specifies whether the subordinate restore actions should wait for all  ## workloads (Deployments, StatefulSets or DeploymentConfigs)  ## to be ready before completing. Optional.  ## Default: false.  skipWaitForWorkloadReady: false  ## Hooks are Kanister actions executed first or last in each subordinate RestoreAction.  ## A Kanister ActionSet is created with the target namespace as its subject.  ## The Blueprint must be in the Veeam Kasten namespace. Hooks do not use Location Profile. Optional.  hooks:    ## The Kanister action referenced by preHook will be executed before    ## other phases of the RestoreAction. Optional.    preHook:      blueprint: restore-hook-blueprint      actionName: before-restore    ## The Kanister action referenced by onSuccess will be executed once all    ## other phases in the RestoreAction have completed successfully. Optional.    onSuccess:      blueprint: restore-hook-blueprint      actionName: on-success    ## The Kanister action referenced by onFailure will be executed only    ## when the RestoreAction fails and exhausts all retries. Optional.    onFailure:      blueprint: restore-hook-blueprint      actionName: on-failure## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (no any application has been restored)  ## Complete - action has completed successfully  state: Complete  ## Initial start time of action. Always present.  startTime: "2023-02-10T15:12:35Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2023-02-10T15:13:04Z"  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: <error message>  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: <exception message>  ## Action execution progress represented as an integer  ## percentage value in range between 0 and 100. Optional.  progress: 100
```

### BatchRestoreAction Details API Type â

The following is a complete specification of the
  [status.actionDetails] section of the BatchRestoreAction API. These fields are only available in the BatchRestoreAction API
  when the [details] sub-resource is used, as shown in the
  example above.

```
apiVersion: actions.kio.kasten.io/v1alpha1kind: BatchRestoreAction...spec:  ...status:  ...  ## Details section of the action resource.  ## Included when the details sub-resource is queried.  actionDetails:    ## Amount of subordinate actions per their state.    actions:      total: 3      cancelled: 0      running: 0      failed: 1      skipped: 0      completed: 2      pending: 0    ## Amount of subjects specified for this action.    subjectsCount: 3    ## List of successfully restored applications. Always present.    restoredApplications:      - mysql      - nginx    ## List of applications that failed to be restored.    ## Only included when there are such applications.    failedApplications:      - sample-app
```

## ExportAction â

Export actions are used to initiate an export of an application to a
  different cluster using an existing restore point.

The snapshot creation process completes without generating output
    artifacts if all the resources are deselected. Attempting to export the
    snapshot fails with the error message "No artifacts provided."
    Therefore, for a successful export, including at least one resource is
    crucial when creating a snapshot.

For scheduled operations, an export action will be included as part of a
  policy following a BackupAction . It is still possible to initiate an
  on-demand export.

### Create ExportAction Example â

The following example illustrates how to initiate an export for an
  application called mysql which resides is in a namespace called mysql .

On-demand export actions can only be initiated in by admin users who
  have permissions to create an ExportAction in the namespace where
  Veeam Kasten is installed.

```
## create on-demand export that exports RP 'mysql-restore-point-02-11-2019-09-00PST'## from the 'mysql' namespace using 'sample-profile'.## Assumes that Veeam Kasten is installed in 'kasten-io' namespace.$ cat > sample-export-action.yaml <<EOFapiVersion: actions.kio.kasten.io/v1alpha1kind: ExportActionmetadata:  generateName: export-mysql-  namespace: kasten-iospec:  ## Expiration timestamp in ``RFC3339`` format. Optional.  ## Garbage collector will automatically retire expired exports if this field is set.  expiresAt: "2002-10-02T15:00:00Z"  subject:    kind: RestorePoint    name: mysql-restore-point-02-11-2019-09-00PST    namespace: mysql  profile:    name: sample-profile    namespace: kasten-ioEOF$ kubectl create -f sample-export-action.yamlactions.kio.kasten.io/export-mysql-brd911 created
```

Snapshot data from a volume provisioned by the vSphere CSI driver in a
  supported vSphere cluster can be exported to a Veeam Repository by
  adding a reference to a Veeam Repository Location Profile in the blockModeProfile field. The remaining data
  associated with the restore point is saved in the location profile
  identified by the profile field.

### Check Status of ExportAction Example â

After creating an ExportAction , Veeam Kasten will validate the action
  and will proceed with execution. The action can be used to verify the
  execution status.

```
$ kubectl get -n mysql exportactions.actions.kio.kasten.io export-mysql-brd911 -ojsonpath="{.status.state}{'\n'}"Running
```

### Get Export String of ExportAction Example â

In addition to checking the ExportAction status, you may need to
  retrieve the [receiveString] that is generated to identify
  the export. This will be used when initiating an import on the other
  cluster.

```
## get the receive string for action 'export-mysql-brd911' created in the 'mysql' namespace$ kubectl get -n mysql exportactions.actions.kio.kasten.io export-mysql-brd911 -ojsonpath="{.spec.receiveString}{'\n'}"bIzAPpoanmFUkXV/lh1KoM...Cg5Mov3xvqgpCbL73levOuISe553w
```

### ExportAction Details Example â

In addition to checking the status of an ExportAction , you can also
  query the details associated with the action. You would use the
  [details] sub-resource for that purpose.

```
## get the details for action 'export-mysql-brd911' created in the 'mysql' namespace## yq only used for readability$ kubectl get --raw /apis/actions.kio.kasten.io/v1alpha1/namespaces/mysql/exportactions/export-mysql-brd911/details | yq -y .status.actionDetails## output is analogous to that for BackupAction with the addition of volume operation details in the 'actionDetails.phases' sectionphases:- attempt: 1  endTime: '2024-05-28T21:29:51Z'  name: Exporting RestorePoint  startTime: '2024-05-28T21:28:35Z'  state: succeeded  updatedTime: '2024-05-28T21:29:51Z'  volumeOperations:    - namespace: mysql      pvcName: pvc0      operation: Upload      dataFormat: Block      exportDirective: FileSystemMayExportInBlockMode      driver: openshift-storage.rbd.csi.ceph.com      storageClass: ocs-storagecluster-ceph-rbd      storageType: CSI      snapshotId: k10-csi-snap-jdn2znqhlqvcck4c      volumeSnapshotClass: ocs-storagecluster-rbdplugin-snapclass
```

### ExportAction Delete Example â

Once an ExportAction is complete, successfully or otherwise, it is
  possible to delete the action. Deleting the action has no effect on the
  application that was exported.

You will not be able to access the [receiveString] after
    deleting the ExportAction so make sure to collect it before deleting.

```
$ kubectl delete exportactions.actions.kio.kasten.io restore-mysql-afr823actions.kio.kasten.io/restore-mysql-afr823 deleted
```

### ExportAction API Type â

The following is a complete specification of the ExportAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.## Must be ExportActionkind: ExportActionmetadata:  ## Kubernetes labels.  ## The following labels will be auto-populated upon creation.  ## These labels can be used for filtering when getting actions.  ## Any additional custom labels can be specified if desired.  labels:    ## Populated for policy initiated RestoreAction only.    k10.kasten.io/policyName: "sample-originating-policy"    k10.kasten.io/policyNamespace: "namespace-of-policy"    ## Populated for on-demand and policy initiated actions    k10.kasten.io/appName: "sample-app"    k10.kasten.io/appNamespace: "sample-app"    ## Populated for on-demand RunActions and policy initiated actions    k10.kasten.io/runActionName: "run-lhr7n6j8dw"    k10.kasten.io/runActionNamespace: "namespace-of-policy"  ## ExportAction name may be any valid Kubernetes object name. Required.  ## ExportAction name is not mutable once created.  name: export-action-example  ## ExportAction names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation  generateName: export-action-  ## Action namespace. Required.  ## Namespace must be where Veeam Kasten is installed.  namespace: kasten-io## ExportAction spec. Required.spec:  ## Target RestorePoint to be used for export. Required.  ## The caller needs to have read permission for the RestorePoint API  ## in the namespace below.  subject:    ## Standard Kubernetes kind declaration. Required.    ## Must be 'RestorePoint'    kind: RestorePoint    ## Name of the restore point to use. Required.    name: sample-restore-point    ## Namespace of the restore point. Required.    namespace: sample-app  ## Location Profile that is used for this export. Required.  profile:    ## Name of the location profile. Required.    name: sample-profile    ## Namespace of the location profile. Required.    ## Must be the namespace where Veeam Kasten is installed.    namespace: kasten-io  ## The blockModeProfile is a reference to a profile that supports block based backup.  ## Optional: If set then a block mode backup of snapshot data will be performed  ## instead of a filesystem backup.  ## This should only be used when the infrastructure also supports block based backup.  blockModeProfile:    ## Name of the location profile supporting block mode. Required.    name: my-block-mode-profile    ## Namespace of the location profile. Required.    ## Must be in the namespace where Veeam Kasten is installed.    namespace: kasten-io  ## String to be used to initiate corresponding import.  ## Will be automatically populated. Do not explicitly specify.  ## This field will be move to 'status' in an upcoming release  receiveString: "xbrd234sampleExportSting123=="  ## Backup portability setting.  ## Convert volume snapshots into an infrastructure-independent  ## format.  exportData:    ## Default setting for all storage classes    enabled: false    ## Optional: Storage class to use for any temporary PVCs created    ## during the snapshot conversion process. If not specified, the    ## storage class of the source volume is used.    exporterStorageClassName: gp2    ## Overrides for the default exportData setting specified above.    ## Use this if you want to modify the defaults for a PVC that    ## has a specific storage class.    overrides:      ## Override setting of a specific storage class.      - storageClassName: gp2        enabled: false      - storageClassName: gp2-eu-west-1a        enabled: true        exporterStorageClassName: io1  ## Optional: Hooks are Kanister actions executed first or last in an ExportAction.  ## A Kanister ActionSet is created with the exported namespace as its subject.  ## The Blueprint must be in the Veeam Kasten namespace. Hooks do not use Location Profile.  hooks:    ## The Kanister action referenced by preHook will be executed before    ## other phases of the ExportAction. Optional.    preHook:      blueprint: export-hook-blueprint      actionName: before-export    ## The Kanister action referenced by onSuccess will be executed once all    ## other phases in the ExportAction have completed successfully. Optional.    onSuccess:      blueprint: export-hook-blueprint      actionName: on-success    ## The Kanister action referenced by onFailure will be executed only    ## when the ExportAction fails and exhausts all retries. Optional.    onFailure:      blueprint: export-hook-blueprint      actionName: on-failure## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Action execution progress represented as an integer percentage value in range between 0 and 100. Optional.  progress: 88  ## Action execution progress details, containing information about amounts of data.  ## Progress details are available for export only.  ## Export process consists of three operations:  ## - reading from disk (readBytes value reflects how much data was read from disk)  ## - calculating changes between data on disk and previously exported data (processedBytes value reflects how much data was analyzed).  ##   Data known to be unchanged since the last export will not be read from disk but will still count as being processed.  ## - uploading newly added data (transferredBytes value reflects how much data was uploaded to the export location for the namespace being exported)  progressDetails:    ## Total size of the volumes containing data to be exported.    totalBytes: 10000    ## Number of bytes which were read.    readBytes: 9000    ## Number of bytes which were processed.    processedBytes: 8000    ## Number of bytes which were transferred.    transferredBytes: 5000    ## Number of bytes processed per second    processingRate: 8000    ## Number of volumes to be exported    totalVolumes: 3    ## Number of already exported volumes    completedVolumes: 1    ## Time stamp when progress details were updated    updatedTime: "2019-02-11T05:13:10Z"  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

### ExportAction Details API Type â

The specification for [actionDetails] for ExportAction API
  is the same as the [actionDetails] section of the BackupAction API.

## ImportAction â

Currently ImportAction can only be initiated as part of a policy. See Create Import Policy for details.

You can still use ImportAction to check status, get details, and
  delete completed actions the same way you would for any other action
  type.

### ImportAction API Type â

The following is a complete specification of the ImportAction API.

This can only be created by policy at this point.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.## Must be ImportActionkind: ImportActionmetadata:  ## Kubernetes labels.  ## The following labels will be auto-populated upon creation.  ## These labels can be used for filtering when getting actions.  ## Any additional custom labels can be specified if desired.  labels:    ## Populated for policy initiated RestoreAction only.    k10.kasten.io/policyName: "sample-originating-policy"    k10.kasten.io/policyNamespace: "namespace-of-policy"    ## Populated for on-demand and policy initiated actions    k10.kasten.io/appName: "sample-app"    k10.kasten.io/appNamespace: "sample-app"    ## Populated for on-demand RunActions and policy initiated actions    k10.kasten.io/runActionName: "run-lhr7n6j8dw"    k10.kasten.io/runActionNamespace: "namespace-of-policy"  ## Action name. May be any valid Kubernetes object name. Required.  ## Name is not mutable once created.  name: import-action-example  ## Action namespace. Required.  ## Namespace will the namespace where Veeam Kasten is installed.  namespace: kasten-io## ImportAction spec. Required.spec:  ## Location Profile that is used for this import. Required.  profile:    ## Name of the location profile.    name: sample-profile    ## Namespace of the location profile.    ## Will always be the the namespace where Veeam Kasten is installed.    namespace: kasten-io  ## The receiveString that was specified when initiating the policy.  receiveString: "xbrd234sampleExportSting123=="## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## Reference to the RestorePointContent created by the import  ## Present on successful import.  restorePointContent:    ## Name of the generated RestorePointContent    name: imported-app-restore-point-content    ## Namespace for the RestorePointContent    ## All restore point contents reside in the Veeam Kasten install namespace.    namespace: kasten-io  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

### ImportAction Details API Type â

The specification for [actionDetails] for ImportAction API
  is the same as the [actionDetails] section of the BackupAction API.

## BackupClusterAction â

Backup cluster actions are used to initiate backup operations on
  cluster-scoped resources. A backup cluster action can be submitted as
  part of a policy or as a standalone action.

Backup cluster actions are non-namespaced.

### BackupClusterAction List Example â

The following example illustrates listing all BackupClusterActions .

```
## list backup cluster actions$ kubectl get backupclusteractions.actions.kio.kasten.ioNAME                          CREATED ATscheduled-6b5s8               2020-12-29T23:57:20Zscheduled-szmhn               2020-12-28T23:57:16Zbackup-cluster-action-j2brg   2020-12-23T00:20:41Zscheduled-h7qzd               2020-12-23T00:10:44Z
```

### BackupClusterAction API Type â

The following is a complete specification of the BackupClusterAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: BackupClusterActionmetadata:  ## Kubernetes labels.  ## The following labels will be auto-populated upon creation.  ## These labels can be used for filtering when getting actions.  ## Any additional custom labels can be specified if desired.  labels:    ## Populated for policy initiated BackupClusterAction only.    k10.kasten.io/policyName: "sample-originating-policy"    k10.kasten.io/policyNamespace: "namespace-of-policy"  ## BackupClusterAction name. May be any valid Kubernetes object name. Required.  ## BackupClusterAction name is not mutable once created.  name: backup-cluster-action-example  ## BackupClusterAction names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation  generateName: backup-cluster-action-## BackupClusterAction spec. Required.spec:  ## Scheduled time of action when initiated by policy. Optional.  scheduledTime: "2019-02-11T05:10:45Z"  ## Filters describe which Kubernetes resources should be included or excluded  ## in the backup. If no filters are specified, default cluster-scoped  ## resources are captured by the BackupClusterAction.  #  ## Resource types are identified by group, version, and resource type names,  ## or GVR, e.g. rbac.authorization.k8s.io/v1/clusterroles.  #  ## Individual resources are identified by their resource type and resource  ## name, or GVRN. In a filter, an empty or omitted group, version, resource  ## type or resource name matches any value.  #  ## Filters reduce the resources in the backup by selectively including and  ## then excluding resources.  ## - If includeClusterResources is not specified, default cluster-scoped  ##   resources are included in the set of resources to be backed up.  ## - If includeClusterResources is specified, cluster-scoped resources  ##   matching any GVRN entry in includeClusterResources are included in  ##   the set of resources to be backed up.  ## - If excludeClusterResources is specified, cluster-scoped resources  ##   matching any GVRN entry in excludeClusterResources are excluded from  ##   the set of resources to be backed up.  filters:    ## Include only resources that match any of the following NGVRs    includeClusterResources:      ## Include individual resource    - name: <resource1 resource name>      group: <resource1 group>      version: <resource1 version>      resource: <resource1 type name>      ## Include resource type    - group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>    ## Exclude resources that match any of the following NGVRs    excludeClusterResources:      ## Exclude specific instance of resource2 type    - name: <resource2 resource name>      group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## RestorePoint created by a successful action.  ## Always present when the action succeeds.  restorePoint:    ## Name of the cluster restore point.    name: backup-cluster-action-example-restorepoint  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

## RestoreClusterAction â

Restore cluster actions are used to restore cluster-scoped resources
  from a ClusterRestorePoint . A restore cluster action can be submitted
  as part of a policy or as a standalone action.

Restore cluster actions are non-namespaced.

### RestoreClusterAction List Example â

The following example illustrates listing all RestoreClusterActions .

```
## list restore cluster actions$ kubectl get restoreclusteractions.actions.kio.kasten.ioNAME                          CREATED ATscheduled-6b5s8               2020-12-29T23:57:20Zscheduled-szmhn               2020-12-28T23:57:16Zrestore-cluster-action-j2brg  2020-12-23T00:20:41Zscheduled-h7qzd               2020-12-23T00:10:44Z
```

### RestoreClusterAction API Type â

The following is a complete specification of the RestoreClusterAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: RestoreClusterActionmetadata:  ## Kubernetes labels.  ## The following labels will be auto-populated upon creation.  ## These labels can be used for filtering when getting actions.  ## Any additional custom labels can be specified if desired.  labels:    ## Populated for policy initiated BackupClusterAction only.    k10.kasten.io/policyName: "sample-originating-policy"    k10.kasten.io/policyNamespace: "namespace-of-policy"  ## RestoreClusterAction name. May be any valid Kubernetes object name. Required.  ## RestoreClusterAction name is not mutable once created.  name: restore-cluster-action-example  ## RestoreClusterAction names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation  generateName: restore-cluster-action-## RestoreClusterAction spec. Required.spec:  ## Scheduled time of action when initiated by policy. Optional.  scheduledTime: "2019-02-11T05:10:45Z"  ## Target ClusterRestorePoint to be used. Required.  ## The caller needs to have read permission for the ClusterRestorePoint  ## API object below.  subject:    ## Standard Kubernetes kind declaration. Required.    ## Must be 'ClusterRestorePoint'    kind: ClusterRestorePoint    ## Name of the cluster restore point to use. Required.    name: sample-cluster-restore-point  ## Optional: Filters describe which Kubernetes resources should be restored  ## from the ClusterRestorePoint.  If no filters are specified, all the  ## artifacts in the ClusterRestorePoint are restored.  #  ## Filters reduce the resources restored by selectively including and then  ## excluding resources.  ## - If includeClusterResources is not specified, all resources in the  ##   ClusterRestorePoint are included in the set of resources to be restored.  ## - If includeClusterResources is specified, resources matching any GVRN entry  ##   are included in the set of resources to be restored.  ## - If excludeClusterResources is specified, resources matching any GVRN entry  ##   are excluded from the set of resources to be restored.  ## - In a filter, an empty or omitted group, version, resource type or  ##   resource name matches any value.  filters:    ## Include only resources that match any of the following NGVRs    includeClusterResources:      ## Include individual resource    - name: <resource1 resource name>      group: <resource1 group>      version: <resource1 version>      resource: <resource1 type name>      ## Include resource type    - group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>    ## Exclude resources that match any of the following NGVRs    excludeClusterResources:      ## Exclude specific instance of resource2 type    - name: <resource2 resource name>      group: <resource2 group>      version: <resource2 version>      resource: <resource2 type name>  ## The list of transforms. Optional.  ## Each transform can be defined inline or in a referenced transform set.  transforms:    ## Specifies which resource artifacts to apply this transform to. Required.    ## At least one filter should be set.  - subject:      ## Resource group. Optional.      group: apps      ## Resource version. Optional.      version: v1      ## Resource type. Optional.      resource: deployments      ## Resource name. Optional.      name: my-app    ## The name of the transform. Optional.    name: 'copyRelease'    ## An array of RFC-6902 JSON patch-like operations. Required.    ## It can be an empty array if the transform references a transform set.    json:      ## Operation name. Required.      ## Transforms support six command operations:      ##   ## 'test' - checks that an element exists (and equals the value / matches the regexp if specified)      ##   ## 'add' - inserts a new element to the resource definition      ##   ## 'remove' - deletes an existing element from the resource definition      ##   ## 'copy' - duplicates an element, overwriting the value in the new path if it already exists      ##   ## 'move' - relocates an element, overwriting the value in the new path if it already exists      ##   ## 'replace' - replaces an existing element with a new element    - op: copy      ## Source reference for operation. Optional.      ## Required and valid only for 'move' and 'copy' operations.      from: '/metadata/labels/release'      ## Target reference for operation. Required for every operation.      path: '/spec/template/metadata/labels/release'      ## Regex to match expression. Optional.      ## When used with 'copy', 'move' or 'replace' operation,      ## the transform will match the target text against the `regex`      ## and substitute regex capturing groups with `value`.      ## When used with 'test' operation,      ## the transform will match the target text against the `regex`.      regex: 'prod-v.*'      ## Value is any valid JSON. Optional.      ## Required for 'add' and 'replace' operations.      ## Required for 'copy' and 'move' operations only when used along with `regex`.      ## 'test' operation can use either `regex` or `value`.      value: 'prod'    ## Transform set to be used instead of in-place JSON specification. Optional.    transformSetRef:      name: copy-release-transformset      namespace: kasten-io## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

## RunAction â

RunActions are used for manual execution and monitoring of actions
  related to policy runs.

Manual policy runs are not subject to Policy Retention

### Create RunAction Example â

The following example illustrates how to initiate a manual execution of
  a policy called backup-policy in namespace app-ns .

```
$ cat > sample-run-action.yaml <<EOFapiVersion: actions.kio.kasten.io/v1alpha1kind: RunActionmetadata:  generateName: run-backup-  namespace: app-nsspec:  subject:    kind: Policy    name: backup-policy    namespace: app-nsEOF$ kubectl create -f sample-run-action.yaml -n app-nsactions.kio.kasten.io/run-backup-th7z23 created
```

### Check Status of RunAction Example â

Any execution of a policy will create a RunAction . After creating a RunAction , Veeam Kasten will validate the action and will proceed with
  execution of the subject policy actions. The action can be used to
  verify the execution status.

```
$ kubectl get runactions.actions.kio.kasten.io run-backup-th7z23 -n app-ns -ojsonpath="{.status.state}{'\n'}"Running
```

### Check Status of actions subordinate to RunAction Example â

Once started, a RunAction will create subordinate actions to perform
  the work outlined in the subject policy actions. These can be retrieved
  by filtering on the label [k10.kasten.io/runActionName].

```
$ kubectl get backupactions.actions.kio.kasten.io -l 'k10.kasten.io/runActionName=run-backup-th7z23' -ojsonpath="{range .items[*]}{.metadata.name}:{.metadata.namespace} {.status.state}{'\n'}{end}"scheduled-jrwp2:ns-f9e74035 Runningscheduled-prb5g:ns-697a6a0a Runningscheduled-r9sts:ns-5615d5f3 Completescheduled-w7q5p:ns-7a7d5da7 Completescheduled-2lcjk:ns-e96562c5 Runningscheduled-tchl4:ns-b6bf19f2 Complete
```

### RunAction Delete Example â

Once a RunAction is complete, successfully or otherwise, it is
  possible to delete the action. Deleting the action has no effect on the
  underlying operations performed by the policy execution

```
$ kubectl delete runactions.actions.kio.kasten.io run-backup-th7z23 -n app-nsactions.kio.kasten.io/run-backup-th7z23 deleted
```

### RunAction List Example â

The following example illustrates listing all RunActions

```
## list run actions$ kubectl get runactions.actions.kio.kasten.io -n app-nsNAME                      CREATED AT             STATE    PCTrun-backup-th7z23         2024-04-03T19:34:06Z   Complete 100run-backup-t99ha8         2024-04-02T19:34:06Z   Complete 100
```

### RunAction API Type â

The following is a complete specification of the RunAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: RunActionmetadata:  ## RunAction name. May be any valid Kubernetes object name. Required.  ## RunAction name is not mutable once created.  name: run-action-example  ## RunAction names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation  generateName: run-action-  ## RunAction namespace must be the same as the policy it references in  ## spec.subject.namespace  namespace: app-ns## RunAction spec. Required.spec:  ## Expiration timestamp in ``RFC3339`` format. Optional.  ## Garbage collector will automatically retire expired backups and exports created by this RunAction.  expiresAt: "2002-10-02T15:00:00Z"  ## Target Policy to be used. Required.  ## The caller needs to have read permission for the Policy API  ## in the namespace below.  subject:    ## Standard Kubernetes kind declaration. Required.    ## Must be 'Policy'    kind: Policy    ## Name of the policy to use. Required.    name: sample-policy    ## Namespace of the policy. Required. Must be namespace where    ## Veeam Kasten is installed    namespace: app-ns## Status of the action. Users should not set directly.status:  ## portions of the Policy used to construct subordinate actions (eg. BackupActions and ExportActions).  ## For complete structure of RunAction policy spec, refer to [Policy API Type](./policies.md#policy_api_type)  policySpec:    actions:    ## Policy parameters used to construct subordinate actions    - action: backup    - action: export    selector:      matchLabels:        k10.kasten.io/appNamespace: sampleApp  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

## RetireAction â

Currently RetireAction can only be initiated by a policy, Garbage Collector or
  by the deletion of a RestorePointContent .

When a RestorePoint created by one or more policies is no longer
  retained by at least one policy or when a RestorePointContent is
  deleted using the API, a RetireAction is initiated.

See Create Backup Policy and RestorePointContent for more details.

You can use the RetireAction to check status and delete completed
  actions the same way you would for any other action type.

Retire actions are non-namespaced.

### RetireAction List Example â

The following example illustrates listing all RetireActions

```
$ kubectl get retireactions.actions.kio.kasten.ioNAME                                         CREATED ATretire-mysql-manualbackup-n4xfs-rbfb9        2021-01-26T17:19:32Zretire-mysql-manualbackup-n4xfsvlw54-k8d59   2021-01-26T17:15:06Z
```

### Check Status of RetireAction Example â

The following example illustrates querying one of the RetireActions for its current status.

```
$ kubectl get retireactions.actions.kio.kasten.io retire-mysql-manualbackup-n4xfs-rbfb9 -ojsonpath="{.status.state}{'\n'}"Complete
```

### RetireAction Details Example â

The following example illustrates querying one of the RetireActions for more details.

```
## get the details for action 'retire-mysql-manualbackup-n4xfs-rbfb9'## yq only used for readability$ kubectl get --raw /apis/actions.kio.kasten.io/v1alpha1/retireactions/retire-mysql-manualbackup-n4xfs-rbfb9/details | yq -y .status.actionDetails## output is analogous to that for BackupAction
```

### RetireAction API Type â

The following is a complete specification of the RetireAction API.

This can only be created by a policy's retire action or deletion of a
    restore point content at this point.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.## Must be RetireActionkind: RetireActionmetadata:  ## Kubernetes labels.  ## The following labels will be auto-populated upon creation.  ## These labels can be used for filtering when getting actions.  ## Any additional custom labels can be specified if desired.  labels:    ## Populated for policy initiated RetireAction only.    k10.kasten.io/policyName: "sample-originating-policy"    k10.kasten.io/policyNamespace: "namespace-of-policy"  ## Action name. May be any valid Kubernetes object name. Required.  ## Name is not mutable once created.  name: retire-action-example## RetireAction spec. Required.spec:  ## Scheduled time of the action that created the RestorePointContent  scheduledTime: "2019-02-11T05:10:45Z"## Status of the action. Users should not set directly.status:  ## State of the action. Always present.  ## Valid values are:  ## Pending - action has been created  ## Running - action has been validated and is running  ## AttemptFailed - at least one action phase needs to retry  ## Failed - action has failed (at least one phase failed permanently)  ## Complete - action has completed successfully  ## Skipped - action has been skipped  ## Deleting - action is being deleted  state: Complete  ## Initial start time of action. Always present.  startTime: "2019-02-11T05:10:45Z"  ## End time of action. Can be 'null' if action still running. Always present.  endTime: "2019-02-11T05:13:10Z"  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message
```

### RetireAction Details API Type â

The specification for [actionDetails] for the RetireAction API is the same as the [actionDetails] section of the BackupAction API.

## CancelAction â

CancelActions are created to halt progress of another action and
  prevent any remaining retries. Cancellation is best effort and not every
  phase of an Action may be cancellable. When an action is cancelled, its
  state becomes Cancelled .

CancelActions are limited API Objects. Only the create method is
    supported and CancelActions are not persisted. To see the effect of a CancelAction , check the status of the target action.

### CancelAction API Type â

The following is a complete specification of the CancelAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.## Must be CancelActionkind: CancelActionmetadata:  ## Action name. May be any valid Kubernetes object name.  ## Name or generateName is required.  name: cancel-action-example  generateName: cancel-action-  ## Action namespace. Required to be same as namespace  ## of action to be cancelled, if that action is namespaced.  ## Required to be Veeam Kasten namespace if action to be cancelled  ## is not namespaced.  namespace: sample-app## CancelAction spec. Required.spec:  subject:    ## Kind of the Action to be cancelled. Required.    ## Valid values are:    ## BackupAction    ## RestoreAction    ## ImportAction    ## ExportAction    ## RunAction    ## RetireAction (not namespaced)    ## BackupClusterAction (not namespaced)    ## RestoreClusterAction (not namespaced)    kind: BackupAction    ## Name of the Action to be cancelled. Required.    name: sample-action    ## Namespace of the Action to be cancelled. Required.    namespace: sample-app
```

## ReportAction â

A ReportAction resource is created to generate a Veeam Kasten Report
  and provide insights into system performance and status. A successful
  ReportAction produces a Veeam Kasten Report that
  contains information gathered at the time of the ReportAction.

### ReportAction API Type â

The following is a complete specification of the ReportAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: ReportActionmetadata:  ## Action name. May be any valid Kubernetes object name.  ## Name or generateName is required.  name: report-action-example  generateName: report-action-  ## Action namespace. Currently required to be Veeam Kasten namespace.  namespace: kasten-iospec:  ## Subject specifies scope of Report to be generated.  ## Currently must specify Veeam Kasten namespace for system Report.  subject:    name: kasten-io    namespace: kasten-io  ## Scheduled time of action when initiated by policy. Optional.  scheduledTime: "2021-10-11T05:10:45Z"  ## Reports include metrics collected by the Veeam Kasten Prometheus service  ## and queried over an interval up to the time of the Report.  ## The query interval must be non-zero and is calculated to be  ## (24 * statsIntervalDays) + statsIntervalHours.  statsIntervalDays: 1  statsIntervalHours: 0
```

## UpgradeAction â

An UpgradeAction resource is created to upgrade the backup data and
  metadata associated with a given Export Policy or Repository .

### UpgradeAction API Type â

The following is a complete specification for the UpgradeAction API.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: actions.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.## Must be 'UpgradeAction'kind: UpgradeActionmetadata:  ## Action name. May be any valid Kubernetes object name.  ## Name or generateName is required.  name: upgrade-action-example  ## UpgradeAction names must be unique and as an alternative to  ## name above one can take advantage of Kubernetes name auto-generation.  generateName: upgrade-action-## UpgradeAction specification. Required.spec:  ## Subject specifies the Policy or StorageRepository to be upgraded. Required.  subject:    ## Standard kubernetes kind declaration. Required.    ## Must be 'StorageRepository' or 'Policy'.    kind: StorageRepository    ## Name of the upgrade's subject. Required.    name: storage-repository-example    ## Namespace of the upgrade's subject. Required.    namespace: kasten-io    ## Profile specifies the location profile with which the    ## subject (StorageRepository or Policy) is associated. Required.  profile:    ## Name of the profile. Required.    name: aws-location-profile-example    ## Namespace of the profile. Required.    ## Must be the same namespace Veeam Kasten is installed in.    namespace: kasten-iostatus:  ## Error associated with the action.  ## Only included if the action does not succeed.  error:    message: Sample error message  ## List of exceptions associated with the action.  ## Only included if exceptions are present.  exceptions:    - message: Sample exception message  ## Start time and end time of the upgrade action.  startTime: "2004-02-29T21:08:07Z"  endTime: "2004-02-29T21:13:07Z"  ## State of the upgrade action: "Running", "Complete" or "Failed"  state: Complete
```

---

## Api Auditconfigs

An AuditConfig custom resource (CR) is used to send Veeam Kasten audit
  event logs to a cloud object store by using a reference to a Location Profile .

## Creating an Audit Config â

When creating an AuditConfig , you first need to create a Location
  Profile that points to a cloud object store.

With a Location Profile already defined, you can now create an Audit
  Config by executing the following commands:

```
$ cat <<EOF >>sample-audit-config.yamlapiVersion: config.kio.kasten.io/v1alpha1kind: AuditConfigmetadata:  name: sample-audit-config  namespace: kasten-iospec:  profile:    name: audit-s3    namespace: kasten-ioEOF$ kubectl apply -f sample-audit-config.yamlauditconfig.config.kio.kasten.io/sample-audit-config created## Make sure it is initialized and validated properly$ kubectl get auditconfigs.config.kio.kasten.io --namespace kasten-io -wNAME                STATUS    AGEsample-config       Success   5s
```

The AuditConfig can assume four different statuses:

| Status | Meaning | Pending | Created and waiting for Location Profile |
| :---: | :---: | :---: | :---: |
| Pending | Created and waiting for Location Profile |
| UpdateRequested | Audit Config or Location Profile has changed |
| DeleteRequested | Stop sending logs to this Location Profile |
| Success | Sending logs to this Location Profile |

## Updating an Audit Config â

To update an AuditConfig , edit the spec portion using your preferred
  method for submitting resource changes with kubectl .

```
$ kubectl apply -f sample-audit-config-changed.yamlauditconfig.config.kio.kasten.io/sample-audit-config configured
```

Once the change is submitted, Veeam Kasten will re-validate the audit
  config and update .status.validation accordingly.

```
$ kubectl get auditconfigs.config.kio.kasten.io --namespace kasten-io -wNAME                    STATUS    AGEsample-audit-config     Success   7s
```

This action will trigger the extended audit mechanism to update and send
  logs to the updated Location Profile.

## Deleting an Audit Config â

You can delete an AuditConfig using the following command:

```
## Delete audit config "sample-audit-config" for Veeam Kasten installed in "kasten-io"$ kubectl delete auditconfigs.config.kio.kasten.io sample-audit-config --namespace kasten-ioauditconfig.config.kio.kasten.io "sample-audit-config" deleted
```

This action will trigger the extended audit mechanism to stop sending
  logs to this Location Profile.

---

## Api Blueprintbindings

A BlueprintBinding custom resource (CR) is used to automate the
  assignment of Kanister blueprints to applications. Once a BlueprintBinding is created, Veeam Kasten will use it during snapshot,
  export and restore routines to automatically run a desired blueprint for
  matching workloads including workloads that are yet to be created in a
  cluster. You can learn more about Kanister blueprints in this section.

A BlueprintBinding consists of two parts: a reference to a Kanister
  blueprint and a resource selector. For resources that match the
  selector, Veeam Kasten will automatically use the specified blueprint.

A BlueprintBinding has priority over blueprint annotations by
    default. If a resource matches a BlueprintBinding and has a
    blueprint annotation at the same time, Veeam Kasten will use the
    blueprint specified in the BlueprintBinding .

For complete documentation of the BlueprintBinding CR, refer to BlueprintBinding API Type .

## Resource Selector â

The resources portion of the blueprint binding spec indicates which kind of resources this blueprint
  binding will apply to.

For resources that match multiple blueprint bindings, Veeam Kasten
    will use the earliest created one.

For a resource to match the selector, it must meet all the requirements
  from matchAll and at least one requirement from matchAny (if any). A blueprint binding with no
  requirements is considered invalid.

Both matchAll and matchAny portions of resources represent a list of resource requirements to
  meet. A single resource requirement can set one of the following
  constraints:

- type : selects resources by group, version, resource and name (GVRN) values
- namespace : selects resources by namespace
- annotations : selects resources by annotations
- labels : selects resources by labels

## Example BlueprintBinding Operations â

- Create a Blueprint Binding
- Update a Blueprint Binding
- Delete a Blueprint Binding

### Create a Blueprint Binding â

The following example illustrates how to create a blueprint binding
  which will automatically apply a blueprint to all statefulsets in the group apps that has no
  custom blueprint annotations.

```
$ cat > sample-blueprint-binding.yaml <<EOFapiVersion: config.kio.kasten.io/v1alpha1kind: BlueprintBindingmetadata:  name: sample-blueprint-binding  namespace: kasten-iospec:  blueprintRef:    name: my-blueprint    namespace: kasten-io  resources:    matchAll:      - type:          operator: In          values:            - group: apps              resource: statefulsets      - annotations:          key: kanister.kasten.io/blueprint          operator: DoesNotExistEOF$ kubectl apply -f sample-blueprint-binding.yamlblueprintbinding.config.kio.kasten.io/sample-blueprint-binding created## make sure it initializes and validates properly$ kubectl get blueprintbindings.config.kio.kasten.io --namespace kasten-io -wNAME                       DISABLED   STATUS    AGEsample-blueprint-binding              Success   7s
```

### Update a Blueprint Binding â

To update a BlueprintBinding , edit the spec portion of a BlueprintBinding CR using your preferred method of submitting resource
  changes with kubectl . E.g. disabled: true can be added to the spec to disable the blueprint binding.

```
$ kubectl apply -f sample-blueprint-binding-changed.yamlblueprintbinding.config.kio.kasten.io/sample-blueprint-binding configured
```

Once the change is submitted, Veeam Kasten will re-validate the BlueprintBinding and update .status.validation accordingly.

```
$ kubectl get blueprintbindings.config.kio.kasten.io --namespace kasten-io -wNAME                       DISABLED   STATUS    AGEsample-blueprint-binding              Success   45ssample-blueprint-binding   true       Success   47s
```

### Delete a Blueprint Binding â

You can delete a BlueprintBinding using the following command.

```
## delete blueprint binding "sample-blueprint-binding" for Veeam Kasten installed in "kasten-io"$ kubectl delete blueprintbindings.config.kio.kasten.io sample-blueprint-binding --namespace kasten-ioblueprintbinding.config.kio.kasten.io "sample-blueprint-binding" deleted
```

## BlueprintBinding API Type â

The following is a complete specification of the BlueprintBinding CR.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: config.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: BlueprintBinding## Standard Kubernetes metadata. Required.metadata:  ## BlueprintBinding name. May be any valid Kubernetes object name. Required.  ## BlueprintBinding name is not mutable once created.  name: sample-blueprint-binding  ## BlueprintBinding names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation.  generateName: blueprint-binding-  ## BlueprintBinding namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io## BlueprintBinding parameters. Required.spec:  ## Disabled blueprint bindings are ignored by Veeam Kasten. Optional.  ## Default: false  disabled: false  ## Blueprint to be used by BlueprintBinding. Required.  blueprintRef:    name: my-blueprint    namespace: kasten-io  ## Resource selector for which the blueprint will be used. Required  resources:    ## Array of resource requirements. Optional.    ## A resource must meet all of them to match the selector.    ## A resource requirement is a requirement for either type, namespace, annotations, or labels.    ## BlueprintBinding must have at least one requirement in matchAll or matchAny.    matchAll:      ## Type selector requirement for group, version, resource and name (GVRN). Optional.      - type:          ## Operator represents a resource type's relationship to a set of values. Required.          ## Valid operators are In and NotIn.          operator: In          ## Array of GVRN values. Required.          values:            - group: apps              version: v1              resource: statefulsets              name: mysql      ## Namespace selector requirement. Optional.      - namespace:          ## Operator represents a resource namespace's relationship to a set of values. Required.          ## Valid operators are In, NotIn, Exists and DoesNotExist.          operator: In          ## Array of string values. Required if the operator is In or NotIn.          ## If the operator is Exists or DoesNotExist, the values array must be empty.          values:            - ns1            - ns2      ## Annotation selector requirement that contains a key, values and an operator that      ## relates the key and values. Optional.      - annotations:          ## Annotation name that the selector applies to. Required.          key: kanister.kasten.io/blueprint          ## Operator represents a key's relationship to a set of values. Required.          ## Valid operators are In, NotIn, Exists and DoesNotExist.          operator: NotIn          ## Array of string values. Required if the operator is In or NotIn.          ## If the operator is Exists or DoesNotExist, the values array must be empty.          values:            - "production-blueprint"      ## Annotation selector requirement that contains a key, values and an operator that      ## relates the key and values. Optional.      - labels:          ## Label key that the selector applies to. Required.          key: app          ## Operator represents a key's relationship to a set of values. Required.          ## Valid operators are In, NotIn, Exists and DoesNotExist.          operator: In          ## Array of string values. Required if the operator is In or NotIn.          ## If the operator is Exists or DoesNotExist, the values array must be empty.          values:            - "myapp"    ## Array of resource requirements. Optional.    ## A resource must meet at least one of them to match the selector.    ## A resource requirement is a requirement for either type, namespace, annotations, or labels.    ## BlueprintBinding must have at least one requirement in matchAll or matchAny.    matchAny:      - ## Array items have the same syntax as in matchAll## Status of the BlueprintBinding. Users should not set any data here.status:  ## Validation status of the BlueprintBinding  ## Valid values are:  ##   ## Success - successfully initialized and validated  ##   ## Failed - not properly initialized or validated  ## Only blueprint bindings which have status of Success  ## (and which are not disabled) will be used by the system  validation: Success  ## An array of any validation or initialization errors encountered.  error: null  ## Object generation last observed by the controller.  observedGeneration: 2
```

---

## Api Cli

Veeam Kasten exposes an API based on Kubernetes Custom Resource
Definitions
(CRDs) and Kubernetes API
Aggregation .
  The simplest way to use the API is through kubectl .

To understand the API better refer to the following:

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
- StorageSecurityContext

---

## Api Concepts

Veeam Kasten exposes an API based on Kubernetes Custom Resource
Definitions
(CRDs) .

This section helps you learn about the Veeam Kasten platform and the
  abstractions that that are available through the API.

Currently the following Veeam Kasten objects are supported:

- Profile - abstracts a location (e.g. object store, NFS/SMB file store) and a set of credentials for accessing it. The Profile location is used to store and transfer application meta-data and, in some cases, actual persistent data during Veeam Kasten data management operations.
- Policy - represents a collection of data management actions that are configured to occur on a periodic or event driven basis. Policies would typically encode a set of business rules and translate them to specific actions that Veeam Kasten will apply on the applications it has discovered.
- PolicyPreset - is a predefined set of settings that can easily be applied to a Policy . A PolicyPreset can represent organizational SLAs requiring a user to specify only the application details to be used in a Policy .
- Applications - abstracts an application that has been automatically discovered on the cluster where Veeam Kasten is running. The application object encapsulates information about all stateful and stateless resources that comprise the application.
- Action - represents a data management operation that Veeam Kasten perform. Actions can be initiated on demand or as part of a policy . A number of different types of actions are supported.
- RestorePoint - created as a result of a backup or import action, a RestorePoint represents a version-in-time of an application that has been captured by Veeam Kasten and that can be restored using a restore action .
- StorageRepository - a representation of where and how Veeam Kasten stores its exported backup data. These objects provide a mechanism of more precisely managing and monitoring low-level data layout.
- KastenDR - Veeam Kasten Disaster Recovery (KDR) enables the recovery of a Veeam Kasten instance in the event of various disasters, including accidental deletion of Veeam Kasten resources, failure of underlying cluster infrastructure, or malicious acts. Its representation includes resources that fetch the list of available KDR restore points and restore an instance from a KDR restore point.
- TransformSet - store a set of Transforms as a custom resource. It provides more granular RBAC control, and the possibility of repeated use for Transforms .
- BlueprintBinding - represents a selection of resources in a cluster and a blueprint that Veeam Kasten will use for such resources.
- StorageSecurityContext -represents pod security context settings to access target storage to execute backup and restore operations.

---

## Api Dr

The DR API group consists of two resources used to initiate a Veeam Kasten Disaster Recovery (KDR) restore operation:

- KastenDRReview
- KastenDRRestore

## KastenDRReview â

KastenDRReview is an API resource used to fetch a list of available
  Veeam Kasten Disaster Recovery (KDR) restore points for a provided
  source cluster, from a provided location profile.

This resource provides the ability to track the progress of the
  operation, report on any errors encountered, and provide details
  regarding each available KDR restore point. The output is used to
  determine the id of a specific KDR restore point to be
  used in defining a KastenDRRestore resource.

### Create a KastenDRReview Example â

The following example illustrates how to create a KastenDRReview resource. This resource connects to the specified Veeam Kasten location
  profile and fetches KDR restore point information for the specified
  source cluster UID.

Creating a KastenDRReview resource assumes the following
  prerequisites:

- The location profile containing KDR restore points has been configured
- The k10-dr-secret secret has been configured in the install namespace

To avoid accidental, concurrent requests, only a single instance of a KastenDRReview is allowed to exist.

```
$ cat > sample-kastendrreview.yaml <<EOFapiVersion: dr.kio.kasten.io/v1alpha1kind: KastenDRReviewmetadata:  name: example-kdrreview  namespace: kasten-iospec:  sourceClusterInfo:    profileName: <Name of Location Profile containing KDR Restore Points>    sourceClusterID: <Source Cluster UID>EOF$ kubectl create -f sample-kastendrreview.yamlkastendrreview.dr.kio.kasten.io/example-kdrreview created
```

### List KastenDRReviews Example â

The following example illustrates listing all KastenDRReviews resources.

The status field provides information about the available KDR restore
  points, operation progress and any errors.

```
## list kastendrreviews$ kubectl get kastendrreviews.dr.kio.kasten.io --namespace kasten-ioNAME                SOURCE CLUSTERID                                 RESTOREPOINTS   PHASE                                     ERROR   STATEexample-kdrreview   9ff3c728-2b8a-4337-8e92-ae9da755f2a8             4               Successfully fetched data from storage            success## get a specific kastendrreview$ kubectl get kastendrreviews.dr.kio.kasten.io example-kdrreview -oyaml  apiVersion: dr.kio.kasten.io/v1alpha1  kind: KastenDRReview  metadata:    creationTimestamp: "2024-10-18T08:03:30Z"    name: example-kdrreview    namespace: kasten-io    resourceVersion: "6"    uid: 78ab33b0-3026-4392-bf9f-ab042206fd10  spec:    sourceClusterInfo:      profileName: sample-prof      sourceClusterID: 9ff3c728-2b8a-4337-8e92-ae9da755f2a8  status:    restorePoints:      count: 4      restorePointList:      - version: v3.2_metadata        createdTime: "2024-10-18T09:03:30Z"        id: 1ff3c798-3b8a-4734-8b62-dc9da753f2a8        localSnapshotTaken: true        validSnapshotAvailable: false        exportedCatalogAvailable: false      - version: v3.2_data        createdTime: "2024-10-18T09:03:30Z"        id: 1ff3c798-3b8a-4734-8b62-dc9da753f2a8        localSnapshotTaken: true        validSnapshotAvailable: false        exportedCatalogAvailable: true      - version: v3        createdTime: "2024-10-18T09:03:30Z"        id: 1ff3c798-3b8a-4734-8b62-dc9da753f2a8        localSnapshotTaken: true        validSnapshotAvailable: true        exportedCatalogAvailable: false      - version: v3        createdTime: "2024-10-18T08:30:45Z"        id: 8af3c729-2b8a-8337-6b92-be9da790f2a7        localSnapshotTaken: true        validSnapshotAvailable: false        exportedCatalogAvailable: false    state: success    phase: Successfully fetched data from storage
```

### Delete KastenDRReview Example â

KastenDRReview API resources can be deleted. Functionally, this only
  serves to clean up the API representation; no restore point data will be
  deleted.

```
## delete kastendrreview 'example-kdrreview' in namespace 'kasten-io'$ kubectl delete kastendrreviews.dr.kio.kasten.io example-kdrreview --namespace kasten-iokastendrreviews.dr.kio.kasten.io "example-kdrreview" deleted
```

### KastenDRReview API Type â

The following is a complete specification of the KastenDRReview resource.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: dr.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: KastenDRReview## Standard Kubernetes metadata. Required.metadata:  ## Name of the KastenDRReview. Required.  name: example-drreview  ## Namespace of the KastenDRReview. Required.  namespace: kasten-io## Spec of the KastenDRReview.spec:  ## SourceClusterInfo provides the source cluster details for disaster recovery.  sourceClusterInfo:    ## Unique identifier of the source cluster.    sourceClusterID: <clusterID>    ## Name of the location profile associated with the KDR policy on the source cluster.    profileName: <profileName>    ## Point in time for the KDR review (optional).    ## Can be specified for immutable location profiles in    ## the event of attempted direct deletion from the repository    pointInTime: "2023-11-06T00:00:00Z"## Status of the KastenDRReview.status:  ## The current state of the disaster recovery operation.  state: [none | running | failed | success]  ## The list of restore points for the disaster recovery process.  restorePoints:    count: 2    restorePointList:      - ## First restore point information.        ## KDR version of the snapshot        ## v3.2_metadata refers to "Quick DR (No Catalog Snapshot)"        ## v3.2_data refers to "Quick DR (Exported Catalog Snapshot)"         ## v3 refers to "Quick DR (Local Catalog Snapshot)"        ## v2 refers to "Legacy DR (Full Catalog Exports)"        version: "v3"        creationTime: "2023-11-01T12:00:00Z"        ## Restore point ID to be referenced in a KastenDRRestore        ## to select a specific KDR restore point        id: 1ff3c798-3b8a-4734-8b62-dc9da753f2a8        ## For "Quick DR" configuration of Veeam Kasten Disaster Recovery,        ## indicates that a local storage snapshot of the catalog PVC was taken        localSnapshotTaken: true        ## For "Quick DR" configuration of Veeam Kasten Disaster Recovery,        ## indicates that the associated local snapshot is available and will        ## be restored as part of the KDR restore point        validSnapshotAvailable: true        ## For "Quick DR" configuration of Veeam Kasten Disaster Recovery,        ## indicates that the associated local snapshot of the catalog PVC is         ## exported and will be restored as part of the KDR restore point        exportedCatalogAvailable: true      - ## Second restore point information.        version: "v2"        creationTime: "2023-11-02T12:00:00Z"        id: 1ff3c798-3b8a-4734-8b62-dc9da753f4f5        localSnapshotTaken: false        validSnapshotAvailable: false        exportedCatalogAvailable: false  ## Error details, if any, encountered during the KDR review process.  error: ""  ## Additional cause of the error, if applicable.  cause: ""  ## Current running phase of the disaster recovery review.  phase: ""
```

## KastenDRRestore â

KastenDRRestore is an API resource used to manage and track Veeam
  Kasten Disaster Recovery (KDR) restore operations.

This resource allows users to:

- Initiate a KDR restore operation from the latest KDR restore point
- Initiate a KDR restore operation from a specific restore point provided by the KastenDRReview process.
- Specify which resources to skip during the restore process (e.g., secrets, profiles).
- Monitor the status of the restore operation, including error information, cause and the phase of the operation.

### Create a KastenDRRestore Example â

The following examples illustrate how to create a KastenDRRestore resource.

Creating a KastenDRRestore resource assumes the following
  prerequisites:

- The location profile containing KDR restore points has been configured
- The k10-dr-secret Secret has been configured in the install namespace

To avoid accidental, concurrent requests, only a single instance of a KastenDRRestore is allowed to exist.

#### Use Latest KDR Restore Point â

The following example fetches all KDR restore points for the referenced
  source cluster and restores the latest available as of the specified
  point in time. This method can be used without first creating a KastenDRReview .

The pointInTime parameter is optional and can only be used for review
    and restore operations from an immutable location profile.

```
$ cat > sample-kastendrrestore.yaml <<EOFapiVersion: dr.kio.kasten.io/v1alpha1kind: KastenDRRestoremetadata:  name: sample-kdrrestore  namespace: kasten-iospec:  sourceClusterInfo:    profileName: <Name of Location Profile containing KDR restore points>    sourceClusterID: <Source Cluster UID>    pointInTime: "2024-10-08T04:00:33Z"EOFkastendrrrestore.dr.kio.kasten.io/sample-kdrrestore created
```

#### Use Specific KDR Restore Point â

The following example restores using a specific KDR restore point
  ( id ), from an existing KastenDRReview resource
  ( kastenDRReviewRef ).

```
$ cat > sample-kastendrrestore.yaml <<EOFapiVersion: dr.kio.kasten.io/v1alpha1kind: KastenDRRestoremetadata:  name: sample-kdrrestore  namespace: kasten-iospec:  kastenDRReviewDetails:    kastenDRReviewRef:      name: <KastenDRReview Name>      namespace: kasten-io    id: <KDR Restore Point ID from KastenDRReview RestorePointList>EOFkastendrrrestore.dr.kio.kasten.io/sample-kdrrestore created
```

### List KastenDRRestore Example â

The following example illustrates listing all KastenDRRestore resources in a namespace. The phase column indicates the various step
  through which restore operation is progressing.

```
## list kastendrrestores$ kubectl get kastendrrestores.dr.kio.kasten.io --namespace kasten-ioNAME                SOURCECLUSTERID                                 PHASE                                   STATE   ERRORexample-kdrrestore  2ff3c728-2b9a-4337-5e34-ae9da766f2a5            Importing application restore points    running## get a specific kastendrrestore$ kubectl get kastendrrestores.dr.kio.kasten.io example-kdrrestore -oyaml  apiVersion: dr.kio.kasten.io/v1alpha1  kind: KastenDRRestore  metadata:    creationTimestamp: "2024-10-18T08:03:30Z"    name: example-kdrrestore    namespace: kasten-io    resourceVersion: "6"    uid: 78ab33b0-3026-4392-bf9f-ab042206fd10  spec:    profileName: sample-prof    sourceClusterID: 7708b583-13d8-4104-8af3-57d1ac70f23e    pointInTime: "2024-10-08T04:00:33Z"  status:    state: success    phase: Successfully restored resources
```

### Delete KastenDRRestore Example â

KastenDRRestore API resources can be deleted. Functionally, this only
  serves to clean up the API representation.

```
## delete kastendrrestore 'example-kdrrestore' in namespace 'kasten-io'$ kubectl delete kastendrrestores.dr.kio.kasten.io example-kdrrestore --namespace kasten-iokastendrrestores.dr.kio.kasten.io "example-kdrrestore" deleted
```

### KastenDRRestore API Type â

The following is a complete specification of the KastenDRRestore resource.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: dr.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: KastenDRRestore## Standard Kubernetes metadata. Required.metadata:  ## Name of the KastenDRRestore. Required.  name: example-drrestore  ## Namespace of the KastenDRRestore. Required.  namespace: kasten-io## Spec of the KastenDRRestore.spec:  ## KastenDRReviewDetails holds the reference to the associated KastenDRReview.  kastenDRReviewDetails:    ## The NamespacedName reference to the KastenDRReview resource.    kastenDRReviewRef:      ## The name of the KastenDRReview resource.      name: example-drreview      ## The namespace of the KastenDRReview resource.      namespace: kasten-io    ## Unique identifier of the KDR restore point selected for restore operation.    id: 78ab33b0-3026-4392-bf9f-ab042206fd10  ## SourceClusterInfo provides the source cluster details for disaster recovery.  sourceClusterInfo:    ## Unique identifier of the source cluster.    sourceClusterID: 7708b583-13d8-4104-8af3-57d1ac70f23e    ## Name of the location profile associated with the KDR policy on the source cluster.    profileName: sample-profile    ## Point in time for the KDR review (optional).    ## Can be specified for immutable location profiles in    ## the event of attempted direct deletion from the repository    pointInTime: "2023-11-06T00:00:00Z"  ## SkipResources specifies resources to skip during restore operation (optional).  skipResources: "secrets,profiles"## Status of the KastenDRRestore.status:  ## The current state of the disaster recovery restore operation.  state: [none | running | failed | success]  ## Error details, if any, encountered during the restore process.  error: ""  ## Additional cause of the error, if applicable.  cause: ""  ## Current running phase of the disaster recovery restore process.  phase: ""
```

---

## Api K10Apps

The Application resource is in developer preview and a number of
    breaking changes to the resource API schema may happen in subsequent
    releases.

An Application resource represents an application that Veeam Kasten
  has been automatically discovered on the Kubernetes cluster. The
  application encapsulates all stateless and stateful resources that
  comprise it.

## Life Cycle and Namespaces â

Application resources are read-only and are automatically instantiated
  by Veeam Kasten when it discovers applications that are running on the
  Kubernetes cluster.

An Application resource is available in for each application that is
  currently running in the cluster. This resource resides in the same
  namespace as the application that it corresponds to.

When an application, for which Veeam Kasten has at least one existing RestorePointContent from a previous backup, is deleted from the cluster, a Application resource representing the application is still available
  in the namespace where Veeam Kasten is installed. The resource will be
  marked as a deleted application, but it will be possible for an
  administrator to restore the application.

Apps are also available to track applications that have been deleted
  from the Kubernetes cluster, but are available to be restored based on
  an existing RestorePointContent captured by Veeam Kasten.

## Application Operations â

### List of Applications â

The Application API allows you to discover all applications that are
  installed and currently present on the Kubernetes cluster.

```
## list available applications$ kubectl get applications.apps.kio.kasten.io --namespace kasten-io \                           --field-selector=status.state=ActiveNAME                       AGEmy-app-1                   <unknown>my-app-2                   <unknown>my-app-3                   <unknown>
```

### List of Deleted Applications â

The Application API allows you to discover applications that Veeam
  Kasten can restore which have been previously deleted from the cluster.

```
## list deleted applications$ kubectl get applications.apps.kio.kasten.io --namespace kasten-io \                           --field-selector=status.state=DeletedNAME                       AGEmy-app-5                   <unknown>my-app-6                   <unknown>
```

### Restore of Deleted Applications â

In addition to discovery of deleted applications, Veeam Kasten makes it
  possible to restore an application that has been deleted but was
  previously protected.

The procedure, which requires Veeam Kasten administrative privileges, is
  as follows:

- Step 1: Find the RestorePointContent that corresponds to the desired point-in-time.
- Step 2: Re-create the namespace where you would like to restore the application.
- Step 3: Create a RestorePoint in the new namespace that is backed by the RestorePointContent . See Creating RestorePoint from RestorePointContent Example for details.
- Step 4: Initiate a RestoreAction to restore the application from the created RestorePoint . See RestoreAction for details.

### Get Application Components â

In addition to discovering the applications on the cluster, Veeam Kasten
  also tracks all resources associated with the application. You can get a
  summary of all resources (stateful and stateless) discovered in the
  context of the application. This is done by querying a details sub-resource for the particular application you
  are interested in.

```
## get the details of application named <APPNAME> in namespace <NS>## yq is used for readability$ kubectl get --raw /apis/apps.kio.kasten.io/v1alpha1/namespaces/<NS>/applications/<APPNAME>/details | yq -y .status.appDetailscomponents:  config:  - kind: secret    name: default-token-wghrq    namespace: sample-app  - kind: secret    name: muddled-saola-postgresql    namespace: sample-app  network:  - kind: service    name: muddled-saola-postgresql    namespace: sample-app  - kind: service    name: muddled-saola-postgresql-headless    namespace: sample-app  volumes:  - persistentVolumeClaimName: datadir    size: 1    type: EBS  workloads:  - kind: statefulset    name: muddled-saola-postgresql    namespace: sample-app
```

### Initiate Backup for an Application â

Apps can be protected on a scheduled basis using a Policy or in an
  ad hoc manner using a BackupAction .

For details see, Create a Backup Policy or BackupAction .

## Veeam Kasten App API Type â

The following is a complete specification of the Application resource.

The Application resource is read-only.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: apps.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: Application## Standard Kubernetes metadata. Required.metadata:  ## Name of the K10App. Auto-derived.  name: sample-app  ## Namespace of the K10App. Auto-derived.  namespace: sample-app  ## Timestamp for when the application was created.  creationTimestamp: '2019-02-11T03:03:47Z'## K10App parameters. Required.spec:  ## Currently only applications defines as namespaces are supported.  ## This may change in the near future with additional app types  ## Namespaced based app.  namespace:    ## Name of the namespace hosting the application    name: sample-app## Status of the K10App. Users should not set any data here.status:  ## State of the application.  ## Possible values:  ## Active - application is currently active  ## Deleted - application is not active but can be recovered  state: Active
```

## Veeam Kasten App Details API Type â

The following is a complete specification of the appDetails section of the Application API. These fields
  are only available in the Application API when the details sub-resource is used as shown in the example
  above.

```
apiVersion: apps.kio.kasten.io/v1alpha1kind: Application...spec:...status:  ...  ## Details about the components of the application.  appDetails:    ## Categorized components of the application.    components:      ## List of 'config' components.      config:        ## Zero or more elements.        ## Kind for config components.      - kind: secret        ## Kubernetes name of the component.        name: default-token-wghrq        ## Namespace of the component.        namespace: sample-app        ## API version of the component.        apiVersion: v1        ## Group name of the component.        group:        ## Resource name of the component.        resource: secrets        ## Annotations of the component.        annotations:        - sample-annotation: sample-app        ## List of blueprints bound to the resource via blueprint bindings.        boundBlueprints:          ## Name of the bound blueprint.        - name: my-blueprint          ## Namespace of the bound blueprint.          namespace: kasten-io          ## Reference to a source blueprint binding.          bindingRef:            name: my-blueprint-binding            namespace: kasten-io      ## List of 'network' components.      network:        ## Analogous to 'config'.        ## Possible kinds: service | ingress      ## List of 'workload' components.      workloads:        ## Analogous to 'config'.        ## Possible kinds: deployment | statefulset | cronjob      ## List of 'customresource' components.      customresources:        ## Analogous to 'config'.      ## List of 'volumes' components.      volumes:        ## Analogous to 'config' with the following additional fields:        ##   persistentVolumeClaimName - name of PVC        ##   podName - name of the pod        ##   size - size of underlying volume in GB        ##   type - identifier of disk type      - persistentVolumeClaimName: datadir        podName: sample-app-84xu1        size: 1        type: EBS    ## Additional component types maybe introduced.
```

---

## Api Policies

A Policy custom resource (CR) is used to perform operations on Veeam
  Kasten Policies. Policies allow you to manage application protection and
  migration at scale. You can learn more about using Veeam Kasten Policies
  in the Veeam Kasten Protecting Applications section.

## Example Policy Operations â

- Create a Backup Policy
- Create a Backup Policy using a Policy Preset
- Create an Import Policy
- Update a Policy
- Delete a Policy

### Create a Backup Policy â

The following example illustrates how to create a backup policy which
  executes hourly and retains 24 hourly and 7 daily snapshots. The policy
  covers an application running in the namespace sampleApp .

```
$ cat > sample-backup-policy.yaml <<EOFapiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: sample-backup-policy  namespace: kasten-iospec:  comment: My sample backup policy  frequency: '@hourly'  retention:    hourly: 24    daily: 7  actions:  - action: backup  selector:    matchLabels:      k10.kasten.io/appNamespace: sampleAppEOF$ kubectl apply -f sample-backup-policy.yamlpolicy.config.kio.kasten.io/sample-backup-policy created## make sure it initializes and validates properly$ kubectl get policies.config.kio.kasten.io --namespace kasten-io -wNAME                          STATUS    AGEsample-backup-policy          Success   12s
```

For complete documentation of the Policy CR, refer to Policy API
Type .

### Create a Backup Policy using a Policy Preset â

The following example illustrates how to create a backup policy which
  uses a predefined policy preset sample-policy-preset and covers an
  application running in the namespace sampleApp .

```
$ cat > sample-backup-policy-with-preset.yaml <<EOFapiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: sample-backup-policy-with-preset  namespace: kasten-iospec:  comment: My sample backup policy with preset  presetRef:    name: sample-policy-preset    namespace: kasten-io  actions:  - action: backup  selector:    matchLabels:      k10.kasten.io/appNamespace: sampleAppEOF$ kubectl apply -f sample-backup-policy-with-preset.yamlpolicy.config.kio.kasten.io/sample-backup-policy-with-preset created## make sure it initializes and validates properly$ kubectl get policies.config.kio.kasten.io --namespace kasten-io -wNAME                              STATUS    AGEsample-backup-policy-with-preset  Success   12s
```

For more information about PolicyPreset CR, refer to Policy Presets section.

### Create an Import Policy â

The following example illustrates how to create a policy which executes
  hourly and imports an application that was previously exported to the
  application-imports Profile .

```
$ cat > sample-import-policy.yaml <<EOFapiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: sample-import-policy  namespace: kasten-iospec:  comment: My sample import policy  frequency: '@hourly'  actions:  - action: import    importParameters:      profile:        namespace: kasten-io        name: application-imports      receiveString: <encoded string received on Export>EOF$ kubectl apply -f sample-import-policy.yamlpolicy.config.kio.kasten.io/sample-import-policy created## make sure it initializes and validates properly$ kubectl get policies.config.kio.kasten.io --namespace kasten-io -wNAME                          STATUS    AGEsample-import-policy          Success   12s
```

### Update a Policy â

To update a Policy , edit the spec portion of a Policy CR using your preferred method of submitting resource changes with
  [kubectl].

```
$ kubectl apply -f sample-backup-policy-changed.yamlpolicy.config.kio.kasten.io/sample-backup-policy configured
```

Once the change is submitted, Veeam Kasten will re-validate the Policy
  and update [.status.validation] accordingly.

```
$ kubectl get policies.config.kio.kasten.io --namespace kasten-io -wNAME                          STATUS    AGEsample-backup-policy          Pending   3ssample-backup-policy          Success   12s
```

Since Veeam Kasten processes API object changes asynchronously, to avoid
  confusion with a previous Policy status, it is recommended as
  convention that the status portion of the Policy is
  omitted when submitting changes.

### Delete a Policy â

You can delete a Policy using the following command.

```
## delete policy "sample-backup-policy" for Veeam Kasten installed in "kasten-io"$ kubectl delete policies.config.kio.kasten.io sample-backup-policy --namespace kasten-iopolicy.config.kio.kasten.io "sample-backup-policy" deleted## delete policy "sample-import-policy" for Veeam Kasten installed in "kasten-io"$ kubectl delete policies.config.kio.kasten.io sample-import-policy --namespace kasten-iopolicy.config.kio.kasten.io "sample-import-policy" deleted
```

## Policy Scheduling â

Within the Policy API Type , Veeam Kasten provides
  control of:

- How often the primary snapshot or import action should be performed
- How often snapshots should be exported into backups
- Which and how many snapshots and backups to retain
- When the primary snapshot or import action should be performed

### Frequency â

The frequency portion of the policy spec indicates how often the primary policy action should be performed. On
  demand policies run only when the run once button is clicked or a RunAction is created.

The optional frequency portion of exportParameters indicates how often snapshots should be
  exported into backups. If not specified, every snapshot is to be
  exported.

### Retention â

The retention portion of the policy spec indicates which and how many snapshots to retain.

The optional retention portion of the export action allows
  exported backups to be retained independently from snapshots. If not
  specified, exported backups are retained with the same schedule as
  snapshots.

### BackupWindow â

The optional backupWindow portion of the policy spec indicates when in the day the backup policy can be
  scheduled to run and by when any snapshot action must complete.

The start and end times of the backupWindow are specified
  by hour and minute. backupWindow length is limited to 24
  hours. If the end time specified is earlier than the start time, this
  means backupWindow end time is in the next day.

The policy is scheduled to run once at the backupWindow start time. If the policy has an hourly frequency and the duration of
  the backupWindow exceeds 1 hour, the policy is also
  scheduled to run every 60 minutes thereafter within the
  [backupWindow].

The snapshot action of the policy will be forcibly cancelled if it does
  not complete within the backup window. If the snapshot action completes
  within the backup window, no time restrictions are imposed on further
  actions such as snapshot export.

#### Staggering â

The optional enableStaggering portion of the policy spec indicates whether Veeam Kasten may choose when within
  the backupWindow to schedule the backup policy to run.

This allows Veeam Kasten the flexibility to stagger runs of multiple
  policies and reduce the peak load on the overall system.

The backupWindow is required when enableStaggering is set. The number of the scheduled
  policy runs within the backupWindow and the cancelling of
  in-progress snapshot actions at the end of the backupWindow are not affected by staggering.

### SubFrequency â

By default:

- Policies run once within the period of the frequency.
- Hourly policies run at the top of the hour.
- Daily policies run at midnight UTC.
- Weekly policies run at midnight Sunday UTC.
- Monthly policies run at midnight on the 1st of the month UTC.
- Yearly policies run at midnight on the 1st of January UTC.
- Snapshots and backups at those times are retained by the corresponding retention counts.

The optional subFrequency portion of the policy spec provides fine-grained control of when to run a
  policy, how many times to run a policy within a frequency, and which
  snapshots and backups are retained.

The frequency , subFrequency , backupWindow and retention interact as
  follows:

- When backupWindow is set, the time of day setting from subFrequency is not allowed
- backupWindow and subFrequency entries within the frequency indicate when the policy is to run e.g. the minutes and hours subFrequency entries indicate the minutes and hours at which a policy with a daily frequency runs e.g. backupWindow indicates the period of the day during which a policy with an hourly frequency runs e.g. backupWindow indicates the period of the day and subFrequency indicates the certain days of the week during which a policy with a weekly frequency runs
- subFrequency entries immediately within the frequency may have multiple values to run multiple times within the frequency e.g. multiple minutes may be specified for an hourly frequency (without backupWindow being set) e.g. multiple hours may be specified for a daily frequency (without backupWindow being set) e.g. multiple days may be specified for a monthly frequency (while backupWindow can indicate the common period of the day)
- subFrequency entries indicate which snapshots and backups graduate to higher retention tiers e.g. for a policy with an hourly frequency, the hours subFrequency entry indicates the hour of day that will graduate and be retained as a daily
- For subFrequency entries with multiple values, the first value indicates the time of the snapshot or backup to be retained by higher tiers e.g. an hourly frequency with subFrequency minutes entry of [45, 15] will run twice an hour at 15 and 45 minutes after the hour, will retain both according to the hourly retention count, and will graduate the hourly taken at 45 minutes after the hour designated by the subFrequency hour entry to the daily tier and higher
- When backupWindow is used, the start value indicates the time of the snapshot or backup to be retained by higher tiers e.g. for a policy with an hourly frequency, the start of backupWindow indicates the time of day that will graduate and be retained as a daily

- e.g. the minutes and hours subFrequency entries indicate the minutes and hours at which a policy with a daily frequency runs
- e.g. backupWindow indicates the period of the day during which a policy with an hourly frequency runs
- e.g. backupWindow indicates the period of the day and subFrequency indicates the certain days of the week during which a policy with a weekly frequency runs

- e.g. multiple minutes may be specified for an hourly frequency (without backupWindow being set)
- e.g. multiple hours may be specified for a daily frequency (without backupWindow being set)
- e.g. multiple days may be specified for a monthly frequency (while backupWindow can indicate the common period of the day)

- e.g. for a policy with an hourly frequency, the hours subFrequency entry indicates the hour of day that will graduate and be retained as a daily

- e.g. an hourly frequency with subFrequency minutes entry of [45, 15] will run twice an hour at 15 and 45 minutes after the hour, will retain both according to the hourly retention count, and will graduate the hourly taken at 45 minutes after the hour designated by the subFrequency hour entry to the daily tier and higher

- e.g. for a policy with an hourly frequency, the start of backupWindow indicates the time of day that will graduate and be retained as a daily

All time values in backupWindow and subFrequency entries in the API are
  in UTC.

If a subFrequency entry is omitted, it defaults as above (taking
  backupWindow into account, if set).

## Advanced Backup Policy Examples â

- Scheduling frequency and retention
- Export snapshots to a Veeam Repository

### Scheduling frequency and retention â

The following example illustrates how to use [frequency],
  [subFrequency], backupWindow and retention to create a backup policy that

- creates snapshots every day between 22:30 and 07:00
- exports the snapshot created on the fifteenth of the month including exporting snapshot data to create a durable and portable backup
- retains 14 daily snapshots
- retains 4 weekly snapshots from 22:30 each Friday
- retains 6 monthly snapshots from 22:30 on the fifteenth of each month
- retains 12 exported monthly backups from 22:30 on the fifteenth of each month
- retains 5 exported yearly backups from 22:30 on the fifteenth of January each year

- including exporting snapshot data to create a durable and portable backup

This policy covers an application running in the namespace sampleApp .

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: sample-custom-backup-policy  namespace: kasten-iospec:  comment: My sample custom backup policy  frequency: '@daily'  subFrequency:    weekdays: [5]    days: [15]  backupWindow:    start:      hour: 22      minute: 30    end:      hour: 7  retention:    daily: 14    weekly: 4    monthly: 6  actions:  - action: backup  - action: export    exportParameters:      frequency: '@monthly'      profile:        name: my-profile        namespace: kasten-io      exportData:        enabled: true    retention:      monthly: 12      yearly: 5  selector:    matchLabels:      k10.kasten.io/appNamespace: sampleApp
```

### Export snapshots to a Veeam Repository â

Snapshot data of vSphere CSI provisioned volumes in supported vSphere clusters
  can be exported to a Veeam Repository by
  adding a reference to a Veeam Repository Location Profile in the blockModeProfile field of the exportParameters .
  Only snapshot data is saved in the Veeam Repository. The remaining data
  associated with the restore point is saved in the location profile
  identified by the profile field of the exportParameters .

A block level copy of the snapshot is backed up to the specified Veeam
  repository. Configuring Change Tracking on the vSphere cluster nodes is not mandatory, but if configured it does enable the use
  of more efficient incremental backups of just the changes between
  snapshots when possible, instead of full backups every time.

All of the persistent volumes of an application are associated with a
  single restore point, per invocation of the policy. When an exported
  restore point is deleted, Veeam Kasten will also delete the
  corresponding restore point for the exported snapshots. Veeam Kasten
  always converts each backup into a synthetic full in order to support
  the policy retention functionality that permits the deletion of restore
  points in any order.

The following YAML illustrates how to create a policy that exports to a
  Veeam Repository:

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: sample-vbr-export  namespace: kasten-iospec:  comment: Sample backup and export to VBR policy  frequency: '@hourly'  retention:    hourly: 3  actions:  - action: backup  - action: export    exportParameters:      profile:        name: sample-profile        namespace: kasten-io      blockModeProfile:        name: sample-vbr-profile        namespace: kasten-io      exportData:        enabled: true      frequency: '@hourly'      retention:        daily: 7        hourly: 24        monthly: 12        weekly: 4        yearly: 7  selector:    matchLabels:      k10.kasten.io/appNamespace: sampleApp
```

The policy above maintains just 3 local restore points (and hence VMware
  snapshots) but uses a more sophisticated GFS retention policy for the
  exported restore points.

## Policy API Type â

The following is a complete specification of the Policy CR.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: config.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: Policy## Standard Kubernetes metadata. Required.metadata:  ## Policy name. May be any valid Kubernetes object name. Required.  ## Policy name is not mutable once created.  name: sample-backup-policy  ## Policy names must be unique and as an alternative to name above  ## one can take advantage of Kubernetes auto name generation.  generateName: backup-policy-  ## Policy namespace. Required. Can be namespace where Veeam Kasten is installed  ## or the namespace of the application. If the namesace of the application  ## is selected, then the policy can protect only that application.  namespace: kasten-io## Policy parameters. Required.spec:  ## User friendly comment describing the policy. Optional.  comment:  ## The name of the user who created the policy. Optional.  createdBy:  ## The name of the user who last updated the policy. Optional.  modifiedBy:  ## The hash of the policy spec block after the last modification made. Optional.  lastModifyHash:  ## Policy preset to be used by policy. Optional.  ## Allowed only for backup policy.  presetRef:    name: backup-preset    namespace: kasten-io  ## Selector for the application that the backup policy applies to.  ## Required for backup policy.  selector:    ## Standard Kubernetes set-based selector. Optional.    ## One of matchExpressions or matchLabels required.    ## When the namespace of the policy is the application's namespace,    ## the value in a matchExpression, matchLabel or both must match the    ## application's namespace. Only a single selector can be defined in    ## the matchExpression or matchLabel for application-scoped policies.    matchExpressions:      ## Standard Kubernetes set-based selector key.      ## 'k10.kasten.io/appNamespace' is a special label indicating that      ## the selector is targeting an application namespace      ## `kasten-io-cluster` is a special value for `k10.kasten.io/appNamespace`      ## that indicates that cluster-scoped resources should be backed up.      - key: k10.kasten.io/appNamespace        ## Standard Kubernetes set-based selector operator.        ## Only In is supported        operator: In        ## Array of values (labels on app names or wildcards) to use in the selector.        ## With this construct ANY value of the label key will match        ## Use this construct if creating a policy for multiple applications.        values:        - myApp        - myApp-* (will select all apps beginning with myApp-)    ## Standard Kubernetes label selector. Optional.    ## One of matchExpressions or matchLabels required.    #    ## NOTE: Label selector that resolves to a given Kubernetes resource    ## will have the effect of selecting the entire application that the    ## resource belongs to    matchLabels:      ## Map of label key and value pairs to match      ## 'k10.kasten.io/appNamespace' special label described above is supported      ## With this construct ALL labels must match for an object      myLabelKey1: myLabelValue1      myLabelKey2: myLabelValue2  ## Execution frequency. Required.  ## Allowable values: '@hourly', '@daily', '@weekly', '@monthly', '@yearly', '@onDemand'  ## frequency is not allowed when policy preset is used.  frequency: '@hourly'  ## Execution frequency modifier. Optional.  ## subFrequency specifies when to run and how many times to run within frequency.  ## subFrequency is not allowed for '@onDemand' frequency and with policy preset.  subFrequency:    ## minutes within hour (0-59). Optional.    ## Multiple minutes valid only for '@hourly' frequency.    ## Multiple minutes values must all be multiples of 5 minutes.    ## First entry determines minute of daily and longer retention.    ## minutes are not allowed when backupWindow is set.    minutes: [0,30]    ## hours within day (0-23). Optional.    ## Multiple hours valid only for '@daily' frequency.    ## First entry determines hour of weekly and longer retention.    ## hours are not allowed when backupWindow is set.    hours: [0]    ## days within week (0-7 (Sun-Sun)). Optional.    ## weekdays not valid for '@monthly' or '@yearly' frequencies.    ## Multiple weekdays valid only for '@weekly' frequency. With '@weekly'    ## frequency, first entry determines day of monthly and yearly retention.    weekdays: [0]    ## days within month (1-31). Optional.    ## days not valid for '@weekly' frequency.    ## Multiple days valid only for '@monthly' frequency.    ## First entry determines day of monthly and yearly retention.    days: [1]    ## months within year (1-12). Optional.    ## Multiple months valid only for '@yearly' frequency.    ## First entry determines month of yearly retention.    ## Valid for '@yearly' frequency.    months: [1]  ## Backup window. Optional.  ## backupWindow specifies the time period of the day when runs can occur within frequency and subFrequency.  ## backupWindow is not allowed for '@onDemand' frequency and with policy preset.  backupWindow:    ## Start of the window. Required.    start:      ## Hour within a day (0-23).      hour: 22      ## Minute within an hour (0-59). Must be a multiple of 5.      minute: 0    ## End of the window. Required.    end:      ## Hour within a day (0-23).      hour: 6      ## Minute within an hour (0-59). Must be a multiple of 5.      minute: 30  ## Staggering can be enabled only when backupWindow is set. Optional.  ## enableStaggering is not allowed when policy preset is used.  enableStaggering: false  ## Pause scheduled policy runs. Optional.  paused: false  retention:    ## Number of retained artifacts for different frequencies. Required except    ## for '@onDemand' frequency.    ## The number of retained artifacts can only be specified for frequencies    ## of the same or lower granularity than the policy frequency. For example,    ## if the policy frequency is '@daily', then retention can have values for    ## 'daily', 'weekly', 'monthly' and 'yearly', but not for 'hourly'.    ## If the policy frequency is 'hourly', then all retention values are    ## allowed. If the policy frequency is '@onDemand' or policy preset is used    ## then retention values are not allowed.    hourly: 24    daily: 7    weekly: 4    monthly: 12    yearly: 5  ## Actions executed by the policy. Required: at least one of backup or import.  actions:  ## Backup policy action.  ## Required when policy preset is used.  - action: backup    ## Optional backup parameters    backupParameters:      ## Filters describe which Kubernetes resources should be included or excluded      ## in the backup. If no filters are specified, all the API resources in a      ## namespace are captured by the BackupActions created by this Policy.      #      ## Resource types are identified by group, version, and resource type names,      ## or GVR, e.g. networking.k8s.io/v1/networkpolicies. Core Kubernetes types      ## do not have a group name and are identified by just a version and resource      ## type name, e.g. v1/configmaps.      #      ## Individual resources are identified by their resource type and resource      ## name, or GVRN. In a filter, an empty or omitted group, version, resource      ## type or resource name matches any value.      #      ## Filters reduce the resources in the backup by selectively including and      ## then excluding resources.      ## - If includeResources is not specified, all the API resources in a      ##   namespace are included in the set of resources to be backed up.      ## - If includeResources is specified, resources matching any GVRN entry in      ##   includeResources are included in the set of resources to be backed up.      ## - If excludeResources is specified, resources matching any GVRN entry in      ##   excludeResources are excluded from the set of resources to be backed up.      #      ## For RestorePoint usefulness after BackupActions, Veeam Kasten automatically      ## includes associated PVCs and PVs when a statefulset, deployment, or      ## deploymentconfig is included by includeResources unless the PVC is      ## excluded by excludeResources.      #      ## Backup policy that selects cluster-scoped resources may provide      ## optional filters that apply to any BackupClusterAction.      filters:        ## Include only resources that match any of the following NGVRs        includeResources:          ## Include individual resource        - name: <resource1 resource name>          group: <resource1 group>          version: <resource1 version>          resource: <resource1 type name>          ## Include resource type        - group: <resource2 group>          version: <resource2 version>          resource: <resource2 type name>        ## Exclude resources that match any of the following NGVRs        excludeResources:          ## Exclude specific instance of resource2 type        - name: <resource2 resource name>          group: <resource2 group>          version: <resource2 version>          resource: <resource2 type name>        ## Include only matching cluster-scoped resources        includeClusterResources:          ## Include individual resource        - name: <resource3 resource name>          group: <resource3 group>          version: <resource3 version>          resource: <resource3 type name>          ## Include resource type        - group: <resource4 group>          version: <resource4 version>          resource: <resource4 type name>        ## Exclude matching cluster-scoped resources        excludeClusterResources:          ## Exclude specific instance of resource4 type        - name: <resource4 resource name>          group: <resource4 group>          version: <resource4 version>          resource: <resource4 type name>      ## Optional: Location Profile that is used for this backup.      ## Profile used for Kanister-enabled operations and Generic Storage Backups.      ## profile is not allowed when policy preset is used.      profile:        name: my-profile        namespace: kasten-io      ## Optional: Ignore exceptions and continue if possible.      ## Snapshots with exceptions will be flagged as potentially flawed.      ## Default: false      ignoreExceptions: false      ## Optional: Hooks are Kanister actions executed first or last in a BackupAction.      ## A Kanister ActionSet is created with the application namespace as its subject.      ## The Blueprint must be in the Veeam Kasten namespace. Hooks do not use Location Profile.      hooks:        ## The Kanister action referenced by preHook will be executed before        ## other phases of the BackupAction. Optional.        preHook:          blueprint: backup-hook-blueprint          actionName: before-backup        ## The Kanister action referenced by onSuccess will be executed once all        ## other phases in the BackupAction have completed successfully. Optional.        onSuccess:          blueprint: backup-hook-blueprint          actionName: on-success        ## The Kanister action referenced by onFailure will be executed only        ## when the BackupAction fails and exhausts all retries. Optional.        onFailure:          blueprint: backup-hook-blueprint          actionName: on-failure  ## Export action. Export can only be specified after a backup action.  ## If policy uses a preset that enables export, export action will be  ## added to the policy automatically. Once the export will be disabled  ## in a preset, export action will be removed from the policy, unless  ## the export action has user-defined settings specified.  - action: export    exportParameters:      ## How often should a backup be exported. This frequency has to be less      ## or equal than the policy frequency. Optional.      ## For '@onDemand' policies this can only be '@onDemand' or excluded.      ## frequency is not allowed when using a preset.      frequency: '@hourly'      ## Location Profile that is used for this export. Required.      ## profile is not allowed when using a preset.      profile:        name: my-profile        namespace: kasten-io      ## The blockModeProfile is a reference to a profile that supports block based backup.      ## Optional. If set then a block mode backup of snapshot data will be performed      ## instead of a filesystem backup.      ## This should only be used when the infrastructure also supports block based backup.      ## blockModeProfile is not allowed when using a preset.      blockModeProfile:        ## Name of the location profile supporting block mode. Required.        name: my-block-mode-profile        ## Namespace of the location profile (must be the Veeam Kasten namespace). Required.        namespace: kasten-io      ## Backup portability setting.      ## Convert volume snapshots into an infrastructure-independent format. Optional.      exportData:        ## Default setting for all storage classes. Optional.        enabled: false        ## Storage class to use for any temporary PVCs created        ## during the snapshot conversion process. If not specified, the        ## storage class of the source volume is used. Optional.        exporterStorageClassName: gp2        ## Overrides for the default exportData setting specified above.        ## Use this if you want to modify the defaults for a PVC that        ## has a specific storage class. Optional.        overrides:            ## Override setting of a specific storage class.          - storageClassName: gp2            enabled: false          - storageClassName: gp2-eu-west-1a            enabled: true            exporterStorageClassName: io1      ## Volume snapshot destination region and account. Optional, or      ## with one of awsEbs or azure only. Non-portable export only.      ## volumeSnapshots is not allowed when using a preset.      volumeSnapshots:        awsEbs:          regions:            - us-east-1          ## Destination Account name.          destinationAccount: sample-destination-account        azure:          regions:            - eastus      ## Optional: Hooks are Kanister actions executed first or last in an ExportAction.      ## A Kanister ActionSet is created with the exported namespace as its subject.      ## The Blueprint must be in the Veeam Kasten namespace. Hooks do not use Location Profile.      hooks:        ## The Kanister action referenced by preHook will be executed before        ## other phases of the ExportAction. Optional.        preHook:          blueprint: export-hook-blueprint          actionName: before-export        ## The Kanister action referenced by onSuccess will be executed once all        ## other phases in the ExportAction have completed successfully. Optional.        onSuccess:          blueprint: export-hook-blueprint          actionName: on-success        ## The Kanister action referenced by onFailure will be executed only        ## when the ExportAction fails and exhausts all retries. Optional.        onFailure:          blueprint: export-hook-blueprint          actionName: on-failure    retention:      ## Optional exported artifact retention. If not provided, exported      ## artifacts are retained by the policy retention table.      ## Number of retained export artifacts for different frequencies.      ## The number of retained artifacts can only be specified for frequencies      ## of the same or lower granularity than the exportParameters frequency.      ## retention is not allowed when using a preset.      hourly: 24      daily: 7      weekly: 4      monthly: 12      yearly: 5  ## Import action.  - action: import    ## Parameters available to import actions. Required.    importParameters:      ## Location Profile that is used for this import. Required.      profile:        ## Profile name. Required.        name: sample-profile        ## Namespace where the Profile CR resides. Required.        namespace: kasten-io      ## Encoded string generated on Export. Required.      receiveString: VGhpcyBpcyBhIHNhbXBsZSBleHBvcnQgc3RyaW5nLgo=  ## Restore action. Restore can only be specified after an import action.  - action: restore    ## Optional restore parameters    restoreParameters:      ## Optional: set to true to only restore the application data to its original location      ## by overwriting existing PVC and re-scaling workloads.      ## Must be false if filters are specified.      ## Default: false      dataOnly: false      ## Optional: set to true to only restore the application data as a cloned volume      ## without overwriting existing PVC and re-scaling workloads.      ## Can be true if filters are specified.      ## Default: false      volumeClones: false      ## Optional: set to true to restore imported cluster-scope resources      ## Default: false      restoreClusterResources: false      ## Optional: Filters describe which Kubernetes resources should be restored      ## from the RestorePoint.  If no filters are specified, all the artifacts      ## in the RestorePoint are restored.      #      ## Filters reduce the resources restored by selectively including and then      ## excluding resources.      ## - If includeResources is not specified, all resources in the RestorePoint      ##   are included in the set of resources to be restored.      ## - If includeResources is specified, resources matching any GVRN entry in      ##   includeResources are included in the set of resources to be restored.      ## - If excludeResources is specified, resources matching any GVRN entry in      ##   excludeResources are excluded from the set of resources to be restored.      ## - In a filter, an empty or omitted group, version, resource type or      ##   resource name matches any value.      #      ## For precise control of RestoreActions, Veeam Kasten only restores resources that      ## are explicitly included by includeResources. For RestoreActions, when a      ## statefulset, deployment, or deploymentconfig is included by includeResources,      ## Veeam Kasten does not restore associated PVCs unless the PVC is included by      ## includeResources.      #      ## Restore action that selects cluster-scoped resources may provide      ## optional filters that apply to any imported ClusterRestorePoint.      filters:        ## Include only resources that match any of the following NGVRs        includeResources:          ## Include individual resource        - name: <resource1 resource name>          group: <resource1 group>          version: <resource1 version>          resource: <resource1 type name>          ## Include resource type        - group: <resource2 group>          version: <resource2 version>          resource: <resource2 type name>        ## Exclude resources that match any of the following NGVRs        excludeResources:          ## Exclude specific instance of resource2 type        - name: <resource2 resource name>          group: <resource2 group>          version: <resource2 version>          resource: <resource2 type name>        ## Include only matching cluster-scoped resources        includeClusterResources:          ## Include individual resource        - name: <resource3 resource name>          group: <resource3 group>          version: <resource3 version>          resource: <resource3 type name>          ## Include resource type        - group: <resource4 group>          version: <resource4 version>          resource: <resource4 type name>        ## Exclude matching cluster-scoped resources        excludeClusterResources:          ## Exclude specific instance of resource4 type        - name: <resource4 resource name>          group: <resource4 group>          version: <resource4 version>          resource: <resource4 type name>      ## The list of transforms. Optional.      ## Each transform can be defined inline or in a referenced transform set.      transforms:        ## Specifies which resource artifacts to apply this transform to. Required.        ## At least one filter should be set.      - subject:          ## Resource group. Optional.          group: apps          ## Resource version. Optional.          version: v1          ## Resource type. Optional.          resource: deployments          ## Resource name. Optional.          name: my-app        ## The name of the transform. Optional.        name: 'copyRelease'        ## An array of RFC-6902 JSON patch-like operations. Optional.        json:          ## Operation name. Required.          ## Transforms support six command operations:          ##   ## 'test' - checks that an element exists (and equals the value / matches the regexp if specified)          ##   ## 'add' - inserts a new element to the resource definition          ##   ## 'remove' - deletes an existing element from the resource definition          ##   ## 'copy' - duplicates an element, overwriting the value in the new path if it already exists          ##   ## 'move' - relocates an element, overwriting the value in the new path if it already exists          ##   ## 'replace' - replaces an existing element with a new element        - op: copy          ## Source reference for operation. Optional.          ## Required and valid only for 'move' and 'copy' operations.          from: '/metadata/labels/release'          ## Target reference for operation. Required for every operation.          path: '/spec/template/metadata/labels/release'          ## Regex to match expression. Optional.          ## When used with 'copy', 'move' or 'replace' operation,          ## the transform will match the target text against the `regex`          ## and substitute regex capturing groups with `value`.          ## When used with 'test' operation,          ## the transform will match the target text against the `regex`.          regex: 'prod-v.*'          ## Value is any valid JSON. Optional.          ## Required for 'add' and 'replace' operations.          ## Required for 'copy' and 'move' operations only when used along with `regex`.          ## 'test' operation can use either `regex` or `value`.          value: 'prod'        ## Transform set to be used instead of in-place JSON specification. Optional.        transformSetRef:          name: copy-release-transformset          namespace: kasten-io      ## Optional: Namespace where the application is to be restored.      ## Defaults to the namespace of the application in the imported      ## RestorePoint.      targetNamespace: mysql      ## Only used with Kanister blueprints that support point-in-time restore      ## Value is the desired timestamp. Optional.      pointInTime: "2019-02-11T05:13:10Z"      ## Optional: Hooks are Kanister actions executed first or last in a RestoreAction.      ## A Kanister ActionSet is created with the target namespace as its subject.      ## The Blueprint must be in the Veeam Kasten namespace. Hooks do not use Location Profile.      hooks:        ## The Kanister action referenced by preHook will be executed before        ## other phases of the RestoreAction. Optional.        preHook:          blueprint: restore-hook-blueprint          actionName: before-restore        ## The Kanister action referenced by onSuccess will be executed once all        ## other phases in the RestoreAction have completed successfully. Optional.        onSuccess:          blueprint: restore-hook-blueprint          actionName: on-success        ## The Kanister action referenced by onFailure will be executed only        ## when the RestoreAction fails and exhausts all retries. Optional.        onFailure:          blueprint: restore-hook-blueprint          actionName: on-failure      ## Optional: Virtual Machine restore parameters.      virtualMachineParameters:        ## Optional: restore parameters specific to virtual machines on the        ## SUSE Virtualization (Harvester) platform.        harvester:          ## Map of VM image PVCs to be restored and existing VM image references (identified by          ## name and namespace). After the restore, all references to VM images in the selected          ## VM image PVCs will be replaced with the provided new VM image references.          overrideVolumeImages:            vm-image-pvc-1:                ## Namespace where the VM image is located.                namespace: vm-image-1-ns                ## Name of the VM image used for override.                name: vm-image-1                ## ignoreChecks determines whether to skip VM image checksum validation during                ## the restore process.                 ignoreChecks: false            vm-image-pvc-2:                ## Namespace where the VM image is located.                namespace: vm-image-2-ns                ## Name of the VM image used for override.                name: vm-image-2                ## If ignoreChecks is set to true, the image will be used without verifying its integrity.                ## This is useful when intentionally using a different VM image than the one used in the backup.                ignoreChecks: true ## Report action.  - action: report    ## Parameters available to report actions. Required.    reportParameters:      ## Reports include metrics collected by the Veeam Kasten Prometheus service      ## and queried over an interval up to the time of the Report.      ## The query interval must be non-zero and is calculated to be      ## (24 * statsIntervalDays) + statsIntervalHours.      statsIntervalDays: 1      statsIntervalHours: 0## Status of the Policy. Users should not set any data here.status:  ## Validation status of the Policy  ## Valid values are:  ##   ## Pending - undergoing initialization and validation  ##   ## Success - successfully initialized and validated  ##   ## Failed - not properly initialized or validated  ## Only policies which have status of Success will be used by the system  validation: Success  ## An array of any validation or initialization errors encountered.  error: null  ## Hash of the spec portion of the policy.  ## Used internally to determine when successfully validated policies  ## need to be reprocessed.  hash: 3369880242
```

---

## Api Policypresets

A PolicyPreset custom resource (CR) is used to save and reuse
  configuration of Veeam Kasten Policies. Follow this page to learn more
  about using Veeam Kasten Policy Presets.

A PolicyPreset specifies schedule, retention, location and
  infrastructure information, while Policy that uses a preset is
  supposed to specify application specific information. A detailed
  description of the schedule settings can be found in the Policy Scheduling section.

For complete documentation of the PolicyPreset CR, refer to PolicyPreset API Type .

## Example PolicyPreset Operations â

- Create a PolicyPreset
- Update a PolicyPreset
- Delete a PolicyPreset

### Create a PolicyPreset â

The following example illustrates how to create a preset for policies
  which execute hourly, retain 24 hourly and 7 daily snapshots and export
  every daily snapshot with the same retention schedule as for snapshots
  (i.e. retain 7 daily exported snapshots).

```
$ cat > sample-policy-preset.yaml <<EOFapiVersion: config.kio.kasten.io/v1alpha1kind: PolicyPresetmetadata:  name: sample-policy-preset  namespace: kasten-iospec:  comment: My sample policy preset  backup:    frequency: '@hourly'    retention:      hourly: 24      daily: 7  export:    frequency: '@daily'    exportData:      enabled: true    profile:      name: my-location-profile      namespace: kasten-ioEOF$ kubectl apply -f sample-policy-preset.yamlpolicypreset.config.kio.kasten.io/sample-policy-preset created## make sure it initializes and validates properly$ kubectl get policypresets.config.kio.kasten.io --namespace kasten-io -wNAME                   STATUS   AGEsample-policy-preset   Success  32s
```

### Update a PolicyPreset â

To update a PolicyPreset , edit the [spec] portion of a PolicyPreset CR using your preferred method of submitting resource
  changes with [kubectl].

```
$ kubectl apply -f sample-policy-preset-changed.yamlpolicypreset.config.kio.kasten.io/sample-policy-preset configured
```

Once the change is submitted, Veeam Kasten will re-validate the PolicyPreset and update [.status.validation] accordingly.

```
$ kubectl get policypresets.config.kio.kasten.io --namespace kasten-io -wNAME                    STATUS   AGEsample-policy-preset    Failed   48ssample-policy-preset    Success  50s
```

Since Veeam Kasten processes API object changes asynchronously, to avoid
  confusion with a previous PolicyPreset status, it is recommended as
  convention that the [status] portion of the PolicyPreset is omitted when submitting changes.

Every preset's validation status change entails a revalidation of
    all the policies that use this preset. If the preset becomes invalid,
    the dependent policies also become invalid, and thus their runs will be
    skipped. Changing the preset's type (from being a backup only to
    backup+export and vice versa) also entails policies revalidation.

### Delete a PolicyPreset â

You can delete a PolicyPreset using the following command.

```
## delete policypreset "sample-policy-preset" for Veeam Kasten installed in "kasten-io"$ kubectl delete policypresets.config.kio.kasten.io sample-policy-preset --namespace kasten-iopolicypreset.config.kio.kasten.io "sample-policy-preset" deleted
```

All the policies that use the deleted preset will be automatically
    marked as invalid.

## PolicyPreset API Type â

The following is a complete specification of the PolicyPreset CR.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: config.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: PolicyPreset## Standard Kubernetes metadata. Required.metadata:  ## PolicyPreset name. May be any valid Kubernetes object name. Required.  ## PolicyPreset name is not mutable once created.  name: sample-backup-preset  ## PolicyPreset namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io## PolicyPreset parameters. Required.spec:  ## User friendly comment describing the policy preset. Optional.  comment:  ## Backup settings. Required.  backup:    ## Execution frequency. Required.    ## Allowable values: '@hourly', '@daily', '@weekly', '@monthly', '@yearly'    frequency:    ## Execution frequency modifier. Optional.    ## subFrequency specifies when to run and how many times to run within frequency.    subFrequency:      ## minutes within hour (0-59). Optional.      ## Multiple minutes valid only for '@hourly' frequency.      ## Multiple minutes values must all be multiples of 5 minutes.      ## First entry determines minute of daily and longer retention.      ## minutes are not allowed when backupWindow is set.      minutes: [0,30]      ## hours within day (0-23). Optional.      ## Multiple hours valid only for '@daily' frequency.      ## First entry determines hour of weekly and longer retention.      ## hours are not allowed when backupWindow is set.      hours: [0]      ## days within week (0-7 (Sun-Sun)). Optional.      ## weekdays not valid for '@monthly' or '@yearly' frequencies.      ## Multiple weekdays valid only for '@weekly' frequency. With '@weekly'      ## frequency, first entry determines day of monthly and yearly retention.      weekdays: [0]      ## days within month (1-31). Optional.      ## days not valid for '@weekly' frequency.      ## Multiple days valid only for '@monthly' frequency.      ## First entry determines day of monthly and yearly retention.      days: [1]      ## months within year (1-12). Optional.      ## Multiple months valid only for '@yearly' frequency.      ## First entry determines month of yearly retention.      ## Valid for '@yearly' frequency.      months: [1]    ## Backup window. Optional.    ## backupWindow specifies the time period of the day when runs can occur within frequency and subFrequency.    backupWindow:      ## Start of the window. Required.      start:        ## Hour within a day (0-23).        hour: 22        ## Minute within an hour (0-59). Must be a multiple of 5.        minute: 0      ## End of the window. Required.      end:        ## Hour within a day (0-23).        hour: 6        ## Minute within an hour (0-59). Must be a multiple of 5.        minute: 30    ## Staggering can be enabled only when backupWindow is set. Optional.    enableStaggering: false    ## Number of retained artifacts for different frequencies. Required.    ## The number of retained artifacts can only be specified for frequencies    ## of the same or lower granularity than the policy frequency. For example,    ## if the policy frequency is '@daily', then retention can have values for    ## 'daily', 'weekly', 'monthly' and 'yearly', but not for 'hourly'.    ## If the policy frequency is 'hourly', then all retention values are allowed.    retention:      hourly: 24      daily: 7      weekly: 4      monthly: 12      yearly: 5    ## Optional: Location Profile that is used for this backup.    ## Profile used for Kanister-enabled operations and Generic Storage Backups.    profile:      name: my-profile      namespace: kasten-io  ## Export settings. Optional.  export:    ## How often should a backup be exported. This frequency has to be less    ## or equal than the backup frequency. Optional.    ## If not specified, the backup frequency is used.    frequency: '@hourly'    ## Optional exported artifact retention. If not provided, exported    ## artifacts are retained by the backup retention table.    ## The number of retained artifacts can only be specified for frequencies    ## of the same or lower granularity than the export frequency.    ## If export frequency is set, but export retention is omitted,    ## the backup retention must be specified also for the export frequency granularity.    retention:      hourly: 24      daily: 7      weekly: 4      monthly: 12      yearly: 5    ## Location Profile that is used for export. Required.    profile:      name: my-profile      namespace: kasten-io    ## The blockModeProfile is a reference to a profile that supports block based backup.    ## Optional. If set then a block mode backup of snapshot data will be performed    ## instead of a filesystem backup.    ## This should only be used when the infrastructure also supports block based backup.    blockModeProfile:      name: my-block-mode-profile      namespace: kasten-io    ## Backup portability setting.    ## Convert volume snapshots into an infrastructure-independent format. Required.    exportData:      ## Default setting for all storage classes. Required.      enabled: true      ## Storage class to use for any temporary PVCs created      ## during the snapshot conversion process. If not specified, the      ## storage class of the source volume is used. Optional.      exporterStorageClassName: gp2      ## Overrides for the default exportData setting specified above.      ## Use this if you want to modify the defaults for a PVC that      ## has a specific storage class. Optional.      overrides:          ## Override setting of a specific storage class.        - storageClassName: gp2          enabled: false        - storageClassName: gp2-eu-west-1a          enabled: true          exporterStorageClassName: io1    ## Volume snapshot destination region and account. Optional, or    ## with one of awsEbs or azure only. Non-portable export only.    volumeSnapshots:      awsEbs:        regions:          - us-east-1        ## Destination Account name.        destinationAccount: sample-destination-account      azure:        regions:          - eastus## Status of the PolicyPreset. Users should not set any data here.status:  ## Validation status of the PolicyPreset  ## Valid values are:  ##   ## Success - successfully initialized and validated  ##   ## Failed - not properly initialized or validated  ## Only policy presets which have status of Success will be used by the system  validation: Success  ## An array of any validation or initialization errors encountered.  error: null  ## Detected type of the PolicyPreset  ## Valid values are:  ##  ## unknown - 'spec' is empty  ##  ## backup - only 'backup' portion of 'spec' is specified  ##  ## backup-export - both 'backup' and 'export' portions of 'spec' are specified  type: backup-export
```

---

## Api Profiles

As of March 5, 2024, "Azure Active Directory" has been renamed as
    "Microsoft Entra ID." Throughout this documentation, references to
    "Azure Active Directory" will be updated to use both the new and old
    names. Both names will be used for a while, after which the
    documentation will be updated to use only the new name.

A Profile custom resource (CR) is used to perform operations on Veeam
  Kasten Profiles. You can learn more about using Veeam Kasten Profiles at k10_config .

## Example Profile Operations â

- Create a Profile Secret
- Create an Object Store Location Profile
- Create an Infrastructure Profile
- Create a Veeam Repository Location Profile
- Create a Veeam Vault Location Profile
- Update a Profile
- Delete a Profile

### Create a Profile Secret â

When creating a Profile , you first need to create a Kubernetes secret
  that holds the credentials for the location associated with the profile.
  The examples below use an S3 bucket and therefore requires a properly
  formatted S3 secret.

```
$ kubectl create secret generic k10-s3-secret \      --namespace kasten-io \      --type secrets.kanister.io/aws \      --from-literal=aws_access_key_id=AKIAIOSFODNN7EXAMPLE \      --from-literal=aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

For complete documentation of secret formats, refer to Profile Secret
Types .

### Create an Object Store Location Profile â

With a secret already defined, you can now create an Object Store
  Location Profile . Object Store location profiles can be used for
  import as well as export operations.

```
$ cat <<EOF >>sample-profile.yamlapiVersion: config.kio.kasten.io/v1alpha1kind: Profilemetadata:  name: sample-profile  namespace: kasten-iospec:  type: Location  locationSpec:    credential:      secretType: AwsAccessKey      secret:        apiVersion: v1        kind: Secret        name: k10-s3-secret        namespace: kasten-io    type: ObjectStore    objectStore:      name: profile-s3-bucket      objectStoreType: S3      region: us-east-2EOF$ kubectl apply -f sample-profile.yamlprofile.config.kio.kasten.io/sample-profile created# make sure it is initialized and validated properly$ kubectl get profiles.config.kio.kasten.io --namespace kasten-io -wNAME                    STATUS    AGEsample-profile          Success   7s
```

For complete documentation of the Profile CR, refer to Profile API
Type .

### Create an Infrastructure Profile â

The example demonstrates how to create a AWS Infrastructure Profile ,
  but an analogous approach applies to creating an OpenStack Profile .

First, create a secret with the AWS credentials as described in AWS S3
and S3 Compatible Bucket
Secret .

```
$ cat <<EOF >>sample-aws-profile.yamlapiVersion: config.kio.kasten.io/v1alpha1kind: Profilemetadata:  name: sample-aws-profile  namespace: kasten-iospec:  infra:    aws:      hasAccessForEBS: true      hasAccessForEFS: true    credential:      secret:        apiVersion: v1        kind: secret        name: k10-aws-secret        namespace: kasten-io      secretType: AwsAccessKey    type: AWS  type: InfraEOF$ kubectl apply -f sample-aws-profile.yamlprofile.config.kio.kasten.io/sample-aws-profile created# make sure it is initialized and validated properly$ kubectl get profiles.config.kio.kasten.io --namespace kasten-io -wNAME                         STATUS    AGEsample-aws-profile           Success   7s
```

### Create a Veeam Repository Location Profile â

A Veeam Repository Location Profile is used to export or import vSphere CSI provisioned volume
  snapshot data in a supported vSphere cluster
  from a Veeam Repository . A Veeam Repository cannot be used to save restore points so
  such a location profile is always used in conjunction with another
  location profile that can be used to save restore point data.

This profile requires a secret whose creation is described in Veeam
Repository Secret . Once the secret has been
  created the Veeam Repository Location Profile is created as follows:

```
$ cat <<EOF >>sample-vbr-profile.yamlapiVersion: config.kio.kasten.io/v1alpha1kind: Profilemetadata:  name: sample-vbr-profile  namespace: kasten-iospec:  type: Location  locationSpec:    credential:      secretType: VBRKey      secret:        apiVersion: v1        kind: Secret        name: k10-vbr-secret        namespace: kasten-io    type: VBR    vbr:      repoName: Default Backup Repository      serverAddress: 192.168.1.218      serverPort: 9419      skipSSLVerify: trueEOF$ kubectl apply -f sample-vbr-profile.yamlprofile.config.kio.kasten.io/sample-vbr-profile created
```

The repoName field specifies the name of the repository to use; it
  should not be an immutable repository. The serverPort and skipSSLVerify fields are optional. For complete documentation of the Profile CR, refer to Profile API Type .

### Create a Veeam Data Cloud Vault Location Profile â

A Veeam Vault Location Profile is used to
  export or import data from a Veeam Vault .

This configuration must be produced through the Veeam Vault registration process but is documented here for reference.

This profile requires a secret whose creation is described in Veeam Data Cloud Vault Secret . Once the secret
  has been created the Veeam Vault Location Profile can be created as follows:

```
$ cat <<EOF >>sample-vbr-profile.yamlapiVersion: config.kio.kasten.io/v1alpha1kind: Profilemetadata:  name: sample-vault-profile  namespace: kasten-iospec:  type: Location  locationSpec:    credential:      secretType: VeeamVault      secret:        apiVersion: v1        kind: Secret        name: k10-vault-secret        namespace: kasten-io    type: ObjectStore    objectStore:      name: immutable-kasten      objectStoreType: VeeamVault      path: k10/<cluster_id>/migration      pathType: Directory      protectionPeriod: 720h0m0sEOF$ kubectl apply -f sample-vault-profile.yamlprofile.config.kio.kasten.io/sample-vault-profile created
```

#### Determining the selected Veeam Vault â

The Veeam storage vault selected during location profile creation is not shown again but if you require
  it, it can be determined by running the following commands by an administrator.

```
$ kubectl get profiles.config.kio.kasten.io --namespace kasten-io -w sample-vault-profile --output=jsonpath="{.spec.locationSpec.credential.secret.name}"k10secret-abcde
```

```
$ kubectl get secret --namespace kasten-io k10secret-abcde --output=jsonpath="{.data.veeam_vault_storage_account}" | base64 -dvault-storage-account-name
```

For complete documentation of the Profile CR, refer to Profile API Type .

### Update a Profile â

To update a Profile edit the [spec] portion of a Profile CR using your preferred method of submitting resource changes with kubectl .

```
$ kubectl apply -f sample-profile-changed.yamlprofile.config.kio.kasten.io/sample-profile configured
```

Once the change is submitted, Veeam Kasten will re-validate the profile
  and update .status.validation accordingly.

```
$ kubectl get profiles.config.kio.kasten.io --namespace kasten-io -wNAME                    STATUS    AGEsample-profile          Success   7s
```

Since Veeam Kasten processes API object changes asynchronously, to avoid
  confusion with a previous Profile status, it is recommended as
  convention that the status portion of the Profile is
  omitted when submitting changes.

### Delete a Profile â

You can delete a Profile using the following command.

```
# delete profile "sample-profile" for Veeam Kasten installed in "kasten-io"$ kubectl delete profiles.config.kio.kasten.io sample-profile --namespace kasten-ioprofile.config.kio.kasten.io "sample-profile" deleted
```

## Profile API Type â

The following is a complete specification of the Profile CR.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: config.kio.kasten.io/v1alpha1# Standard Kubernetes Kind declaration. Required.kind: Profile# Standard Kubernetes metadata. Required.metadata:  # Profile name. May be any valid Kubernetes object name. Required.  # Profile name is not mutable once created.  name: sample-location-profile  # Profile namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Profile parameters. Required.spec:  # Type of Profile. Required  # Valid values are Location, Infra  type: Location  # Only one of the profile type sections can be specified  # NOTE: camelCasing of the key is important  locationSpec:    # Credentials associated with profile location. Required.    credential:      # Type of secret being specified. Required.      # Valid values are:      #   # AwsAccessKey (Amazon S3 and Generic S3)      #   # GcpServiceAccountKey (Google Cloud Storage)      #   # AzStorageAccount (Azure Storage)      #   # VBRKey (Veeam Backup & Replication Storage)      #   # VeeamVault (Veeam Data Cloud Vault Storage)      secretType: AwsAccessKey      # Reference to K8s secret with credentials of secretType. Required.      secret:        # Standard Kubernetes API Version. Must be 'v1'. Required.        apiVersion: v1        # Standard Kubernetes Kind declaration. Must be 'secret'. Required.        kind: secret        # Secret name. May be any valid Kubernetes secret name. Required.        name: sample-profile-secret        # Secret namespace. Must be Veeam Kasten installed namespace . Required.        namespace: kasten-io    # Location for profile data. Required.    location:      # Type of location being specified. Required.      # Valid values are ObjectStore, FileStore, VBR      locationType: ObjectStore      # When the type above is ObjectStore. Required.      # Only one of the location type sections can be specified      objectStore:        # Type of object store. Required        # Valid values are:        #   # S3 (Amazon S3 and Generic S3)        #   # GCS (Google Cloud Storage)        #   # Azure (Azure Storage)        #   # VeeamVault (Veeam Data Cloud Vault Storage)        objectStoreType: S3        # The endpoint for object store API. Optional.        # Can be omitted unless an S3 compatible provider is used.        endpoint: ''        # If set to true, do not verify SSL cert. Optional.        # Default, when omitted, is false        skipSSLVerify: false        # Name of the object store bucket. Required        name: gmm-test        # Region valid for the object store provider.        # Required, if supported by provider.        # If provider does not support region, pass ""        region: us-east-2        # Path within bucket for profile artifacts. Optional.        # If not used, it will be generated by the system and        # updated during delayed initialization and validation.        # If used, it requires pathType below as well.        path: k10/q4ees3b2zilluaxw/migration        # Type of the path within the bucket above. Optional.        # Defaults to Directory if not specified.        pathType: Directory        # The protection period for immutable backups. Optional. Required if VeeamVault.        # Must be shorter than the bucket default retention        # period minus 20 days.        protectionPeriod: 240h      # When the type above is FileStore. Required.      # Only one of the location type sections can be specified      fileStore:        # Name of the Persistent Volume Claim. Required.        claimName: test-pvc        # Path within the PVC mount for profile artifacts. Optional.        # If not used, it will be generated by the system and        # updated during delayed initialization and validation.        path: k10/q4ees3b2zilluaxw/migration      # When the type above is VBR. Required.      # Only one of the location type sections can be specified      vbr:        # Address of the Veeam backup server. Required.        serverAddress: vbr-server        # VBR server RESTful API port number. Optional.        # Defaults to 9419 if not specified.        serverPort: 9419        # Name of the target Veeam cloud repository for backup files. Required.        repoName: k10-repo        # Identifier of the target Veeam cloud repository for backup files. Optional.        # Reserved field for internal use. Once the profile is created,        # this field will contain the ID of the repository specified in the repoName field.        repoId: 123e4567-e89b-12d3-a456-426614174000        # Type of the target Veeam cloud repository for backup files. Optional.        # Reserved field for internal use. Once the profile is created,        # this field will contain the type of the repository specified in the repoName field.        repoType: LinuxHardened        # If set to true, do not verify SSL cert. Optional.        # Default, when omitted, is false.        skipSSLVerify: false    # Optional: Make export to this profile infra-portable.    # Default: false    infraPortable: false  # When type above is Infra - Infrastructure profile. Required.  # Only one of the following profile type sections can be specified  # NOTE: camelCasing of the key is important  infra:    # type of Infrastructure profile. Required    # Valid values are OpenStack, Portworx, VSphere, AWS or GCP    type: OpenStack    # When type of this Infra profile above is OpenStack. Required.    # Only one of the following infra profiles can be specified    # NOTE: camelCasing of the key is important    openStack:      # Endpoint for the Keystone auth provider. Required      keystoneEndpoint: https://my-keystone-ip:1234    # When type of this Infra profile above is OpenStack. Required.    # Only one of the following infra profiles can be specified    # NOTE: camelCasing of the key is important    azure:      # Endpoint for the active directory login. Optional      ADEndpoint: https://login.microsoftonline.com/      # Resource ID to obtain AD tokens .Optional      ADResource: https://management.example.com/71fb132f-xxxx-4e60-yyyy-example47e19      # The name of Azure Cloud, e.g. AzurePublicCloud. Optional      cloudEnv: AzurePublicCloud      # Type of credentials used for profile. To be filled by controller      credentialType: ClientSecret      # Name of the Resource Group that was created for the Kubernetes cluster. Required      resourceGroup: myResourceGroup      # Endpoint for the resource manager. Optional      resourceManagerEndpoint: https://management.azure.com/      # Subscription ID for your Azure resources. Required      subscriptionID: 00000000-0000-0000-0000-000000000000      # Option to use the default Managed Identity. Optional      # If set to true, profile does not need a secret.      useDefaultMSI: true    portworx:      # The namespace of the Portworx service.      namespace: kube-system      # The name of the Portworx service.      serviceName: portworx-service    vsphere:      # The vSphere endpoint      serverAddress: vsphere.server.com    # Credentials associated with the infrastructure provider. Required.    credential:      # Type of secret being specified. Required.      # Valid values are:      #   # OpenStackAccount (OpenStack storage provider)      #   # PortworxKey (Portworx storage provider)      #   # VSphereKey  (vSphere storage provider)      #   # GcpServiceAccountKey  (GCP/GCS storage provider)      #   # AwsAccessKey  (AWS storage provider)      secretType: OpenStackAccount      # Reference to K8s secret with credentials of secretType. Required.      secret:        # Same format as above        # ###################### Status of the Profile. Users should not set any data here.status:      # Validation status of the Profile      # Valid values are:      #   # Success - successfully initialized and validated      #   # Failed - not properly initialized or validated      # Only profiles which have status of Success should be used      validation: Success      # An array of any validation or initialization errors encountered.      error: null      # Hash of the spec portion of the profile.      # Used internally to determine when successfully validated profiles      # need to be reprocessed.      hash: 3369880242
```

## Profile Secret Types â

The following are the different secret types and formats to be used with
  profiles.

- AWS S3 and S3 Compatible Bucket Secret
- GCS Bucket Secret
- Azure Storage Bucket Secret
- OpenStack Account Secret
- Portworx Key Secret
- vSphere Key Secret
- Veeam Repository Secret
- Veeam Data Cloud Vault

### AWS S3 and S3 Compatible Bucket Secret â

When a Profile is using an S3 or S3-compatible bucket location, the
  credential secret must follow the format below. In order to use
  temporary security credentials, you can generate an IAM role and provide
  it as a part of the S3 secret as shown below. Veeam Kasten supports the
  generation of temporary credentials to perform generic backups, export
  collections to an object store, and for EBS/EFS snapshot operations.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-s3-secret  # Secret namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Standard Kubernetes secret type. Must be Opaque. Required.type: secrets.kanister.io/aws# Secret data payload. Required.data:  # Base64 encoded value for key with proper permissions for the bucket  aws_access_key_id: QUtJQUlPU0ZPRE5ON0VYQU1QTEUK  # Base64 encoded value for the secret corresponding to the key above  aws_secret_access_key: d0phbHJYVXRuRkVNSS9LN01ERU5HL2JQeFJmaUNZRVhBTVBMRUtFWQo=  # (optional field) Base64 encoded value for AWS IAM role  role: YXJuOmF3czppYW06OjAwMDAwMDAwMDAwMDpyb2xlL2Zha2Utcm9sZQo=
```

Alternatively, the secret can be created using [kubectl] as
  follows.

### GCS Bucket Secret â

When a Profile is using a GCS Storage bucket location the credential
  secret must follow the format below.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-gcs-secret  # Secret namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Standard Kubernetes secret type. Must be Opaque. Required.type: Opaque# Secret data payload. Required.data:  # Base64 encoded value for project with proper permissions for the bucket  project-id: bXktcHJvamVjdC1pZAo=  # Base64 encoded value for the SA with proper permissions for the bucket  # This value is base64 encoding of the service account json file when  # creating a new service account, or the credential configuration json file  # when workload identity federation is used  service-account.json: <base64 encoded SA json file>
```

This example shows how to create a secret using a GCP service account
  JSON file , assuming that the service account has the necessary
  permissions for accessing your bucket and that the JSON file is located
  in your working directory.

```
$ kubectl create secret generic k10-gcs-secret \      --namespace kasten-io \      --from-literal=project-id=my-project-id \      --from-file=service-account.json=./gcs-access-service-account.json
```

This is an example that shows how to create a secret with a workload
  identity federation credentials configurations file, assuming that the
  service account the credentials will impersonate has the proper
  permissions for accessing your bucket, and that the json file is in your
  working directory.

```
$ kubectl create secret generic k10-gcs-secret \      --namespace kasten-io \      --from-literal=project-id=my-project-id \      --from-file=service-account.json=./clientLibraryConfig-gwif-creds.json
```

When using Google Workload Identity Federation with Kubernetes as the
    Identity Provider, ensure that the credential configuration file is
    configured with the format type ( --credential-source-type ) set to Text , and specify the OIDC ID token path ( --credential-source-file )
    as /var/run/secrets/kasten.io/serviceaccount/GWIF/token .

### Azure Storage Bucket Secret â

When a Profile is using an Azure Storage bucket location the
  credential secret must follow the format below.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-azure-secret  # Secret namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Azure Kubernetes secret type. Required.type: secrets.kanister.io/azure# Secret data payload. Required.data:  # Base64 encoded value for account with proper permissions for the bucket  azure_storage_account_id: QUtJQUlPU0ZPRE5ON0VYQU1QTEVBQ0NUCg==  # Base64 encoded value for the key corresponding to the account above  azure_storage_key: d0phbHJYVXRuRkVNSS9LN01ERU5HL2JQeFJmaUNZRVhBTVBMRUtFWQo=  # Base64 encoded value for the storage environment.  # Can be left empty. Acceptable values are AzureCloud, AzureChinaCloud, AzureUSGovernment  azure_storage_environment: QXp1cmVVU0dvdmVybm1lbnRDbG91ZA==
```

```
$ kubectl create secret generic k10-azure-secret \      --namespace kasten-io \      --type secrets.kanister.io/azure \      --from-literal=azure_storage_account_id=AKIAIOSFODNN7EXAMPLEACCT \      --from-literal=azure_storage_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \      --from-literal=azure_storage_environment=AzureUSGovernment
```

### Microsoft Entra ID Secret â

When a Profile uses Microsoft Entra ID (formerly Azure Active
  Directory) for authentication, the credential secret must follow the
  format below. Please note that an Azure infrastructure profile using the
  default Managed Identity does not need a secret.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-azure-secret  # Secret namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Azure Kubernetes secret type. Required.type: secrets.kanister.io/azure# Secret data payload. Required.data:  # Base64 encoded value for the tenant ID of the Microsoft Entra ID (formerly Azure Active Directory)  to be used for authentication.  azure_tenant_id: QUtJQUlPU0ZPRE5ON0VYQU1QTEVBQ0NUCg==  # Base64 encoded value for the client id of the identity to be used for authentication.  azure_client_key: MTIzNDU2NzgtMTIzNC0xMjM0LTEyMzQtZXhhbXBsZWNsaWVudGlkCg==  # Base64 encoded value for the client secret corresponding to the client id above.  azure_client_secret: d0phbHJYVXRuRkVNSS9LN01ERU5HL2JQeFJmaUNZRVhBTVBMRUtFWQo=
```

```
$ kubectl create secret generic k10-azure-secret \      --namespace kasten-io \      --type secrets.kanister.io/azure \      --from-literal=azure_tenant_id=AKIAIOSFODNN7EXAMPLEACCT \      --from-literal=azure_client_key=12345678-1234-1234-1234-exampleclientid \      --from-literal=azure_client_secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### OpenStack Account Secret â

When an Infrastructure Profile is being configured for accessing
  storage that supports the Open Stack Cinder interface, the credential
  secret must follow the format below:

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-openstack-infra-secret  # Secret namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Standard Kubernetes secret type. Must be Opaque. Required.type: Opaque# Secret data payload. Required.data:  # Base64 encoded value for an OpenStack user name to use with provider  os_username: b3MtdXNlcm5hbWUK  # Base64 encoded OpenStack password  os_password: b3MtcGFzc3dvcmQK  # Base64 encoded OpenStack domain  os_domain: b3MtZG9tYWluCg==  # Base64 encoded OpenStack project  os_project: b3MtcHJvamVjdAo=  # Base64 encoded OpenStack region  os_region: b3MtcmVnaW9u
```

```
$ kubectl create secret generic k10-openstack-secret \      --namespace kasten-io \      --from-literal=os_username=my-os-username \      --from-literal=os_password=my-os-password-user \      --from-literal=os_domain=my-os-domain \      --from-literal=os_project=my-os-project
```

### Portworx Key Secret â

When an Infrastructure Profile is being configured for accessing
  storage that supports the Portworx interface, the credential secret must
  follow the format below.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-portworx-infra-secret  # Secret namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Standard Kubernetes secret type. Must be Opaque. Required.type: Opaque# Secret data payload. Required.data:  # Base64 encoded value for a Portworx jwt issuer.  pwx_issuer: cHd4X2lzc3Vlcg==  # Base64 encoded value for a Portworx jwt secret.  pwx_secret: cHd4X3NlY3JldA==
```

```
$ kubectl create secret generic k10-portworx-infra-secret \      --namespace kasten-io \      --from-literal=pwx_issuer=my-pwx-issuer \      --from-file=pwx_secret=my-pwx-secret
```

### vSphere Key Secret â

When a vSphere Infrastructure Profile is being configured the credential secret must follow the
  format below.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-vsphere-infra-secret  # Secret namespace. Required. Must be namespace where Veeam Kasten is installed.  namespace: kasten-io# Standard Kubernetes secret type. Must be Opaque. Required.type: Opaque# Secret data payload. Required.data:  # Base64 encoded value for a vSphere user.  vsphere_user: dnNwaGVyZV91c2Vy  # Base64 encoded value for a vSphere password.  vsphere_password: dnNwaGVyZV9wYXNzd29yZA==
```

```
$ kubectl create secret generic k10-vsphere-infra-secret \      --namespace kasten-io \      --from-literal=vsphere_user=my-vsphere-user \      --from-file=vsphere_password=my-vsphere-password
```

### Veeam Repository Secret â

A Veeam Repository Location Profile requires a credential secret in the format below.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-vbr-secret  # Secret namespace. Required. Must be the namespace where Veeam Kasten is installed.  namespace: kasten-io# Standard Kubernetes secret type. Must be Opaque. Required.type: Opaque# Secret data payload. Required.data:  # Base64 encoded value for the Veeam server account name.  vbr_user: QWRtaW5pc3RyYXRvcg==  # Base64 encoded value for the password.  vbr_password: UEFTU1dPUkQ=
```

Alternatively, the secret can be created using [kubectl] as
  follows:

```
$ kubectl create secret generic k10-vbr-secret \  --namespace kasten-io \  --from-literal=vbr_user=Administrator \  --from-literal=vbr_password=PASSWORD
```

### Veeam Data Cloud Vault Secret â

A Veeam Data Cloud Vault Location Profile requires a credential secret in the format below.

```
# Standard Kubernetes API Version declaration. Required.apiVersion: v1# Standard Kubernetes Kind declaration. Required.kind: Secret# Standard Kubernetes metadata. Required.metadata:  # Secret name. May be any valid Kubernetes secret name. Required.  name: k10-vault-secret  # Secret namespace. Required. Must be the namespace where Veeam Kasten is installed.  namespace: kasten-io# Standard Kubernetes secret type. Must be Opaque. Required.type: Opaque# Secret data payload. Required.data:  # Base64 encoded value for the Veeam Vault client ID.  veeam_vault_client_id: bXljbGllbnRpZA==  # Base64 encoded value for the Veeam Vault TenantID.  veeam_vault_tenant_id: UEFTU1dPUkQ=  # Base64 encoded value for the Veeam Vault storage acct.  veeam_vault_storage_account: UEFTU1dPUkQ=
```

```
$ kubectl create secret generic k10-vault-secret \  --namespace kasten-io \    --from-literal=veeam_vault_client_id=myclientid \    --from-literal=veeam_vault_tenant_id=t-id \    --from-literal=veeam_vault_storage_account=my-storage-account
```

---

## Api Reports

The Report resource is in developer preview and a number of breaking
    changes to the resource API schema may happen in subsequent releases.

## Report â

A Report API resource captures information about the state of the
  system at the time the report was generated as well as select metrics
  collected from the Veeam Kasten Prometheus service. A Report is
  produced by a api_report_action when
  Veeam Kasten Reports are enabled.

Enabling and viewing Reports in the Veeam Kasten dashboard or with the
  API are discussed more fully in Reporting .

### Report API Type â

The following is a complete specification of the Report resource.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: reporting.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: Report## Standard Kubernetes metadata. Required.metadata:  ## Name of the Report. Required.  name: scheduled-45cfn-qwmcw  ## Namespace of the Report. Required.  namespace: kasten-io## Report parameters from ReportActionspec:  ## Time of Report generation  reportTimestamp: '2021-10-20T00:00:00Z'  ## Query Interval for Prometheus metrics in Report  statsIntervalDays: 1  statsIntervalHours: 0  statsIntervalStartTimestamp: '2021-10-19T00:00:00Z'  statsIntervalEndTimestamp: '2021-10-20T00:00:00Z'## Results contains captured system information.results:  ## General system information  general:    ## Veeam Kasten version    k10Version: '4.5'    ## Veeam Kasten namespace. Optional.    k10Namespace: kasten-io    ## Kubenetes version    k8sVersion: '1.21'    ## Cluster identifier. Optional.    clusterId: sample-cluster-ID    ## Cluster region. Optional.    clusterRegion: sample-cluster-region    ## Cluster name when multi-cluster was configured. Optional.    clusterName: sample-cluster    ## Infrastructure type    infraType:      ## Cloud provider. Possible values: azure, aws, gcp, unknown. Optional.      provider: aws      ## Whether the cluster is built with the use of Red HatÂ® OpenShiftÂ®      isOpenShift: false    ## Indicates the type of authentication. Possible values: basic, oidc, token, none. Optional.    authType: oidc    ## AWS information. For AWS clusters only. Optional.    aws:      ## AWS IAM role. Optional.      role: 'arn:aws:iam::123456789012:role/adminrole'  ## Licensing information  licensing:    ## License type    type: Enterprise    ## License expiry    expiry: '0000-00-00T00:00:00Z'    ## Nodes in use    nodeCount: 199    ## Maximum licensed nodes    nodeLimit: 220    ## License status    status: Valid  ## Veeam Kasten Action metrics from Prometheus. Optional.  actions:    ## Action count stats from Prometheus    countStats:      backup:        completed:        failed:        cancelled:        skipped:      backupCluster:        ...      export:        ...      import:        ...      report:        ...      restore:        ...      restoreCluster:        ...      run:        ...  ## Policy information  polices:    ## Veeam Kasten Disaster Recovery policy information    k10DR:      status: Enabled      backupFrequency: '@hourly'      immutability:        protection: Enabled        protectionDays: 30      profile: my-k10-dr-profile    ## Policy summary information    summaries:      - name: policy1        namespace: kasten-io        actions:          - backup        frequency: '@hourly'        profileNames:        paused: true        validation: Success      - name: policy2        namespace: basic-user-app        actions:          - backup            export        frequency: '@daily'        profileNames: basic-user-profile        validation: Success  ## Profile information  profiles:    ## Profile summary information    summaries:      - name: my-k10-dr-profile        type: Location        validation: Success        ## SSL verification status, if applicable.        sslVerification: Verify | SkipVerification        ## Profile setting forces infraportable data export, if applicable.        dataPortability: Enabled | omitted        ## Immutability        immutability:          protection: Enabled          protectionDays: 30        ## Object store type, if applicable.        objectStoreType: S3        region: sample-region        bucket: sample-bucket        ## Endpoint, if not default.        endpoint:        ## NFS location profile details        claimName:        path:        ## VBR server profile details        vbrServer:        vbrPort:        vbrRepoName:      - name: basic-user-profile        type: Location        validation: Success        sslVerification: Verify        immutability:          protection: Disabled          protectionDays: 0        ## Object store type, if applicable.        objectStoreType: S3        region: sample-region        bucket: basic-user-bucket  ## Compliance information  compliance:    ## Loading indicates compliance data not available. Omitted if false.    loading:    ## Count of total applications on system    applicationCount: 25    ## Count of compliant applications on system    compliantCount: 11    ## Count of non-compliant applications on system    nonCompliantCount: 2    ## Count of unmanaged applications on system    unmanagedCount: 12    ## Names of up to 10 non-compliant applications. Optional.    someNonCompliantApps:      - name: non-compliant-app-1      - name: non-compliant-app-2  ## Storage information  storage:    ## Snapshot information    snapshotStorage:      count: 243      logicalBytes: 275951648768      physicalBytes: 63568035264      freedBytes: ## Optional    ## Objectstore backup information    objectStorage:      count: 805      logicalBytes: 392624800      physicalBytes: 378777373      freedBytes: ## Optional    pvcStats:      pvcCount: 5      pvcBytes: 35433480192  ## Veeam Kasten services information from Prometheus. Optional.  k10Services:  - diskUsage:      freeBytes: 13789057024      freePercentage: 65      usedBytes: 7214526464    name: logging  - diskUsage:      freeBytes: 20267335680      freePercentage: 96      usedBytes: 736247808    name: catalog  - diskUsage:      freeBytes: 20228878336      freePercentage: 96      usedBytes: 774705152    name: jobs
```

### Retiring Reports â

By default the reports are not retired. To set up a retention count,
  update the policy spec to include the desired value:

```
kind: PolicyapiVersion: config.kio.kasten.io/v1alpha1metadata:## ... metadata fields ...spec:  ## Optional retention section can only have one child field: hourly, daily, weekly, monthly or yearly.  ## It also must correspond to the policy frequency (i.e. "@hourly" frequency must use hourly  ## retention field).  retention:    ## Number of the reports to keep (the oldest ones will be deleted).    ## Note: only automated reports will be deleted. Any report that was created    ## by a manual policy run or that was injected manually will be preserved.    daily: 2  ## ... other spec fields ...
```

---

## Api Repositories

## StorageRepository â

A StorageRepository API resource is used to represent how Veeam Kasten
  backup data is stored at a particular location (represented by a Profile<api_profile> ). Veeam Kasten will distribute
  backup data generated by a Policy<api_policy> run into
  one or more repositories, based on data type and deduplication domain.

The API gives the user an insight into the status of these repositories,
  and provides a means of performing maintenance and management actions on
  them.

### List StorageRepositories Example â

The following example illustrates listing all StorageRepositories created by a policy backing up two applications, each with PVCs.

```
### list storage repositories$ kubectl get storagerepositories.repositories.kio.kasten.io --namespace kasten-ioNAME                                     LOCATIONTYPEkopia-volumedata-repository-zcfk68hdht   ObjectStorekopia-volumedata-repository-hkpjmr2w6d   ObjectStorekopia-metadata-repository-2bgqbcf724     ObjectStore
```

### Get StorageRepositories Details Example â

In addition to getting a StorageRepository , you can also query the
  details associated with the restore point. You would use the details sub-resource for that purpose.

```
# get the details for storagerepository 'kopia-metadata-repository-2bgqbcf724' in the 'kasten-io' namespace.# yq only used for readability$ kubectl get --raw /apis/repositories.kio.kasten.io/v1alpha1/namespaces/kasten-io/storagerepositories/kopia-metadata-repository-2bgqbcf724/details | yq -y .status.detailskopiaMeta:  ...
```

### Modify StorageRepository Background Maintenance Behavior â

Veeam Kasten will periodically run maintenance on the StorageRepositories it creates. Among other tasks, the maintenance
  process tidies up unused data, detects inconsistent states, and measures
  the overall storage usage over time. This behavior can be disabled on a
  per-repository basis by modifying the
  [spec.disableMaintenance] field. Additionally, the
  background operations performed on the repository will, by default, have
  a 10-hour timeout. The timeout can be customized as needed by setting
  the [spec.backgroundProcessTimeout] field.

```
# disable maintenance for storagerepository# 'kopia-metadata-repository-2bgqbcf724' in the 'kasten-io' namespace.$ kubectl patch storagerepository kopia-metadata-repository-2bgqbcf724 -n kasten-io \ --type merge \ --patch $'spec:\n  disableMaintenance: true'# set the timeout for any background processes working on storagerepository# 'kopia-metadata-repository-2bgqbcf724' in the 'kasten-io' namespace.$ kubectl patch storagerepository kopia-metadata-repository-2bgqbcf724 -n kasten-io \ --type merge \ --patch $'spec:\n  backgroundProcessTimeout: 1h'# restore the 10h default timeout for background processes working on storagerepository# 'kopia-metadata-repository-2bgqbcf724' in the 'kasten-io' namespace.$ kubectl patch storagerepository kopia-metadata-repository-2bgqbcf724 -n kasten-io \ --type merge \ --patch $'spec:\n  backgroundProcessTimeout: null'
```

### Delete StorageRepository Example â

StorageRepository API resources can be deleted. Functionally, this
  only serves to clean up the API representation; no backup data will be
  deleted, and Veeam Kasten still tracks the associated repository data
  internally. After deletion, if the repository is used again (e.g., by
  creating a new backup), the StorageRepository API representation will
  be recreated.

```
### delete storage repository 'kopia-metadata-repository-cq6qrfd4vm' in namespace 'kasten-io'$ kubectl delete storagerepository kopia-metadata-repository-cq6qrfd4vm --namespace kasten-iostoragerepository.repositories.kio.kasten.io "kopia-metadata-repository-cq6qrfd4vm" deleted
```

### StorageRepository API Type â

The following is a complete specification of the StorageRepository resource.

```
### Standard Kubernetes API Version declaration. Required.apiVersion: repositories.kio.kasten.io/v1alpha1### Standard Kubernetes Kind declaration. Required.kind: StorageRepository### Standard Kubernetes metadata. Required.metadata:  ### Name of the StorageRepository. Required.  name: kopia-metadata-repository-2bgqbcf724  ### Namespace of the StorageRepository. Required.  namespace: kasten-io### Spec of the StorageRepository.spec:  ### Disable background maintenance for this repository.  disableMaintenance: false  ### Timeout (duration) for background tasks involving this repository.  ### If set to null, default value of 10h is used.  backgroundProcessTimeout: 10h  # If specified, this is the location that is used to connect  # to the repository. This field overrides the `status.location`  # field.  overrideLocation:    name: minio-profile    namespace: kasten-io### Status of the StorageRepository.status:  ### Content type of the data stored in this repository.  contentType: metadata  ### Backend type of this repository.  backendType: kopia  ### Details  details:    nextProcessTime:    modifiedTime:    kopiaMeta:      formatVersion: 2      repoStatus:        completedTime:        ### Capacity and available may not apply when repository is in cloud object store.        capacity:        available:        hash:        encryption:        splitter:        formatVersion:        indexFormat:      maintenanceInfo:        completedTime:        quick:          enabled: true          interval: 4h        full:          enabled: true          interval: 24h        nextFullMaintenanceTime:        nextQuickMaintenanceTime:        runs:        - start:          end:          success: true          error: null      maintenanceRun:        runsTotal: 100        deletedUnrefBlobsTotal: 100        cleanedLogsTotal: 100        recentResults:        - completedTime:          scheduledTime:          stats:            unusedContents: 0            unusedContentsRecent: 0            inUseContents: 0            inUseSysContents: 0            deletedUnrefBlobs: 0            keptLogs: 0            cleanedLogs: 0      storageUsage:        blobStats:          completedTime:          sizeStat:            count: 100            sizeB: 65536        snapshotStats:          completedTime:          sizeStat:            count: 100            sizeB: 65536  ### Location specifying where the data associated with this repository  ### can be found. This will match the format of the location spec  ### in a policy.  location:  ### If this repository was used only to import restore points, it is marked as read-only.  readOnly: false  ### The name of the application associated with the data in this repository.j  appName: kasten-io  ### Process results of recent background tasks run against this storage repository.  processResults:    ### Total number of times this storage repository was processed for any background task.    processCount: 0    ### The result of the last 10 background processing runs scheduled for this storage repository.    recentResults:    - start:      end:      ### The name of the procedure that was performed.      procedure: maintenanceRun      succeeded: true      error: null      commandResults:      ### Description of an individual command that was executed against the repository.      - desc: MaintenanceRun        startTime:        endTime:        error: null        succeeded: true
```

---

## Api Restorepoints

## RestorePoint â

A RestorePoint API resource is used to represent a Application that
  is captured at a specific time as a result of a BackupAction or a RestoreAction .

A RestorePoint resides in the namespace of the Application and
  access to it can be controlled using Kubernetes RBAC role and binding
  for the RestorePoint API.

### List RestorePoint Example â

The following example illustrates listing all RestorePoints for a
  sample application.

```
## list restore point in namespace 'sample-app'$ kubectl get restorepoints.apps.kio.kasten.io --namespace sample-appNAME                              AGEsample-app-backup-rp-raq923       1hsample-app-backup-rp-rdq309       2h
```

### Get RestorePoint Details Example â

In addition to getting a RestorePoint , you can also query the details
  associated with the restore point. You would use the
  [details] sub-resource for that purpose.

```
## get the details for restorepoint 'sample-app-backup-rp-raq923' created in 'mysql' namespace## yq only used for readability$ kubectl get --raw /apis/apps.kio.kasten.io/v1alpha1/namespaces/mysql/restorepoints/sample-app-backup-rp-raq923/details | yq -y .status.restorePointDetailsartifacts:  ...originatingPolicies:  ...
```

### Delete RestorePoint Example â

For RestorePoints created by policy, RestorePoints will
  automatically be deleted as part of the retention scheme that is
  specified.

A Veeam Kasten administrator may chose to not enable RBAC that allows
  deleting RestorePoints directly in order to force such operations to
  happen through policy retirement only.

```
## delete restore point 'sample-app-backup-rp-raq923' in namespace 'sample-app'$ kubectl delete restorepoints.apps.kio.kasten.io sample-app-backup-rp-raq923 --namespace sample-apprestorepoint.apps.kio.kasten.io/sample-app-backup-rp-raq923 deleted
```

Currently, deleting a RestorePoint manually does not delete the
    underlying resources. For all associated resources (e.g. persistent
    volumes, application-level artifacts, etc.) to be reclaimed, see, Delete RestorePointContent Example

### Creating RestorePoint from RestorePointContent Example â

When an application which has previously been protected by Veeam Kasten
  is deleted, the RestorePoints associated with the application are no
  longer available, but the corresponding RestorePointContent resources
  remain available. A Veeam Kasten administrator has the opportunity
  re-create a RestorePoint that would be [bound] to the RestorePointContent .

The following example illustrates creating a RestorePoint in the mysql namespace. The operation requires that the caller has read
  access to the RestorePointContent resource.

```
$ cat > create-rp-from-rpc.yaml <<EOFapiVersion: apps.kio.kasten.io/v1alpha1kind: RestorePointmetadata:  name: new-restore-point  namespace: mysqlspec:  restorePointContentRef:    name: rpc-mysql-backupEOF$ kubectl create -f create-rp-from-rpc.yamlrestorepoint.apps.kio.kasten.io/new-restore-point created#validate that the new restore point is bound$ kubectl get restorepoints.apps.kio.kasten.io new-restore-point --namespace mysql \       -ojsonpath="{.status.state}{'\n'}"Bound
```

### RestorePoint API Type â

The following is a complete specification of the RestorePoint resource.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: apps.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: RestorePoint## Standard Kubernetes metadata. Required.metadata:  ## Name of the RestorePoint. Required.  name: sample-restore-point  ## Namespace of the RestorePoint. Required.  namespace: sample-app  ## Kubernetes labels  labels:    ## Labels that can be used for filtering.    ## Automatically populated when creating the the resource    k10.kasten.io/appName: sample-app    k10.kasten.io/appNamespace: sample-app## Restore point resource parametersspec:  ## Reference to the underlying RestorePointContent resource.  ## When creating a RestorePoint the caller need to have  ## read access to the RestorePointContent being referenced.  restorePointContentRef:    ## Name of the underlying RestorePointContent resource    name: rpc-sample-app-backip-art245## Status of the RestorePointContent. Users should not set any data here.status:  ## State of the resource.  ## Possible values:  ##   Bound - corresponding RestorePoint resource exists  ##   Unbound - no RestorePoint references the resource  state: Bound  ## Size of the volumes contained within this RestorePoint.  logicalSizeBytes: 17179869184  ## Reported size of the snapshots contained within this RestorePoint.  physicalSizeBytes: 4852012  ## Scheduled backup or import time associated with the resource.  ## Could be 'null' for on-demand actions.  scheduledTime: '2019-02-11T03:03:47Z'  ## Time of actual creation by the corresponding action  actionCreationTime: '2019-02-11T03:03:47Z'
```

## RestorePointContent â

A RestorePointContent API resource backs the content of a RestorePoint .

When a RestorePoint exists for a given RestorePointContent , that RestorePointContent resource is [bound]. If there is no
  corresponding RestorePoint (e.g. application was deleted), then the
  resource is [unbound].

Deletion of a RestorePointContent resource frees up the artifacts
  associated with the restore point content and deletes any bound RestorePointContents .

Access to RestorePointContent is typically reserved for users with
  Veeam Kasten administrative privileges through Kubernetes RBAC since the
  resources are cluster-scoped.

### List RestorePointContent Example â

RestorePointContent resources can be listed similarly to RestorePoint resources, but the operation is non-namespaced.

In addition, to get the RestorePointContent resources associated with
  a specific Application , you can use a label selector to constrain your
  query.

```
## list RestorePointContent resources for 'sample-app'## assume Veeam Kasten is installed in 'kasten-io'$ kubectl get restorepointcontents.apps.kio.kasten.io \    --selector=k10.kasten.io/appName=sample-appNAME                              AGEsample-app-backup-rp-raq923       1hsample-app-backup-rp-rdq309       2h
```

### Get RestorePointContent Details Example â

In addition to getting a RestorePointContent , you can also query the
  details associated with the restore point content. You would use the
  [details] sub-resource for that purpose.

```
## get the details for restorepointcontent 'sample-app-backup-rp-raq923'## yq only used for readability$ kubectl get --raw /apis/apps.kio.kasten.io/v1alpha1/restorepointcontents/sample-app-backup-rp-raq923/details | yq -y .status.restorePointContentDetailsartifacts:  ...originatingPolicies:  ...
```

### Delete RestorePointContent Example â

In addition to policy-based deletion of RestorePoints and RestorePointContents , you can explicitly delete a RestorePointContent . Deleting a RestorePointContent will cause its
  bound RestorePoints and all associated resources (e.g. persistent
  volumes, application-level artifacts, etc.) to be reclaimed.

Deleting a RestorePointContent resource creates a RetireAction that can
  be examined to monitor progress of the retirement.

Deletion of a RestorePointContent is permanent and overrides retention
    by a Policy .

Some resources associated with the deleted restore point content may be
    cleaned immediately, while others, such as backup data exported to an
    object store, may take much longer to be completely removed. Data
    references shared between restore points, aggregated data awaiting
    garbage collection, version retention for immutable backups, and safety
    windows for re-referencing data are among the reasons why retiring a
    restore point might not immediately free up space in the underlying
    storage.

Additionally, due to data deduplication, some retirements may result in
    minimal or no resource usage reclamation. It is important to note that
    the increase in storage usage when creating a restore point does not
    reflect the expected space reclamation once the restore point is cleaned
    up.

The following example illustrates deleting a RestorePointContent . The
  operation requires that the caller has delete access to the RestorePointContent resource.

```
## delete restore point content 'sample-app-backup-rpc-raq923'$ kubectl delete restorepointcontents.apps.kio.kasten.io sample-app-backup-rpc-raq923restorepointcontent.apps.kio.kasten.io/sample-app-backup-rpc-raq923 deleted
```

### RestorePointContent API Type â

The following is a complete specification of the RestorePointContent resource.

The RestorePointContent resource cannot be created directly.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: apps.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: RestorePointContent## Standard Kubernetes metadata. Required.metadata:  ## Name of the RestorePointContent. Required.  name: sample-restore-point-content  ## Kubernetes labels  labels:  ## Labels that can be used fot filtering.  ## Automatically populated when creating the the resource  k10.kasten.io/appName: sample-app  k10.kasten.io/appNamespace: sample-app## Status of the RestorePointContent. Users should not set any data here.status:  ## State of the resource.  ## Possible values:  ##   Bound - corresponding RestorePoint resource exists  ##   Unbound - no RestorePoint references the resource  state: Bound  ## Scheduled backup or import time associated with the resource.  ## Could be 'null' for on-demand actions.  scheduledTime: '2019-02-11T03:03:47Z'  ## Time of actual creation by the corresponding action  actionCreationTime: '2019-02-11T03:03:47Z'
```

## ClusterRestorePoint â

A ClusterRestorePoint API resource is created by a BackupClusterAction that captures cluster-scoped resources. A RestoreClusterAction is used to restore cluster-scoped resources from
  a ClusterRestorePoint .

Deleting a ClusterRestorePoint resource frees up the artifacts
  associated with it.

Access to ClusterRestorePoint is typically reserved for users with
  Veeam Kasten administrative privileges through Kubernetes RBAC since the
  resources are cluster-scoped.

### List ClusterRestorePoint Example â

ClusterRestorePoint resources can be listed similarly to RestorePoint resources, but the operation is non-namespaced.

```
## list ClusterRestorePoint resources$ kubectl get clusterrestorepoints.apps.kio.kasten.ioNAME                               CREATED ATscheduled-6b5s8                    2020-12-29T23:57:20Zscheduled-szmhn                    2020-12-28T23:57:16Zbackup-cluster-action-fqbrndc5bz   2020-12-22T00:27:37Zbackup-cluster-action-fqbrn        2020-12-22T00:22:30Zscheduled-w86gf                    2020-12-21T22:08:30Zbackup-cluster-action-dnxl6        2020-12-19T01:20:53Z
```

### Delete ClusterRestorePoint Example â

In addition to policy-based deletion of ClusterRestorePoints , a ClusterRestorePoint can be directly deleted.

Deleting a ClusterRestorePoint resource creates a RetireAction that
  frees up the artifacts associated with the ClusterRestorePoint and
  that can be examined to monitor progress of the retirement.

Deletion of a ClusterRestorePoint is permanent and overrides retention
    by a Policy .

The following example illustrates deleting a ClusterRestorePoint . The
  operation requires that the caller has delete access to the ClusterRestorePoint resource.

```
## delete cluster restore point 'backup-cluster-action-raq923'$ kubectl delete clusterrestorepoints.apps.kio.kasten.io backup-cluster-action-raq923clusterrestorepoint.apps.kio.kasten.io "backup-cluster-action-raq923" deleted
```

### ClusterRestorePoint API Type â

The following is a complete specification of the ClusterRestorePoint resource.

```
## Standard Kubernetes API Version declaration. Required.apiVersion: apps.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: ClusterRestorePoint## Standard Kubernetes metadata. Required.metadata:  ## Name of the ClusterRestorePoint. Required.  name: sample-cluster-restore-point  ## Kubernetes labels  labels:  ## Labels that can be used fot filtering.  ## Populated for policy initiated BackupClusterAction only.  k10.kasten.io/policyName: "sample-originating-policy"  k10.kasten.io/policyNamespace: "namespace-of-policy"## Status of the ClusterRestorePoint. Users should not set any data here.status:  ## Scheduled backup or import time associated with the resource.  ## Could be 'null' for on-demand actions.  scheduledTime: '2019-02-11T03:03:47Z'  ## Time of actual creation by the corresponding action  actionTime: '2019-02-11T03:03:47Z'
```

---

## Api Storagesecuritycontexts

A StorageSecurityContext custom resource (CR) represents pod security
  context settings to access target storage to execute backup and restore
  operations. Once the StorageSecurityContext is created and bound to
  specific storage using StorageSecurityContextBinding , Veeam Kasten
  will use the parameters set in the StorageSecurityContext for its
  internal pods, which access bound storage.

If the target storage type is NFS/SMB and a StorageSecurityContext is
    used for restoration, the owner of the restored files and directories
    will be set to the UID and GID specified in the StorageSecurityContext .

## StorageSecurityContextBinding â

StorageSecurityContextBinding binds a StorageSecurityContext to a
  storage.

Only a single binding of a particular type can be created for a
    storage. If multiple bindings with the same type are found, Veeam Kasten
    will stop execution with an error.

Bindings might be one of three types:

- Volume - binds StorageSecurityContext to a PV.
- StorageClass - binds StorageSecurityContext to a StorageClass.
- Provisioner - binds StorageSecurityContext to a Provisioner.

## Example of StorageSecurityContext and StorageSecurityContextBindings Usage â

- Create a StorageSecurityContext
- Create a StorageSecurityContextBinding

As an example, an NFS storage with the filestore.csi.storage.gke.io StorageClass is used.

To enable snapshotting for NFS storage in rootless mode, two requirements must be met:

- NFS CSI driver should support VolumeSnapshots
- NFS CSI driver should support fsGroup

If you have a lost+found directory on the target volume, you can
    either remove it or change the owner's GID to match the GID set for the
    other files on the volume. This adjustment will allow Veeam Kasten to
    read the directory. By default, the lost+found directory has UID=root
    and GID=root, making it unreadable in rootless mode.

In this example, only UID and GID are set in the StorageSecurityContext . However, if a target storage contains files or
  directories owned by several different GIDs, SupplementalGroup should
  also be used to enable Veeam Kasten to read all the data. Please note
  that after the restore, the owner of files and directories will be set
  to the UID and GID specified in the StorageSecurityContext .

### Create a StorageSecurityContext â

The following example illustrates how to create a StorageSecurityContext for NFS storage:

```
$ cat > sample-storage-security-context.yaml << EOFapiVersion: config.kio.kasten.io/v1alpha1kind: StorageSecurityContextmetadata:  name: "sample-storage-security-context"  namespace: kasten-iospec:  security:    userId: 1005    groupId: 1006    supplementalGroups: []EOF$ kubectl apply -f sample-storage-security-context.yamlstoragesecuritycontext.config.kio.kasten.io/sample-storage-security-context added## make sure it initializes and validates properly$ kubectl get storagesecuritycontext.config.kio.kasten.io --namespace kasten-io
```

For complete documentation of StorageSecurityContext CR , please refer
  to StorageSecurityContext API Type .

When the StorageSecurityContext is applied, Veeam Kasten will start a
  pod that reads the target storage with UID=1005 and GID=1006. If the
  target storage contains files owned by other users, which cannot be
  accessed by the provided UID and GID, Veeam Kasten will fail to complete
  the Export process.

### Create a StorageSecurityContextBinding â

The following example illustrates how to create a StorageSecurityContextBinding to bind the StorageSecurityContext named "sample-storage-security-context" to all storages created with filestore.csi.storage.gke.io Provisioner.

When creating a StorageSecurityContextBinding , make sure to create
    a StorageSecurityContext first. Otherwise, the validation of the StorageSecurityContextBinding will fail.

```
$ cat > sample-storage-security-context-binding.yaml << EOFapiVersion: config.kio.kasten.io/v1alpha1kind: StorageSecurityContextBindingmetadata:  name: sample-storage-security-context-binding  namespace: kasten-iospec:  storageSecurityContextRef:    name: sample-storage-security-context  subjects:    - kind: Provisioner      name: "filestore.csi.storage.gke.io"EOF$ kubectl apply -f sample-storage-security-context-binding.yamlstoragesecuritycontextbinding.config.kio.kasten.io/sample-storage-security-context-binding added## make sure it initializes and validates properly$ kubectl get storagesecuritycontextbinding.config.kio.kasten.io --namespace kasten-io
```

For complete documentation of StorageSecurityContextBinding CR , please
  refer to StorageSecurityContextBinding API
Type .

## StorageSecurityContext API Type â

```
# Standard Kubernetes API Version declaration. Required.apiVersion: config.kio.kasten.io/v1alpha1# Standard Kubernetes Kind declaration. Required.kind: StorageSecurityContext# Standard Kubernetes metadata. Required.metadata:  # StorageSecurityContext name. May be any valid Kubernetes object name. Required.  # StorageSecurityContext name is not mutable once created.  name: sample-storagesecuritycontext  # StorageSecurityContext namespace. Required. Must be the namespace where Veeam Kasten is installed.  namespace: kasten-io# StorageSecurityContext parameters. Requiredspec:  # Security-related parmaeters for StorageSecurityContext. Required  security:    # Internal pods which work with the storage will use this field as UID    # Optional    userId: 0    # Internal pods which work with the storage will use this field as GID    # Optional    groupId: 0    # Groups set in this field will be added to the internal pods which work with the storage    # Optional    supplementalGroups: []
```

## StorageSecurityContextBinding API Type â

```
# Standard Kubernetes API Version declaration. Required.apiVersion: config.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: StorageSecurityContextBinding# Standard Kubernetes metadata. Required.metadata:  # StorageSecurityContextBinding name. May be any valid Kubernetes object name. Required.  # StorageSecurityContextBinding name is not mutable once created.  name: sample-storagesecuritycontextbinding  # StorageSecurityContextBinding namespace. Required. Must be the namespace where Veeam Kasten is installed.  namespace: kasten-io# StorageSecurityContext parameters. Requiredspec:  # Reference to StorageSecurityContext which will be applied to subjects  storageSecurityContextRef:    name: sample-storagesecuritycontext  # List of selectors to select storages where StorageSecurityContext will be applied to  subjects:      # Possible values Volume, StorageClass, Provisioner    - kind: StorageClass      name: "sample-storageclass"      # Namespace is used only in a case when kind=Volume      namespace: ""
```

---

## Api Transforms

Transforms enable modifications to Kubernetes resources on restore.
  Restore actions may include transforms to modify resources prior to
  creation in the target environment.

Transforms are loosely modeled on JSON Patch
  ( RFC-6902 ) which structures
  patches into patch documents containing patch operations. Transforms
  follow a similar structure to JSON Patch, with transform documents
  containing transform commands. Transforms deviates from JSON Patch in
  its support for regular expressions and path globbing.

To take advantage of Kubernetes native RBAC or reuse transforms, they
  can be aggregated into TransformSet custom resources. Follow Transform Sets page to
  learn more.

## Transform Structure â

A transform document is composed of transformation commands to be
  performed on a subject . Each transformation command within the
  document is performed in sequence. Processing halts if a transform
  command results in an error. If the error is the result of a test failure processing will continue to the next document, otherwise the
  restore will fail.

The example below contains two transform documents that contains two
  commands. The first command, test , checks for the presence of the 'metadata/labels/release' element within a deployment resource. The copy command following the test will execute if the test succeeds.

The second document will be evaluated independent of the first document.
  The second document replaces the "/metadata/labels/component" key
  value with "webserver" only if the value is "nginx" .

```
transforms:## Group, version, resource and/or name of the resource for transformation.## Every transform should have at least one resource specified.- subject:    resource: deployments  ## The name of the transform. Required.  name: 'copyRelease'  ## ``json`` key below indicates JSON patch document object used to perform  ## a JSON patch-like transform. Required.  json:  - op: test    ## reference for operation. mandatory.    path: '/metadata/labels/release'  - op: copy    ## source reference for operation. only valid for the 'move' and 'copy' operations    from: '/metadata/labels/release'    ## target reference for operation. mandatory.    path: '/spec/template/metadata/labels/release'    ## apply regex to match expression. Valid for 'replace', 'move',    ## 'copy' and 'test'.    regex: 'prod-v.*'    ## value is any json structure. only valid for 'add', 'replace'    ## and 'test' operation    value: 'prod'### Second transform document also applies transform to deployments.## Transforms on a resource are guaranteed to be applied in the order## specified in the restore action.### Group, version, resource and/or name of the resource for transformation.## Every transform should have at least one resource specified.- subject:    resource: deployments  ## The name of the transform. Required.  name: 'replaceLabelComponent'  ## ``json`` key below indicates JSON patch document object used to perform  ## a JSON patch-like transform. Required.  json:  - op: test    ## reference for operation. mandatory.    path: '/metadata/labels/component'  - op: replace    ## reference for operation. mandatory.    path: '/metadata/labels/component'    ## use regex to test for presence of element value for replacement    regex: 'nginx'    ## value is any json structure. only valid for 'add', 'replace'    ## and 'test' operation    value: 'webserver'
```

Transforms supports six command operations test , add , remove , copy , move and replace :

- test checks that an element exists (and equals the value / matches the regexp if specified).
- add inserts a new element to the resource definition.
- remove deletes an existing element from the resource definition.
- copy duplicates an element, overwriting the value in the new path if it already exists.
- move relocates an element, overwriting the value in the new path if it already exists.
- replace replaces an existing element with a new element.

The subject property, as used in the example above, is used to
  transform a subset of resources on restore. Only those resources
  matching the group , version , resource or name will be selected
  from the restore-point. Any empty subject property will match all
  values. The subject above matches all deployment resources with any
  name, for any group or version.

Each command has an operation, op , and a path . op specifies the
  command operation to perform, path references the element within the
  resource to operate on.

copy and move operations contain two paths - from for the source
  element of the operation and path for the destination element of the
  operation.

value contains either an element for comparison or a new element for
  inclusion. Similarly regex can be used for comparing string elements
  or processing elements into new string elements.

### Transform Validation Requirements â

To create a valid transform, it is required to match the following
  requirements:

- Transform's name should not be empty
- Transform should contain the spec
- Transform should contain at least one operation
- Transform should have at least one resource specified

### Paths â

Every command has at least one path that references element(s) to
  operate on. path and from are the only command properties that
  contain paths. Paths consist of keys delineated by slashes ( / ). Keys
  can be object property names or array indexes. For example, "/spec/template/spec/containers/0" references the first container, nginx , within the Deployment resource in the example below .
  Note that every path should be absolute, starting with / .

When adding an element to an array, "-" can be used in the path to
  add an element at the and of the array.

Per RFC-6901 , paths may contain
  character escapes that allow inclusion of / characters within path
  keys. For example "/metadata/annotations/k10~1injectGenericVolumeBackupSidecar" will
  reference the k10/injectGenericVolumeBackupSidecar key on the annotations object within the resource metadata. ~ characters
  may be included by using ~0 .

### Regex and Value â

The function of value and regex properties depend on the operation
  performed:

- test with value compares the element at path to value for an exact match.
- test with regex compares the string element at path to the regular expression in regex
- copy and move that include a regex property operate only on from string elements that match the regular expression in regex .
- copy and move that include a regex and a value property operate only on from string elements that match regex and replace destination path elements with expanded value strings. Capturing groups in value are replaced to produce new values from regex expressions.
- replace that include a regex property operate only on path string elements that match the regular expression in regex .
- replace that include a regex and a value property operate only on path string elements that match regex and replace destination elements with expanded value strings. Capturing groups in value are replaced to produce new values from regex expressions.

value and regex do not apply to the remove and add operations. A test operation with both value and regex properties will produce
  and error.

See re2 for the syntax
  accepted by regex .

Capturing groups are referenced in value with identifiers starting
  with a dollar-sign, ["$"], followed by the index of the
  capturing group.

api-transform-example mountPath from the first volumeMounts entry to the second using regex and value with
  capturing group replacement. The example uses the Deployment resource below . The parent path, /etc/nginx from mountPath is preserved
  and copied into the second volumeMounts as /etc/nginx/config .

```
op: copyfrom: "spec/template/spec/containers/0/volumeMounts/0/mountPath"path: "spec/template/spec/containers/0/volumeMounts/1/mountPath"regex: "([a-z/]+)/ssl"value: "$1/config"
```

### Path Wildcards â

Path wildcards allow path or from to apply to sets of elements. A
  wildcard can be used in place of a path key to refer to all keys of an
  object or array. Valid wildcards are * and ** - * references all
  keys within one element, ** references all keys across multiple
  consecutive elements.

Using the deployment example below ,
  all spec app labels can be accessed with "spec/**/app" , expanding to
  two concrete paths:

```
[  "/spec/selector/matchLabels/app"  "/spec/template/metadata/labels/app"]
```

In the example below , all metadata labels can be accessed with the path "**/metadata/labels/*" expanding to the four concrete paths below:

```
[  "/metadata/labels/app"  "/metadata/labels/version"  "/metadata/labels/release"  "/spec/template/metadata/labels/app"]
```

Reference groups can be used in the path property of the copy and move operations to form new groups of destination paths. Reference
  groups allow for constructing new destination paths from source paths
  with wildcards. Reference groups have keys that start with
  [$] followed by a numeric index of the wildcard. The index
  refers the wildcard ordinal, counting from one. During processing, the
  reference group will be replaced with concrete values of the indexed
  wildcard.

The following copy command example copies all selector matchLabels to
  the spec template metadata.

```
op: copyfrom: "/**/selector/matchLabels/*"path: "/spec/template/metadata/labels/$2"
```

## Transform Commands â

All of the available command forms are listed below. Examples apply to
  the Deployment resource below.

```
apiVersion: apps/v1kind: Deploymentmetadata:  name: nginx-deployment  labels:    app: nginx    version: 1.7.9    release: canaryspec:  replicas: 3  selector:    matchLabels:      app: nginx  template:    metadata:      labels:        app: nginx    spec:      containers:      - name: nginx        image: containers.example.com/nginx:1.7.9        ports:        - containerPort: 443        - containerPort: 80        volumeMounts:        - mountPath: /etc/nginx/ssl          name: secret-volume        - mountPath: /etc/nginx/conf.d          name: configmap-volume
```

### Test â

```
op: testpath: "/metadata/name"
```

Test that element at path exists. path may contain wildcards. If a
  test fails, the remainder of the current transform document will be
  skipped and processing of the next transform document will begin.

```
op: testpath: "/metadata/labels"value: { app: nginx, release: "canary" }
```

Test that element at path equals element in value . Order of map keys
  is not significant. Otherwise, set of map keys and values must match
  exactly. Arrays must be the same size and elements are compared in
  order. If path contains wildcards, all elements referenced by path must equal value . If a test fails, the remaining commands in the
  current transform document will be skipped and processing of the next
  transform document will begin.

```
op: testpath: "/metadata/name"regex: "nginx.*"
```

Test that string element at path exists and matches regular expression
  in regex . path may contain wildcards. If a test fails, the remaining
  commands in the current transform document will be skipped and
  processing of the next transform document will begin.

### Add â

```
op: addpath: "/metadata/label/release"value: canary
```

Add value at path . If path references a map, the key will be added
  or replaced. If path references an array, a new value will be
  inserted. value must be a value JSON/YAML element. path may contain
  wildcards.

The transform will fail if the path does not exist. The last key of
  the path may contain a new map key or an array index.

### Remove â

```
op: removepath: "/metadata/label/release"
```

Remove element at path . path may contain wildcards.

The transform will fail if path does not exist.

### Copy â

```
op: copyfrom: "/metadata/label"path: "/spec/selector/matchLabel"
```

Copy element at from to path . If path references a map, element
  will be added/replaced as in add above. If path references an array,
  copy will insert element as in add above. If from contains
  wildcards, path may contain wildcard variables. If from is a
  concrete path, path may contain wildcards.

The transform will fail if from or path does not exist. The last key
  of path may contain a new map key or an array index.

```
op: copyfrom: "metadata/labels/app"path: "metadata/labels/release"regex: "(.*)"value: "prod-$1"
```

Copy string element at from to path . If path references a map,
  node will be added/replaced as in add above. If path references is
  array, copy will insert element as in add above. If from element
  matches regular expression in regex , perform copy of element with
  replacement of capturing groups in value . If from contains
  wildcards, path may contain wildcard variables. If from is a
  concrete path, path may contain wildcards.

The transform will fail if from element does not exist or is not a
  string. The transform will fail if path does not exist. The last key
  of path may contain a new map key or an array index.

### Move â

```
op: movefrom: "/spec/template/spec/containers/1/port"path: "/spec/template/spec/containers/0/port"
```

Move element at from to path . If path references a map, element
  will be added/replaced as in add above. If path references an array,
  copy will insert element as in add above.

```
op: movefrom: "/metadata/labels/version"path: "/spec/template/metadata/labels/version"regex: "(.*)"value: "v$1"
```

Move string element at from to path . If path references a map,
  element will be added/replaced as in add above. If path references
  an array, copy will insert element as in add above. If regular
  expression in regex matches element at from , perform replacement of
  capturing groups in value . If from contains wildcards, path may
  contain wildcard variables. If from is a concrete path, path may
  contain wildcards.

The transform will fail if from element does not exist or is not a
  string. Transform will fail if path does not exist. The last key of path may contain a new map key or an array index.

### Replace â

```
op: replacepath: "/spec/replicas"value: 5
```

Replace element at path with the element in value . path must
  reference an existing element. path may contain wildcards.

The transform will fail if path element does not exist.

```
op: replacepath: "/spec/template/spec/template/containers/0/image"regex: ".*[/]([a-z/]+):([0-9.]+)"value: "$2/$1"
```

Replace element at path with string element in value . If path references a map, node will be added/replaced as in add above. If path references is array, the element referenced will be replaced. If
  element at path matches regular expression in regex , replace element
  at path with value. Any capturing groups in value will be expanded value . path may contain wildcard variables.

The transform will fail if path element does not exist or is not a
  string.

## Transform Example â

Transform to change the storage class on a persistent volume claim
  ( pvc ):

```
transforms:- subject:    resource: persistentvolumeclaims  name: replaceStorageClassName  json:  - op: replace    path: /spec/storageClassName    regex: ^ssd$    value: gp2
```

Resource to operate on:

```
apiVersion: v1kind: PersistentVolumeClaimmetadata:  name: pic-gallery  namespace: gallery-appspec:  accessModes:  - ReadWriteOnce  resources:    requests:      storage: 2Gi  storageClassName: ssd  volumeMode: Filesystem
```

Transformed resource:

```
apiVersion: v1kind: PersistentVolumeClaimmetadata:  name: pic-gallery  namespace: gallery-appspec:  accessModes:  - ReadWriteOnce  resources:    requests:      storage: 2Gi  storageClassName: gp2  volumeMode: Filesystem
```

---

## Api Transformsets

A TransformSet custom resource (CR) is used to save and reuse the set
  of Transforms to be used
  in Restore Actions , Restore Cluster Actions and Policies .

## Example TransformSet Operations â

- Create a TransformSet
- [Update a TransformSet]./transformsets.md(#update-a-transformset)
- Using a TransformSet
- Delete a TransformSet

### Create a TransformSet â

The following example illustrates how to create a transform set that
  contains two transforms, one of which changes the deadline parameter
  value to 300 seconds and another one scales deployments to 3 replicas.

```
$ cat > sample-transform-set.yaml <<EOFapiVersion: config.kio.kasten.io/v1alpha1kind: TransformSetmetadata:  name: sample-transformset  namespace: kasten-iospec:  comment: "Transform Set Example"  transforms:    - subject:        resource: deployments      name: progressDeadlineSeconds5m      json:        - op: replace          path: /spec/progressDeadlineSeconds          value: 300    - subject:        resource: deployments      name: scaleDeployment3      json:        - op: replace          path: /spec/replicas          value: 3EOF$ kubectl apply -f sample-transform-set.yamltransformset.config.kio.kasten.io/sample-transformset created## make sure it initializes and validates properly$ kubectl get transformsets.config.kio.kasten.io --namespace kasten-io -wNAME                  STATUS    AGEsample-transformset   Success   30s
```

### Update a TransformSet â

To update a TransformSet , edit the [spec] portion of a TransformSet CR using your preferred method of submitting resource
  changes with [kubectl].

```
$ kubectl apply -f sample-transform-set-updated.yamltransformset.config.kio.kasten.io/sample-transformset configured
```

Once the change is submitted, Veeam Kasten will re-validate the TransformSet and update [.status.validation] accordingly.

```
$ kubectl get transformsets.config.kio.kasten.io --namespace kasten-io -wNAME                  STATUS    AGEsample-transformset   Failed    25msample-transformset   Success   30m
```

Since Veeam Kasten processes API object changes asynchronously, to avoid
  confusion with a previous TransformSet status, it is recommended as
  convention that the [status] portion of the TransformSet is omitted when submitting changes.

A transform set is invalid if it has no transforms or if one of the
    transforms it contains is invalid.

### Using a TransformSet â

The following example illustrates how to use a TransformSet in a RestoreAction .

```
$ cat > restore-action-with-transform-set.yaml <<EOFapiVersion: actions.kio.kasten.io/v1alpha1kind: RestoreActionmetadata:  generateName: restore-nginx-  namespace: nginxspec:  subject:    kind: RestorePoint    name: backup-nginx-sdxg2    namespace: nginx  targetNamespace: nginx  transforms:    - json: []      transformSetRef:        name: sample-transformset        namespace: kasten-ioEOF$ kubectl create -f restore-action-with-transform-set.yamlrestoreaction.actions.kio.kasten.io/restore-nginx-l69nd created
```

The TransformSet will be applied to the restored application.

### Delete a TransformSet â

A TransformSet can be deleted using the following command.

```
## delete transformset "sample-transformset" for Veeam Kasten installed in "kasten-io"$ kubectl delete transformsets.config.kio.kasten.io sample-transformset --namespace kasten-iotransformset.config.kio.kasten.io "sample-transformset" deleted
```

## TransformSet API Type â

The following is a complete specification of a TransformSet CR.

To learn more about the transforms structure, see Transforms .

```
## Standard Kubernetes API Version declaration. Required.apiVersion: config.kio.kasten.io/v1alpha1## Standard Kubernetes Kind declaration. Required.kind: TransformSet## Standard Kubernetes metadata. Required.metadata:  ## TransformSet name. May be any valid Kubernetes object name. Required.  ## TransformSet name is not mutable once created.  name: sample-transformset  ## TransformSet namespace. Required.  namespace: kasten-io## TransformSet parameters. Required.spec:  ## User friendly comment describing the transform set. Optional.  comment:  ## The list of transforms. Required.  transforms:    ## Specifies which resource artifacts to apply this transform to. Required.    ## At least one filter should be set.    - subject:        ## Resource group. Optional.        group: apps        ## Resource version. Optional.        version: v1        ## Resource type. Optional.        resource: deployments        ## Resource name. Optional.        name: my-app      ## The name of the transform. Required.      name: 'copyRelease'      ## An array of RFC-6902 JSON patch-like operations. Required.      json:        ## Operation name. Required.        ## Transforms support six command operations:        ##   ## 'test' - checks that an element exists (and equals the value / matches the regexp if specified)        ##   ## 'add' - inserts a new element to the resource definition        ##   ## 'remove' - deletes an existing element from the resource definition        ##   ## 'copy' - duplicates an element, overwriting the value in the new path if it already exists        ##   ## 'move' - relocates an element, overwriting the value in the new path if it already exists        ##   ## 'replace' - replaces an existing element with a new element        - op: copy          ## Source reference for operation. Optional.          ## Required and valid only for 'move' and 'copy' operations.          from: '/metadata/labels/release'          ## Target reference for operation. Required for every operation.          path: '/spec/template/metadata/labels/release'          ## Regex to match expression. Optional.          ## When used with 'copy', 'move' or 'replace' operation,          ## the transform will match the target text against the `regex`          ## and substitute regex capturing groups with `value`.          ## When used with 'test' operation,          ## the transform will match the target text against the `regex`.          regex: 'prod-v.*'          ## Value is any valid JSON. Optional.          ## Required for 'add' and 'replace' operations.          ## Required for 'copy' and 'move' operations only when used along with `regex`.          ## 'test' operation can use either `regex` or `value`.          value: 'prod'## Status of the TransformSet. Users should not set any data here.status:  ## Object generation last observed by the controller  observedGeneration: 2  ## Validation status of the TransformSet  ## Valid values are:  ##   ## Success â successfully initialized and validated  ##   ## Failed - not properly initialized or validated  ##   ## Indeterminate â indicate an indeterminate validation status for multi-cluster TransformSets.  validation: Success  ## An array of any validation or initialization errors encountered.  error: null
```

---

