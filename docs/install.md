## Install Documentation
### latest_install_index.md
## Installing Veeam Kastenï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
Veeam Kasten is available in two main editions, Veeam Kasten Free
and Enterprise. The Kasten product page
contains a comparison of the two Veeam Kasten editions, also
described below, but both editions use the same container images
and follow an identical install process.
- Veeam Kasten Free: The default Veeam Kasten Starter edition,
provided at no charge and intended for evaluation or for use in
smaller or non-production clusters, is functionally the same as
the Enterprise edition but limited from a support and scale
perspective.
- Enterprise: Customers choosing to upgrade to the Enterprise
edition can obtain a license key from Kasten or install from cloud
marketplaces.
The documentation below covers installing both Veeam Kasten editions
on a variety of public cloud and on-premises environments, storage
integration, security key management, license upgrades, and other
advanced installation options.
- Install Requirements
Supported Platforms
Prerequisites
Pre-flight Checks
Veeam Kasten Image Source Repositories
- Supported Platforms
- Prerequisites
- Pre-flight Checks
- Veeam Kasten Image Source Repositories
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
Direct Provider Integration
Container Storage Interface (CSI)
AWS Storage
Azure Managed Disks
Pure Storage
NetApp Trident
Google Persistent Disk
Ceph
Cinder/OpenStack
vSphere
Portworx
Veeam Backup
- Direct Provider Integration
- Container Storage Interface (CSI)
- AWS Storage
- Azure Managed Disks
- Pure Storage
- NetApp Trident
- Google Persistent Disk
- Ceph
- Cinder/OpenStack
- vSphere
- Portworx
- Veeam Backup
- Generic Storage Backup and Restore
Activating Generic Storage Backup
Using Sidecars
End-to-End Example
Generic Storage Backup and Restore on Unmounted PVCs
- Activating Generic Storage Backup
- Using Sidecars
- End-to-End Example
- Generic Storage Backup and Restore on Unmounted PVCs
- Shareable Volume Backup and Restore
Supported storage providers
Prerequisites
- Supported storage providers
- Air-Gapped Install
Air-Gapped Veeam Kasten Installation
Preparing Veeam Kasten Container Images for Air-Gapped Use
- Air-Gapped Veeam Kasten Installation
- Preparing Veeam Kasten Container Images for Air-Gapped Use
- Installing Kasten in FIPS mode
Cryptographic Modules
FIPS Supported Kubernetes Distributions
Limitations in FIPS mode
Installation in FIPS mode
- Cryptographic Modules
- FIPS Supported Kubernetes Distributions
- Limitations in FIPS mode
- Installation in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
Registry1
Installing Veeam Kasten
Using Iron Bank Veeam Kasten Images in an Air-Gapped Environment
Implementing Iron Bank for Veeam Kasten Disaster Recovery
- Registry1
- Using Iron Bank Veeam Kasten Images in an Air-Gapped Environment
- Implementing Iron Bank for Veeam Kasten Disaster Recovery
- Installing Veeam Kasten with Google Workload Identity Federation
Installing Veeam Kasten
Creating a Location Profile with Google Workload Identity Federation
Restoring Veeam Kasten with Google Workload Identity Federation
- Creating a Location Profile with Google Workload Identity Federation
- Restoring Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
FREE Veeam Kasten Edition and Licensing
Manually Creating or Using an Existing Service Account
Pinning Veeam Kasten to Specific Nodes
Using Trusted Root Certificate Authority Certificates for TLS
Running Veeam Kasten Containers as a Specific User
Configuring Prometheus
Complete List of Veeam Kasten Helm Options
Helm Configuration for Parallel Upload to the Storage Repository
Helm Configuration for Parallel Download from the Storage Repository
Setting Custom Labels and Annotations on Veeam Kasten Pods
- FREE Veeam Kasten Edition and Licensing
- Manually Creating or Using an Existing Service Account
- Pinning Veeam Kasten to Specific Nodes
- Using Trusted Root Certificate Authority Certificates for TLS
- Running Veeam Kasten Containers as a Specific User
- Configuring Prometheus
- Complete List of Veeam Kasten Helm Options
- Helm Configuration for Parallel Upload to the Storage Repository
- Helm Configuration for Parallel Download from the Storage Repository
- Setting Custom Labels and Annotations on Veeam Kasten Pods
- Configuring Veeam Kasten Encryption
Bootstrapping Passkeys Before Install
PassKey Management
- Bootstrapping Passkeys Before Install
- PassKey Management
- Upgrading Veeam Kasten
Upgrade Assistant
Upgrading Helm-Installed Veeam Kasten
Upgrading on the Google Cloud Marketplace
Upgrading on the AWS Marketplace
Upgrading an Operator Installed Veeam Kasten
- Upgrade Assistant
- Upgrading Helm-Installed Veeam Kasten
- Upgrading on the Google Cloud Marketplace
- Upgrading on the AWS Marketplace
- Upgrading an Operator Installed Veeam Kasten
- Production Deployment Checklist
Pre-Install
Post-Install
- Pre-Install
- Post-Install
© Copyright 2017-2024, Kasten, Inc.
### latest_install_checklist.md
## Production Deployment Checklistï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
Pre-Install
Encryption Key
Authentication Mode
CSI-based Storage Providers
FIPS Compliant Mode
Post-Install
Disaster Recovery
Encryption Key
Monitoring
User Roles
- Pre-Install
Encryption Key
Authentication Mode
CSI-based Storage Providers
FIPS Compliant Mode
- Encryption Key
- Authentication Mode
- CSI-based Storage Providers
- FIPS Compliant Mode
- Post-Install
Disaster Recovery
Encryption Key
Monitoring
User Roles
- Disaster Recovery
- Monitoring
- User Roles
-
- Installing Veeam Kasten
- Production Deployment Checklist
When you are deploying the Veeam Kasten platform in your production
cluster, there are a few things you should consider.
We have created a quick checklist for you to make sure your
installation is easy.
### Pre-Installï
Following are the items you need to check and configure before you
install Veeam Kasten's platform.  The complete installation instructions
can be found here.
### Encryption Keyï
Before you setup Kasten, you need to set and configure an encryption
key. This key is needed for data and metadata encryption.
More information can be found here.
### Authentication Modeï
During installation, you have an option to choose an authentication mode.
You can choose between Direct Access, Basic Authentication,
Token-based Authentication or OpenID Connect.
You can learn more about it here.
### CSI-based Storage Providersï
If you are provisioning storage via the Container Storage Interface
(CSI) and want to leverage CSI Volume Snapshots, please follow the
documentation here to ensure that the
VolumeSnapshotClass has the Veeam Kasten annotation.
### FIPS Compliant Modeï
When installing, you have the option to enable FIPS mode, which enforces
the use of FIPS approved algorithms. This ensures Kasten is compliant
with FIPS requirements.
However, in order to ensure success, this must be done on a new
installation of Kasten. The underlying cluster should also be in
running in FIPS mode.
You can find more information on this topic here.
### Post-Installï
Following are the items you need to check and configure after you
have installed Veeam Kasten's platform. The complete installation instructions
can be found here.
### Disaster Recoveryï
Kasten allows you to enable Disaster Recovery (DR) to protect Veeam Kasten
from any infrastructure failures. Make sure to enable DR and save your
cluster ID as well as the passphrase for recovery. More information about DR
can be found here.
### Encryption Keyï
Once Veeam Kasten installation is complete, be sure to save the encryption key
for future use. You can lose access to the data in case of loss of
this encryption key.
### Monitoringï
Once you have Veeam Kasten protecting your applications, you want to ensure
that problems such as backup failures, infrastructure issues, and job
failures due to license expiry are immediately noticed without having
to constantly check the dashboard. We therefore highly recommend
integrating your monitoring with our Prometheus
endpoints and triggering alerts based on failure
notifications.
Note
Veeam Kasten does not allow the disabling of Prometheus
services. Attempting to disable these services may result in
unsupported scenarios and potential issues with monitoring and logging
functionalities, affecting Veeam Kasten's overall functionality. It
is recommended to maintain these services enabled in order to ensure
proper functionality and prevent unexpected behavior.
### User Rolesï
User roles are only available for certain authentication modes.
Veeam Kasten is set up with different Cluster Roles
that you can use to enable authorization in your cluster. You should not
change these user roles but you can add on top of them to customize
it to your needs.
For more information about User Roles and Authorization, check
here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_other_other.md
## Installing Veeam Kasten on Other Kubernetes Distributionsï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
Prerequisites
Installing Veeam Kasten
Validating the Install
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Other Kubernetes Distributions
### Prerequisitesï
Before installing Veeam Kasten on any other certified Kubernetes
distributions not explicitly covered, please ensure that
the install prerequisites are met.
### Installing Veeam Kastenï
To use Veeam Kasten with a certified Kubernetes distribution installed
on-premises or in another environment you can follow the general
instructions below. This includes running Veeam Kasten on distributions
such as Rancher, PKS, and OKD (OpenShift Origin). Depending on your
underlying infrastructure, you might also need to provide access
credentials as specified elsewhere for public cloud providers.
Note
When using Cilium as the Container Network Interface (CNI),
make sure to refer to the Kubernetes distribution's specific
documentation for implementation details.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_azure_azure.md
## Installing Veeam Kasten on Azureï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Azure
Note
As of March 5, 2024, "Azure Active Directory" has been renamed as
"Microsoft Entra ID." Throughout this documentation, references to "Azure
Active Directory" will be updated to use both the new and old names. Both
names will be used for a while, after which the documentation will be updated
to use only the new name.
### Prerequisitesï
Before installing Veeam Kasten on Azure Kubernetes Service (AKS), please ensure
that the install prerequisites are met.
### Installing Veeam Kastenï
Veeam Kasten supports multiple options to authenticate with Microsoft Entra
ID (formerly Azure Active Directory), including Azure Service Principal,
Azure Managed Identity with a specific Client ID, and Azure Managed Identity
with the default ID. Please select one of these options if you wish to
provide Azure credentials through helm. If multiple credential sets
are provided, the installation will fail.
### Installing Veeam Kasten with Service Principalï
To install on Azure with Service Principal, you need to specify Client Secret
credentials including your Azure tenant, service principal client ID and
service principal client secret.
### Installing Veeam Kasten on Azure Stack with Service Principalï
To install on Azure Stack, you need to specify your -
- Azure tenant: the Azure Stack tenant ID (you'll find it in global
azure portal > Azure Directory > Properties)
- Service principal client ID: client ID of the app that was used
to create the Kubernetes cluster (you'll find it in global azure
portal > Azure Directory > App registration)
- Service principal client secret: client-secret of the app that was
used to create the Kubernetes cluster (you'll find it in global
azure portal > Azure Directory > App registration > Certificate and
secrets)
- Azure Resource Group: name of the Resource Group that was created for
the Kubernetes cluster
- Azure subscription ID: a valid subscription in your Azure Stack
tenant (if your az client has its default cloud set to your Azure
Stack instance, you can obtain the first subscription ID with
az account list | jq '.[0].id')
- Azure Resource Manager endpoint: the resource management endpoint
for this Azure Stack instance (if your az client has its default
cloud set to your Azure Stack instance, you can obtain it with
az cloud show | jq '.endpoints.resourceManager'. e.g.,
https://management.ppe5.example.com)
- Active Directory endpoint: the active directory login endpoint
(if your az client has its default cloud set to your Azure Stack
instance, you can obtain it with az cloud show |
jq '.endpoints.activeDirectory'. e.g.,
https://login.microsoftonline.com/)
- Active Directory resource ID: the resource ID to obtain AD tokens
(if your az client has its default cloud set to your Azure
Stack instance, you can obtain it with az cloud show | jq
'.endpoints.activeDirectoryResourceId. e.g.,
https://management.example.com/71fb132f-xxxx-4e60-yyyy-example47e19)
You can find more information for creating a Kubernetes cluster on
Azure Stack in this
Microsoft tutorial
### Existing Secret Usageï
It is possible to use an existing secret
to provide the following parameters for Azure configuration:
- Azure tenantField name - azure_tenant_id
- Service principal client IDField name - azure_client_id
- Service principal client secretField name - azure_client_secret
Field name - azure_tenant_id
Field name - azure_client_id
Field name - azure_client_secret
To do so, the following Helm option can be used:
Please ensure that the secret exists in the namespace where
Veeam Kasten is installed.
The default namespace assumed throughout this documentation is kasten-io.
### Installing Veeam Kasten with Managed Identityï
Before installing Veeam Kasten with Azure Managed Identity, you need to
ensure that Managed Identity
is enabled on your cluster. Please note that Veeam Kasten supports only
single-identity nodes at the moment.
When installing Veeam Kasten with Managed Identity, you have an option of
installing with a specific Client ID, or to use the default ID.
To install on Azure using a specific client ID, you need to specify
the client ID.
To install on Azure using the default Managed Identity, you need to set
azure.useDefaultMSI to true.
### Installing Veeam Kasten on Azure US Government Cloud (...and others)ï
To install Veeam Kasten on Microsoft Azure US Government cloud, make sure to
set the following helm options:
This will ensure that Veeam Kasten points to appropriate endpoints. These
options can also be used to specify other clouds like AzureChinaCloud.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_upgrade.md
## Upgrading Veeam Kastenï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
Upgrade Assistant
Upgrading Helm-Installed Veeam Kasten
Upgrading on the Google Cloud Marketplace
Upgrading on the AWS Marketplace
Upgrading an Operator Installed Veeam Kasten
- Upgrade Assistant
- Upgrading Helm-Installed Veeam Kasten
- Upgrading on the Google Cloud Marketplace
- Upgrading on the AWS Marketplace
- Upgrading an Operator Installed Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Upgrading Veeam Kasten
Note
Currently, upgrades are only supported across a maximum of
four versions (e.g., 2.0.10 -> 2.0.14). If your Veeam Kasten version
is further behind the latest, a step upgrade process is recommended
where you can use the --version flag with helm upgrade to control
the version jumps. At least 50% free space is required in catalog storage
also.
### Upgrade Assistantï
You can verify the available free space for the catalog and access your
recommended upgrade path by navigating to the System Information page from
the Settings menu in the navigation sidebar or by using
Veeam Kasten Primer for Upgrades resource.
### Upgrading Helm-Installed Veeam Kastenï
To upgrade to the latest Veeam Kasten release, unless you have installed
Veeam Kasten via the a public cloud marketplace, you should run the
following command assuming you installed in the kasten-io namespace
with the release name k10. If you do not remember your release name,
you can easily discover that via the use of
helm list --namespace=kasten-io.
Known Issues: Helm 3 has known bugs with upgrade (e.g., ##6850). If you run into errors along the lines of
Please use the following as a workaround and then run the above upgrade
commands.
### Upgrading on the Google Cloud Marketplaceï
If you have installed Veeam Kasten via the Google Cloud Marketplace, please
follow the instructions here.
### Upgrading on the AWS Marketplaceï
If you have installed Veeam Kasten via the AWS Container Marketplace or AWS
Marketplace for Containers Anywhere, please follow the marketplace upgrade
instructions.
### Upgrading an Operator Installed Veeam Kastenï
Upgrading a Veeam Kasten installation made by a Veeam Kasten Operator requires
updating the Veeam Kasten Operator.
Ref: Red Hat documentation for upgrading installed Operators.
The process of upgrading the Veeam Kasten Operator depends on how update was
configured during install - Automatic or Manual.
The Operator update approval strategy can be changed anytime after install
from the Subscription tab of the Operator.
For an Automatic update, the Veeam Kasten Operator and Operand
(which is the Veeam Kasten install) are both automatically updated
any time a new Veeam Kasten Operator is published.
For a Manual update, the cluster administrator must approve the update when it shows up
for the installation to begin.
Ref: Red Hat documentation for manually approving a pending Operator upgrade.
The Veeam Kasten operators are published with a maximum supported OpenShift
version. This will cause warnings to appear when trying to upgrade a cluster
beyond the maximum supported version.
Warning
Upgrading the cluster beyond the Veeam Kasten maximum supported OpenShift version
may cause unpredictable Veeam Kasten behavior and will result in losing Kasten support.
Examples of warning messages for cluster upgrade:
© Copyright 2017-2024, Kasten, Inc.
### latest_install_ironbank.md
## Installing Veeam Kasten with Iron Bank Imagesï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
Registry1
Installing Veeam Kasten
Fetching the Helm Chart Values for Iron Bank Images
Providing Registry1 Credentials for Veeam Kasten Helm Deployment
Installing Veeam Kasten with Iron Bank Hardened Images
Using Iron Bank Veeam Kasten Images in an Air-Gapped Environment
Implementing Iron Bank for Veeam Kasten Disaster Recovery
- Registry1
- Installing Veeam Kasten
Fetching the Helm Chart Values for Iron Bank Images
Providing Registry1 Credentials for Veeam Kasten Helm Deployment
Installing Veeam Kasten with Iron Bank Hardened Images
- Fetching the Helm Chart Values for Iron Bank Images
- Providing Registry1 Credentials for Veeam Kasten Helm Deployment
- Installing Veeam Kasten with Iron Bank Hardened Images
- Using Iron Bank Veeam Kasten Images in an Air-Gapped Environment
- Implementing Iron Bank for Veeam Kasten Disaster Recovery
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Veeam Kasten with Iron Bank Images
Iron Bank, which is a crucial part of Platform One, the DevSecOps managed
services platform for the United States (US) Department of Defense (DoD), acts
as the central repository for all hardened images that have gone through
the container hardening process.
It serves as the DoD's Centralized Artifacts Repository (DCAR), housing these
secure images.
All images required to deploy Veeam Kasten have gone through this process and can be
viewed in Iron Bank's
catalog.
Note
To view the catalog, registration with Platform One is necessary.
If you do not have an account, follow the instructions by clicking the
catalog page above to register now.
The catalog page shows the verified findings, compliance details, and overall
risk assessment score associated with each image.
Diving into a specific image shows additional information including the
Software Bill of Materials (SBOMs) in both SPDX and CycloneDX formats.
It also provides Vulnerability Assessment Tracker (VAT) findings, showcasing
justifications for vulnerabilities and their verification status.
Warning
Getting newly released versions of Veeam Kasten images through the
Iron Bank hardening process can take some time. This may result in the
unavailability of new releases for Iron Bank-based deployments for a few
days following the release of standard Veeam Kasten images.
- Installing Veeam Kasten
Fetching the Helm Chart Values for Iron Bank Images
Providing Registry1 Credentials for Veeam Kasten Helm Deployment
Installing Veeam Kasten with Iron Bank Hardened Images
### Registry1ï
Iron Bank uses Harbor for its registry,
which can be accessed using your Platform One credentials.
The username and password required for pulling images from Registry1 via the
command line can be found by clicking on your profile in the upper right
corner.
The password is the same as the CLI secret token.
Veeam Kasten images can be found by using the search bar at the top of the
screen and searching for veeam or kasten. Clicking on an image provides
more information, such as the tags that can be pulled and the sha256 of
the image.
Images are signed by Cosign
and the relevant information is shown for each valid image.
### Installing Veeam Kastenï
Deploying Veeam Kasten with Iron Bank hardened images is possible using the
public Kasten Helm chart. Please ensure that the
prerequisites have been met.
### Fetching the Helm Chart Values for Iron Bank Imagesï
Installing Veeam Kasten with the Iron Bank images, as
shown below, uses a pre-configured values file
specifically for Iron Bank. To view the file, download it by executing the
following command substituting <VERSION> with either latest or a previous
version of Veeam Kasten that's being installed:
This file contains the correct helm values that ensure the deployment of
Veeam Kasten only with Iron Bank hardened images.
This file is protected and should not be modified. It is
necessary to specify all other values using the corresponding Helm flags,
such as --set, --values, etc.
### Providing Registry1 Credentials for Veeam Kasten Helm Deploymentï
Since all images are pulled from Registry1 for a Veeam Kasten deployment using
Iron Bank hardened images, your credentials must be provided in order to
successfully pull the images.
- --set secrets.dockerConfig=<BASE64 ENCODED DOCKERCONFIG>, or
- --set-file secrets.dockerConfigPath=<PATH TO DOCKERCONFIG>
The dockerconfig encoded in base64 can be created with the
jq tool:
### Installing Veeam Kasten with Iron Bank Hardened Imagesï
To install Veeam Kasten with Iron Bank hardened images, execute the following
command substituting <VERSION> with either latest or a previous version of
Veeam Kasten that's being installed:
Since the only differences as compared to a standard Veeam Kasten installation
are the images used, the rest of the process can follow the official Veeam
Kasten documentation.
### Using Iron Bank Veeam Kasten Images in an Air-Gapped Environmentï
Iron Bank hardened Veeam Kasten images can be used in an air-gapped
environment by following the instructions found here.
### Implementing Iron Bank for Veeam Kasten Disaster Recoveryï
The Iron Bank hardened restorectl image can be used for Veeam Kasten
disaster recovery by following the instructions found here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_aws-containers-anywhere_aws-containers-anywhere.md
## Installing Veeam Kasten on AWS Marketplace for Containers Anywhereï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten
Validating the Install
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Note
With the 7.0 release in May 2024, "Kasten by Veeam" and
"Kasten K10" have been replaced with "Veeam Kasten for Kubernetes."
Throughout this documentation, references to "K10" will be modified
to include both the new and simpler "Veeam Kasten" names. Both names
will be used for a while, and then the documentation will be
modified only to use the new names. The name K10 is still used for
functional examples.
### Installing Veeam Kastenï
Follow the installation instructions here.
### Attaching permissions for EKS installationsï
Warning
This is a required step. Veeam Kasten will not be able to
backup any AWS resources unless these permissions are granted.
IAM Role created during installation need to have permissions that allow
Veeam Kasten to perform operations on EBS and, if needed, EFS and S3.
The minimal set of permissions needed by Veeam Kasten for integrating
against different AWS services can be found here:
- Using Veeam Kasten with AWS EBS
- Using Veeam Kasten with AWS S3
- Using Veeam Kasten with Amazon RDS
- Using Veeam Kasten with AWS EFS
- Using Veeam Kasten with AWS Secrets Manager
- Optional KMS Permissions
Create a policy
with the required permissions from the options above. To attach this policy to
the IAM Role created during installation, follow the steps below.
The steps above assume that the Veeam Kasten service account name is
k10-k10 and the Veeam Kasten installation is in the kasten-io
namespace. Please modify these as needed.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_azure-marketplace_azure-marketplace-quick-guide.md
## Installing Veeam Kasten on Azure Marketplaceï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Prerequisites
Installing or Upgrading Veeam Kasten
Accessing the Veeam Kasten Dashboard
Setting Advanced Configurations for Veeam Kasten
Deleting Veeam Kasten
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
Prerequisites
Installing or Upgrading Veeam Kasten
Accessing the Veeam Kasten Dashboard
Setting Advanced Configurations for Veeam Kasten
Deleting Veeam Kasten
- Prerequisites
- Installing or Upgrading Veeam Kasten
- Accessing the Veeam Kasten Dashboard
- Setting Advanced Configurations for Veeam Kasten
- Deleting Veeam Kasten
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Azure Marketplace
The Veeam Kasten data management platform, which is purpose-built for
Kubernetes, provides enterprise operations teams with an easy-to-use,
scalable, and secure solution for backup and restore, disaster recovery,
and mobility of Kubernetes applications. Veeam Kasten's
application-centric approach, along with its deep integrations with both
relational and NoSQL databases, Kubernetes distributions, and all cloud
environments, providing teams the freedom of infrastructure choice without
compromising on operational simplicity.
Veeam Kasten is a policy-driven and extensible platform, which includes
features such as full-spectrum consistency, database integrations,
automatic application discovery, multi-cloud mobility, and a
powerful web-based user interface.
This documentation focuses on deploying and managing Veeam Kasten
using Azure Marketplace. For other deployment scenarios on Azure
Kubernetes Service (AKS), please refer to the more general Azure
installation instructions.
Veeam Kasten on Azure Marketplace Overview
- Installing or Upgrading Veeam Kasten
Searching for Veeam Kasten on Azure Marketplace
Selecting AKS Cluster Details
Provide Veeam Kasten Dashboard Access Details
Provide Ingress Details to Access Veeam Kasten Dashboard
Provide Veeam Kasten Authentication Details
Basic Authentication
Azure Active Directory Authentication
Reviewing and Creating
Verifying Installation Status
- Searching for Veeam Kasten on Azure Marketplace
- Selecting AKS Cluster Details
- Provide Veeam Kasten Dashboard Access Details
Provide Ingress Details to Access Veeam Kasten Dashboard
- Provide Ingress Details to Access Veeam Kasten Dashboard
- Provide Veeam Kasten Authentication Details
Basic Authentication
Azure Active Directory Authentication
- Basic Authentication
- Azure Active Directory Authentication
- Reviewing and Creating
Verifying Installation Status
- Verifying Installation Status
- Accessing the Veeam Kasten Dashboard
Accessing Veeam Kasten Externally Using Ingress
Accessing Veeam Kasten Internally
- Accessing Veeam Kasten Externally Using Ingress
- Accessing Veeam Kasten Internally
- Deleting Veeam Kasten
Deleting from the Azure Marketplace Console
Deleting via the Command Line
- Deleting from the Azure Marketplace Console
- Deleting via the Command Line
Provide Veeam Kasten Dashboard Access Details
Provide Veeam Kasten Authentication Details
Reviewing and Creating
### Prerequisitesï
Before deploying and managing Veeam Kasten using Azure Marketplace,
make sure the following prerequisites are in place to ensure an
efficient installation and operation:
- Make sure kubectl has proper access to the cluster where
Veeam Kasten needs to be installed.
- Create a dedicated namespace for the Veeam Kasten installation.
For example, if Veeam Kasten needs to be installed in a namespace
named kasten-io,  run the following command:
### Installing or Upgrading Veeam Kastenï
### Searching for Veeam Kasten on Azure Marketplaceï
Veeam Kasten is published as an application on Azure Marketplace and can be
searched using the following steps:
1. Go to the Azure Marketplace <https://azuremarketplace.microsoft.com/en-gb/marketplace/apps>_.
2. In the search bar, type Veeam Kasten for Kubernetes on Azure Marketplace
and select the listed application.
3. Locate the Veeam Kasten offer, as shown in the figure below.
4. Click the Get It Now button.
5. Choose one of the plans: Bring Your Own License or
Hybrid Deployments - Term.
as shown in the figure below
6. Click Continue to proceed.
### Selecting AKS Cluster Detailsï
After clicking Continue by selecting one of the plans
in the previous section, begin the process of adding the
Azure Kubernetes Cluster details as shown in the image below
- Subscription : Select the Azure subscription where the AKS cluster
is created.
- Resource group: Select the Resource Group of the AKS cluster.
- AKS Cluster name: Provide the name of the AKS cluster.
- K10 extension Name on the cluster: Specify a unique name that
will be used to represent Veeam Kasten in the cluster. This field is
also used as helm release name on the cluster.
Click Next to provide
the Veeam Kasten dashboard access details.
### Provide Veeam Kasten Dashboard Access Detailsï
Before installing Veeam Kasten, determine how the
dashboard should be exposed.
The dashboard can be accessed externally by enabling ingress resource or
internally using localhost. If Veeam Kasten needs to be exposed using
ingress, provide ingress related information as explained below.
### Provide Ingress Details to Access Veeam Kasten Dashboardï
Select the Expose K10 using Ingress checkbox if Veeam Kasten needs
to be exposed via ingress.
Provide below additional Ingress details as shown in the image below:
- Specify ingress'class: This is an optional field to specify
the Ingress class on the cluster.
- Specify ingress controller service's FQDN: Specify the Ingress
controller Kubernetes Service's FQDN.
For example, if the nginx ingress controller is deployed in the cluster
where Veeam Kasten will be installed, execute the below command to find
the ingress class name:
The Ingress controller service's FQDN can be found
by listing the Kubernetes service of type Loadbalancer
in the namespace where the ingress controller is deployed.
Execute the below commands to get the ingress controller
service's FQDN:
To find the FQDN for the External-IP of the Kubernetes
service listed in the previous command, the
value of the annotation external-dns.alpha.kubernetes.io/hostname
of the Kubernetes service can be used.
Execute the below command to get the annotation:
So, the ingress class name is nginx and ingress controller
service's FQDN is ak-azuremp.dev.azure.kasten.io in the
above example.
Click Next to provide the Veeam Kasten authentication details.
### Provide Veeam Kasten Authentication Detailsï
### Basic Authenticationï
To enable Basic Authentication, first generate
htpasswd
credentials in the format of username:hashedpassword
using either an online tool or the
htpasswd binary found on most systems. Once generated, specify the
credentials as shown in the figure below. After Veeam Kasten is installed,
use the htpasswd credentials to log in to the Veeam Kasten dashboard.
### Azure Active Directory Authenticationï
To configure Active Directory authentication, specify
the following details:
Azure Directory (AD) Server Configuration:
- AD Host: Provide the host and optional port of the AD server
in the form of host:port.
- Bind DN:  Provide the Distinguished Name used for connecting
to the AD host.
- Bind DN Password: Provide the password corresponding to the
bind DN for connecting to the Active Directory host.
- Disable SSL: Select this checkbox if the Active Directory
host is not using TLS.
- Disable SSL Verification: Select this checkbox to disable
SSL verification of connections to the Active Directory server.
- Start TLS for server : Select this checkbox to use ldap://
to connect to the server followed by creation of a TLS session.
If this option is deselected, ldaps:// is used for the connection.
- Specify SSL certificate configmap name: If SSL is enabled
for the AD server, create a Configmap with the SSL
certificate of the AD server in the Veeam Kasten namespace before
installing it. Since Veeam Kasten will be installed in the
kasten-io namespace, create the kasten-io namespace first and
then create a Configmap in it.
Note
The SSL certificate must be in PEM format, e.g.; custom-ca-bundle.pem.
Create a ConfigMap to contain the certificate
$ kubectl --namespace kasten-io create configmap cacertconfigmap --from-file=custom-ca-bundle.pem
Specify the Configmap name on Azure Marketplace as shown in the figure below:
Specify SSL certificate configmap name: If SSL is enabled
for the AD server, create a Configmap with the SSL
certificate of the AD server in the Veeam Kasten namespace before
installing it. Since Veeam Kasten will be installed in the
kasten-io namespace, create the kasten-io namespace first and
then create a Configmap in it.
Note
The SSL certificate must be in PEM format, e.g.; custom-ca-bundle.pem.
Create a ConfigMap to contain the certificate
Specify the Configmap name on Azure Marketplace as shown in the figure below:
User Search Details:
- Base DN: Provide the base Distinguished Name to start the AD user
search.
- User attribute to search users in the AD: Provide the user's AD
attribute used for comparing user entries when searching the directory.
- AD Attribute for User ID: Provide the user's AD attribute that
should map to the user ID field in the Veeam Kasten token.
- AD Attribute for User's Email: Provide the user's AD attribute that
should map to the email field in the Veeam Kasten token.
- AD Attribute for User's Name: Provide the user's AD attribute
that should map to the name field in the Veeam Kasten token.
- AD Attribute for User's PreferredUserName: Provide the user's
AD attribute that should map to the preferred_username field
in the Veeam Kasten token.
- User Search Filter: Provide the optional filter to apply
when searching the AD for users.
Group Search Details:
- Group Base DN: Provide the base Distinguished Name to start the
AD group search from.
- AD Attribute for Group's Name:  Provide the AD attribute that
represents a group's name in the directory.
- Group Search Filter: Provide the optional filter to apply when
searching the directory for groups.
- Group Search - User attribute: This attribute, in combination
with Group Search - Group attribute, is used to search group
memberships for a user. In this field, specify the user's AD attribute
that should match the group's AD attribute specified in
Group Search - Group attribute.
- Group Search - Group attribute: This attribute, in combination
with Group Search - User attribute, is used to search group
memberships for a user. In this field, specify the group's AD attribute
that should match a user's AD attribute specified in
Group Search - User attribute.
Click Next to review and create the Kasten K10
application
### Reviewing and Creatingï
Once all of the configurations is done, review them and
click Create.
### Verifying Installation Statusï
1. Log in to Azure portal and search
for the cluster where Veeam Kasten is installed. Upon locating the
cluster, Veeam Kasten will be listed under Extensions + application
for the cluster.
2. Verify that the provisioning state is Succeeded.
Alternatively, one can connect to the AKS cluster using kubectl and
verify whether Veeam Kasten pods are in the Running state.
### Accessing the Veeam Kasten Dashboardï
### Accessing Veeam Kasten Externally Using Ingressï
If ingress is enabled, as mentioned in the section
configure Veeam Kasten Dashboard access using Ingress
, Veeam Kasten will be available at https://<ingress-controller-fqdn>/k10/##.
For example, https://ak-azuremp.dev.azure.kasten.io/k10/##
### Accessing Veeam Kasten Internallyï
If Ingress is not enabled, enable local access to the dashboard by
executing the following commands after the Veeam Kasten is installed:
Assuming that Veeam Kasten is installed in namespace kasten-io and the
K10 extension Name on the cluster is configured as k10,
the dashboard will be accessible at: http://127.0.0.1:8080/k10/##/
For detailed documentation on how to use Veeam Kasten after installation,
please refer to Using Veeam Kasten.
### Setting Advanced Configurations for Veeam Kastenï
To set advanced configuration options for
Kasten deployed via the Azure Marketplace
(i.e. Complete List of Veeam Kasten Helm Options),
within the Azure Portal, navigate to the AKS cluster on which
Kasten is deployed, and select Extensions + Applications
Select k10, then scroll down and select Configuration Settings.
Here the advanced configuration options can be modified, added, or removed.
### Deleting Veeam Kastenï
### Deleting from the Azure Marketplace Consoleï
1. Login to azure portal and search for
the cluster where Veeam Kasten is installed. Veeam Kasten will be listed
under Extensions + application for the cluster.
2. Click the Uninstall option to remove the Veeam Kasten from the console.
### Deleting via the Command Lineï
To delete a Veeam Kasten instance installed via Azure Marketplace,
delete all resources in the Veeam Kasten namespace using the following
command:
For example, if Veeam Kasten is installed the in namespace kasten-io
and the application is named k10, use the following command to delete
it:
Once all the resources are deleted, use the following command to
delete the namespace:
Regardless of the approach, all resources will be cleaned up unless
the ReclaimPolicy for PersistentVolume is changed to value other
than the default value delete. If that is the case, manual cleaning
of PVs will be necessary.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_gvs_restricted.md
## Restricted Use of Generic Storage Backupï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
Generic Storage Backup (GSB) is a feature developed by
Kasten to provide backup capabilities for Kubernetes applications with
persistent volumes using a storage provisioner that lacks snapshot
capabilities. While this feature provided flexibility in the early stages of
Kubernetes storage, it comes with certain limitations. GSB essentially copies
the live filesystem of a persistent volume, and any changes occurring to that
filesystem during the file copy operation can lead to inconsistent backup data.
This inconsistency could potentially result in unexpected behavior when
restoring applications using a GSB backup.
Unlike GSB, storage snapshots allow for the creation of crash-consistent and
data-consistent backups. The general availability of VolumeSnapshot APIs for
Container Storage Interface (CSI) drivers allowed storage vendors to integrate
their snapshot and cloning capabilities using a standardized interface.
Since 2018, the list of production-ready CSI drivers
has grown to over 100, with the majority now supporting VolumeSnapshots.
Given the increasing availability and adoption of snapshot-capable CSI
drivers, the utility of GSB has become limited.
It is highly recommended for existing customers to migrate to a CSI driver with
snapshot and clone capabilities based on their storage requirements. In rare
cases where migration to a CSI driver is not possible, existing
customers can contact Kasten by Veeam Support via MyVeeam,
to open a support case and request the activation token for GSB.
For all current prospects evaluating Veeam Kasten, we recommend reaching
out to your local Kasten by Veeam Sales team through the local point of contact
within the Veeam channel.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_openshift_openshift.md
## Installing Veeam Kasten on Red Hat OpenShiftï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Helm based Installation
OpenShift on Azure
Operator based Installation
Managed Red Hat OpenShift Offerings
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
Helm based Installation
OpenShift on Azure
Operator based Installation
Managed Red Hat OpenShift Offerings
- Helm based Installation
- OpenShift on Azure
- Operator based Installation
- Managed Red Hat OpenShift Offerings
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Red Hat OpenShift
There are two methods to install Veeam Kasten on Red Hat OpenShift:
While the two installation methods have similarities, the details
will differ. Please make sure to choose the method that most closely
follows the requirements of your organization.
Note
When deploying Veeam Kasten on a Red Hat OpenShift managed
Kubernetes cluster using Cilium as a Container Network Interface
(CNI), it is important to consider the associated limitations,
including potential compatibility issues or differences in
configuration compared to the default CNIs. Refer to this page
for instructions on addressing these issues and optimizing the
deployment with Cilium.
### Managed Red Hat OpenShift Offeringsï
The two installation methods mentioned above are also
applicable when installing Veeam Kasten on Managed Red Hat
OpenShift offerings, including:
- Red Hat OpenShift on AWS (ROSA)
- Azure Red Hat OpenShift (ARO)
No additional or platform-specific configurations are required
for installation.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_suserancher_suserancher.md
## SUSE Rancher Apps & Marketplace Based Installationï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Prerequisites
Veeam Kasten Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
Prerequisites
Veeam Kasten Installation
- Prerequisites
- Veeam Kasten Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Veeam Kasten on Kubernetes
- SUSE Rancher Apps & Marketplace Based Installation
Note
With the 7.0 release in May 2024, "Kasten by Veeam" and
"Kasten K10" have been replaced with "Veeam Kasten for Kubernetes."
Throughout this documentation, references to "K10" will be modified
to include both the new and simpler "Veeam Kasten" names. Both names
will be used for a while, and then the documentation will be
modified only to use the new names. The name K10 is still used for
functional examples.
### Prerequisitesï
Before installing Veeam Kasten on a SUSE Rancher managed
Kubernetes cluster, please ensure that the
install prerequisites are met.
Prior to deploying Veeam Kasten, it is recommended that
you need to create the namespace where Kasten will be
installed. By default, the documentation uses kasten-io.
In the SUSE Rancher user interface, navigate to Clusters
-> Project/Namespaces and click "Create Namespace" and
create a namespace called âkasten-ioâ.
### Veeam Kasten Installationï
1. Find the Veeam Kasten chart of the SUSE Rancher Marketplace.
Navigate to Apps & Marketplace -> Charts and search for âKastenâ.
1. To begin the installation, simply click Install.
3. Select the namespace 'kasten-io' from the Namespace dropdown menu.
Optionally select "Customize Helm options before install" to
customize the deployment.
See this page
for detailed descriptions of available options.
1. To complete installation, click Next.
When deploying Veeam Kasten on a SUSE Rancher managed
Kubernetes cluster using Cilium as a Container Network
Interface (CNI), it is important to consider the associated
limitations, including potential compatibility issues or
differences in configuration compared to the default CNIs.
Refer to this Knowledge Base
page for instructions on addressing these issues and optimizing
the deployment with Cilium.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_configure.md
## Configuring Veeam Kasten Encryptionï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
Bootstrapping Passkeys Before Install
Passphrases
AWS Customer Managed Keys
HashiCorp Vault Transit Secrets Engine
PassKey Management
Creating Passkeys
Listing Passkeys
Getting Passkeys
Deleting Passkeys
Changing Passkeys
- Bootstrapping Passkeys Before Install
Passphrases
AWS Customer Managed Keys
HashiCorp Vault Transit Secrets Engine
- Passphrases
- AWS Customer Managed Keys
- HashiCorp Vault Transit Secrets Engine
- PassKey Management
Creating Passkeys
Listing Passkeys
Getting Passkeys
Deleting Passkeys
Changing Passkeys
- Creating Passkeys
- Listing Passkeys
- Getting Passkeys
- Deleting Passkeys
- Changing Passkeys
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Configuring Veeam Kasten Encryption
Veeam Kasten supports encryption for data and metadata stored in an object
store or an NFS file store (e.g., for cross-cloud snapshot migration) via the
use of the AES-256-GCM encryption algorithm. Veeam Kasten encryption
is always enabled for external data and metadata (more information below),
it cannot be disabled. Multiple methods of encryption can be used, and Veeam
Kasten can be configured to use any of them. Veeam Kasten allows users to
have multiple Passkeys. These Passkeys can be a combination of any of the
different types listed below. However, only one of them will be in use at
any point in time.
A Passkey API resource is used to add, edit, list or remove a Passkey
used for data and metadata encryption.
### Bootstrapping Passkeys Before Installï
If you do not specify a cluster secret, a Passkey with a random
passphrase will be generated by Veeam Kasten during install. The randomly
generated Passkey can be changed via the Changing
Passkeys instructions. However, if the passphrase
needs to be specified before install, it can be done via the creation
of a Kubernetes secret with a well-known name (k10-cluster-passphrase)
in the namespace you will install Veeam Kasten in (default kasten-io):
Warning
Once the cluster secret is set or auto-generated, do
not modify or delete the cluster secret directly, please follow
the Passkey change workflow below.
### Passphrasesï
A passphrase is used to protect the encryption key used by Veeam Kasten to
encrypt application data.
Note
The Passkey passphrase should be stored separately in a
secure location for Veeam Kasten Disaster Recovery.
### AWS Customer Managed Keysï
An AWS Customer Managed Key (CMK) can also be used to protect
the encryption key used by Veeam Kasten to encrypt application data.
IAM must be configured for Veeam Kasten. Refer to
Using AWS IAM Roles for
more information on IAM roles.
AWS keys are required while installing Veeam Kasten in order to use
the AWS Customer Manager Key. The IAM role is an optional value to be
configured if Veeam Kasten should assume a specific role.
Following is the AWS policy needed for access to AWS KMS.
Additionally, the user/role needs to be added to the corresponding CMK policy
as well.
### HashiCorp Vault Transit Secrets Engineï
- Configuring Vault Server for Kubernetes Auth
HashiCorp Vault Transit Secrets Engine can also be used to protect
the encryption key used by Veeam Kasten to encrypt application data.
Refer to the Vault Transit Secret Engine documentation
for more information on configuring the transit secret engine.
In addition to the Transit Secret Engine setup, Veeam Kasten needs to be
authorized to access Vault. Either token or kubernetes authentication
is supported for the Vault server.
### Token Authï
The token should be provided via a secret.
This method will be deprecated in the future in favor of kubernetes auth
This may cause the token to be stored in shell history.
It is recommended to regularly rotate the token used for accessing Vault.
When a new token is generated, the vault-creds secret should be updated
with the new token provided below:
Credentials can be provided with the Helm install or upgrade command
using the following flags.
### Kubernetes Authï
Refer to Configuring Vault Server For Kubernetes Auth prior to installing Veeam Kasten.
After setup is done, credentials can be provided with the Helm install or
upgrade command using the following flags:
vault.role is needed to authenticate via kubernetes service account tokens.
vault.serviceAccountTokenPath can be left blank if the service account path
was not changed from the default of:
/var/run/secrets/kubernetes.io/serviceaccount/token
vault.secretName can be provided to the helm install to do a
best-effort fallback to token auth if kubernetes authentication fails. If not present
and kubernetes authentication fails, then the primary key encryption will not
succeed and will return an error.
### PassKey Managementï
### Creating Passkeysï
A Passkey that represents a passphrase, expects a Kubernetes Secret to be
provided which contains the passphrase. This can be done via the creation of
a Kubernetes secret in the Veeam Kasten namespace:
As shown below, this secret can then be used to create a
Passkey. Note that Passkeys are non-namespaced.
A Passkey can also be used to represent an AWS KMS Customer Managed Key(CMK).
The AWS CMK key ID can be provided directly in the passkey.
A Passkey can also be used to represent a HashiCorp Vault Transit Secrets
Engine. The Vault Transit key name and mount path can be provided directly in
the passkey, as shown below.
In addition, a vault authentication role and path to the service account token
used for Vault's Kubernetes Authentication method can be passed in,
vaultauthrole and vaultk8sserviceaccounttokenpath, respectively. This
will override those values originally set via the helm install Kubernetes Auth.
If using Token Auth, passing in these two values will
have the effect of upgrading the authentication method from Token to Kubernetes.
Please ensure your vault server is properly configured as shown in
Configuring Vault Server for Kubernetes Auth before
adding these to the Passkey.
If usenow is set to true, while adding a Passkey, it will become
the default Passkey.  For changing the default (in use) Passkey, take
a look at  the Changing Passkeys instructions.
Multiple Passkeys can have their usenow flags sets but only one
Passkey will be in use at any point in time. The
Passkey that is most recently added with usenow set to true,
will be the Passkey in use.
You can verify which Passkey is inuse by listing the Passkeys and
checking the status. The status of the Passkey in use will have the inuse
flag set to true.
### Listing Passkeysï
To list all Passkeys, simply run:
### Getting Passkeysï
To get a specific Passkey, run:
You may see additional Passkey detail by using the -o yaml option:
### Deleting Passkeysï
You can delete existing Passkeys if they are no longer required.
If a Passkey is currently in use or only one Passkey exists,
it cannot be deleted.
### Changing Passkeysï
Veeam Kasten allows you to change the current Passkey used for data
and metadata encryption.
To change the Passkey, first add a new Passkey by following the
instructions for adding Passkeys,
but set the usenow flag to true.
You can then delete the old Passkey by following the instructions for
deleting Passkeys.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_fips.md
## Installing Kasten in FIPS modeï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
Cryptographic Modules
FIPS Supported Kubernetes Distributions
Limitations in FIPS mode
Installation in FIPS mode
- Cryptographic Modules
- FIPS Supported Kubernetes Distributions
- Limitations in FIPS mode
- Installation in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Kasten in FIPS mode
Kasten, as of version 7.0, supports an installation option that complies with
the Federal Information Processing Standards (FIPS) defined by the National
Institute of Standards and Technology (NIST). This is especially important for
organizations operating in highly regulated industries or government sectors.
FIPS-compliant software ensures that cryptographic algorithms and security
protocols meet strict government requirements, including those set by the
United States Department of Defense (DoD). To learn more about FIPS, visit
NIST's Compliance FAQs.
Kasten in FIPS mode was designed to comply with the FIPS 140-3 standard.
Activate this mode by using a set of Helm values specified below during the
installation process, as explained in the accompanying document. To learn
more about FIPS 140-3, please refer to
NIST FIPS 140-3.
### Cryptographic Modulesï
Kasten uses OpenSSL for its implementation of cryptographic primitives and
algorithms. OpenSSL is provided by Red Hat's Universal Base Images (UBI). This
cryptographic module is currently listed as "review pending" by
NIST's Cryptographic Module Validation Program.
By incorporating OpenSSL, UBI, and aligning its implementation with Red Hat Compliance recommendations, Kasten ensures compliance of the FIPS 140-3 security requirements.
### FIPS Supported Kubernetes Distributionsï
Kasten has been extensively tested and verified with Red Hat OpenShift,
ensuring seamless integration between the two platforms. By using Kasten
with Red Hat OpenShift, customers can benefit from enhanced security and
compliance features, which are necessary for protecting critical data in
FIPS-compliant environments.
While Kasten's FIPS mode can be activated in other environments, it may
necessitate additional testing and configuration to ensure the cryptographic
module's compliance. However, Kasten is continuously exploring opportunities
to support additional Kubernetes distributions in the future.
### Limitations in FIPS modeï
Some Kasten features are not currently supported when FIPS is enabled:
- Prometheus
- PDF Reports
- Block mode exports and restores of supported Ceph CSI volumes do
not use the Ceph API
As a workaround for dashboards please install and configure a FIPS
compliant version of Grafana and Prometheus with Kasten.
### Installation in FIPS modeï
Warning
During initialization, Kasten generates encryption keys using the configured
encryption algorithms.
This means FIPS algorithms must be enabled during the initial installation.
However, some features will be unavailable (see above).
To ensure that certified cryptographic modules are utilized and non-compliant
features are disabled, you must install Kasten with additional Helm values that
can be found here: FIPS values.
To install the latest version of Kasten with the latest values use the
command below:
© Copyright 2017-2024, Kasten, Inc.
### latest_install_requirements.md
## Install Requirementsï
- Install Requirements
Supported Platforms
Prerequisites
Pre-flight Checks
Veeam Kasten Image Source Repositories
- Supported Platforms
- Prerequisites
- Pre-flight Checks
- Veeam Kasten Image Source Repositories
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Install Requirements
Veeam Kasten can be installed in a variety of different environments and
on a number of Kubernetes distributions today. To ensure a smooth install
experience, it is highly recommended to meet the prerequisites and
run the pre-flight checks.
### Supported Platformsï
The following operating systems and architectures are supported.
Note
All nodes within the cluster must be running the same platform. Clusters with blended platforms are not supported.
Operating System
Architectures
FIPS Support
Veeam Repository Exports
vSphere Block Mode Exports
Linux
x86_86 (amd64)
Yes
Arm (arm64/v8)
No
Power (ppc64le)
N/A
### Prerequisitesï
This section describes the general requirements for installing Veeam Kasten
in any environment.
Follow the steps below to install Veeam Kasten with Helm:
1. Verify the Helm 3 package manager and configure access
to the Veeam Kasten Helm Charts repository.
- The Helm version  should be compatible with the version of the Kubernetes
cluster where Veeam Kasten is expected to be deployed. Helm is assumed to
be compatible with n-3 versions of Kubernetes it was compiled against.
Follow the Helm version skew policy
to determine suitable binary version.
- Add the Veeam Kasten Helm charts repository using:
1. Verify Helm Chart Signature.
- The integrity of the Veeam Kasten Helm chart published on the Helm chart
repository can be verified using the public key published.
Check the security page for more details.
- Download the public key from this link.
- When installing Veeam Kasten using the helm install command, pass the
--verify flag along with the --keyring to verify the Helm chart
during installation.
Helm chart provenance is supported only in Veeam Kasten chart versions 6.5.14 and later.
1. Run Pre-flight Checks.
- Perform the necessary checks to make sure that the environment is ready for
installation. Refer to the Pre-Flight Checks for
additional information.
The pre-flight check does not include verification of the cluster being in FIPS mode. This is a requirement for Veeam Kasten to be installed in FIPS mode.
1. Create the installation namespace for Veeam Kasten(by default, kasten-io):
(by default, kasten-io):
- When Veeam Kasten is installed, helm will automatically generate a new
Service Account to grant Veeam Kasten the required access to Kubernetes
resources.
- If a pre-existing Service Account needs to be used, please follow these instructions.
1. Identify a performance-oriented storage class:
- Veeam Kasten assumes that SSDs or similar fast storage media support the
default storage class. If the default storage class doesn't meet the
performance requirements, add the following option to the Veeam Kasten Helm
installation commands:
### Pre-flight Checksï
By installing the primer tool, you can perform pre-flight checks provided
that your default kubectl context is pointed to the cluster you intend to
install Veeam Kasten on. This tool runs in a cluster pod and performs the
following operations:
- Validates if the Kubernetes settings meet the Veeam Kasten requirements.
- Catalogs the available StorageClasses.
- If a CSI provisioner exists, it will also perform basic validation
of the cluster's CSI capabilities and any relevant objects that may
be required. It is strongly recommended that the same tool be used
to perform a more comprehensive CSI validation using the
documentation here.
Note that running the pre-flight checks using the primer tool will
create and subsequently clean up a ServiceAccount and ClusterRoleBinding
to perform sanity checks on your Kubernetes cluster.
The primer tool assumes that the Helm 3 package manager
is installed and access to the Veeam Kasten Helm Charts repository is
configured.
Run the following command to deploy the the pre-check tool:
To run the pre-flight checks in an air-gapped environment, use the
following command:
Follow this guide to prepare Veeam Kasten container images for air-gapped use.
### Veeam Kasten Image Source Repositoriesï
All Veeam Kasten images for a default install are hosted at
gcr.io/kasten-images.
When deploying Veeam Kasten using Iron Bank hardened
images, the following repositories are used:
- registry1.dso.mil/ironbank/veeam/kasten
- registry1.dso.mil/ironbank/opensource/prometheus-operator
- registry1.dso.mil/ironbank/opensource/dexidp
- registry1.dso.mil/ironbank/opensource/prometheus
- registry1.dso.mil/ironbank/redhat/ubi
© Copyright 2017-2024, Kasten, Inc.
### latest_install_install.md
## Installing Veeam Kasten on Kubernetesï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Veeam Kasten on Kubernetes
While Veeam Kasten can be installed on any Linux system running a certified Kubernetes
distribution, the resources below provide specific installation
options for various public clouds, managed Kubernetes services,
and other certified Kubernetes distributions:
Following a successful installation, there are several options
for setting up access to the Veeam Kasten dashboard. For more
information, refer to Dashboard Access.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_gwif.md
## Installing Veeam Kasten with Google Workload Identity Federationï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
Installing Veeam Kasten
Creating a Location Profile with Google Workload Identity Federation
Restoring Veeam Kasten with Google Workload Identity Federation
- Installing Veeam Kasten
- Creating a Location Profile with Google Workload Identity Federation
- Restoring Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten with Google Workload Identity Federation
Google Workload Identity Federation
uses service account impersonation for authentication and authorization,
thereby avoiding the use of Google Service Account keys with extended
lifespans.
It is compatible with various identity providers such as AWS, Azure, or
Kubernetes. An example of implementing Google Workload Identity Federation on
an OpenShift cluster on GKE with Kubernetes as the identity provider can be
found here.
Veeam Kasten supports the use of Google Workload Identity Federation with Kubernetes
as the Identity Provider both
during the export of applications and in Veeam Kasten DR Backup and Restore
processes.
### Installing Veeam Kastenï
When Kubernetes is used as the Identity Provider, workloads can use the
Kubernetes service account tokens to authenticate to Google Cloud. These tokens
are made available to workloads through the service account token volume
projection , which requires some additional Helm settings to be set.
To install Veeam Kasten with Google Workload Identity Federation, use the
following commands:
With <audience> is the Audience set up for the Workload Identity Pool.
### Creating a Location Profile with Google Workload Identity Federationï
Instructions on how to create a Location Profile with Google Workload Identity
Federation can be found here.
### Restoring Veeam Kasten with Google Workload Identity Federationï
Veeam Kasten supports the use of Google Workload Identity Federation with Kubernetes as the
Identity Provider
during Veeam Kasten DR Backup and Restore process. For more information
on Veeam Kasten DR Backup and Restore, please see here.
Please note that it is possible to restore Veeam Kasten with Google
Workload Identity Federation, regardless of the authentication mechanism
used for the Google Location Profile selected while enabling Veeam Kasten
disaster recovery on the source cluster.
The restore process will require a Location Profile with Google Workload
Identity Federation. Please refer back to this
section for instructions on how to install Veeam Kasten on the target
cluster with Google Workload Identity Federation, and the
Google Cloud Storage Location Profile configuration
section for instructions on how to create a Location Profile.
Following that, Veeam Kasten can be restored using Google Workload Identity
Federation credentials by executing the command below:
<audience> is the Audience set up for the Workload Identity Pool of the
target cluster.
<location-profile-name> is the profile on target cluster that contains the
credential configuration file.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_google_google.md
## Installing Veeam Kasten on Google Cloudï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Google Cloud
Note
With the 7.0 release in May 2024, "Kasten by Veeam" and
"Kasten K10" have been replaced with "Veeam Kasten for Kubernetes."
Throughout this documentation, references to "K10" will be modified
to include both the new and simpler "Veeam Kasten" names. Both names
will be used for a while, and then the documentation will be
modified only to use the new names. The name K10 is still used for
functional examples.
### Prerequisitesï
Before installing Veeam Kasten on Google Cloud's Google Kubernetes Engine
(GKE), please ensure that the install
prerequisites are met.
### Installing Veeam Kastenï
Installing Veeam Kasten on Google requires two kinds of Service Accounts.
The first, documented below, is a Google Cloud Platform (GCP) Service
Account (SA)
that grants access to underlying Google Cloud infrastructure resources such as
storage. The second, as mentioned above in the Prerequisites section,
is a Kubernetes Service Account that grants access to Kubernetes resources
and will be auto-created during the helm install process or via
Google Marketplace options.
It is advised to make sure that the necessary permissions are available
before proceeding with the installation of Veeam Kasten. The process of
granting permissions may vary depending on the chosen installation mode.
It is important to follow the instructions relevant to the desired
installation mode to ensure a smooth and successful installation of
Veeam Kasten.
### GCP Service Account Configurationï
Veeam Kasten uses the Google Cloud Platform Service Account to manage volumesnapshot
in the GCP account. Therefore, the service account needs to be assigned the
compute.storageAdmin
role.
Service Account Key
Veeam Kasten requires a Service Account key for the GCP Service Account
and the GCP Project ID associated with it.
### Using a Separate GCP Service Accountï
The preferred option for a Veeam Kasten install is to create and use a
separate Google service account with the appropriate permissions to
operate on the underlying Google Cloud infrastructure and then use that.
For more details on how to create and use a separate service account,
refer to the following links:
- Creating a New Service Account
- Installing Veeam Kasten with the new Service Account
Using a Custom Project ID
Existing Secret Usage
- Using a Custom Project ID
- Existing Secret Usage
For information on adding the compute.storageAdmin role to a Google
Cloud Platform Service Account for the associated GCP project, refer to
this link.
### Service Accounts for a Marketplace Installï
If you are installing on Google via the Google Marketplace,
first follow the below instructions on correctly configuring the
cluster's default SA and then follow these
instructions to install.
### Using the Default GCP Service Accountï
A GCP Service Account automatically gets created with every GKE
cluster. This SA can be accessed within the GKE cluster to perform
actions on GCP resources and, if set up correctly at cluster creation
time, can be the simplest way to run the Kasten platform.
This SA configuration needs to be done at cluster creation time. When
using the Google Cloud Console to create a new Kubernetes cluster,
please select More Options for every node pool you have
added. Search for Security in the expanded list of options and,
under Access Scopes, select Set access for each API. In the list
of scopes that show up, please ensure that Compute Engine is set to
Read Write.
Once the Service Accounts are created and the node pools are running,
Veeam Kasten can then be installed by running the following install command:
To address any troubleshooting issues while installing Veeam
Kasten on a Kubernetes platform using the Cilium Container Network
Interface (CNI) setup, refer to this page.
The page provides specific steps for resolving installation issues with
Cilium CNI and Veeam Kasten compatibility.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_aws_aws.md
## Installing Veeam Kasten on AWSï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on AWS
### Prerequisitesï
Before installing Veeam Kasten on Amazon EKS, it is important to determine the
preferred authentication mechanism: either Long-term access keys or IAM Roles
for service accounts. The choice of authentication mechanism will affect the
necessary steps and prerequisites for the installation process.
AWS provides two types of authentication mechanisms for programmatic access:
- Long-term access keys
- IAM Roles for Service Accounts
If you opt for long-term access keys, you will need to provide the Access
Key ID and Secret Access Key during the setup. In addition, you may optionally
provide an additional IAM Role.
The additional IAM Role allows for extra permissions to be granted to the
identity authenticated with the long-term access key.
On the other hand, if you choose IAM Roles for service accounts, you would
not need to provide the Access Key ID and Secret Access Key. Instead, you will
need to ensure the presence of the required IAM role.
Please consider the authentication mechanism that best suits your
requirements and follow the appropriate steps and instructions provided to
ensure a seamless authentication experience.
These mechanisms are designed to authenticate and authorize the programmatic
interactions between scripts or command line interfaces and AWS services.
Both authentication mechanisms provide secure programmatic access to
AWS resources.
Let's dive into the details:
1. Long-term access keys:
These keys are commonly used when authenticating programmatic access
to AWS resources. When creating long-term access keys, you receive
an Access key ID and a Secret Access Key. The Access Key ID serves
as the identifier for the access key, and the Secret Access Key is a
unique secret value used for authentication.
During the Helm installation process, you are given the choice to
assign a role. This role will be used during authentication when Veeam
Kasten initially authenticates using the provided Access Key ID and
Secret Access Key, along with the additional assigned role.
During the Helm installation process, you can choose to configure
long-term access secret keys and key IDs by providing the necessary
key pairs:
--set secrets.awsAccessKeyId and
--set secrets.awsSecretAccessKey.
(Optional) In addition to the long-term access keys,
you can choose to provide an additional IAM role. This additional
role will be associated with the secrets.awsIamRole configuration
parameter.
2. During the Helm installation process, you can choose to configure
long-term access secret keys and key IDs by providing the necessary
key pairs:
--set secrets.awsAccessKeyId and
--set secrets.awsSecretAccessKey.
3. (Optional) In addition to the long-term access keys,
you can choose to provide an additional IAM role. This additional
role will be associated with the secrets.awsIamRole configuration
parameter.
4. IAM Roles for Service Accounts:
IAM roles are useful in scenarios where you want to provide access to
AWS services without managing or exposing long-term access keys.
To know more about it, refer to IAM Roles for Service Accounts.
Long-term access keys:
These keys are commonly used when authenticating programmatic access
to AWS resources. When creating long-term access keys, you receive
an Access key ID and a Secret Access Key. The Access Key ID serves
as the identifier for the access key, and the Secret Access Key is a
unique secret value used for authentication.
During the Helm installation process, you are given the choice to
assign a role. This role will be used during authentication when Veeam
Kasten initially authenticates using the provided Access Key ID and
Secret Access Key, along with the additional assigned role.
AWS IAM roles grant access to AWS account resources to trusted entities.
The following links contain information on how to create roles and other
permission-related details:
- Using AWS IAM Roles with Veeam Kasten
Creating an IAM Policy
Veeam Kasten Installs with IAM Roles
Option I: Using IAM Role With a Kubernetes Service Account (EKS)
Enabling OIDC on your EKS Cluster
Creating an IAM Role for Veeam Kasten Install
Option II: Using an IAM Role With an IAM User
- Creating an IAM Policy
- Veeam Kasten Installs with IAM Roles
Option I: Using IAM Role With a Kubernetes Service Account (EKS)
Enabling OIDC on your EKS Cluster
Creating an IAM Role for Veeam Kasten Install
Option II: Using an IAM Role With an IAM User
- Option I: Using IAM Role With a Kubernetes Service Account (EKS)
Enabling OIDC on your EKS Cluster
Creating an IAM Role for Veeam Kasten Install
- Enabling OIDC on your EKS Cluster
- Creating an IAM Role for Veeam Kasten Install
- Option II: Using an IAM Role With an IAM User
### Installing Veeam Kastenï
To install on AWS, you need to define two environment variables that
specify your access key id and secret access key.
After doing so, just run the following command to install Veeam Kasten,
the Kasten platform on either AWS EKS or any other Kubernetes
distribution running on EC2.
If you want Veeam Kasten to assume an IAM Role in AWS infrastructure
operations, refer to Using AWS IAM Roles with Veeam Kasten
on how to create and use the role.
For IAM Roles for Service Accounts, once the setup is completed, you will need to
provide a token file to assign the role to the k10-k10 service account.
With the assigned role, there is no need for Access Key and Secret Access Key.
During the Veeam Kasten installation, you can choose to manually configure
the k10-k10 service account.
For additional information, refer to Associate Service Account Role.
In some scenarios, it is advantageous to avoid pre-configuring a service
account manually, and instead, leverage Helm's capabilities to streamline
the process. By providing a role through the Helm package manager using
the --set secrets.awsIamRole flag, the service account can be
dynamically created.
AWS keys or IAM Roles need to have permissions that allow Veeam Kasten to
perform operations on EBS and, if needed, EFS and S3. The minimal set
of permissions needed by Veeam Kasten for integrating against different AWS
services can be found here:
- Using Veeam Kasten with AWS EBS
- Using Veeam Kasten with AWS S3
- Using Veeam Kasten with Amazon RDS
- Using Veeam Kasten with AWS EFS
- Using Veeam Kasten with AWS Secrets Manager
- Optional KMS Permissions
The above permissions can also be used in the context of IAM Policies
and Roles. Refer to Using AWS IAM Roles with Veeam Kasten for more information
regarding IAM Policies and Roles.
Note
To address any troubleshooting issues while installing Veeam Kasten
on a Kubernetes platform using the Cilium Container Network Interface (CNI)
setup, refer to this page.
The page provides specific steps for resolving installation issues with
Cilium CNI and Veeam Kasten compatibility.
### Existing Secret Usageï
It is possible to use an existing secret
to provide the following parameters for AWS configuration:
- AWS Access Key ID
Field name - aws_access_key_id
- AWS Secret Access Key
Field name - aws_secret_access_key
- AWS IAM Role
Field name - role
To do so, the following Helm option can be used:
Please ensure that the secret exists in the namespace where Veeam Kasten
is installed.
The default namespace assumed throughout this documentation is kasten-io.
### EKS Authentication Setupï
Finally, for end-to-end instructions on how to set up token-based
authentication for AWS EKS clusters, please follow the documentation
here.
### Elastic File System Limitationï
Currently, Veeam Kasten supports backup and recovery of AWS Elastic
File System (EFS) volumes. However, due to EFS limitations, cross-cluster
EFS restores within the same region and across regions require manual
intervention using the AWS CLI or AWS console using the below
instructions.
- Using the Veeam Kasten dashboard and AWS CLI for EFS Snapshot Migration
- Using the Veeam Kasten dashboard and AWS Console for EFS Snapshot Migration
### EKS IPv6 Clustersï
To install Veeam Kasten on an IPv6 cluster, run the following command:
This will enable IPv6 listeners for all required services.
Same option can be used to enable IPv6 listeners for a dual-stack setup.
Veeam Kasten was tested in IPv6-only setup only on AWS EKS platform.
Although it is expected to work on other platforms as well.
Warning
Port-forwarding to Veeam Kasten services may not work in IPv6-only setup with Dockershim CRI.
Containerd CRI supports IPv6 port-forwarding since 1.5.2 release.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_vmware_vsphere.md
## Installing Veeam Kasten on VMware vSphereï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
Prerequisites
Installing Veeam Kasten
Validating the Install
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on VMware vSphere
### Prerequisitesï
Before installing Veeam Kasten on VMware vSphere, please
ensure that the install prerequisites are met.
Persistent Volumes must be provisioned using the vSphere CSI provisioner
or one of the other supported storage providers.
### Installing Veeam Kastenï
To backup volumes provisioned by the vSphere
CSI driver, credentials must be provided.
These credentials can be supplied either via
Helm parameters
or using a vSphere Infrastructure Profile.
### Providing the vSphere Credentials using Helmï
Setting up vSphere credentials requires configuring all of the
following Helm flags during the execution of helm install or
helm upgrade:
Also, it is possible to use an existing secret
instead of setting credentials through Helm parameters:
Note
Please ensure that the secret exists in the namespace where Veeam
Kasten is installed.
The default namespace assumed throughout this documentation is kasten-io.
### Providing Credentials via the vSphere Infrastructure Profileï
Creation of a vSphere Infrastructure Profile is
required to backup volumes provisioned by the vSphere CSI driver.
Additional information related to the management of vSphere volumes
is also found in the same section.
If a Veeam Repository will be used
to export snapshot data of vSphere CSI volumes, then
configuring Change Tracking on the nodes
would enable more efficient incremental backups.
Refer to this
or later Knowledge Base articles for details.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_storage.md
## Storage Integrationï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
Direct Provider Integration
Container Storage Interface (CSI)
CSI Requirements
Pre-Flight Checks
CSI Snapshot Configuration
AWS Storage
Amazon Elastic Block Storage (EBS) Integration
Amazon Elastic File System (EFS) Integration
AWS Infrastructure Profile
Azure Managed Disks
Service Principal
Managed Identities
Federated Identity
Other Configuration
Pure Storage
NetApp Trident
Google Persistent Disk
Ceph
CSI Integration
Snapshots as Shallow Read-Only Volumes (CephFS only)
Cinder/OpenStack
vSphere
Portworx
Veeam Backup
Instant Recovery
- Direct Provider Integration
- Container Storage Interface (CSI)
CSI Requirements
Pre-Flight Checks
CSI Snapshot Configuration
- CSI Requirements
- Pre-Flight Checks
- CSI Snapshot Configuration
- AWS Storage
Amazon Elastic Block Storage (EBS) Integration
Amazon Elastic File System (EFS) Integration
AWS Infrastructure Profile
- Amazon Elastic Block Storage (EBS) Integration
- Amazon Elastic File System (EFS) Integration
- AWS Infrastructure Profile
- Azure Managed Disks
Service Principal
Managed Identities
Federated Identity
Other Configuration
- Service Principal
- Managed Identities
- Federated Identity
- Other Configuration
- Pure Storage
- NetApp Trident
- Google Persistent Disk
- Ceph
CSI Integration
Snapshots as Shallow Read-Only Volumes (CephFS only)
- CSI Integration
- Snapshots as Shallow Read-Only Volumes (CephFS only)
- Cinder/OpenStack
- vSphere
- Portworx
- Veeam Backup
Instant Recovery
- Instant Recovery
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Storage Integration
Note
As of March 5, 2024, "Azure Active Directory" has been renamed as
"Microsoft Entra ID." Throughout this documentation, references to "Azure
Active Directory" will be updated to use both the new and old names. Both
names will be used for a while, after which the documentation will be updated
to use only the new name.
Veeam Kasten supports direct integration with public cloud storage vendors
as well as CSI integration. While most
integrations are transparent, the below sections document the
configuration needed for the exceptions.
### Direct Provider Integrationï
Veeam Kasten supports seamless and direct storage integration with a number of
storage providers. The following storage providers are either
automatically discovered and configured within Veeam Kasten or can be
configured for direct integration:
- Amazon Elastic Block Store (EBS)
- Amazon Elastic File System (EFS)
- Azure Managed Disks (Azure Managed Disks)
- Ceph
- Cinder-based providers on OpenStack
- vSphere Cloud Native Storage (CNS)
- Veeam Backup (snapshot data export only)
### Container Storage Interface (CSI)ï
Apart from direct storage provider integration, Veeam Kasten also supports
invoking volume snapshots operations via the Container Storage
Interface (CSI). To ensure that this works correctly, please ensure
the following requirements are met.
### CSI Requirementsï
- Kubernetes v1.14.0 or higher
- The VolumeSnapshotDataSource feature has been enabled in the
Kubernetes cluster
- A CSI driver that has Volume Snapshot support. Please look at the
list of CSI drivers to confirm
snapshot support.
### Pre-Flight Checksï
Assuming that the default kubectl context is pointed to a cluster
with CSI enabled, CSI pre-flight checks can be run by deploying the
primer tool with a specified StorageClass.  This tool runs in a
pod in the cluster and performs the following operations:
- Creates a sample application with a persistent volume and writes
some data to it
- Takes a snapshot of the persistent volume
- Creates a new volume from the persistent volume snapshot
- Validates the data in the new persistent volume
First, run the following command to derive the list of provisioners
along with their StorageClasses and VolumeSnapshotClasses.
Then, run the following command with a valid StorageClass to deploy the
pre-check tool:
### CSI Snapshot Configurationï
For each CSI driver, ensure that a VolumeSnapshotClass has been added
with Veeam Kasten annotation (k10.kasten.io/is-snapshot-class: "true").
Note that CSI snapshots are not durable. In particular, CSI snapshots
have a namespaced VolumeSnapshot object and a non-namespaced
VolumeSnapshotContent object.  With the default (and recommended)
deletionPolicy, if there is a deletion of a volume or the
namespace containing the volume, the cleanup of the namespaced
VolumeSnapshot object will lead to the cascading delete of the
VolumeSnapshotContent object and therefore the underlying storage
snapshot.
Setting deletionPolicy to Delete isn't sufficient either as
some storage systems will force snapshot deletion if the associated
volume is deleted (snapshot lifecycle is not independent of the
volume). Similarly, it might be possible to force-delete snapshots
through the storage array's native management interface.  Enabling
backups together with volume snapshots is therefore required for a
durable backup.
Veeam Kasten creates a clone of the original VolumeSnapshotClass with
the DeletionPolicy set to 'Retain'. When restoring a CSI VolumeSnapshot,
an independent replica is created using this cloned class to avoid
any accidental deletions of the underlying VolumeSnapshotContent.
### VolumeSnapshotClass Configurationï
Given the configuration requirements, the above code illustrates a
correctly-configured VolumeSnapshotClass for Veeam Kasten. If the
VolumeSnapshotClass does not match the above template, please
follow the below instructions to modify it.  If the existing
VolumeSnapshotClass cannot be modified, a new one can be created
with the required annotation.
1. Whenever Veeam Kasten detects volumes that were provisioned via a CSI
driver, it will look for a VolumeSnapshotClass with Veeam Kasten
annotation for the identified CSI driver and use it to create
snapshots.  You can easily annotate an existing
VolumeSnapshotClass using:
$ kubectl annotate volumesnapshotclass ${VSC_NAME} \
    k10.kasten.io/is-snapshot-class=true
Verify that only one VolumeSnapshotClass per storage
provisioner has the Veeam Kasten annotation. Currently, if no
VolumeSnapshotClass or more than one has the Veeam Kasten annotation,
snapshot operations will fail.
## List the VolumeSnapshotClasses with Veeam Kasten annotation
$ kubectl get volumesnapshotclass -o json | \
    jq '.items[] | select (.metadata.annotations["k10.kasten.io/is-snapshot-class"]=="true") | .metadata.name'
k10-snapshot-class
Whenever Veeam Kasten detects volumes that were provisioned via a CSI
driver, it will look for a VolumeSnapshotClass with Veeam Kasten
annotation for the identified CSI driver and use it to create
snapshots.  You can easily annotate an existing
VolumeSnapshotClass using:
Verify that only one VolumeSnapshotClass per storage
provisioner has the Veeam Kasten annotation. Currently, if no
VolumeSnapshotClass or more than one has the Veeam Kasten annotation,
snapshot operations will fail.
### StorageClass Configurationï
As an alternative to the above method, a StorageClass can be
annotated with the following-
(k10.kasten.io/volume-snapshot-class: "VSC_NAME").
All volumes created with this StorageClass will be snapshotted by
the specified VolumeSnapshotClass:
### Migration Requirementsï
If application migration across clusters is needed, ensure that the
VolumeSnapshotClass names match between both clusters. As the
VolumeSnapshotClass is also used for restoring volumes, an
identical name is required.
### CSI Snapshotter Minimum Requirementsï
Finally, ensure that the csi-snapshotter container for all CSI
drivers you might have installed has a minimum version of v1.2.2. If
your CSI driver ships with an older version that has known bugs, it
might be possible to transparently upgrade in place using the
following code.
### AWS Storageï
Veeam Kasten supports Amazon Web Services (AWS) storage integration, including
Amazon Elastic Block Storage (EBS) and Amazon Elastic File System (EFS)
### Amazon Elastic Block Storage (EBS) Integrationï
Veeam Kasten currently supports backup and restores of EBS CSI volumes as well as
Native (In-tree) volumes. In order to work with the In-tree provisioner,
or to migrate snapshots within AWS, Veeam Kasten requires an Infrastructure
Profile. Please refer to AWS Infrastructure Profile
on how to create one.
Block Mode Exports of EBS volumes use the AWS
EBS Direct API.
### Amazon Elastic File System (EFS) Integrationï
Veeam Kasten currently supports backup and restores of statically
provisioned EFS CSI volumes. Since statically provisioned volumes use
the entire file system we are able to utilize AWS APIs to take backups.
While the EFS CSI driver has begun supporting dynamic provisioning, it
does not create new EFS volumes. Instead, it creates and uses access points
within existing EFS volumes. The current AWS APIs do not support backups
of individual access points.
However, Veeam Kasten can take backups of these dynamically provisioned EFS
volumes using the Shareable Volume Backup and Restore
mechanism.
For all other operations, EFS requires an Infrastructure Profile. Please refer
to AWS Infrastructure Profile on how to create one.
### AWS Infrastructure Profileï
To enable Veeam Kasten to take snapshots and restore volumes from AWS, an
Infrastructure Profile must be created from the Infrastructure page of
the Profiles menu in the navigation sidebar.
The AWS Access Key and AWS Secret fields are required.
Using AWS IAM Service Account Credentials that Veeam Kasten was installed
with is also possible with the Authenticate with AWS IAM Role checkbox.
An additional AWS IAM Role can be provided if the user requires
Veeam Kasten to assume a different role.
The provided credentials are verified for both EBS and EFS.
Currently, Veeam Kasten also supports the legacy mode of providing AWS
credentials via Helm. In this case, an AWS Infrastructure Profile will
be created automatically with the values provided through Helm, and can
be seen on the Dashboard. This profile can later be replaced or updated
manually if necessary, such as when the credentials change.
In future releases, providing AWS credential via Helm will be deprecated.
### Azure Managed Disksï
Veeam Kasten supports backups and restores for both CSI volumes and
in-tree volumes within Azure Managed Disks. To work with the Azure
in-tree provisioner, Veeam Kasten requires the creation of an Infrastructure
Profile from the Infrastructure page of the Profiles menu in the
navigation sidebar.
Veeam Kasten can perform block mode exports with changed block tracking (CBT)
for volumes provisioned using the disk.csi.azure.com CSI driver. This
capability is automatically utilized when the following conditions are met:
- Veeam Kasten includes a valid Azure Infrastructure Profile
- Either the Azure Disk storage class or individual PVC enables
Block Mode Exports
- The Azure Disk volume snapshot class enables incremental snapshots, as
shown in the example below:
### Service Principalï
Veeam Kasten supports authentication with Microsoft Entra ID (formerly
Azure Active Directory) with Azure Client Secret credentials, as well as
Azure Managed Identity.
To authenticate with Azure Client Secret credentials, Veeam Kasten requires
Tenant ID, Client ID, and Client Secret.
### Managed Identitiesï
If Use Azure TenantID, Secret and ClientID to authenticate is chosen, users will
opt out of using Managed Identity and need to provide their own Tenant ID,
Client Secret and Client ID.
To use Managed Identity but provide a custom Client ID, users can choose
Custom Client ID and provide their own, otherwise the default Managed Identity will be used.
To authenticate with Azure Managed Identity, clusters must have Azure Managed Identity enabled.
### Federated Identityï
To authenticate with Azure Federated Identity (also known as workload identity),
clusters must have Azure Federated Credentials set up.
This can only be done via helm. More information can be found
here.
Federated Identity is currently only supported on Openshift clusters
with version 4.14 and later.
If you are using Federated Identity, you cannot edit or delete the
infrastructure profile once created. You can edit or delete by using helm
upgrade.
### Other Configurationï
In addition to authentication credentials, Veeam Kasten also requires Subscription ID
and Resource Group. For information on how to retrieve the required data,
please refer to Installing Veeam Kasten on Azure.
Additionally, information for Azure Stack such as Storage Environment Name,
Resource Manager Endpoint, AD Endpoint, and AD Resource
can also be specified. These fields are not mandatory, and default values
will be used if they are not provided by the user.
Field
Value
Storage Environment Name
AzurePublicCloud
Resource Manager Endpoint
https://management.azure.com/
AD Endpoint
https://login.microsoftonline.com/
AD Resource
Veeam Kasten also supports the legacy method of providing Azure credentials
via Helm. In this case, an Azure Infrastructure Profile will be created
automatically with the values provided through Helm, and can be seen on the
Dashboard. This profile can later be replaced or updated manually if necessary,
such as when the credentials change.
In future releases, providing Azure credentials via Helm will be deprecated.
### Pure Storageï
For integrating Veeam Kasten with Pure Storage, please follow Pure Storage's
instructions on deploying the Pure Storage Orchestrator
and the VolumeSnapshotClass.
Once the above two steps are completed, follow the instructions for
Veeam Kasten CSI integration. In particular, the Pure
VolumeSnapshotClass needs to be edited using the following commands.
### NetApp Tridentï
For integrating Veeam Kasten with NetApp Trident, please follow NetApp's
instructions on deploying Trident as a CSI provider
and then follow the instructions above.
### Google Persistent Diskï
Veeam Kasten supports Google Persistent Disk (GPD) storage integration with
both CSI and native (in-tree) drivers.
In order to use GPD native driver, an Infrastructure Profile must be created
from the Infrastructure page of the Profiles menu in the navigation
sidebar.
The GCP Project ID and GCP Service Key fields are required.
The GCP Service Key takes the complete content of the service account
json file when creating a new service account.
Currently, Veeam Kasten also supports the legacy mode of providing Google
credentials via Helm. In this case, a Google Infrastructure Profile will
be created automatically with the values provided through Helm, and can be
seen on the Dashboard. This profile can later be replaced or updated manually
if necessary, such as when the credentials change.
In future releases, providing Google credential via Helm will be deprecated.
### Cephï
Veeam Kasten supports Ceph RBD and Ceph FS snapshots and backups via their CSI
drivers.
### CSI Integrationï
If you are using Rook to install Ceph, Veeam Kasten only supports
Rook v1.3.0 and above. Previous versions had bugs that
prevented restore from snapshots.
Veeam Kasten supports integration with Ceph (RBD and FS) via its CSI interface
by following the instructions for CSI integration. In
particular, the Ceph VolumeSnapshotClass needs to be edited using the
following commands.
Ceph CSI RBD volume snapshots can be exported in
block mode
with the appropriate annotation on their StorageClass.
The Ceph Rados Block Device API can enable direct access to
data blocks through the network and provide information on the
allocated blocks in a snapshot, which could reduce the size and
duration of a backup;
however, it is important to note that Changed Block Tracking is
not supported for Ceph CSI RBD snapshots.
The output of the
Veeam Kasten Primer Block Mount Check
command indicates if the API will be used:
### Snapshots as Shallow Read-Only Volumes (CephFS only)ï
Veeam Kasten supports the use of snapshots as shallow read-only volumes specifically designed for file systems (FS),
particularly for the CephFS CSI driver. Using
this feature requires a special StorageClass, which is usually a copy of the
regular StorageClass of the CephFS CSI driver, but with the
backingSnapshot: "true" option in the parameters section. This StorageClass
has to meet the Veeam Kasten requirements for CSI StorageClass configuration.
In addition to this, it is necessary to define specific changes (overrides) for
the exportData setting within a policy. An illustrative example can be found
here: overrides for exportData setting of Policy.
Below is an example of how to specify these overrides for your reference:
Since 'Snapshots as a shallow read-only volumes' feature requires a read-only
mount of the Snapshot PVC during the Export phase, support for read-only mount
has to be enabled:
An Openshift cluster requires preserving SELinuxLevel of source namespace to
Kanister Pod during the Export phase. This functionality always enabled in
Veeam Kasten, thus additional actions are not required.
### Cinder/OpenStackï
Veeam Kasten supports snapshots and backups of OpenStack's Cinder block
storage.
To enable Veeam Kasten to take snapshots, an OpenStack Infrastructure
Profile must be created from the Infrastructure page of the Profiles
menu in the navigation sidebar.
The Keystone Endpoint, Project Name, Domain Name, Username
and Password are required fields.
If the OpenStack environment spans multiple regions then the Region field
must also be specified.
### vSphereï
Veeam Kasten supports vSphere storage integration with PersistentVolumes
provisioned using the vSphere CSI Provisioner.
Currently, backup and restore operations are not supported for RWX/ROX
volumes provisioned using vSAN File Services.
The available functionality varies by the type of cluster infrastructure
used and is summarized in the table below:
vSphere with Tanzu [1]
Other Kubernetes infrastructures [1]
Supported versions
7.0 U3 or higher
7.0 U1 or higher
vCenter access required [2]
Required
Export
Export in filesystem mode
Not Supported [3]
Supported
Export in block mode [4]
To an Object Storage Location, an NFS File Storage Location or a Veeam Repository [5]
Restore
Restore from a snapshot
Restore from an export (any mode)
Instant Recovery restore
From a Veeam Repository
Import
Import a filesystem mode export
Import a block mode export
From an Object Storage Location, an NFS File Storage Location or a Veeam Repository [5]
1. vSphere with Tanzu
supervisor clusters and
VMware Tanzu Kubernetes Grid
management clusters are not supported.
1. Access to vCenter is required with all types of cluster
infrastructures as Veeam Kasten directly communicates
with vSphere to snapshot a
First Class Disk (FCD),
resolve paravirtualized volume handles, set tags and access volume data with
the VMware VDDK API.
1. The guest clusters of vSphere with Tanzu use paravirtualized
PersistentVolumes.
These clusters do not support the static provisioning of a specific
FCD
from within the guest cluster itself.
This disables Veeam Kasten's ability to restore applications from their
local snapshots, Instant Recovery and the ability to export snapshot data in
filesystem mode.
1. Block mode snapshot exports
are available in all types of vSphere cluster infrastructures.
Snapshot content is accessed at the block level directly
through the network using the VMware VDDK API.
Enable changed block tracking on the VMware cluster nodes
to reduce the amount of data transferred during export.
See this Veeam Kasten knowledge base article
for how to do so in vSphere with Tanzu guest clusters.
1. Block mode snapshot exports
can be saved in an Object Storage Location, an NFS File Storage Location
or a Veeam Repository.
A vSphere Infrastructure Profile must be created from the
Infrastructure page of the Profiles menu in the navigation sidebar
to identify the vCenter server.
The vCenter Server is required and must be a valid IP address or hostname
that points to the vSphere infrastructure.
The vSphere User and vSphere Password fields are also required.
If vSphere credentials are provided during the installation of Veeam Kasten
(Installing Veeam Kasten on VMware vSphere)
those parameters will be ignored in favor of the credentials
contained in the Infrastructure profile.
It is recommended that a dedicated user account be created for Veeam Kasten.
To authorize the account, create a role with the following privileges (for 7.0.x and 8.0.x):
- Datastore Privileges(7.0 / 8.0)
Allocate space
Browse datastore
Low level file operations
- Allocate space
- Browse datastore
- Low level file operations
- Global Privileges (7.0 / 8.0)
Disable methods
Enable methods
Licenses
- Disable methods
- Enable methods
- Licenses
- Virtual Machine Snapshot Management Privileges (7.0 / 8.0)
Create snapshot
Remove snapshot
Revert to snapshot
- Create snapshot
- Remove snapshot
- Revert to snapshot
- Cryptographic operations (8.0)
Decrypt
- Decrypt
Datastore Privileges(7.0 / 8.0)
Global Privileges (7.0 / 8.0)
Virtual Machine Snapshot Management Privileges (7.0 / 8.0)
Cryptographic operations (8.0)
vSphere with Tanzu clusters require the following additional
privilege to resolve paravirtualized volume handles:
- CNS Privileges (7.0 / 8.0)
Searchable
- Searchable
CNS Privileges (7.0 / 8.0)
Also for vSphere with Tanzu, assign the can edit role to the custom user
in the vSphere Namespace using the following UI path:
- Workload Management > Namespaces > Select the namespace associated with the TKG service > Permissions > Add (assign can edit role)
Assign this role to the dedicated Veeam Kasten user account on the following objects:
- The root vCenter object
- The datacenter objects (propagate down each subtree
to reach datastore and virtual machine objects)
There is an upper limit on the maximum number of snapshots for a VMware Kubernetes
PersistentVolume.
Refer to this
or more recent VMware knowledge base articles
for the limit and for recommendations on the number of snapshots to maintain.
A Veeam Kasten backup policy
provides control over the number of local
Veeam Kasten restore points
retained, and by implication, the number of local snapshots retained.
A Veeam Kasten backup and export policy
allows separate retention policies for local and
exported Veeam Kasten restore points.
It is possible to set a 0 local restore point retention value
(i.e. no local snapshots are retained),
as long as a non-zero exported restore point retention value is set;
doing so does not adversely impact the ability to use
incremental block mode exports
with changed block tracking.
The Veeam Kasten default timeout for vSphere snapshot related operations may be
too short if you are dealing with very large volumes.
If you encounter timeout errors then adjust the vmWare.taskTimeoutMin
Helm option accordingly.
You may observe that an application's PersistentVolumes do not get deleted even
if their Reclaim Policy is Delete.
This can happen when using Veeam Kasten to restore an application in the same namespace or when
deleting or uninstalling an application previously backed up by Veeam Kasten.
This is because the VMware CSI driver fails in the deletion of PersistentVolumes
containing snapshots:
a VMware snapshot is embedded in its associated FCD volume and does not
exist independent of this volume, and
it is not possible to delete an FCD volume if it has snapshots.
The VMware CSI driver leaves such PersistentVolumes in the Released state with
a "failed to delete volume" warning (visible with
kubectl describe).
You may also see errors flagged for this operation in the vCenter GUI.
The driver re-attempts the deletion operation periodically, so
when all snapshots get deleted the PersistentVolume will eventually be deleted.
One can also attempt to manually delete the PersistentVolume again at this time.
When Veeam Kasten restores an application in the same namespace from some restore point,
new Kubernetes PersistentVolume objects (with new FCD volumes) are created for the
application.
However, any restore point that involves local snapshots will now point
into FCD volumes associated with PersistentVolume objects in the Released state!
Deletion of these Veeam Kasten restore points (manually or by schedule) will delete
the associated FCD snapshots after which the PersistentVolume objects and their
associated FCD volumes will eventually be released.
When uninstalling or deleting an application, do not
force delete Kubernetes PersistentVolume objects in the Released state
as this would orphan the associated FCD volumes!
Instead, use the vCenter GUI or a CLI tool like
govc
to manually delete the snapshots.
### Portworxï
Apart from CSI-level support, Veeam Kasten also directly integrates with the
Portworx storage platform.
To enable Veeam Kasten to take snapshots and restore volumes from Portworx, an
Infrastructure Profile must be created from the Infrastructure page
of the Profiles menu in the navigation sidebar.
The Namespace and Service Name fields are used to determine the
Portworx endpoint. If these fields are left blank the Portworx defaults of
kube-system and portworx-service will be used respectively.
In an authorization-enabled Portworx setup, the Issuer and Secret
fields must be set.
The Issuer must represent the JWT issuer. The Secret is the JWT shared
secret, which is represented by the Portworx environment variable-
PORTWORX_AUTH_JWT_SHAREDSECRET. Refer to Portworx Security
for more information.
### Veeam Backupï
A Veeam Repository can be used
as the destination for exported snapshot data from persistent volumes
provisioned by the vSphere CSI provider in supported
vSphere clusters.
See the
Integration with Veeam Backup Repositories for Kasten K10 Guide
for additional details, including the Veeam user account permissions needed,
network ports used and licensing information.
A Veeam Repository Location Profile
must be created to identify the desired repository on a particular
Veeam Backup server (immutable repositories are also supported,
refer to the setup instructions for more details),
A Veeam Repository can only store the image based volume data
from the backup, so a policy which uses a Veeam Repository
location profile will always be used in conjunction with another
location profile that will be used to store the remaining data
in a Veeam Kasten restore point.
A Veeam Repository Location Profile
cannot be used as a destination for Kanister actions in a Backup policy.
A Veeam Backup Policy will be created in the Veeam Backup server for each
distinct Veeam Kasten protected application and Veeam Kasten backup and
export policy pair encountered when the Veeam Kasten backup and export
policy is executed. The Veeam Kasten catalog identifier is added to the
name to ensure uniqueness across multiple clusters that back up to the
same Veeam Backup server.
Data from a manual (i.e. not associated with a Veeam Kasten backup and
export policy) export of an application's volumes is associated with a
fixed policy called Kasten K10 Manual Backup and is saved as a
VeeamZIP backup.
Veeam Kasten will delete any Veeam restore point associated with a Veeam
Kasten restore point being retired.
Import and restoration of Veeam Kasten restore points that contain
snapshot data exported to a Veeam Repository is possible in supported
vSphere clusters using
volumes provisioned by the vSphere CSI driver.
As Veeam Kasten restore points are not saved in the Veeam Repository
the import action is actually performed on the location profile
that contains the Veeam Kasten restore point being imported. A
Veeam Repository Location Profile
Veeam Kasten object with the same name as that used on the exporting system
must be present in the importing system and will be referenced
during the restore action.
Snapshot data is accessed in block mode directly through the VMware
VDDK API.
If change block tracking is enabled in the VMware cluster nodes,
Veeam Kasten will send incremental changes to the Veeam Backup Server
if possible; if incremental upload is not possible a full backup will be
done each export. Regardless, Veeam Kasten will convert Veeam restore
points into a synthetic full to satisfy Veeam Kasten retirement
functionality.
### Instant Recoveryï
Instant Recovery will get an exported restore point up and running much faster
than a regular restore.  This feature requires vSphere 7.0.3+ and a Veeam
Backup server version V12 or higher.  This is not supported on vSphere with
Tanzu clusters at this time.  Before using Instant Recovery, you should ensure
that all Storage Classes in your Kubernetes clusters are configured to avoid
placing new volumes in the Instant Recovery datastore.  Please see this
Knowledge Base article
for recommendations on Storage Classes for use with Instant Recovery.
When a Veeam Kasten Instant Recovery is triggered, rather than creating
volumes and populating them with data from VBR, Veeam Kasten asks the Veeam
Backup server to do an Instant Recovery of the FCDs (vSphere First Class
Disks) that are needed and then creates PVs that use those FCDs. The FCDs
exist in a vPower NFS datastore created by the Veeam Backup server and
attached to the vSphere cluster hosting the Kubernetes cluster.
Once the Instant Recovery has completed, the application will be running
using the Veeam Backup server storage.  At that point, the virtual
disks will be migrated into their permanent home with no interruption
in service.  The application will not see any differences in how it
is using the storage and all of the pods using the disks will continue
operating without any restarts.  The migration will start automatically after
the Instant recovery process completes.
Currently Instant Recovery is only supported for
Restore Actions,
not Restore Policies.  To use Instant Recovery, select the
Enable Instant Recovery checkbox (this will only appear if all
compatibility criteria are met) or set the InstantRecovery property
in the RestoreAction spec.
All restore features are supported with Instant Recovery.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_digitalocean_digitalocean.md
## Installing Veeam Kasten on DigitalOceanï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on DigitalOcean
### Prerequisitesï
Before installing Veeam Kasten on DigitalOcean, please ensure that the
install prerequisites are met.
### Installing Veeam Kastenï
To install Veeam Kasten on DigitalOcean, you also need to annotate the
VolumeSnapshotClass as specified in our CSI documentation.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_other_k3s.md
## Installing Veeam Kasten on K3Sï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on K3S
### Prerequisitesï
Before installing Veeam Kasten on k3s, please ensure that the
install prerequisites are met.
### Installing Veeam Kastenï
To install Veeam Kasten on k3s, you also need to annotate the
default VolumeSnapshotClass as specified in our CSI documentation.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_shareable-volume.md
## Shareable Volume Backup and Restoreï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
Supported storage providers
Prerequisites
Create a Location Profile
- Supported storage providers
- Prerequisites
Create a Location Profile
- Create a Location Profile
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Shareable Volume Backup and Restore
In some situations Veeam Kasten may not currently support the creation of
snapshots through the underlying storage provider. Generally, we recommend
backing up volumes in these circumstances using the
Generic Volume Snapshot method. However, this method
involves configuring the application with a Kanister sidecar
container that will mount the volume concerned and copy out the data.
As a special case, when the storage concerned is capable of being shared
between pods, Veeam Kasten can back up the data without any modifications
to the application. This is done by using an external pod in the application
namespace.
### Supported storage providersï
The following storage providers support this feature-
- Amazon Elastic File System (EFS)
### Prerequisitesï
### Create a Location Profileï
If you haven't done so already, create a Location profile with
the appropriate Location and Credentials information from the Veeam
Kasten settings page. Instructions for creating location profiles
can be found here
Warning
Shareable volume backup and restore workflows are not
compatible with immutable backups location profiles.
Immutable backups enabled location profiles can be used with these
workflows, but will be treated as a non-immutability-enabled profile:
the protection period will be ignored, and no point-in-time restore
functionality will be provided. Please note that use of an object-locking
bucket for such cases can amplify storage usage without any additional
benefit.
Shareable volume backup and restore workflows are not
compatible with NFS FileStore location profiles.
The location profile must be present for shareable volume backups to work.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_offline.md
## Air-Gapped Installï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
Air-Gapped Veeam Kasten Installation
Fetching the Helm Chart for Local Use
Installing Veeam Kasten with Local Helm Chart and Container Images
Installing Veeam Kasten with Disconnected OpenShift Operator
Running Veeam Kasten Within a Local Network
Providing Credentials if Local Container Repository is Private
Preparing Veeam Kasten Container Images for Air-Gapped Use
List Veeam Kasten Container Images
Copy Kasten Images into a Private Repository
Copy Kasten Images to/from a Filesystem Directory
Using Iron Bank Veeam Kasten Container Images
- Air-Gapped Veeam Kasten Installation
Fetching the Helm Chart for Local Use
Installing Veeam Kasten with Local Helm Chart and Container Images
Installing Veeam Kasten with Disconnected OpenShift Operator
Running Veeam Kasten Within a Local Network
Providing Credentials if Local Container Repository is Private
- Fetching the Helm Chart for Local Use
- Installing Veeam Kasten with Local Helm Chart and Container Images
- Installing Veeam Kasten with Disconnected OpenShift Operator
- Running Veeam Kasten Within a Local Network
- Providing Credentials if Local Container Repository is Private
- Preparing Veeam Kasten Container Images for Air-Gapped Use
List Veeam Kasten Container Images
Copy Kasten Images into a Private Repository
Copy Kasten Images to/from a Filesystem Directory
Using Iron Bank Veeam Kasten Container Images
- List Veeam Kasten Container Images
- Copy Kasten Images into a Private Repository
- Copy Kasten Images to/from a Filesystem Directory
- Using Iron Bank Veeam Kasten Container Images
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Air-Gapped Install
For environments that are connected to the Internet, one needs access
to three repositories to install Veeam Kasten:
- The Helm repository that contains the Veeam Kasten chart
- The container registry that contains the Veeam Kasten container images
- Upstream repositories to install Veeam Kasten dependencies (e.g., Prometheus)
However, if an air-gapped installation is required, it is possible to
use your own private container registry to install Veeam Kasten. While this can
always be done manually, the k10tools image command makes it easier to
automate the process.
- Air-Gapped Veeam Kasten Installation
Fetching the Helm Chart for Local Use
Installing Veeam Kasten with Local Helm Chart and Container Images
Installing Veeam Kasten with Disconnected OpenShift Operator
Running Veeam Kasten Within a Local Network
Providing Credentials if Local Container Repository is Private
- Preparing Veeam Kasten Container Images for Air-Gapped Use
List Veeam Kasten Container Images
Copy Kasten Images into a Private Repository
Copy Kasten Images to/from a Filesystem Directory
Using Iron Bank Veeam Kasten Container Images
Air-Gapped Veeam Kasten Installation
Preparing Veeam Kasten Container Images for Air-Gapped Use
### Air-Gapped Veeam Kasten Installationï
If the Veeam Kasten container images are already available in a private
repository, the below instructions can be used to install in an
air-gapped environment. If needed, support for uploading images to a
private image registry is documented below.
### Fetching the Helm Chart for Local Useï
To fetch the most recent Veeam Kasten Helm chart for local use, run
the following command to pull the latest Veeam Kasten chart as a
compressed tarball (.tgz) file into the working directory.
If you need to fetch a specific version, please run the following command:
### Installing Veeam Kasten with Local Helm Chart and Container Imagesï
If the Veeam Kasten container images were uploaded to a registry at
repo.example.com, an air-gapped installation can be performed by
setting global.airgapped.repository=repo.example.com as shown in
the below command:
### Installing Veeam Kasten with Disconnected OpenShift Operatorï
To install Veeam Kasten with an OpenShift operator in an air-gapped
cluster, follow the steps under
offline operator install.
### Running Veeam Kasten Within a Local Networkï
To run Veeam Kasten in a network without the ability to connect to the
internet, Veeam Kasten needs to be installed in an air-gapped mode with
the helm value metering.mode=airgap as shown in the command below:
Note
If metering.mode=airgap is not set in an offline cluster, some functionality
will be disabled. A message warning that Veeam Kasten is "Unable to validate license" will
be displayed in the web based user interface. Errors containing messages
"Could not get google bucket for metrics", "License check failed" and "Unable to validate license"
will be logged.
If the metering service is unable to connect to the internet for 24 hours,
the metering service will restart.
### Providing Credentials if Local Container Repository is Privateï
If the local repository that has been provided as the value of
global.airgapped.repository is private, credentials for that
repository can be provided using secrets.dockerConfig and
global.imagePullSecret flags, as below, with
the helm install command.
Our Helm chart creates a secret with the name k10-ecr
with the value that has been provided for secrets.dockerConfig.
That's why we are providing secret name k10-ecr as value of
global.imagePullSecret.
### Preparing Veeam Kasten Container Images for Air-Gapped Useï
There are multiple ways to use a private repository including setting
up a caching or proxy image registry that points to the Veeam Kasten
image repositories using tools such as JFrog Artifactory. However, if
images need to be manually uploaded or an automated upload pipeline is
required to add Veeam Kasten images into your private repository, the
following documentation should help.
To see all available commands and flags for running k10tools image please
run the following:
The following commands operate against the latest version of Veeam Kasten
(7.5.7).
Warning
k10tools image is only supported for versions 7.5.0+ of Veeam Kasten and
must match the version you're installing.
For older version, please refer to their documentation: https://docs.kasten.io/<version>/install/offline.html.
### List Veeam Kasten Container Imagesï
The following command will list all images used by the current Veeam Kasten
version (7.5.7). This can be helpful if there is a requirement to tag and
push Veeam Kasten images into your private repository manually instead of using
the Kasten provided tool documented below.
### Copy Kasten Images into a Private Repositoryï
The following command will copy the Veeam Kasten container images into your
specified registry. If the destination image tag should be different than the
Veeam Kasten version, then the --dst-image-tag can be used to specify a new
image tag.
The following example uses a repository located at repo.example.com.
This command will use your local docker config if the private registry
requires authentication.
The credsStore field in the $HOME/.docker/config.json is used to
specify the credential store. This is typically an external credential
store requiring an external helper and it may not be usable from within
the docker container. Please refer to the docker documentation
for more information.
Alternatively, k10tools image provides authentication mechanisms such as
passing a username and password (--dst-username and --dst-password
flags) or a bearer token (--dst-token flag). Please refer to
the help flag for more information.
After running the previous command, use the
instructions above to install Veeam Kasten via images
uploaded to repo.example.com.
### Copy Kasten Images to/from a Filesystem Directoryï
Network limitations may limit the ability to directly copy images into a
private repository. Alternatively, images can be copied to the local filesystem
and then pushed to a repository separately. This requires downloading the
k10tools binary.
The following example copies the images to a directory images. This
directory can then be used to upload to a private repository located at
repo.example.com.
### Using Iron Bank Veeam Kasten Container Imagesï
If you want to use the Iron Bank hardened Veeam Kasten images in an air-gapped
environment, execute the above commands but replace
image with ironbank image:
This ensures the images are pulled from Registry1.
You must be logged in to the docker registry locally for this process
to function correctly. Use docker login registry1.dso.mil --username
"${REGISTRY1_USERNAME}" --password-stdin with your Registry1 CLI secret as
the password to login.
Alternatively, provide credentials using the methods
described above.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_generic.md
## Generic Storage Backup and Restoreï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
Activating Generic Storage Backup
Using Sidecars
Enabling Kanister Sidecar Injection
Updating the resource manifest
End-to-End Example
Prerequisites
Deploy the application
Create a Location Profile
Insert Data
Backup Data
Destroy Data
Restore Data
Verify Data
Generic Storage Backup and Restore on Unmounted PVCs
- Activating Generic Storage Backup
- Using Sidecars
Enabling Kanister Sidecar Injection
Updating the resource manifest
- Enabling Kanister Sidecar Injection
- Updating the resource manifest
- End-to-End Example
Prerequisites
Deploy the application
Create a Location Profile
Insert Data
Backup Data
Destroy Data
Restore Data
Verify Data
- Prerequisites
- Deploy the application
- Create a Location Profile
- Insert Data
- Backup Data
- Destroy Data
- Restore Data
- Verify Data
- Generic Storage Backup and Restore on Unmounted PVCs
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Generic Storage Backup and Restore
Warning
Generic Storage Backup must be used only in cases
where migration to a CSI driver with snapshot support is not possible.
For more details, refer to this page.
Applications can often be deployed using non-shared storage (e.g.,
local SSDs) or on systems where Veeam Kasten does not currently support
the underlying storage provider. To protect data in these scenarios,
Veeam Kasten with Kanister provides you with the ability
to add functionality for backup, restore, and migration of application data
with minimal modifications. This can be done in an efficient and
transparent manner.
While a complete example is provided below, the only changes needed are
the activation of Generic Storage Backup (GSB) on Veeam Kasten (see below),
addition of a sidecar to your application deployment that can mount the
application data volume, and an annotation that requests GSB.
### Activating Generic Storage Backupï
By default, the GSB feature is disabled. It can be activated by providing
an activation token when installing Veeam Kasten via the Helm chart.
Existing customers can contact Kasten by Veeam Support via MyVeeam,
to open a support case and request the activation token for GSB.
For all current prospects evaluating Veeam Kasten, we recommend reaching out to
your local Kasten by Veeam Sales team through the local point of contact within
the Veeam channel.
Provide the cluster ID (UUID of the default namespace) when requesting
an activation token. This ID will help Veeam Kasten identify a cluster where
GSB is activated. Use the following kubectl command to get the UUID:
Once the token is obtained, provide it to Veeam Kasten with the following Helm
option:
Note
A separate activation token is required for every cluster
where you want to activate GSB.
### Using Sidecarsï
The sidecar can be added either by leveraging Veeam Kasten's sidecar injection
feature or by manually patching the resource as described below.
### Enabling Kanister Sidecar Injectionï
Veeam Kasten implements a Mutating Webhook Server which mutates workload
objects by injecting a Kanister sidecar into the workload when the
workload is created. The Mutating Webhook Server also adds the
k10.kasten.io/forcegenericbackup annotation to the targeted
workloads to enforce generic backup. By default, the sidecar injection
feature is disabled. To enable this feature, the following options
need to be used when installing Veeam Kasten via the Helm chart:
Once enabled, Kanister sidecar injection will be enabled for all
workloads in all namespaces. To perform sidecar injections on
workloads only in specific namespaces, the namespaceSelector
labels can be set using the following option:
By setting namespaceSelector labels, the Kanister sidecar will be
injected only in the workloads which will be created in the namespace
matching labels with namespaceSelector labels.
Similarly, to inject the sidecar for only specific workloads,
the objectSelector option can be set as shown below:
It is recommended to add at least one namespaceSelector or
objectSelector when enabling the injectGenericVolumeBackupSidecar feature.
Otherwise, Veeam Kasten will try to inject a sidecar into every new workload.
In the common case, this will lead to undesirable results and potential
performance issues.
For example, to inject sidecars into workloads that match the label
component: db and are in namespaces that are labeled with
k10/injectGenericVolumeBackupSidecar: true, the following options should be
added to the Veeam Kasten Helm install command:
The labels set with namespaceSelector and objectSelector are
mutually inclusive. This means that if both the options are set to
perform sidecar injection, the workloads should have labels matching
the objectSelector labels AND they have to be created in the
namespace with labels that match the namespaceSelector
labels. Similarly, if multiple labels are specified for either
namespaceSelector or objectSelector, they will all needed to
match for a sidecar injection to occur.
For the sidecar to choose a security context that can
read data from the volume, Veeam Kasten performs the following checks in order:
1. If there are multiple primary containers, the list of containers will be
iterated over, and the SecurityContext of the containers will be merged so
that the final SecurityContext is the most restrictive one. If there is
only one primary container, the final SecurityContext of the sidecar will
be the SecurityContext of the primary container.
2. If the workload PodSpec has a SecurityContext set, the sidecar
does not need an explicit specification and will automatically use
the context from the PodSpec.
3. If the above criteria are not met, by default, no SecurityContext
will be set.
The SecurityContext of the sidecar will have some additional "add"
capabilities, and while selecting the most restrictive security context,
some operations will be restricted. See this
Veeam Kasten knowledge base article for more details.
When the helm option for providing a Root CA to Veeam Kasten,
i.e cacertconfigmap.name, is enabled, the Mutating Webhook will create a
new ConfigMap, if it does not already exist, in the application namespace to
provide the Root CA to the sidecar. This ConfigMap in the application
namespace would be a copy of the Root CA ConfigMap residing in the Veeam Kasten
namespace.
Sidecar injection for standalone Pods is not currently supported.
Refer to the following section to manually add the the Kanister sidecar
to standalone Pods.
### Updating the resource manifestï
Alternatively, the Kanister sidecar can be added by updating the
resource manifest with the Kanister sidecar. An example, where
/data is used as an sample mount path, can be seen in the below
specification. Note that the sidecar must be named
kanister-sidecar and the sidecar image version should be pinned to
the latest Kanister release.
Alternatively, the below command can be run to add the sidecar into the
workload. Make sure to specify correct values for the specified
placeholders resource_type, namespace, resource_name,
volume-name and volume-mount-path:
After injecting the sidecar manually, workload pods
will be recreated. If the deployment strategy used for the
workload is RollingUpdate,
the workload should be scaled down and scaled up
so that the volumes are mounted into the
newly created pods.
Once the above changes are made, Veeam Kasten will be able to automatically
extract data and, using its data engine, efficiently
deduplicate data and transfer it into an object store or NFS file store.
If you have multiple volumes used by your pod, you simply need to
mount them all within this sidecar container. There is no naming
requirement on the mount path as long as they are unique.
Note that a backup operation can take up to 800 MB of memory for
some larger workloads. To ensure the pod containing the kanister-sidecar
is scheduled on a node with sufficient memory for a particularly intensive
workload, you can add a resource request to the container definition.
### Generic Backup Annotationï
Generic backups can be requested by adding the
k10.kasten.io/forcegenericbackup annotation to the workload as shown in the
example below.
The following is a kubectl example to add the annotation to a running
deployment:
Finally, note that the Kanister sidecar and Location profile must both
be present for generic backups to work.
### Required Capabilities for Generic Storage Backupï
OpenShift Container Platform (OCP) introduced more restrictive default
security context constraints (SCCs) in
the 4.11 release - Pod Security Admission.
The change affects the ability to perform rootless
Generic Storage Backup.
Since K10 5.5.8 rootless is a default behavior for
Veeam Kasten.
To use Generic Storage Backup with OCP 4.11 and above,
the following capabilities must be allowed:
- FOWNER
- CHOWN
- DAC_OVERRIDE
Even if Veeam Kasten is installed on Kubernetes distributions other than OCP,
the capabilities mentioned above are required for ensuring the proper
functionality of Generic Storage Backup.
Previous version of restricted SCC can be used as a template.
Change the allowedCapabilities field as follows:
### End-to-End Exampleï
The below section provides a complete end-to-end example of how to
extend your application to support generic backup and restore. A dummy
application is used below but it should be straightforward to extend
this example.
### Prerequisitesï
- Make sure you have obtained the activation token and have Veeam Kasten
installed by providing the token using the genericStorageBackup.token
option.
- Make sure you have installed Veeam Kasten with
injectGenericVolumeBackupSidecar enabled.
- (Optional) namespaceSelector labels are set for
injectGenericVolumeBackupSidecar.
injectGenericVolumeBackupSidecar can be enabled by passing the following
flags while installing Veeam Kasten helm chart
### Deploy the applicationï
The following specification contains a complete example of how to
exercise generic backup and restore functionality. It consists of a an
application Deployment that use a Persistent Volume Claim (mounted
internally at /data) for storing data.
Saving the below specification as a file, deployment.yaml, is
recommended for reuse later.
- Create a namespace:
$ kubectl create namespace <namespace>
If injectGenericVolumeBackupSidecar.namespaceSelector labels are set while
installing Veeam Kasten, add the labels to namespace to match with
namespaceSelector
$ kubectl label namespace <namespace> k10/injectGenericVolumeBackupSidecar=true
- Deploy the above application as follows:
## Deploying in a specific namespace
$ kubectl apply --namespace=<namespace> -f deployment.yaml
- Check status of deployed application:
List pods in the namespace. The demo-app pods can be seen created with two
containers.
## List pods
$ kubectl get pods --namespace=<namespace> | grep demo-app
## demo-app-56667f58dc-pbqqb   2/2     Running   0          24s
- Describe the pod and verify the kanister-sidecar container is injected
with the same volumeMounts.
volumeMounts:
- name: data
  mountPath: /data
Create a namespace:
If injectGenericVolumeBackupSidecar.namespaceSelector labels are set while
installing Veeam Kasten, add the labels to namespace to match with
namespaceSelector
Deploy the above application as follows:
Check status of deployed application:
List pods in the namespace. The demo-app pods can be seen created with two
containers.
Describe the pod and verify the kanister-sidecar container is injected
with the same volumeMounts.
### Create a Location Profileï
If you haven't done so already, create a Location profile with
the appropriate Location and Credentials information from the Veeam
Kasten settings page. Instructions for creating location profiles can be
found here
Generic storage backup and restore workflows are not
compatible with immutable backups location profiles.
Immutable backups enabled location profiles can be used with these
workflows, but will be treated as a non-immutability-enabled profile:
the protection period will be ignored, and no point-in-time restore
functionality will be provided. Please note that use of an object-locking
bucket for such cases can amplify storage usage without any additional
benefit.
### Insert Dataï
The easiest way to insert data into the demo application is to simply
copy it in:
### Backup Dataï
Backup the application data either by creating a Policy or running a
Manual Backup from Veeam Kasten. This assumes that the application is
running on a system where Veeam kasten does not support the provisioned
disks (e.g., local storage). Make sure to specify the location profile
in the advanced settings for the policy. This is required to perform
Kanister operations.
This policy covers an application running in the namespace sampleApp.
For complete documentation of the Policy CR, refer to Policy API Type.
### Destroy Dataï
To destroy the data manually, run the following command:
Alternatively, the application and the PVC can be deleted and recreated.
### Restore Dataï
Restore the data using Veeam Kasten by selecting the appropriate restore point.
### Verify Dataï
After restore, you should verify that the data is intact. One way to
verify this is to use MD5 checksum tool.
The MD5 checksums should match.
### Generic Storage Backup and Restore on Unmounted PVCsï
Generic Storage Backup and Restore on unmounted PVCs can be enabled by adding
k10.kasten.io/forcegenericbackup annotation to the StorageClass with which
the volumes have been provisioned.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_advanced.md
## Advanced Install Optionsï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
FREE Veeam Kasten Edition and Licensing
Using a Custom License During Install
Changing Licenses
Add Licenses via Dashboard
License Grace period
Manually Creating or Using an Existing Service Account
Pinning Veeam Kasten to Specific Nodes
Using Trusted Root Certificate Authority Certificates for TLS
Install Root CA in Veeam Kasten's namespace
Install Root CA in Application's Namespace When Using Kanister Sidecar
Troubleshooting
Running Veeam Kasten Containers as a Specific User
Configuring Prometheus
Complete List of Veeam Kasten Helm Options
Helm Configuration for Parallel Upload to the Storage Repository
Helm Configuration for Parallel Download from the Storage Repository
Setting Custom Labels and Annotations on Veeam Kasten Pods
- FREE Veeam Kasten Edition and Licensing
Using a Custom License During Install
Changing Licenses
Add Licenses via Dashboard
License Grace period
- Using a Custom License During Install
- Changing Licenses
- Add Licenses via Dashboard
- License Grace period
- Manually Creating or Using an Existing Service Account
- Pinning Veeam Kasten to Specific Nodes
- Using Trusted Root Certificate Authority Certificates for TLS
Install Root CA in Veeam Kasten's namespace
Install Root CA in Application's Namespace When Using Kanister Sidecar
Troubleshooting
- Install Root CA in Veeam Kasten's namespace
- Install Root CA in Application's Namespace When Using Kanister Sidecar
- Troubleshooting
- Running Veeam Kasten Containers as a Specific User
- Configuring Prometheus
- Complete List of Veeam Kasten Helm Options
- Helm Configuration for Parallel Upload to the Storage Repository
- Helm Configuration for Parallel Download from the Storage Repository
- Setting Custom Labels and Annotations on Veeam Kasten Pods
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Advanced Install Options
### FREE Veeam Kasten Edition and Licensingï
By default, Veeam Kasten comes with an embedded free edition license.
The free edition license allows you to use the software on a cluster
with at most 50 worker nodes in the first 30 days, and then 5 nodes after the
30-day period.
In order to continue using the free license, regular updates to stay within the
6 month support window might be required.
You can remove the node restriction of the free license by updating to
Enterprise Edition and obtaining the appropriate license from the Kasten team.
### Using a Custom License During Installï
To install a license that removes the node restriction,
please add the following to any of the helm install commands:
or, to install a license from a file:
Note
### Changing Licensesï
To add a new license to Veeam Kasten, a secret needs to be created in
the Veeam Kasten namespace (default is kasten-io) with the requirement
that the license text be set in a field named license. To do this
from the command line, run:
or, to add a license from a file:
The resulting license will look like:
Similarly, old licenses can be removed by deleting the secret that
contains it.
### Add Licenses via Dashboardï
It is possible to add a license via the Licenses page of the Settings
menu in the navigation sidebar. The license can be pasted directly into the
text field or loaded from a .lic file.
### License Grace periodï
If the license status of the cluster becomes invalid (e.g., the licensed node
limit is exceeded), the ability to perform manual actions or creating new
policies will be disabled but your previously scheduled policies will continue
to run for 50 days. The displayed warning will be look like:
By default, Veeam Kasten provides a grace period of 50 days to ensure that
applications remain protected while a new license is obtained or the cluster
is brought back into compliance by reducing the number of nodes. Veeam Kasten
will stop the creation of any new jobs (scheduled or manual) after the grace
period expires.
If the cluster's license status frequently swaps between valid and invalid
states, the amount of time the cluster license spends in an invalid status
will be subtracted from subsequent grace periods.
You can see node usage from the last two months via the Licenses page of
the Settings menu in the navigation sidebar. Usage starts being tracked
from the installation date of 4.5.8+. From 5.0.11+ you can see the same
information through Prometheus.
### Manually Creating or Using an Existing Service Accountï
For more information regarding ServiceAccount restrictions with Kasten,
please refer to this documentation.
The following instructions can be used to create a new Service Account
that grants Veeam Kasten the required permissions to Kubernetes resources
and the use the given Service Account as a part of the install process.
The instructions assume that you will be installing Veeam Kasten in
the kasten-io namespace.
Following the SA creation, you can install Veeam Kasten using:
### Pinning Veeam Kasten to Specific Nodesï
While not generally recommended, there might be situations (e.g., test
environments, nodes reserved for infrastructure tools, or clusters
without autoscaling enabled) where Veeam Kasten might need to be pinned
to a subset of nodes in your cluster. You can do this easily with an
existing deployment by using a combination of NodeSelectors
and Taints and Tolerations.
The process to modify a deployment to accomplish this is demonstrated
in the following example. The example assumes that the nodes you want
to restrict Veeam Kasten to have the label selector-key: selector-value
and a taint set to taint-key=taint-value:NoSchedule.
### Using Trusted Root Certificate Authority Certificates for TLSï
For temporary testing of object storage systems that are
deployed using self-signed certificates signed by a trusted
Root CA, it is also possible to
disable certificate verification if the
Root CA certificate is not easily available.
If the S3-compatible object store configured in a Location Profile
was deployed with a self-signed certificate that was signed by a
trusted Root Certificate Authority (Root CA), then the certificate for
such a certificate authority has to be provided to Veeam Kasten to enable
successful verification of TLS connections to the object store.
Similarly, to authenticate with a private OIDC provider whose self-signed
certificate was signed by a trusted Root CA, the certificate for
the Root CA has to be provided to Veeam Kasten to enable successful
verification of TLS connections to the OIDC provider.
Multiple Root CAs can be bundled together in the same file.
### Install Root CA in Veeam Kasten's namespaceï
Assuming Veeam Kasten will be deployed in the kasten-io namespace, the
following instructions will make a private Root CA certificate
available to Veeam kasten.
The name of the Root CA certificate must be custom-ca-bundle.pem
To provide the Root CA certificate to Veeam Kasten, add the following
to the Helm install command.
### Install Root CA in Application's Namespace When Using Kanister Sidecarï
If you either use Veeam Kasten's Kanister sidecar injection feature for
injecting the Kanister sidecar in your application's namespace or if you
have manually added the Kanister sidecar, you must create a ConfigMap
containing the Root CA in the application's namespace and update the
application's specification so that the ConfigMap is mounted as a Volume.
This will enable the Kanister sidecar to verify TLS connections
successfully using the Root CA in the ConfigMap.
Assuming that the application's namespace is named test-app, use the
following command to create a ConfigMap containing the Root CA in the
application's namespace:
This is an example of a VolumeMount that must be added to the
application's specification.
This is an example of a Volume that must be added to the
application's specification.
### Troubleshootingï
If Veeam Kasten is deployed without the cacertconfigmap.name setting,
validation failures such as the one shown below will be seen while configuring
a Location Profile using the web based user interface.
In the absence of the cacertconfigmap.name setting, authentication
with a private OIDC provider will fail. Veeam Kasten's logs will show an error
x509: certificate signed by unknown authority.
If you do not install the Root CA in the application namespace when using a
Kanister sidecar with the application, the logs will show an error
x509: certificate signed by unknown authority when the sidecar
tries to connect to any endpoint that requires TLS verification.
### Running Veeam Kasten Containers as a Specific Userï
Veeam Kasten service containers run with UID and fsGroup 1000 by
default. If the storage class Veeam Kasten is configured to use for its own
services requires the containers to run as a specific user, then the user
can be modified.
This is often needed when using shared storage, such as NFS, where permissions
on the target storage require a specific user.
To run as a specific user (e.g., root (0), add the following
to the Helm install command:
Other SecurityContext settings for the Veeam Kasten service containers can be specified using the --set service.securityContext.<setting name> and --set prometheus.server.securityContext.<setting name> options.
### Configuring Prometheusï
Prometheus is an open-source system monitoring
and alerting toolkit bundled with Veeam Kasten.
When passing value from the command line, the value key has to be prefixed
with the prometheus. string:
When passing values in a YAML file, all prometheus settings should be
under the prometheus key:
To modify the bundled Prometheus configuration, only
use the helm values listed in the Complete List of Veeam Kasten Helm Options.
Any undocumented configurations may affect the functionality of the
Veeam Kasten. Additionally, Veeam Kasten does not support disabling
Prometheus service, which may lead to unsupported
scenarios, potential monitoring and logging issues, and overall
functionality disruptions. It is recommended to keep these services
enabled to ensure proper functionality and prevent unexpected behavior.
### Complete List of Veeam Kasten Helm Optionsï
The following table lists the configurable parameters of the K10
chart and their default values.
Parameter
Description
Default
eula.accept
Whether to enable accept EULA before installation
false
eula.company
Company name. Required field if EULA is accepted
None
eula.email
Contact email. Required field if EULA is accepted
license
License string obtained from Kasten
rbac.create
Whether to enable RBAC with a specific cluster role and binding for K10
true
scc.create
Whether to create a SecurityContextConstraints for K10 ServiceAccounts
scc.priority
Sets the SecurityContextConstraints priority
15
services.dashboardbff.hostNetwork
Whether the dashboardbff Pods may use the node network
services.executor.hostNetwork
Whether the executor Pods may use the node network
services.aggregatedapis.hostNetwork
Whether the aggregatedapis Pods may use the node network
serviceAccount.create
Specifies whether a ServiceAccount should be created
serviceAccount.name
The name of the ServiceAccount to use. If not set, a name is derived using the release and chart names.
ingress.create
Specifies whether the K10 dashboard should be exposed via ingress
ingress.name
Optional name of the Ingress object for the K10 dashboard. If not set, the name is formed using the release name.
{Release.Name}-ingress
ingress.class
Cluster ingress controller class: nginx, GCE
ingress.host
FQDN (e.g., k10.example.com) for name-based virtual host
ingress.urlPath
URL path for K10 Dashboard (e.g., /k10)
Release.Name
ingress.pathType
Specifies the path type for the ingress resource
ImplementationSpecific
ingress.annotations
Additional Ingress object annotations
{}
ingress.tls.enabled
Configures a TLS use for ingress.host
ingress.tls.secretName
Optional TLS secret name
ingress.defaultBackend.service.enabled
Configures the default backend backed by a service for the K10 dashboard Ingress (mutually exclusive setting with ingress.defaultBackend.resource.enabled).
ingress.defaultBackend.service.name
The name of a service referenced by the default backend (required if the service-backed default backend is used).
ingress.defaultBackend.service.port.name
The port name of a service referenced by the default backend (mutually exclusive setting with port number, required if the service-backed default backend is used).
ingress.defaultBackend.service.port.number
The port number of a service referenced by the default backend (mutually exclusive setting with port name, required if the service-backed default backend is used).
ingress.defaultBackend.resource.enabled
Configures the default backend backed by a resource for the K10 dashboard Ingress (mutually exclusive setting with ingress.defaultBackend.service.enabled).
ingress.defaultBackend.resource.apiGroup
Optional API group of a resource backing the default backend.
''
ingress.defaultBackend.resource.kind
The type of a resource being referenced by the default backend (required if the resource default backend is used).
ingress.defaultBackend.resource.name
The name of a resource being referenced by the default backend (required if the resource default backend is used).
global.persistence.size
Default global size of volumes for K10 persistent services
20Gi
global.persistence.catalog.size
Size of a volume for catalog service
global.persistence.jobs.size
Size of a volume for jobs service
global.persistence.logging.size
Size of a volume for logging service
global.persistence.metering.size
Size of a volume for metering service
global.persistence.storageClass
Specified StorageClassName will be used for PVCs
global.podLabels
Configures custom labels to be set to all Kasten Pods
global.podAnnotations
Configures custom annotations to be set to all Kasten Pods
global.airgapped.repository
Specify the helm repository for offline (airgapped) installation
global.imagePullSecret
Provide secret which contains docker config for private repository. Use k10-ecr when secrets.dockerConfigPath is used.
global.prometheus.external.host
Provide external prometheus host name
global.prometheus.external.port
Provide external prometheus port number
global.prometheus.external.baseURL
Provide Base URL of external prometheus
global.network.enable_ipv6
Enable IPv6 support for K10
google.workloadIdentityFederation.enabled
Enable Google Workload Identity Federation for K10
google.workloadIdentityFederation.idp.type
Identity Provider type for Google Workload Identity Federation for K10
google.workloadIdentityFederation.idp.aud
Audience for whom the ID Token from Identity Provider is intended
secrets.awsAccessKeyId
AWS access key ID (required for AWS deployment)
secrets.awsSecretAccessKey
AWS access key secret
secrets.awsIamRole
ARN of the AWS IAM role assumed by K10 to perform any AWS operation.
secrets.awsClientSecretName
The secret that contains AWS access key ID, AWS access key secret and AWS IAM role for AWS
secrets.googleApiKey
Non-default base64 encoded GCP Service Account key
secrets.googleProjectId
Sets Google Project ID other than the one used in the GCP Service Account
secrets.azureTenantId
Azure tenant ID (required for Azure deployment)
secrets.azureClientId
Azure Service App ID
secrets.azureClientSecret
Azure Service APP secret
secrets.azureClientSecretName
The secret that contains ClientID, ClientSecret and TenantID for Azure
secrets.azureResourceGroup
Resource Group name that was created for the Kubernetes cluster
secrets.azureSubscriptionID
Subscription ID in your Azure tenant
secrets.azureResourceMgrEndpoint
Resource management endpoint for the Azure Stack instance
secrets.azureADEndpoint
Azure Active Directory login endpoint
secrets.azureADResourceID
Azure Active Directory resource ID to obtain AD tokens
secrets.microsoftEntraIDEndpoint
Microsoft Entra ID login endpoint
secrets.microsoftEntraIDResourceID
Microsoft Entra ID resource ID to obtain AD tokens
secrets.azureCloudEnvID
Azure Cloud Environment ID
secrets.vsphereEndpoint
vSphere endpoint for login
secrets.vsphereUsername
vSphere username for login
secrets.vspherePassword
vSphere password for login
secrets.vsphereClientSecretName
The secret that contains vSphere username, vSphere password and vSphere endpoint
secrets.dockerConfig
Set base64 encoded docker config to use for image pull operations. Alternative to the secrets.dockerConfigPath
secrets.dockerConfigPath
Use --set-file secrets.dockerConfigPath=path_to_docker_config.yaml to specify docker config for image pull. Will be overwritten if secrets.dockerConfig is set
cacertconfigmap.name
Name of the ConfigMap that contains a certificate for a trusted root certificate authority
clusterName
Cluster name for better logs visibility
metering.awsRegion
Sets AWS_REGION for metering service
metering.mode
Control license reporting (set to airgap for private-network installs)
metering.reportCollectionPeriod
Sets metric report collection period (in seconds)
1800
metering.reportPushPeriod
Sets metric report push period (in seconds)
3600
metering.promoID
Sets K10 promotion ID from marketing campaigns
metering.awsMarketplace
Sets AWS cloud metering license mode
metering.awsManagedLicense
Sets AWS managed license mode
metering.redhatMarketplacePayg
Sets Red Hat cloud metering license mode
metering.licenseConfigSecretName
Sets AWS managed license config secret
externalGateway.create
Configures an external gateway for K10 API services
externalGateway.annotations
Standard annotations for the services
externalGateway.fqdn.name
Domain name for the K10 API services
externalGateway.fqdn.type
Supported gateway type: route53-mapper or external-dns
externalGateway.awsSSLCertARN
ARN for the AWS ACM SSL certificate used in the K10 API server
auth.basicAuth.enabled
Configures basic authentication for the K10 dashboard
auth.basicAuth.htpasswd
A username and password pair separated by a colon character
auth.basicAuth.secretName
Name of an existing Secret that contains a file generated with htpasswd
auth.k10AdminGroups
A list of groups whose members are granted admin level access to K10's dashboard
auth.k10AdminUsers
A list of users who are granted admin level access to K10's dashboard
auth.tokenAuth.enabled
Configures token based authentication for the K10 dashboard
auth.oidcAuth.enabled
Configures Open ID Connect based authentication for the K10 dashboard
auth.oidcAuth.providerURL
URL for the OIDC Provider
auth.oidcAuth.redirectURL
URL to the K10 gateway service
auth.oidcAuth.scopes
Space separated OIDC scopes required for userinfo. Example: "profile email"
auth.oidcAuth.prompt
The type of prompt to be used during authentication (none, consent, login or select_account)
select_account
auth.oidcAuth.clientID
Client ID given by the OIDC provider for K10
auth.oidcAuth.clientSecret
Client secret given by the OIDC provider for K10
auth.oidcAuth.clientSecretName
The secret that contains the Client ID and Client secret given by the OIDC provider for K10
auth.oidcAuth.usernameClaim
The claim to be used as the username
sub
auth.oidcAuth.usernamePrefix
Prefix that has to be used with the username obtained from the username claim
auth.oidcAuth.groupClaim
Name of a custom OpenID Connect claim for specifying user groups
auth.oidcAuth.groupPrefix
All groups will be prefixed with this value to prevent conflicts
auth.oidcAuth.sessionDuration
Maximum OIDC session duration
1h
auth.oidcAuth.refreshTokenSupport
Enable OIDC Refresh Token support
auth.openshift.enabled
Enables access to the K10 dashboard by authenticating with the OpenShift OAuth server
auth.openshift.serviceAccount
Name of the service account that represents an OAuth client
auth.openshift.clientSecret
The token corresponding to the service account
auth.openshift.clientSecretName
The secret that contains the token corresponding to the service account
auth.openshift.dashboardURL
The URL used for accessing K10's dashboard
auth.openshift.openshiftURL
The URL for accessing OpenShift's API server
auth.openshift.insecureCA
To turn off SSL verification of connections to OpenShift
auth.openshift.useServiceAccountCA
Set this to true to use the CA certificate corresponding to the Service Account auth.openshift.serviceAccount usually found at /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
auth.openshift.caCertsAutoExtraction
Set this to false to disable the OCP CA certificates automatic extraction to the K10 namespace
auth.ldap.enabled
Configures Active Directory/LDAP based authentication for the K10 dashboard
auth.ldap.restartPod
To force a restart of the authentication service Pod (useful when updating authentication config)
auth.ldap.dashboardURL
auth.ldap.host
Host and optional port of the AD/LDAP server in the form host:port
auth.ldap.insecureNoSSL
Required if the AD/LDAP host is not using TLS
auth.ldap.insecureSkipVerifySSL
To turn off SSL verification of connections to the AD/LDAP host
auth.ldap.startTLS
When set to true, ldap:// is used to connect to the server followed by creation of a TLS session. When set to false, ldaps:// is used.
auth.ldap.bindDN
The Distinguished Name(username) used for connecting to the AD/LDAP host
auth.ldap.bindPW
The password corresponding to the bindDN for connecting to the AD/LDAP host
auth.ldap.bindPWSecretName
The name of the secret that contains the password corresponding to the bindDN for connecting to the AD/LDAP host
auth.ldap.userSearch.baseDN
The base Distinguished Name to start the AD/LDAP search from
auth.ldap.userSearch.filter
Optional filter to apply when searching the directory
auth.ldap.userSearch.username
Attribute used for comparing user entries when searching the directory
auth.ldap.userSearch.idAttr
AD/LDAP attribute in a user's entry that should map to the user ID field in a token
auth.ldap.userSearch.emailAttr
AD/LDAP attribute in a user's entry that should map to the email field in a token
auth.ldap.userSearch.nameAttr
AD/LDAP attribute in a user's entry that should map to the name field in a token
auth.ldap.userSearch.preferredUsernameAttr
AD/LDAP attribute in a user's entry that should map to the preferred_username field in a token
auth.ldap.groupSearch.baseDN
The base Distinguished Name to start the AD/LDAP group search from
auth.ldap.groupSearch.filter
Optional filter to apply when searching the directory for groups
auth.ldap.groupSearch.nameAttr
The AD/LDAP attribute that represents a group's name in the directory
auth.ldap.groupSearch.userMatchers
List of field pairs that are used to match a user to a group.
auth.ldap.groupSearch.userMatchers.userAttr
Attribute in the user's entry that must match with the groupAttr while searching for groups
auth.ldap.groupSearch.userMatchers.groupAttr
Attribute in the group's entry that must match with the userAttr while searching for groups
auth.groupAllowList
A list of groups whose members are allowed access to K10's dashboard
services.securityContext
Custom security context for K10 service containers
{"runAsUser" : 1000, "fsGroup": 1000}
services.securityContext.runAsUser
User ID K10 service containers run as
1000
services.securityContext.runAsGroup
Group ID K10 service containers run as
services.securityContext.fsGroup
FSGroup that owns K10 service container volumes
siem.logging.cluster.enabled
Whether to enable writing K10 audit event logs to stdout (standard output)
siem.logging.cloud.path
Directory path for saving audit logs in a cloud object store
k10audit/
siem.logging.cloud.awsS3.enabled
Whether to enable sending K10 audit event logs to AWS S3
injectGenericVolumeBackupSidecar.enabled
Enables injection of sidecar container required to perform Generic Volume Backup into workload Pods
injectGenericVolumeBackupSidecar.namespaceSelector.matchLabels
Set of labels to select namespaces in which sidecar injection is enabled for workloads
injectGenericVolumeBackupSidecar.objectSelector.matchLabels
Set of labels to filter workload objects in which the sidecar is injected
injectGenericVolumeBackupSidecar.webhookServer.port
Port number on which the mutating webhook server accepts request
8080
gateway.resources.[requests|limits].[cpu|memory]
Resource requests and limits for gateway Pod
gateway.service.externalPort
Specifies the gateway services external port
80
genericVolumeSnapshot.resources.[requests|limits].[cpu|memory]
Specifies resource requests and limits for generic backup sidecar and all temporary Kasten worker Pods. Superseded by ActionPodSpec
multicluster.enabled
Choose whether to enable the multi-cluster system components and capabilities
multicluster.primary.create
Choose whether to setup cluster as a multi-cluster primary
multicluster.primary.name
Primary cluster name
multicluster.primary.ingressURL
Primary cluster dashboard URL
prometheus.k10image.registry
(optional) Set Prometheus image registry.
gcr.io
prometheus.k10image.repository
(optional) Set Prometheus image repository.
kasten-images
prometheus.rbac.create
(optional) Whether to create Prometheus RBAC configuration. Warning - this action will allow prometheus to scrape Pods in all k8s namespaces
prometheus.alertmanager.enabled
DEPRECATED: (optional) Enable Prometheus alertmanager service
prometheus.alertmanager.serviceAccount.create
DEPRECATED: (optional) Set true to create ServiceAccount for alertmanager
prometheus.networkPolicy.enabled
DEPRECATED: (optional) Enable Prometheus networkPolicy
prometheus.prometheus-node-exporter.enabled
DEPRECATED: (optional) Enable Prometheus node-exporter
prometheus.prometheus-node-exporter.serviceAccount.create
DEPRECATED: (optional) Set true to create ServiceAccount for prometheus-node-exporter
prometheus.prometheus-pushgateway.enabled
DEPRECATED: (optional) Enable Prometheus pushgateway
prometheus.prometheus-pushgateway.serviceAccount.create
DEPRECATED: (optional) Set true to create ServiceAccount for prometheus-pushgateway
prometheus.scrapeCAdvisor
DEPRECATED: (optional) Enable Prometheus ScrapeCAdvisor
prometheus.server.enabled
(optional) If false, K10's Prometheus server will not be created, reducing the dashboard's functionality.
prometheus.server.securityContext.runAsUser
(optional) Set security context runAsUser ID for Prometheus server Pod
65534
prometheus.server.securityContext.runAsNonRoot
(optional) Enable security context runAsNonRoot for Prometheus server Pod
prometheus.server.securityContext.runAsGroup
(optional) Set security context runAsGroup ID for Prometheus server Pod
prometheus.server.securityContext.fsGroup
(optional) Set security context fsGroup ID for Prometheus server Pod
prometheus.server.retention
(optional) K10 Prometheus data retention
"30d"
prometheus.server.strategy.rollingUpdate.maxSurge
DEPRECATED: (optional) The number of Prometheus server Pods that can be created above the desired amount of Pods during an update
"100%"
prometheus.server.strategy.rollingUpdate.maxUnavailable
DEPRECATED: (optional) The number of Prometheus server Pods that can be unavailable during the upgrade process
prometheus.server.strategy.type
DEPRECATED: (optional) Change default deployment strategy for Prometheus server
"RollingUpdate"
prometheus.server.persistentVolume.enabled
DEPRECATED: (optional) If true, K10 Prometheus server will create a Persistent Volume Claim
prometheus.server.persistentVolume.size
(optional) K10 Prometheus server data Persistent Volume size
8Gi
prometheus.server.persistentVolume.storageClass
(optional) StorageClassName used to create Prometheus PVC. Setting this option overwrites global StorageClass value
""
prometheus.server.configMapOverrideName
DEPRECATED: (optional) Prometheus configmap name to override default generated name
k10-prometheus-config
prometheus.server.fullnameOverride
(optional) Prometheus deployment name to override default generated name
prometheus-server
prometheus.server.baseURL
(optional) K10 Prometheus external url path at which the server can be accessed
/k10/prometheus/
prometheus.server.prefixURL
(optional) K10 Prometheus prefix slug at which the server can be accessed
prometheus.server.serviceAccounts.server.create
DEPRECATED: (optional) Set true to create ServiceAccount for Prometheus server service
resources.<deploymentName>.<containerName>.[requests|limits].[cpu|memory]
Overwriting the default K10 container resource requests and limits
varies depending on the container
route.enabled
Specifies whether the K10 dashboard should be exposed via route
route.host
FQDN (e.g., .k10.example.com) for name-based virtual host
route.path
/
route.annotations
Additional Route object annotations
route.labels
Additional Route object labels
route.tls.enabled
Configures a TLS use for route.host
route.tls.insecureEdgeTerminationPolicy
Specifies behavior for insecure scheme traffic
Redirect
route.tls.termination
Specifies the TLS termination of the route
edge
limiter.executorReplicas
Specifies the number of executor-svc Pods used to process Kasten jobs
3
limiter.executorThreads
Specifies the number of threads per executor-svc Pod used to process Kasten jobs
8
limiter.workloadSnapshotsPerAction
Per action limit of concurrent manifest data snapshots, based on workload (ex. Namespace, Deployment, StatefulSet, VirtualMachine)
5
limiter.csiSnapshotsPerCluster
Cluster-wide limit of concurrent CSI VolumeSnapshot creation requests
10
limiter.directSnapshotsPerCluster
Cluster-wide limit of concurrent non-CSI snapshot creation requests
limiter.snapshotExportsPerAction
Per action limit of concurrent volume export operations
limiter.snapshotExportsPerCluster
Cluster-wide limit of concurrent volume export operations
limiter.genericVolumeBackupsPerCluster
Cluster-wide limit of concurrent Generic Volume Backup operations
limiter.imageCopiesPerCluster
Cluster-wide limit of concurrent ImageStream container image backup (i.e. copy from) and restore (i.e. copy to) operations
limiter.workloadRestoresPerAction
Per action limit of concurrent manifest data restores, based on workload (ex. Namespace, Deployment, StatefulSet, VirtualMachine)
limiter.csiSnapshotRestoresPerAction
Per action limit of concurrent CSI volume provisioning requests when restoring from VolumeSnapshots
limiter.volumeRestoresPerAction
Per action limit of concurrent volume restore operations from an exported backup
limiter.volumeRestoresPerCluster
Cluster-wide limit of concurrent volume restore operations from exported backups
cluster.domainName
Specifies the domain name of the cluster
timeout.blueprintBackup
Specifies the timeout (in minutes) for Blueprint backup actions
45
timeout.blueprintRestore
Specifies the timeout (in minutes) for Blueprint restore actions
600
timeout.blueprintDelete
Specifies the timeout (in minutes) for Blueprint delete actions
timeout.blueprintHooks
Specifies the timeout (in minutes) for Blueprint backupPrehook and backupPosthook actions
20
timeout.checkRepoPodReady
Specifies the timeout (in minutes) for temporary worker Pods used to validate backup repository existence
timeout.statsPodReady
Specifies the timeout (in minutes) for temporary worker Pods used to collect repository statistics
timeout.efsRestorePodReady
Specifies the timeout (in minutes) for temporary worker Pods used for shareable volume restore operations
timeout.workerPodReady
Specifies the timeout (in minutes) for all other temporary worker Pods used during Veeam Kasten operations
timeout.jobWait
Specifies the timeout (in minutes) for completing execution of any child job, after which the parent job will be canceled. If no value is set, a default of 10 hours will be used
awsConfig.assumeRoleDuration
Duration of a session token generated by AWS for an IAM role. The minimum value is 15 minutes and the maximum value is the maximum duration setting for that IAM role. For documentation about how to view and edit the maximum session duration for an IAM role see https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html##id_roles_use_view-role-max-session. The value accepts a number along with a single character m(for minutes) or h (for hours)  Examples: 60m or 2h
awsConfig.efsBackupVaultName
Specifies the AWS EFS backup vault name
k10vault
vmWare.taskTimeoutMin
Specifies the timeout for VMWare operations
60
encryption.primaryKey.awsCmkKeyId
Specifies the AWS CMK key ID for encrypting K10 Primary Key
garbagecollector.daemonPeriod
Sets garbage collection period (in seconds)
21600
garbagecollector.keepMaxActions
Sets maximum actions to keep
garbagecollector.actions.enabled
Enables action collectors
kubeVirtVMs.snapshot.unfreezeTimeout
Defines the time duration within which the VMs must be unfrozen while backing them up. To know more about format go doc can be followed
5m
excludedApps
Specifies a list of applications to be excluded from the dashboard & compliance considerations. Format should be a YAML array
["kube-system", "kube-ingress", "kube-node-lease", "kube-public", "kube-rook-ceph"]
workerPodMetricSidecar.enabled
Enables a sidecar container for temporary worker Pods used to push Pod performance metrics to Prometheus
workerPodMetricSidecar.metricLifetime
Specifies the period after which metrics for an individual worker Pod are removed from Prometheus
2m
workerPodMetricSidecar.pushGatewayInterval
Specifies the frequency for pushing metrics into Prometheus
30s
workerPodMetricSidecar.resources.[requests|limits].[cpu|memory]
Specifies resource requests and limits for the temporary worker Pod metric sidecar
forceRootInBlueprintActions
Forces any Pod created by a Blueprint to run as root user
defaultPriorityClassName
Specifies the default priority class name for all K10 deployments and ephemeral Pods
priorityClassName.<deploymentName>
Overrides the default priority class name for the specified deployment
ephemeralPVCOverhead
Set the percentage increase for the ephemeral Persistent Volume Claim's storage request, e.g. PVC size = (file raw size) * (1 + ephemeralPVCOverhead)
0.1
datastore.parallelUploads
Specifies how many files can be uploaded in parallel to the data store
datastore.parallelDownloads
Specifies how many files can be downloaded in parallel from the data store
datastore.parallelBlockUploads
Specifies how many blocks can be uploaded in parallel to the data store
datastore.parallelBlockDownloads
Specifies how many blocks can be downloaded in parallel from the data store
kastenDisasterRecovery.quickMode.enabled
Enables K10 Quick Disaster Recovery
fips.enabled
Specifies whether K10 should be run in the FIPS mode of operation
workerPodCRDs.enabled
Specifies whether K10 should use ActionPodSpec for granular resource control of worker Pods
workerPodCRDs.resourcesRequests.maxCPU
Max CPU which might be setup in ActionPodSpec
workerPodCRDs.resourcesRequests.maxMemory
Max memory which might be setup in ActionPodSpec
workerPodCRDs.defaultActionPodSpec.name
The name of ActionPodSpec that will be used by default for worker Pod resources.
workerPodCRDs.defaultActionPodSpec.namespace
The namespace of ActionPodSpec that will be used by default for worker Pod resources.
### Helm Configuration for Parallel Upload to the Storage Repositoryï
Veeam Kasten provides an option to manage parallelism for
file mode
uploads to the storage repository through a configurable parameter,
datastore.parallelUploads via Helm. To upload N files in parallel to the
storage repository, configure this flag to N. This flag is adjusted when
dealing with larger PVCs to improve performance. By default, the value is set
to 8.
A similar option called datastore.parallelBlockUploads is used to control
how many blocks can be uploaded concurrently when exporting a snapshot in
block mode.
Adjusting this value may be necessary to decrease the upload time for larger
PVCs but comes at a cost of additional memory utilization in the ephemeral
Pod launched for the operation.
By default, the value is set to 8.
These parameters should not be modified unless
instructed by the support team.
### Helm Configuration for Parallel Download from the Storage Repositoryï
Veeam Kasten provides an option to manage parallelism for
file mode
downloads from the storage repository through a configurable parameter,
datastore.parallelDownloads via Helm. To download N files in parallel from
the storage repository, configure this flag to N. This flag is adjusted when
dealing with larger PVCs to improve performance. By default, the value is set
to 8.
A similar option called datastore.parallelBlockDownloads is used to
control how many blocks can be downloaded concurrently when restoring from a
snapshot exported in block mode.
Adjusting this value may be necessary to decrease the restore time for larger
PVCs but comes at a cost of additional memory utilization in the ephemeral
Pod launched for the operation.
By default, the value is set to 8.
### Setting Custom Labels and Annotations on Veeam Kasten Podsï
Veeam Kasten provides the ability to apply labels and annotations to all of its
pods. This applies to both core pods and all temporary worker pods created
as a result of Veeam Kasten operations. Labels and annotations are
applied using the global.podLabels and global.podAnnotations Helm
flags, respectively.
For example, if using a values.yaml file:
Alternatively, the Helm parameters can be configured using the --set
flag:
Labels and annotations passed using these Helm parameters
(global.podLabels and global.podAnnotations) apply to
the Prometheus pod as well, if it is managed by
Veeam Kasten. However, if labels and annotations are set in the Prometheus
sub-chart, they will be prioritized over the global pod labels
and annotations set.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_vault_vault.md
## Configuring Vault Server for Kubernetes Authï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
Bootstrapping Passkeys Before Install
Passphrases
AWS Customer Managed Keys
HashiCorp Vault Transit Secrets Engine
PassKey Management
- Bootstrapping Passkeys Before Install
Passphrases
AWS Customer Managed Keys
HashiCorp Vault Transit Secrets Engine
- Passphrases
- AWS Customer Managed Keys
- HashiCorp Vault Transit Secrets Engine
- PassKey Management
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Configuring Veeam Kasten Encryption
- Configuring Vault Server for Kubernetes Auth
Refer to the Vault Authentication
documentation
for additional help.
There are a few steps required for configuring Vault in order
for Kubernetes Authentication to work properly:
Create a policy that has the following permissions, which are
needed by Veeam Kasten:
Next, create a role that will bind the Veeam Kasten service account and
namespace to the vault policy:
© Copyright 2017-2024, Kasten, Inc.
### latest_install_aws_aws_permissions.md
## Using Veeam Kasten with AWS EBSï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on AWS
- Using Veeam Kasten with AWS EBS
The following permissions are needed by Kasten to operate on EBS, AWS
EC2's underlying block storage solution
The following additional permissions are required to use the
EBS Direct API
to get changed block data in a Block Mode Export.
While Veeam Kasten can use AWS S3 to migrate applications between
different clusters or even clouds, the access permissions should
not be specified as a part of the Veeam Kasten install, but instead
later as a part of creating Location profiles.
The credentials used for the profile should have the following
permissions on the needed buckets.
Additional permissions are needed for the creation and maintenance
of immutable backups in Veeam Kasten.
- s3:ListBucketVersions
- s3:GetObjectRetention
- s3:PutObjectRetention
- s3:GetBucketObjectLockConfiguration
- s3:GetBucketVersioning
- s3:GetObjectVersion
- s3:DeleteObjectVersion
The credentials specified as a part of creating
Location profiles should have the following
permissions for Veeam Kasten to perform Amazon RDS operations.
Veeam Kasten assumes that the user has successfully provisioned an EFS
volume and is using the EFS CSI driver to mount the
volume within Kubernetes. While Veeam Kasten will transparently work
with this setup, there are a couple of things to be aware of when
using Veeam Kasten to back up EFS that is different from EBS.
- Veeam Kasten creates its own vault to back up EFS.
- EFS volumes are created externally and today require manual cleanup
when all references to them from Kubernetes are gone. This also means
that when a restore happens, a manual cleanup of the old volumes
will be needed.
- Unlike EBS, EFS backups can be slow because of the underlying AWS
performance constraints with different data sets. Backup policy
action frequencies should be set to accommodate this performance
difference.
Finally, to operate on AWS EFS, Veeam Kasten will need the following
permissions to perform backups and restores.
When enabling Veeam Kasten DR using AWS Secrets Manager, it is
required that an AWS Infrastructure Profile
is created prior with credentials that have the adequate permissions.
More policy examples for secrets in AWS Secrets Manager are
documented here.
When operating on Encrypted EBS volumes, Veeam Kasten will ensure
snapshots and any new volumes created from those snapshots are encrypted
with the same key.
If Customer Managed Keys (CMKs) are used to encrypt the EBS volumes,
the following permissions should be granted for all KMS keys.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_google_service_account_install.md
## Creating a New Service Accountï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Google Cloud
- Creating a New Service Account
Veeam Kasten requires a newly created service account to contain the following
roles:
Note
Currently, the Google Service Account key needs to be created in the same GCP account as the GKE cluster.
The following steps should be used to create the service account and
add the required permissions:
Use the base64 tool to encode the k10-sa-key.json file generated above,
and then install Veeam Kasten with the newly created credentials.
### Using a Custom Project IDï
If the Google Service Account belongs to a project other than the one
in which the cluster is located, then the project's ID for the cluster
must also be provided during the installation.
### Existing Secret Usageï
It is possible to use an existing secret
to provide Service Account and Project ID.
To do so, the following Helm option can be used:
Please ensure that the secret exists in the namespace where Veeam Kasten
is installed.
The default namespace assumed throughout this documentation is kasten-io.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_openshift_helm.md
## Helm based Installationï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Helm based Installation
OpenShift on Azure
Operator based Installation
Managed Red Hat OpenShift Offerings
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
Helm based Installation
OpenShift on Azure
Operator based Installation
Managed Red Hat OpenShift Offerings
- Helm based Installation
- OpenShift on Azure
- Operator based Installation
- Managed Red Hat OpenShift Offerings
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Red Hat OpenShift
### Prerequisitesï
Before installing Veeam Kasten on Red Hat OpenShift, please ensure that the
install prerequisites are met.
### Veeam Kasten Installationï
Depending on your OpenShift infrastructure provider, you might need to
provide access credentials as specified elsewhere for public cloud
providers.
You will also need to add the following argument to create the
SecurityContextConstraints for Veeam Kasten ServiceAccounts.
### OpenShift on AWSï
When deploying OpenShift on AWS without using the EBS CSI driver
for persistent storage, make sure that you configure
these policies
before executing the installation command provided below:
When running OpenShift on Azure, you need to specify a credential if
you want to snapshot your volumes using in-tree (non-CSI) storage.
Veeam Kasten supports the following credentials types described below.
### Service Principalï
If using service principal, the principal needs a contributor role on
the resource group. You also need to specify the resource group of the
openshift nodes and the subscription id.
### Federated Identityï
If using federated identity, the user-assigned managed identity needs
a contributor role on the resource group. The federated identity needs
to be created and setup for the Veeam Kasten Service Account.
While installing Veeam Kasten, specify the azureClientId of the
user-assigned managed identity along with the resource group of the
openshift nodes and the subscription id. You also need to set the
useFederatedIdentity flag.
### Accessing Dashboard via Routeï
As documented here, the Veeam Kasten
dashboard can also be accessed via an OpenShift Route.
### Authenticationï
### OpenShift OAuth serverï
As documented here, the OpenShift OAuth
server can be used to authenticate access to Veeam Kasten.
### Using an OAuth Proxyï
As documented here, the OpenShift OAuth
proxy can be used for authenticating access to Veeam Kasten.
### Securing Veeam Kasten with SecurityContextConstraintsï
Veeam Kasten installs customized SecurityContextConstraints (SCC)
to ensure that all workloads associated with Veeam Kasten
have just enough privileges to perform their respective tasks.
For additional information about SCCs, please refer to the official
OpenShift documentation
Note
Starting with OpenShift 4.14, a new openshift.io/required-scc annotation was introduced.
Veeam Kasten applies this annotation to its own pods to ensure that the correct SecurityContextConstraints (SCC) have been applied.
Please note that pods created for Kanister Execution Hooks execution will not receive the openshift.io/required-scc annotation.
For more information, visit the Managing security context constraints.
### SecurityContextConstraints customizationï
The value of the Priority field in
SecurityContextConstraints (SCC) can be adjusted to align the
priority with the existing cluster configuration.
To set the desired Priority value in an Operator-managed
installation, modify the YAML of the Veeam Kasten Operand
configuration with the parameters below:
This customization can be achieved in a Helm-based installation
by adding the following parameter to the Helm command:
### SecurityContextConstraints Leakageï
OpenShift assigns SCC to workloads automatically.
By default, the most restrictive SCC matching a workload
security requirement will be selected and assigned to
that workload.
One of the criteria for SCC selection is the availability of the
SCC to a User or ServiceAccount.
SCC leakage means that some workloads might get an SCC
applied to them, which was not the intended one.
Veeam Kasten protects its SCC from leaking onto other workloads
by limiting access only to its dedicated ServiceAccount:
In this example, and in the rest of this page, Veeam Kasten is
installed into the namespace kasten-io (default), the
ServiceAccount name is the default one - k10-k10, and the
SCC name is also the default one - k10-scc.
If the cluster being considered has a different configuration,
those values need to be adapted to match the values used during
Veeam Kasten's installation in this cluster.
Despite the usage restrictions, it is still possible
to get Veeam Kasten's SCC assigned to other workloads.
This could happen when a workload is started by a cluster admin
or any other user with an allowed use action on all SCCs (*)
or on Veeam Kasten's specific SCC (k10-scc).
This is because users with the ClusterRole cluster-admin
bound to them have unlimited access to all available
SCCs, without any restrictions.
Veeam Kasten's SCC may be unexpectedly applied to workloads it
was not intended for under the following conditions:
- The workload is initiated by a user with cluster admin privileges
- The user initiating the workload has a role that grants access to all SCCs
### How to verify if access to a specific SecurityContextConstraints is grantedï
OpenShift's command line (CLI) client, oc, has a can-i command
that can be used with impersonation to check if a user can perform
a specific action on a specific resource.
Alternatively, the standard kubectl CLI client also has the same
command built-in and can be used to perform the same check.
Simply replace oc with kubectl in the command below.
To check if a user can use/access Veeam Kasten's SCC, the following
command can be used:
The output will contain yes if the specified user is able to use
Veeam Kasten's SCC or no if it is not.
For example, the output for the following check,
"Can Veeam Kasten's ServiceAccount use Veeam Kasten's SCC", should be yes:
Detailed information about can-i and impersonation
can be found in the official Kubernetes documentation.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
### Using Veeam Kasten Console Pluginï
The Veeam Kasten operator includes the OpenShift Console Plugin, providing
faster and more convenient access to the essential data about the Veeam Kasten
application state.
### Enable Veeam Kasten Console Pluginï
The Veeam Kasten Console Plugin can be enabled during the installation of the
Veeam Kasten operator. For more details, see
Veeam Kasten Installation
To enable the plugin for existing K10 deployments, navigate to the
Operator Details page for Veeam Kasten operator in the OpenShift Console.
In the Console Plugin section on the right-hand side, select the
Enabled checkbox.
If Veeam Kasten was installed using
Helm based Installation, enabling the plugin from the
Console Details page will be the only available option. Navigate to the
Console Plugins tab of the Console Details page in the OpenShift
Console. Find the Veeam Kasten Plugin from OpenShift Console and select the
Enabled checkbox.
### Veeam Kasten Console Plugin UI Overviewï
The Veeam Kasten Console Plugin adds a new Veeam Kasten tab to the
OpenShift Web Console panel on the left. Click on the tab to open the plugin.
The plugin UI contains all the essential data from the
Veeam Kasten Dashboard, including the system overview and the
recent activity.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_openshift_operator.md
## Operator based Installationï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Helm based Installation
OpenShift on Azure
Operator based Installation
Managed Red Hat OpenShift Offerings
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
Helm based Installation
OpenShift on Azure
Operator based Installation
Managed Red Hat OpenShift Offerings
- Helm based Installation
- OpenShift on Azure
- Operator based Installation
- Managed Red Hat OpenShift Offerings
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on Red Hat OpenShift
Note
With the 7.0 release in May 2024, "Kasten by Veeam" and
"Kasten K10" have been replaced with "Veeam Kasten for Kubernetes."
Throughout this documentation, references to "K10" will be modified
to include both the new and simpler "Veeam Kasten" names. Both names
will be used for a while, and then the documentation will be
modified only to use the new names. The name K10 is still used for
functional examples.
### Veeam Kasten Operator Editionsï
- Veeam Kasten (Free): Free edition of Veeam Kasten for use in clusters
up to 5 nodes
- Veeam Kasten (Enterprise - PAYGO): Enterprise edition of Veeam Kasten,
billed per usage of node-hours
- Veeam Kasten (Enterprise - Term): Enterprise edition of Veeam Kasten
intended to be used with a term license
### Pre-Flight Checksï
Assuming that your default oc context is pointed to the cluster you want
to install Veeam Kasten on, you can run pre-flight checks by deploying the
primer tool. This tool runs in a pod in the cluster and does the following:
- Validates if the Kubernetes settings meet the Veeam Kasten requirements.
- Catalogs the available StorageClasses.
- If a CSI provisioner exists, it will also perform a basic validation of the
cluster's CSI capabilities and any relevant objects that may be required. It
is strongly recommended that the same tool be used to also perform a more
complete CSI validation using the documentation here.
Note that this will create and clean up a ServiceAccount and
ClusterRoleBinding to perform sanity checks on your Kubernetes cluster.
Run the following command to deploy the pre-check tool:
### Prerequisitesï
Before installing Veeam Kasten, it is essential to have a functional
and accessible Red Hat OpenShift environment.
Optionally, you can create a new project in advance
where Veeam Kasten will be installed. Select this project during
operator deployment, or create a project (namespace) during the
operator installation process.
By default, the documentation uses the kasten-io namespace.
### Veeam Kasten Installationï
### Interactive Demoï
### Step-by-Step Guideï
1. Select the OperatorHub from the Operators Menu, search for Veeam
Kasten. Select either the Certified Operator, or Marketplace version,
depending on the requirements.
1. To begin the installation, simply click Install.
1. Next, set the channel to stable and the installation mode to A specific
namespace on the cluster. Choose the kasten-io project created in
an earlier step. Optionally, enable the console plugin provided with the
Veeam Kasten operator. For more information on the plugin, refer to the
plugin documentation.
1. After installation, click Create Instance on the operator details
page to create a Veeam Kasten instance.
1. The default installation can be done through either the Form View or
YAML View. By default, no changes are required to install.
Veeam Kasten assumes that the default storage class is supported by SSDs or
equivalent fast storage media. If this assumption is not true, please modify
the installation values to specify a performance-oriented storage
class. This modification can be done within the form view or
directly within the YAML of the Veeam Kasten Operand configuration by
setting the parameters below:
global:
  persistence:
    storageClass: <storage-class-name>
The default installation can be done through either the Form View or
YAML View. By default, no changes are required to install.
Veeam Kasten assumes that the default storage class is supported by SSDs or
equivalent fast storage media. If this assumption is not true, please modify
the installation values to specify a performance-oriented storage
class. This modification can be done within the form view or
directly within the YAML of the Veeam Kasten Operand configuration by
setting the parameters below:
### Offline Operator Installï
Only Veeam Kasten Operator Editions "Veeam Kasten (Free)" and
"Veeam Kasten (Enterprise - Term)" are supported in disconnected environments.
1. Create a filtered RedHat marketplace index image in the private registry.
Log into both the Red Hat registry and the private registry. The private
registry is the registry disconnected cluster has access to.
Prune the index image to include the Veeam Kasten operator(s).
The steps below are using the Veeam Kasten operators from
registry.redhat.io/redhat/redhat-marketplace-index:v4.9.
Push the pruned index image to the private registry.
1. Create a pull secret with RedHat and private registry credentials.
Follow the steps in Configuring credentials that allow images to be mirrored
to create an image registry credentials file that allows mirroring images to
the private registry.
1. Mirror the operator images to the private registry
This copies the operator images from RedHat to the local registry.
This also creates a manifest directory, which is used in the next two steps.
Example output:
1. Create an ImageContentSourcePolicy in the disconnected cluster.
Create an ImageContentSourcePolicy object using the
imageContentSourcePolicy.yaml file in the manifests directory created
in step 3.
1. Create a CatalogSource in the disconnected cluster.
Create a CatalogSource object using the catalogSource.yaml file in the
manifests directory created in step 3.
catalogSource.yaml can be updated to specify a catalog display name as the
example below.
Optionally, default catalog sources can be removed with the command below.
Verify the package manifest.
1. Install the operators via the operator hub.
Veeam Kasten operators can be now installed from the operator hub.
Follow the steps under operator install to
continue installing Veeam Kasten.
### Other Installation Optionsï
For a complete list of installation options, please visit our
advanced installation page.
After installing the "Veeam Kasten (Enterprise - PAYGO)" edition, if
the warning message "Unable to validate Red Hat Marketplace license" is
displayed on the Veeam Kasten dashboard, please verify the cluster is
registered with Red Hat Marketplace and the Red Hat Marketplace Operator
is installed, and then re-install Veeam Kasten.
### OpenShift on AWSï
When deploying OpenShift on AWS without using the EBS CSI driver
for persistent storage, make sure that you configure
these policies
before executing the installation command provided below:
### Securing Veeam Kasten with SecurityContextConstraintsï
Veeam Kasten installs customized SecurityContextConstraints (SCC)
to ensure that all workloads associated with Veeam Kasten
have just enough privileges to perform their respective tasks.
For additional information about SCCs, please refer to the official
OpenShift documentation
Starting with OpenShift 4.14, a new openshift.io/required-scc annotation was introduced.
Veeam Kasten applies this annotation to its own pods to ensure that the correct SecurityContextConstraints (SCC) have been applied.
Please note that pods created for Kanister Execution Hooks execution will not receive the openshift.io/required-scc annotation.
For more information, visit the Managing security context constraints.
### SecurityContextConstraints customizationï
The value of the Priority field in
SecurityContextConstraints (SCC) can be adjusted to align the
priority with the existing cluster configuration.
To set the desired Priority value in an Operator-managed
installation, modify the YAML of the Veeam Kasten Operand
configuration with the parameters below:
This customization can be achieved in a Helm-based installation
by adding the following parameter to the Helm command:
### SecurityContextConstraints Leakageï
OpenShift assigns SCC to workloads automatically.
By default, the most restrictive SCC matching a workload
security requirement will be selected and assigned to
that workload.
One of the criteria for SCC selection is the availability of the
SCC to a User or ServiceAccount.
SCC leakage means that some workloads might get an SCC
applied to them, which was not the intended one.
Veeam Kasten protects its SCC from leaking onto other workloads
by limiting access only to its dedicated ServiceAccount:
In this example, and in the rest of this page, Veeam Kasten is
installed into the namespace kasten-io (default), the
ServiceAccount name is the default one - k10-k10, and the
SCC name is also the default one - k10-scc.
If the cluster being considered has a different configuration,
those values need to be adapted to match the values used during
Veeam Kasten's installation in this cluster.
Despite the usage restrictions, it is still possible
to get Veeam Kasten's SCC assigned to other workloads.
This could happen when a workload is started by a cluster admin
or any other user with an allowed use action on all SCCs (*)
or on Veeam Kasten's specific SCC (k10-scc).
This is because users with the ClusterRole cluster-admin
bound to them have unlimited access to all available
SCCs, without any restrictions.
Veeam Kasten's SCC may be unexpectedly applied to workloads it
was not intended for under the following conditions:
- The workload is initiated by a user with cluster admin privileges
- The user initiating the workload has a role that grants access to all SCCs
### How to verify if access to a specific SecurityContextConstraints is grantedï
OpenShift's command line (CLI) client, oc, has a can-i command
that can be used with impersonation to check if a user can perform
a specific action on a specific resource.
Alternatively, the standard kubectl CLI client also has the same
command built-in and can be used to perform the same check.
Simply replace oc with kubectl in the command below.
To check if a user can use/access Veeam Kasten's SCC, the following
command can be used:
The output will contain yes if the specified user is able to use
Veeam Kasten's SCC or no if it is not.
For example, the output for the following check,
"Can Veeam Kasten's ServiceAccount use Veeam Kasten's SCC", should be yes:
Detailed information about can-i and impersonation
can be found in the official Kubernetes documentation.
### Accessing Dashboard via Routeï
As documented here, the Veeam Kasten
dashboard can also be accessed via an OpenShift Route.
### Authenticationï
### OpenShift OAuth serverï
As documented here, the OpenShift OAuth
server can be used to authenticate access to Veeam Kasten.
### Using an OAuth Proxyï
As documented here, the OpenShift OAuth
proxy can be used for authenticating access to Veeam Kasten.
### Validating the Installï
To validate that Veeam Kasten has been installed properly, the
following command can be run in Veeam Kasten's namespace (the
install default is kasten-io) to watch for the status of
all Veeam Kasten pods:
It may take a couple of minutes for all pods to come up but all pods
should ultimately display the status of Running.
In the unlikely scenario that pods that are stuck in any other state,
please follow the support documentation to debug
further.
### Validate Dashboard Accessï
By default, the Veeam Kasten dashboard will not be exposed externally.
To establish a connection to it, use the following kubectl command
to forward a local port to the Veeam Kasten ingress port:
The Veeam Kasten dashboard will be available at
http://127.0.0.1:8080/k10/##/.
For a complete list of options for accessing the Kasten Veeam Kasten
dashboard through a LoadBalancer, Ingress or OpenShift Route you can
use the instructions here.
### Using Veeam Kasten Console Pluginï
The Veeam Kasten operator includes the OpenShift Console Plugin, providing
faster and more convenient access to the essential data about the Veeam Kasten
application state.
### Enable Veeam Kasten Console Pluginï
The Veeam Kasten Console Plugin can be enabled during the installation of the
Veeam Kasten operator. For more details, see
Veeam Kasten Installation
To enable the plugin for existing K10 deployments, navigate to the
Operator Details page for Veeam Kasten operator in the OpenShift Console.
In the Console Plugin section on the right-hand side, select the
Enabled checkbox.
If Veeam Kasten was installed using
Helm based Installation, enabling the plugin from the
Console Details page will be the only available option. Navigate to the
Console Plugins tab of the Console Details page in the OpenShift
Console. Find the Veeam Kasten Plugin from OpenShift Console and select the
Enabled checkbox.
### Veeam Kasten Console Plugin UI Overviewï
The Veeam Kasten Console Plugin adds a new Veeam Kasten tab to the
OpenShift Web Console panel on the left. Click on the tab to open the plugin.
The plugin UI contains all the essential data from the
Veeam Kasten Dashboard, including the system overview and the
recent activity.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_aws_aws_efs_workaround.md
## Using the Veeam Kasten dashboard and AWS CLI for EFS Snapshot Migrationï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on AWS
- Using the Veeam Kasten dashboard and AWS CLI for EFS Snapshot Migration
Before starting, make sure the right security group has been created on
the AWS console with an NFS rule added to it. Follow steps 1 to 4 provided
here
to create a new security group.
On the source cluster, follow the instructions provided
for Exporting Applications.
On the target cluster follow the instructions provided below:
- Create an import policy. Do not select Restore After Import.
- Create the namespace (name must be identical as the source cluster) in which
the snapshot has to be restored. Once the namespace is created,
it will appear as an application on the Veeam Kasten Dashboard.
- For the restore, go to Applications â your_namespace â Restore
Select a restore point. From details, deselect Spec Artifacts and
deselect Volume Snapshots. Only the StorageClass has to be restored first
and therefore only that should be selected from the list of specs.
Click Restore.
- Once the restore job is successful, volumes can be restored.
To accomplish that, select the same restore point as before but this time,
Deselect Spec Artifacts and click Restore.
- Wait till the Volume artifacts are set during the process.
The job artifacts can be seen by clicking on the restore job.
Once the Volumes artifacts are set, the Volume ID
(i.e the file-system-id) will be visible in the description.
The EFS volume will have been created in the target cluster but is linked
to the VPC of the source cluster. As a result, this restored EFS volume will
not be accessible to any application running in the target cluster. In other
words, an attempt to restore the application will result in failure to bind
the pods to the restored PVC. Hence, to restore the application successfully
in the target cluster, the restored EFS volume should be made available from
the target VPC. This can be achieved by updating the VPC and mount targets of
the restored EFS volume using AWS CLI (or AWS Console).
Wait till the Volume artifacts are set during the process.
The job artifacts can be seen by clicking on the restore job.
Once the Volumes artifacts are set, the Volume ID
(i.e the file-system-id) will be visible in the description.
The EFS volume will have been created in the target cluster but is linked
to the VPC of the source cluster. As a result, this restored EFS volume will
not be accessible to any application running in the target cluster. In other
words, an attempt to restore the application will result in failure to bind
the pods to the restored PVC. Hence, to restore the application successfully
in the target cluster, the restored EFS volume should be made available from
the target VPC. This can be achieved by updating the VPC and mount targets of
the restored EFS volume using AWS CLI (or AWS Console).
Note
The volume restore job waits for the VPC and mount targets of the
restored EFS volume to be updated. If it's not done within 45 minutes, the job gets terminated.
- Delete the mount targets and create a new mount target in each Availability
Zone using the target security groups and subnet. Use the following AWS CLI
commands to update the mount target, so that the volume is mounted
from target VPC:
- When EFS volumes become mountable from the target VPC,
the volume restore job becomes successful.
- Once the volume restore job is successful, applications can be restored.
To restore, select Applications â your_namespace â Restore.
Select the restore point that was selected earlier. In the restore point
details,  deselect Volume Snapshots and click Restore.
- Once the pods are created, they should be successfully bound to their
respective PVCs.
Follow the steps outlined above to export the application from the source
cluster to the target cluster and then to run restore actions to restore
StorageClass and volume. Obtain the Volume ID (i.e., the file-system-id) from
the restore job description.
To update the mount targets using the AWS Console instead of the AWS CLI
follow the instructions below:
- Log in to the AWS Console
Use the file-system-id of the restored volume to select the correct
EFS on the AWS console. Click on  Actions â Manage Network Access.
- The console displays the list of Availability Zones and mount target
information. It will also display the VPC of source cluster. Click X
(left hand-side of AZ column) to remove all mount targets, then Save.
- Once they are deleted, click on Actions â Manage Network Access
to create new mount targets. Then, select the VPC of the target cluster.
Click on the + sign to the left of AZ to add new mount targets. Select
the security group (target cluster) that was created with type NFS, and click
Save.
From the Veeam Kasten dashboard, follow the steps outlined earlier to restore
applications.
© Copyright 2017-2024, Kasten, Inc.
### latest_install_aws_using_aws_iam_roles.md
## Using AWS IAM Roles with Veeam Kastenï
- Install Requirements
- Installing Veeam Kasten on Kubernetes
Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
Installing Veeam Kasten on Azure
Installing Veeam Kasten on Azure Marketplace
Installing Veeam Kasten on Red Hat OpenShift
Installing Veeam Kasten on Google Cloud
Installing Veeam Kasten on DigitalOcean
Installing Veeam Kasten on VMware vSphere
SUSE Rancher Apps & Marketplace Based Installation
Installing Veeam Kasten on K3S
Installing Veeam Kasten on Other Kubernetes Distributions
- Installing Veeam Kasten on AWS
Prerequisites
Installing Veeam Kasten
Validating the Install
- Prerequisites
- Installing Veeam Kasten
- Validating the Install
- Installing Veeam Kasten on AWS Marketplace for Containers Anywhere
- Installing Veeam Kasten on Azure
- Installing Veeam Kasten on Azure Marketplace
- Installing Veeam Kasten on Red Hat OpenShift
- Installing Veeam Kasten on Google Cloud
- Installing Veeam Kasten on DigitalOcean
- Installing Veeam Kasten on VMware vSphere
- SUSE Rancher Apps & Marketplace Based Installation
- Installing Veeam Kasten on K3S
- Installing Veeam Kasten on Other Kubernetes Distributions
- Storage Integration
- Generic Storage Backup and Restore
- Restricted Use of Generic Storage Backup
- Shareable Volume Backup and Restore
- Air-Gapped Install
- Installing Kasten in FIPS mode
- Installing Veeam Kasten with Iron Bank Images
- Installing Veeam Kasten with Google Workload Identity Federation
- Advanced Install Options
- Configuring Veeam Kasten Encryption
- Upgrading Veeam Kasten
- Production Deployment Checklist
-
- Installing Veeam Kasten on Kubernetes
- Installing Veeam Kasten on AWS
- Using AWS IAM Roles with Veeam Kasten
AWS IAM Roles
allow delegating access to AWS resources to a trusted entity (e.g., an
AWS user or a Kubernetes Service Account). Veeam Kasten can be
configured to access AWS infrastructure using an IAM Role.
To use a role with Veeam Kasten, an IAM Policy that describes the
permissions the role will grant needs to be created first. Second,
a role with this policy attached needs to be created. Finally, the
trusted entities (IAM User or Kubernetes Service Account) that can
assume that role need to be configured.
### Creating an IAM Policyï
An IAM Policy specifies permissions the role will grant.  The set of
permissions needed by Veeam Kasten for integrating against different AWS
services are described here.
The example below is a policy definition that grants permissions
required to snapshot and restore EBS volumes and migrate them across
Kubernetes clusters.
Note
To enable AWS KMS encryption additional policies are required. Refer to
Configuring Veeam Kasten encryption for more information.
### Veeam Kasten Installs with IAM Rolesï
### Option I: Using IAM Role With a Kubernetes Service Account (EKS)ï
### Enabling OIDC on your EKS Clusterï
Supporting IAM Roles with Kubernetes Service Accounts (SAs) requires
the IAM Roles for Service Accounts feature that is available for AWS
EKS clusters. Refer to Enabling IAM Roles for Service Accounts on
your Cluster
for complete instructions to enable this feature. If you have
eksctl available, you can run:
### Creating an IAM Role for Veeam Kasten Installï
To create an IAM Role that delegates permissions to a Kubernetes
Service Account, see the AWS documentation on Creating an IAM Role
and Policy for your Service Account.
Use kasten-io (or the namespace you installed Veeam Kasten in) for
the SERVICE_ACCOUNT_NAMESPACE and
k10-k10 for the SERVICE_ACCOUNT_NAME in the instructions.
Veeam Kasten can now be installed using the helm command below. No credentials
are required. EKS will inject the credentials into Veeam Kasten's pods.
my-service-account refers to the Kubernetes Service Account created
in the previous steps, as per the AWS documentation on Creating an IAM Role and Policy for your Service Account.
### Option II: Using an IAM Role With an IAM Userï
To create an IAM Role that delegates permissions to an IAM User, see
the AWS documentation on Creating a Role to Delegate Permissions to
an IAM User.
Once the IAM Role is created, the IAM User must also be
granted permissions to assume the role programmatically. For more
information about this step, see Granting a User Permissions to
Switch Roles.
Once the AWS IAM Role is created, configure Veeam Kasten with the
AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for the IAM User
along with the AWS ARN of the role.
© Copyright 2017-2024, Kasten, Inc.
