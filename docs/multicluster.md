# Multicluster Documentation

## Multicluster

The Veeam Kasten Multi-Cluster manager simplifies Veeam Kasten
  operations across multiple Kubernetes clusters.

Administrators define primary-secondary relationships between their
  Veeam Kasten instances. Primary Veeam Kasten instances provide a single
  entry point and dashboard for administrators to manage secondary
  instances.

Veeam Kasten resources, like Policies and Profiles, are defined in the
  primary instance and distributed to secondary instances. Secondary
  instances enact their policies and the secondaries' actions and metrics
  are summarized in the primary instance.

---

