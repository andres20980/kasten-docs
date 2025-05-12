# Kanister Documentation

## Kanister Hooks

Kanister Blueprints can be used to execute arbitrary functionality
  before or after Veeam Kasten Actions.

To use a Blueprint to define an execution hook, create the Blueprint in
  the Veeam Kasten namespace and add a reference to one of the
  Blueprint's actions in a Policy or Action.

1. For snapshot/export actions, these execution hooks operate on namespaces and can be set independently. The namespace is the source namespace where the application being snapshotted/exported is deployed. A hook blueprint can use this namespace via template parameters like {{ .Namespace.Name }}
2. For restore actions, the execution hooks can operate on other Kubernetes resources as well. The resource on which the hook would operate can be selected on the dashboard as shown in the image below. For example, if a StatefulSet is selected as the target resource, a hook blueprint can access it via template parameters like {{ .StatefulSet.Name }} . Only the resources created in the target namespace can be selected as a subject. If no target resource is selected, namespace would be the target resource.

For snapshot/export actions, these execution hooks operate on
      namespaces and can be set independently. The namespace is the source
      namespace where the application being snapshotted/exported is
      deployed. A hook blueprint can use this namespace via template
      parameters like {{ .Namespace.Name }}

For restore actions, the execution hooks can operate on other
      Kubernetes resources as well. The resource on which the hook would
      operate can be selected on the dashboard as shown in the image
      below. For example, if a StatefulSet is selected as the target
      resource, a hook blueprint can access it via template parameters
      like {{ .StatefulSet.Name }} . Only the resources created in the
      target namespace can be selected as a subject. If no target resource
      is selected, namespace would be the target resource.

Policies that apply to multiple namespaces will invoke hooks on each
  namespace.

Execution hooks do not require location profiles and hook Blueprint
  actions cannot use template parameters and helpers such as {{ .Profile.Location.Bucket }} or kando location .

For example, the following Blueprint defines a hook which updates a
  label on the namespace that was snapshotted.

```
apiVersion: cr.kanister.io/v1alpha1kind: Blueprintmetadata:  name: hook-blueprint  namespace: kasten-ioactions:  post-export:    kind: Namespace    phases:    - func: KubeTask      name: hookPhase      args:        podOverride:          serviceAccountName: "k10-k10"        image: bitnami/kubectl        command:        - /bin/sh        - -c        - |          kubectl patch namespace "{{ .Namespace.Name }}" --type json -p='[{"op": "remove", "path": "/metadata/labels/migrate"}]'
```

The following Blueprint defines a hook which checks if a particular pod
  is ready after restore.

```
apiVersion: cr.kanister.io/v1alpha1kind: Blueprintmetadata:  name: hook-blueprint  namespace: kasten-ioactions:  post-restore:    phases:    - func: Wait      name: WaitForPod      args:        timeout: 120s        conditions:         anyOf:         - condition: '{{ if { $.status.containerStatuses[].ready } }}true{{ else }}false{{ end }}'           objectReference:            apiVersion: v1            resource: pods            name: '{{ .StatefulSet.Name }}'            namespace: '{{ .StatefulSet.Namespace }}'
```

A hook reference may include preHook , onSuccess , or onFailure :

- A preHook action is executed before the Veeam Kasten Action (after any Veeam Kasten setup steps have succeeded).
- An onSuccess action is executed after the Veeam Kasten Action has succeeded.
- An onFailure action is executed when there is a failure in an earlier step and Veeam Kasten has reached its retry limit.

Once successful, hook actions are not retried. If a preHook or onSuccess action fails, it may be retried by Veeam Kasten. If an onFailure action fails, Veeam Kasten will not retry. Execution hooks
  may or may not be invoked when a Veeam Kasten Action is cancelled
  asynchronously.

Kanister artifacts returned as outputArtifacts by the hook Blueprint
  action for preHook are passed as inputArtifacts to any hook
  Blueprint action for onSuccess or onFailure .

For example, the following hook reference specifies an execution hook
  for before a Restore Action and the error and non-error cases:

```
...hooks:  preHook:    blueprint: hook-blueprint    actionName: pre-restore  onSuccess:    blueprint: hook-blueprint    actionName: post-restore    subject:       name: mysql-statefulset       namespace: mysql       type: statefulset  onFailure:    blueprint: hook-blueprint    actionName: post-restore-failed...
```

Look here to see how to
  embed hook references in API objects.

Note, using VBR as a profile for blueprint based backups is currently
  unsupported.

## Configuring Security Context for Kanister Execution Hooks â

By default, Pods provisioned as part of a Kanister Execution Hook action
  run with root privileges. If certain conditions are met, it is possible
  to change this behavior (e.g., to configure Kanister Hooks in a rootless
  manner).

The Kanister Pod Override ConfigMap holds the highest priority. If the pod's security
    context is defined in this ConfigMap, it will override any other
    configuration.

Setting the forceRootInBlueprintActions flag to false provides more
  flexibility for configuring the security context for the Kanister
  Execution Hooks but should be done cautiously.

Once the flag is set to false , Veeam Kasten will use the security
  context specified in the Kanister Blueprint's phase. If no security
  context is set for the phase, Veeam Kasten will default to using an
  empty security context.

The security context can be set in the args.podOverride section of any
    phase in the Kanister Blueprint for all functions that deploy temporary
    Pods. See the Kanister
documentation for a complete list of functions that support args.podOverride .

For example, the following section should be added to the phase's args section to make it run as the user 1000 :

```
...podOverride:  serviceAccountName: "k10-k10"  ## Add the securityContext section here to use it in Kanister Hook.  securityContext:    runAsUser: 1000    runAsNonRoot: true...
```

---

## Kanister Kanister

By default, Generic Storage Backup will be disabled for all new
    deployments of Veeam Kasten and for existing deployments when upgraded
    to version 6.5.0 or later. For more details, refer to this page.

The Veeam Kasten data management platform, purpose-built for Kubernetes,
  provides enterprise operations teams an easy-to-use, scalable, and
  secure system for backup/restore, disaster recovery, and mobility of
  Kubernetes applications.

Veeam Kasten's application-centric approach and deep integrations with
  relational and NoSQL databases, Kubernetes distributions, and all clouds
  provide teams with the freedom of infrastructure choice without
  sacrificing operational simplicity. Policy-driven and extensible, Veeam
  Kasten provides a native Kubernetes API and includes features such as
  full-spectrum consistency, database integrations, automatic application
  discovery, multi-cloud mobility, and a powerful web-based user
  interface.

Given Veeam Kasten's extensive ecosystem support you have the
  flexibility to choose environments (public/ private/ hybrid cloud/
  on-prem) and Kubernetes distributions (cloud vendor managed or self
  managed) in support of three principal use cases:

- Backup and Restore
- Disaster Recovery
- Application Mobility

## Veeam Kasten Editions (Free and Enterprise) â

Veeam Kasten is available in two editions. The default Starter edition,
  provided at no charge and intended for evaluation or for use in small
  non-production clusters, is functionally the same as the Enterprise
  edition but limited from a support and scale perspective. Customers
  choosing to upgrade to the Enterprise edition can obtain a license key
  from Kasten or install from cloud marketplaces. Please see the product
page for a comparison of the editions.

---

## Kanister Kanister

By default, Generic Storage Backup will be disabled for all new
    deployments of Veeam Kasten and for existing deployments when upgraded
    to version 6.5.0 or later. For more details, refer to this page.

The Veeam Kasten data management platform, purpose-built for Kubernetes,
  provides enterprise operations teams an easy-to-use, scalable, and
  secure system for backup/restore, disaster recovery, and mobility of
  Kubernetes applications.

Veeam Kasten's application-centric approach and deep integrations with
  relational and NoSQL databases, Kubernetes distributions, and all clouds
  provide teams with the freedom of infrastructure choice without
  sacrificing operational simplicity. Policy-driven and extensible, Veeam
  Kasten provides a native Kubernetes API and includes features such as
  full-spectrum consistency, database integrations, automatic application
  discovery, multi-cloud mobility, and a powerful web-based user
  interface.

Given Veeam Kasten's extensive ecosystem support you have the
  flexibility to choose environments (public/ private/ hybrid cloud/
  on-prem) and Kubernetes distributions (cloud vendor managed or self
  managed) in support of three principal use cases:

- Backup and Restore
- Disaster Recovery
- Application Mobility

## Veeam Kasten Editions (Free and Enterprise) â

Veeam Kasten is available in two editions. The default Starter edition,
  provided at no charge and intended for evaluation or for use in small
  non-production clusters, is functionally the same as the Enterprise
  edition but limited from a support and scale perspective. Customers
  choosing to upgrade to the Enterprise edition can obtain a license key
  from Kasten or install from cloud marketplaces. Please see the product
page for a comparison of the editions.

---

## Kanister Override

In some cases, there can be a requirement to override Kanister jobs pods
  specifications with custom values, such as tolerations for taints , nodeSelector , or serviceAccountName . This can serve a use-case when
  the pods need to be scheduled on a particular node, or use a
  ServiceAccount which provides limited access. Changing these values
  manually for Kanister Job pods will not be feasible.

To handle specifying the custom pod override for all Kanister Pods, a
  ConfigMap named pod-spec-override must be created in the kasten-io namespace. Veeam Kasten will merge the specifications configured in pod-spec-override with other specifications set through Helm (such as
  Root CA) and apply the merged configuration to all Kanister Job Pods.

imagePullSecrets and securityContext should not be set via pod-spec-override . If these configurations are set in this manner,
    Veeam Kasten will ignore them.

When the helm option for providing a Root CA to Veeam Kasten (i.e., cacertconfigmap.name ) is enabled, the Kanister Backup/Restore workflow
    will create a new ConfigMap, in the application namespace to provide the
    Root CA to the sidecar. This ConfigMap in the application namespace
    would be a copy of the Root CA ConfigMap residing in the Veeam Kasten
    namespace, which would be deleted at the end of the workflow. To
    override this, the Root CA ConfigMap can be created in the application
    namespace and the respective Volume and VolumeMounts in the pod-spec-override in kasten-io namespace.

For example, the following ConfigMap defines a Pod Specification, which
  contains tolerations to node taints, and a nodeSelector .

```
apiVersion: v1data:  override: |    kind: Pod    spec:      nodeSelector:        disktype: ssd      tolerations:        - effect: NoSchedule          key: app          operator: Equal          value: mysql      serviceAccountName: abcd      containers:        - name: container          volumeMounts:            - mountPath: /etc/ssl/certs/custom-ca-bundle.pem              name: custom-ca-bundle-store              subPath: custom-ca-bundle.pem      volumes:        - configMap:            defaultMode: 420            name: custom-ca-bundle-store          name: custom-ca-bundle-storekind: ConfigMapmetadata:  name: pod-spec-override  namespace: kasten-io...
```

This ConfigMap now would be merged with all Kanister job Pod
  specifications. The Kanister restore job Pods would look like:

```
apiVersion: v1kind: Podmetadata:  name: restore-data-*  namespace: mysqlspec:  containers:    - name: container      imagePullPolicy: IfNotPresent      volumeMounts:        - mountPath: /etc/ssl/certs/custom-ca-bundle.pem          name: custom-ca-bundle-store          subPath: custom-ca-bundle.pem  nodeSelector:    disktype: ssd  serviceAccount: abcd  serviceAccountName: abcd  tolerations:    - effect: NoSchedule      key: app      operator: Equal      value: mysql  volumes:    - configMap:        defaultMode: 420        name: custom-ca-bundle-store      name: custom-ca-bundle-store...
```

## Configuring custom labels and annotations â

Kanister pods launched during Veeam Kasten operations can be configured
  with additional custom labels and annotations through Helm Values.

Custom labels can be configured through Helm in following ways:

- Providing the path to one or more YAML files during helm install or helm upgrade with the --values flag: kanisterPodCustomLabels : "key1=value1,key2=value2" kanisterPodCustomAnnotations : "key1=value1,key2=value2"
- Modifying the resource values one at a time with the --set flag during helm install or helm upgrade : --set = kanisterPodCustomLabels = "key1=value1,key2=value2" --set = kanisterPodCustomAnnotations = "key1=value1,key2=value2"

Providing the path to one or more YAML files during helm install or helm upgrade with the --values flag:

```
kanisterPodCustomLabels: "key1=value1,key2=value2"kanisterPodCustomAnnotations: "key1=value1,key2=value2"
```

Modifying the resource values one at a time with the --set flag
      during helm install or helm upgrade :

```
--set=kanisterPodCustomLabels="key1=value1,key2=value2"--set=kanisterPodCustomAnnotations="key1=value1,key2=value2"
```

---

