# Kanister Documentation

## Kanister Kanister

Kanister, an extensible open-source framework used by Kasten's Veeam
  Kasten platform, can be used for application-level data management on
  Kubernetes. It allows domain experts to capture application specific
  data management tasks in blueprints which can be easily shared and
  extended. The framework takes care of the tedious details around
  execution on Kubernetes and presents a homogeneous operational
  experience across applications at scale. Further, it gives you a natural
  mechanism to extend the Veeam Kasten platform by adding your own code to
  modify any desired step performed for data lifecycle management.

Below you can find useful resources about the project as well as helpful
  information for testing Veeam Kasten with Kanister-enabled applications.

---

## Kanister Kanister

Kanister, an extensible open-source framework used by Kasten's Veeam
  Kasten platform, can be used for application-level data management on
  Kubernetes. It allows domain experts to capture application specific
  data management tasks in blueprints which can be easily shared and
  extended. The framework takes care of the tedious details around
  execution on Kubernetes and presents a homogeneous operational
  experience across applications at scale. Further, it gives you a natural
  mechanism to extend the Veeam Kasten platform by adding your own code to
  modify any desired step performed for data lifecycle management.

Below you can find useful resources about the project as well as helpful
  information for testing Veeam Kasten with Kanister-enabled applications.

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
apiVersion: v1data:  override: |    kind: Pod    spec:      nodeSelector:        disktype: ssd      tolerations:        - effect: NoSchedule          key: app          operator: Equal          value: mysql      serviceAccountName: abcd      containers:        - name: container          volumeMounts:            - mountPath: /etc/ssl/certs/<custom-bundle-file>.pem              name: custom-ca-bundle-store              subPath: <custom-bundle-file>.pem      volumes:        - configMap:            defaultMode: 420            name: custom-ca-bundle-store          name: custom-ca-bundle-storekind: ConfigMapmetadata:  name: pod-spec-override  namespace: kasten-io
```

Replace <custom-bundle-file> with the desired filename

This ConfigMap now would be merged with all Kanister job Pod
  specifications. The Kanister restore job Pods would look like:

```
apiVersion: v1kind: Podmetadata:  name: restore-data-*  namespace: mysqlspec:  containers:    - name: container      imagePullPolicy: IfNotPresent      volumeMounts:        - mountPath: /etc/ssl/certs/<custom-bundle-file>.pem          name: custom-ca-bundle-store          subPath: <custom-bundle-file>.pem  nodeSelector:    disktype: ssd  serviceAccount: abcd  serviceAccountName: abcd  tolerations:    - effect: NoSchedule      key: app      operator: Equal      value: mysql  volumes:    - configMap:        defaultMode: 420        name: custom-ca-bundle-store      name: custom-ca-bundle-store
```

---

