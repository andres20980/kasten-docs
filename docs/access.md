## Access Documentation
### latest_access_access.md
## Accessing Veeam Kasten
- Dashboard Access
- API and Command Line
- Authentication
- Authorization
- Veeam Kasten RBAC
- Veeam Kasten RBAC Dashboard
-
- Accessing Veeam Kasten
One of the considerations when installing Veeam Kasten is deciding
how it will be accessible to users. The options that you will learn
about in this section can be included as part of the initial install
command or can be used with a helm upgrade (see more about
upgrade at Upgrading Veeam Kasten) command to modify an
existing installation.
The platform can be accessed through the Veeam Kasten Dashboard, through
the Veeam Kasten API, or the kubectl CLI.
© Copyright 2017-2024, Kasten, Inc.
### latest_access_authorization.md
## Authorization
- Dashboard Access
- API and Command Line
- Authentication
- Authorization
Administrative Access
Limited Access
Additional RBAC Access
- Administrative Access
- Limited Access
- Additional RBAC Access
- Veeam Kasten RBAC
- Veeam Kasten RBAC Dashboard
-
- Accessing Veeam Kasten
- Authorization
### Administrative Access
For admin access, make sure that when using kubectl or trying
to access the Veeam Kasten dashboard
with Token Authentication you authenticate with
a user that has a ClusterRoleBinding to the predefined k10-admin
role.
### Limited Access
Non-admin users may be granted limited permissions to Veeam Kasten.
Read-only access to the dashboard config is granted by creating a
ClusterRoleBinding between the user and the predefined
k10-config-view role. In addition, users may be granted operational
access to their applications by creating a RoleBinding to the
k10-basic role in their application's namespace.
### Additional RBAC Access
Veeam Kasten now supports a more flexible permissions model
which allows scoping of user permissions to perform Veeam Kasten
actions only within the context of specified applications.
Check out Veeam Kasten RBAC for more information.
© Copyright 2017-2024, Kasten, Inc.
### latest_access_dashboard.md
## Dashboard Access
- Dashboard Access
Access via kubectl
Veeam Kasten Dashboard Directly From the Google Cloud Console
Accessing via a LoadBalancer
Configuring DNS
Adding Custom Annotations
Existing Ingress Controller
Access via OpenShift Routes
- Access via kubectl
Veeam Kasten Dashboard Directly From the Google Cloud Console
- Veeam Kasten Dashboard Directly From the Google Cloud Console
- Accessing via a LoadBalancer
Configuring DNS
Adding Custom Annotations
- Configuring DNS
- Adding Custom Annotations
- Existing Ingress Controller
- Access via OpenShift Routes
- API and Command Line
- Authentication
- Authorization
- Veeam Kasten RBAC
- Veeam Kasten RBAC Dashboard
-
- Accessing Veeam Kasten
- Dashboard Access
There are several options for accessing the Veeam Kasten dashboard.
### Access via kubectl
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it use the following kubectl commands.
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/
Note
If you installed Veeam Kasten with a different release name than
k10 (specified via the --name option in the install
command), the above URL should be modified to replace the last
occurrence of k10 with the specified release name. The revised
URL would look like
http://127.0.0.1:8080/<release-name>/##/
If you are running on GKE and want to access the dashboard without local
kubectl access, you can use the following advanced GKE console
instructions:
### Accessing via a LoadBalancer
If you would like to expose the Veeam Kasten dashboard via an external
load balancer, you will need to configure an authentication method. The
currently supported options are Basic Authentication,
Token Authentication, or
OpenID Connect Authentication.
To configure the Veeam Kasten dashboard to be exposed through the default
LoadBalancer and potentially a DNS entry, please use the following helm
options. If you have not yet installed Veeam Kasten, add the options to the
install command for your environment. Alternatively, you can upgrade the
installation as follows:
### Configuring DNS
The Veeam Kasten dashboard will be available at the /k10/ URL path of the
DNS or IP address setup using the below options.
If you installed Veeam Kasten with a different release name than
k10 (specified via the --name option in the install
command), the dashboard will be available at the /<release-name>/
URL path.
### Using ExternalDNS
If your Kubernetes cluster is already using ExternalDNS and has it
properly configured, you should add the following options to
automatically configure a DNS entry for the load balancer.
### Manually adding a DNS entry
If your environment does not support ExternalDNS, first find the
LoadBalancer's public DNS/IP address:
You can then optionally setup a DNS record that points from a desired
FQDN to the LoadBalancer DNS or IP address from above.
### Adding Custom Annotations
In certain scenarios, custom annotations on the LoadBalancer be
required. These can be added as a part of the install process too. For
example, if an annotation of the form
service.beta.kubernetes.io/aws-loadbalancer-internal: 0.0.0.0/0
was needed, add it to a values file as follows:
and then use --values in the helm install command:
### Existing Ingress Controller
If there is already an Ingress controller installed and the goal is to
expose the Veeam Kasten dashboard through it, the following option must be
specified with the helm install command:
By default, the Ingress object is created with the name
{release-name}-ingress. To use a different name, specify the following
option:
It is necessary to follow the specific Ingress controller guidelines to
expose an external endpoint for the k10-ingress Kubernetes Ingress
object that will be installed in the kasten-io namespace as part of
the Helm installation.
Additionally, an Ingress class can be chosen for the Ingress object
by specifying the following option to the helm command:
In some environments, additional Ingress annotations might be required.
Required annotations can be added during install via the
ingress.annotations
option. For example, the below option will add
nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
to the Veeam Kasten Ingress resource.
By default, the Ingress is configured with the default path
/<release-name>/. A custom path can be specified for the Ingress using
the following option:
If you want to expose pre-installed Veeam Kasten with ingress, the
path in the ingress specs must be set to the release-name used while
installing Veeam Kasten.
To redirect the traffic that does not match the default path, a
defaultBackend can be optionally configured for the Ingress.
There are two possible options for configuring the defaultBackend:
1. Using a backing service:
1. Using a resource backend:
### Access via OpenShift Routes
To access the Veeam Kasten dashboard via an OpenShift Route,
an authentication method needs to be configured.
The currently supported authentication options are
Basic Authentication,
Token Authentication,
Active Directory,
Openshift Authentication,or
OpenID Connect Authentication.
The following Helm options can be used to configure the
Veeam Kasten dashboard to be exposed through an OpenShift Route and
potentially a DNS entry. If Veeam Kasten is not yet installed, add the
options to the helm install command for the environment.
Alternatively, the installation can be upgraded as follows:
The following option will auto-generate a route hostname as
a subdomain to the existing FQDN. A host name can be explicitly
with the route with the following option:
The ability to use the kubectl proxy method described above or
an externally accessible endpoint is still there but their configuration
depends on the specific cluster configuration.
Additionally, the path for the Route object can be specified by using
the following option:
If you want to expose pre-installed Veeam Kasten with route,
the path in the route specs must be set to the release-name used
while installing Veeam Kasten.
SSL/TLS with the Route can enabled by specifying the
following option:
Additionally, to specify the TLS insecureEdgeTerminationPolicy or
termination Route parameters, the following option needs
to be specified:
© Copyright 2017-2024, Kasten, Inc.
### latest_access_rbac_ui.md
## Veeam Kasten RBAC Dashboard
- Dashboard Access
- API and Command Line
- Authentication
- Authorization
- Veeam Kasten RBAC
- Veeam Kasten RBAC Dashboard
User Access
Admin Access
Multi Tenant Access
Read-Only Access
Customizing Access
- User Access
Admin Access
Multi Tenant Access
Read-Only Access
Customizing Access
- Admin Access
- Multi Tenant Access
- Read-Only Access
- Customizing Access
-
- Accessing Veeam Kasten
- Veeam Kasten RBAC Dashboard
The Veeam Kasten Role Based Access Control (RBAC) dashboard can be
used to setup varying levels of access to Veeam Kasten's dashboard
and APIs.
Note
This dashboard can be viewed only if the user is authorized to
view Kubernetes namespace-scoped Roles, Role Bindings and/or Cluster
Roles and Cluster Role Bindings. Refer RBAC
permissions for more information.
### User Access
Veeam Kasten allows users to manage Kubernetes access through the Veeam
Kasten dashboard. Users can create Role Bindings as well as Cluster Role
Bindings by choosing existing or creating new Roles and Cluster Roles.
Bindings are available for subject type Users and Groups. If a
Service Account binding is required, use the format
system:serviceaccount:<sa_namespace>:<sa_name> in the User field for a single
Service Account in a specific namespace. Alternatively, use the format
system:serviceaccounts:<sa_name> in the Group field for a Service
Account in all namespaces.
### Admin Access
To setup administrator access for a user or group, the Veeam Kasten
RBAC dashboard can be used to create a Cluster Role Binding. Select
the Cluster Role named k10-admin from the drop down. Provide one
or more users/groups while configuring the subjects of the Cluster
Role Binding.
### Multi Tenant Access
To setup access for users so that they can perform data protection
operations, only in their namespaces, the Veeam Kasten RBAC dashboard
can be used to create Role Binding(s) in a specific list of namespaces.
Select the Cluster Role named k10-basic from the drop down.
Provide one or more users/groups while configuring the subjects of
the Role Binding.
### Read-Only Access
To setup read-only access for users, the Veeam Kasten RBAC dashboard can
be used to create a Cluster Role Binding. Select the Cluster Role named
k10-config-view from the drop down. Provide one or more users/groups
while configuring the subjects of the Cluster Role Binding.
### Customizing Access
To customize access to Veeam Kasten dashboard and APIs, users can create
custom Roles and Cluster Roles and create corresponding Role Bindings and
Cluster Role Bindings using those Roles and Cluster Roles as well as the
default ones deployed when Veeam Kasten is installed.
Veeam Kasten will only display a table of permissions related to
Veeam Kasten resources, while creating Roles and Cluster Roles.
### Roles
Single or multiple Roles can be created via the Veeam Kasten dashboard.
Roles can be created for multiple namespaces by selecting them from the
drop down menu. A separate instance of the Role will be created in each
namespace.
Permissions are grouped into three categories: Read (get, list, and watch),
Write (create, update, and patch), and Delete (delete). These groups of
permissions can be applied to all Veeam Kasten resources, groups of Veeam
Kasten resources, or individual Veeam Kasten resources.
### Cluster Roles
A Cluster Role can be created by selecting the permissions from the
resources table.
### Role Bindings
Single or multiple Role Bindings can be created via the Veeam Kasten dashboard.
If a Role Binding is be created in a namespace, either a Cluster Role or a
Role from the corresponding namespace can be selected from the drop down menu.
If multiple Role Bindings are to be created, a Cluster Role can be selected
from the drop down.
### Cluster Role Bindings
A Cluster Role Binding can be created by choosing a Cluster Role from the
drop down. A Cluster Role Binding will give access throughout the entire
cluster.
Veeam Kasten will only display a subset of Roles and Cluster Roles which
cover Veeam Kasten APIs while creating Bindings.
© Copyright 2017-2024, Kasten, Inc.
### latest_access_rbac.md
## Veeam Kasten RBAC
- Dashboard Access
- API and Command Line
- Authentication
- Authorization
- Veeam Kasten RBAC
Default Veeam Kasten ClusterRoles
K10-Admin
K10-Basic
K10-Config-View
RBAC Permissions
- Default Veeam Kasten ClusterRoles
K10-Admin
K10-Basic
K10-Config-View
- K10-Admin
- K10-Basic
- K10-Config-View
- RBAC Permissions
- Veeam Kasten RBAC Dashboard
-
- Accessing Veeam Kasten
- Veeam Kasten RBAC
For facilitating role-based access for users, Veeam Kasten leverages
Kubernetes ClusterRoles and Bindings.
RBAC Overview
- Default Veeam Kasten ClusterRoles
K10-Admin
K10-Admin Binding
K10-Namespace-Admin
K10-Basic
K10-Basic ClusterRole
K10-Basic Binding
K10-Basic-Config ClusterRole
K10-Basic-Config Binding
K10-Config-View
K10-Config-View Binding
- K10-Admin
K10-Admin Binding
K10-Namespace-Admin
- K10-Admin Binding
- K10-Namespace-Admin
- K10-Basic
K10-Basic ClusterRole
K10-Basic Binding
K10-Basic-Config ClusterRole
K10-Basic-Config Binding
- K10-Basic ClusterRole
- K10-Basic Binding
- K10-Basic-Config ClusterRole
- K10-Basic-Config Binding
- K10-Config-View
K10-Config-View Binding
- K10-Config-View Binding
Default Veeam Kasten ClusterRoles
### Default Veeam Kasten ClusterRoles
Every Veeam Kasten deployment comes installed with three default
Veeam Kasten ClusterRoles: k10-admin, k10-basic, and k10-config-view.
### K10-Admin
The k10-admin ClusterRole is useful for administrators who want
uninterrupted access to all Veeam Kasten operations.
The k10-admin user is allowed to work with all Veeam Kasten APIs
including profiles, policies, policy presets, actions, restore points,
transform sets and blueprint bindings.
Note
k10-admin will be installed under the name <release_name>-admin
The following is an example of the k10-admin ClusterRole:
### K10-Admin Binding
The k10-admin ClusterRole needs a ClusterRoleBinding. The admin
access needs to be cluster-wide.
Veeam Kasten creates a ClusterRoleBinding for a default Group
k10:admins.  Admin users can be added to this k10:admin
Group and will be able to use the above k10-admin ClusterRole.
For individual users and service accounts, the k10-admin ClusterRole
needs a ClusterRoleBinding. The admin access needs to be cluster-wide.
To bind the k10-admin ClusterRole, use the following command
The above kubectl command will create the following ClusterRoleBinding object
Alternatively, you can also bind the ClusterRole to a ServiceAccount.
If you want k10-admin access given to existing users and do not want
to create new clusterrole bindings, you can add the rules from above
k10-admin role to existing cluster roles.
### K10-Namespace-Admin
The k10-ns-admin Role is added for secrets, configmaps access in the
Veeam Kasten release namespace.
k10-ns-admin will be installed under the name <release_name>-ns-admin
The following is an example of the k10-ns-admin Role:
The k10-ns-admin Role needs a RoleBinding in the release namespace.
Veeam Kasten creates a RoleBinding for a default Group k10:admins in the
Veeam Kasten release namespace. Admin users can be added to this Group
and will be able to use the above k10-ns-admin Role.
To bind the k10-ns-admin Role, use the following command
The above kubectl command will create the following RoleBinding object
Alternatively, you can also bind the Role to a ServiceAccount.
### K10-Basic
### K10-Basic ClusterRole
The k10-basic ClusterRole is useful for administrators who want to
give some operational Veeam Kasten access to users in specific namespaces.
A user with the k10-basic ClusterRole is allowed to backup and restore
applications in the namespaces they have access to. This user can
create policies in the application's namespace to backup and export
the application. The k10-basic ClusterRole also gives access to view
applications, actions, and restore point details in their namespaces.
A user with the k10-basic ClusterRole is also allowed to cancel
actions in the namespaces they have access to.
k10-basic will be installed under the name <release_name>-basic
The following is an example of the k10-basic ClusterRole:
### K10-Basic Binding
The k10-basic ClusterRole needs a RoleBinding in the namespace(s)
the user needs access to.
To bind the k10-basic ClusterRole, use the following command
If you want k10-basic access given to existing users and do not want
to create new role bindings, you can add the rules from above
k10-basic role to existing roles.
### K10-Basic-Config ClusterRole
The k10-basic-config ClusterRole can be used by administrators
to give basic users access to specific location profiles or
blueprints in Veeam Kasten's namespace.
An example of the k10-basic-config ClusterRole:
### K10-Basic-Config Binding
The k10-basic-config ClusterRole needs a RoleBinding in K10's namespace to
give access to basic users to specific location profiles or blueprints.
To bind the k10-basic-config ClusterRole, use the following command
### K10-Config-View
The k10-config-view ClusterRole is useful for administrators who
want to give K10 config view access to some users.
The k10-config-view ClusterRole gives a user read-only access
to K10 config information, including profiles, policies,
policy presets, transform sets and blueprint bindings on the dashboard.
k10-config-view will be installed under the name <release_name>-config-view
The following is an example of the k10-config-view ClusterRole:
### K10-Config-View Binding
The k10-config-view ClusterRole needs a ClusterRoleBinding. The
config-view access needs to be cluster-wide.
To bind the k10-config-view ClusterRole, use the following command
If you want k10-config-view access given to existing users and do
not want to create new clusterrole bindings, you can add the rules
from above k10-config-view role to existing cluster roles.
### RBAC Permissions
For viewing Kubernetes RBAC objects on the K10 Dashboard UI, additional RBAC
permissions are required for users.
The following Cluster Role will give access to list Kubernetes RBAC objects
across the cluster.
Warning
Although you can grant additional verbs such as create, update, and
delete this will allow users to escalate their own privileges. This allows them
to grant themselves administrative privileges.
Please refer to Kubernetes documentation for more details.
The corresponding Cluster Role Binding is needed to bind the Cluster Role
to users and groups.
© Copyright 2017-2024, Kasten, Inc.
### latest_access_authentication.md
## Authentication
- Dashboard Access
- API and Command Line
- Authentication
Direct Access
Basic Authentication
Token Authentication
Obtaining Tokens
Token-Based Authentication with AWS EKS
Obtaining Tokens with Red Hat OpenShift
OAuth Proxy with Red Hat OpenShift (Preview)
OpenID Connect Authentication
Cluster Setup
Veeam Kasten Setup
OpenShift Authentication
Extract Root CA certificates to the Veeam Kasten namespace
Install or Update Veeam Kasten with OpenShift Authentication
Extract Root CA certificates to the Veeam Kasten namespace
Manual OAuth Client Configuration
Sample Auth Flow with Screenshots
Active Directory Authentication
Veeam Kasten Setup
Sample Auth Flow with Screenshots
Troubleshooting
Other Authentication Options
Group Allow List
Veeam Kasten Admin Groups
Veeam Kasten Admin Users
- Direct Access
- Basic Authentication
- Token Authentication
Obtaining Tokens
Token-Based Authentication with AWS EKS
Obtaining Tokens with Red Hat OpenShift
OAuth Proxy with Red Hat OpenShift (Preview)
- Obtaining Tokens
- Token-Based Authentication with AWS EKS
- Obtaining Tokens with Red Hat OpenShift
- OAuth Proxy with Red Hat OpenShift (Preview)
- OpenID Connect Authentication
Cluster Setup
Veeam Kasten Setup
- Cluster Setup
- Veeam Kasten Setup
- OpenShift Authentication
Extract Root CA certificates to the Veeam Kasten namespace
Install or Update Veeam Kasten with OpenShift Authentication
Extract Root CA certificates to the Veeam Kasten namespace
Manual OAuth Client Configuration
Sample Auth Flow with Screenshots
- Extract Root CA certificates to the Veeam Kasten namespace
- Install or Update Veeam Kasten with OpenShift Authentication
- Manual OAuth Client Configuration
- Sample Auth Flow with Screenshots
- Active Directory Authentication
Veeam Kasten Setup
Sample Auth Flow with Screenshots
Troubleshooting
- Troubleshooting
- Other Authentication Options
Group Allow List
Veeam Kasten Admin Groups
Veeam Kasten Admin Users
- Group Allow List
- Veeam Kasten Admin Groups
- Veeam Kasten Admin Users
- Authorization
- Veeam Kasten RBAC
- Veeam Kasten RBAC Dashboard
-
- Accessing Veeam Kasten
- Authentication
Veeam Kasten offers a variety of different ways to secure access to its
dashboard and APIs:
- Token Authentication
Obtaining Tokens
Token-Based Authentication with AWS EKS
Obtaining Tokens with Red Hat OpenShift
OAuth Proxy with Red Hat OpenShift (Preview)
Configuration
Forwarding Traffic to the Proxy
Sample Auth Flow with Screenshots
Additional Documentation
- OAuth Proxy with Red Hat OpenShift (Preview)
Configuration
Forwarding Traffic to the Proxy
Sample Auth Flow with Screenshots
Additional Documentation
- Configuration
- Forwarding Traffic to the Proxy
- Additional Documentation
- OpenID Connect Authentication
Cluster Setup
Veeam Kasten Setup
Provider Redirect URI Authorizations
Veeam Kasten Configuration
Existing Secret Usage
- Veeam Kasten Setup
Provider Redirect URI Authorizations
Veeam Kasten Configuration
Existing Secret Usage
- Provider Redirect URI Authorizations
- Veeam Kasten Configuration
- Existing Secret Usage
- OpenShift Authentication
Extract Root CA certificates to the Veeam Kasten namespace
Install or Update Veeam Kasten with OpenShift Authentication
Extract Root CA certificates to the Veeam Kasten namespace
Manual Root CA Certificates Extraction
Manual OAuth Client Configuration
Manual Client Service Account Creation
Manual Client Secret Creation
Sample Auth Flow with Screenshots
- Extract Root CA certificates to the Veeam Kasten namespace
Manual Root CA Certificates Extraction
- Manual Root CA Certificates Extraction
- Manual OAuth Client Configuration
Manual Client Service Account Creation
Manual Client Secret Creation
- Manual Client Service Account Creation
- Manual Client Secret Creation
- Active Directory Authentication
Veeam Kasten Setup
Sample Auth Flow with Screenshots
Troubleshooting
Common Name Certificates
- Troubleshooting
Common Name Certificates
- Common Name Certificates
- Other Authentication Options
Group Allow List
Veeam Kasten Admin Groups
Veeam Kasten Admin Users
Token Authentication
OpenID Connect Authentication
OpenShift Authentication
Active Directory Authentication
Other Authentication Options
### Direct Access
When exposing the Veeam Kasten dashboard externally, it is required that
an authentication method is properly configured to secure access.
Please note that the token-based authentication is always enabled
as a secondary authentication type to let Veeam Kasten Multi-Cluster Manager
components and Veeam Backup & Replication services work with Veeam Kasten.
If accessing the Veeam Kasten API directly or using kubectl, any
authentication method configured for the cluster is acceptable. For
more information, see
Kubernetes authentication.
Warning
When using Direct Access, there is no RBAC set on Veeam Kasten.
Any user who has access to the dashboard can perform all Veeam Kasten
operations which is not advisable if granular access is needed.
### Basic Authentication
Basic Authentication allows you to protect access to the Veeam Kasten
dashboard with a user name and password. To enable Basic Authentication,
you will first need to generate
htpasswd
credentials by either using an online tool or via the
htpasswd binary found on most systems.  Once generated, you need to
supply the resulting string with the helm install or upgrade command
using the following flags.
Alternatively, you can use an existing secret that contains a file created
with htpasswd. The secret must be in the Veeam Kasten namespace. This
secret must be created with the key named auth and the value as the
password generated using htpasswd in the data field of the secret.
When using Basic Authentication, there is no RBAC set on Veeam Kasten.
Any user who has access to the dashboard can perform all Veeam Kasten
operations which is not advisable if granular access is needed.
### Token Authentication
To enable token authentication use the following flag as part of the
initial Helm install or subsequent Helm upgrade command.
Once the dashboard is configured, you will be prompted to provide a
bearer token that will be used when accessing the dashboard.
### Obtaining Tokens
Token authentication allows using any token that can be verified by
the Kubernetes server. For details on the supported token types
see Authentication Strategies.
The most common token type that you can use is a service account bearer token.
You can use kubectl to obtain such a token for a service account
that you know has the proper permissions.
For example, assuming that Veeam Kasten is installed in the kasten-io
namespace and the ServiceAccount is named my-kasten-sa:
1. Generate a token with an expiration period (recommended practice):
$ kubectl --namespace kasten-io create token my-kasten-sa --duration=24h
Generate a token with an expiration period (recommended practice):
Note
kubectl client version of 1.24 or higher is required to create a token resource.
1. Create a secret for the desired service account
and fetch a permanent token:
$ desired_token_secret_name=my-kasten-sa-token
$ kubectl apply --namespace=kasten-io --filename=- <<EOF
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: ${desired_token_secret_name}
  annotations:
    kubernetes.io/service-account.name: "my-kasten-sa"
EOF
$ kubectl get secret ${desired_token_secret_name} --namespace kasten-io -ojsonpath="{.data.token}" | base64 --decode
Create a secret for the desired service account
and fetch a permanent token:
Prior to Kubernetes 1.24, the token must be extracted from a service
account's secret:
If a suitable service account doesn't already exist, one can be created with:
The new service account will need appropriate role bindings or cluster role
bindings in order to use it within Veeam Kasten. To learn more about
the necessary Veeam Kasten permissions, see Authorization.
### Token-Based Authentication with AWS EKS
For more details on how to set up token-based authentication with AWS EKS,
please follow the following documentation.
- Enabling AWS IAM Token-Based Auth for EKS
Creating IAM Policies and Roles
Installing and Configuring Veeam Kasten
Configuring RBAC
Logging into the Veeam Kasten Dashboard using AWS IAM Tokens
Debugging Login Issues
- Creating IAM Policies and Roles
- Installing and Configuring Veeam Kasten
- Configuring RBAC
- Logging into the Veeam Kasten Dashboard using AWS IAM Tokens
Debugging Login Issues
- Debugging Login Issues
### Obtaining Tokens with Red Hat OpenShift
An authentication token can be obtained from Red Hat OpenShift via the
OpenShift Console by clicking on your user name in the top right
corner of the console and selecting Copy Login
Command. Alternatively, the token can also be obtained by using the
following command:
### OAuth Proxy with Red Hat OpenShift (Preview)
The OpenShift OAuth proxy can be used for authenticating access to Veeam
Kasten. The following resources have to be deployed in order to setup
OAuth proxy in the same namespace as Veeam Kasten.
### Configuration
ServiceAccount
Create a ServiceAccount that is to be used by the OAuth proxy deployment
Cookie Secret
Create a Secret that is used for encrypting the cookie created by the proxy.
The name of the Secret will be used in the configuration of the OAuth proxy.
ConfigMap for OpenShift Root CA
Create a ConfigMap annotated with the inject-cabundle OpenShift
annotation. The annotation results in the injection of OpenShift's root
CA into the ConfigMap. The name of this ConfigMap is used in the
configuration of the OAuth proxy.
NetworkPolicy
Create a NetworkPolicy to allow ingress traffic on port 8080 and port 8083 to
to be forwarded to the OAuth proxy service.
Service
Deploy a Service for OAuth proxy. This needs to be annotated with the
serving-cert-secret-name annotation. This will result in OpenShift
generating a TLS private key and certificate that will be used by the
OAuth proxy for secure connections to it. The name of the Secret used
with the annotation must match with the name used in the OAuth proxy
deployment.
Deployment
Next, a Deployment for OAuth proxy needs to be created. It is recommended
that a separate OpenShift OAuth client be registered for this purpose.
The name of the client and its Secret will be used with the --client-id
and --client-secret configuration options respectively.
When an OpenShift ServiceAccount was used as the OAuth client, it
was observed that the token generated by the proxy did not have sufficient
scopes to operate Veeam Kasten. It is therefore not recommended to deploy the proxy
using an OpenShift ServiceAccount as the OAuth client.
It is also important to configure the --pass-access-token with the proxy
so that it includes the OpenShift token in the
X-Forwarded-Access-Token header when forwarding a request to Veeam Kasten.
The --scope configuration must have the user:full scope to ensure that
the token generated by the proxy has sufficient scopes for operating Veeam Kasten.
The --upstream configuration must point to the Veeam Kasten gateway
Service.
OAuth Client
As mentioned earlier, it is recommended that a new OpenShift OAuth client be.
registered.
The redirectURIs has to point to the domain name where Veeam Kasten is
accessible. For example if Veeam Kasten is available at https://example.com/k10,
the redirect URI should be set to https://example.com.
The name of this client must match with the --client-id configuration in
the OAuth proxy deployment.
The Secret in this client must match with the --client-secret configuration
in the OAuth proxy deployment.
The grantMethod can be either prompt or auto.
### Forwarding Traffic to the Proxy
Traffic meant for Veeam Kasten must be forwarded to the OAuth proxy for
authentication before it reaches Veeam Kasten. Ensure that ingress traffic
on port 80 is forwarded to port 8080 and traffic on port 443 is forwarded to
port 8083 of the oauth-proxy-svc Service respectively.
Here is one example of how to forward traffic to the proxy.
In this example, Veeam Kasten was deployed with an external gateway Service.
The gateway Service's ports were modified to forward traffic like so:
### Sample Auth Flow with Screenshots
This section is meant to provide an example of configuring
authentication and authorization for operating Veeam Kasten in an
OpenShift cluster to help provide an end to end picture of the Auth flow
when working with the OAuth proxy.
- Okta was configured as the OIDC provider in the OpenShift cluster.
- An OpenShift group called k10-admins was created and users were
added to this group.
- A cluster role binding was created to bind the k10-admins group to the
k10-admin cluster role.
- A role binding was created to map the k10-admins group to the
k10-ns-admin role in the Veeam Kasten namespace.
- When the user navigates to the Veeam Kasten dashboard, the request
reaches the proxy. The proxy presents a login screen to the user.
- After clicking the login button, the user is forwarded to the OpenShift
login screen. The OpenShift screen will provide the option of selecting
kube:admin or the OIDC option if it has been configured in
the cluster.
- After clicking on the OIDC option okta in this example, the OIDC
provider's login screen is shown.
- When authentication with the OIDC provider succeeds,
the user is redirected to the Veeam Kasten dashboard.
### Additional Documentation
For more information about the OpenShift OAuth proxy, refer to the
documentation here.
### OpenID Connect Authentication
For more information regarding TLS restrictions with Kasten, please
refer to this documentation.
Veeam Kasten supports the ability to obtain a token from an OIDC provider
and then use that token for authentication. Veeam Kasten extracts the user's
ID from the token and uses Kubernetes User Impersonation with that ID to
ensure that user-initiated actions (via the API, CLI or dashboard) are
attributed to the authenticated user.
It also supports a refresh token workflow for OIDC, which ensures that
authenticated sessions remain active even after access tokens have expired.
This feature eliminates the need for frequent re-authentication, thereby
enhancing usability. This workflow is disabled by default. You need to
enable it using the auth.oidcAuth.refreshTokenSupport helm flag and you
might need to do some additional configuration changes to your OIDC provider.
Each OIDC provider will have different requirements to enable support for
token refresh, please refer to their documentation to make sure it is properly
enabled.
When configuring your OIDC provider to support the refresh token workflow,
please make sure that it allows the offline_access scope.
The standard OIDC documentation contains detailed descriptions
of how token refresh works. No additional configuration is necessary on
the Veeam Kasten side.
Helm Flags for Refresh Token Workflow
The refresh token workflow and Veeam Kasten UI session can be managed using
the two new flags listed below:
1. auth.oidcAuth.refreshTokenSupport: This flag enables or disables
the refresh token workflow.
2. auth.oidcAuth.sessionDuration: This flag sets the duration
of the Veeam Kasten UI session when using OIDC authentication. It manages
how often users are prompted to re-authenticate.
### Cluster Setup
Veeam Kasten works with your OIDC provider irrespective of whether the
Kubernetes cluster is configured with the same OIDC provider, a
different OIDC provider, or without any identity providers.
For configuring a cluster with OIDC Tokens see
OpenID Connect(OIDC) Token.
For more information on the Kubernetes API configuration options, see
Configuring the API Server.
When working with a hosted Kubernetes offering (e.g. GKE, AKS, IKS) there will
usually be specific instruction on how to enable this since you may not be
able to explicitly configure the Kubernetes API server.
Overall, this portion of the configuration is beyond the scope of the
Veeam Kasten product and is part of the base setup of your Kubernetes cluster.
### Veeam Kasten Setup
### Provider Redirect URI Authorizations
As part of the exchange with the OIDC provider, Veeam Kasten will include a
redirect URL in its request to the provider. The provider will return the
user to that endpoint after the user has been authenticated. If the OIDC
provider that you are using requires that redirects are specifically
authorized, you will need to add the redirect URL to the provider's allow-list:
- For a Veeam Kasten instance exposed externally use
https://<URL to k10 gateway service>/<k10 release name>/auth-svc/v0/oidc/redirect
- For a Veeam Kasten instance exposed through kubectl port-forward use
http://127.0.0.1:<forwarding port>/<k10 release name>/auth-svc/v0/oidc/redirect
### Veeam Kasten Configuration
The final step is providing Veeam Kasten with the settings needed to initiate
the OIDC workflow and obtain a token.
- Enable OIDC
To enable OIDC based authentication use the following flag as part of the
initial Helm install or subsequent Helm upgrade command.
--set auth.oidcAuth.enabled=true
- OIDC Provider
This is a URL for OIDC provider. If the Kubernetes API server and Veeam
Kasten share the same OIDC provider, use the same URL that was used when
configuring the --oidc-issuer-url option of the API server.
Use the following Helm option:
--set auth.oidcAuth.providerURL=<provider URL>
- Redirect URL
This is the URL to the Veeam Kasten gateway service.
Use https://<URL to k10 gateway service> for Veeam Kasten exposed
externally or http://127.0.0.1:<forwarding port> for Veeam Kasten
exposed through kubectl port-forward.
Use the following Helm option:
--set auth.oidcAuth.redirectURL=<gateway URL>
- OIDC Scopes
This option defines the scopes that should be requested from the OIDC
provider. If the Kubernetes API server and Veeam Kasten share the same
OIDC provider, use the same claims that were requested when configuring
the --oidc-username-claim option of the API server.
Use the following Helm option:
--set auth.oidcAuth.scopes=<space separated scopes. Quoted if multiple>
- OIDC Prompt
If provided, this option specifies whether the OIDC provider must
prompt the user for consent or re-authentication. The well known
values for this field are select_account, login, consent, and
none. Check the OIDC provider's documentation to determine
what value is supported. The default value is select_account.
Use the following Helm option:
--set auth.oidcAuth.prompt=<prompt>
- OIDC Client ID
This option defines the Client ID that is registered with the OIDC Provider.
If the Kubernetes API server and Veeam Kasten share the same OIDC provider,
use the same client ID specified when configuring the --oidc-client-id
option of the API server.
Use the following Helm option:
--set auth.oidcAuth.clientID=<client id string>
- OIDC Client Secret
This option defines the Client Secret that corresponds to the Client ID
registered. You should have received this value from the OIDC provider
when registering the Client ID.
Use the following Helm option:
--set auth.oidcAuth.clientSecret=<secret string>
- OIDC User Name Claim
This option defines the OpenID claim that has to be used by Veeam Kasten
as the user name. It will be used by Veeam Kasten for impersonating the user
while interacting with the Kubernetes API server for authorization.
If not provided, the default claim is sub. This user name must
match the User defined in the role bindings described here: Veeam Kasten RBAC.
Use the following Helm option:
--set auth.oidcAuth.usernameClaim=<username claim>
- OIDC User Name Prefix
If provided, all usernames will be prefixed with this value.
If not provided, username claims other than email are
prefixed by the provider URL to avoid clashes. To skip any
prefixing, provide the value -.
Use the following Helm option:
--set auth.oidcAuth.usernamePrefix=<username prefix>
- OIDC Group Name Claim
If provided, this specifies the name of a custom OpenID
Connect claim to be used by Veeam Kasten to identify the groups
that a user belongs to. The groups and the username
will be used by Veeam Kasten for impersonating the user while
interacting with the Kubernetes API server for authorization.
To ensure that authorization for the user is successful,
one of the groups should match with a Kubernetes group
that has the necessary role bindings to allow the user
to access Veeam Kasten.
If the user is an admin user, then the user is most likely
set up with all the required permissions for accessing Veeam
Kasten and no new role bindings are necessary.
To avoid creating new role bindings for non-admin users every
time a new user needs to be added to the list of users who will
operate Veeam Kasten, consider adding the user to a group such
as my-K10-admins in the OIDC provider and add that user to
the same group in the Kubernetes cluster. Create role bindings
to associate the my-K10-admins group with a cluster role -
k10-admin and namespace scoped role - k10-ns-admin
(see Veeam Kasten RBAC for more information about these roles that are
created by Veeam Kasten as part of the installation process).
This ensures that once a user is authenticated successfully with
the OIDC provider, if the groups information from the provider
matches the groups information in Kubernetes, it will authorize
the user for accessing Veeam Kasten.
Note that instead of my-k10-admins, if the user is added
to k10:admins in the OIDC provider and to the same
group in the Kubernetes cluster, no additional role bindings
need to be created since Veeam Kasten creates them as a part of the
installation process.
For more information about role bindings - Veeam Kasten RBAC.
Use the following Helm option:
--set auth.oidcAuth.groupClaim=<group claim>
- OIDC Group Prefix
If provided, all groups will be prefixed with this value
to prevent conflicts. To disable the group prefix, either
remove this setting or set it to "".
Use the following Helm option:
--set auth.oidcAuth.groupPrefix=<group prefix>
Enable OIDC
To enable OIDC based authentication use the following flag as part of the
initial Helm install or subsequent Helm upgrade command.
OIDC Provider
This is a URL for OIDC provider. If the Kubernetes API server and Veeam
Kasten share the same OIDC provider, use the same URL that was used when
configuring the --oidc-issuer-url option of the API server.
Use the following Helm option:
Redirect URL
This is the URL to the Veeam Kasten gateway service.
Use https://<URL to k10 gateway service> for Veeam Kasten exposed
externally or http://127.0.0.1:<forwarding port> for Veeam Kasten
exposed through kubectl port-forward.
OIDC Scopes
This option defines the scopes that should be requested from the OIDC
provider. If the Kubernetes API server and Veeam Kasten share the same
OIDC provider, use the same claims that were requested when configuring
the --oidc-username-claim option of the API server.
OIDC Prompt
If provided, this option specifies whether the OIDC provider must
prompt the user for consent or re-authentication. The well known
values for this field are select_account, login, consent, and
none. Check the OIDC provider's documentation to determine
what value is supported. The default value is select_account.
OIDC Client ID
This option defines the Client ID that is registered with the OIDC Provider.
If the Kubernetes API server and Veeam Kasten share the same OIDC provider,
use the same client ID specified when configuring the --oidc-client-id
option of the API server.
OIDC Client Secret
This option defines the Client Secret that corresponds to the Client ID
registered. You should have received this value from the OIDC provider
when registering the Client ID.
OIDC User Name Claim
This option defines the OpenID claim that has to be used by Veeam Kasten
as the user name. It will be used by Veeam Kasten for impersonating the user
while interacting with the Kubernetes API server for authorization.
If not provided, the default claim is sub. This user name must
match the User defined in the role bindings described here: Veeam Kasten RBAC.
OIDC User Name Prefix
If provided, all usernames will be prefixed with this value.
If not provided, username claims other than email are
prefixed by the provider URL to avoid clashes. To skip any
prefixing, provide the value -.
OIDC Group Name Claim
If provided, this specifies the name of a custom OpenID
Connect claim to be used by Veeam Kasten to identify the groups
that a user belongs to. The groups and the username
will be used by Veeam Kasten for impersonating the user while
interacting with the Kubernetes API server for authorization.
To ensure that authorization for the user is successful,
one of the groups should match with a Kubernetes group
that has the necessary role bindings to allow the user
to access Veeam Kasten.
If the user is an admin user, then the user is most likely
set up with all the required permissions for accessing Veeam
Kasten and no new role bindings are necessary.
To avoid creating new role bindings for non-admin users every
time a new user needs to be added to the list of users who will
operate Veeam Kasten, consider adding the user to a group such
as my-K10-admins in the OIDC provider and add that user to
the same group in the Kubernetes cluster. Create role bindings
to associate the my-K10-admins group with a cluster role -
k10-admin and namespace scoped role - k10-ns-admin
(see Veeam Kasten RBAC for more information about these roles that are
created by Veeam Kasten as part of the installation process).
This ensures that once a user is authenticated successfully with
the OIDC provider, if the groups information from the provider
matches the groups information in Kubernetes, it will authorize
the user for accessing Veeam Kasten.
Note that instead of my-k10-admins, if the user is added
to k10:admins in the OIDC provider and to the same
group in the Kubernetes cluster, no additional role bindings
need to be created since Veeam Kasten creates them as a part of the
installation process.
For more information about role bindings - Veeam Kasten RBAC.
OIDC Group Prefix
If provided, all groups will be prefixed with this value
to prevent conflicts. To disable the group prefix, either
remove this setting or set it to "".
Below is a summary of all the options together. These options
can be included as part of the initial install command or
can be used with a helm upgrade (see more about
upgrade at Upgrading Veeam Kasten) command to modify an
existing installation.
### Existing Secret Usage
It is possible to use an existing secret
to provide the following parameters for OIDC configuration:
- OIDC Client IDThe Client ID that is registered with the OIDC Provider.
Field name - client-id
- OIDC Client SecretThe Client Secret that corresponds to the registered Client ID.
Field name - client-secret
The Client ID that is registered with the OIDC Provider.
Field name - client-id
The Client Secret that corresponds to the registered Client ID.
Field name - client-secret
Please ensure that the secret exists in the namespace where Veeam Kasten
is installed.
The default namespace assumed throughout this documentation is kasten-io.
Additionally, ensure that the Secret contains both the client-id
and client-secret fields with valid values.
If both the auth.oidcAuth.clientSecretName and auth.oidcAuth.clientID
auth.oidcAuth.clientSecret Helm values are set, the content of the
Secret referred by clientSecretName will be used.
### OpenShift Authentication
This mode can be used to authenticate access to Veeam Kasten
using OpenShift's OAuth server.
### Extract Root CA certificates to the Veeam Kasten namespace
To interact with the OpenShift's OAuth server, Veeam Kasten requires
Root CA certificates from the OpenShift cluster to be extracted to
the Veeam Kasten namespace.
To extract the Root CA certificates, please use the command-line tool
documented in the
Extracting OpenShift CA Certificates section
or refer to the
Manual Root CA Certificates Extraction
section.
### Install or Update Veeam Kasten with OpenShift Authentication
Veeam Kasten can be installed onto an OpenShift cluster either through
the Red Hat Operator or by using a Helm command, as described in the
Installing Veeam Kasten on Red Hat OpenShift section. Depending on the
selected method, the appropriate Veeam Kasten configuration should be
applied.
For example, if installed using the OpenShift Operator, the configuration must
be applied using the OpenShift Veeam Kasten Operand YAML, not through Helm
upgrade.
By default, Veeam Kasten automatically configures the OAuth Client during
installation.This process includes extracting the Root CA certificates,
creating the OAuth Client Service Account, and generating the corresponding
secret. If manual configuration is preferred, please refer to the section
on Manual OAuth Client Configuration.
Red Hat OpenShift Operator Configuration
To enable this mode of authentication when installing or upgrading via the
Red Hat OpenShift Operator, enable the configuration options below while
installing or upgrading Veeam Kasten. The following section provides detailed
explanations for each value, as specified by the corresponding Helm flag.
Helm-based Configuration
When installing or upgrading Veeam Kasten using Helm, enable the Helm
options below to activate this authentication mode.
The following section provides detailed explanations for each Helm
value:
- Enable OpenShift Authentication
To enable OpenShift-based authentication, use the following
flag as part of the initial Helm install or subsequent Helm
upgrade command:
--set auth.openshift.enabled=true
- Veeam Kasten's Dashboard URL
Provide the URL used for accessing Veeam Kasten's dashboard. Assuming
the base domain is mydomain.com, the Veeam Kasten namespace
is kasten-io, the Veeam Kasten release name is k10, and the
route.enabled Helm value is set to true. In this case,
the auth.openshift.dashboardURL Helm value will be the following:
--set auth.openshift.dashboardURL="https://k10-route-kasten-io.apps.mydomain.com/k10"
- OpenShift API Server URL
Provide the URL for accessing OpenShift's API server. For example, if the
base domain is mydomain.com, the auth.openshift.openshiftURL
Helm value will be the following:
--set auth.openshift.openshiftURL="https://api.mydomain.com:6443"
- Disabling TLS verification to OpenShift API server
The default value for this setting is false, indicating that connections
to the API server are secure by default. The TLS connections to
the API server are verified.
To disable TLS verification, set this value to true.
Use the following Helm option to enable or disable TLS
verification of connections to OpenShift's API server.
--set auth.openshift.insecureCA=false
Note
For security reasons, disabling TLS verification to the OpenShift
API server in a production environment is strongly discouraged.
Enable OpenShift Authentication
To enable OpenShift-based authentication, use the following
flag as part of the initial Helm install or subsequent Helm
upgrade command:
Veeam Kasten's Dashboard URL
Provide the URL used for accessing Veeam Kasten's dashboard. Assuming
the base domain is mydomain.com, the Veeam Kasten namespace
is kasten-io, the Veeam Kasten release name is k10, and the
route.enabled Helm value is set to true. In this case,
the auth.openshift.dashboardURL Helm value will be the following:
OpenShift API Server URL
Provide the URL for accessing OpenShift's API server. For example, if the
base domain is mydomain.com, the auth.openshift.openshiftURL
Helm value will be the following:
Disabling TLS verification to OpenShift API server
The default value for this setting is false, indicating that connections
to the API server are secure by default. The TLS connections to
the API server are verified.
To disable TLS verification, set this value to true.
Use the following Helm option to enable or disable TLS
verification of connections to OpenShift's API server.
For security reasons, disabling TLS verification to the OpenShift
API server in a production environment is strongly discouraged.
### Extract Root CA certificates to the Veeam Kasten namespace
To interact with the OpenShift OAuth server, Veeam Kasten requires
Root CA certificates from the OpenShift cluster to be added to
the custom CA bundle ConfigMap in the Veeam Kasten namespace. By default,
the extraction of the required certificates is performed automatically
during installation and upgrades.
Using the automated process for CA extraction is recommended unless
otherwise instructed by Kasten support.
To disable automatic CA certificate extraction:
- For Operator-based installations:
Set K10 > spec > auth > openshift > caCertsAutoExtraction to false
- For Helm-based installations:
Set auth.openshift.caCertsAutoExtraction to false
In this case, please use the command-line tool documented in the
Extracting OpenShift CA Certificates section
or refer to the
Manual Root CA Certificates Extraction
section to extract the Root CA certificates.
### Manual Root CA Certificates Extraction
Depending on the OpenShift cluster's configuration,
there are two methods to obtain a certificate.
If a cluster-wide proxy is
not used, then use Method 1 documented below.
Otherwise use Method 2 documented below.
If you are using a third-party signed certificate for OpenShift instead of a self-signed certificate, it is important to ensure that the third-party signed certificate and CA are used within the Veeam Kasten config map.
Method 1: Obtain certificates from the Openshift Ingress
and External Load Balancer
In the OpenShift-Ingress-Operator namespace, the Secret Router is responsible
for routing encrypted traffic between the
client
and the target service. This encrypted traffic is usually in the form of
HTTPS requests.
The Secret Router uses a certificate stored in a Kubernetes Secret object to
encrypt the traffic.
Example for self-signed certificates in OpenShift
If using default or self-signed certificates in Openshift, in addition to
the Secret Router, the certificate from the Open Shift External Load Balancer
is required for Veeam Kasten to send authentication requests
to the OpenShift API server.
Example for thirdy-party signed certificates in OpenShift
If using 3rd party API server certificate in OpenShift, in addition to
the Secret Router, the certificate configured for the API server
is required for Veeam Kasten to send authentication requests to the OpenShift
API Server.
Alternatively, the API Server Certificate can be exported from a web browser: https://<Open Shift API Server URI>:6443/.well-known/oauth-authorization-server
Method 2: Obtain certificate from the OpenShift cluster-wide proxy
The OpenShift Proxy is responsible for routing incoming requests
to the appropriate service or pod in the cluster.
The proxy can perform various functions such as load balancing,
SSL termination, URL rewriting, and request forwarding.
The name of the Root CA certificate must be custom-ca-bundle.pem
Create a ConfigMap that will contain the certificate
Provide the name of the ConfigMap using K10 > spec > cacertconfigmap > name
for the Operator config or as a Helm option cacertconfigmap.name.
### Manual OAuth Client Configuration
### Manual Client Service Account Creation
By default, Veeam Kasten automatically generates the Client Service
Account and its corresponding secret. To use a manually created
Service Account, perform the steps described in this section.
Before installing or upgrading Veeam Kasten, a Service Account must
be created in the namespace where Veeam Kasten will be installed or
upgraded. This Service Account represents an OAuth client that will
interact with OpenShift's OAuth server.
Assuming Veeam Kasten is installed in the namespace kasten-io,
deployed with the release name k10, and the URL for accessing Veeam
Kasten is https://k10-route-kasten-io.apps.mydomain.com/k10, use
the following command to create a Service Account named k10-dex-sa
annotated with the serviceaccounts.openshift.io/oauth-redirecturi.dex
annotation. This annotation registers the Service Account as an OAuth
client with the OpenShift OAuth server.
Ensure that the redirect URI specified in the ServiceAccount
annotation uses the correct protocol for the Veeam Kasten callback.
In most cases, it is the HTTPS, but it depends on the value of the
K10 > spec > route > tls > enabled parameter for the OpenShift Operator
or the --route.tls.enabled flag in Helm.
It also depends on the configuration of the K8s Ingress or the Service used
to expose the Veeam Kasten.
Provide the name of the Service Account using
K10 > spec > auth > openshift > serviceAccount for the Operator config or
as a Helm option auth.openshift.serviceAccount.
### Manual Client Secret Creation
By default, Veeam Kasten automatically generates the corresponding client
secret required to connect to the OpenShift OAuth server for the Service
Account, whether it is automatically or manually created. Choose one of
the options described in this section to use a manually created secret.
To manually create the Service Account token to be used in
K10 > spec > auth > openshift > clientSecret for the Operator config or
as a Helm option auth.openshift.clientSecret, follow these steps:
1. Creating the Secret: This secret will be associated with the k10-dex-sa
Service Account.
Run the following commands:
2. Retrieving the Token: Use the following command to get the token from the
Secret:
An alternative approach is to provide the name of an existing secret
containing a token. This approach can be achieved by passing
the secret name (e.g. k10-dex-sa-secret) to the
K10 > spec > auth > openshift > clientSecretName for
the Operator config or as the Helm option auth.openshift.clientSecretName.
Ensure that the secret exists in the Veeam Kasten namespace and contains
a valid token in the .data.token field of the secret.
If both auth.openshift.clientSecret and auth.openshift.clientSecretName are provided, the token referenced by name will be used.
### Sample Auth Flow with Screenshots
This section shows screenshots depicting the Auth flow
when Veeam Kasten is installed with OpenShift authentication.
- When the user navigates to the Veeam Kasten dashboard, the user
is redirected to OpenShift's login screen.
### Active Directory Authentication
This mode allows access to Veeam Kasten to be authenticated using an Active
Directory or LDAP server.
To enable this authentication mode, make sure that you enable the
specified Helm options during the installation or upgrade of Veeam Kasten.
The detailed descriptions of the required and optional Helm values
are provided below:
The complete list of configurable parameters is available in
Advanced Install Options.
Because of the behavior of the --set option, if you need to use commas
within LDAP values, you must escape them. For example,
Alternatively, you can define the values in a Helm values file without
escaping the commas. Then, you can use the file by using the -f option
with the helm install or upgrade command.
For example, helm upgrade k10 kasten/k10 --namespace kasten-io -f path_to_values_file.
### Veeam Kasten Setup
- Enable Active Directory Authentication
To enable Active Directory based authentication use the following
flag as part of the initial Helm install or subsequent Helm
upgrade command.
--set auth.ldap.enabled=true
- Restart the Authentication Pod
If the Helm option auth.ldap.bindPWSecretName has been used
to specify the name of the secret that contains the Active Directory
bind password, and if this password is modified after Veeam Kasten
has been installed, use this Helm option to restart the Authentication
Service's Pod as part of the Helm upgrade command.
--set auth.ldap.restartPod=true
- Veeam Kasten's Dashboard URL
Provide the URL used for accessing Veeam Kasten's dashboard using the
following Helm option.
--set auth.ldap.dashboardURL="https://<URL to k10 gateway service>/<k10 release name>"
- Active Directory/LDAP host
Provide the host and optional port of the AD/LDAP server in the form
host:port using the following Helm option.
--set auth.ldap.host="host:port"
- Disable SSL
Set this field to true if the Active Directory/LDAP host is not using TLS,
using the following Helm option.
--set auth.ldap.insecureNoSSL="true"
- Disable SSL verification
Use the following helm option to set this field to true to disable SSL
verification of connections to the Active Directory/LDAP server.
--set auth.ldap.insecureSkipVerifySSL="true"
- Start TLS
When set to true, ldap:// is used to connect to the server followed by
creation of a TLS session. When set to false, ldaps:// is used.
--set auth.ldap.startTLS="true"
- Bind Distinguished Name
Use this helm option to provide the Distinguished Name(username)
used for connecting to the Active Directory/LDAP host.
--set auth.ldap.bindDN="cn=admin,dc=example,dc=org"
- Bind Password
Use this helm option to provide the password corresponding to the
bindDN for connecting to the Active Directory/LDAP host.
--set auth.ldap.bindPW="password"
- Bind Password Secret Name
Use this helm option to provide the name of the secret that contains
the password corresponding to the bindDN for connecting to the
AD/LDAP host. This option can be used instead of auth.ldap.bindPW.
If both have been configured, then this option overrides
auth.ldap.bindPW.
--set auth.ldap.bindPWSecretName="bind-pw-secret"
This secret can be created using the following command:
kubectl create secret generic bind-pw-secret --from-literal=bindPW="password"
- User Search Base Distinguished Name
Use this helm option to provide the base Distinguished Name to start
the Active Directory/LDAP user search from.
--set auth.ldap.userSearch.baseDN="ou=users,dc=example,dc=org"
- User Search Filter
Use this helm option to provide the optional filter to apply when
searching the directory for users.
--set auth.ldap.userSearch.filter="(objectClass=inetOrgPerson)"
- User Search Username
Use this helm option to provide the attribute used for comparing user
entries when searching the directory.
--set auth.ldap.userSearch.username="uid"
- User Search ID Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the user ID field in a token.
--set auth.ldap.userSearch.idAttr="uid"
- User Search email Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the email field in a token.
--set auth.ldap.userSearch.emailAttr="uid"
- User Search Name Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the name field in a token.
--set auth.ldap.userSearch.nameAttr="uid"
- User Search Preferred Username Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the preferred_username
field in a token.
--set auth.ldap.userSearch.preferredUsernameAttr="uid"
- Group Search Base Distinguished Name
Use this helm option to provide the base Distinguished Name to
start the AD/LDAP group search from.
--set auth.ldap.groupSearch.baseDN="ou=users,dc=example,dc=org"
- Group Search Filter
Use this helm option to provide the optional filter to apply when
searching the directory for groups.
--set auth.ldap.groupSearch.filter="(objectClass=groupOfNames)"
- Group Search Name Attribute
Use this helm option to provide the Active Directory/LDAP attribute
that represents a group's name in the directory.
--set auth.ldap.groupSearch.nameAttr="cn"
- Group Search User Matchers
The userMatchers helm option represents a list. Each entry
in this list consists of a pair of fields named userAttr and
groupAttr. This helm option is used to find users in the directory
based on the condition that, the user entry's attribute represented
by userAttr must match a group entry's attribute represented by
groupAttr.
As an example, suppose a group's definition in the directory looks like
the one below:
## k10admins, users, example.org
dn: cn=k10admins,ou=users,dc=example,dc=org
cn: k10admins
objectClass: groupOfNames
member: cn=user1@kasten.io,ou=users,dc=example,dc=org
member: cn=user2@kasten.io,ou=users,dc=example,dc=org
member: cn=user3@kasten.io,ou=users,dc=example,dc=org
Suppose user1's entry in the directory looks like the one below:
## user1@kasten.io, users, example.org
dn: cn=user1@kasten.io,ou=users,dc=example,dc=org
cn: User1
cn: user1@kasten.io
sn: Bar1
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
userPassword:: < Removed >
uid: user1@kasten.io
uidNumber: 1000
gidNumber: 1000
homeDirectory: /home/user1@kasten.io
For the example directory entries above, a suitable configuration
for the userMatchers would be like the one below. If the dn field
of a user matches the member field in a group, then the user's record
will be returned by the Active Directory/LDAP server.
--set auth.ldap.groupSearch.userMatchers[0].userAttr="dn"
--set auth.ldap.groupSearch.userMatchers[0].groupAttr="member"
Enable Active Directory Authentication
To enable Active Directory based authentication use the following
flag as part of the initial Helm install or subsequent Helm
upgrade command.
Restart the Authentication Pod
If the Helm option auth.ldap.bindPWSecretName has been used
to specify the name of the secret that contains the Active Directory
bind password, and if this password is modified after Veeam Kasten
has been installed, use this Helm option to restart the Authentication
Service's Pod as part of the Helm upgrade command.
Provide the URL used for accessing Veeam Kasten's dashboard using the
following Helm option.
Active Directory/LDAP host
Provide the host and optional port of the AD/LDAP server in the form
host:port using the following Helm option.
Disable SSL
Set this field to true if the Active Directory/LDAP host is not using TLS,
using the following Helm option.
Disable SSL verification
Use the following helm option to set this field to true to disable SSL
verification of connections to the Active Directory/LDAP server.
Start TLS
When set to true, ldap:// is used to connect to the server followed by
creation of a TLS session. When set to false, ldaps:// is used.
Bind Distinguished Name
Use this helm option to provide the Distinguished Name(username)
used for connecting to the Active Directory/LDAP host.
Bind Password
Use this helm option to provide the password corresponding to the
bindDN for connecting to the Active Directory/LDAP host.
Bind Password Secret Name
Use this helm option to provide the name of the secret that contains
the password corresponding to the bindDN for connecting to the
AD/LDAP host. This option can be used instead of auth.ldap.bindPW.
If both have been configured, then this option overrides
auth.ldap.bindPW.
This secret can be created using the following command:
User Search Base Distinguished Name
Use this helm option to provide the base Distinguished Name to start
the Active Directory/LDAP user search from.
User Search Filter
Use this helm option to provide the optional filter to apply when
searching the directory for users.
User Search Username
Use this helm option to provide the attribute used for comparing user
entries when searching the directory.
User Search ID Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the user ID field in a token.
User Search email Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the email field in a token.
User Search Name Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the name field in a token.
User Search Preferred Username Attribute
Use this helm option to provide the Active Directory/LDAP attribute
in a user's entry that should map to the preferred_username
field in a token.
Group Search Base Distinguished Name
Use this helm option to provide the base Distinguished Name to
start the AD/LDAP group search from.
Group Search Filter
Use this helm option to provide the optional filter to apply when
searching the directory for groups.
Group Search Name Attribute
Use this helm option to provide the Active Directory/LDAP attribute
that represents a group's name in the directory.
Group Search User Matchers
The userMatchers helm option represents a list. Each entry
in this list consists of a pair of fields named userAttr and
groupAttr. This helm option is used to find users in the directory
based on the condition that, the user entry's attribute represented
by userAttr must match a group entry's attribute represented by
groupAttr.
As an example, suppose a group's definition in the directory looks like
the one below:
Suppose user1's entry in the directory looks like the one below:
For the example directory entries above, a suitable configuration
for the userMatchers would be like the one below. If the dn field
of a user matches the member field in a group, then the user's record
will be returned by the Active Directory/LDAP server.
### Sample Auth Flow with Screenshots
This section shows screenshots depicting the Auth flow
when Veeam Kasten is installed with Active Directory authentication.
- AWS Simple AD service was setup as the Active Directory service
used by Veeam Kasten in a Kubernetes cluster deployed in Digital Ocean.
- A user named productionadmin was created in the Simple AD
service and added to a group named k10admins.
- A cluster role binding was created to bind the k10admins group to the
k10-admin cluster role.
- A role binding was created to bind the k10admins group to the
k10-ns-admin role in the Veeam Kasten namespace.
- When the user navigates to the Veeam Kasten dashboard, the user is redirected
to the Active Directory/LDAP login screen.
- When authentication with the Active Directory/LDAP server succeeds,
the user is redirected to the Veeam Kasten dashboard.
### Troubleshooting
### Common Name Certificates
Certificates that have a Common Name (CN), but no Subject Alternate Name (SAN)
may cause  an error to be displayed: "x509: certificate relies on legacy Common
Name field, use SANs instead".
This is because the Common Name field of a certificate is no longer used by
some clients to verify DNS names. For more information, see
RFC 6125, Section 6.4.4.
To correct this error, the certificate must be updated to include the DNS name
in the SAN field of the certificate.
If necessary, it is possible to run an older version of Dex until the
certificate can be updated with a proper SAN.
Running with an older version of Dex is not a recommended configuration!
Older images are missing critical security patches and should only be used
as a temporary workaround until a new certificate can be provisioned.
To run with an older version of Dex, use the following values:
### Other Authentication Options
### Group Allow List
When using authentication modes such as Active Directory, OpenShift, or
OIDC, after a user has successfully authenticated with the authentication
provider, Veeam Kasten creates a JSON Web Token (JWT) that contains
information returned by the provider. This includes the groups that a user
is a member of.
If the number of groups returned by an authentication provider results in a
token whose size is more than 4KB, the token gets dropped and is not
returned to the dashboard. This results in a failed login attempt.
The helm option below can be used to reduce the number of groups in JWT.
It represents a list of groups that are allowed admin access to Veeam
Kasten's dashboard. These groups will be appended to the list of subjects
in the default ClusterRoleBinding that is created when Veeam Kasten is
installed to bind them to the ClusterRole named k10-admin. If the
namespace where Veeam Kasten was installed is kasten-io and the Veeam
Kasten ServiceAccount in that namespace is named k10-k10, then the
ClusterRoleBinding would be named kasten-io-k10-k10-admin.
### Veeam Kasten Admin Groups
Suppose the auth.groupAllowList helm option is defined with a list of
groups as "admin-group1, basic-group1, basic-group2" to restrict the number
of groups included in the JSON Web Token, and if the group named
admin-group1 is the only group that needs to be setup with admin level
access to Veeam Kasten, then use the helm option below.
Instead of the groups in auth.groupAllowList, only the groups in
auth.k10AdminGroups will be appended to the list of subjects in the
default ClusterRoleBinding that is created when Veeam Kasten is installed
to bind them to the ClusterRole named k10-admin. If the namespace
where Veeam Kasten was installed is kasten-io and the Veeam Kasten
ServiceAccount in that namespace is named k10-k10, then the
ClusterRoleBinding would be named kasten-io-k10-k10-admin.
### Veeam Kasten Admin Users
This helm option can be used to define a list of users who are granted
admin level access to Veeam Kasten's dashboard. The users in
auth.k10AdminUsers will be appended to the list of subjects in the
default ClusterRoleBinding that is created when Veeam Kasten is installed
to bind them to the ClusterRole named k10-admin. If the namespace
where Veeam Kasten was installed is kasten-io and the Veeam Kasten
ServiceAccount in that namespace is named k10-k10, then the
ClusterRoleBinding would be named kasten-io-k10-k10-admin.
© Copyright 2017-2024, Kasten, Inc.
### latest_access_gcp_details_gcp_console_dashboard.md
## Veeam Kasten Dashboard Directly From the Google Cloud Console
- Dashboard Access
Access via kubectl
Veeam Kasten Dashboard Directly From the Google Cloud Console
Accessing via a LoadBalancer
Existing Ingress Controller
Access via OpenShift Routes
- Access via kubectl
Veeam Kasten Dashboard Directly From the Google Cloud Console
- Veeam Kasten Dashboard Directly From the Google Cloud Console
- Accessing via a LoadBalancer
- Existing Ingress Controller
- Access via OpenShift Routes
- API and Command Line
- Authentication
- Authorization
- Veeam Kasten RBAC
- Veeam Kasten RBAC Dashboard
-
- Accessing Veeam Kasten
- Dashboard Access
If you are running on GKE and do not have kubectl installed
locally, it is possible to use the cloud console to also access the
Veeam Kasten dashboard. You can accomplish this with the following steps:
- Select the Kubernetes cluster that has Veeam Kasten installed and choose
Connect from the menu options on the top of your browser window.
- A cloud shell window will be created and will be auto-populated with a
kubectl command.
- Execute the command in the window to have the console version of kubectl
properly configured.
- Run kubectl --namespace kasten-io port-forward service/gateway 8080:80
to enable forwarding when Veeam Kasten is installed in the kasten-io
namespace.
- Select the Web preview icon from the cloud shell menu.
- In the window that opens, replace the default URL (will look like
https://8080-example.appspot.com/?authuser=0) with
https://8080-example.appspot.com/k10/ where k10 is the release
name under which you installed Veeam Kasten.
© Copyright 2017-2024, Kasten, Inc.
### latest_access_authentication_aws_eks_token_auth.md
## Enabling AWS IAM Token-Based Auth for EKS
- Dashboard Access
- API and Command Line
- Authentication
Direct Access
Basic Authentication
Token Authentication
Obtaining Tokens
Token-Based Authentication with AWS EKS
Obtaining Tokens with Red Hat OpenShift
OAuth Proxy with Red Hat OpenShift (Preview)
OpenID Connect Authentication
OpenShift Authentication
Active Directory Authentication
Other Authentication Options
- Direct Access
- Basic Authentication
- Token Authentication
Obtaining Tokens
Token-Based Authentication with AWS EKS
Obtaining Tokens with Red Hat OpenShift
OAuth Proxy with Red Hat OpenShift (Preview)
- Obtaining Tokens
- Token-Based Authentication with AWS EKS
- Obtaining Tokens with Red Hat OpenShift
- OAuth Proxy with Red Hat OpenShift (Preview)
- OpenID Connect Authentication
- OpenShift Authentication
- Active Directory Authentication
- Other Authentication Options
- Authorization
- Veeam Kasten RBAC
- Veeam Kasten RBAC Dashboard
-
- Accessing Veeam Kasten
- Authentication
- Enabling AWS IAM Token-Based Auth for EKS
The following guide documents integrating AWS Elastic Kubernetes
Service (EKS) clusters with IAM roles for authentication. The
documentation assumes that an EKS cluster exists with IAM roles
enabled
and that the aws CLI, eksctl, and aws-iam-authenticator
tools are available.
### Creating IAM Policies and Roles
Follow the below instructions to create the right IAM policy and role
for the Veeam Kasten setup.
- Follow the instructions here to:
Create an IAM Policy and obtain the IAM Policy ARN from the AWS
IAM Console.
Create an IAM Role for Veeam Kasten use.
- Create an IAM Policy and obtain the IAM Policy ARN from the AWS
IAM Console.
- Create an IAM Role for Veeam Kasten use.
- Obtain the ARN for the newly-created IAM Role from the AWS IAM
Console or by running the
following command.
$ aws iam get-role --role-name <role-name> | grep Arn
Export the value as AWS_IAM_ROLE_ARN:
$ export AWS_IAM_ROLE_ARN=arn:aws:iam::<AWS ACCOUNT>:role/<ROLE NAME>
Follow the instructions here to:
Obtain the ARN for the newly-created IAM Role from the AWS IAM
Console or by running the
following command.
Export the value as AWS_IAM_ROLE_ARN:
### Installing and Configuring Veeam Kasten
Note
With the below configuration, the Veeam Kasten dashboard or API/CLI
access will fail until the RBAC setup documented below is
completed.
Veeam Kasten should now be installed using the instructions here for
using IAM roles but the following option
must be added to the install command to enable token-based
authentication. If this was missed during the initial install, it can also
be added as an upgrade option provided to Helm.
### Configuring RBAC
As defined in our RBAC documentation, Veeam
Kasten comes with pre-defined ClusterRoles that will be used in the below
examples, but additional roles can be defined by the administrator.
See Managing Users or IAM Roles for your Cluster
for the authoritative set of instructions on providing access to an
IAM user or role to an EKS cluster.
This section assumes that the administrator has:
1. Created an IAM Role for users to assume (no policies should be attached
to this role)
2. Added user ARNs for all users that will assume this role under AWS
(a trust relationship)
The IAM Role ARN from step 1 above needs to be extracted via the AWS
console or by using the following command:
Assuming the aws-auth ConfigMap already exists on your cluster,
you need to edit it to include the appropriate IAM users that need
access to Veeam Kasten.
The below example will use the default
k10-basic ClusterRole defined by Veeam Kasten
but this process can be easily extended to arbitrary ClusterRoles. The
ClusterRole can, in turn, be bound to groups and, while not
recommended, individual users. A new group (k10:basic) will be
used, and, to give this group the ability to access Veeam Kasten, the
aws-auth ConfigMap needs to be edited to include the following
configuration under the mapRoles section:
Once done, the aws-auth ConfigMap should look similar to this:
A ClusterRoleBinding for the k10:basic group needs to be created
next by using the following command:
This will generate a ClusterRoleBinding that looks similar to the following:
For ease-of-use, a
ClusterRoleBinding for a default
k10:admins Group is auto-created during Veeam Kasten install.
### Logging into the Veeam Kasten Dashboard using AWS IAM Tokens
To get a user token to authenticate against the Veeam Kasten dashboard
or API for the above user, run:
You can then access the dashboard by logging in with
the above token. The user and permissions can be verified in the
top-right section of the screen.
### Debugging Login Issues
If there are login issues with the token obtained above, validating
that the role assumption is correctly configured can be accomplished
by creating the following profile in ${HOME}/.aws/config:
and then executing:
© Copyright 2017-2024, Kasten, Inc.
