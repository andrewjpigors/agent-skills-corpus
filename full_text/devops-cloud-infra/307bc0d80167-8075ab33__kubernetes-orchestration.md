---
name: kubernetes-orchestration
description: Use when deploying applications to Kubernetes, implementing deployment strategies, pod security, resource management, horizontal pod autoscaling, service mesh, ingress controllers, secrets management, and production-ready cluster configurations. Includes Helm charts, Kustomize, GitOps, and CKA/CKAD/CKS best practices.
license: MIT
---

# Kubernetes Orchestration Skill — Production-Ready Cluster Management

## Overview

This skill provides comprehensive guidance for **deploying and managing applications on Kubernetes**, including deployment strategies, pod security policies, resource management, autoscaling, service mesh integration, ingress configuration, secrets management, and production best practices. Based on official Kubernetes documentation and CKA/CKAD/CKS certification standards.

## When to Use

**Use this skill when:**

- Deploying applications to Kubernetes clusters
- Implementing deployment strategies (rolling, blue-green, canary)
- Configuring pod security policies and Pod Security Admission
- Setting up resource requests, limits, and quotas
- Implementing Horizontal Pod Autoscaling (HPA) or Vertical Pod Autoscaling (VPA)
- Configuring ingress controllers (NGINX, Traefik, AWS ALB)
- Setting up service mesh (Istio, Linkerd)
- Managing secrets and config maps securely
- Deploying stateful sets for databases and stateful applications
- Configuring daemon sets for logging and monitoring agents
- Setting up jobs and cron jobs for batch processing
- Implementing monitoring with Prometheus and Grafana
- Setting up logging with EFK/ELK stack
- Configuring network policies for pod isolation
- Implementing RBAC and service accounts
- Setting up persistent volumes and storage classes
- Using Helm charts for application packaging
- Implementing GitOps with ArgoCD or Flux
- Configuring node affinity, anti-affinity, taints and tolerations
- Setting up pod disruption budgets for high availability
- Implementing multi-cluster management strategies
- Configuring namespace isolation and resource quotas
- Securing clusters with OPA/Gatekeeper or Falco
- Scanning images with Trivy before deployment

**Do NOT use this skill when:**

- Containerizing applications (use docker-containerization skill)
- Setting up cloud infrastructure (use terraform-iac skill)
- Configuring CI/CD pipelines (use devops-pipeline skill)
- Building serverless functions (use aws-serverless or cloudflare-workers skill)
- Managing database schema (use database-design skill)
- Implementing application code (use backend-developer or frontend-developer skill)
- Setting up standalone monitoring without Kubernetes (use monitoring skill)
- Deploying to PaaS platforms without Kubernetes (use vercel-deployment or cloudflare-pages skill)

**Why avoid:** Kubernetes is for container orchestration, not containerization, infrastructure provisioning, or application development. Use the right tool for each layer of the stack.

## Core Concepts

### Workload Types

| Type                      | Use Case                   | State      | Scaling    |
| ------------------------- | -------------------------- | ---------- | ---------- |
| **Deployment**            | Stateless applications     | Stateless  | Horizontal |
| **StatefulSet**           | Databases, message queues  | Stateful   | Ordered    |
| **DaemonSet**             | Logging, monitoring agents | Node-bound | 1 per node |
| **Job**                   | One-time batch processing  | Ephemeral  | Fixed      |
| **CronJob**               | Scheduled batch processing | Ephemeral  | Scheduled  |
| **ReplicationController** | Legacy pod replication     | Stateless  | Horizontal |

### Deployment Strategies

| Strategy           | Downtime | Risk   | Rollback  | Use Case                        |
| ------------------ | -------- | ------ | --------- | ------------------------------- |
| **Rolling Update** | Zero     | Low    | Automatic | Most applications               |
| **Blue-Green**     | Zero     | Medium | Instant   | High-traffic apps               |
| **Canary**         | Zero     | Low    | Gradual   | Risky deployments               |
| **Recreate**       | Full     | High   | Manual    | Database migrations             |
| **Shadow**         | Zero     | Lowest | N/A       | Testing with production traffic |

### Resource Management Hierarchy

```
Cluster
├── Namespaces (logical isolation)
│   ├── ResourceQuotas (namespace limits)
│   └── LimitRanges (default pod limits)
│   └── Pods
│       ├── Containers
│       │   ├── Requests (guaranteed resources)
│       │   └── Limits (maximum resources)
```

## Deployment Strategy Examples

### Rolling Update (Default)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1 # Max pods unavailable during update
      maxSurge: 1 # Max extra pods during update
  template:
    metadata:
      labels:
        app: web-app
        version: v1
    spec:
      containers:
        - name: web-app
          image: myregistry/web-app:v1.2.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: '100m'
              memory: '128Mi'
            limits:
              cpu: '500m'
              memory: '512Mi'
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Blue-Green Deployment

```yaml
# Blue (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-blue
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: web-app
        track: blue
    spec:
      containers:
        - name: web-app
          image: myregistry/web-app:v1.1.0
---
# Green (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-green
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: web-app
        track: green
    spec:
      containers:
        - name: web-app
          image: myregistry/web-app:v1.2.0
---
# Service switches between blue and green
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  selector:
    app: web-app
    track: green # Change to 'blue' to rollback
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

### Canary Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-stable
spec:
  replicas: 9 # 90% traffic
  template:
    metadata:
      labels:
        app: web-app
        version: stable
    spec:
      containers:
        - name: web-app
          image: myregistry/web-app:v1.1.0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-canary
spec:
  replicas: 1 # 10% traffic
  template:
    metadata:
      labels:
        app: web-app
        version: canary
    spec:
      containers:
        - name: web-app
          image: myregistry/web-app:v1.2.0
---
# Service distributes traffic based on replica count
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  selector:
    app: web-app
  ports:
    - port: 80
      targetPort: 8080
```

## Pod Security and RBAC

### Pod Security Admission (Replaces PSP)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # Pod Security Standards: restricted (most secure)
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### RBAC Configuration

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: production
automountServiceAccountToken: false # Disable by default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'watch', 'list']
  - apiGroups: ['apps']
    resources: ['deployments']
    verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
  - kind: ServiceAccount
    name: app-service-account
    namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Security Context

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: app
          image: myregistry/app:latest
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

## Resource Management and Autoscaling

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: requests-per-second
        target:
          type: AverageValue
          averageValue: '1000'
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 60
        - type: Pods
          value: 4
          periodSeconds: 60
      selectPolicy: Max
```

### Resource Quotas and Limit Ranges

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: '10'
    requests.memory: 20Gi
    limits.cpu: '20'
    limits.memory: 40Gi
    pods: '50'
    services: '20'
    persistentvolumeclaims: '10'
---
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - default:
        cpu: '500m'
        memory: '512Mi'
      defaultRequest:
        cpu: '100m'
        memory: '128Mi'
      max:
        cpu: '2'
        memory: '4Gi'
      min:
        cpu: '50m'
        memory: '64Mi'
      type: Container
```

## Ingress Configuration

### NGINX Ingress Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/rate-limit: '100'
    nginx.ingress.kubernetes.io/rate-limit-window: '1m'
    nginx.ingress.kubernetes.io/proxy-body-size: '50m'
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls-secret
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-app-service
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080
```

### Ingress with Canary (NGINX)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-canary-ingress
  annotations:
    nginx.ingress.kubernetes.io/canary: 'true'
    nginx.ingress.kubernetes.io/canary-weight: '10' # 10% traffic
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-app-canary
                port:
                  number: 80
```

## Service Mesh (Istio)

### VirtualService and DestinationRule

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: web-app-vs
spec:
  hosts:
    - web-app
  http:
    - route:
        - destination:
            host: web-app
            subset: v1
          weight: 90
        - destination:
            host: web-app
            subset: v2
          weight: 10
      timeout: 5s
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: gateway-error,connect-failure,refused-stream
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: web-app-dr
spec:
  host: web-app
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

## Secrets and Config Maps

### Secrets Management

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
stringData:
  database-url: 'postgresql://user:password@db:5432/app'
  api-key: 'sk-xxxxxxxxxxxxxxxx'
  jwt-secret: 'super-secret-jwt-key'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
        - name: app
          image: myregistry/app:latest
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: api-key
          # Mount secrets as files (more secure than env vars)
          volumeMounts:
            - name: secret-volume
              mountPath: /etc/secrets
              readOnly: true
      volumes:
        - name: secret-volume
          secret:
            secretName: app-secrets
```

### Config Maps

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  APP_ENV: 'production'
  LOG_LEVEL: 'info'
  CACHE_TTL: '3600'
  # Configuration file
  app.conf: |
    [server]
    port = 8080
    workers = 4

    [database]
    pool_size = 10
    timeout = 30
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
        - name: app
          image: myregistry/app:latest
          envFrom:
            - configMapRef:
                name: app-config
          volumeMounts:
            - name: config-volume
              mountPath: /etc/app
      volumes:
        - name: config-volume
          configMap:
            name: app-config
            items:
              - key: app.conf
                path: app.conf
```

## Stateful Sets for Databases

### PostgreSQL StatefulSet

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
  namespace: production
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
    - port: 5432
      name: postgres
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: production
spec:
  serviceName: postgres-headless
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 999
        fsGroup: 999
      containers:
        - name: postgres
          image: postgres:16-alpine
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_DB
              value: 'app'
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          resources:
            requests:
              cpu: '500m'
              memory: '1Gi'
            limits:
              cpu: '2'
              memory: '4Gi'
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: postgres-data
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 50Gi
```

## Daemon Sets for Monitoring

### Fluentd DaemonSet

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
  labels:
    app: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      tolerations:
        - operator: Exists # Run on all nodes including master
      serviceAccountName: fluentd
      containers:
        - name: fluentd
          image: fluent/fluentd:v1.16-1
          resources:
            limits:
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 200Mi
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
            - name: fluentd-config
              mountPath: /fluentd/etc
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
        - name: fluentd-config
          configMap:
            name: fluentd-config
```

## Jobs and CronJobs

### Batch Processing Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration
  namespace: production
spec:
  template:
    metadata:
      labels:
        job: data-migration
    spec:
      restartPolicy: Never
      containers:
        - name: migrator
          image: myregistry/migrator:latest
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: connection-string
          resources:
            requests:
              cpu: '500m'
              memory: '1Gi'
            limits:
              cpu: '2'
              memory: '4Gi'
  backoffLimit: 4
  activeDeadlineSeconds: 3600
  completionMode: NonIndexed
  completions: 1
---
# CronJob for scheduled tasks
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-report
  namespace: production
spec:
  schedule: '0 2 * * *' # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: reporter
              image: myregistry/reporter:latest
              resources:
                requests:
                  cpu: '200m'
                  memory: '256Mi'
                limits:
                  cpu: '1'
                  memory: '1Gi'
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  concurrencyPolicy: Forbid
```

## Network Policies

### Pod Isolation

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-web-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: web
      ports:
        - protocol: TCP
          port: 8080
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-to-db
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53 # DNS
```

## Node Affinity and Scheduling

### Advanced Scheduling

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpu-workload
spec:
  template:
    spec:
      # Node Affinity: Schedule only on specific nodes
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node-type
                    operator: In
                    values:
                      - gpu
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 1
              preference:
                matchExpressions:
                  - key: zone
                    operator: In
                    values:
                      - us-east-1a
        # Pod Anti-Affinity: Spread pods across nodes
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - web-app
              topologyKey: kubernetes.io/hostname
      # Tolerations: Allow scheduling on tainted nodes
      tolerations:
        - key: 'workload-type'
          operator: 'Equal'
          value: 'compute-intensive'
          effect: 'NoSchedule'
        - key: 'dedicated'
          operator: 'Equal'
          value: 'ml-workloads'
          effect: 'NoExecute'
      # Pod Priority
      priorityClassName: high-priority
      containers:
        - name: ml-model
          image: myregistry/ml-model:latest
          resources:
            requests:
              cpu: '4'
              memory: '16Gi'
              nvidia.com/gpu: 1
            limits:
              cpu: '4'
              memory: '16Gi'
              nvidia.com/gpu: 1
```

### Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-app-pdb
  namespace: production
spec:
  minAvailable: 2 # At least 2 pods always available
  # OR use maxUnavailable: 1
  selector:
    matchLabels:
      app: web-app
```

## Persistent Volumes and Storage

### Storage Class and PVC

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com # AWS EBS CSI driver
parameters:
  type: io2
  iopsPerGB: '5000'
  fsType: ext4
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
  namespace: production
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
  volumeMode: Filesystem
---
# Using PVC in Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
        - name: app
          image: myregistry/app:latest
          volumeMounts:
            - name: data
              mountPath: /app/data
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: app-data
```

## Helm Chart Structure

```
my-chart/
├── Chart.yaml
├── values.yaml
├── values-production.yaml
├── values-staging.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── configmap.yaml
    ├── secrets.yaml
    ├── networkpolicy.yaml
    ├── pdb.yaml
    ├── serviceaccount.yaml
    ├── role.yaml
    ├── rolebinding.yaml
    └── _helpers.tpl
```

### Chart.yaml

```yaml
apiVersion: v2
name: web-app
description: Production-ready web application chart
type: application
version: 1.2.0
appVersion: '2.0.0'
maintainers:
  - name: platform-team
    email: platform@example.com
keywords:
  - web
  - microservice
  - production
```

### values.yaml

```yaml
replicaCount: 3

image:
  repository: myregistry/web-app
  pullPolicy: IfNotPresent
  tag: '2.0.0'

imagePullSecrets: []
nameOverride: ''
fullnameOverride: ''

serviceAccount:
  create: true
  annotations: {}
  name: ''

podAnnotations: {}

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls-secret
      hosts:
        - app.example.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

podDisruptionBudget:
  enabled: true
  minAvailable: 2
```

## GitOps with ArgoCD

### Application Manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/my-app.git
    targetRevision: main
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m0s
  revisionHistoryLimit: 10
```

### Kustomize Overlay

```yaml
# k8s/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namespace: production

namePrefix: prod-

replicas:
  - name: web-app
    count: 5

configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=info
      - METRICS_ENABLED=true

patches:
  - target:
      kind: Deployment
      name: web-app
    patch: |-
      - op: add
        path: /spec/template/spec/affinity
        value:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web-app
              topologyKey: kubernetes.io/hostname
```

## Monitoring and Logging

### Prometheus ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: web-app-monitor
  namespace: monitoring
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: web-app
  namespaceSelector:
    matchNames:
      - production
  endpoints:
    - port: metrics
      interval: 15s
      path: /metrics
      scrapeTimeout: 10s
```

## Security Best Practices

### Security Checklist

```yaml
# ✅ GOOD: Complete security configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      serviceAccountName: app-sa
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: app
          image: myregistry/app:v1.2.0 # Specific tag, not latest
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          resources:
            requests:
              cpu: '100m'
              memory: '128Mi'
            limits:
              cpu: '500m'
              memory: '512Mi'
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Security Anti-Patterns

```yaml
# ❌ BAD: Running as root (no securityContext)
# ❌ BAD: Using 'latest' tag
image: myregistry/app:latest
# ❌ BAD: No resource limits
# ❌ BAD: Privileged container
securityContext:
  privileged: true
# ❌ BAD: No health checks
# ❌ BAD: Automount service account token unnecessarily
automountServiceAccountToken: true
# ❌ BAD: No network policies (open cluster)
# ❌ BAD: Secrets in ConfigMaps instead of Secrets
```

## Production Checklist

Before deploying to production:

- [ ] Resource requests and limits set on all containers
- [ ] Liveness and readiness probes configured
- [ ] Pod Security Admission enabled (restricted profile)
- [ ] RBAC with least privilege principles
- [ ] Network policies for pod isolation
- [ ] Horizontal Pod Autoscaler configured
- [ ] Pod Disruption Budgets for high availability
- [ ] Secrets stored in Kubernetes Secrets (or external vault)
- [ ] ConfigMaps for non-sensitive configuration
- [ ] Persistent volumes with appropriate storage classes
- [ ] Ingress with TLS termination
- [ ] Monitoring with Prometheus ServiceMonitors
- [ ] Logging with Fluentd/FluentBit DaemonSet
- [ ] Image vulnerability scanning (Trivy)
- [ ] Helm charts or Kustomize for deployment
- [ ] GitOps workflow (ArgoCD/Flux)
- [ ] Namespace isolation for multi-tenant clusters
- [ ] Resource quotas and limit ranges
- [ ] Node affinity and anti-affinity rules
- [ ] Pod priority and preemption configured
- [ ] Backup strategy for persistent data
- [ ] Disaster recovery plan tested

## Real-World Impact

**Before this skill:**

- Manual deployments with downtime
- No resource management leading to node exhaustion
- Running containers as root with full privileges
- No autoscaling causing over/under-provisioning
- Missing health checks causing traffic to unhealthy pods
- No network policies leaving cluster wide open
- Secrets hardcoded in manifests or environment variables
- No monitoring or logging infrastructure

**After this skill:**

- Zero-downtime deployments with rolling updates
- Proper resource management with HPA/VPA
- Non-root containers with minimal privileges
- Automated scaling based on metrics
- Health checks ensuring only healthy pods receive traffic
- Network policies enforcing least-privilege networking
- Secrets managed through Kubernetes Secrets or external vaults
- Comprehensive monitoring and logging with Prometheus/EFK

## Cross-References

- **`docker-containerization`** - For building container images before deployment
- **`devops-pipeline`** - For CI/CD integration with Kubernetes deployments
- **`terraform-iac`** - For provisioning Kubernetes clusters (EKS, GKE, AKS)
- **`aws-serverless`** - For AWS EKS-specific configurations
- **`monitoring`** - For Prometheus/Grafana dashboard setup
- **`security-auditor`** - For cluster security audits and compliance
- **`disaster-recovery`** - For backup and recovery strategies

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- [CKA Study Guide](https://github.com/cncf/curriculum)
- [CKAD Study Guide](https://github.com/cncf/curriculum)
- [CKS Study Guide](https://github.com/cncf/curriculum)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/overview/)
- [Helm Documentation](https://helm.sh/docs/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Istio Documentation](https://istio.io/latest/docs/)
- [Prometheus Kubernetes Monitoring](https://prometheus.io/docs/guides/kube-prometheus-stack/)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
