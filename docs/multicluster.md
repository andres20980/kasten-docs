## Multicluster Documentation
### latest_multicluster_index.md
## Veeam Kasten Multi-Cluster Managerï
- Concepts
- Getting Started
- How-Tos
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
The Veeam Kasten Multi-Cluster manager simplifies Veeam Kasten operations
across multiple Kubernetes clusters.
Administrators define primary-secondary relationships between their Veeam
Kasten instances. Primary Veeam Kasten instances provide a single entry point
and dashboard for administrators to manage secondary instances.
Veeam Kasten resources, like Policies and Profiles, are defined in the
primary instance and distributed to secondary instances. Secondary instances
enact their policies and the secondaries' actions and metrics are summarized
in the primary instance.
- Concepts
Overview
License Management
- Overview
- License Management
- Getting Started
Setting up Through the UI
Setting Up Via CLI
- Setting up Through the UI
- Setting Up Via CLI
- How-Tos
Dashboard Access
Using The Dashboard
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
Multi-Cluster API Reference
RBAC Reference
- Multi-Cluster API Reference
- RBAC Reference
- Upgrading
v6.5.14
v6.5.0
v5.5.8
v3.0.8
- v6.5.14
- v6.5.0
- v5.5.8
- v3.0.8
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_known_limitations.md
## Known Limitationsï
- Concepts
- Getting Started
- How-Tos
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- The status of resources distributed to target clusters is not represented at
a global level.
- Modified global resources may not be re-distributed until the corresponding
distribution resource is modified.
- Resources distributed to target clusters will be overwritten when the global
resource is re-distributed.
- Modifications to resources distributed to target clusters will not be
overwritten until the global resource is modified.
- Disconnecting a cluster does not remove previously distributed global
resources.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_concepts_license.md
## License Managementï
- Concepts
Overview
License Management
License Sharing Model
Enabling Multi-Cluster License Management
Multi-Cluster Lease
License Usage
Multi-cluster Lease States
- Overview
- License Management
License Sharing Model
Enabling Multi-Cluster License Management
Multi-Cluster Lease
License Usage
Multi-cluster Lease States
- License Sharing Model
- Enabling Multi-Cluster License Management
- Multi-Cluster Lease
- License Usage
- Multi-cluster Lease States
- Getting Started
- How-Tos
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- Concepts
- License Management
Multi-Cluster Manager enables licensing all clusters in
the same multi-cluster system with a single license.
This can be achieved by installing a single license on the primary cluster,
which will then distribute license leases to secondary clusters.
Any excess license capacity from licenses installed on secondary clusters,
will be contributed to a global pool of licenses maintained by the primary
cluster.
Note
### License Sharing Modelï
When Multi-Cluster license management is enabled, a cluster can contribute its
excess license capacity to the Multi-Cluster license pool.
The excess license capacity is calculated by subtracting the number of
worker nodes in the cluster from the sum of the node limits of all valid
licenses installed in the cluster.
Clusters that do not have sufficient licenses will use the Multi-Cluster
license pool to meet the licensing requirements.
E.g. There are two clusters, A and B, in a Multi-Cluster system, with 4 and
5 worker nodes, respectively.
A license for 10 nodes is installed in cluster A, and cluster B has no
licenses.
The 10 node license covers the 4 nodes in cluster A, and there is an excess
license capacity of 6 (= 10 - 4) on this cluster.
This excess license capacity can be leased by cluster B to meet its license
requirement for 5 nodes.
Both clusters are licensed with a single license in cluster A.
### Enabling Multi-Cluster License Managementï
To enable Multi-Cluster license management, the primary cluster needs to be
setup with an ingress, which the secondary clusters are able to connect to.
If an ingress was not specified when setting up the primary, the ingress may
be set by editing the Cluster resource directly. See
Upgrading for details.
### Multi-Cluster Leaseï
When Multi-Cluster license management is enabled, a Multi-Cluster Lease will
be shown on each cluster's Settings -> Licenses page.
This lease is valid for an hour, and clusters will connect to the primary
cluster to renew the lease prior to expiry.
- Example lease of a cluster leasing from the Multi-Cluster license pool:
This cluster has 2 worker nodes, but does not have any valid licenses
installed locally.
The cluster is leasing 2 nodes from the Multi-Cluster license pool, to
license its 2 worker nodes.ï
- Example lease of a cluster contributing to the Multi-Cluster license pool:
This cluster has 2 worker nodes and licenses installed locally for 100
nodes.
The cluster is contributing excess license capacity of 98 (= 100 - 2)
nodes to the Multi-Cluster license pool.ï
### License Usageï
Multi-Cluster Manager's Licensing page
provides the cumulative license capacity of the Multi-Cluster system, and the
cumulative number of worker nodes licensed in the Multi-Cluster system.
License capacity of this Multi-Cluster system is 100 nodes, and the
sum of worker nodes in this Multi-Cluster system is 4.ï
### Multi-cluster Lease Statesï
### Updatingï
This indicates that the Multi-Cluster lease state is updating. This state
should transition to a different state within minutes.
### Validï
Multi-Cluster lease is valid, and cluster meets the license requirements.
### Expiredï
Multi-Cluster lease has expired. This indicates that the cluster was not able
to connect to the Multi-Cluster license manager in the primary cluster to
renew its lease.
Please verify the cluster is able to connect to the primary.
### Limit Exceededï
The Multi-Cluster lease is insufficient to license the nodes in the cluster.
Please contact Kasten through your account contact or at contact@kasten.io.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_access.md
## Dashboard Accessï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Multi-Cluster Admins
Multi-Cluster Users
Using The Dashboard
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
Multi-Cluster Admins
Multi-Cluster Users
- Multi-Cluster Admins
- Multi-Cluster Users
- Using The Dashboard
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
- Dashboard Access
Once a primary cluster is configured for the Multi-Cluster
Manager features can be accessed via the Dashboard.
### Multi-Cluster Adminsï
The Multi-Cluster Manager dashboard will be available at
https://<URL to k10 gateway service>/k10/##/clusters for Veeam Kasten
exposed externally or http://127.0.0.1:<forwarding port>/k10/##/clusters
for Veeam Kasten exposed through kubectl port-forward during install.
Refer Dashboard Access for more information.
If a cluster is setup as primary, the dashboard will have
a drop-down at top of the navigation sidebar that allows navigation to the
Multi-Cluster Manager dashboard.
For users to get admin access to the Multi-Cluster Manager
dashboard as well as other Multi-Cluster features, additional
role bindings may be required.
The k10-mc-admin ClusterRole is installed during install/
upgrade. It grants admin users access to Distributions, Clusters, Config,
Secrets and Multi-Cluster RBAC configurations in
the Multi-Cluster namespace.
During joining, Veeam Kasten creates a RoleBinding for a default Group
k10:admins in the Multi-Cluster namespace. Admin users can be
added to this Group and will be able to use the above k10-mc-admin
ClusterRole.
Note
k10-mc-admin will be installed under the name <release_name>-mc-admin.
This ClusterRole is not configurable and is installed with Veeam Kasten.
You can also create role bindings for existing users or service accounts.
To bind the k10-mc-admin ClusterRole to a User, use the following command
To bind the k10-mc-admin ClusterRole to a ServiceAccount, use the following
command
Multi-Cluster RBAC section.
Admin users might also need to configure additional K10ClusterRoleBindings.
The K10ClusterRoleBindings allow users to be granted access to the
secondary clusters.
K10ClusterRoleBindings are used for defining who (users/groups) have what
access in which clusters. They are resources that can be created
in the primary cluster to give users/groups access to all or some secondary
clusters.
During joining, Veeam Kasten creates a K10ClusterRoleBinding in the
Multi-Cluster namespace. The default group for this binding is
k10:admins. Other admin users or groups can be
added to this K10ClusterRoleBinding via API or via the dashboard, or a
new K10ClusterRoleBinding can be created.
The complete K10ClusterRoleBinding reference can be found in the
Multi-Cluster Access section.
### Multi-Cluster Usersï
For users who need access only to certain cluster-level operations but
not all the Multi-Cluster Manager configurations, admins can
configure users to have limited access control using Veeam Kasten
Multi-Cluster RBAC. Refer Multi-Cluster User Access
for more information.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_http_primary_ingress_connection.md
## HTTP Primary Ingress Connectionï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
When joining a secondary cluster to a Multi-Cluster system, the ingress
used to connect to the primary cluster requires a secure scheme (https)
by default.
Warning
Using an insecure primary ingress is not recommended for security
reasons.
If an insecure scheme (http) is required for the primary cluster ingress,
an additional flag in Join ConfigMap is needed. Follow the steps in
Adding a Secondary Cluster within the
Setting Up Via CLI flow and ensure that the
option allow-insecure-primary-ingress in
Join ConfigMap is set to "true" with the
following command.
Note
Usage of an insecure primary ingress scheme is not supported in the
UI, regardless of the allow-insecure-primary-ingress flag.
The flag is required whether the primary is set up with an insecure
ingress, or if the ingress used for the primary cluster was overridden
to an insecure scheme.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_disable.md
## Disabling Multi Clusterï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
To disable the Multi-Cluster Manager system on the primary or
a secondary cluster, please add the following to any of
the helm install or helm upgrade commands:
Note
If Multi-Cluster Manager was already running on a cluster,
it will fail during helm upgrade if Multi-Cluster is disabled.
To disable Multi-Cluster safely, disconnect all clusters
before disabling.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_user_access.md
## Multi-Cluster Accessï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Disconnect
Multi-Cluster Access
Configuring Access for Multi-Cluster Users
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
- Disconnect
- Multi-Cluster Access
Configuring Access for Multi-Cluster Users
- Configuring Access for Multi-Cluster Users
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
- Multi-Cluster Access
For users to get access to Multi-Cluster Manager,
Multi-Cluster access control can be configured.
Users first need access to clusters joined and available in
the Multi-Cluster Manager setup. Refer
Multi-Cluster User section for
more information.
### Configuring Access for Multi-Cluster Usersï
Veeam Kasten allows users and/or groups to be bound to a list of
clusters with pre-defined K10ClusterRoles. This ensures, users
and/or groups can be given granular access for individual clusters.
Veeam Kasten will handle any Kubernetes roles or bindings required
to facilitate the access control.
Note
Because Veeam Kasten handles access control, authentication
domains for users/groups can be different on primary and secondary
clusters.
Admin users can add or update K10ClusterRoleBindings in the
Multi-Cluster Manager dashboard.
### K10ClusterRoleBindingsï
K10ClusterRoleBindings defines users/groups access to clusters.
One of the predefined K10ClusterRoles, k10-multi-cluster-admin,
k10-multi-cluster-basic or k10-multi-cluster-config-view,  can
be selected.
Either all clusters or a list of clusters can be selected using name or a
selector string.
List of users or groups can be added using fully qualified names.
The complete RBAC reference for K10ClusterRoleBindings can be found in
this section.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_upgrading.md
## Upgradingï
- Concepts
- Getting Started
- How-Tos
- References
- Known Limitations
- Upgrading
v6.5.14
v6.5.0
v5.5.8
v3.0.8
- v6.5.14
- v6.5.0
- v5.5.8
- v3.0.8
-
- Veeam Kasten Multi-Cluster Manager
- Upgrading
### v6.5.14ï
- New joins requests from clusters from versions 6.5.13 or lower will be
rejected by primary clusters running versions 6.5.14 or higher.
- Secondary clusters from versions 6.5.14 or higher are not able to use join
tokens issued by a primary cluster using versions 6.5.13 or lower.
- Existing join tokens the in the primary cluster will be regenerated as a part
of the upgrade.
- Join configuration options in the Join ConfigMap
were updated.
The option to override the primary-endpoint field was removed,
and an option to override primary-ingress was added.
- Clusters that are already a part of Multi-Cluster are not affected by the
upgrade.
### v6.5.0ï
For Multi-Cluster features to function properly,
ingress for the primary cluster needs
to be configured. The ingress must be specified as the full URL used to access
the Veeam Kasten dashboard, e.g. https://primary.example.com/k10/.
This can be done by editing the Cluster resource for the primary cluster,
and setting the spec.k10.ingress.url field using kubectl edit:
### v5.5.8ï
To enable License Management feature, the ingress for the primary cluster
needs to be configured.
Refer to the v6.5.0 upgrade note for how to set the ingress for the primary
cluster, which is required for all Multi-Cluster features from v6.5.0 onward.
### v3.0.8ï
For upgrades from versions 3.0.7 or lower to version 3.0.8 and higher, all
clusters must be individually upgraded and all secondary clusters should be
re-joined.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_concepts_overview.md
## Overviewï
- Concepts
Overview
Primary
Secondary
Requirements
License Management
- Overview
Primary
Secondary
Requirements
- Primary
- Secondary
- Requirements
- License Management
- Getting Started
- How-Tos
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- Concepts
- Overview
In a Multi-Cluster setup, one cluster is designated as primary, while
all others are designated as secondaries. All primary and secondary
clusters must have Veeam Kasten installed. See
Installing Veeam Kasten for instructions.
### Primaryï
The cluster from which the Multi-Cluster Manager will be
accessed is designated as primary.
The primary cluster defines policies and other configuration centrally.
Centrally defined policies and configuration can then be distributed to
designated clusters to be enacted.
The primary cluster also aggregates metrics so that they may be reported
centrally.
This provides a single pane of glass through which all clusters in the system
are managed.
### Secondaryï
Non-primary clusters are designated as secondaries.
The secondary clusters receive policies and other configuration from the
primary cluster. Once policies are distributed to a secondary, the local
Veeam Kasten installation enacts the policy. This ensures that the policy
will continue to be enforced, even if disconnected from the primary.
### Requirementsï
### Networkï
- Primary cluster's dashboard ingress must be accessible by secondaryclusters.
- If using custom certificates, please make sure that secondary has the correct
certificates to connect to the primary. More information can be found at
Using Trusted Root Certificate.
- Secondary Dashboard Access via Multi-Cluster Dashboard (Optional)
Secondary cluster's dashboard ingress must be accessible by
the primary cluster.
If using custom certificates, please make sure that primary has the correct
certificates to connect to the secondary. More information can be found at
Using Trusted Root Certificate.
- Secondary cluster's dashboard ingress must be accessible by
the primary cluster.
- If using custom certificates, please make sure that primary has the correct
certificates to connect to the secondary. More information can be found at
Using Trusted Root Certificate.
clusters.
Secondary Dashboard Access via Multi-Cluster Dashboard (Optional)
### Clock Synchronizationï
- Primary and secondary clusters must have less than 5 minute clock skew
for multi-cluster metrics functionality.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_disconnect.md
## Disconnectï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Disconnect
Disconnecting a Secondary Cluster
Disconnecting a Primary Cluster
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
- Disconnect
Disconnecting a Secondary Cluster
Disconnecting a Primary Cluster
- Disconnecting a Secondary Cluster
- Disconnecting a Primary Cluster
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
- Disconnect
### Disconnecting a Secondary Clusterï
A secondary cluster can be disconnected via the
Multi-Cluster Manager dashboard.
Alternatively, a secondary cluster can also be disconnected via
kubectl by initiating a deletion of the cluster object on the
primary cluster that corresponds to the secondary cluster to be
disconnected:
### Disconnecting an Unresponsive Secondary Clusterï
Note
Follow the steps below to manually disconnect a secondary cluster:
1. In the secondary cluster, delete the mc-cluster-info secret.
1. In the secondary cluster, delete the service account created for access from
the primary cluster.
1. In the primary cluster, manually remove the finalizer
"dist.kio.kasten.io/cluster-info"
from the cluster object corresponding to the secondary cluster.
1. Verify that the cluster object in step 3 is deleted.
### Disconnecting a Primary Clusterï
After disconnecting all the secondary clusters, you can disconnect a primary
cluster, by simply deleting the primary cluster object.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_reference_rbac.md
## RBAC Referenceï
- Concepts
- Getting Started
- How-Tos
- References
Multi-Cluster API Reference
RBAC Reference
Multi-Cluster Admin
Multi-Cluster User
- Multi-Cluster API Reference
- RBAC Reference
Multi-Cluster Admin
Multi-Cluster User
- Multi-Cluster Admin
- Multi-Cluster User
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- References
- RBAC Reference
For facilitating role-based access for users, Veeam Kasten leverages
Kubernetes ClusterRoles and Bindings. Currently, the Veeam Kasten
Multi-Cluster global manager is only available to admin users and
requires additional RBAC roles and bindings.
### Multi-Cluster Adminï
The k10-mc-admin ClusterRole is added for Distributions, Clusters,
Config, Secrets and Multi-Cluster RBAC configuration access in the Veeam
Kasten Multi-Cluster namespace.
Note
k10-mc-admin will be installed under the name <release_name>-mc-admin.
This ClusterRole is not configurable and is installed with Veeam Kasten.
The following is an example of the k10-mc-admin ClusterRole:
### Multi-Cluster Admin Bindingï
The k10-mc-admin ClusterRole needs a RoleBinding in the Veeam Kasten
Multi-Cluster namespace.
Veeam Kasten creates a RoleBinding for a default Group k10:admins in the
Veeam Kasten Multi-Cluster namespace. Admin users can be added to this Group
and will be able to use the above k10-mc-admin ClusterRole.
To bind the k10-mc-admin ClusterRole to a User, use the following command
The above kubectl command will create the following RoleBinding object
Alternatively, you can also bind the ClusterRole to a ServiceAccount.
### Multi-Cluster Userï
For non-admin users of Veeam Kasten Multi-Cluster Manager, admins
can allow cluster-level access, without giving access to configuration
or admin-only operations.
The following rules can be applied to any existing user's ClusterRole or a new
ClusterRole can be created.
Above ClusterRole will give access to ALL clusters, for a more granular
access, use resourceNames option.
To bind the k10-mc-user ClusterRole to a User, use the following command
To bind the k10-mc-user ClusterRole to a ServiceAccount, use the following
command
### Multi-Cluster User Bindingï
Once users are bound to clusters using the cluster role or rules defined above,
a K10ClusterRoleBinding is required to define the level of access within
the clusters.
### K10ClusterRolesï
These are pre-defined K10ClusterRoles already installed with K10.
k10-multi-cluster-admin K10ClusterRole has access defined in k10-admin
ClusterRole, k10-multi-cluster-basic K10ClusterRole has access defined in
k10-basic ClusterRole, and k10-multi-cluster-config-view K10ClusterRole
has access defined in k10-config-view ClusterRole. More about
k10-admin, k10-basic, and k10-config-view can be found at
K10 RBAC.
### K10ClusterRoleBindingsï
K10ClusterRoleBindings are used for defining who (users/groups) have what
(K10ClusterRole) access in which clusters. They are Custom Resources
that can be created in the primary cluster to give users/groups access to
all or some secondary clusters.
K10 is installed with three pre-defined K10ClusterRoles that correspond to
k10-admin, k10-basic and k10-config-view ClusterRoles.
The following example illustrates how to create a K10ClusterRoleBinding for
user user1, using k10-multi-cluster-admin K10ClusterRole, for cluster
cluster1.
For service account users, a prefix of
system:serviceaccount:<sa_namespace>: is needed for adding such users.
The following example illustrates how to create a K10ClusterRoleBinding for
user sa1, using k10-multi-cluster-admin K10ClusterRole, for cluster
cluster1.
### K10ClusterRoleBindings API Typeï
The following is a complete specification of the K10ClusterRoleBinding API.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_reference_api.md
## Multi-Cluster API Referenceï
- Concepts
- Getting Started
- How-Tos
- References
Multi-Cluster API Reference
Distributions API
RBAC Reference
- Multi-Cluster API Reference
Distributions API
- Distributions API
- RBAC Reference
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- References
- Multi-Cluster API Reference
Veeam Kasten Multi-Cluster exposes an API based on Kubernetes Custom Resource
Definitions (CRDs).
The simplest way to use the API is through kubectl.
To understand the API better refer to the following:
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos.md
## How-Tosï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
This section contains instructions on how to do individual tasks.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_usage.md
## Using The Dashboardï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Overview
Global Resources
Distributions
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
Overview
Global Resources
Distributions
- Overview
- Global Resources
- Distributions
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
- Using The Dashboard
The following sections provide an overview of how to perform common
tasks using the Multi-Cluster Manager. The equivalent
actions can also be performed via a Kubernetes-native API.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_reference.md
## Referencesï
- Concepts
- Getting Started
- How-Tos
- References
Multi-Cluster API Reference
RBAC Reference
- Multi-Cluster API Reference
- RBAC Reference
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- References
This section contains references to tools and APIs related to the
Veeam Kasten Multi-Cluster Manager system.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_concepts.md
## Conceptsï
- Concepts
Overview
License Management
- Overview
- License Management
- Getting Started
- How-Tos
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- Concepts
This section contains concepts related to the Veeam Kasten
Multi-Cluster Manager system. It helps you obtain a deeper
understanding of how the Veeam Kasten Multi-Cluster manager
works.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_getting_started.md
## Getting Startedï
- Concepts
- Getting Started
Setting up Through the UI
Promoting a Primary Cluster
Creating a Join Token
Joining a Multi-Cluster System
Setting Up Via CLI
Setup Primary
Adding a Secondary Cluster
- Setting up Through the UI
Promoting a Primary Cluster
Creating a Join Token
Joining a Multi-Cluster System
- Promoting a Primary Cluster
- Creating a Join Token
- Joining a Multi-Cluster System
- Setting Up Via CLI
Setup Primary
Adding a Secondary Cluster
- Setup Primary
- Adding a Secondary Cluster
- How-Tos
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- Getting Started
With Veeam Kasten already installed in each cluster, a simple joining process
enables the Veeam Kasten Multi-Cluster Manager. Through the joining process,
one cluster will be setup as the primary. Additional clusters are then joined
as secondaries.
Tip
To get started, just setting up a primary can be a great way to go!
Secondaries can be added at any time.
### Setting up Through the UIï
### Promoting a Primary Clusterï
To initiate a Multi-Cluster setup, the first step is to designate one cluster
as the primary, which will serve as the host for the Multi-cluster Manager.
1. Navigate to the Multi-Cluster page.
1. Click the Promote button inside the Promote to Primary card.
3. Enter a memorable name for the primary cluster.
This name must adhere to specific formatting rules:
- Only lower case letters, numbers, hyphens -, or periods .
are allowed.
- The name must start and end with an alphanumeric character
(a letter or a number).
Additionally, the Primary Ingress field will be auto-populated with
the browser's current protocol and domain. However, if necessary,
it can be modified.
1. Click Promote Cluster.
When the promotion is successful, the application will redirect to the new
Multi-Cluster Manager page, where the primary cluster should be visible in the
list of clusters.
### Creating a Join Tokenï
1. Navigate to the Join Tokens page on the Multi-Cluster
Manager on the Primary Cluster.
1. Click the Create New Join Token button.
3. Enter a memorable name for the Join Token.
This name must adhere to specific formatting rules:
1. Click Confirm.
1. Click the Copy button to save the new Join Token to the clipboard.
6. Then, click Done. The newly created Join Token should be listed
in the table.
### Joining a Multi-Cluster Systemï
Using a Join Token, it is possible to connect a secondary cluster
to a Multi-Cluster primary instance.
1. On the secondary cluster, navigate to the Multi-Cluster page.
1. Click the Join button inside the Join a Multi-Cluster card.
1. Paste the Join Token that was into the Token input.
The ingress of the Primary cluster is encoded in the token,
and that ingress is most likely the correct one.
However, the option to override the ingress in the token is available
and may be necessary in certain situations.
4. To override the token, enable the Override Primary Ingress switch
and enter a URL in the Primary Ingress Override input.
5. Enter a memorable name for this cluster to be used by the Multi-Cluster
Manager. This name must adhere to specific formatting rules:
If a name is not entered, a random name will be assigned.
1. Click the Connect button.
1. Verify the information in the dialog box, then click Yes, Join.
The join process will take several seconds.
Afterwards, the Multi-Cluster information page should
be displayed.
If a Join Request is rejected (due to an expired token),
an option to try again will be displayed, and users can return to the
Join a Multi-Cluster form by clicking the Start Over button.
### Setting Up Via CLIï
### Setup Primaryï
Note
If a secondary cluster needs to be set up as a primary,
it cannot be done while it is a already a part of a Multi-Cluster system.
Before proceeding, it is necessary to disconnect
the cluster and then initiate the setup process.
### Setting Up the Primary Cluster Using Helmï
Setting up the primary cluster using Helm requires configuring all of the
following Helm flags during the execution of helm install or
helm upgrade:
- multicluster.primary.create=true
- multicluster.primary.name=<cluster name>
- multicluster.primary.ingressURL=<dashboard URL of primary cluster>
The format for multicluster.primary.ingressURL is
<URL of cluster>/<helm release name>
(e.g., https://cluster-name.dev.kasten.io/k10).
### Setting Up the Primary Cluster Using kubectlï
Create namespace kasten-io-mc.
Create a bootstrap object in the newly created
kasten-io-mc namespace. Assuming that Veeam Kasten has been
installed in the kasten-io namespace using k10
as the release name:
Edit sample-primary-bootstrap.yaml to set
<cluster name> and <cluster dashboard URL>
values for the primary cluster.
Apply the manifest.
When the bootstrap completes successfully, a cluster object is created
in the kasten-io-mc namespace.
### Adding a Secondary Clusterï
### Join Tokensï
Create a join token secret in the primary cluster to generate a join token that
can be used by a secondary cluster to connect to the given primary.
The data will be automatically filled in and you can retrieve the token.
The token is used for authenticating the joining request
from a secondary cluster.
Do not share the join tokens. To revoke a token, simply delete
the join token secret.
### Join Secretï
Create a mc-join secret in the secondary cluster or clusters with the above
token.
### Join ConfigMapï
Create a ConfigMap with the name mc-join-config in the secondary
cluster(s) to configure optional information like cluster name,
cluster ingress and primary ingress.
All fields are optional but the mc-join-config ConfigMap is
required to trigger a join from the secondary.
- If the cluster-name is specified, the primary cluster will attempt to
use it for identifying the created cluster resource.  The cluster-name
must adhere to Kubernetes naming conventions and be unique within the
managed cluster set; otherwise, the join will fail.
- If cluster-name is not specified, the primary cluster will automatically
generate the cluster name.
- If the cluster-ingress is specified, the primary cluster will attempt to
use it for proxying dashboard requests to the secondary cluster. The
cluster-ingress is the Veeam Kasten ingress for the secondary cluster.
- If cluster-ingress is not specified, the primary cluster disables proxy.
Additionally, click-through into the secondary cluster from the primary
cluster dashboard will not be allowed.
- If primary-ingress is specified, the provided ingress will be used
during the join process to connect to the primary. This will override
the primary ingress encoded in the join token.
- If primary-ingress is not specified, the join process will use the
ingress encoded in the join token in the mc-join secret.
This will trigger a join from the secondary cluster to the primary cluster. The
primary cluster will validate the token and admit the cluster.
If Multi-Cluster is disabled, creating the mc-join secret and
mc-join-config ConfigMap will have no effect on the system.
Both mc-join secret and mc-join-config ConfigMap are required to initiate
a join.
### Join Status Secretï
The progress of the join will be recorded in the mc-join-status secret.
Any failures will also be recorded in this secret.
You can see the status by looking at the mc-join-status secret.
The msg field will be populated with any failures (transient or permanent),
recorded during the joining process. The status field records the current
status.
### Cluster Info Secretï
Once the join is successful, the mc-cluster-info secret is created with
information needed by the secondary cluster to communicate with the primary.
You can see the information by looking at the mc-cluster-info secret.
A corresponding bootstrap and cluster object should be created in the primary
cluster's kasten-io-mc namespace.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_reference_api_distribution.md
## Distributions APIï
- Concepts
- Getting Started
- How-Tos
- References
Multi-Cluster API Reference
Distributions API
RBAC Reference
- Multi-Cluster API Reference
Distributions API
- Distributions API
- RBAC Reference
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- References
- Multi-Cluster API Reference
A Distribution is a custom resource (CR) that is used to distribute Global
Resources to clusters in a Multi-Cluster setup.
Additional information can be found on the Distributions page and the
Global Resources page.
### Example Distribution Operationsï
### Create Distributionï
The following example illustrates how to create a distribution that distributes
a global policy and corresponding profile. The distribution and global
resources are all defined in the kasten-io-mc namespace.
Note
Although secrets may be added to a distribution as well, secrets referenced
by a profile will be automatically discovered and distributed with the
profile.
### Distribution API Typeï
The following is a complete specification of the Distribution CR.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_distributions.md
## Distributionsï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Overview
Global Resources
Distributions
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
Overview
Global Resources
Distributions
- Overview
- Global Resources
- Distributions
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
- Using The Dashboard
Distributions provide a way to describe the relationship between globally
defined resources and the clusters to which they should be distributed. This
affords a tremendous amount of flexibility, allowing the correct policies to be
applied to the correct clusters.
For simple setups, a single distribution may be sufficient. Multiple
distributions may be used to accommodate more complex setups and topologies.
### Global Resourcesï
Resources managed centrally in the Multi-Cluster Manager are also
called Global Resources.
Global resources are defined independently from other resources defined in the
primary cluster. This separation means global resources, such as Policies, do
not apply to the primary cluster unless they are also distributed to the
cluster. This ensures the administrator has control over where global resources
are applied.
See Global Resources for additional details.
### Clustersï
Distributions can target any cluster or set of clusters that have been
joined. This includes the primary cluster.
Tip
For more details on the joining process, see the
Getting Started guide.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_overview.md
## Overviewï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Overview
Global Resources
Distributions
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
Overview
Global Resources
Distributions
- Overview
- Global Resources
- Distributions
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
- Using The Dashboard
The Multi-Cluster Manager dashboard has a number of different
sections. A brief description of the sections is provided below.
Refer to Multi-Cluster Access page, to learn
how to access the Multi-Cluster Manager via dashboard and API.
### System Overviewï
The Multi-Cluster Manager gives an overview of the entire
Multi-Cluster system. All cluster information, application, global resource,
data usage and recent activity across clusters can be inspected in a single
pane of glass.
### Veeam Kasten Global Resourcesï
With Multi-Cluster Manager, profiles and policies can be
defined at a global level and then distributed to individual or group
of clusters. This allows for managing of resources in a single place
without having to configure each resource separately on each individual
cluster.
### Data Usageï
With Multi-Cluster Manager, aggregated data usage across clusters
can also be viewed in a single place.
### Recent Activityï
The recent activity section, uses Prometheus metrics across all clusters,
and gives an aggregated view of recent actions. The actions can be viewed
over a week, day or an hour.
### Clustersï
Multi-Cluster Manager allows for an aggregated view of all
clusters configured in the system. Clusters can be filtered by name or
labels. Each cluster displays application, policy and actions information.
A cluster that has been joined into the Multi-Cluster system
using the instructions here
will by default have click through disabled.
If clicking through into the secondary cluster is required, then
the ingress URL of the secondary cluster must be configured.
© Copyright 2017-2024, Kasten, Inc.
### latest_multicluster_how-tos_global_resources.md
## Global Resourcesï
- Concepts
- Getting Started
- How-Tos
Dashboard Access
Using The Dashboard
Overview
Global Resources
Distributions
Disconnect
Multi-Cluster Access
Disabling Multi Cluster
HTTP Primary Ingress Connection
- Dashboard Access
- Using The Dashboard
Overview
Global Resources
Distributions
- Overview
- Global Resources
- Distributions
- Disconnect
- Multi-Cluster Access
- Disabling Multi Cluster
- HTTP Primary Ingress Connection
- References
- Known Limitations
- Upgrading
-
- Veeam Kasten Multi-Cluster Manager
- How-Tos
- Using The Dashboard
### Global Location Profilesï
With Multi-Cluster Manager, location profiles can be created
at a global level in the primary cluster and then distributed to the
clusters in the system.
Creation of location profiles is similar to location profiles in a single
Veeam Kasten deployment. More information can be found in the
Location Profiles section.
Once a global location profile is created, it is ready to be distributed to
the clusters in the system.
Note
Global location profiles are not validated or used until they are
distributed to at least one cluster.
Similar to location profiles, infrastructure profiles can also be created at
a global level and then distributed to the clusters in the system.
### Global Policiesï
With Multi-Cluster Manager, policies can also be created at
a global level in the primary cluster and then distributed to the clusters
in the system.
Creation of policies is similar to policies in a single Veeam Kasten
deployment. More information can be found in the
Protecting Applications section.
Once a global policy is created, it is ready to be distributed to
the clusters in the system.
Global policies are not validated or executed until they are
distributed to at least one cluster.
Refer to the Distributions section for more
information on how to distribute global resources.
### Global License Usageï
If Multi-Cluster license management is enabled, the Licensing tab provides
the global license usage information.
See License Usage section for more information.
© Copyright 2017-2024, Kasten, Inc.
