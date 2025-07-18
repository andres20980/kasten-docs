# Install Documentation

## Install

Veeam Kasten is available in two main editions, Veeam Kasten Free and Enterprise. The Kasten product page contains a comparison of the two Veeam Kasten editions, also described below, but both editions use the same container images and follow an identical install process.

- Veeam Kasten Free : The default Veeam Kasten Starter edition, provided at no charge and intended for evaluation or for use in smaller or non-production clusters, is functionally the same as the Enterprise edition but limited from a support and scale perspective.
- Enterprise : Customers choosing to upgrade to the Enterprise edition can obtain a license key from Kasten or install from cloud marketplaces.

Veeam Kasten Free : The default Veeam Kasten Starter edition, provided at no charge and intended for evaluation or for use in smaller or non-production clusters, is functionally the same as the Enterprise edition but limited from a support and scale perspective.

Enterprise : Customers choosing to upgrade to the Enterprise edition can obtain a license key from Kasten or install from cloud marketplaces.

The documentation below covers installing both Veeam Kasten editions on a variety of public cloud and on-premises environments, storage integration, security key management, license upgrades, and other advanced installation options.

---

## Install Advanced

## FREE Veeam Kasten Edition and Licensing â

By default, Veeam Kasten comes with an embedded free edition license.
  The free edition license allows you to use the software on a cluster
  with at most 50 worker nodes in the first 30 days, and then 5 nodes
  after the 30-day period. In order to continue using the free license,
  regular updates to stay within the 6 month support window might be
  required. You can remove the node restriction of the free license by
  updating to Enterprise Edition and obtaining the appropriate license
  from the Kasten team.

### Using a Custom License During Install â

To install a license that removes the node restriction, please add the
  following to any of the helm install commands:

```
--set license=<license-text>
```

or, to install a license from a file:

```
--set-file license=<path-to-license-file>
```

Veeam Kasten dynamically retrieves the license key and a pod restart
    is not required.

### Changing Licenses â

To add a new license to Veeam Kasten, a secret needs to be created in
  the Veeam Kasten namespace (default is kasten-io ) with the requirement
  that the license text be set in a field named license . To do this from
  the command line, run:

```
$ kubectl create secret generic <license-secret-name> \    --namespace kasten-io \    --from-literal=license="<license-text>"
```

or, to add a license from a file:

```
$ kubectl create secret generic <license-secret-name> \    --namespace kasten-io \    --from-file=license="<path-to-license-file>"
```

Multiple license secrets can exist simultaneously and Veeam Kasten
    will check if any are valid. This license check is done periodically and
    so, no Veeam Kasten restarts are required if a different existing
    license becomes required (e.g., due to a cluster expansion or an old
    license expiry) or when a new license is added.

The resulting license will look like:

```
apiVersion: v1data:  license: Y3Vz...kind: Secretmetadata:  creationTimestamp: "2020-04-14T23:50:05Z"  labels:    app: k10    app.kubernetes.io/instance: k10    app.kubernetes.io/managed-by: Helm    app.kubernetes.io/name: k10    helm.sh/chart: k10-8.0.4    heritage: Helm    release: k10  name: k10-custom-license  namespace: kasten-iotype: Opaque
```

Similarly, old licenses can be removed by deleting the secret that
  contains it.

```
$ kubectl delete secret <license-secret-name> \    --namespace kasten-io
```

### Add Licenses via Dashboard â

It is possible to add a license via the Licenses page of the Settings menu in the navigation sidebar. The license can be pasted
  directly into the text field or loaded from a .lic file.

### License Grace period â

If the license status of the cluster becomes invalid (e.g., the licensed
  node limit is exceeded), the ability to perform manual actions or
  creating new policies will be disabled but your previously scheduled
  policies will continue to run for 50 days. The displayed warning will be
  look like:

By default, Veeam Kasten provides a grace period of 50 days to ensure
  that applications remain protected while a new license is obtained or
  the cluster is brought back into compliance by reducing the number of
  nodes. Veeam Kasten will stop the creation of any new jobs (scheduled or
  manual) after the grace period expires.

If the cluster's license status frequently swaps between valid and
  invalid states, the amount of time the cluster license spends in an
  invalid status will be subtracted from subsequent grace periods.

You can see node usage from the last two months via the Licenses page
  of the Settings menu in the navigation sidebar. Usage starts being
  tracked from the installation date of 4.5.8+. From 5.0.11+ you can see
  the same information through Prometheus .

## Manually Creating or Using an Existing Service Account â

```
For more information regarding ServiceAccount restrictions with Kasten,please refer to this [documentation](../restrictions.md#cluster-admin-restrictions).
```

The following instructions can be used to create a new Service Account
  that grants Veeam Kasten the required permissions to Kubernetes
  resources and the use the given Service Account as a part of the install
  process. The instructions assume that you will be installing Veeam
  Kasten in the kasten-io namespace.

```
# Create kasten-io namespace if have not done it yet.$ kubectl create namespace kasten-io# Create a ServiceAccount for k10 k10-sa$ kubectl --namespace kasten-io create sa k10-sa# Create a cluster role binding for k10-sa$ kubectl create clusterrolebinding k10-sa-rb \    --clusterrole cluster-admin \    --serviceaccount=kasten-io:k10-sa
```

Following the SA creation, you can install Veeam Kasten using:

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set rbac.create=false \    --set serviceAccount.create=false \    --set serviceAccount.name=k10-sa
```

## Pinning Veeam Kasten to Specific Nodes â

While not generally recommended, there might be situations (e.g., test
  environments, nodes reserved for infrastructure tools, or clusters
  without autoscaling enabled) where Veeam Kasten might need to be pinned
  to a subset of nodes in your cluster. You can do this easily with an
  existing deployment by using a combination of NodeSelectors and Taints and
Tolerations .

The process to modify a deployment to accomplish this is demonstrated in
  the following example. The example assumes that the nodes you want to
  restrict Veeam Kasten to have the label selector-key: selector-value and a taint set to taint-key=taint-value:NoSchedule .

```
$ cat << EOF > patch.yamlspec:  template:    spec:      nodeSelector:        selector-key: selector-value      tolerations:      - key: "taint-key"        operator: "Equal"        value: "taint-value"        effect: "NoSchedule"EOF$ kubectl get deployment --namespace kasten-io | awk 'FNR == 1 {next} {print $1}' \  | xargs -I DEP kubectl patch deployments DEP --namespace kasten-io --patch "$(cat patch.yaml)"
```

## Using Trusted Root Certificate Authority Certificates for TLS â

For temporary testing of object storage systems that are deployed using
    self-signed certificates signed by a trusted Root CA, it is also
    possible to disable certificate verification if the Root CA certificate is not easily available.

If the S3-compatible object store configured in a Location Profile was
  deployed with a self-signed certificate that was signed by a trusted
  Root Certificate Authority (Root CA), then the certificate for such a
  certificate authority has to be provided to Veeam Kasten to enable
  successful verification of TLS connections to the object store.

Similarly, to authenticate with a private OIDC provider whose
  self-signed certificate was signed by a trusted Root CA, the certificate
  for the Root CA has to be provided to Veeam Kasten to enable successful
  verification of TLS connections to the OIDC provider.

Multiple Root CAs can be bundled together in the same file.

### Install Root CA in Veeam Kasten's namespace â

Assuming Veeam Kasten will be deployed in the kasten-io namespace, the
  following instructions will make a private Root CA certificate available
  to Veeam kasten.

```
$ kubectl --namespace kasten-io create configmap <configmap-name> --from-file=<custom-bundle-file>.pem
```

Replace <custom-bundle-file> with the desired filename

To provide the Root CA certificate to Veeam Kasten, add the following to
  the Helm install command.

```
--set cacertconfigmap.name=<configmap-name>--set cacertconfigmap.key=<configmap-key>
```

Replace <configmap-key> with the desired key

Use of cacertconfigmap.key is optional. If it is unspecified,
    the ConfigMap referenced by cacertconfigmap.name must use
    the expected default key name, custom-ca-bundle.pem .

### Install Root CA in Application's Namespace When Using Kanister Sidecar â

If you either use Veeam Kasten's Kanister sidecar injection feature for
  injecting the Kanister sidecar in your application's namespace or if
  you have manually added the Kanister sidecar, you must create a
  ConfigMap containing the Root CA in the application's namespace and
  update the application's specification so that the ConfigMap is mounted
  as a Volume. This will enable the Kanister sidecar to verify TLS
  connections successfully using the Root CA in the ConfigMap.

Assuming that the application's namespace is named test-app , use the
  following command to create a ConfigMap containing the Root CA in the
  application's namespace:

```
$ kubectl --namespace test-app create configmap <configmap-name> --from-file= <custom-bundle-file>.pem
```

Replace <configmap-name> with any desired ConfigMap name and <custom-bundle-file> with the desired filename

This is an example of a VolumeMount that must be added to the
  application's specification.

```
- name: custom-ca-bundle-store  mountPath: "/etc/ssl/certs/<custom-bundle-file>.pem"  subPath:<custom-bundle-file>.pem
```

This is an example of a Volume that must be added to the application's
  specification.

```
- name: custom-ca-bundle-store  configMap:    name: custom-ca-bundle-store
```

### Troubleshooting â

If Veeam Kasten is deployed without the cacertconfigmap.name setting,
  validation failures such as the one shown below will be seen while
  configuring a Location Profile using the web based user interface.

In the absence of the cacertconfigmap.name setting, authentication
  with a private OIDC provider will fail. Veeam Kasten's logs will show
  an error x509: certificate signed by unknown authority .

If you do not install the Root CA in the application namespace when
  using a Kanister sidecar with the application, the logs will show an
  error x509: certificate signed by unknown authority when the sidecar
  tries to connect to any endpoint that requires TLS verification.

## Running Veeam Kasten Containers as a Specific User â

Veeam Kasten service containers run with UID and fsGroup 1000 by
  default. If the storage class Veeam Kasten is configured to use for its
  own services requires the containers to run as a specific user, then the
  user can be modified.

This is often needed when using shared storage, such as NFS/SMB, where
  permissions on the target storage require a specific user.

To run as a specific user (e.g., root (0), add the following to the Helm
  install command:

```
--set services.securityContext.runAsUser=0 \--set services.securityContext.fsGroup=0 \--set prometheus.server.securityContext.runAsUser=0 \--set prometheus.server.securityContext.runAsGroup=0 \--set prometheus.server.securityContext.runAsNonRoot=false \--set prometheus.server.securityContext.fsGroup=0
```

Other SecurityContext settings for the Veeam Kasten service containers can be specified using
  the --set service.securityContext.<setting name> and --set prometheus.server.securityContext.<setting name> options.

## Configuring Prometheus â

Prometheus is an open-source system monitoring
  and alerting toolkit bundled with Veeam Kasten.

When passing value from the command line, the value key has to be
  prefixed with the prometheus. string:

```
--set prometheus.server.persistentVolume.storageClass=default.sc
```

When passing values in a YAML file, all prometheus settings should be
  under the prometheus key:

```
# values.yaml# global values - apply to both Veeam Kasten and prometheusglobal:  persistence:    storageClass: default-sc# Veeam Kasten specific settingsauth:  basicAuth: enabled# prometheus specific settingsprometheus:  server:    persistentVolume:      storageClass: another-sc
```

To modify the bundled Prometheus configuration, only use the helm values
    listed in the Complete List of Veeam Kasten Helm Options . Any undocumented configurations may affect the
    functionality of the Veeam Kasten. Additionally, Veeam Kasten does not
    support disabling Prometheus service, which may lead to
    unsupported scenarios, potential monitoring and logging issues, and
    overall functionality disruptions. It is recommended to keep these
    services enabled to ensure proper functionality and prevent unexpected
    behavior.

## Complete List of Veeam Kasten Helm Options â

| Parameter | Description | Default | eula.accept | Whether to enable accept EULA before installation | false |
| :---: | :---: | :---: | :---: | :---: | :---: |
| eula.accept | Whether to enable accept EULA before installation | false |
| eula.company | Company name. Required field if EULA is accepted | None |
| eula.email | Contact email. Required field if EULA is accepted | None |
| license | License string obtained from Kasten | None |
| rbac.create | Whether to enable RBAC with a specific cluster role and binding for K10 | true |
| scc.create | Toggle creation of SecurityContextConstraints for Kasten ServiceAccount(s) | false |
| scc.priority | Sets the SecurityContextConstraints priority | 15 |
| scc.allowCSI | Toggles allowing CSI ephemeral volumes in SecurityContextConstraints | false |
| networkPolicy.create | Toggle creation of built-in NetworkPolicies | true |
| services.dashboardbff.hostNetwork | Whether the dashboardbff Pods may use the node network | false |
| services.executor.hostNetwork | Whether the executor Pods may use the node network | false |
| services.aggregatedapis.hostNetwork | Whether the aggregatedapis Pods may use the node network | false |
| serviceAccount.create | Specifies whether a ServiceAccount should be created | true |
| serviceAccount.name | The name of the ServiceAccount to use. If not set, a name is derived using the release and chart names. | None |
| ingress.create | Specifies whether the K10 dashboard should be exposed via ingress | false |
| ingress.name | Optional name of the Ingress object for the K10 dashboard. If not set, the name is formed using the release name. | {Release.Name}-ingress |
| ingress.class | Cluster ingress controller class:nginx,GCE | None |
| ingress.host | FQDN (e.g.,k10.example.com) for name-based virtual host | None |
| ingress.urlPath | URL path for K10 Dashboard (e.g.,/k10) | Release.Name |
| ingress.pathType | Specifies the path type for the ingress resource | ImplementationSpecific |
| ingress.annotations | Additional Ingress object annotations | {} |
| ingress.tls.enabled | Configures a TLS use foringress.host | false |
| ingress.tls.secretName | Optional TLS secret name | None |
| ingress.defaultBackend.service.enabled | Configures the default backend backed by a service for the K10 dashboard Ingress (mutually exclusive setting withingress.defaultBackend.resource.enabled). | false |
| ingress.defaultBackend.service.name | The name of a service referenced by the default backend (required if the service-backed default backend is used). | None |
| ingress.defaultBackend.service.port.name | The port name of a service referenced by the default backend (mutually exclusive setting with portnumber, required if the service-backed default backend is used). | None |
| ingress.defaultBackend.service.port.number | The port number of a service referenced by the default backend (mutually exclusive setting with portname, required if the service-backed default backend is used). | None |
| ingress.defaultBackend.resource.enabled | Configures the default backend backed by a resource for the K10 dashboard Ingress (mutually exclusive setting withingress.defaultBackend.service.enabled). | false |
| ingress.defaultBackend.resource.apiGroup | Optional API group of a resource backing the default backend. | '' |
| ingress.defaultBackend.resource.kind | The type of a resource being referenced by the default backend (required if the resource default backend is used). | None |
| ingress.defaultBackend.resource.name | The name of a resource being referenced by the default backend (required if the resource default backend is used). | None |
| global.persistence.size | Default global size of volumes for K10 persistent services | 20Gi |
| global.persistence.catalog.size | Size of a volume for catalog service | global.persistence.size |
| global.persistence.jobs.size | Size of a volume for jobs service | global.persistence.size |
| global.persistence.logging.size | Size of a volume for logging service | global.persistence.size |
| global.persistence.metering.size | Size of a volume for metering service | global.persistence.size |
| global.persistence.storageClass | Specified StorageClassName will be used for PVCs | None |
| global.podLabels | Configures custom labels to be set to all Kasten Pods | None |
| global.podAnnotations | Configures custom annotations to be set to all Kasten Pods | None |
| global.airgapped.repository | Specify the helm repository for offline (airgapped) installation | '' |
| global.imagePullSecret | Provide secret which contains docker config for private repository. Usek10-ecrwhen secrets.dockerConfigPath is used. | '' |
| global.prometheus.external.host | Provide external prometheus host name | '' |
| global.prometheus.external.port | Provide external prometheus port number | '' |
| global.prometheus.external.baseURL | Provide Base URL of external prometheus | '' |
| global.network.enable_ipv6 | EnableIPv6support for K10 | false |
| google.workloadIdentityFederation.enabled | Enable Google Workload Identity Federation for K10 | false |
| google.workloadIdentityFederation.idp.type | Identity Provider type for Google Workload Identity Federation for K10 | '' |
| google.workloadIdentityFederation.idp.aud | Audience for whom the ID Token from Identity Provider is intended | '' |
| secrets.awsAccessKeyId | AWS access key ID (required for AWS deployment) | None |
| secrets.awsSecretAccessKey | AWS access key secret | None |
| secrets.awsIamRole | ARN of the AWS IAM role assumed by K10 to perform any AWS operation. | None |
| secrets.awsClientSecretName | The secret that contains AWS access key ID, AWS access key secret and AWS IAM role for AWS | None |
| secrets.googleApiKey | Non-default base64 encoded GCP Service Account key | None |
| secrets.googleProjectId | Sets Google Project ID other than the one used in the GCP Service Account | None |
| secrets.azureTenantId | Azure tenant ID (required for Azure deployment) | None |
| secrets.azureClientId | Azure Service App ID | None |
| secrets.azureClientSecret | Azure Service APP secret | None |
| secrets.azureClientSecretName | The secret that contains ClientID, ClientSecret and TenantID for Azure | None |
| secrets.azureResourceGroup | Resource Group name that was created for the Kubernetes cluster | None |
| secrets.azureSubscriptionID | Subscription ID in your Azure tenant | None |
| secrets.azureResourceMgrEndpoint | Resource management endpoint for the Azure Stack instance | None |
| secrets.azureADEndpoint | Azure Active Directory login endpoint | None |
| secrets.azureADResourceID | Azure Active Directory resource ID to obtain AD tokens | None |
| secrets.microsoftEntraIDEndpoint | Microsoft Entra ID login endpoint | None |
| secrets.microsoftEntraIDResourceID | Microsoft Entra ID resource ID to obtain AD tokens | None |
| secrets.azureCloudEnvID | Azure Cloud Environment ID | None |
| secrets.vsphereEndpoint | vSphere endpoint for login | None |
| secrets.vsphereUsername | vSphere username for login | None |
| secrets.vspherePassword | vSphere password for login | None |
| secrets.vsphereClientSecretName | The secret that contains vSphere username, vSphere password and vSphere endpoint | None |
| secrets.dockerConfig | Set base64 encoded docker config to use for image pull operations. Alternative to thesecrets.dockerConfigPath | None |
| secrets.dockerConfigPath | Use--set-file secrets.dockerConfigPath=path_to_docker_config.yamlto specify docker config for image pull. Will be overwritten ifsecrets.dockerConfigis set | None |
| cacertconfigmap.name | Name of the ConfigMap that contains a certificate for a trusted root certificate authority | None |
| clusterName | Cluster name for better logs visibility | None |
| metering.awsRegion | Sets AWS_REGION for metering service | None |
| metering.mode | Control license reporting (set toairgapfor private-network installs) | None |
| metering.reportCollectionPeriod | Sets metric report collection period (in seconds) | 1800 |
| metering.reportPushPeriod | Sets metric report push period (in seconds) | 3600 |
| metering.promoID | Sets K10 promotion ID from marketing campaigns | None |
| metering.awsMarketplace | Sets AWS cloud metering license mode | false |
| metering.awsManagedLicense | Sets AWS managed license mode | false |
| metering.redhatMarketplacePayg | Sets Red Hat cloud metering license mode | false |
| metering.licenseConfigSecretName | Sets AWS managed license config secret | None |
| externalGateway.create | Configures an external gateway for K10 API services | false |
| externalGateway.annotations | Standard annotations for the services | None |
| externalGateway.fqdn.name | Domain name for the K10 API services | None |
| externalGateway.fqdn.type | Supported gateway type:route53-mapperorexternal-dns | None |
| externalGateway.awsSSLCertARN | ARN for the AWS ACM SSL certificate used in the K10 API server | None |
| auth.basicAuth.enabled | Configures basic authentication for the K10 dashboard | false |
| auth.basicAuth.htpasswd | A username and password pair separated by a colon character | None |
| auth.basicAuth.secretName | Name of an existing Secret that contains a file generated with htpasswd | None |
| auth.k10AdminGroups | A list of groups whose members are granted admin level access to K10's dashboard | None |
| auth.k10AdminUsers | A list of users who are granted admin level access to K10's dashboard | None |
| auth.tokenAuth.enabled | Configures token based authentication for the K10 dashboard | false |
| auth.oidcAuth.enabled | Configures Open ID Connect based authentication for the K10 dashboard | false |
| auth.oidcAuth.providerURL | URL for the OIDC Provider | None |
| auth.oidcAuth.redirectURL | URL to the K10 gateway service | None |
| auth.oidcAuth.scopes | Space separated OIDC scopes required for userinfo. Example: "profile email" | None |
| auth.oidcAuth.prompt | The type of prompt to be used during authentication (none, consent, login or select_account) | select_account |
| auth.oidcAuth.clientID | Client ID given by the OIDC provider for K10 | None |
| auth.oidcAuth.clientSecret | Client secret given by the OIDC provider for K10 | None |
| auth.oidcAuth.clientSecretName | The secret that contains the Client ID and Client secret given by the OIDC provider for K10 | None |
| auth.oidcAuth.usernameClaim | The claim to be used as the username | sub |
| auth.oidcAuth.usernamePrefix | Prefix that has to be used with the username obtained from the username claim | None |
| auth.oidcAuth.groupClaim | Name of a custom OpenID Connect claim for specifying user groups | None |
| auth.oidcAuth.groupPrefix | All groups will be prefixed with this value to prevent conflicts | None |
| auth.oidcAuth.sessionDuration | Maximum OIDC session duration | 1h |
| auth.oidcAuth.refreshTokenSupport | Enable OIDC Refresh Token support | false |
| auth.openshift.enabled | Enables access to the K10 dashboard by authenticating with the OpenShift OAuth server | false |
| auth.openshift.serviceAccount | Name of the service account that represents an OAuth client | None |
| auth.openshift.clientSecret | The token corresponding to the service account | None |
| auth.openshift.clientSecretName | The secret that contains the token corresponding to the service account | None |
| auth.openshift.dashboardURL | The URL used for accessing K10's dashboard | None |
| auth.openshift.openshiftURL | The URL for accessing OpenShift's API server | None |
| auth.openshift.insecureCA | To turn off SSL verification of connections to OpenShift | false |
| auth.openshift.useServiceAccountCA | Set this to true to use the CA certificate corresponding to the Service Accountauth.openshift.serviceAccountusually found at/var/run/secrets/kubernetes.io/serviceaccount/ca.crt | false |
| auth.openshift.caCertsAutoExtraction | Set this to false to disable the OCP CA certificates automatic extraction to the K10 namespace | true |
| auth.ldap.enabled | Configures Active Directory/LDAP based authentication for the K10 dashboard | false |
| auth.ldap.restartPod | To force a restart of the authentication service Pod (useful when updating authentication config) | false |
| auth.ldap.dashboardURL | The URL used for accessing K10's dashboard | None |
| auth.ldap.host | Host and optional port of the AD/LDAP server in the formhost:port | None |
| auth.ldap.insecureNoSSL | Required if the AD/LDAP host is not using TLS | false |
| auth.ldap.insecureSkipVerifySSL | To turn off SSL verification of connections to the AD/LDAP host | false |
| auth.ldap.startTLS | When set to true, ldap:// is used to connect to the server followed by creation of a TLS session. When set to false, ldaps:// is used. | false |
| auth.ldap.bindDN | The Distinguished Name(username) used for connecting to the AD/LDAP host | None |
| auth.ldap.bindPW | The password corresponding to thebindDNfor connecting to the AD/LDAP host | None |
| auth.ldap.bindPWSecretName | The name of the secret that contains the password corresponding to thebindDNfor connecting to the AD/LDAP host | None |
| auth.ldap.userSearch.baseDN | The base Distinguished Name to start the AD/LDAP search from | None |
| auth.ldap.userSearch.filter | Optional filter to apply when searching the directory | None |
| auth.ldap.userSearch.username | Attribute used for comparing user entries when searching the directory | None |
| auth.ldap.userSearch.idAttr | AD/LDAP attribute in a user's entry that should map to the user ID field in a token | None |
| auth.ldap.userSearch.emailAttr | AD/LDAP attribute in a user's entry that should map to the email field in a token | None |
| auth.ldap.userSearch.nameAttr | AD/LDAP attribute in a user's entry that should map to the name field in a token | None |
| auth.ldap.userSearch.preferredUsernameAttr | AD/LDAP attribute in a user's entry that should map to the preferred_username field in a token | None |
| auth.ldap.groupSearch.baseDN | The base Distinguished Name to start the AD/LDAP group search from | None |
| auth.ldap.groupSearch.filter | Optional filter to apply when searching the directory for groups | None |
| auth.ldap.groupSearch.nameAttr | The AD/LDAP attribute that represents a group's name in the directory | None |
| auth.ldap.groupSearch.userMatchers | List of field pairs that are used to match a user to a group. | None |
| auth.ldap.groupSearch.userMatchers.userAttr | Attribute in the user's entry that must match with thegroupAttrwhile searching for groups | None |
| auth.ldap.groupSearch.userMatchers.groupAttr | Attribute in the group's entry that must match with theuserAttrwhile searching for groups | None |
| auth.groupAllowList | A list of groups whose members are allowed access to K10's dashboard | None |
| services.securityContext | Customsecurity contextfor K10 service containers | {"runAsUser" : 1000, "fsGroup": 1000} |
| services.securityContext.runAsUser | User ID K10 service containers run as | 1000 |
| services.securityContext.runAsGroup | Group ID K10 service containers run as | 1000 |
| services.securityContext.fsGroup | FSGroup that owns K10 service container volumes | 1000 |
| siem.logging.cluster.enabled | Whether to enable writing K10 audit event logs to stdout (standard output) | true |
| siem.logging.cloud.path | Directory path for saving audit logs in a cloud object store | k10audit/ |
| siem.logging.cloud.awsS3.enabled | Whether to enable sending K10 audit event logs to AWS S3 | true |
| injectGenericVolumeBackupSidecar.enabled | Enables injection of sidecar container required to perform Generic Volume Backup into workload Pods | false |
| injectGenericVolumeBackupSidecar.namespaceSelector.matchLabels | Set of labels to select namespaces in which sidecar injection is enabled for workloads | {} |
| injectGenericVolumeBackupSidecar.objectSelector.matchLabels | Set of labels to filter workload objects in which the sidecar is injected | {} |
| injectGenericVolumeBackupSidecar.webhookServer.port | Port number on which the mutating webhook server accepts request | 8080 |
| gateway.resources.[requests\|limits].[cpu\|memory] | Resource requests and limits for gateway Pod | {} |
| gateway.service.externalPort | Specifies the gateway services external port | 80 |
| genericVolumeSnapshot.resources.[requests\|limits].[cpu\|memory] | Specifies resource requests and limits for generic backup sidecar and all temporary Kasten worker Pods. Superseded by ActionPodSpec | {} |
| multicluster.enabled | Choose whether to enable the multi-cluster system components and capabilities | true |
| multicluster.primary.create | Choose whether to setup cluster as a multi-cluster primary | false |
| multicluster.primary.name | Primary cluster name | '' |
| multicluster.primary.ingressURL | Primary cluster dashboard URL | '' |
| prometheus.k10image.registry | (optional) Set Prometheus image registry. | gcr.io |
| prometheus.k10image.repository | (optional) Set Prometheus image repository. | kasten-images |
| prometheus.rbac.create | (optional) Whether to create Prometheus RBAC configuration. Warning - this action will allow prometheus to scrape Pods in all k8s namespaces | false |
| prometheus.alertmanager.enabled | DEPRECATED: (optional) Enable Prometheusalertmanagerservice | false |
| prometheus.alertmanager.serviceAccount.create | DEPRECATED: (optional) Set true to create ServiceAccount foralertmanager | false |
| prometheus.networkPolicy.enabled | DEPRECATED: (optional) Enable PrometheusnetworkPolicy | false |
| prometheus.prometheus-node-exporter.enabled | DEPRECATED: (optional) Enable Prometheusnode-exporter | false |
| prometheus.prometheus-node-exporter.serviceAccount.create | DEPRECATED: (optional) Set true to create ServiceAccount forprometheus-node-exporter | false |
| prometheus.prometheus-pushgateway.enabled | DEPRECATED: (optional) Enable Prometheuspushgateway | false |
| prometheus.prometheus-pushgateway.serviceAccount.create | DEPRECATED: (optional) Set true to create ServiceAccount forprometheus-pushgateway | false |
| prometheus.scrapeCAdvisor | DEPRECATED: (optional) Enable Prometheus ScrapeCAdvisor | false |
| prometheus.server.enabled | (optional) If false, K10's Prometheus server will not be created, reducing the dashboard's functionality. | true |
| prometheus.server.securityContext.runAsUser | (optional) Set security contextrunAsUserID for Prometheus server Pod | 65534 |
| prometheus.server.securityContext.runAsNonRoot | (optional) Enable security contextrunAsNonRootfor Prometheus server Pod | true |
| prometheus.server.securityContext.runAsGroup | (optional) Set security contextrunAsGroupID for Prometheus server Pod | 65534 |
| prometheus.server.securityContext.fsGroup | (optional) Set security contextfsGroupID for Prometheus server Pod | 65534 |
| prometheus.server.retention | (optional) K10 Prometheus data retention | "30d" |
| prometheus.server.strategy.rollingUpdate.maxSurge | DEPRECATED: (optional) The number of Prometheus server Pods that can be created above the desired amount of Pods during an update | "100%" |
| prometheus.server.strategy.rollingUpdate.maxUnavailable | DEPRECATED: (optional) The number of Prometheus server Pods that can be unavailable during the upgrade process | "100%" |
| prometheus.server.strategy.type | DEPRECATED: (optional) Change default deployment strategy for Prometheus server | "RollingUpdate" |
| prometheus.server.persistentVolume.enabled | DEPRECATED: (optional) If true, K10 Prometheus server will create a Persistent Volume Claim | true |
| prometheus.server.persistentVolume.size | (optional) K10 Prometheus server data Persistent Volume size | 8Gi |
| prometheus.server.persistentVolume.storageClass | (optional) StorageClassName used to create Prometheus PVC. Setting this option overwrites global StorageClass value | "" |
| prometheus.server.configMapOverrideName | DEPRECATED: (optional) Prometheus configmap name to override default generated name | k10-prometheus-config |
| prometheus.server.fullnameOverride | (optional) Prometheus deployment name to override default generated name | prometheus-server |
| prometheus.server.baseURL | (optional) K10 Prometheus external url path at which the server can be accessed | /k10/prometheus/ |
| prometheus.server.prefixURL | (optional) K10 Prometheus prefix slug at which the server can be accessed | /k10/prometheus/ |
| prometheus.server.serviceAccounts.server.create | DEPRECATED: (optional) Set true to create ServiceAccount for Prometheus server service | true |
| resources.<deploymentName>.<containerName>.[requests\|limits].[cpu\|memory] | Overwriting the default K10container resource requests and limits | varies depending on the container |
| route.enabled | Specifies whether the K10 dashboard should be exposed via route | false |
| route.host | FQDN (e.g.,.k10.example.com) for name-based virtual host | "" |
| route.path | URL path for K10 Dashboard (e.g.,/k10) | / |
| route.annotations | Additional Route object annotations | {} |
| route.labels | Additional Route object labels | {} |
| route.tls.enabled | Configures a TLS use forroute.host | false |
| route.tls.insecureEdgeTerminationPolicy | Specifies behavior for insecure scheme traffic | Redirect |
| route.tls.termination | Specifies the TLS termination of the route | edge |
| limiter.executorReplicas | Specifies the number of executor-svc Pods used to process Kasten jobs | 3 |
| limiter.executorThreads | Specifies the number of threads per executor-svc Pod used to process Kasten jobs | 8 |
| limiter.workloadSnapshotsPerAction | Per action limit of concurrent manifest data snapshots, based on workload (ex. Namespace, Deployment, StatefulSet, VirtualMachine) | 5 |
| limiter.csiSnapshotsPerCluster | Cluster-wide limit of concurrent CSI VolumeSnapshot creation requests | 10 |
| limiter.directSnapshotsPerCluster | Cluster-wide limit of concurrent non-CSI snapshot creation requests | 10 |
| limiter.snapshotExportsPerAction | Per action limit of concurrent volume export operations | 3 |
| limiter.snapshotExportsPerCluster | Cluster-wide limit of concurrent volume export operations | 10 |
| limiter.genericVolumeBackupsPerCluster | Cluster-wide limit of concurrent Generic Volume Backup operations | 10 |
| limiter.imageCopiesPerCluster | Cluster-wide limit of concurrent ImageStream container image backup (i.e. copy from) and restore (i.e. copy to) operations | 10 |
| limiter.workloadRestoresPerAction | Per action limit of concurrent manifest data restores, based on workload (ex. Namespace, Deployment, StatefulSet, VirtualMachine) | 3 |
| limiter.csiSnapshotRestoresPerAction | Per action limit of concurrent CSI volume provisioning requests when restoring from VolumeSnapshots | 3 |
| limiter.volumeRestoresPerAction | Per action limit of concurrent volume restore operations from an exported backup | 3 |
| limiter.volumeRestoresPerCluster | Cluster-wide limit of concurrent volume restore operations from exported backups | 10 |
| cluster.domainName | Specifies the domain name of the cluster | "" |
| timeout.blueprintBackup | Specifies the timeout (in minutes) for Blueprint backup actions | 45 |
| timeout.blueprintRestore | Specifies the timeout (in minutes) for Blueprint restore actions | 600 |
| timeout.blueprintDelete | Specifies the timeout (in minutes) for Blueprint delete actions | 45 |
| timeout.blueprintHooks | Specifies the timeout (in minutes) for Blueprint backupPrehook and backupPosthook actions | 20 |
| timeout.checkRepoPodReady | Specifies the timeout (in minutes) for temporary worker Pods used to validate backup repository existence | 20 |
| timeout.statsPodReady | Specifies the timeout (in minutes) for temporary worker Pods used to collect repository statistics | 20 |
| timeout.efsRestorePodReady | Specifies the timeout (in minutes) for temporary worker Pods used for shareable volume restore operations | 45 |
| timeout.workerPodReady | Specifies the timeout (in minutes) for all other temporary worker Pods used during Veeam Kasten operations | 15 |
| timeout.jobWait | Specifies the timeout (in minutes) for completing execution of any child job, after which the parent job will be canceled. If no value is set, a default of 10 hours will be used | None |
| awsConfig.assumeRoleDuration | Duration of a session token generated by AWS for an IAM role. The minimum value is 15 minutes and the maximum value is the maximum duration setting for that IAM role. For documentation about how to view and edit the maximum session duration for an IAM role seehttps://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html#id_roles_use_view-role-max-session. The value accepts a number along with a single characterm(for minutes) orh(for hours) Examples: 60m or 2h | '' |
| awsConfig.efsBackupVaultName | Specifies the AWS EFS backup vault name | k10vault |
| vmWare.taskTimeoutMin | Specifies the timeout for VMWare operations | 60 |
| encryption.primaryKey.awsCmkKeyId | Specifies the AWS CMK key ID for encrypting K10 Primary Key | None |
| garbagecollector.daemonPeriod | Sets garbage collection period (in seconds) | 21600 |
| garbagecollector.keepMaxActions | Sets maximum actions to keep | 1000 |
| garbagecollector.actions.enabled | Enables action collectors | false |
| kubeVirtVMs.snapshot.unfreezeTimeout | Defines the time duration within which the VMs must be unfrozen while backing them up. To know more about formatgo doccan be followed | 5m |
| excludedApps | Specifies a list of applications to be excluded from the dashboard & compliance considerations. Format should be a :ref:YAML array<k10_compliance> | ["kube-system", "kube-ingress", "kube-node-lease", "kube-public", "kube-rook-ceph"] |
| workerPodMetricSidecar.enabled | Enables a sidecar container for temporary worker Pods used to push Pod performance metrics to Prometheus | true |
| workerPodMetricSidecar.metricLifetime | Specifies the period after which metrics for an individual worker Pod are removed from Prometheus | 2m |
| workerPodMetricSidecar.pushGatewayInterval | Specifies the frequency for pushing metrics into Prometheus | 30s |
| workerPodMetricSidecar.resources.[requests\|limits].[cpu\|memory] | Specifies resource requests and limits for the temporary worker Pod metric sidecar | {} |
| forceRootInBlueprintActions | Forces any Pod created by a Blueprint to run as root user | true |
| defaultPriorityClassName | Specifies the defaultpriority classname for all K10 deployments and ephemeral Pods | None |
| priorityClassName.<deploymentName> | Overrides the defaultpriority classname for the specified deployment | {} |
| ephemeralPVCOverhead | Set the percentage increase for the ephemeral Persistent Volume Claim's storage request, e.g. PVC size = (file raw size) * (1 +ephemeralPVCOverhead) | 0.1 |
| datastore.parallelUploads | Specifies how many files can be uploaded in parallel to the data store | 8 |
| datastore.parallelDownloads | Specifies how many files can be downloaded in parallel from the data store | 8 |
| datastore.parallelBlockUploads | Specifies how many blocks can be uploaded in parallel to the data store | 8 |
| datastore.parallelBlockDownloads | Specifies how many blocks can be downloaded in parallel from the data store | 8 |
| kastenDisasterRecovery.quickMode.enabled | Enables K10 Quick Disaster Recovery | false |
| fips.enabled | Specifies whether K10 should be run in the FIPS mode of operation | false |
| workerPodCRDs.enabled | Specifies whether K10 should useActionPodSpecfor granular resource control of worker Pods | false |
| workerPodCRDs.resourcesRequests.maxCPU | Max CPU which might be setup inActionPodSpec | '' |
| workerPodCRDs.resourcesRequests.maxMemory | Max memory which might be setup inActionPodSpec | '' |
| workerPodCRDs.defaultActionPodSpec.name | The name ofActionPodSpecthat will be used by default for worker Pod resources. | '' |
| workerPodCRDs.defaultActionPodSpec.namespace | The namespace ofActionPodSpecthat will be used by default for worker Pod resources. | '' |
| vap.kastenPolicyPermissions.enabled | Enable installation of the ValidatingAdmissionPolicy to evaluate non-admin user permissions while creating a Kasten policy. | false |

## Helm Configuration for Parallel Upload to the Storage Repository â

Veeam Kasten provides an option to manage parallelism for file mode uploads to the storage repository through a configurable parameter, datastore.parallelUploads via Helm. To upload N files in parallel to the
  storage repository, configure this flag to N. This flag is adjusted
  when dealing with larger PVCs to improve performance. By default, the
  value is set to 8.

A similar option called datastore.parallelBlockUploads is used to control
  how many blocks can be uploaded concurrently when exporting a snapshot in block mode .
  Adjusting this value may be necessary to decrease the upload time for larger
  PVCs but comes at a cost of additional memory utilization in the ephemeral
  Pod launched for the operation.
  By default, the value is set to 8.

These parameters should not be modified unless instructed by the support
    team.

## Helm Configuration for Parallel Download from the Storage Repository â

Veeam Kasten provides an option to manage parallelism for file mode downloads from the storage repository through a configurable parameter, datastore.parallelDownloads via Helm. To download N files in parallel from
  the storage repository, configure this flag to N. This flag is
  adjusted when dealing with larger PVCs to improve performance. By
  default, the value is set to 8.

A similar option called datastore.parallelBlockDownloads is used to
  control how many blocks can be downloaded concurrently when restoring from a
  snapshot exported in block mode .
  Adjusting this value may be necessary to decrease the restore time for larger
  PVCs but comes at a cost of additional memory utilization in the ephemeral
  Pod launched for the operation.
  By default, the value is set to 8.

## Setting Custom Labels and Annotations on Veeam Kasten Pods â

Veeam Kasten provides the ability to apply labels and annotations to all
  of its pods. This applies to both core pods and all temporary worker
  pods created as a result of Veeam Kasten operations. Labels and
  annotations are applied using the global.podLabels and global.podAnnotations Helm flags, respectively. For example, if using
  a values.yaml file:

```
global: podLabels:   app.kubernetes.io/component: "database"   topology.kubernetes.io/region: "us-east-1" podAnnotations:   config.kubernetes.io/local-config: "true"   kubernetes.io/description: "Description"
```

Alternatively, the Helm parameters can be configured using the --set flag:

```
--set global.podLabels.labelKey1=value1 --set global.podLabels.labelKey2=value2 \--set global.podAnnotations.annotationKey1="Example annotation" --set global.podAnnotations.annotationKey2=value2
```

Labels and annotations passed using these Helm parameters
    ( global.podLabels and global.podAnnotations ) apply to the Prometheus pods as well, if it is managed by Veeam
    Kasten. However, if labels and annotations are set in the Prometheus sub-chart, they will be prioritized over the global pod labels
    and annotations set.

---

## Install Advanced

## FREE Veeam Kasten Edition and Licensing â

By default, Veeam Kasten comes with an embedded free edition license.
  The free edition license allows you to use the software on a cluster
  with at most 50 worker nodes in the first 30 days, and then 5 nodes
  after the 30-day period. In order to continue using the free license,
  regular updates to stay within the 6 month support window might be
  required. You can remove the node restriction of the free license by
  updating to Enterprise Edition and obtaining the appropriate license
  from the Kasten team.

### Using a Custom License During Install â

To install a license that removes the node restriction, please add the
  following to any of the helm install commands:

```
--set license=<license-text>
```

or, to install a license from a file:

```
--set-file license=<path-to-license-file>
```

Veeam Kasten dynamically retrieves the license key and a pod restart
    is not required.

### Changing Licenses â

To add a new license to Veeam Kasten, a secret needs to be created in
  the Veeam Kasten namespace (default is kasten-io ) with the requirement
  that the license text be set in a field named license . To do this from
  the command line, run:

```
$ kubectl create secret generic <license-secret-name> \    --namespace kasten-io \    --from-literal=license="<license-text>"
```

or, to add a license from a file:

```
$ kubectl create secret generic <license-secret-name> \    --namespace kasten-io \    --from-file=license="<path-to-license-file>"
```

Multiple license secrets can exist simultaneously and Veeam Kasten
    will check if any are valid. This license check is done periodically and
    so, no Veeam Kasten restarts are required if a different existing
    license becomes required (e.g., due to a cluster expansion or an old
    license expiry) or when a new license is added.

The resulting license will look like:

```
apiVersion: v1data:  license: Y3Vz...kind: Secretmetadata:  creationTimestamp: "2020-04-14T23:50:05Z"  labels:    app: k10    app.kubernetes.io/instance: k10    app.kubernetes.io/managed-by: Helm    app.kubernetes.io/name: k10    helm.sh/chart: k10-8.0.4    heritage: Helm    release: k10  name: k10-custom-license  namespace: kasten-iotype: Opaque
```

Similarly, old licenses can be removed by deleting the secret that
  contains it.

```
$ kubectl delete secret <license-secret-name> \    --namespace kasten-io
```

### Add Licenses via Dashboard â

It is possible to add a license via the Licenses page of the Settings menu in the navigation sidebar. The license can be pasted
  directly into the text field or loaded from a .lic file.

### License Grace period â

If the license status of the cluster becomes invalid (e.g., the licensed
  node limit is exceeded), the ability to perform manual actions or
  creating new policies will be disabled but your previously scheduled
  policies will continue to run for 50 days. The displayed warning will be
  look like:

By default, Veeam Kasten provides a grace period of 50 days to ensure
  that applications remain protected while a new license is obtained or
  the cluster is brought back into compliance by reducing the number of
  nodes. Veeam Kasten will stop the creation of any new jobs (scheduled or
  manual) after the grace period expires.

If the cluster's license status frequently swaps between valid and
  invalid states, the amount of time the cluster license spends in an
  invalid status will be subtracted from subsequent grace periods.

You can see node usage from the last two months via the Licenses page
  of the Settings menu in the navigation sidebar. Usage starts being
  tracked from the installation date of 4.5.8+. From 5.0.11+ you can see
  the same information through Prometheus .

## Manually Creating or Using an Existing Service Account â

```
For more information regarding ServiceAccount restrictions with Kasten,please refer to this [documentation](../restrictions.md#cluster-admin-restrictions).
```

The following instructions can be used to create a new Service Account
  that grants Veeam Kasten the required permissions to Kubernetes
  resources and the use the given Service Account as a part of the install
  process. The instructions assume that you will be installing Veeam
  Kasten in the kasten-io namespace.

```
# Create kasten-io namespace if have not done it yet.$ kubectl create namespace kasten-io# Create a ServiceAccount for k10 k10-sa$ kubectl --namespace kasten-io create sa k10-sa# Create a cluster role binding for k10-sa$ kubectl create clusterrolebinding k10-sa-rb \    --clusterrole cluster-admin \    --serviceaccount=kasten-io:k10-sa
```

Following the SA creation, you can install Veeam Kasten using:

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set rbac.create=false \    --set serviceAccount.create=false \    --set serviceAccount.name=k10-sa
```

## Pinning Veeam Kasten to Specific Nodes â

While not generally recommended, there might be situations (e.g., test
  environments, nodes reserved for infrastructure tools, or clusters
  without autoscaling enabled) where Veeam Kasten might need to be pinned
  to a subset of nodes in your cluster. You can do this easily with an
  existing deployment by using a combination of NodeSelectors and Taints and
Tolerations .

The process to modify a deployment to accomplish this is demonstrated in
  the following example. The example assumes that the nodes you want to
  restrict Veeam Kasten to have the label selector-key: selector-value and a taint set to taint-key=taint-value:NoSchedule .

```
$ cat << EOF > patch.yamlspec:  template:    spec:      nodeSelector:        selector-key: selector-value      tolerations:      - key: "taint-key"        operator: "Equal"        value: "taint-value"        effect: "NoSchedule"EOF$ kubectl get deployment --namespace kasten-io | awk 'FNR == 1 {next} {print $1}' \  | xargs -I DEP kubectl patch deployments DEP --namespace kasten-io --patch "$(cat patch.yaml)"
```

## Using Trusted Root Certificate Authority Certificates for TLS â

For temporary testing of object storage systems that are deployed using
    self-signed certificates signed by a trusted Root CA, it is also
    possible to disable certificate verification if the Root CA certificate is not easily available.

If the S3-compatible object store configured in a Location Profile was
  deployed with a self-signed certificate that was signed by a trusted
  Root Certificate Authority (Root CA), then the certificate for such a
  certificate authority has to be provided to Veeam Kasten to enable
  successful verification of TLS connections to the object store.

Similarly, to authenticate with a private OIDC provider whose
  self-signed certificate was signed by a trusted Root CA, the certificate
  for the Root CA has to be provided to Veeam Kasten to enable successful
  verification of TLS connections to the OIDC provider.

Multiple Root CAs can be bundled together in the same file.

### Install Root CA in Veeam Kasten's namespace â

Assuming Veeam Kasten will be deployed in the kasten-io namespace, the
  following instructions will make a private Root CA certificate available
  to Veeam kasten.

```
$ kubectl --namespace kasten-io create configmap <configmap-name> --from-file=<custom-bundle-file>.pem
```

Replace <custom-bundle-file> with the desired filename

To provide the Root CA certificate to Veeam Kasten, add the following to
  the Helm install command.

```
--set cacertconfigmap.name=<configmap-name>--set cacertconfigmap.key=<configmap-key>
```

Replace <configmap-key> with the desired key

Use of cacertconfigmap.key is optional. If it is unspecified,
    the ConfigMap referenced by cacertconfigmap.name must use
    the expected default key name, custom-ca-bundle.pem .

### Install Root CA in Application's Namespace When Using Kanister Sidecar â

If you either use Veeam Kasten's Kanister sidecar injection feature for
  injecting the Kanister sidecar in your application's namespace or if
  you have manually added the Kanister sidecar, you must create a
  ConfigMap containing the Root CA in the application's namespace and
  update the application's specification so that the ConfigMap is mounted
  as a Volume. This will enable the Kanister sidecar to verify TLS
  connections successfully using the Root CA in the ConfigMap.

Assuming that the application's namespace is named test-app , use the
  following command to create a ConfigMap containing the Root CA in the
  application's namespace:

```
$ kubectl --namespace test-app create configmap <configmap-name> --from-file= <custom-bundle-file>.pem
```

Replace <configmap-name> with any desired ConfigMap name and <custom-bundle-file> with the desired filename

This is an example of a VolumeMount that must be added to the
  application's specification.

```
- name: custom-ca-bundle-store  mountPath: "/etc/ssl/certs/<custom-bundle-file>.pem"  subPath:<custom-bundle-file>.pem
```

This is an example of a Volume that must be added to the application's
  specification.

```
- name: custom-ca-bundle-store  configMap:    name: custom-ca-bundle-store
```

### Troubleshooting â

If Veeam Kasten is deployed without the cacertconfigmap.name setting,
  validation failures such as the one shown below will be seen while
  configuring a Location Profile using the web based user interface.

In the absence of the cacertconfigmap.name setting, authentication
  with a private OIDC provider will fail. Veeam Kasten's logs will show
  an error x509: certificate signed by unknown authority .

If you do not install the Root CA in the application namespace when
  using a Kanister sidecar with the application, the logs will show an
  error x509: certificate signed by unknown authority when the sidecar
  tries to connect to any endpoint that requires TLS verification.

## Running Veeam Kasten Containers as a Specific User â

Veeam Kasten service containers run with UID and fsGroup 1000 by
  default. If the storage class Veeam Kasten is configured to use for its
  own services requires the containers to run as a specific user, then the
  user can be modified.

This is often needed when using shared storage, such as NFS/SMB, where
  permissions on the target storage require a specific user.

To run as a specific user (e.g., root (0), add the following to the Helm
  install command:

```
--set services.securityContext.runAsUser=0 \--set services.securityContext.fsGroup=0 \--set prometheus.server.securityContext.runAsUser=0 \--set prometheus.server.securityContext.runAsGroup=0 \--set prometheus.server.securityContext.runAsNonRoot=false \--set prometheus.server.securityContext.fsGroup=0
```

Other SecurityContext settings for the Veeam Kasten service containers can be specified using
  the --set service.securityContext.<setting name> and --set prometheus.server.securityContext.<setting name> options.

## Configuring Prometheus â

Prometheus is an open-source system monitoring
  and alerting toolkit bundled with Veeam Kasten.

When passing value from the command line, the value key has to be
  prefixed with the prometheus. string:

```
--set prometheus.server.persistentVolume.storageClass=default.sc
```

When passing values in a YAML file, all prometheus settings should be
  under the prometheus key:

```
# values.yaml# global values - apply to both Veeam Kasten and prometheusglobal:  persistence:    storageClass: default-sc# Veeam Kasten specific settingsauth:  basicAuth: enabled# prometheus specific settingsprometheus:  server:    persistentVolume:      storageClass: another-sc
```

To modify the bundled Prometheus configuration, only use the helm values
    listed in the Complete List of Veeam Kasten Helm Options . Any undocumented configurations may affect the
    functionality of the Veeam Kasten. Additionally, Veeam Kasten does not
    support disabling Prometheus service, which may lead to
    unsupported scenarios, potential monitoring and logging issues, and
    overall functionality disruptions. It is recommended to keep these
    services enabled to ensure proper functionality and prevent unexpected
    behavior.

## Complete List of Veeam Kasten Helm Options â

| Parameter | Description | Default | eula.accept | Whether to enable accept EULA before installation | false |
| :---: | :---: | :---: | :---: | :---: | :---: |
| eula.accept | Whether to enable accept EULA before installation | false |
| eula.company | Company name. Required field if EULA is accepted | None |
| eula.email | Contact email. Required field if EULA is accepted | None |
| license | License string obtained from Kasten | None |
| rbac.create | Whether to enable RBAC with a specific cluster role and binding for K10 | true |
| scc.create | Toggle creation of SecurityContextConstraints for Kasten ServiceAccount(s) | false |
| scc.priority | Sets the SecurityContextConstraints priority | 15 |
| scc.allowCSI | Toggles allowing CSI ephemeral volumes in SecurityContextConstraints | false |
| networkPolicy.create | Toggle creation of built-in NetworkPolicies | true |
| services.dashboardbff.hostNetwork | Whether the dashboardbff Pods may use the node network | false |
| services.executor.hostNetwork | Whether the executor Pods may use the node network | false |
| services.aggregatedapis.hostNetwork | Whether the aggregatedapis Pods may use the node network | false |
| serviceAccount.create | Specifies whether a ServiceAccount should be created | true |
| serviceAccount.name | The name of the ServiceAccount to use. If not set, a name is derived using the release and chart names. | None |
| ingress.create | Specifies whether the K10 dashboard should be exposed via ingress | false |
| ingress.name | Optional name of the Ingress object for the K10 dashboard. If not set, the name is formed using the release name. | {Release.Name}-ingress |
| ingress.class | Cluster ingress controller class:nginx,GCE | None |
| ingress.host | FQDN (e.g.,k10.example.com) for name-based virtual host | None |
| ingress.urlPath | URL path for K10 Dashboard (e.g.,/k10) | Release.Name |
| ingress.pathType | Specifies the path type for the ingress resource | ImplementationSpecific |
| ingress.annotations | Additional Ingress object annotations | {} |
| ingress.tls.enabled | Configures a TLS use foringress.host | false |
| ingress.tls.secretName | Optional TLS secret name | None |
| ingress.defaultBackend.service.enabled | Configures the default backend backed by a service for the K10 dashboard Ingress (mutually exclusive setting withingress.defaultBackend.resource.enabled). | false |
| ingress.defaultBackend.service.name | The name of a service referenced by the default backend (required if the service-backed default backend is used). | None |
| ingress.defaultBackend.service.port.name | The port name of a service referenced by the default backend (mutually exclusive setting with portnumber, required if the service-backed default backend is used). | None |
| ingress.defaultBackend.service.port.number | The port number of a service referenced by the default backend (mutually exclusive setting with portname, required if the service-backed default backend is used). | None |
| ingress.defaultBackend.resource.enabled | Configures the default backend backed by a resource for the K10 dashboard Ingress (mutually exclusive setting withingress.defaultBackend.service.enabled). | false |
| ingress.defaultBackend.resource.apiGroup | Optional API group of a resource backing the default backend. | '' |
| ingress.defaultBackend.resource.kind | The type of a resource being referenced by the default backend (required if the resource default backend is used). | None |
| ingress.defaultBackend.resource.name | The name of a resource being referenced by the default backend (required if the resource default backend is used). | None |
| global.persistence.size | Default global size of volumes for K10 persistent services | 20Gi |
| global.persistence.catalog.size | Size of a volume for catalog service | global.persistence.size |
| global.persistence.jobs.size | Size of a volume for jobs service | global.persistence.size |
| global.persistence.logging.size | Size of a volume for logging service | global.persistence.size |
| global.persistence.metering.size | Size of a volume for metering service | global.persistence.size |
| global.persistence.storageClass | Specified StorageClassName will be used for PVCs | None |
| global.podLabels | Configures custom labels to be set to all Kasten Pods | None |
| global.podAnnotations | Configures custom annotations to be set to all Kasten Pods | None |
| global.airgapped.repository | Specify the helm repository for offline (airgapped) installation | '' |
| global.imagePullSecret | Provide secret which contains docker config for private repository. Usek10-ecrwhen secrets.dockerConfigPath is used. | '' |
| global.prometheus.external.host | Provide external prometheus host name | '' |
| global.prometheus.external.port | Provide external prometheus port number | '' |
| global.prometheus.external.baseURL | Provide Base URL of external prometheus | '' |
| global.network.enable_ipv6 | EnableIPv6support for K10 | false |
| google.workloadIdentityFederation.enabled | Enable Google Workload Identity Federation for K10 | false |
| google.workloadIdentityFederation.idp.type | Identity Provider type for Google Workload Identity Federation for K10 | '' |
| google.workloadIdentityFederation.idp.aud | Audience for whom the ID Token from Identity Provider is intended | '' |
| secrets.awsAccessKeyId | AWS access key ID (required for AWS deployment) | None |
| secrets.awsSecretAccessKey | AWS access key secret | None |
| secrets.awsIamRole | ARN of the AWS IAM role assumed by K10 to perform any AWS operation. | None |
| secrets.awsClientSecretName | The secret that contains AWS access key ID, AWS access key secret and AWS IAM role for AWS | None |
| secrets.googleApiKey | Non-default base64 encoded GCP Service Account key | None |
| secrets.googleProjectId | Sets Google Project ID other than the one used in the GCP Service Account | None |
| secrets.azureTenantId | Azure tenant ID (required for Azure deployment) | None |
| secrets.azureClientId | Azure Service App ID | None |
| secrets.azureClientSecret | Azure Service APP secret | None |
| secrets.azureClientSecretName | The secret that contains ClientID, ClientSecret and TenantID for Azure | None |
| secrets.azureResourceGroup | Resource Group name that was created for the Kubernetes cluster | None |
| secrets.azureSubscriptionID | Subscription ID in your Azure tenant | None |
| secrets.azureResourceMgrEndpoint | Resource management endpoint for the Azure Stack instance | None |
| secrets.azureADEndpoint | Azure Active Directory login endpoint | None |
| secrets.azureADResourceID | Azure Active Directory resource ID to obtain AD tokens | None |
| secrets.microsoftEntraIDEndpoint | Microsoft Entra ID login endpoint | None |
| secrets.microsoftEntraIDResourceID | Microsoft Entra ID resource ID to obtain AD tokens | None |
| secrets.azureCloudEnvID | Azure Cloud Environment ID | None |
| secrets.vsphereEndpoint | vSphere endpoint for login | None |
| secrets.vsphereUsername | vSphere username for login | None |
| secrets.vspherePassword | vSphere password for login | None |
| secrets.vsphereClientSecretName | The secret that contains vSphere username, vSphere password and vSphere endpoint | None |
| secrets.dockerConfig | Set base64 encoded docker config to use for image pull operations. Alternative to thesecrets.dockerConfigPath | None |
| secrets.dockerConfigPath | Use--set-file secrets.dockerConfigPath=path_to_docker_config.yamlto specify docker config for image pull. Will be overwritten ifsecrets.dockerConfigis set | None |
| cacertconfigmap.name | Name of the ConfigMap that contains a certificate for a trusted root certificate authority | None |
| clusterName | Cluster name for better logs visibility | None |
| metering.awsRegion | Sets AWS_REGION for metering service | None |
| metering.mode | Control license reporting (set toairgapfor private-network installs) | None |
| metering.reportCollectionPeriod | Sets metric report collection period (in seconds) | 1800 |
| metering.reportPushPeriod | Sets metric report push period (in seconds) | 3600 |
| metering.promoID | Sets K10 promotion ID from marketing campaigns | None |
| metering.awsMarketplace | Sets AWS cloud metering license mode | false |
| metering.awsManagedLicense | Sets AWS managed license mode | false |
| metering.redhatMarketplacePayg | Sets Red Hat cloud metering license mode | false |
| metering.licenseConfigSecretName | Sets AWS managed license config secret | None |
| externalGateway.create | Configures an external gateway for K10 API services | false |
| externalGateway.annotations | Standard annotations for the services | None |
| externalGateway.fqdn.name | Domain name for the K10 API services | None |
| externalGateway.fqdn.type | Supported gateway type:route53-mapperorexternal-dns | None |
| externalGateway.awsSSLCertARN | ARN for the AWS ACM SSL certificate used in the K10 API server | None |
| auth.basicAuth.enabled | Configures basic authentication for the K10 dashboard | false |
| auth.basicAuth.htpasswd | A username and password pair separated by a colon character | None |
| auth.basicAuth.secretName | Name of an existing Secret that contains a file generated with htpasswd | None |
| auth.k10AdminGroups | A list of groups whose members are granted admin level access to K10's dashboard | None |
| auth.k10AdminUsers | A list of users who are granted admin level access to K10's dashboard | None |
| auth.tokenAuth.enabled | Configures token based authentication for the K10 dashboard | false |
| auth.oidcAuth.enabled | Configures Open ID Connect based authentication for the K10 dashboard | false |
| auth.oidcAuth.providerURL | URL for the OIDC Provider | None |
| auth.oidcAuth.redirectURL | URL to the K10 gateway service | None |
| auth.oidcAuth.scopes | Space separated OIDC scopes required for userinfo. Example: "profile email" | None |
| auth.oidcAuth.prompt | The type of prompt to be used during authentication (none, consent, login or select_account) | select_account |
| auth.oidcAuth.clientID | Client ID given by the OIDC provider for K10 | None |
| auth.oidcAuth.clientSecret | Client secret given by the OIDC provider for K10 | None |
| auth.oidcAuth.clientSecretName | The secret that contains the Client ID and Client secret given by the OIDC provider for K10 | None |
| auth.oidcAuth.usernameClaim | The claim to be used as the username | sub |
| auth.oidcAuth.usernamePrefix | Prefix that has to be used with the username obtained from the username claim | None |
| auth.oidcAuth.groupClaim | Name of a custom OpenID Connect claim for specifying user groups | None |
| auth.oidcAuth.groupPrefix | All groups will be prefixed with this value to prevent conflicts | None |
| auth.oidcAuth.sessionDuration | Maximum OIDC session duration | 1h |
| auth.oidcAuth.refreshTokenSupport | Enable OIDC Refresh Token support | false |
| auth.openshift.enabled | Enables access to the K10 dashboard by authenticating with the OpenShift OAuth server | false |
| auth.openshift.serviceAccount | Name of the service account that represents an OAuth client | None |
| auth.openshift.clientSecret | The token corresponding to the service account | None |
| auth.openshift.clientSecretName | The secret that contains the token corresponding to the service account | None |
| auth.openshift.dashboardURL | The URL used for accessing K10's dashboard | None |
| auth.openshift.openshiftURL | The URL for accessing OpenShift's API server | None |
| auth.openshift.insecureCA | To turn off SSL verification of connections to OpenShift | false |
| auth.openshift.useServiceAccountCA | Set this to true to use the CA certificate corresponding to the Service Accountauth.openshift.serviceAccountusually found at/var/run/secrets/kubernetes.io/serviceaccount/ca.crt | false |
| auth.openshift.caCertsAutoExtraction | Set this to false to disable the OCP CA certificates automatic extraction to the K10 namespace | true |
| auth.ldap.enabled | Configures Active Directory/LDAP based authentication for the K10 dashboard | false |
| auth.ldap.restartPod | To force a restart of the authentication service Pod (useful when updating authentication config) | false |
| auth.ldap.dashboardURL | The URL used for accessing K10's dashboard | None |
| auth.ldap.host | Host and optional port of the AD/LDAP server in the formhost:port | None |
| auth.ldap.insecureNoSSL | Required if the AD/LDAP host is not using TLS | false |
| auth.ldap.insecureSkipVerifySSL | To turn off SSL verification of connections to the AD/LDAP host | false |
| auth.ldap.startTLS | When set to true, ldap:// is used to connect to the server followed by creation of a TLS session. When set to false, ldaps:// is used. | false |
| auth.ldap.bindDN | The Distinguished Name(username) used for connecting to the AD/LDAP host | None |
| auth.ldap.bindPW | The password corresponding to thebindDNfor connecting to the AD/LDAP host | None |
| auth.ldap.bindPWSecretName | The name of the secret that contains the password corresponding to thebindDNfor connecting to the AD/LDAP host | None |
| auth.ldap.userSearch.baseDN | The base Distinguished Name to start the AD/LDAP search from | None |
| auth.ldap.userSearch.filter | Optional filter to apply when searching the directory | None |
| auth.ldap.userSearch.username | Attribute used for comparing user entries when searching the directory | None |
| auth.ldap.userSearch.idAttr | AD/LDAP attribute in a user's entry that should map to the user ID field in a token | None |
| auth.ldap.userSearch.emailAttr | AD/LDAP attribute in a user's entry that should map to the email field in a token | None |
| auth.ldap.userSearch.nameAttr | AD/LDAP attribute in a user's entry that should map to the name field in a token | None |
| auth.ldap.userSearch.preferredUsernameAttr | AD/LDAP attribute in a user's entry that should map to the preferred_username field in a token | None |
| auth.ldap.groupSearch.baseDN | The base Distinguished Name to start the AD/LDAP group search from | None |
| auth.ldap.groupSearch.filter | Optional filter to apply when searching the directory for groups | None |
| auth.ldap.groupSearch.nameAttr | The AD/LDAP attribute that represents a group's name in the directory | None |
| auth.ldap.groupSearch.userMatchers | List of field pairs that are used to match a user to a group. | None |
| auth.ldap.groupSearch.userMatchers.userAttr | Attribute in the user's entry that must match with thegroupAttrwhile searching for groups | None |
| auth.ldap.groupSearch.userMatchers.groupAttr | Attribute in the group's entry that must match with theuserAttrwhile searching for groups | None |
| auth.groupAllowList | A list of groups whose members are allowed access to K10's dashboard | None |
| services.securityContext | Customsecurity contextfor K10 service containers | {"runAsUser" : 1000, "fsGroup": 1000} |
| services.securityContext.runAsUser | User ID K10 service containers run as | 1000 |
| services.securityContext.runAsGroup | Group ID K10 service containers run as | 1000 |
| services.securityContext.fsGroup | FSGroup that owns K10 service container volumes | 1000 |
| siem.logging.cluster.enabled | Whether to enable writing K10 audit event logs to stdout (standard output) | true |
| siem.logging.cloud.path | Directory path for saving audit logs in a cloud object store | k10audit/ |
| siem.logging.cloud.awsS3.enabled | Whether to enable sending K10 audit event logs to AWS S3 | true |
| injectGenericVolumeBackupSidecar.enabled | Enables injection of sidecar container required to perform Generic Volume Backup into workload Pods | false |
| injectGenericVolumeBackupSidecar.namespaceSelector.matchLabels | Set of labels to select namespaces in which sidecar injection is enabled for workloads | {} |
| injectGenericVolumeBackupSidecar.objectSelector.matchLabels | Set of labels to filter workload objects in which the sidecar is injected | {} |
| injectGenericVolumeBackupSidecar.webhookServer.port | Port number on which the mutating webhook server accepts request | 8080 |
| gateway.resources.[requests\|limits].[cpu\|memory] | Resource requests and limits for gateway Pod | {} |
| gateway.service.externalPort | Specifies the gateway services external port | 80 |
| genericVolumeSnapshot.resources.[requests\|limits].[cpu\|memory] | Specifies resource requests and limits for generic backup sidecar and all temporary Kasten worker Pods. Superseded by ActionPodSpec | {} |
| multicluster.enabled | Choose whether to enable the multi-cluster system components and capabilities | true |
| multicluster.primary.create | Choose whether to setup cluster as a multi-cluster primary | false |
| multicluster.primary.name | Primary cluster name | '' |
| multicluster.primary.ingressURL | Primary cluster dashboard URL | '' |
| prometheus.k10image.registry | (optional) Set Prometheus image registry. | gcr.io |
| prometheus.k10image.repository | (optional) Set Prometheus image repository. | kasten-images |
| prometheus.rbac.create | (optional) Whether to create Prometheus RBAC configuration. Warning - this action will allow prometheus to scrape Pods in all k8s namespaces | false |
| prometheus.alertmanager.enabled | DEPRECATED: (optional) Enable Prometheusalertmanagerservice | false |
| prometheus.alertmanager.serviceAccount.create | DEPRECATED: (optional) Set true to create ServiceAccount foralertmanager | false |
| prometheus.networkPolicy.enabled | DEPRECATED: (optional) Enable PrometheusnetworkPolicy | false |
| prometheus.prometheus-node-exporter.enabled | DEPRECATED: (optional) Enable Prometheusnode-exporter | false |
| prometheus.prometheus-node-exporter.serviceAccount.create | DEPRECATED: (optional) Set true to create ServiceAccount forprometheus-node-exporter | false |
| prometheus.prometheus-pushgateway.enabled | DEPRECATED: (optional) Enable Prometheuspushgateway | false |
| prometheus.prometheus-pushgateway.serviceAccount.create | DEPRECATED: (optional) Set true to create ServiceAccount forprometheus-pushgateway | false |
| prometheus.scrapeCAdvisor | DEPRECATED: (optional) Enable Prometheus ScrapeCAdvisor | false |
| prometheus.server.enabled | (optional) If false, K10's Prometheus server will not be created, reducing the dashboard's functionality. | true |
| prometheus.server.securityContext.runAsUser | (optional) Set security contextrunAsUserID for Prometheus server Pod | 65534 |
| prometheus.server.securityContext.runAsNonRoot | (optional) Enable security contextrunAsNonRootfor Prometheus server Pod | true |
| prometheus.server.securityContext.runAsGroup | (optional) Set security contextrunAsGroupID for Prometheus server Pod | 65534 |
| prometheus.server.securityContext.fsGroup | (optional) Set security contextfsGroupID for Prometheus server Pod | 65534 |
| prometheus.server.retention | (optional) K10 Prometheus data retention | "30d" |
| prometheus.server.strategy.rollingUpdate.maxSurge | DEPRECATED: (optional) The number of Prometheus server Pods that can be created above the desired amount of Pods during an update | "100%" |
| prometheus.server.strategy.rollingUpdate.maxUnavailable | DEPRECATED: (optional) The number of Prometheus server Pods that can be unavailable during the upgrade process | "100%" |
| prometheus.server.strategy.type | DEPRECATED: (optional) Change default deployment strategy for Prometheus server | "RollingUpdate" |
| prometheus.server.persistentVolume.enabled | DEPRECATED: (optional) If true, K10 Prometheus server will create a Persistent Volume Claim | true |
| prometheus.server.persistentVolume.size | (optional) K10 Prometheus server data Persistent Volume size | 8Gi |
| prometheus.server.persistentVolume.storageClass | (optional) StorageClassName used to create Prometheus PVC. Setting this option overwrites global StorageClass value | "" |
| prometheus.server.configMapOverrideName | DEPRECATED: (optional) Prometheus configmap name to override default generated name | k10-prometheus-config |
| prometheus.server.fullnameOverride | (optional) Prometheus deployment name to override default generated name | prometheus-server |
| prometheus.server.baseURL | (optional) K10 Prometheus external url path at which the server can be accessed | /k10/prometheus/ |
| prometheus.server.prefixURL | (optional) K10 Prometheus prefix slug at which the server can be accessed | /k10/prometheus/ |
| prometheus.server.serviceAccounts.server.create | DEPRECATED: (optional) Set true to create ServiceAccount for Prometheus server service | true |
| resources.<deploymentName>.<containerName>.[requests\|limits].[cpu\|memory] | Overwriting the default K10container resource requests and limits | varies depending on the container |
| route.enabled | Specifies whether the K10 dashboard should be exposed via route | false |
| route.host | FQDN (e.g.,.k10.example.com) for name-based virtual host | "" |
| route.path | URL path for K10 Dashboard (e.g.,/k10) | / |
| route.annotations | Additional Route object annotations | {} |
| route.labels | Additional Route object labels | {} |
| route.tls.enabled | Configures a TLS use forroute.host | false |
| route.tls.insecureEdgeTerminationPolicy | Specifies behavior for insecure scheme traffic | Redirect |
| route.tls.termination | Specifies the TLS termination of the route | edge |
| limiter.executorReplicas | Specifies the number of executor-svc Pods used to process Kasten jobs | 3 |
| limiter.executorThreads | Specifies the number of threads per executor-svc Pod used to process Kasten jobs | 8 |
| limiter.workloadSnapshotsPerAction | Per action limit of concurrent manifest data snapshots, based on workload (ex. Namespace, Deployment, StatefulSet, VirtualMachine) | 5 |
| limiter.csiSnapshotsPerCluster | Cluster-wide limit of concurrent CSI VolumeSnapshot creation requests | 10 |
| limiter.directSnapshotsPerCluster | Cluster-wide limit of concurrent non-CSI snapshot creation requests | 10 |
| limiter.snapshotExportsPerAction | Per action limit of concurrent volume export operations | 3 |
| limiter.snapshotExportsPerCluster | Cluster-wide limit of concurrent volume export operations | 10 |
| limiter.genericVolumeBackupsPerCluster | Cluster-wide limit of concurrent Generic Volume Backup operations | 10 |
| limiter.imageCopiesPerCluster | Cluster-wide limit of concurrent ImageStream container image backup (i.e. copy from) and restore (i.e. copy to) operations | 10 |
| limiter.workloadRestoresPerAction | Per action limit of concurrent manifest data restores, based on workload (ex. Namespace, Deployment, StatefulSet, VirtualMachine) | 3 |
| limiter.csiSnapshotRestoresPerAction | Per action limit of concurrent CSI volume provisioning requests when restoring from VolumeSnapshots | 3 |
| limiter.volumeRestoresPerAction | Per action limit of concurrent volume restore operations from an exported backup | 3 |
| limiter.volumeRestoresPerCluster | Cluster-wide limit of concurrent volume restore operations from exported backups | 10 |
| cluster.domainName | Specifies the domain name of the cluster | "" |
| timeout.blueprintBackup | Specifies the timeout (in minutes) for Blueprint backup actions | 45 |
| timeout.blueprintRestore | Specifies the timeout (in minutes) for Blueprint restore actions | 600 |
| timeout.blueprintDelete | Specifies the timeout (in minutes) for Blueprint delete actions | 45 |
| timeout.blueprintHooks | Specifies the timeout (in minutes) for Blueprint backupPrehook and backupPosthook actions | 20 |
| timeout.checkRepoPodReady | Specifies the timeout (in minutes) for temporary worker Pods used to validate backup repository existence | 20 |
| timeout.statsPodReady | Specifies the timeout (in minutes) for temporary worker Pods used to collect repository statistics | 20 |
| timeout.efsRestorePodReady | Specifies the timeout (in minutes) for temporary worker Pods used for shareable volume restore operations | 45 |
| timeout.workerPodReady | Specifies the timeout (in minutes) for all other temporary worker Pods used during Veeam Kasten operations | 15 |
| timeout.jobWait | Specifies the timeout (in minutes) for completing execution of any child job, after which the parent job will be canceled. If no value is set, a default of 10 hours will be used | None |
| awsConfig.assumeRoleDuration | Duration of a session token generated by AWS for an IAM role. The minimum value is 15 minutes and the maximum value is the maximum duration setting for that IAM role. For documentation about how to view and edit the maximum session duration for an IAM role seehttps://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html#id_roles_use_view-role-max-session. The value accepts a number along with a single characterm(for minutes) orh(for hours) Examples: 60m or 2h | '' |
| awsConfig.efsBackupVaultName | Specifies the AWS EFS backup vault name | k10vault |
| vmWare.taskTimeoutMin | Specifies the timeout for VMWare operations | 60 |
| encryption.primaryKey.awsCmkKeyId | Specifies the AWS CMK key ID for encrypting K10 Primary Key | None |
| garbagecollector.daemonPeriod | Sets garbage collection period (in seconds) | 21600 |
| garbagecollector.keepMaxActions | Sets maximum actions to keep | 1000 |
| garbagecollector.actions.enabled | Enables action collectors | false |
| kubeVirtVMs.snapshot.unfreezeTimeout | Defines the time duration within which the VMs must be unfrozen while backing them up. To know more about formatgo doccan be followed | 5m |
| excludedApps | Specifies a list of applications to be excluded from the dashboard & compliance considerations. Format should be a :ref:YAML array<k10_compliance> | ["kube-system", "kube-ingress", "kube-node-lease", "kube-public", "kube-rook-ceph"] |
| workerPodMetricSidecar.enabled | Enables a sidecar container for temporary worker Pods used to push Pod performance metrics to Prometheus | true |
| workerPodMetricSidecar.metricLifetime | Specifies the period after which metrics for an individual worker Pod are removed from Prometheus | 2m |
| workerPodMetricSidecar.pushGatewayInterval | Specifies the frequency for pushing metrics into Prometheus | 30s |
| workerPodMetricSidecar.resources.[requests\|limits].[cpu\|memory] | Specifies resource requests and limits for the temporary worker Pod metric sidecar | {} |
| forceRootInBlueprintActions | Forces any Pod created by a Blueprint to run as root user | true |
| defaultPriorityClassName | Specifies the defaultpriority classname for all K10 deployments and ephemeral Pods | None |
| priorityClassName.<deploymentName> | Overrides the defaultpriority classname for the specified deployment | {} |
| ephemeralPVCOverhead | Set the percentage increase for the ephemeral Persistent Volume Claim's storage request, e.g. PVC size = (file raw size) * (1 +ephemeralPVCOverhead) | 0.1 |
| datastore.parallelUploads | Specifies how many files can be uploaded in parallel to the data store | 8 |
| datastore.parallelDownloads | Specifies how many files can be downloaded in parallel from the data store | 8 |
| datastore.parallelBlockUploads | Specifies how many blocks can be uploaded in parallel to the data store | 8 |
| datastore.parallelBlockDownloads | Specifies how many blocks can be downloaded in parallel from the data store | 8 |
| kastenDisasterRecovery.quickMode.enabled | Enables K10 Quick Disaster Recovery | false |
| fips.enabled | Specifies whether K10 should be run in the FIPS mode of operation | false |
| workerPodCRDs.enabled | Specifies whether K10 should useActionPodSpecfor granular resource control of worker Pods | false |
| workerPodCRDs.resourcesRequests.maxCPU | Max CPU which might be setup inActionPodSpec | '' |
| workerPodCRDs.resourcesRequests.maxMemory | Max memory which might be setup inActionPodSpec | '' |
| workerPodCRDs.defaultActionPodSpec.name | The name ofActionPodSpecthat will be used by default for worker Pod resources. | '' |
| workerPodCRDs.defaultActionPodSpec.namespace | The namespace ofActionPodSpecthat will be used by default for worker Pod resources. | '' |
| vap.kastenPolicyPermissions.enabled | Enable installation of the ValidatingAdmissionPolicy to evaluate non-admin user permissions while creating a Kasten policy. | false |

## Helm Configuration for Parallel Upload to the Storage Repository â

Veeam Kasten provides an option to manage parallelism for file mode uploads to the storage repository through a configurable parameter, datastore.parallelUploads via Helm. To upload N files in parallel to the
  storage repository, configure this flag to N. This flag is adjusted
  when dealing with larger PVCs to improve performance. By default, the
  value is set to 8.

A similar option called datastore.parallelBlockUploads is used to control
  how many blocks can be uploaded concurrently when exporting a snapshot in block mode .
  Adjusting this value may be necessary to decrease the upload time for larger
  PVCs but comes at a cost of additional memory utilization in the ephemeral
  Pod launched for the operation.
  By default, the value is set to 8.

These parameters should not be modified unless instructed by the support
    team.

## Helm Configuration for Parallel Download from the Storage Repository â

Veeam Kasten provides an option to manage parallelism for file mode downloads from the storage repository through a configurable parameter, datastore.parallelDownloads via Helm. To download N files in parallel from
  the storage repository, configure this flag to N. This flag is
  adjusted when dealing with larger PVCs to improve performance. By
  default, the value is set to 8.

A similar option called datastore.parallelBlockDownloads is used to
  control how many blocks can be downloaded concurrently when restoring from a
  snapshot exported in block mode .
  Adjusting this value may be necessary to decrease the restore time for larger
  PVCs but comes at a cost of additional memory utilization in the ephemeral
  Pod launched for the operation.
  By default, the value is set to 8.

## Setting Custom Labels and Annotations on Veeam Kasten Pods â

Veeam Kasten provides the ability to apply labels and annotations to all
  of its pods. This applies to both core pods and all temporary worker
  pods created as a result of Veeam Kasten operations. Labels and
  annotations are applied using the global.podLabels and global.podAnnotations Helm flags, respectively. For example, if using
  a values.yaml file:

```
global: podLabels:   app.kubernetes.io/component: "database"   topology.kubernetes.io/region: "us-east-1" podAnnotations:   config.kubernetes.io/local-config: "true"   kubernetes.io/description: "Description"
```

Alternatively, the Helm parameters can be configured using the --set flag:

```
--set global.podLabels.labelKey1=value1 --set global.podLabels.labelKey2=value2 \--set global.podAnnotations.annotationKey1="Example annotation" --set global.podAnnotations.annotationKey2=value2
```

Labels and annotations passed using these Helm parameters
    ( global.podLabels and global.podAnnotations ) apply to the Prometheus pods as well, if it is managed by Veeam
    Kasten. However, if labels and annotations are set in the Prometheus sub-chart, they will be prioritized over the global pod labels
    and annotations set.

---

## Install Aws Aws Permissions

## Using Veeam Kasten with AWS EBS â

The following permissions are needed by Kasten to operate on EBS, AWS
  EC2's underlying block storage solution

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "ec2:CopySnapshot",                "ec2:CreateSnapshot",                "ec2:CreateTags",                "ec2:CreateVolume",                "ec2:DeleteTags",                "ec2:DeleteVolume",                "ec2:DescribeSnapshotAttribute",                "ec2:ModifySnapshotAttribute",                "ec2:DescribeAvailabilityZones",                "ec2:DescribeRegions",                "ec2:DescribeSnapshots",                "ec2:DescribeTags",                "ec2:DescribeVolumeAttribute",                "ec2:DescribeVolumesModifications",                "ec2:DescribeVolumeStatus",                "ec2:DescribeVolumes"            ],            "Resource": "*"        },        {            "Effect": "Allow",            "Action": "ec2:DeleteSnapshot",            "Resource": "*",            "Condition": {                "StringLike": {                    "ec2:ResourceTag/name": "kasten__snapshot*"                }            }        },        {            "Effect": "Allow",            "Action": "ec2:DeleteSnapshot",            "Resource": "*",            "Condition": {                "StringLike": {                    "ec2:ResourceTag/Name": "Kasten: Snapshot*"                }            }        }    ]}
```

The following additional permissions are required to use the EBS Direct
API to get changed block data in a Block Mode Export .

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "ebs:ListSnapshotBlocks",                "ebs:ListChangedBlocks",                "ebs:GetSnapshotBlock"            ],            "Resource": "arn:aws:ec2:*::snapshot/*"        }    ]}
```

## Using Veeam Kasten with AWS S3 â

While Veeam Kasten can use AWS S3 to migrate applications between
  different clusters or even clouds, the access permissions should not be
  specified as a part of the Veeam Kasten install, but instead later as a
  part of creating Location profiles . The credentials used for the profile should have the
  following permissions on the needed buckets.

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "s3:PutObject",                "s3:GetObject",                "s3:PutBucketPolicy",                "s3:ListBucket",                "s3:DeleteObject",                "s3:DeleteBucketPolicy",                "s3:GetBucketLocation",                "s3:GetBucketPolicy"            ],            "Resource": [                "arn:aws:s3:::${BUCKET_NAME}",                "arn:aws:s3:::${BUCKET_NAME}/*"            ]        }    ]}
```

Additional permissions are needed for the creation and maintenance of immutable backups in Veeam
  Kasten.

- s3:ListBucketVersions
- s3:GetObjectRetention
- s3:PutObjectRetention
- s3:GetBucketObjectLockConfiguration
- s3:GetBucketVersioning
- s3:GetObjectVersion
- s3:DeleteObjectVersion

## Using Veeam Kasten with Amazon RDS â

The credentials specified as a part of creating Location profiles should
  have the following permissions for Veeam Kasten to perform Amazon RDS
  operations.

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "rds:CreateDBInstance",                "rds:DeleteDBInstance",                "rds:DescribeDBInstances",                "rds:CreateDBSnapshot",                "rds:DeleteDBSnapshot",                "rds:DescribeDBSnapshots",                "rds:DescribeDBSnapshotAttributes",                "rds:CreateDBCluster",                "rds:DescribeDBClusters",                "rds:DeleteDBCluster",                                 "rds:CreateDBClusterSnapshot",                "rds:DeleteDBClusterSnapshot",                "rds:DescribeDBClusterSnapshots",                "rds:DescribeDBClusterSnapshotAttributes",                "rds:RestoreDBInstanceFromDBSnapshot",                "rds:RestoreDBClusterFromSnapshot"            ],            "Resource": "*"        }    ]}
```

## Using Veeam Kasten with AWS EFS â

Veeam Kasten assumes that the user has successfully provisioned an EFS
  volume and is using the EFS CSI
driver to mount
  the volume within Kubernetes. While Veeam Kasten will transparently work
  with this setup, there are a couple of things to be aware of when using
  Veeam Kasten to back up EFS that is different from EBS.

- Veeam Kasten creates its own vault to back up EFS.
- EFS volumes are created externally and today require manual cleanup when all references to them from Kubernetes are gone. This also means that when a restore happens, a manual cleanup of the old volumes will be needed.
- Unlike EBS, EFS backups can be slow because of the underlying AWS performance constraints with different data sets. Backup policy action frequencies should be set to accommodate this performance difference.

Finally, to operate on AWS EFS, Veeam Kasten will need the following
  permissions to perform backups and restores.

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "backup:CreateBackupVault",                "backup:DeleteRecoveryPoint",                "backup:DescribeBackupJob",                "backup:DescribeRecoveryPoint",                "backup:DescribeRestoreJob",                "backup:GetRecoveryPointRestoreMetadata",                "backup:ListRecoveryPointsByBackupVault",                "backup:ListRecoveryPointsByResource",                "backup:ListTags",                "backup:StartBackupJob",                "backup:StartRestoreJob",                "backup:TagResource",                "elasticfilesystem:CreateFileSystem",                "elasticfilesystem:CreateMountTarget",                "elasticfilesystem:CreateTags",                "elasticfilesystem:DeleteFileSystem",                "elasticfilesystem:DeleteMountTarget",                "elasticfilesystem:DescribeFileSystems",                "elasticfilesystem:DescribeMountTargets",                "elasticfilesystem:DescribeMountTargetSecurityGroups",                "elasticfilesystem:DescribeTags",                "elasticfilesystem:TagResource",                "sts:GetCallerIdentity"            ],            "Resource": [                "*"            ]        },        {            "Effect": "Allow",            "Action": [                "iam:PassRole"            ],            "Resource": [                "arn:aws:iam::<accountID>:role/aws-service-role/elasticfilesystem.amazonaws.com/AWSServiceRoleForAmazonElasticFileSystem",                "arn:aws:iam::<accountID>:role/service-role/AWSBackupDefaultServiceRole"            ]        }    ]}
```

## Using Veeam Kasten with AWS Secrets Manager â

When enabling Veeam Kasten DR using AWS Secrets Manager, it is required
  that an AWS Infrastructure Profile is created prior with credentials that have the adequate
  permissions.

```
{  "Version": "2012-10-17",  "Statement": [    {      "Effect": "Allow",      "Principal": {        "AWS": "arn:aws:iam::AccountId:role/EC2RoleToAccessSecrets"      },      "Action": "secretsmanager:GetSecretValue",      "Resource": "*"    }  ]}
```

More policy examples for secrets in AWS Secrets Manager are documented
here .

## Optional KMS Permissions â

When operating on Encrypted EBS volumes, Veeam Kasten will ensure
  snapshots and any new volumes created from those snapshots are encrypted
  with the same key.

If Customer Managed Keys (CMKs) are used to encrypt the EBS volumes, the
  following permissions should be granted for all KMS keys.

```
{  "Version": "2012-10-17",  "Statement": [      {        "Effect": "Allow",        "Action": [            "kms:GenerateDataKeyWithoutPlaintext",            "kms:DescribeKey",            "kms:ReEncryptTo",            "kms:ReEncryptFrom"        ],        "Resource": "arn:aws:kms:::key/${KMS_KEY_ID}"      }  ]}
```

---

## Install Aws Using Aws Iam Roles

AWS IAM
Roles allow delegating access to AWS resources to a trusted entity (e.g., an
  AWS user or a Kubernetes Service Account). Veeam Kasten can be
  configured to access AWS infrastructure using an IAM Role.

To use a role with Veeam Kasten, an IAM Policy that describes the
  permissions the role will grant needs to be created first. Second, a
  role with this policy attached needs to be created. Finally, the trusted
  entities (IAM User or Kubernetes Service Account) that can assume that
  role need to be configured.

## Creating an IAM Policy â

An IAM Policy specifies permissions the role will grant. The set of
  permissions needed by Veeam Kasten for integrating against different AWS
  services are described here .

The example below is a policy definition that grants permissions
  required to snapshot and restore EBS volumes and migrate them across
  Kubernetes clusters.

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "ec2:CopySnapshot",                "ec2:CreateSnapshot",                "ec2:CreateTags",                "ec2:CreateVolume",                "ec2:DeleteTags",                "ec2:DeleteVolume",                "ec2:DescribeSnapshotAttribute",                "ec2:ModifySnapshotAttribute",                "ec2:DescribeAvailabilityZones",                "ec2:DescribeRegions",                "ec2:DescribeSnapshots",                "ec2:DescribeTags",                "ec2:DescribeVolumeAttribute",                "ec2:DescribeVolumesModifications",                "ec2:DescribeVolumeStatus",                "ec2:DescribeVolumes"            ],            "Resource": "*"        },        {            "Effect": "Allow",            "Action": "ec2:DeleteSnapshot",            "Resource": "*",            "Condition": {                "StringLike": {                    "ec2:ResourceTag/name": "kasten__snapshot*"                }            }        },        {            "Effect": "Allow",            "Action": "ec2:DeleteSnapshot",            "Resource": "*",            "Condition": {                "StringLike": {                    "ec2:ResourceTag/Name": "Kasten: Snapshot*"                }            }        },        {            "Effect": "Allow",            "Action": [                "s3:CreateBucket",                "s3:PutObject",                "s3:GetObject",                "s3:PutBucketPolicy",                "s3:ListBucket",                "s3:DeleteObject",                "s3:DeleteBucketPolicy",                "s3:GetBucketLocation",                "s3:GetBucketPolicy"            ],            "Resource": "*"        }    ]}
```

To enable AWS KMS encryption additional policies are required. Refer to Configuring Veeam Kasten encryption for more information.

## Veeam Kasten Installs with IAM Roles â

### Option I: Using IAM Role With a Kubernetes Service Account (EKS) â

#### Enabling OIDC on your EKS Cluster â

Supporting IAM Roles with Kubernetes Service Accounts (SAs) requires the
  IAM Roles for Service Accounts feature that is available for AWS EKS
  clusters. Refer to Enabling IAM Roles for Service Accounts on your
Cluster for complete instructions to enable this feature. If you have eksctl available, you can run:

```
$ eksctl utils associate-iam-oidc-provider --cluster ${EKS_CLUSTER_NAME} --approve
```

#### Creating an IAM Role for Veeam Kasten Install â

To create an IAM Role that delegates permissions to a Kubernetes Service
  Account, see the AWS documentation on Creating an IAM Role and Policy
for your Service
Account .
  Use kasten-io (or the namespace you installed Veeam Kasten in) for the SERVICE_ACCOUNT_NAMESPACE and k10-k10 for the SERVICE_ACCOUNT_NAME in the instructions.

Veeam Kasten can now be installed using the helm command below. No
  credentials are required. EKS will inject the credentials into Veeam
  Kasten's pods.

```
$ helm install k10 kasten/k10 -n kasten-io --create-namespace    --set serviceAccount.create=false --set serviceAccount.name=my-service-account
```

my-service-account refers to the Kubernetes Service Account created in
    the previous steps, as per the AWS documentation on Creating an IAM
Role and Policy for your Service
Account .

### Option II: Using an IAM Role With an IAM User â

To create an IAM Role that delegates permissions to an IAM User, see the
  AWS documentation on Creating a Role to Delegate Permissions to an IAM
User .

Once the IAM Role is created, the IAM User must also be granted
    permissions to assume the role programmatically. For more information
    about this step, see Granting a User Permissions to Switch
Roles .

Once the AWS IAM Role is created, configure Veeam Kasten with the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for the IAM User along
  with the AWS ARN of the role.

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set secrets.awsAccessKeyId="${AWS_ACCESS_KEY_ID}" \    --set secrets.awsSecretAccessKey="${AWS_SECRET_ACCESS_KEY}" \    --set secrets.awsIamRole="${AWS_IAM_ROLE_ARN}"
```

---

## Install Azure Azure

## Prerequisites â

Before installing Veeam Kasten on Azure Kubernetes Service (AKS), please
  ensure that the install prerequisites are met.

## Installing Veeam Kasten â

Veeam Kasten supports multiple options to authenticate with Microsoft
  Entra ID (formerly Azure Active Directory), including Azure Service
  Principal, Azure Managed Identity with a specific Client ID, and Azure
  Managed Identity with the default ID. Please select one of these options
  if you wish to provide Azure credentials through helm . If multiple
  credential sets are provided, the installation will fail.

### Installing Veeam Kasten with Service Principal â

To install on Azure with Service Principal, you need to specify Client
  Secret credentials including your Azure tenant, service principal client
  ID and service principal client secret.

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set secrets.azureTenantId=<tenantID> \    --set secrets.azureClientId=<azureclient_id> \    --set secrets.azureClientSecret=<azureclientsecret>
```

### Installing Veeam Kasten on Azure Stack with Service Principal â

To install on Azure Stack, you need to specify your -

- Azure tenant: the Azure Stack tenant ID (you'll find it in [global azure portal > Azure Directory > Properties])
- Service principal client ID: client ID of the app that was used to create the Kubernetes cluster (you'll find it in [global azure portal > Azure Directory > App registration])
- Service principal client secret: client-secret of the app that was used to create the Kubernetes cluster (you'll find it in [global azure portal > Azure Directory > App registration > Certificate and secrets])
- Azure Resource Group: name of the Resource Group that was created for the Kubernetes cluster
- Azure subscription ID: a valid subscription in your Azure Stack tenant (if your az client has its default cloud set to your Azure Stack instance, you can obtain the first subscription ID with az account list | jq '.[0].id' )
- Azure Resource Manager endpoint: the resource management endpoint for this Azure Stack instance (if your az client has its default cloud set to your Azure Stack instance, you can obtain it with az cloud show | jq '.endpoints.resourceManager' . e.g., https://management.ppe5.example.com )
- Active Directory endpoint: the active directory login endpoint (if your az client has its default cloud set to your Azure Stack instance, you can obtain it with az cloud show | jq '.endpoints.activeDirectory' . e.g., https://login.microsoftonline.com/ )
- Active Directory resource ID: the resource ID to obtain AD tokens (if your az client has its default cloud set to your Azure Stack instance, you can obtain it with az cloud show | jq '.endpoints.activeDirectoryResourceId . e.g., https://management.example.com/71fb132f-xxxx-4e60-yyyy-example47e19 )

You can find more information for creating a Kubernetes cluster on Azure
  Stack in this Microsoft
tutorial

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set secrets.azureTenantId=<tenantID> \    --set secrets.azureClientId=<azureclientID> \    --set secrets.azureClientSecret=<azureclientsecret> \    --set secrets.azureResourceGroup=<resourceGroup> \    --set secrets.azureSubscriptionID=<subscriptionID> \    --set secrets.azureResourceMgrEndpoint=<resourceManagerEndpoint> \    --set secrets.azureADEndpoint=<activeDirectoryEndpoint> \    --set secrets.azureADResourceID=<activeDirectoryResourceID> \    --set services.dashboardbff.hostNetwork=true
```

#### Existing Secret Usage â

It is possible to use an existing secret to provide the following
  parameters for Azure configuration:

- Azure tenant Field name - azure_tenant_id
- Service principal client ID Field name - azure_client_id
- Service principal client secret Field name - azure_client_secret

Azure tenant

Field name - azure_tenant_id

Service principal client ID

Field name - azure_client_id

Service principal client secret

Field name - azure_client_secret

To do so, the following Helm option can be used:

```
--set secrets.azureClientSecretName=<secret name>
```

Please ensure that the secret exists in the namespace where Veeam Kasten
    is installed. The default namespace assumed throughout this
    documentation is kasten-io .

```
apiVersion: v1kind: Secretmetadata:  name: my-azure-creds  namespace: kasten-iodata:  azure_client_id: MjMzODAyNWMEXAMPLEID  azure_client_secret: UlVMOFF+dnpwM1EXAMPLESECRET  azure_tenant_id: YmEwN2JhEXAMPLETENANTIDtype: Opaque
```

### Installing Veeam Kasten with Managed Identity â

Before installing Veeam Kasten with Azure Managed Identity, you need to
  ensure that Managed
Identity is enabled on your cluster. Please note that Veeam Kasten supports only
  single-identity nodes at the moment.

When installing Veeam Kasten with Managed Identity, you have an option
  of installing with a specific Client ID, or to use the default
ID .

To install on Azure using a specific client ID, you need to specify the
  client ID.

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set secrets.azureClientId=<azureclient_id> \
```

To install on Azure using the default Managed Identity, you need to set azure.useDefaultMSI to true.

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set azure.useDefaultMSI=true \
```

### Installing Veeam Kasten on Azure US Government Cloud (...and others) â

To install Veeam Kasten on Microsoft Azure US Government cloud, make
  sure to set the following helm options:

```
--set secrets.azureCloudEnvID=AzureUSGovernmentCloud
```

This will ensure that Veeam Kasten points to appropriate endpoints.
  These options can also be used to specify other clouds like AzureChinaCloud .

## Validating the Install â

To validate that Veeam Kasten has been installed properly, the following
  command can be run in Veeam Kasten's namespace (the install default is kasten-io ) to watch for the status of all Veeam Kasten pods:

```
$ kubectl get pods --namespace kasten-io --watch
```

It may take a couple of minutes for all pods to come up but all pods
  should ultimately display the status of Running .

```
$ kubectl get pods --namespace kasten-ioNAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGEkasten-io     aggregatedapis-svc-b45d98bb5-w54pr      1/1     Running   0          1m26skasten-io     auth-svc-8549fc9c59-9c9fb               1/1     Running   0          1m26skasten-io     catalog-svc-f64666fdf-5t5tv             2/2     Running   0          1m26s...
```

In the unlikely scenario that pods that are stuck in any other state,
  please follow the support documentation to debug further.

### Validate Dashboard Access â

By default, the Veeam Kasten dashboard will not be exposed externally.
  To establish a connection to it, use the following kubectl command to
  forward a local port to the Veeam Kasten ingress port:

```
$ kubectl --namespace kasten-io port-forward service/gateway 8080:80
```

The Veeam Kasten dashboard will be available at http://127.0.0.1:8080/k10/#/ .

For a complete list of options for accessing the Kasten Veeam Kasten
  dashboard through a LoadBalancer, Ingress or OpenShift Route you can use
  the instructions here .

---

## Install Configure

Veeam Kasten supports encryption for data and metadata stored in an
  object store or an NFS/SMB file store (e.g., for cross-cloud snapshot
  migration) via the use of the AES-256-GCM encryption algorithm. Veeam
  Kasten encryption is always enabled for external data and metadata
  (more information below), it cannot be disabled.

To maintain the security of the primary encryption key, Passkeys are used
  to perform envelope encryption. By default, Kasten will create a
  passphrase-based Passkey. Users can configure multiple passkeys,
  even from different key management stores, to facilitate key rotation
  and enhance security by reducing the risk of key compromise. Users may
  delete passkeys as long as at least one valid passkey remains. This
  approach ensures flexible key management with uninterrupted access to
  backup data.

A Passkey API resource is used to add, edit, list or remove a Passkey
  used for data and metadata encryption.

## Bootstrapping Passkeys Before Install â

If you do not specify a cluster secret, a Passkey with a random
  passphrase will be generated by Veeam Kasten during install. The
  randomly generated Passkey can be changed via the Changing
Passkeys instructions.
  However, if the passphrase needs to be specified before install, it can
  be done via the creation of a Kubernetes secret with a well-known name
  ( k10-cluster-passphrase ) in the namespace you will install Veeam
  Kasten in (default kasten-io ):

Once the cluster secret is set or auto-generated, do not modify or
    delete the cluster secret directly, please follow the Passkey change
    workflow below.

### Passphrases â

A passphrase is used to protect the encryption key used by Veeam Kasten
  to encrypt application data.

```
$ kubectl create secret generic k10-cluster-passphrase \    --namespace kasten-io \    --from-literal passphrase=<key>
```

The Passkey passphrase should be stored separately in a secure location
    for Veeam Kasten Disaster Recovery .

### AWS Customer Managed Keys â

An AWS Customer Managed Key (CMK) can also be used to protect the
  encryption key used by Veeam Kasten to encrypt application data.

```
$ kubectl create secret generic k10-cluster-passphrase \    --namespace kasten-io \    --from-literal awscmkkeyid=arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab
```

IAM must be configured for Veeam Kasten. Refer to Using AWS IAM Roles for more information on IAM roles.

AWS keys are required while installing Veeam Kasten in order to use the
  AWS Customer Manager Key. The IAM role is an optional value to be
  configured if Veeam Kasten should assume a specific role.

```
$ helm install k10 kasten/k10 --namespace=kasten-io \    --set secrets.awsAccessKeyId="${AWS_ACCESS_KEY_ID}" \    --set secrets.awsSecretAccessKey="${AWS_SECRET_ACCESS_KEY}" \    --set secrets.awsIamRole="${AWS_IAM_ROLE_ARN}"
```

Following is the AWS policy needed for access to AWS KMS.

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "kms:Decrypt",                "kms:Encrypt"            ],            "Resource": "arn:aws:kms:::key/${KMS_KEY_ID}"        }    ]}
```

Additionally, the user/role needs to be added to the corresponding CMK
  policy as well.

```
{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Principal": {              "AWS": [                "arn:aws:iam::<AWS ACCOUNT>:role/<ROLE NAME>"              ]            },            "Action": "kms:*",            "Resource": "*"        }    ]}
```

### HashiCorp Vault Transit Secrets Engine â

- Configuring Vault Server for Kubernetes Auth

HashiCorp Vault Transit Secrets Engine can also be used to protect the
  encryption key used by Veeam Kasten to encrypt application data.

Refer to the Vault Transit Secret Engine documentation for more information on configuring the transit secret engine.

```
$ kubectl create secret generic k10-cluster-passphrase \  --namespace kasten-io \  --from-literal vaulttransitkeyname=<vault_transit_key_name> \  --from-literal vaulttransitpath=<vault_transit_path>
```

In addition to the Transit Secret Engine setup, Veeam Kasten needs to be
  authorized to access Vault. Either token or kubernetes authentication is
  supported for the Vault server.

### Token Auth â

The token should be provided via a secret.

This method will be deprecated in the future in favor of kubernetes auth

```
$ kubectl create secret generic vault-creds \     --namespace kasten-io \     --from-literal vault_token=<vault_token>
```

This may cause the token to be stored in shell history. It is
    recommended to regularly rotate the token used for accessing Vault.

When a new token is generated, the vault-creds secret should be
  updated with the new token provided below:

```
$ kubectl patch secret vault-creds \    --namespace kasten-io \    --type='json' -p='[{"op" : "replace" ,"path" : "/data/vault_token" ,"value" : "<updated_vault_token>"}]'
```

Credentials can be provided with the Helm install or upgrade command
  using the following flags.

```
--set vault.address=<vault_server_address> \--set vault.secretName=vault-creds
```

### Kubernetes Auth â

Refer to Configuring Vault Server For Kubernetes Auth prior to installing
  Veeam Kasten.

After setup is done, credentials can be provided with the Helm install
  or upgrade command using the following flags:

```
--set vault.address=<vault_server_address> \--set vault.role=<vault_role> \--set vault.serviceAccountTokenPath=<service_account_token_path>
```

vault.role is needed to authenticate via kubernetes service account
  tokens.

vault.serviceAccountTokenPath can be left blank if the service account
  path was not changed from the default of:
  /var/run/secrets/kubernetes.io/serviceaccount/token

vault.secretName can be provided to the helm install to do a
    best-effort fallback to token auth if kubernetes authentication fails.
    If not present and kubernetes authentication fails, then the primary key
    encryption will not succeed and will return an error.

## PassKey Management â

### Creating Passkeys â

A Passkey that represents a passphrase, expects a
  Kubernetes Secret to be provided which contains the passphrase. This can
  be done via the creation of a Kubernetes secret in the Veeam Kasten
  namespace:

```
$ kubectl create secret generic <secret-name> \    --namespace kasten-io \    --from-literal passphrase=<key>
```

As shown below, this secret can then be used to create a Passkey . Note that Passkeys are non-namespaced.

```
$ cat > sample-passkey.yaml <<EOFapiVersion: vault.kio.kasten.io/v1alpha1kind: Passkeymetadata:  name: passkey1spec:  secret:    ## Reference to the passkey secret    name: <secret-name>    namespace: kasten-ioEOF$ kubectl create -f sample-passkey.yamlvault.kio.kasten.io/passkey1 created
```

A Passkey can also be used to represent an AWS KMS
  Customer Managed Key(CMK). The AWS CMK key ID can be provided directly
  in the passkey.

```
$ cat > sample-passkey.yaml <<EOFapiVersion: vault.kio.kasten.io/v1alpha1kind: Passkeymetadata:  name: passkey2spec:  awscmkkeyid: arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890abEOF$ kubectl create -f sample-passkey.yamlvault.kio.kasten.io/passkey2 created
```

A Passkey can also be used to represent a HashiCorp Vault Transit
  Secrets Engine. The Vault Transit key name and mount path can be
  provided directly in the passkey, as shown below.

In addition, a vault authentication role and path to the service account
  token used for Vault's Kubernetes Authentication method can be passed
  in, vaultauthrole and vaultk8sserviceaccounttokenpath , respectively.
  This will override those values originally set via the helm install Kubernetes Auth .

If using Token Auth ,
  passing in these two values will have the effect of upgrading the
  authentication method from Token to Kubernetes. Please ensure your vault
  server is properly configured as shown in Configuring Vault Server for Kubernetes Auth before adding these to the Passkey .

```
$ cat > sample-passkey.yaml <<EOFapiVersion: vault.kio.kasten.io/v1alpha1kind: Passkeymetadata:  name: passkey3spec:  vaulttransitkeyname: my-key  vaulttransitpath: my-transit-path  vaultauthrole: my-auth-role  vaultk8sserviceaccounttokenpath: /var/run/secrets/kubernetes.io/serviceaccount/tokenEOF$ kubectl create -f sample-passkey.yamlvault.kio.kasten.io/passkey3 created
```

### Listing Passkeys â

To list all Passkeys , simply run:

```
$ kubectl get passkeys.vault.kio.kasten.ioNAME              VALIDpasskey1          truepasskey2          true
```

### Getting Passkeys â

To get a specific Passkey , run:

```
$ kubectl get passkeys.vault.kio.kasten.io passkey1NAME              VALIDpasskey1          true
```

You may see additional Passkey detail by using the -o yaml option:

```
$ kubectl get passkeys.vault.kio.kasten.io passkey1 -o yamlapiVersion: vault.kio.kasten.io/v1alpha1metadata:  name: passkey1  creationtimestamp: <creation-time>status:  valid: true  state: Added to Catalog
```

### Deleting Passkeys â

You can delete existing Passkeys if they are no longer required. If
  only a single Passkey exists, it cannot be deleted.

```
$ kubectl delete passkeys.vault.kio.kasten.io passkey1  vault.kio.kasten.io/passkey1 deleted
```

---

## Install Fips

Versions 7.5.10, 8.0.0, 8.0.1, 8.0.2, and 8.0.3 should not be used if requiring FIPS compliance.

Kasten, as of version 7.0, supports an installation option that complies
  with the Federal Information Processing Standards (FIPS) defined by the
  National Institute of Standards and Technology (NIST). This is
  especially important for organizations operating in highly regulated
  industries or government sectors. FIPS-compliant software ensures that
  cryptographic algorithms and security protocols meet strict government
  requirements, including those set by the United States Department of
  Defense (DoD). To learn more about FIPS, visit NIST's Compliance
FAQs .

Kasten in FIPS mode was designed to comply with the FIPS 140-3 standard.
  Activate this mode by using a set of Helm values specified below during
  the installation process, as explained in the accompanying document. To
  learn more about FIPS 140-3, please refer to NIST FIPS
140-3 .

## Cryptographic Modules â

Kasten uses OpenSSL for its implementation of cryptographic primitives
  and algorithms. OpenSSL is provided by Red Hat's Universal Base Images
  (UBI). This cryptographic module is currently listed as "review
  pending" by NIST's Cryptographic Module Validation
Program .

By incorporating OpenSSL, UBI, and aligning its implementation with Red
Hat
Compliance recommendations, Kasten ensures compliance of the FIPS 140-3 security
  requirements.

## FIPS Supported Kubernetes Distributions â

Kasten has been extensively tested and verified with Red Hat OpenShift,
  ensuring seamless integration between the two platforms. By using Kasten
  with Red Hat OpenShift, customers can benefit from enhanced security and
  compliance features, which are necessary for protecting critical data in
  FIPS-compliant environments.

While Kasten's FIPS mode can be activated in other environments, it may
  necessitate additional testing and configuration to ensure the
  cryptographic module's compliance. However, Kasten is continuously
  exploring opportunities to support additional Kubernetes distributions
  in the future.

## Limitations in FIPS mode â

Some Kasten features are not currently supported when FIPS is enabled:

- Prometheus
- PDF Reports
- Block mode exports and restores of supported Ceph CSI volumes do not use the Ceph API

As a workaround for dashboards please install and configure a FIPS
  compliant version of Grafana and Prometheus with Kasten.

## Installation in FIPS mode â

During initialization, Kasten generates encryption keys using the
    configured encryption algorithms.

This means FIPS algorithms must be enabled during the initial
    installation. However, some features will be unavailable (see above).

To ensure that certified cryptographic modules are utilized and
  non-compliant features are disabled, you must install Kasten with
  additional Helm values that can be found here: FIPS
values .

To install the latest version of Kasten with the latest values use the
  command below:

```
helm install k10 kasten/k10 \    --namespace=kasten-io \    --values=https://docs.kasten.io/downloads/8.0.4/fips/fips-values.yaml
```

---

## Install Generic

Generic Storage Backup must be used only in cases where migration to a
    CSI driver with snapshot support is not possible. For more details,
    refer to this page.

Applications can often be deployed using non-shared storage (e.g., local
  SSDs) or on systems where Veeam Kasten does not currently support the
  underlying storage provider. To protect data in these scenarios, Veeam
  Kasten with Kanister provides
  you with the ability to add functionality for backup, restore, and
  migration of application data with minimal modifications. This can be
  done in an efficient and transparent manner.

While a complete example is provided below, the only changes needed are
  the activation of Generic Storage Backup (GSB) on Veeam Kasten (see
  below), addition of a sidecar to your application deployment that can
  mount the application data volume, and an annotation that requests GSB.

## Activating Generic Storage Backup â

By default, the GSB feature is disabled. It can be activated by
  providing an activation token when installing Veeam Kasten via the Helm
  chart.

Existing customers can contact Kasten by Veeam Support via MyVeeam , to
  open a support case and request the activation token for GSB.

For all current prospects evaluating Veeam Kasten, we recommend reaching
  out to your local Kasten by Veeam Sales team through the local point of
  contact within the Veeam channel.

Provide the cluster ID (UUID of the default namespace) when
  requesting an activation token. This ID will help Veeam Kasten identify
  a cluster where GSB is activated. Use the following kubectl command to
  get the UUID:

```
## Extract UUID of the `default` namespace$ kubectl get namespace default -o jsonpath="{.metadata.uid}{'\n'}"
```

Once the token is obtained, provide it to Veeam Kasten with the
  following Helm option:

```
--set genericStorageBackup.token=<activation token for the cluster>
```

A separate activation token is required for every cluster where you want
    to activate GSB.

## Using Sidecars â

The sidecar can be added either by leveraging Veeam Kasten's sidecar
  injection feature or by manually patching the resource as described
  below.

### Enabling Kanister Sidecar Injection â

Veeam Kasten implements a Mutating Webhook Server which mutates workload
  objects by injecting a Kanister sidecar into the workload when the
  workload is created. The Mutating Webhook Server also adds the k10.kasten.io/forcegenericbackup annotation to the targeted workloads
  to enforce generic backup. By default, the sidecar injection feature is
  disabled. To enable this feature, the following options need to be used
  when installing Veeam Kasten via the Helm chart:

```
--set injectGenericVolumeBackupSidecar.enabled=true
```

Once enabled, Kanister sidecar injection will be enabled for all
  workloads in all namespaces. To perform sidecar injections on workloads
  only in specific namespaces, the namespaceSelector labels can be set
  using the following option:

```
--set-string injectGenericVolumeBackupSidecar.namespaceSelector.matchLabels.key=value
```

By setting namespaceSelector labels, the Kanister sidecar will be
  injected only in the workloads which will be created in the namespace
  matching labels with namespaceSelector labels.

Similarly, to inject the sidecar for only specific workloads, the objectSelector option can be set as shown below:

```
--set-string injectGenericVolumeBackupSidecar.objectSelector.matchLabels.key=value
```

It is recommended to add at least one namespaceSelector or objectSelector when enabling the injectGenericVolumeBackupSidecar feature.
    Otherwise, Veeam Kasten will try to inject a sidecar into every new
    workload. In the common case, this will lead to undesirable results and
    potential performance issues.

For example, to inject sidecars into workloads that match the label component: db and are in namespaces that are labeled with k10/injectGenericVolumeBackupSidecar: true , the following options should be added
  to the Veeam Kasten Helm install command:

```
--set injectGenericVolumeBackupSidecar.enabled=true \--set-string injectGenericVolumeBackupSidecar.objectSelector.matchLabels.component=db \--set-string injectGenericVolumeBackupSidecar.namespaceSelector.matchLabels.k10/injectGenericVolumeBackupSidecar=true
```

The labels set with namespaceSelector and objectSelector are
  mutually inclusive. This means that if both the options are set to
  perform sidecar injection, the workloads should have labels matching the objectSelector labels AND they have to be created in the
  namespace with labels that match the namespaceSelector labels. Similarly, if multiple labels are specified for either namespaceSelector or objectSelector , they will all needed to match
  for a sidecar injection to occur.

For the sidecar to choose a security context that can read data from the
  volume, Veeam Kasten performs the following checks in order:

1. If there are multiple primary containers, the list of containers will be iterated over, and the SecurityContext of the containers will be merged so that the final SecurityContext is the most restrictive one. If there is only one primary container, the final SecurityContext of the sidecar will be the SecurityContext of the primary container.
2. If the workload PodSpec has a SecurityContext set, the sidecar does not need an explicit specification and will automatically use the context from the PodSpec.
3. If the above criteria are not met, by default, no SecurityContext will be set.

The SecurityContext of the sidecar will have some additional "add"
    capabilities, and while selecting the most restrictive security context,
    some operations will be restricted. See this Veeam Kasten knowledge base article
    for more details.

When the helm option for providing a Root CA to Veeam Kasten, i.e cacertconfigmap.name , is enabled, the Mutating Webhook will create a
    new ConfigMap, if it does not already exist, in the application
    namespace to provide the Root CA to the sidecar. This ConfigMap in the
    application namespace would be a copy of the Root CA ConfigMap residing
    in the Veeam Kasten namespace.

Sidecar injection for standalone Pods is not currently supported. Refer
    to the following section to manually add the the Kanister sidecar to
    standalone Pods.

### Updating the resource manifest â

Alternatively, the Kanister sidecar can be added by updating the
  resource manifest with the Kanister sidecar. An example, where /data is used as an sample mount path, can be seen in the below specification.
  Note that the sidecar must be named kanister-sidecar and the
  sidecar image version should be pinned to the latest Kanister release.

```
- name: kanister-sidecar  image: gcr.io/kasten-images/kanister-tools:|kasten_version|  command: ["bash", "-c"]  args:  - "tail -f /dev/null"  volumeMounts:  - name: data    mountPath: /data
```

Alternatively, the below command can be run to add the sidecar into the
  workload. Make sure to specify correct values for the specified
  placeholders resource_type , namespace , resource_name , volume-name and volume-mount-path :

```
$ kubectl patch <resource_type> \    -n <namespace> \    <resource_name> \    --type='json' \    -p='[{"op": "add", "path": "/spec/template/spec/containers/0", "value": {"name": "kanister-sidecar", "image": "gcr.io/kasten-images/kanister-tools:<kasten_version>", "command": ["bash", "-c"], "args": ["tail -f /dev/null"], "volumeMounts": [{"name": "<volume-name>", "mountPath": "<volume-mount-path>"}] } }]'
```

After injecting the sidecar manually, workload pods will be recreated.
    If the deployment strategy used for the workload is RollingUpdate ,
    the workload should be scaled down and scaled up so that the volumes are
    mounted into the newly created pods.

Once the above changes are made, Veeam Kasten will be able to
  automatically extract data and, using its data engine, efficiently
  deduplicate data and transfer it into an object store or NFS/SMB file store.

If you have multiple volumes used by your pod, you simply need to mount
  them all within this sidecar container. There is no naming requirement
  on the mount path as long as they are unique.

Note that a backup operation can take up to 800 MB of memory for some
  larger workloads. To ensure the pod containing the kanister-sidecar is
  scheduled on a node with sufficient memory for a particularly intensive
  workload, you can add a resource request to the container definition.

```
resources:  requests:    memory: 800Mi
```

#### Generic Backup Annotation â

Generic backups can be requested by adding the k10.kasten.io/forcegenericbackup annotation to the workload as shown
  in the example below.

```
apiVersion: apps/v1kind: Deploymentmetadata:  name: demo-app  labels:    app: demoannotations:  k10.kasten.io/forcegenericbackup: "true"
```

The following is a kubectl example to add the annotation to a running
  deployment:

```
## Add annotation to force generic backups$ kubectl annotate deployment <deployment-name> k10.kasten.io/forcegenericbackup="true" --namespace=<namespace-name>
```

Finally, note that the Kanister sidecar and Location profile must both
  be present for generic backups to work.

#### Required Capabilities for Generic Storage Backup â

OpenShift Container Platform (OCP) introduced more restrictive default
  security context constraints (SCCs) in the 4.11 release - Pod Security
Admission .
  The change affects the ability to perform rootless Generic Storage
  Backup. Since K10 5.5.8 rootless is a default behavior for Veeam Kasten.

To use Generic Storage Backup with OCP 4.11 and above, the following
  capabilities must be allowed:

- FOWNER
- CHOWN
- DAC_OVERRIDE

Even if Veeam Kasten is installed on Kubernetes distributions other than
  OCP, the capabilities mentioned above are required for ensuring the
  proper functionality of Generic Storage Backup.

Previous version of restricted SCC can be used as a template. Change
  the allowedCapabilities field as follows:

```
allowedCapabilities:- CHOWN- DAC_OVERRIDE- FOWNER
```

## End-to-End Example â

The below section provides a complete end-to-end example of how to
  extend your application to support generic backup and restore. A dummy
  application is used below but it should be straightforward to extend
  this example.

### Prerequisites â

- Make sure you have obtained the activation token and have Veeam Kasten installed by providing the token using the genericStorageBackup.token option.
- Make sure you have installed Veeam Kasten with injectGenericVolumeBackupSidecar enabled.
- (Optional) namespaceSelector labels are set for injectGenericVolumeBackupSidecar .

injectGenericVolumeBackupSidecar can be enabled by passing the following flags
  while installing Veeam Kasten helm chart

```
...          --set injectGenericVolumeBackupSidecar.enabled=true \          --set-string injectGenericVolumeBackupSidecar.namespaceSelector.matchLabels.k10/injectGenericVolumeBackupSidecar=true ## Optional
```

### Deploy the application â

The following specification contains a complete example of how to
  exercise generic backup and restore functionality. It consists of a an
  application Deployment that use a Persistent Volume Claim (mounted
  internally at /data ) for storing data.

Saving the below specification as a file, deployment.yaml , is
  recommended for reuse later.

```
apiVersion: v1kind: PersistentVolumeClaimmetadata:  name: demo-pvc  labels:    app: demo    pvc: demospec:  accessModes:    - ReadWriteOnce  resources:    requests:      storage: 1Gi---apiVersion: apps/v1kind: Deploymentmetadata:  name: demo-app  labels:    app: demospec:  replicas: 1  selector:    matchLabels:      app: demo  template:    metadata:      labels:        app: demo    spec:      containers:      - name: demo-container        image: alpine:3.7        resources:            requests:              memory: 256Mi              cpu: 100m        command: ["tail"]        args: ["-f", "/dev/null"]        volumeMounts:        - name: data          mountPath: /data      volumes:      - name: data        persistentVolumeClaim:          claimName: demo-pvc
```

- Create a namespace: $ kubectl create namespace < namespace > If injectGenericVolumeBackupSidecar.namespaceSelector labels are set while installing Veeam Kasten, add the labels to namespace to match with namespaceSelector $ kubectl label namespace < namespace > k10/injectGenericVolumeBackupSidecar = true
- Deploy the above application as follows: ## Deploying in a specific namespace $ kubectl apply --namespace = < namespace > -f deployment.yaml
- Check status of deployed application: List pods in the namespace. The demo-app pods can be seen created with two containers. ## List pods $ kubectl get pods --namespace = < namespace > | grep demo-app ## demo-app-56667f58dc-pbqqb 2/2 Running 0 24s
- Describe the pod and verify the kanister-sidecar container is injected with the same volumeMounts . volumeMounts : - name : data mountPath : /data

Create a namespace:

```
$ kubectl create namespace <namespace>
```

If injectGenericVolumeBackupSidecar.namespaceSelector labels are set while
      installing Veeam Kasten, add the labels to namespace to match with namespaceSelector

```
$ kubectl label namespace <namespace> k10/injectGenericVolumeBackupSidecar=true
```

Deploy the above application as follows:

```
## Deploying in a specific namespace$ kubectl apply --namespace=<namespace> -f deployment.yaml
```

Check status of deployed application:

List pods in the namespace. The demo-app pods can be seen created
      with two containers.

```
## List pods$ kubectl get pods --namespace=<namespace> | grep demo-app## demo-app-56667f58dc-pbqqb   2/2     Running   0          24s
```

Describe the pod and verify the kanister-sidecar container is
      injected with the same volumeMounts .

```
volumeMounts:- name: data  mountPath: /data
```

### Create a Location Profile â

If you haven't done so already, create a Location profile with the
  appropriate Location and Credentials information from the Veeam Kasten
  settings page. Instructions for creating location profiles can be found here

Generic storage backup and restore workflows are not compatible with immutable backups location profiles . Immutable backups enabled location profiles can be used
    with these workflows, but will be treated as a non-immutability-enabled
    profile: the protection period will be ignored, and no point-in-time
    restore functionality will be provided. Please note that use of an
    object-locking bucket for such cases can amplify storage usage without
    any additional benefit.

### Insert Data â

The easiest way to insert data into the demo application is to simply
  copy it in:

```
## Get pods for the demo application from its namespace$ kubectl get pods --namespace=<namespace> | grep demo-app## Copy required data manually into the pod$ kubectl cp <file-name> <namespace>/<pod>:/data/## Verify if the data was copied successfully$ kubectl exec --namespace=<namespace> <pod> -- ls -l /data
```

### Backup Data â

Backup the application data either by creating a Policy or running a
  Manual Backup from Veeam Kasten. This assumes that the application is
  running on a system where Veeam kasten does not support the provisioned
  disks (e.g., local storage). Make sure to specify the location profile
  in the advanced settings for the policy. This is required to perform
  Kanister operations.

This policy covers an application running in the namespace sampleApp .

```
apiVersion: config.kio.kasten.io/v1alpha1kind: Policymetadata:  name: sample-custom-backup-policy  namespace: kasten-iospec:  comment: My sample custom backup policy  frequency: '@daily'  subFrequency:    minutes: [30]    hours: [22,7]    weekdays: [5]    days: [15]  retention:    daily: 14    weekly: 4    monthly: 6  actions:  - action: backup    backupParameters:      profile:        name: my-profile        namespace: kasten-io  selector:    matchLabels:      k10.kasten.io/appNamespace: sampleApp
```

For complete documentation of the Policy CR, refer to policy_api_type .

### Destroy Data â

To destroy the data manually, run the following command:

```
## Using kubectl$ kubectl exec --namespace=<namespace> <pod> -- rm -rf /data/<file-name>
```

Alternatively, the application and the PVC can be deleted and recreated.

### Restore Data â

Restore the data using Veeam Kasten by selecting the appropriate restore
  point.

### Verify Data â

After restore, you should verify that the data is intact. One way to
  verify this is to use MD5 checksum tool.

```
## MD5 on the original file copied$ md5 <file-name>## Copy the restored data back to local env$ kubectl get pods --namespace=<namespace> | grep demo-app$ kubectl cp <namespace>/<pod>:/data/<filename> <new-filename>## MD5 on the new file$ md5 <new-filename>
```

The MD5 checksums should match.

## Generic Storage Backup and Restore on Unmounted PVCs â

Generic Storage Backup and Restore on unmounted PVCs can be enabled by
  adding k10.kasten.io/forcegenericbackup annotation to the StorageClass
  with which the volumes have been provisioned.

---

## Install Google Gcp Marketplace Quick Guide

This documentation is specific to deploying and managing Veeam Kasten
  using the GCP Marketplace. For other deployment scenarios on Google
  Kubernetes Engine (GKE), please refer to the more general GKE
install instructions .

## Prerequisites â

- Ensure that the GKE node pool has Compute Engine set to Read Write , per the more general GKE install instructions
- Connect to the cluster where you intend to install Veeam Kasten via kubectl .
- Ensure that your cluster has been created with a Service Account with the required access to the underlying storage infrastructure. See Using the Default GCP Service Account for more details.
- Create a dedicated namespace where you will install Veeam Kasten. This can be accomplished during the Kasten installation wizard within the Google Cloud Marketplace or alternatively can be done ahead of time. For example, if you want to pre-create namespace kasten-io , you will run the following command.

```
$ kubectl create namespace kasten-io
```

## Install from the GCP Marketplace Console â

To deploy using the GCP Marketplace UI, follow these steps:

- From the Applications section of Google Kubernetes Engine, select Deploy from the Cloud Marketplace
- Locate Veeam Kasten from the list of applications.
- Select the Configure option.
- Select the cluster on which you would like to deploy.
- If you haven't pre-created the kasten-io namespace, select "Create Namespace" and specify kasten-io as the new namespace name.
- Leave "Create a new Veeam Kasten Service Account" selected that will have the proper permissions, or alternatively specify a pre-created service account with the required permissions
- Specify a name for the application instance. It is recommended to remove the default value and instead specify k10 . Whatever is specified as the application instance name will be the directory to which you will need to navigate via your browser. So if you specify k10 and port forward the gateway service, it will be accessible at http://127.0.0.1:8080/k10/#/
- Confirm by typing 'yes' that you are deploying in a dedicated, non-default namespace
- Leave "Reporting service account" set to "Create a new service account," or choose a pre-created service account. To pre-create a service account run the following command: gcloud iam service-accounts create k10-reporting-sa \ --project = ${myproject} \ --display-name = "Kasten Reporting Service Account" \ --description = "Service account for Kasten reporting"

From the Applications section of Google Kubernetes Engine, select Deploy from the Cloud Marketplace

Locate Veeam Kasten from the list of applications.

Select the Configure option.

Select the cluster on which you would like to deploy.

If you haven't pre-created the kasten-io namespace,
      select "Create Namespace" and specify kasten-io as the
      new namespace name.

Leave "Create a new Veeam Kasten Service Account" selected that will have the proper
      permissions, or alternatively specify a pre-created service account with the
required permissions

Specify a name for the application instance. It is recommended to remove
      the default value and instead specify k10 . Whatever is specified
      as the application instance name will be the directory to which you
      will need to navigate via your browser. So if you specify k10 and port forward the gateway service, it will be accessible at http://127.0.0.1:8080/k10/#/

Confirm by typing 'yes' that you are deploying in a dedicated,
      non-default namespace

Leave "Reporting service account" set to "Create a new service account,"
      or choose a pre-created service account. To pre-create a service account
      run the following command:

```
gcloud iam service-accounts create k10-reporting-sa \                                                                 --project=${myproject} \   --display-name="Kasten Reporting Service Account" \--description="Service account for Kasten reporting"
```

This will deploy a version of Veeam Kasten using default settings.

It is strongly recommended that you install Veeam Kasten in a dedicated
    non-default namespace on your cluster. The instructions above describe
    how to do so

## Using Veeam Kasten â

### Accessing the Veeam Kasten Dashboard â

Once Veeam Kasten has been installed, enable access to the dashboard,
  which is not exposed by default. To access the dashboard, run the
  following commands locally:

```
$ kubectl --namespace kasten-io port-forward service/gateway 8080:80
```

Assuming that you installed in namespace kasten-io and named the
  application kasten-k10 , the dashboard will be accessible at: http://127.0.0.1:8080/k10/#/

For detailed documentation on how to use Veeam Kasten once installed,
  please refer to Using Veeam Kasten .

## Updating Veeam Kasten â

When installing a new instance of Veeam Kasten on a cluster, you will
  always get the latest images corresponding to a given version. To
  upgrade to subsequent patch/minor versions, follow the instructions
  below.

Please collect Namespace and ServiceAccount settings for your Veeam
  Kasten deployment. To extract the ServiceAccount name, you can run the
  following command:

```
$ kubectl --namespace <k10-namespace> get sa --selector=app.kubernetes.io/name=<k10-application-name> -o jsonpath="{.items[*].metadata.name}"
```

Assuming that you installed in namespace kasten-io and named the
  application k10

```
$ kubectl --namespace kasten-io get sa --selector=app.kubernetes.io/name=k10 -o jsonpath="{.items[*].metadata.name}"
```

Replace [<k10-sa-name>] with your ServiceAccount and [<k10-namespace>] with Namespace in the command below.
  Then simply execute the modified command.

```
$ kubectl run -i --rm --tty updater --image=us-docker.pkg.dev/veeam-marketplace-public/veeam-kasten/k10/updater:7.5 --image-pull-policy=Always --restart=Never --overrides='{ "apiVersion": "v1",  "spec": {"serviceAccountName": "<k10-sa-name>"}}' --namespace <k10-namespace>
```

## Deleting Veeam Kasten â

### Deleting from the GCP Marketplace Console â

Select Veeam Kasten from the Applications section of the Google
  Kubernetes Engine Console, and then select Delete .

### Deleting via the Command Line â

To delete a Veeam Kasten instance that was installed using GCP
  Marketplace, simply delete all resources with the label corresponding to
  the application instance from the Veeam Kasten namespace.

```
$ kubectl delete all --namespace=<k10 namespace> --selector=app.kubernetes.io/name=<k10 instance name>
```

For example, if Veeam Kasten was installed in the namespace kasten-io and the application was named kasten-k10 , then you can delete it using
  the command.

```
$ kubectl delete all --namespace=kasten-io --selector=app.kubernetes.io/name=k10
```

If you followed best practices and installed Veeam Kasten in a dedicated
  namespace, you should be able to simply delete that namespace.

```
$ kubectl delete namespace <k10 namespace>
```

Regardless of the approach, all resources will be cleaned up unless you
  have changed the default ReclaimPolicy for PersistentVolume to something
  other than the default of delete . If that is the case, you
  will need to manually clean PVs.

---

## Install Google Google

## Prerequisites â

Before installing Veeam Kasten on Google Cloud's Google Kubernetes
  Engine (GKE), please ensure that the install
prerequisites are met.

For a default GKE install, a volumesnapshotclass will need to be
    created and annotated with k10.kasten.io/is-snapshot-class: "true" .
    To see how to create a volumesnapshotclass, refer to this google documentation

## Installing Veeam Kasten â

Installing Veeam Kasten on Google requires two kinds of Service
  Accounts. The first, documented below, is a Google Cloud Platform (GCP)
Service Account
(SA) that grants access to underlying Google Cloud infrastructure resources
  such as storage. The second, as mentioned above in the Prerequisites
  section, is a Kubernetes Service Account that grants access to
  Kubernetes resources and will be auto-created during the helm install
  process or via Google Marketplace options.

It is advised to make sure that the necessary permissions are available
  before proceeding with the installation of Veeam Kasten. The process of
  granting permissions may vary depending on the chosen installation mode.
  It is important to follow the instructions relevant to the desired
  installation mode to ensure a smooth and successful installation of
  Veeam Kasten.

### GCP Service Account Configuration â

Veeam Kasten uses the Google Cloud Platform Service Account to
  manage volumesnapshot in the GCP account. Therefore, the service
  account needs to be assigned the compute.storageAdmin role.

#### Using the Default GCP Service Account â

A GCP Service Account automatically gets created with every GKE cluster.
  This SA can be accessed within the GKE cluster to perform actions on GCP
  resources and, if set up correctly at cluster creation time, can be the
  simplest way to run the Kasten platform.

This SA configuration needs to be done at cluster creation time. When
  using the Google Cloud Console to create a new Kubernetes cluster,
  please select More Options for every node pool you have added.
  Search for Security in the expanded list of options and, under Access
Scopes , select Set access for each API . In the list of scopes that
  show up, please ensure that Compute Engine is set to Read Write .

#### Using a Separate GCP Service Account â

The preferred option for a Veeam Kasten install is to create and use a
  separate Google service account with the appropriate permissions to
  operate on the underlying Google Cloud infrastructure and then use that.
  For more details on how to create and use a separate service account,
  refer to the following links:

- Creating a New Service Account
- Installing Veeam Kasten with the new Service Account Using a Custom Project ID Existing Secret Usage

- Using a Custom Project ID
- Existing Secret Usage

For information on adding the compute.storageAdmin role to a Google
  Cloud Platform Service Account for the associated GCP project, refer to
  this link .

Service Account Key

Veeam Kasten requires a Service Account key for the GCP Service Account
  and the GCP Project ID associated with it.

#### Service Accounts for a Marketplace Install â

If you are installing on Google via the Google
Marketplace ,
  you can elect to allow the marketplace install create a K10 service account
  as well as a reporting service account, although your user may require
  administrative privileges in IAM to do so. Alternatively, you can
  pre-create the service accounts by following these
instructions to install.

Once the Service Accounts are created and the node pools are running,
  Veeam Kasten can then be installed by running the following install
  command:

```
$ helm install k10 kasten/k10 --namespace=kasten-io
```

To address any troubleshooting issues while installing Veeam Kasten on a
    Kubernetes platform using the Cilium Container Network Interface (CNI)
    setup, refer to this page . The page
    provides specific steps for resolving installation issues with Cilium
    CNI and Veeam Kasten compatibility.

## Validating the Install â

To validate that Veeam Kasten has been installed properly, the following
  command can be run in Veeam Kasten's namespace (the install default is kasten-io ) to watch for the status of all Veeam Kasten pods:

```
$ kubectl get pods --namespace kasten-io --watch
```

It may take a couple of minutes for all pods to come up but all pods
  should ultimately display the status of Running .

```
$ kubectl get pods --namespace kasten-ioNAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGEkasten-io     aggregatedapis-svc-b45d98bb5-w54pr      1/1     Running   0          1m26skasten-io     auth-svc-8549fc9c59-9c9fb               1/1     Running   0          1m26skasten-io     catalog-svc-f64666fdf-5t5tv             2/2     Running   0          1m26s...
```

In the unlikely scenario that pods that are stuck in any other state,
  please follow the support documentation to debug further.

### Validate Dashboard Access â

By default, the Veeam Kasten dashboard will not be exposed externally.
  To establish a connection to it, use the following kubectl command to
  forward a local port to the Veeam Kasten ingress port:

```
$ kubectl --namespace kasten-io port-forward service/gateway 8080:80
```

The Veeam Kasten dashboard will be available at http://127.0.0.1:8080/k10/#/ .

For a complete list of options for accessing the Kasten Veeam Kasten
  dashboard through a LoadBalancer, Ingress or OpenShift Route you can use
  the instructions here .

---

## Install Google Service Account Install

Veeam Kasten requires a newly created service account to contain the
  following roles:

```
roles/compute.storageAdmin
```

Currently, the Google Service Account key needs to be created in the
    same GCP account as the GKE cluster.

The following steps should be used to create the service account and add
  the required permissions:

```
$ myproject=$(gcloud config get-value core/project)$ gcloud iam service-accounts create k10-test-sa --display-name "K10 Service Account"$ k10saemail=$(gcloud iam service-accounts list --filter "k10-test-sa" --format="value(email)")$ gcloud iam service-accounts keys create --iam-account=${k10saemail} k10-sa-key.json$ gcloud projects add-iam-policy-binding ${myproject} --member serviceAccount:${k10saemail} --role roles/compute.storageAdmin
```

## Installing Veeam Kasten with the new Service Account â

Use the base64 tool to encode the k10-sa-key.json file generated
  above, and then install Veeam Kasten with the newly created credentials.

```
$ sa_key=$(base64 -w0 k10-sa-key.json)$ helm install k10 kasten/k10 --namespace=kasten-io --set secrets.googleApiKey=$sa_key
```

### Using a Custom Project ID â

If the Google Service Account belongs to a project other than the one in
  which the cluster is located, then the project's ID for the cluster
  must also be provided during the installation.

```
$ sa_key=$(base64 -w0 k10-sa-key.json)$ helm install k10 kasten/k10 \      --namespace=kasten-io \      --set secrets.googleApiKey=$sa_key \      --set secrets.googleProjectId=<project-id>
```

### Existing Secret Usage â

It is possible to use an existing secret to provide Service Account and
  Project ID.

To do so, the following Helm option can be used:

```
--set secrets.googleClientSecretName=<secret name>
```

Please ensure that the secret exists in the namespace where Veeam Kasten
    is installed. The default namespace assumed throughout this
    documentation is kasten-io .

```
apiVersion: v1kind: Secretmetadata:  name: my-google-creds  namespace: kasten-iodata:  google-api-key: MjMzODAyNWMEXAMPLEAPIKEY  google-project-id: UlVMOFF+dnpwM1EXAMPLEPROJECTIDtype: Opaque
```

---

## Install Gvs Restricted

Generic Storage Backup (GSB) is a feature developed by Kasten to provide backup capabilities
  for Kubernetes applications with persistent volumes using a storage
  provisioner that lacks snapshot capabilities. While this feature
  provided flexibility in the early stages of Kubernetes storage, it comes
  with certain limitations. GSB essentially copies the live filesystem of
  a persistent volume, and any changes occurring to that filesystem during
  the file copy operation can lead to inconsistent backup data. This
  inconsistency could potentially result in unexpected behavior when
  restoring applications using a GSB backup.

Unlike GSB, storage snapshots allow for the creation of crash-consistent
  and data-consistent backups. The general availability of VolumeSnapshot
  APIs for Container Storage Interface (CSI) drivers allowed storage
  vendors to integrate their snapshot and cloning capabilities using a
  standardized interface. Since 2018, the list of production-ready CSI
drivers has grown
  to over 100, with the majority now supporting VolumeSnapshots. Given the
  increasing availability and adoption of snapshot-capable CSI drivers,
  the utility of GSB has become limited.

It is highly recommended for existing customers to migrate to a CSI
  driver with snapshot and clone capabilities based on their storage
  requirements. In rare cases where migration to a CSI driver is not
  possible, existing customers can contact Kasten by Veeam Support via MyVeeam , to
  open a support case and request the activation token for GSB.

For all current prospects evaluating Veeam Kasten, we recommend reaching
  out to your local Kasten by Veeam Sales team through the local point of
  contact within the Veeam channel.

---

## Install Gwif

Google Workload Identity
Federation uses service account impersonation for authentication and authorization,
  thereby avoiding the use of Google Service Account keys with extended
  lifespans. It is compatible with various identity providers such as AWS,
  Azure, or Kubernetes. An example of implementing Google Workload
  Identity Federation on an OpenShift cluster on GKE with Kubernetes as
  the identity provider can be found here .

Veeam Kasten supports the use of Google Workload Identity Federation
with Kubernetes as the Identity
Provider both during the export of applications and in Veeam Kasten DR Backup and
  Restore processes.

## Installing Veeam Kasten â

When Kubernetes is used as the Identity Provider, workloads can use the
  Kubernetes service account tokens to authenticate to Google Cloud. These
  tokens are made available to workloads through the service account
token volume
projection , which requires some additional Helm settings to be set.

To install Veeam Kasten with Google Workload Identity Federation, use
  the following commands:

```
--set google.workloadIdentityFederation.enabled=true \--set google.workloadIdentityFederation.idp.type=kubernetes \--set google.workloadIdentityFederation.idp.aud=<audience>
```

With <audience> is the Audience set up for the Workload Identity Pool.

## Creating a Location Profile with Google Workload Identity Federation â

Instructions on how to create a Location Profile with Google Workload
  Identity Federation can be found here .

## Restoring Veeam Kasten with Google Workload Identity Federation â

Veeam Kasten supports the use of Google Workload Identity Federation
with Kubernetes as the Identity
Provider during Veeam Kasten DR Backup and Restore process. For more information
  on Veeam Kasten DR Backup and Restore, please see here .

Please note that it is possible to restore Veeam Kasten with Google
  Workload Identity Federation, regardless of the authentication mechanism
  used for the Google Location Profile selected while enabling Veeam
  Kasten disaster recovery on the source cluster.

The restore process will require a Location Profile with Google Workload
  Identity Federation. Please refer back to this section for
  instructions on how to install Veeam Kasten on the target cluster with
  Google Workload Identity Federation, and the Google Cloud Storage Location Profile configuration section for instructions on how to create a Location
  Profile.

Following that, Veeam Kasten can be restored using Google Workload
  Identity Federation credentials by executing the command below:

```
## Install the helm chart that creates the restore job and wait for completion of the `k10-restore` job## Assumes that Veeam Kasten is installed in 'kasten-io' namespace.$ helm install k10-restore kasten/k10restore --namespace=kasten-io \         --set=google.workloadIdentityFederation.enabled=true \         --set=google.workloadIdentityFederation.idp.type=kubernetes \         --set=google.workloadIdentityFederation.idp.aud=<audience> \         --set sourceClusterID=<source-clusterID> \         --set profile.name=<location-profile-name>
```

<audience> is the Audience set up for the Workload Identity Pool of
  the target cluster.

<location-profile-name> is the profile on target cluster that contains
  the credential configuration file.

---

## Install Ironbank

Iron Bank, which is a crucial part of Platform One, the DevSecOps
  managed services platform for the United States (US) Department of
  Defense (DoD), acts as the central repository for all hardened images
  that have gone through the container hardening
process . It serves
  as the DoD's Centralized Artifacts Repository (DCAR), housing these
  secure images.

All images required to deploy Veeam Kasten have gone through this
  process and can be viewed in Iron Bank's catalog .

To view the catalog, registration with Platform One is necessary. If you
    do not have an account, follow the instructions by clicking the catalog
    page above to register now.

The catalog page shows the verified findings, compliance details, and
  overall risk assessment score associated with each image.

Diving into a specific image shows additional information including the
  Software Bill of Materials (SBOMs) in both SPDX and CycloneDX formats. It also provides Vulnerability Assessment Tracker (VAT)
  findings, showcasing justifications for vulnerabilities and their
  verification status.

Getting newly released versions of Veeam Kasten images through the Iron
    Bank hardening process can take some time. This may result in the
    unavailability of new releases for Iron Bank-based deployments for a few
    days following the release of standard Veeam Kasten images.

## Registry1 â

Iron Bank uses Harbor for its registry , which can be accessed using your
  Platform One credentials.

The username and password required for pulling images from Registry1 via
  the command line can be found by clicking on your profile in the upper
  right corner.

The password is the same as the CLI secret token.

Veeam Kasten images can be found by using the search bar at the top of
  the screen and searching for veeam or kasten . Clicking on an image provides more information,
  such as the tags that can be pulled and the sha256 of the image.

Images are signed by Cosign and the
  relevant information is shown for each valid image.

## Installing Veeam Kasten â

Deploying Veeam Kasten with Iron Bank hardened images is possible using
  the public Kasten Helm chart. Please ensure that the prerequisites have been
  met.

### Fetching the Helm Chart Values for Iron Bank Images â

Installing Veeam Kasten with the Iron Bank images, as
  shown below , uses a pre-configured values file
  specifically for Iron Bank. To view the file, download it by executing the
  following command substituting <VERSION> with either latest or a previous
  version of Veeam Kasten that's being installed:

```
$ curl -sO https://docs.kasten.io/downloads/8.0.4/ironbank/ironbank-values.yaml
```

This file contains the correct helm values that ensure the deployment of
  Veeam Kasten only with Iron Bank hardened images.

This file is protected and should not be modified. It is necessary to
    specify all other values using the corresponding Helm flags, such as --set , --values , etc.

### Providing Registry1 Credentials for Veeam Kasten Helm Deployment â

Since all images are pulled from Registry1 for a Veeam Kasten deployment
  using Iron Bank hardened images, your credentials must be provided
  in order to successfully pull the images.

Credentials can be provided by using either:

- --set secrets.dockerConfig=<BASE64 ENCODED DOCKERCONFIG> , or
- --set-file secrets.dockerConfigPath=<PATH TO DOCKERCONFIG>

The dockerconfig encoded in base64 can be created with
  the jq tool:

```
jq -nc \--arg registry "registry1.dso.mil" \--arg username "${REGISTRY1_USERNAME}" \--arg password "${REGISTRY1_CLI_SECRET}" \--arg auth $(printf "%s:%s" "${REGISTRY1_USERNAME}" "${REGISTRY1_CLI_SECRET}" | base64) \'{"auths":{($registry):{"username":$username,"password":$password,"auth":$auth}}}' \| base64
```

### Installing Veeam Kasten with Iron Bank Hardened Images â

To install Veeam Kasten with Iron Bank hardened images, execute the
  following command substituting <VERSION> with either latest or a previous version of
  Veeam Kasten that's being installed::

```
$ helm upgrade k10 kasten/k10 --install --namespace=kasten-io \    --values "https://docs.kasten.io/<VERSION>/ironbank/ironbank-values.yaml"    --set secrets.dockerConfig=<BASE64 ENCODED DOCKERCONFIG> \    --set global.imagePullSecret=k10-ecr \    ...
```

Since the only differences as compared to a standard Veeam Kasten
  installation are the images used, the rest of the process can follow the
  official Veeam Kasten documentation.

## Using Iron Bank Veeam Kasten Images in an Air-Gapped Environment â

Iron Bank hardened Veeam Kasten images can be used in an air-gapped
  environment by following the instructions found here .

## Implementing Iron Bank for Veeam Kasten Disaster Recovery â

The Iron Bank hardened restorectl image can be used for Veeam Kasten
  disaster recovery by following the instructions found here .

---

## Install Offline

For environments that are connected to the Internet, one needs access to
  three repositories to install Veeam Kasten:

- The Helm repository that contains the Veeam Kasten chart
- The container registry that contains the Veeam Kasten container images
- Upstream repositories to install Veeam Kasten dependencies (e.g., Prometheus)

However, if an air-gapped installation is required, it is possible to
  use your own private container registry to install Veeam Kasten. While
  this can always be done manually, the k10tools image command makes it easier
  to automate the process.

## Air-Gapped Veeam Kasten Installation â

If the Veeam Kasten container images are already available in a private
  repository, the below instructions can be used to install in an
  air-gapped environment. If needed, support for uploading images to a
  private image registry is documented below .

### Fetching the Helm Chart for Local Use â

To fetch the most recent Veeam Kasten Helm chart for local use, run the
  following command to pull the latest Veeam Kasten chart as a compressed
  tarball ( .tgz ) file into the working directory.

```
$ helm repo update && \    helm fetch kasten/k10
```

If you need to fetch a specific version, please run the following
  command:

```
$ helm repo update && \    helm fetch kasten/k10 --version=<k10-version>
```

### Installing Veeam Kasten with Local Helm Chart and Container Images â

If the Veeam Kasten container images were uploaded to a registry at repo.example.com , an air-gapped installation can be performed by
  setting global.airgapped.repository=repo.example.com as shown in the
  below command:

```
$ kubectl create namespace kasten-io$ helm install k10 k10-8.0.4.tgz --namespace kasten-io \    --set global.airgapped.repository=repo.example.com
```

### Installing Veeam Kasten with Disconnected OpenShift Operator â

To install Veeam Kasten with an OpenShift operator in an air-gapped
  cluster, follow the steps under offline operator install .

### Running Veeam Kasten Within a Local Network â

To run Veeam Kasten in a network without the ability to connect to the
  internet, Veeam Kasten needs to be installed in an air-gapped mode with
  the helm value metering.mode=airgap as shown in the command below:

```
$ kubectl create namespace kasten-io$ helm install k10 k10-8.0.4.tgz --namespace kasten-io \    --set metering.mode=airgap
```

If metering.mode=airgap is not set in an offline cluster, some
    functionality will be disabled. A message warning that Veeam Kasten is
    "Unable to validate license" will be displayed in the web based user
    interface. Errors containing messages "Could not get google bucket for
    metrics", "License check failed" and "Unable to validate license"
    will be logged.

If the metering service is unable to connect to the internet for 24
    hours, the metering service will restart.

### Providing Credentials if Local Container Repository is Private â

If the local repository that has been provided as the value of global.airgapped.repository is private, credentials for that
  repository can be provided using secrets.dockerConfig and global.imagePullSecret flags, as below, with the helm install command.

```
--set secrets.dockerConfig=$(base64 -w 0 < ${HOME}/.docker/config.json) \--set global.imagePullSecret="k10-ecr"
```

Our Helm chart creates a secret with the name k10-ecr with the value
    that has been provided for secrets.dockerConfig . That's why we are
    providing secret name k10-ecr as value of global.imagePullSecret .

## Preparing Veeam Kasten Container Images for Air-Gapped Use â

There are multiple ways to use a private repository including setting up
  a caching or proxy image registry that points to the Veeam Kasten image
  repositories using tools such as JFrog Artifactory. However, if images
  need to be manually uploaded or an automated upload pipeline is required
  to add Veeam Kasten images into your private repository, the following
  documentation should help.

To see all available commands and flags for running k10tools image please
  run the following:

```
$ docker run --rm gcr.io/kasten-images/k10tools:8.0.4 image --help
```

The following commands operate against the latest version of Veeam Kasten (8.0.4).

k10tools image is only supported for versions 7.5.0+ of Veeam Kasten and must match the version you're installing.

For older version, please refer to their documentation: https://docs.kasten.io/<version>/install/offline.html .

### List Veeam Kasten Container Images â

The following command will list all images used by the current Veeam Kasten
  version (8.0.4). This can be helpful if there is a requirement to tag and
  push Veeam Kasten images into your private repository manually instead of using
  the Kasten provided tool documented below.

```
$ docker run --rm gcr.io/kasten-images/k10tools:8.0.4 image list
```

### Copy Kasten Images into a Private Repository â

The following command will copy the Veeam Kasten container images into your
  specified registry. If the destination image tag should be different than the
  Veeam Kasten version, then the --dst-image-tag can be used to specify a new
  image tag.

The following example uses a repository located at repo.example.com .

```
$ docker run --rm -v $HOME/.docker:/home/kio/.docker gcr.io/kasten-images/k10tools:8.0.4 image copy --dst-registry repo.example.com
```

This command will use your local docker config if the private registry
    requires authentication.

The credsStore field in the $HOME/.docker/config.json is used to
    specify the credential store. This is typically an external credential
    store requiring an external helper and it may not be usable from within
    the docker container. Please refer to the docker documentation for more information.

Alternatively, k10tools image provides authentication mechanisms such as
    passing a username and password ( --dst-username and --dst-password flags) or a bearer token ( --dst-token flag). Please refer to
    the help flag for more information.

After running the previous command, use the
  instructions above to install Veeam Kasten via images
  uploaded to repo.example.com .

### Copy Kasten Images to/from a Filesystem Directory â

Network limitations may limit the ability to directly copy images into a
  private repository. Alternatively, images can be copied to the local filesystem
  and then pushed to a repository separately. This requires downloading the k10tools binary .

The following example copies the images to a directory images . This
  directory can then be used to upload to a private repository located at repo.example.com .

```
:substitutions:   $ k10tools image copy --dst-path images   $ k10tools image copy --src-path images --dst-registry repo.example.com
```

### Using Iron Bank Veeam Kasten Container Images â

If you want to use the Iron Bank hardened Veeam Kasten images in an air-gapped
  environment, execute the above commands but replace image with ironbank image :

```
:substitutions:   $ docker run --rm gcr.io/kasten-images/k10tools:8.0.4 ironbank image list   $ docker run --rm -v $HOME/.docker:/home/kio/.docker gcr.io/kasten-images/k10tools:8.0.4 ironbank image copy --dst-registry repo.example.com
```

This ensures the images are pulled from Registry1.

You must be logged in to the docker registry locally for this process
    to function correctly. Use docker login registry1.dso.mil --username "${REGISTRY1_USERNAME}" --password-stdin with your Registry1 CLI secret as
    the password to login.

Alternatively, provide credentials using the methods
    described above .

---

## Install Openshift Openshift

There are two methods to install Veeam Kasten on Red Hat OpenShift:

- Helm based Installation
- Operator based Installation

When deploying Veeam Kasten on a Red Hat OpenShift managed Kubernetes cluster using Cilium as a Container Network Interface (CNI), it is important to consider the associated limitations, including potential compatibility issues or differences in configuration compared to the default CNIs. Refer to this page for instructions on addressing these issues and optimizing the deployment with Cilium.

## Managed Red Hat OpenShift Offerings â

The two installation methods mentioned above are also applicable when
  installing Veeam Kasten on Managed Red Hat OpenShift offerings,
  including:

- Red Hat OpenShift on AWS (ROSA)
- Azure Red Hat OpenShift (ARO)

No additional or platform-specific configurations are required for
  installation.

---

## Install Operating Operating

There are a variety of ways to interact with the Veeam Kasten platform
  ranging from command-line interaction to monitoring the status of
  policies and jobs in the system. The following sections cover these
  topics in depth.

---

## Install Requirements

Veeam Kasten can be installed in a variety of different environments and
  on a number of Kubernetes distributions today. To ensure a smooth
  install experience, it is highly recommended to meet the prerequisites
  and run the pre-flight checks.

## Supported Platforms â

The following operating systems and architectures are supported.

| Operating System | Architectures | FIPS Support | Veeam Repository Exports | vSphere Block Mode Exports | Linux | x86_86 (amd64) | Yes | Yes | Yes |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Linux | x86_86 (amd64) | Yes | Yes | Yes |
| Linux | Arm (arm64/v8) | No | No | No |
| Linux | Power (ppc64le) | No | No | N/A |

## Prerequisites â

This section describes the general requirements for installing Veeam
  Kasten in any environment.

Follow the steps below to install Veeam Kasten with Helm:

1. Verify the Helm 3 package manager and configure access to the Veeam Kasten Helm Charts repository.

- The Helm version should be compatible with the version of the Kubernetes cluster where Veeam Kasten is expected to be deployed. Helm is assumed to be compatible with n-3 versions of Kubernetes it was compiled against. Follow the Helm version skew policy to determine suitable binary version.
- Add the Veeam Kasten Helm charts repository using:

```
$ helm repo add kasten https://charts.kasten.io/
```

1. Verify Helm Chart Signature.

- The integrity of the Veeam Kasten Helm chart published on the Helm chart repository can be verified using the public key published. Check the security page for more details.
- Download the public key from this link .
- When installing Veeam Kasten using the helm install command, pass the --verify flag along with the --keyring to verify the Helm chart during installation.

```
$ helm install k10 kasten/k10 --namespace=kasten-io --verify --keyring=/path/to/downloaded/RPM-KASTEN
```

Helm chart provenance is supported only in Veeam Kasten chart versions
    6.5.14 and later.

1. Run Pre-flight Checks.

- Perform the necessary checks to make sure that the environment is ready for installation. Refer to the Pre-Flight Checks for additional information.

The pre-flight check does not include verification of the cluster
    being in FIPS mode. This is a requirement for Veeam Kasten to be
    installed in FIPS mode.

1. Create the installation namespace for Veeam Kasten

(by default, kasten-io ):

```
$ kubectl create namespace kasten-io
```

- When Veeam Kasten is installed, helm will automatically generate a new Service Account to grant Veeam Kasten the required access to Kubernetes resources.
- If a pre-existing Service Account needs to be used, please follow these instructions .

1. Identify a performance-oriented storage class:

- Veeam Kasten assumes that SSDs or similar fast storage media support the default storage class. If the default storage class doesn't meet the performance requirements, add the following option to the Veeam Kasten Helm installation commands:

```
--set global.persistence.storageClass=<storage-class-name>
```

## Pre-flight Checks â

By installing the primer tool, you can perform pre-flight checks
  provided that your default kubectl context is pointed to the cluster
  you intend to install Veeam Kasten on. This tool runs in a cluster pod
  and performs the following operations:

- Validates if the Kubernetes settings meet the Veeam Kasten requirements.
- Catalogs the available StorageClasses.
- If a CSI provisioner exists, it will also perform basic validation of the cluster's CSI capabilities and any relevant objects that may be required. It is strongly recommended that the same tool be used to perform a more comprehensive CSI validation using the documentation here .

Note that running the pre-flight checks using the primer tool will
  create and subsequently clean up a ServiceAccount and ClusterRoleBinding
  to perform sanity checks on your Kubernetes cluster.

The primer tool assumes that the Helm 3 package
manager is installed and access to the Veeam Kasten
  Helm Charts repository is configured.

Run the following command to deploy the the pre-check tool:

```
$ curl https://docs.kasten.io/downloads/8.0.4/tools/k10_primer.sh | bash
```

To run the pre-flight checks in an air-gapped environment, use the
  following command:

```
$ curl https://docs.kasten.io/downloads/8.0.4/tools/k10_primer.sh | bash /dev/stdin -i repo.example.com/k10tools:8.0.4
```

Follow this guide to
    prepare Veeam Kasten container images for air-gapped use.

## Veeam Kasten Image Source Repositories â

All Veeam Kasten images for a default install are hosted at gcr.io/kasten-images .

When deploying Veeam Kasten using Iron Bank hardened images, the
  following repositories are used:

- registry1.dso.mil/ironbank/veeam/kasten
- registry1.dso.mil/ironbank/opensource/prometheus-operator
- registry1.dso.mil/ironbank/opensource/dexidp
- registry1.dso.mil/ironbank/opensource/prometheus
- registry1.dso.mil/ironbank/redhat/ubi

---

## Install Shareable Volume

In some situations Veeam Kasten may not currently support the creation
  of snapshots through the underlying storage provider. Generally, we
  recommend backing up volumes in these circumstances using the Generic Volume Snapshot method. However, this method involves configuring the
  application with a Kanister sidecar container that will mount the volume concerned and copy out the
  data.

As a special case, when the storage concerned is capable of being shared
  between pods, Veeam Kasten can back up the data without any
  modifications to the application. This is done by using an external pod
  in the application namespace.

## Supported storage providers â

The following storage providers support this feature-

- Amazon Elastic File System (EFS)

## Prerequisites â

### Create a Location Profile â

If you haven't done so already, create a Location profile with the
  appropriate Location and Credentials information from the Veeam Kasten
  settings page. Instructions for creating location profiles can be found here

Shareable volume backup and restore workflows are not compatible with immutable backups location profiles . Immutable backups enabled location profiles can be used
    with these workflows, but will be treated as a non-immutability-enabled
    profile: the protection period will be ignored, and no point-in-time
    restore functionality will be provided. Please note that use of an
    object-locking bucket for such cases can amplify storage usage without
    any additional benefit.

Shareable volume backup and restore workflows are not compatible with NFS/SMB location profiles .

The location profile must be present for shareable volume backups to
  work.

---

## Install Storage

Veeam Kasten supports direct integration with public cloud storage vendors as well as CSI integration. While most integrations are transparent, the below sections document the configuration needed for the exceptions.

## Direct Provider Integration â

Veeam Kasten supports seamless and direct storage integration with a number of storage providers. The following storage providers are either automatically discovered and configured within Veeam Kasten or can be configured for direct integration:

- Amazon Elastic Block Store (EFS)
- Azure Managed Disks (Azure Managed Disks)
- Google Persistent Disk
- Ceph
- Cinder -based providers on OpenStack
- vSphere Cloud Native Storage (CNS)
- Portworx
- Veeam Backup (snapshot data export only)

## Container Storage Interface (CSI) â

Apart from direct storage provider integration, Veeam Kasten also supports invoking volume snapshots operations via the Container Storage Interface (CSI). To ensure that this works correctly, please ensure the following requirements are met.

### CSI Requirements â

- Kubernetes v1.14.0 or higher
- The VolumeSnapshotDataSource feature has been enabled in the Kubernetes cluster
- A CSI driver that has Volume Snapshot support. Please look at the list of CSI drivers to confirm snapshot support.

### Pre-Flight Checks â

Assuming that the default kubectl context is pointed to a cluster with CSI enabled, CSI pre-flight checks can be run by deploying the primer tool with a specified StorageClass. This tool runs in a pod in the cluster and performs the following operations:

- Creates a sample application with a persistent volume and writes some data to it
- Takes a snapshot of the persistent volume
- Creates a new volume from the persistent volume snapshot
- Validates the data in the new persistent volume

First, run the following command to derive the list of provisioners along with their StorageClasses and VolumeSnapshotClasses.

```
curl -s https://docs.kasten.io/downloads/8.0.4/tools/k10_primer.sh | bash
```

Then, run the following command with a valid StorageClass to deploy the pre-check tool:

```
curl -s https://docs.kasten.io/downloads/8.0.4/tools/k10_primer.sh | bash /dev/stdin csi -s ${STORAGE_CLASS}
```

### CSI Snapshot Configuration â

For each CSI driver, ensure that a VolumeSnapshotClass has been added with Veeam Kasten annotation ( k10.kasten.io/is-snapshot-class: "true" ).

Note that CSI snapshots are not durable. In particular, CSI snapshots have a namespaced VolumeSnapshot object and a non-namespaced VolumeSnapshotContent object. With the default (and recommended) deletionPolicy , if there is a deletion of a volume or the namespace containing the volume, the cleanup of the namespaced VolumeSnapshot object will lead to the cascading delete of the VolumeSnapshotContent object and therefore the underlying storage snapshot.

Setting deletionPolicy to Delete isn't sufficient either as some storage systems will force snapshot deletion if the associated volume is deleted (snapshot lifecycle is not independent of the volume). Similarly, it might be possible to force-delete snapshots through the storage array's native management interface. Enabling backups together with volume snapshots is therefore required for a durable backup.

Veeam Kasten creates a clone of the original VolumeSnapshotClass with the DeletionPolicy set to 'Retain'. When restoring a CSI VolumeSnapshot, an independent replica is created using this cloned class to avoid any accidental deletions of the underlying VolumeSnapshotContent.

#### VolumeSnapshotClass Configuration â

- Alpha CSI Snapshot API
- Beta CSI Snapshot API

```
apiVersion: snapshot.storage.k8s.io/v1alpha1snapshotter: hostpath.csi.k8s.iokind: VolumeSnapshotClassmetadata:  annotations:    k10.kasten.io/is-snapshot-class: "true"  name: csi-hostpath-snapclass
```

```
apiVersion: snapshot.storage.k8s.io/v1beta1driver: hostpath.csi.k8s.iokind: VolumeSnapshotClassmetadata:  annotations:    k10.kasten.io/is-snapshot-class: "true"  name: csi-hostpath-snapclass
```

Given the configuration requirements, the above code illustrates a
  correctly-configured VolumeSnapshotClass for Veeam Kasten. If the
  VolumeSnapshotClass does not match the above template, please follow the
  below instructions to modify it. If the existing VolumeSnapshotClass
  cannot be modified, a new one can be created with the required
  annotation.

1. Whenever Veeam Kasten detects volumes that were provisioned via a CSI driver, it will look for a VolumeSnapshotClass with Veeam Kasten annotation for the identified CSI driver and use it to create snapshots. You can easily annotate an existing VolumeSnapshotClass using: $ kubectl annotate volumesnapshotclass ${VSC_NAME} \ k10.kasten.io/is-snapshot-class = true Verify that only one VolumeSnapshotClass per storage provisioner has the Veeam Kasten annotation. Currently, if no VolumeSnapshotClass or more than one has the Veeam Kasten annotation, snapshot operations will fail. # List the VolumeSnapshotClasses with Veeam Kasten annotation $ kubectl get volumesnapshotclass -o json | \ jq '.items[] | select (.metadata.annotations["k10.kasten.io/is-snapshot-class"]=="true") | .metadata.name' k10-snapshot-class

Whenever Veeam Kasten detects volumes that were provisioned via a
      CSI driver, it will look for a VolumeSnapshotClass with Veeam Kasten
      annotation for the identified CSI driver and use it to create
      snapshots. You can easily annotate an existing VolumeSnapshotClass
      using:

```
$ kubectl annotate volumesnapshotclass ${VSC_NAME} \    k10.kasten.io/is-snapshot-class=true
```

Verify that only one VolumeSnapshotClass per storage provisioner has
      the Veeam Kasten annotation. Currently, if no VolumeSnapshotClass or
      more than one has the Veeam Kasten annotation, snapshot operations
      will fail.

```
# List the VolumeSnapshotClasses with Veeam Kasten annotation$ kubectl get volumesnapshotclass -o json | \    jq '.items[] | select (.metadata.annotations["k10.kasten.io/is-snapshot-class"]=="true") | .metadata.name'k10-snapshot-class
```

#### StorageClass Configuration â

As an alternative to the above method, a StorageClass can be annotated
  with the following-( k10.kasten.io/volume-snapshot-class: "VSC_NAME" ).
  All volumes created with this StorageClass will be snapshotted by the
  specified VolumeSnapshotClass:

```
$ kubectl annotate storageclass ${SC_NAME} \    k10.kasten.io/volume-snapshot-class=${VSC_NAME}
```

#### Migration Requirements â

If application migration across clusters is needed, ensure that the
  VolumeSnapshotClass names match between both clusters. As the
  VolumeSnapshotClass is also used for restoring volumes, an identical
  name is required.

#### CSI Snapshotter Minimum Requirements â

Finally, ensure that the csi-snapshotter container for all CSI drivers
  you might have installed has a minimum version of v1.2.2. If your CSI
  driver ships with an older version that has known bugs, it might be
  possible to transparently upgrade in place using the following code.

```
# For example, if you installed the GCP Persistent Disk CSI driver# in namespace ${DRIVER_NS} with a statefulset (or deployment)# name ${DRIVER_NAME}, you can check the snapshotter version as below:$ kubectl get statefulset ${DRIVER_NAME} --namespace=${DRIVER_NS} \    -o jsonpath='{range .spec.template.spec.containers[*]}{.image}{"\n"}{end}'gcr.io/gke-release/csi-provisioner:v1.0.1-gke.0gcr.io/gke-release/csi-attacher:v1.0.1-gke.0quay.io/k8scsi/csi-snapshotter:v1.0.1gcr.io/dyzz-csi-staging/csi/gce-pd-driver:latest# Snapshotter version is old (v1.0.1), update it to the required version.$ kubectl set image statefulset/${DRIVER_NAME} csi-snapshotter=quay.io/k8scsi/csi-snapshotter:v1.2.2 \  --namespace=${DRIVER_NS}
```

## AWS Storage â

Veeam Kasten supports Amazon Web Services (AWS) storage integration,
  including Amazon Elastic Block Storage (EBS) and Amazon Elastic File
  System (EFS)

### Amazon Elastic Block Storage (EBS) Integration â

Veeam Kasten currently supports backup and restores of EBS CSI volumes
  as well as Native (In-tree) volumes. In order to work with the In-tree
  provisioner, or to migrate snapshots within AWS, Veeam Kasten requires
  an Infrastructure Profile. Please refer to AWS Infrastructure Profile on how to create one. Block Mode Exports of
  EBS volumes use the AWS EBS Direct
API .

### Amazon Elastic File System (EFS) Integration â

Veeam Kasten currently supports backup and restores of statically provisioned EFS CSI volumes. Since statically provisioned volumes use
  the entire file system we are able to utilize AWS APIs to take backups.

While the EFS CSI driver has begun supporting dynamic provisioning, it
  does not create new EFS volumes. Instead, it creates and uses access
  points within existing EFS volumes. The current AWS APIs do not support
  backups of individual access points.

However, Veeam Kasten can take backups of these dynamically provisioned EFS volumes using the
  [Shareable Volume Backup and Restore](./shareable-volume.md mechanism).

For all other operations, EFS requires an Infrastructure Profile. Please
  refer to AWS Infrastructure Profile on how to create one.

### AWS Infrastructure Profile â

To enable Veeam Kasten to take snapshots and restore volumes from AWS,
  an Infrastructure Profile must be created from the Infrastructure page
  of the Profiles menu in the navigation sidebar.

Using AWS IAM Service Account Credentials that Veeam Kasten was installed with is also
  possible with the Authenticate with AWS IAM Role checkbox. An
  additional AWS IAM Role can be provided if the user requires Veeam
  Kasten to assume a different role. The provided credentials are verified
  for both EBS and EFS.

Currently, Veeam Kasten also supports the legacy mode of providing AWS
  credentials via Helm. In this case, an AWS Infrastructure Profile will
  be created automatically with the values provided through Helm, and can
  be seen on the Dashboard. This profile can later be replaced or updated
  manually if necessary, such as when the credentials change.

In future releases, providing AWS credential via Helm will be
  deprecated.

## Azure Managed Disks â

Veeam Kasten supports backups and restores for both CSI volumes and
  in-tree volumes within Azure Managed Disks. To work with the Azure
  in-tree provisioner, Veeam Kasten requires the creation of an
  Infrastructure Profile from the Infrastructure page of the Profiles menu in the navigation sidebar.

Veeam Kasten can perform block mode exports with changed block tracking (CBT)
  for volumes provisioned using the disk.csi.azure.com CSI driver. This
  capability is automatically utilized when the following conditions are met:

- Veeam Kasten includes a valid Azure Infrastructure Profile
- Either the Azure Disk storage class or individual PVC enables Block Mode Exports
- The Azure Disk volume snapshot class enables incremental snapshots, as shown in the example below:

```
$ kubectl get volumesnapshotclass csi-azuredisk-vsc -o yamlapiVersion: snapshot.storage.k8s.io/v1deletionPolicy: Deletedriver: disk.csi.azure.comkind: VolumeSnapshotClassmetadata:  annotations:    k10.kasten.io/is-snapshot-class: "true"    snapshot.storage.kubernetes.io/is-default-class: "true"  creationTimestamp: "2024-10-28T14:48:50Z"  generation: 1  name: csi-azuredisk-vsc  resourceVersion: "2502"  uid: 9ebec324-0f09-42fa-aace-39440b3184b6parameters:  incremental: "true"  # available values: "true", "false" ("true" by default for Azure Public Cloud, and "false" by default for Azure Stack Cloud)
```

### Service Principal â

Veeam Kasten supports authentication with Microsoft Entra ID (formerly
  Azure Active Directory) with Azure Client Secret credentials, as well as
  Azure Managed Identity.

To authenticate with Azure Client Secret credentials, Veeam Kasten
  requires Tenant ID , Client ID , and Client Secret .

### Managed Identities â

If Use Azure TenantID, Secret and ClientID to authenticate is chosen, users will
  opt out of using Managed Identity and need to provide their own Tenant ID,
  Client Secret and Client ID.
  To use Managed Identity but provide a custom Client ID, users can choose Custom Client ID and provide their own, otherwise the default Managed Identity will be used.

To authenticate with Azure Managed Identity, clusters must have Azure Managed Identity enabled.

### Federated Identity â

To authenticate with Azure Federated Identity (also known as workload identity),
  clusters must have Azure Federated Credentials set up.
  This can only be done via helm. More information can be found here .

Federated Identity is currently only supported on Openshift clusters with version 4.14 and later.

If you are using Federated Identity , you cannot edit or delete the infrastructure profile once created. You can edit or delete by using helm upgrade.

### Other Configuration â

In addition to authentication credentials, Veeam Kasten also requires Subscription ID and Resource Group . For information on how to
  retrieve the required data, please refer to Installing Veeam Kasten on
Azure .

Additionally, information for Azure Stack such as Storage Environment Name , Resource Manager Endpoint , AD Endpoint ,
  and AD Resource can also be specified. These fields are not mandatory,
  and default values will be used if they are not provided by the user.

| Field | Value | Storage Environment Name | AzurePublicCloud |
| :---: | :---: | :---: | :---: |
| Storage Environment Name | AzurePublicCloud |
| Resource Manager Endpoint | https://management.azure.com/ |
| AD Endpoint | https://login.microsoftonline.com/ |
| AD Resource | https://management.azure.com/ |

Veeam Kasten also supports the legacy method of providing Azure
  credentials via Helm. In this case, an Azure Infrastructure Profile will
  be created automatically with the values provided through Helm, and can
  be seen on the Dashboard. This profile can later be replaced or updated
  manually if necessary, such as when the credentials change.

In future releases, providing Azure credentials via Helm will be
  deprecated.

## Pure Storage â

For integrating Veeam Kasten with Pure Storage, please follow Pure
  Storage's instructions on deploying the Pure Storage
Orchestrator and the VolumeSnapshotClass .

Once the above two steps are completed, follow the instructions for Veeam Kasten CSI integration<csi> . In
  particular, the Pure VolumeSnapshotClass needs to be edited using the
  following commands.

```
$ kubectl annotate volumesnapshotclass pure-snapshotclass \    k10.kasten.io/is-snapshot-class=true
```

## NetApp Trident â

For integrating Veeam Kasten with NetApp Trident, please follow
  NetApp's instructions on deploying Trident as a CSI
provider and then follow the
  instructions above<csi> .

## Google Persistent Disk â

Veeam Kasten supports Google Persistent Disk (GPD) storage integration
  with both CSI and native (in-tree) drivers. In order to use GPD native
  driver, an Infrastructure Profile must be created from the Infrastructure page of the Profiles menu in the navigation sidebar.

The GCP Project ID and GCP Service Key fields are required. The GCP Service Key takes the complete content of the service account json
  file when creating a new service account.

Currently, Veeam Kasten also supports the legacy mode of providing
  Google credentials via Helm. In this case, a Google Infrastructure
  Profile will be created automatically with the values provided through
  Helm, and can be seen on the Dashboard. This profile can later be
  replaced or updated manually if necessary, such as when the credentials
  change.

In future releases, providing Google credential via Helm will be
  deprecated.

## Ceph â

Veeam Kasten supports Ceph RBD and Ceph FS snapshots and backups via
  their CSI drivers.

### CSI Integration â

If you are using Rook to install Ceph, Veeam Kasten only supports Rook
    v1.3.0 and above. Previous versions had bugs that prevented restore from
    snapshots.

Veeam Kasten supports integration with Ceph (RBD and FS) via its CSI
  interface by following the instructions for CSI integration<csi> . In particular, the
  Ceph VolumeSnapshotClass needs to be edited using the following
  commands.

```
$ kubectl annotate volumesnapshotclass csi-snapclass \    k10.kasten.io/is-snapshot-class=true
```

Ceph CSI RBD volume snapshots can be exported in block mode with the
  appropriate annotation on their StorageClass. The Ceph Rados Block
  Device API can enable direct access to data blocks through the network
  and provide information on the allocated blocks in a snapshot, which
  could reduce the size and duration of a backup; however, it is important
  to note that Changed Block Tracking is not supported for Ceph CSI RBD
  snapshots. The output of the Veeam Kasten Primer Block Mount Check command indicates if the API will be used:

```
...Block mount checker:StorageClass ocs-storagecluster-ceph-rbd is annotated with 'k10.kasten.io/sc-supports-block-mode-exports=true'StorageClass ocs-storagecluster-ceph-rbd is supported by K10 in Block volume mode via vendor APIs (Ceph Rados Block Device)
```

### Snapshots as Shallow Read-Only Volumes (CephFS only) â

Veeam Kasten supports the use of snapshots as shallow read-only volumes
  specifically designed for file systems (FS), particularly for the CephFS
  CSI driver. Using this feature requires a special StorageClass, which is
  usually a copy of the regular StorageClass of the CephFS CSI driver, but
  with the backingSnapshot: "true" option in the parameters section. This StorageClass has to meet the Veeam Kasten requirements for CSI StorageClass
configuration .
  In addition to this, it is necessary to define specific changes
  (overrides) for the exportData setting within a policy. An
  illustrative example can be found here: [overrides for exportData
  setting of

Below is an example of how to specify these overrides for your
  reference:

```
exportData:  enabled: true  overrides:    - storageClassName: regular-cephfs-csi-storage-class      enabled: true      exporterStorageClassName: shallow-cephfs-csi-storage-class
```

Since 'Snapshots as a shallow read-only volumes' feature requires a
  read-only mount of the Snapshot PVC during the Export phase, support for
  read-only mount has to be enabled:

```
$ kubectl annotate storageclass shallow-cephfs-csi-storage-class \    k10.kasten.io/sc-supports-read-only-mount="true"
```

An Openshift cluster requires preserving SELinuxLevel of source
  namespace to Kanister Pod during the Export phase. This functionality
  always enabled in Veeam Kasten, thus additional actions are not
  required.

## Cinder/OpenStack â

Veeam Kasten supports snapshots and backups of OpenStack's Cinder block
  storage.

To enable Veeam Kasten to take snapshots, an OpenStack Infrastructure
  Profile must be created from the Infrastructure page of the Profiles menu in the navigation sidebar.

The Keystone Endpoint , Project Name , Domain Name , Username and Password are required fields. If the OpenStack environment spans
  multiple regions then the Region field must also be specified.

## vSphere â

Veeam Kasten supports vSphere storage integration with PersistentVolumes
  provisioned using the vSphere CSI
Provisioner .

Currently, backup and restore operations are not supported for RWX/ROX
    volumes provisioned using vSAN File Services.

The available functionality varies by the type of cluster infrastructure
  used and is summarized in the table below:

|  | vSphere with Tanzu[1] | Other Kubernetes infrastructures[1] | vSphere | Supported versions | 7.0 U3 or higher | 7.0 U1 or higher |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| vSphere | Supported versions | 7.0 U3 or higher | 7.0 U1 or higher |
| vCenter access required[2] | Required | Required |
| Export | Export infilesystem mode | Not Supported[3] | Supported |
| Export inblock mode[4] | To anObject Storage Location, anNFS/SMB File Storage Locationor aVeeam Repository[5] | To anObject Storage Location, anNFS/SMB File Storage Locationor aVeeam Repository[5] |
| Restore | Restore from asnapshot | Not Supported[3] | Supported |
| Restore from an export (any mode) | Supported | Supported |
| Instant Recoveryrestore | Not Supported[3] | From aVeeam Repository |
| Import | Import afilesystem modeexport | Supported | Supported |
| Import ablock modeexport | From anObject Storage Location, anNFS/SMB File Storage Locationor aVeeam Repository[5] | From anObject Storage Location, anNFS/SMB File Storage Locationor aVeeam Repository[5] |

1. vSphere with Tanzu supervisor clusters and VMware Tanzu Kubernetes Grid management clusters are not supported.

1. Access to vCenter is required with all types of cluster infrastructures as Veeam Kasten directly communicates with vSphere to snapshot a First Class Disk (FCD) , resolve paravirtualized volume handles, set tags and access volume data with the VMware VDDK API.

1. The guest clusters of vSphere with Tanzu use paravirtualized PersistentVolumes. These clusters do not support the static provisioning of a specific FCD from within the guest cluster itself. This disables Veeam Kasten's ability to restore applications from their local snapshots, Instant Recovery and the ability to export snapshot data in filesystem mode .

1. Block mode snapshot exports are available in all types of vSphere cluster infrastructures. Snapshot content is accessed at the block level directly through the network using the VMware VDDK API. Enable changed block tracking on the VMware cluster nodes to reduce the amount of data transferred during export. See this Veeam Kasten knowledge base article for how to do so in vSphere with Tanzu guest clusters.

1. Block mode snapshot exports can be saved in an Object Storage Location , an NFS/SMB File Storage Location or a Veeam Repository .

A vSphere Infrastructure Profile must be created from the Infrastructure page of the Profiles menu in the navigation sidebar
  to identify the vCenter server.

The vCenter Server is required and must be a valid IP address or hostname
  that points to the vSphere infrastructure.
  The vSphere User and vSphere Password fields are also required.

If vSphere credentials are provided during the installation of Veeam
    Kasten
    ( Installing Veeam Kasten on VMware vSphere ) those parameters will be ignored in favor of the
    credentials contained in the Infrastructure profile.

It is recommended that a dedicated user account be created for Veeam
    Kasten. To authorize the account, create a role with the following
    privileges (for 7.0.x and 8.0.x):

- Datastore Privileges( 7.0 / 8.0 ) Allocate space Browse datastore Low level file operations
- Global Privileges ( 7.0 / 8.0 ) Disable methods Enable methods Licenses
- Virtual Machine Snapshot Management Privileges ( 7.0 / 8.0 ) Create snapshot Remove snapshot Revert to snapshot
- Cryptographic operations ( 8.0 ) Decrypt

- Allocate space
- Browse datastore
- Low level file operations

- Disable methods
- Enable methods
- Licenses

- Create snapshot
- Remove snapshot
- Revert to snapshot

- Decrypt

vSphere with Tanzu clusters require the following additional privilege
    to resolve paravirtualized volume handles:

- CNS Privileges ( 7.0 / 8.0 ) Searchable

- Searchable

Also for vSphere with Tanzu, assign the can edit role to
    the custom user in the vSphere Namespace using the following UI path:

- Workload Management > Namespaces > Select the namespace associated with the TKG service > Permissions > Add (assign [can edit] role)

Assign this role to the dedicated Veeam Kasten user account on the
    following objects:

- The root vCenter object
- The datacenter objects (propagate down each subtree to reach datastore and virtual machine objects)

There is an upper limit on the maximum number of snapshots for a VMware
  Kubernetes PersistentVolume .
  Refer to this or more recent
  VMware knowledge base articles for the limit and for recommendations on
  the number of snapshots to maintain. A Veeam Kasten backup policy provides control over the number of local Veeam Kasten restore points retained, and by implication, the number of local snapshots
  retained. A Veeam Kasten backup and export policy allows separate retention policies for local and
  exported Veeam Kasten restore points. It is possible to set a 0 local
  restore point retention value (i.e. no local snapshots are
retained ), as long as a non-zero exported restore point retention
  value is set; doing so does not adversely impact the ability to use incremental block mode exports with changed block tracking .

The Veeam Kasten default timeout for vSphere snapshot related operations
  may be too short if you are dealing with very large volumes. If you
  encounter timeout errors then adjust the vmWare.taskTimeoutMin Helm
  option accordingly.

You may observe that an application's PersistentVolumes do not get
    deleted even if their Reclaim Policy is Delete . This can happen when
    using Veeam Kasten to restore an application in the same namespace or
    when deleting or uninstalling an application previously backed up by
    Veeam Kasten.

This is because the VMware CSI driver fails in the deletion of
    PersistentVolumes containing snapshots: a VMware snapshot is embedded in
    its associated FCD volume and does not exist independent of this volume,
    and it is not possible to delete an FCD volume if it has snapshots. The
    VMware CSI driver leaves such PersistentVolumes in the Released state with a "failed to delete volume" warning (visible with kubectl
describe ).
    You may also see errors flagged for this operation in the vCenter GUI.
    The driver re-attempts the deletion operation periodically, so when all
    snapshots get deleted the PersistentVolume will eventually be deleted.
    One can also attempt to manually delete the PersistentVolume again at
    this time.

When Veeam Kasten restores an application in the same namespace from
    some restore point, new Kubernetes PersistentVolume objects (with new
    FCD volumes) are created for the application. However, any restore point
    that involves local snapshots will now point into FCD volumes associated
    with PersistentVolume objects in the Released state! Deletion of
    these Veeam Kasten restore points (manually or by schedule) will delete
    the associated FCD snapshots after which the PersistentVolume objects
    and their associated FCD volumes will eventually be released.

When uninstalling or deleting an application, do not force delete
    Kubernetes PersistentVolume objects in the Released state as this
    would orphan the associated FCD volumes! Instead, use the vCenter GUI or
    a CLI tool like govc to manually
    delete the snapshots.

## Portworx â

Apart from CSI-level support, Veeam Kasten also directly integrates with
  the Portworx storage platform.

To enable Veeam Kasten to take snapshots and restore volumes from
  Portworx, an Infrastructure Profile must be created from the Infrastructure page of the Profiles menu in the navigation sidebar.

The Namespace and Service Name fields are used to determine the
  Portworx endpoint. If these fields are left blank the Portworx defaults
  of kube-system and portworx-service will be used respectively.

In an authorization-enabled Portworx setup, the Issuer and Secret fields must be set. The Issuer must represent the JWT issuer. The Secret is the JWT shared secret, which is represented by the Portworx
  environment variable- PORTWORX_AUTH_JWT_SHAREDSECRET . Refer to Portworx
Security for more information.

## Veeam Backup & Replication â

A Veeam Repository can be used as the destination for persistent volume snapshot data
  for any cluster where a Veeam Backup & Replication (VBR) repository is available, and the storage provisioner for persistent
  volumes supports block mode export.

### Considerations â

The following limitations should be considered when exporting
  data from Veeam Kasten to VBR:

- Veeam Kasten will only export volume data to a VBR repository. Application metadata, artifacts produced by Blueprints, and ImageStream container image data will be stored in a separate Veeam Kasten location profile specified within the policy.
- Both Filesystem and Block persistent volume modes are supported, however only storage provisioners capable of performing block mode exports are compatible.
- All exported volume data is uploaded by a single datamover Pod and stored as a single object in VBR for each export, independent of the number of persistent volumes protected by the policy.
- Copies of backup data in VBR, such as those produced through exporting to scale-out backup repositories or backup copy jobs, cannot be directly restored in Veeam Kasten.
- Each Veeam Kasten instance may only export to a single, unique VBR backup server. Multiple location profiles may be created to export to separate repositories exposed by the same VBR backup server. Multiple Veeam Kasten instances may be integrated with the same VBR backup server.
- Veeam Kasten does not support export to VBR direct object storage repository types.

### Policy-based Backups â

A VBR backup job will be created on the VBR server associated
  with each Veeam Kasten policy. A Veeam Kasten catalog identifier is appended
  to the name to ensure uniqueness across multiple clusters that back up
  to the same VBR server. Each application namespace protected by the
  policy will produce a single, separate restore point object.

Veeam Kasten supports integrations with the following storage
  provisioners to accelerate incremental backups to VBR when available:

- Azure Disk CSI - disk.csi.azure.com
- CephRBD CSI - rbd.csi.ceph.com
- VMWare vSphere CSI - csi.vsphere.vmware.com

If storage integration is unavailable, each export will require
  reading the entire source volume(s), however only changes will be sent to VBR.

Following export, each backup is converted to a synthetic full backup .

### Manual Backups â

Volume data from a manual export of an application's volumes
  (i.e. not associated with a Veeam Kasten policy) will produce
  a standalone K10ManualBackup backup job containing the
  application namespace. Each manual export is saved as a
  full, independent VeeamZIP backup.

### Migrations â

Veeam Kasten restore points that contain snapshot data exported to a
  Veeam Repository may be imported and restored on other supported clusters.
  The target cluster must be configured with both the location profile used
  for restore point metadata and the Veeam Repository location profile used for volume data.

In order to properly restore volume data from VBR, the name of the
    Veeam Repository location profile on both the source and target cluster
    must be identical.

### Retirement â

As Veeam Kasten restore points are retired via policy-based retention
  or manual administrator action, associated VBR restore points are
  automatically deleted.

### Instant Recovery â

Instant Recovery will get an exported restore point up and running much
  faster than a regular restore. This feature requires vSphere 7.0.3+ and
  a Veeam Backup server version V12 or higher. This is not supported on
  vSphere with Tanzu clusters at this time. Before using Instant Recovery,
  you should ensure that all Storage Classes in your Kubernetes clusters
  are configured to avoid placing new volumes in the Instant Recovery
  datastore. Please see this Knowledge Base
article for recommendations on Storage
  Classes for use with Instant Recovery.

When a Veeam Kasten Instant Recovery is triggered, rather than creating
  volumes and populating them with data from VBR, Veeam Kasten asks the
  Veeam Backup server to do an Instant Recovery of the FCDs (vSphere First
  Class Disks) that are needed and then creates PVs that use those FCDs.
  The FCDs exist in a vPower NFS datastore created by the Veeam Backup
  server and attached to the vSphere cluster hosting the Kubernetes
  cluster.

Once the Instant Recovery has completed, the application will be running
  using the Veeam Backup server storage. At that point, the virtual disks
  will be migrated into their permanent home with no interruption in
  service. The application will not see any differences in how it is using
  the storage and all of the pods using the disks will continue operating
  without any restarts. The migration will start automatically after the
  Instant recovery process completes.

Currently Instant Recovery is only supported for Restore Actions , not
  Restore Policies. To use Instant Recovery, select the Enable Instant
  Recovery checkbox (this will only appear if all compatibility criteria
  are met) or set the InstantRecovery property in the RestoreAction spec.

All restore features are supported with Instant Recovery.

---

## Install Upgrade

Currently, upgrades are only supported across a maximum of four versions
    (e.g., 2.0.10 -> 2.0.14). If your Veeam Kasten version is further
    behind the latest, a step upgrade process is recommended where you can
    use the [--version] flag with helm upgrade to
    control the version jumps. At least 50% free space is required in
    catalog storage also.

## Upgrade Assistant â

You can verify the available free space for the catalog and access your
  recommended upgrade path by navigating to the System Information page
  from the Settings menu in the navigation sidebar or by using Veeam Kasten Primer for Upgrades resource.

## Upgrading Helm-Installed Veeam Kasten â

To upgrade to the latest Veeam Kasten release, unless you have installed
  Veeam Kasten via the a public cloud marketplace, you should run the
  following command assuming you installed in the kasten-io namespace
  with the release name k10 . If you do not remember your release name,
  you can easily discover that via the use of helm list --namespace=kasten-io .

If Generic Storage Backup is being used
    for backing the applications and if a new version of
    Kanister-tools image is available, additional steps may need to be performed
    for updating the Kanister sidecar image manually. Follow steps mentioned in Update Kanister Sidecar Image section.

```
$ helm repo update && \    helm get values k10 --output yaml --namespace=kasten-io > k10_val.yaml && \    helm upgrade k10 kasten/k10 --namespace=kasten-io -f k10_val.yaml
```

Known Issues : Helm 3 has known bugs with upgrade (e.g., #6850 ). If you run into
  errors along the lines of

```
Error: UPGRADE FAILED: rendered manifests contain a new resource that already exists. Unable to continue with update: existing resource conflict: kind: Deployment, namespace: kasten-io, name: prometheus-server
```

Please use the following as a workaround and then run the above upgrade
  commands.

```
$ kubectl --namespace=kasten-io delete deployment prometheus-server
```

## Updating Kanister Sidecar Image for Applications using Generic Storage Backup â

After releasing a new version of Veeam Kasten, a new Sidecar container
  may be published. In such cases, the Kanister Sidecar image needs to be
  updated for applications using Generic Storage Backup. Generic Storage Backup .
  If the Sidecar injection was enabled while installing/upgrading Veeam Kasten using the Helm option described in Generic Storage Backup .
  the application pods having the Kanister Sidecar injected in them can be
  restarted.
  This will pull the latest Kanister tools image for the application.

Alternatively, to refrain from the restarting the application,
  one of the below methods can be followed to update the Kanister
  Sidecar image in the application pods.

1. Manual update of the Kanister Sidecar Image : Manually update the Kanister Sidecar image in all the application deployments where the Kanister Sidecar is injected. This can be done by changing the image for kanister-sidecar container in the application deployment.

```
$ kubectl set image deployment/<deployment_name> kanister-sidecar=<image_name>:<version>
```

Executing this updates the deployment and causes the pods to restart. The
    restart behavior depends on the deployment strategy.

1. Removing the Sidecar manually : Once the Kanister Sidecar is removed, mutating webhook will inject the Sidecar with the new image automatically. This can be done by any of the methods mentioned below: 2.1 Use Kasten tools to remove the Sidecar. Note This should be done in a planned maintenance window. $ ./k10tools k10genericbackup uninject all -n < namespace > 2.2 Fetch the YAML manifest for the deployment and manually remove the Kanister Sidecar $ kubectl get deployment < deployment_name > -o yaml > deployment.yaml Identify the section in the YAML file that defines the containers in the deployment. Delete the definition of the unwanted Sidecar container. containers: - args: - tail -f /dev/null image: gcr.io/kasten-images/kanister-tools:108 imagePullPolicy: IfNotPresent name: kanister-sidecar resources: { } terminationMessagePath: /dev/termination-log terminationMessagePolicy: File volumeMounts: - mountPath: /data/data name: data - mountPath: /tmp/kopia-cache name: kopia-cache-volume dnsPolicy: ClusterFirst Apply the modified deployment as below $ kubectl apply -f deployment.yaml -n < namespace_name >

Removing the Sidecar manually : Once the Kanister Sidecar is removed,
      mutating webhook will inject the Sidecar with the new image automatically.
      This can be done by any of the methods mentioned below:

2.1 Use Kasten tools to remove the Sidecar.

This should be done in a planned maintenance window.

```
$ ./k10tools k10genericbackup uninject all -n <namespace>
```

2.2 Fetch the YAML manifest for the deployment and manually remove
      the Kanister Sidecar

```
$ kubectl get deployment <deployment_name> -o yaml > deployment.yaml
```

Identify the section in the YAML file that defines the containers
      in the deployment.
      Delete the definition of the unwanted Sidecar container.

```
containers:- args:- tail -f /dev/nullimage: gcr.io/kasten-images/kanister-tools:108imagePullPolicy: IfNotPresentname: kanister-sidecarresources: {}terminationMessagePath: /dev/termination-logterminationMessagePolicy: FilevolumeMounts:- mountPath: /data/data    name: data- mountPath: /tmp/kopia-cache    name: kopia-cache-volumednsPolicy: ClusterFirst
```

Apply the modified deployment as below

```
$ kubectl apply -f deployment.yaml -n <namespace_name>
```

## Upgrading on the Google Cloud Marketplace â

If you have installed Veeam Kasten via the Google Cloud Marketplace,
  please follow the instructions here .

## Upgrading on the AWS Marketplace â

If you have installed Veeam Kasten via the AWS Container Marketplace or
  AWS Marketplace for Containers Anywhere, please follow the marketplace
  upgrade instructions.

## Upgrading an Operator Installed Veeam Kasten â

Upgrading a Veeam Kasten installation made by a Veeam Kasten Operator
  requires updating the Veeam Kasten Operator. Ref: Red Hat documentation
for upgrading installed
Operators .

The process of upgrading the Veeam Kasten Operator depends on how update
  was configured during install - Automatic or Manual.

The Operator update approval strategy can be changed anytime after
  install from the Subscription tab of the Operator.

For an Automatic update, the Veeam Kasten Operator and Operand
  (which is the Veeam Kasten install) are both automatically updated any
  time a new Veeam Kasten Operator is published.

For a Manual update, the cluster administrator must approve the
  update when it shows up for the installation to begin. Ref: Red Hat
documentation for manually approving a pending Operator
upgrade .

The Veeam Kasten operators are published with a maximum supported
  OpenShift version. This will cause warnings to appear when trying to
  upgrade a cluster beyond the maximum supported version.

Upgrading the cluster beyond the Veeam Kasten maximum supported
    OpenShift version may cause unpredictable Veeam Kasten behavior and will
    result in losing Kasten support.

Examples of warning messages for cluster upgrade:

---

## Install Upgrade

Currently, upgrades are only supported across a maximum of four versions
    (e.g., 2.0.10 -> 2.0.14). If your Veeam Kasten version is further
    behind the latest, a step upgrade process is recommended where you can
    use the [--version] flag with helm upgrade to
    control the version jumps. At least 50% free space is required in
    catalog storage also.

## Upgrade Assistant â

You can verify the available free space for the catalog and access your
  recommended upgrade path by navigating to the System Information page
  from the Settings menu in the navigation sidebar or by using Veeam Kasten Primer for Upgrades resource.

## Upgrading Helm-Installed Veeam Kasten â

To upgrade to the latest Veeam Kasten release, unless you have installed
  Veeam Kasten via the a public cloud marketplace, you should run the
  following command assuming you installed in the kasten-io namespace
  with the release name k10 . If you do not remember your release name,
  you can easily discover that via the use of helm list --namespace=kasten-io .

If Generic Storage Backup is being used
    for backing the applications and if a new version of
    Kanister-tools image is available, additional steps may need to be performed
    for updating the Kanister sidecar image manually. Follow steps mentioned in Update Kanister Sidecar Image section.

```
$ helm repo update && \    helm get values k10 --output yaml --namespace=kasten-io > k10_val.yaml && \    helm upgrade k10 kasten/k10 --namespace=kasten-io -f k10_val.yaml
```

Known Issues : Helm 3 has known bugs with upgrade (e.g., #6850 ). If you run into
  errors along the lines of

```
Error: UPGRADE FAILED: rendered manifests contain a new resource that already exists. Unable to continue with update: existing resource conflict: kind: Deployment, namespace: kasten-io, name: prometheus-server
```

Please use the following as a workaround and then run the above upgrade
  commands.

```
$ kubectl --namespace=kasten-io delete deployment prometheus-server
```

## Updating Kanister Sidecar Image for Applications using Generic Storage Backup â

After releasing a new version of Veeam Kasten, a new Sidecar container
  may be published. In such cases, the Kanister Sidecar image needs to be
  updated for applications using Generic Storage Backup. Generic Storage Backup .
  If the Sidecar injection was enabled while installing/upgrading Veeam Kasten using the Helm option described in Generic Storage Backup .
  the application pods having the Kanister Sidecar injected in them can be
  restarted.
  This will pull the latest Kanister tools image for the application.

Alternatively, to refrain from the restarting the application,
  one of the below methods can be followed to update the Kanister
  Sidecar image in the application pods.

1. Manual update of the Kanister Sidecar Image : Manually update the Kanister Sidecar image in all the application deployments where the Kanister Sidecar is injected. This can be done by changing the image for kanister-sidecar container in the application deployment.

```
$ kubectl set image deployment/<deployment_name> kanister-sidecar=<image_name>:<version>
```

Executing this updates the deployment and causes the pods to restart. The
    restart behavior depends on the deployment strategy.

1. Removing the Sidecar manually : Once the Kanister Sidecar is removed, mutating webhook will inject the Sidecar with the new image automatically. This can be done by any of the methods mentioned below: 2.1 Use Kasten tools to remove the Sidecar. Note This should be done in a planned maintenance window. $ ./k10tools k10genericbackup uninject all -n < namespace > 2.2 Fetch the YAML manifest for the deployment and manually remove the Kanister Sidecar $ kubectl get deployment < deployment_name > -o yaml > deployment.yaml Identify the section in the YAML file that defines the containers in the deployment. Delete the definition of the unwanted Sidecar container. containers: - args: - tail -f /dev/null image: gcr.io/kasten-images/kanister-tools:108 imagePullPolicy: IfNotPresent name: kanister-sidecar resources: { } terminationMessagePath: /dev/termination-log terminationMessagePolicy: File volumeMounts: - mountPath: /data/data name: data - mountPath: /tmp/kopia-cache name: kopia-cache-volume dnsPolicy: ClusterFirst Apply the modified deployment as below $ kubectl apply -f deployment.yaml -n < namespace_name >

Removing the Sidecar manually : Once the Kanister Sidecar is removed,
      mutating webhook will inject the Sidecar with the new image automatically.
      This can be done by any of the methods mentioned below:

2.1 Use Kasten tools to remove the Sidecar.

This should be done in a planned maintenance window.

```
$ ./k10tools k10genericbackup uninject all -n <namespace>
```

2.2 Fetch the YAML manifest for the deployment and manually remove
      the Kanister Sidecar

```
$ kubectl get deployment <deployment_name> -o yaml > deployment.yaml
```

Identify the section in the YAML file that defines the containers
      in the deployment.
      Delete the definition of the unwanted Sidecar container.

```
containers:- args:- tail -f /dev/nullimage: gcr.io/kasten-images/kanister-tools:108imagePullPolicy: IfNotPresentname: kanister-sidecarresources: {}terminationMessagePath: /dev/termination-logterminationMessagePolicy: FilevolumeMounts:- mountPath: /data/data    name: data- mountPath: /tmp/kopia-cache    name: kopia-cache-volumednsPolicy: ClusterFirst
```

Apply the modified deployment as below

```
$ kubectl apply -f deployment.yaml -n <namespace_name>
```

## Upgrading on the Google Cloud Marketplace â

If you have installed Veeam Kasten via the Google Cloud Marketplace,
  please follow the instructions here .

## Upgrading on the AWS Marketplace â

If you have installed Veeam Kasten via the AWS Container Marketplace or
  AWS Marketplace for Containers Anywhere, please follow the marketplace
  upgrade instructions.

## Upgrading an Operator Installed Veeam Kasten â

Upgrading a Veeam Kasten installation made by a Veeam Kasten Operator
  requires updating the Veeam Kasten Operator. Ref: Red Hat documentation
for upgrading installed
Operators .

The process of upgrading the Veeam Kasten Operator depends on how update
  was configured during install - Automatic or Manual.

The Operator update approval strategy can be changed anytime after
  install from the Subscription tab of the Operator.

For an Automatic update, the Veeam Kasten Operator and Operand
  (which is the Veeam Kasten install) are both automatically updated any
  time a new Veeam Kasten Operator is published.

For a Manual update, the cluster administrator must approve the
  update when it shows up for the installation to begin. Ref: Red Hat
documentation for manually approving a pending Operator
upgrade .

The Veeam Kasten operators are published with a maximum supported
  OpenShift version. This will cause warnings to appear when trying to
  upgrade a cluster beyond the maximum supported version.

Upgrading the cluster beyond the Veeam Kasten maximum supported
    OpenShift version may cause unpredictable Veeam Kasten behavior and will
    result in losing Kasten support.

Examples of warning messages for cluster upgrade:

---

## Install Vault Vault

Refer to the Vault Authentication documentation for additional help.

There are a few steps required for configuring Vault in order for
  Kubernetes Authentication to work properly:

Create a policy that has the following permissions, which are needed by
  Veeam Kasten:

```
$ vault policy write <policy_name> - <<EOFpath "transit/keys" {  capabilities = [ "read", "list" ]}path "transit/keys/<vault_transit_key_name>" {  capabilities = [ "read" ]}path "transit/encrypt/<vault_transit_key_name>" {  capabilities = [ "update" ]}path "transit/decrypt/<vault_transit_key_name>" {  capabilities = [ "update" ]}EOF
```

Next, create a role that will bind the Veeam Kasten service account and
  namespace to the vault policy:

```
$ vault write auth/kubernetes/role/<vault_role> \    bound_service_account_names=crypto-svc \    bound_service_account_namespaces=kasten-io \    policies=<policy_name>
```

---

## Install Vmware Vsphere

## Prerequisites â

Before installing Veeam Kasten on VMware vSphere, please ensure that the install prerequisites are met.

Persistent Volumes must be provisioned using the vSphere CSI
provisioner or
  one of the other supported storage providers.

## Installing Veeam Kasten â

To backup volumes provisioned by the vSphere CSI driver, credentials
  must be provided. These credentials can be supplied either via Helm
  parameters or using a vSphere Infrastructure Profile .

### Providing the vSphere Credentials using Helm â

Setting up vSphere credentials requires configuring all of the following
  Helm flags during the execution of helm install or helm upgrade :

```
--set secrets.vsphereUsername=<vsphere username> \--set secrets.vspherePassword=<vsphere password> \--set secrets.vsphereEndpoint=<vsphere ip or hostname>
```

Also, it is possible to use an existing secret instead of setting
  credentials through Helm parameters:

```
--set secrets.vsphereClientSecretName=<secret name>
```

Please ensure that the secret exists in the namespace where Veeam Kasten
    is installed. The default namespace assumed throughout this
    documentation is kasten-io .

```
apiVersion: v1kind: Secretmetadata:  name: my-vsphere-creds  namespace: kasten-iodata:  vsphere_endpoint: MjMzODAyNWMEXAMPLEENDPOINT  vsphere_username: UlVMOFF+dnpwM1EXAMPLEUSERNAME  vsphere_password: YmEwN2JhEXAMPLEPASSWORDtype: Opaque
```

### Providing Credentials via the vSphere Infrastructure Profile â

```
$ helm install k10 kasten/k10 --namespace=kasten-io
```

Creation of a vSphere Infrastructure Profile is required to backup volumes provisioned by the vSphere CSI
  driver. Additional information related to the management of vSphere
  volumes is also found in the same section.

If a Veeam Repository will be used to export snapshot data of vSphere CSI volumes, then
  configuring Change Tracking on the nodes would enable more efficient
  incremental backups. Refer to this or later Knowledge Base
  articles for details.

## Validating the Install â

To validate that Veeam Kasten has been installed properly, the following
  command can be run in Veeam Kasten's namespace (the install default is kasten-io ) to watch for the status of all Veeam Kasten pods:

```
$ kubectl get pods --namespace kasten-io --watch
```

It may take a couple of minutes for all pods to come up but all pods
  should ultimately display the status of Running .

```
$ kubectl get pods --namespace kasten-ioNAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGEkasten-io     aggregatedapis-svc-b45d98bb5-w54pr      1/1     Running   0          1m26skasten-io     auth-svc-8549fc9c59-9c9fb               1/1     Running   0          1m26skasten-io     catalog-svc-f64666fdf-5t5tv             2/2     Running   0          1m26s...
```

In the unlikely scenario that pods that are stuck in any other state,
  please follow the support documentation to debug further.

### Validate Dashboard Access â

By default, the Veeam Kasten dashboard will not be exposed externally.
  To establish a connection to it, use the following kubectl command to
  forward a local port to the Veeam Kasten ingress port:

```
$ kubectl --namespace kasten-io port-forward service/gateway 8080:80
```

The Veeam Kasten dashboard will be available at http://127.0.0.1:8080/k10/#/ .

For a complete list of options for accessing the Kasten Veeam Kasten
  dashboard through a LoadBalancer, Ingress or OpenShift Route you can use
  the instructions here .

---

