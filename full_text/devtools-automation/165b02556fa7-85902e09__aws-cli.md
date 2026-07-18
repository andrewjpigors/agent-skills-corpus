---
name: aws-cli
description: >-
  AWS CLI v2 command reference for 190 AWS services. Covers CLI conventions
  (output formats, --query, pagination, waiters) and per-service references
  with complete flags, types, defaults, and JSON output schemas. Use for any
  AWS resource management via the CLI.
---

# AWS CLI v2 Reference

Complete AWS CLI v2 command reference covering 190 services. Each service includes an overview with common workflows, a quick-reference index, and per-command-group files with full parameter details and output schemas.

Start by reading the overview file for the service you need.

## Service Index

| Service | Reference | Scope |
|---------|-----------|-------|
| ACM | [`acm/overview.md`](references/acm/overview.md) | Certificates, import/export, validation, tags, account configuration |
| Amazon MQ | [`mq/overview.md`](references/mq/overview.md) | ActiveMQ and RabbitMQ brokers, configurations, users, engine types |
| Amplify | [`amplify/overview.md`](references/amplify/overview.md) | Apps, branches, domain associations, jobs, deployments, webhooks |
| API Gateway | [`apigateway/overview.md`](references/apigateway/overview.md) | REST APIs, HTTP APIs, resources, methods, stages, authorizers, API keys, usage plans |
| App Mesh | [`appmesh/overview.md`](references/appmesh/overview.md) | Meshes, virtual nodes, virtual services, virtual routers, routes, virtual gateways, gateway routes |
| App Runner | [`apprunner/overview.md`](references/apprunner/overview.md) | Services, connections, auto scaling, observability, VPC connectors, custom domains |
| AppConfig | [`appconfig/overview.md`](references/appconfig/overview.md) | Feature flags, configuration profiles, deployment strategies, environments, extensions, runtime data retrieval |
| Application Auto Scaling | [`application-autoscaling/overview.md`](references/application-autoscaling/overview.md) | Scalable targets, scaling policies, scheduled actions, predictive scaling |
| Application Discovery | [`discovery/overview.md`](references/discovery/overview.md) | Agents, configurations, applications, tags, export/import tasks |
| Application Insights | [`application-insights/overview.md`](references/application-insights/overview.md) | Applications, components, log patterns, problems, workloads |
| AppStream 2.0 | [`appstream/overview.md`](references/appstream/overview.md) | Fleets, stacks, images, image builders, app blocks, applications, entitlements, users |
| AppSync | [`appsync/overview.md`](references/appsync/overview.md) | GraphQL and Events APIs, data sources, resolvers, functions, types, API keys, caching, domain names, merged APIs |
| Artifact | [`artifact/overview.md`](references/artifact/overview.md) | Reports, agreements, account settings |
| Athena | [`athena/overview.md`](references/athena/overview.md) | Query execution, workgroups, named queries, data catalogs, notebooks, sessions, capacity |
| Audit Manager | [`auditmanager/overview.md`](references/auditmanager/overview.md) | Assessments, frameworks, controls, reports, evidence, delegations, insights |
| Auto Scaling | [`autoscaling/overview.md`](references/autoscaling/overview.md) | Auto Scaling groups, launch configurations, scaling policies, lifecycle hooks, instance refresh, warm pools |
| AWS Health | [`health/overview.md`](references/health/overview.md) | Events, affected entities, organization events |
| Backup | [`backup/overview.md`](references/backup/overview.md) | Backup plans, vaults, backup/copy/restore jobs, recovery points, frameworks, reports, restore testing, legal holds, Backup Gateway |
| Batch | [`batch/overview.md`](references/batch/overview.md) | Jobs, job definitions, job queues, compute environments, scheduling policies |
| Bedrock | [`bedrock/overview.md`](references/bedrock/overview.md) | Foundation models, custom models, fine-tuning, guardrails, inference profiles, agents, knowledge bases, prompts, flows, RAG, model invocation |
| Billing | [`billing/overview.md`](references/billing/overview.md) | Billing views, source views, resource policies |
| Budgets | [`budgets/overview.md`](references/budgets/overview.md) | Budgets, budget actions, notifications, subscribers |
| Chime SDK | [`chime/overview.md`](references/chime/overview.md) | App instances, meetings, attendees, messaging channels, voice connectors, phone numbers, SIP, proxy sessions, voice profiles |
| Clean Rooms | [`cleanrooms/overview.md`](references/cleanrooms/overview.md) | Collaborations, memberships, configured tables, protected queries, privacy budgets, ML models |
| Cloud Map | [`servicediscovery/overview.md`](references/servicediscovery/overview.md) | Namespaces, services, instances, service discovery, operations, health status |
| Cloud9 | [`cloud9/overview.md`](references/cloud9/overview.md) | Cloud IDE environments, memberships, environment status |
| CloudFormation | [`cloudformation/overview.md`](references/cloudformation/overview.md) | Stacks, change sets, stack sets, drift detection, resource scanning, type registry, generated templates |
| CloudFront | [`cloudfront/overview.md`](references/cloudfront/overview.md) | Distributions, origins, cache behaviors, invalidations, functions, origin access control |
| CloudHSM | [`cloudhsmv2/overview.md`](references/cloudhsmv2/overview.md) | Clusters, HSMs, backups, resource policies |
| CloudTrail | [`cloudtrail/overview.md`](references/cloudtrail/overview.md) | Trails, event selectors, event data stores, queries, channels, imports |
| CloudWatch | [`cloudwatch/overview.md`](references/cloudwatch/overview.md) | Metrics, alarms, dashboards, log groups, log streams, metric filters, Insights queries |
| CloudWatch Evidently | [`evidently/overview.md`](references/evidently/overview.md) | Feature flags, A/B testing, projects, features, experiments, launches, segments |
| CloudWatch Network Monitor | [`networkmonitor/overview.md`](references/networkmonitor/overview.md) | Network monitors, probes, network performance monitoring |
| CloudWatch RUM | [`rum/overview.md`](references/rum/overview.md) | Real user monitoring, app monitors, custom metrics, resource policies |
| CloudWatch Synthetics | [`synthetics/overview.md`](references/synthetics/overview.md) | Canaries, canary runs, groups, runtime versions |
| CodeArtifact | [`codeartifact/overview.md`](references/codeartifact/overview.md) | Domains, repositories, packages, package versions, package groups, authorization |
| CodeBuild | [`codebuild/overview.md`](references/codebuild/overview.md) | Projects, builds, build batches, report groups, source credentials, webhooks, fleets |
| CodeCommit | [`codecommit/overview.md`](references/codecommit/overview.md) | Repositories, branches, commits, files, pull requests, approval rules, merges, comments |
| CodeDeploy | [`codedeploy/overview.md`](references/codedeploy/overview.md) | Applications, deployment groups, deployments, deployment configs, revisions |
| CodeGuru | [`codeguru/overview.md`](references/codeguru/overview.md) | Code reviews, repository associations, recommendations, security scans, findings |
| CodePipeline | [`codepipeline/overview.md`](references/codepipeline/overview.md) | Pipelines, stages, actions, action types, webhooks |
| CodeStar Connections | [`codestar/overview.md`](references/codestar/overview.md) | Source provider connections, hosts, repository links, sync configs, notification rules |
| Cognito | [`cognito/overview.md`](references/cognito/overview.md) | User pools, user pool clients, users, groups, identity providers, identity pools, MFA |
| Comprehend | [`comprehend/overview.md`](references/comprehend/overview.md) | NLP text analysis, entity detection, sentiment, key phrases, language detection, document classification, entity recognizers, flywheels, endpoints |
| Comprehend Medical | [`comprehendmedical/overview.md`](references/comprehendmedical/overview.md) | Medical entity detection, PHI detection, ICD-10-CM/RxNorm/SNOMED CT code inference, batch processing |
| Compute Optimizer | [`compute-optimizer/overview.md`](references/compute-optimizer/overview.md) | Resource optimization recommendations for EC2, EBS, Lambda, ASG, ECS, RDS, idle resources |
| Config | [`configservice/overview.md`](references/configservice/overview.md) | Config rules, conformance packs, recorders, delivery channels, remediation, aggregators, resource evaluation |
| Connect | [`connect/overview.md`](references/connect/overview.md) | Contact center instances, contact flows, contacts, users, queues, routing profiles, evaluation forms, metrics, cases, participant connections |
| Control Tower | [`controltower/overview.md`](references/controltower/overview.md) | Landing zones, controls, baselines |
| Cost and Usage Report | [`cur/overview.md`](references/cur/overview.md) | Report definitions, S3 delivery |
| Cost Explorer | [`ce/overview.md`](references/ce/overview.md) | Cost and usage, forecasts, anomalies, savings plans, reservations, rightsizing |
| Data Exchange | [`dataexchange/overview.md`](references/dataexchange/overview.md) | Data sets, revisions, assets, jobs, data grants, event actions |
| Data Pipeline | [`datapipeline/overview.md`](references/datapipeline/overview.md) | Pipelines, definitions, objects, task management (legacy service) |
| DataSync | [`datasync/overview.md`](references/datasync/overview.md) | Agents, tasks, task executions, locations (S3, EFS, FSx, NFS, SMB, HDFS, Azure Blob) |
| Detective | [`detective/overview.md`](references/detective/overview.md) | Behavior graphs, members, investigations, data sources, organization |
| Device Farm | [`devicefarm/overview.md`](references/devicefarm/overview.md) | Projects, device pools, runs, uploads, remote access, test grid, offerings |
| Direct Connect | [`directconnect/overview.md`](references/directconnect/overview.md) | Connections, gateways, virtual interfaces, LAGs, BGP peering, MACsec, interconnects |
| Directory Service | [`ds/overview.md`](references/ds/overview.md) | Directories, hybrid AD, trusts, conditional forwarders, snapshots, networking, certificates |
| DMS | [`dms/overview.md`](references/dms/overview.md) | Replication instances, endpoints, replication tasks, serverless replication, data migrations, migration projects, Fleet Advisor |
| DocumentDB | [`docdb/overview.md`](references/docdb/overview.md) | Clusters, instances, snapshots, parameter groups, global clusters, Elastic Clusters |
| DynamoDB | [`dynamodb/overview.md`](references/dynamodb/overview.md) | Tables, items, indexes, queries, scans, streams, backups, global tables, TTL |
| EC2 | [`ec2/overview.md`](references/ec2/overview.md) | Instances, VPCs, subnets, security groups, key pairs, AMIs, launch templates, auto scaling |
| EC2 Image Builder | [`imagebuilder/overview.md`](references/imagebuilder/overview.md) | Image pipelines, recipes, components, images, infrastructure configs, lifecycle policies, workflows |
| ECR | [`ecr/overview.md`](references/ecr/overview.md) | Repositories, images, lifecycle policies, scanning, authentication, registry |
| ECS | [`ecs/overview.md`](references/ecs/overview.md) | Clusters, services, tasks, task definitions, container instances, capacity providers |
| EFS | [`efs/overview.md`](references/efs/overview.md) | File systems, mount targets, access points, replication, lifecycle |
| EKS | [`eks/overview.md`](references/eks/overview.md) | Clusters, node groups, Fargate profiles, add-ons, access management, Pod Identity, EKS Anywhere |
| Elastic Beanstalk | [`elasticbeanstalk/overview.md`](references/elasticbeanstalk/overview.md) | Applications, environments, versions, configuration templates, platforms, managed actions |
| Elastic Disaster Recovery | [`drs/overview.md`](references/drs/overview.md) | Source servers, recovery instances, replication, launch config, failback, source networks |
| Elastic Transcoder | [`elastictranscoder/overview.md`](references/elastictranscoder/overview.md) | Pipelines, presets, transcoding jobs (legacy service) |
| ElastiCache | [`elasticache/overview.md`](references/elasticache/overview.md) | Clusters, replication groups, parameter groups, snapshots, users, serverless |
| ELB Classic | [`elb/overview.md`](references/elb/overview.md) | Classic Load Balancers, listeners, health checks, stickiness policies, tags |
| ELBv2 | [`elbv2/overview.md`](references/elbv2/overview.md) | ALBs, NLBs, target groups, listeners, rules, health checks, SSL certificates |
| EMR | [`emr/overview.md`](references/emr/overview.md) | Clusters, instance fleets/groups, steps, scaling, studios, EMR on EKS, EMR Serverless |
| Entity Resolution | [`entityresolution/overview.md`](references/entityresolution/overview.md) | Entity matching workflows, ID mapping, ID namespaces, schema mappings, provider services |
| EventBridge | [`eventbridge/overview.md`](references/eventbridge/overview.md) | Event buses, rules, targets, archives, replays, connections, API destinations, pipes |
| EventBridge Pipes | [`pipes/overview.md`](references/pipes/overview.md) | Point-to-point event pipes, source-target connections, filtering, enrichment |
| EventBridge Scheduler | [`scheduler/overview.md`](references/scheduler/overview.md) | One-time and recurring schedules, schedule groups, universal target invocation |
| FinSpace | [`finspace/overview.md`](references/finspace/overview.md) | Kdb environments, databases, clusters, dataviews, changesets, scaling groups, volumes |
| Firehose | [`firehose/overview.md`](references/firehose/overview.md) | Delivery streams, data ingestion, destination management, encryption |
| Firewall Manager | [`fms/overview.md`](references/fms/overview.md) | Admin accounts, policies, apps/protocols lists, resource sets, third-party firewalls |
| FIS | [`fis/overview.md`](references/fis/overview.md) | Experiment templates, experiments, actions, target resources, safety levers |
| Forecast | [`forecast/overview.md`](references/forecast/overview.md) | Time-series forecasting, datasets, AutoPredictors, forecasts, what-if analysis, explainability, monitors, queries |
| FSx | [`fsx/overview.md`](references/fsx/overview.md) | File systems (Windows/Lustre/ONTAP/OpenZFS), backups, volumes, snapshots, storage virtual machines, data repository, file caches |
| GameLift | [`gamelift/overview.md`](references/gamelift/overview.md) | Fleets, builds, game sessions, matchmaking, server groups |
| Global Accelerator | [`globalaccelerator/overview.md`](references/globalaccelerator/overview.md) | Accelerators, listeners, endpoint groups, custom routing, cross-account attachments, BYOIP |
| Glue | [`glue/overview.md`](references/glue/overview.md) | ETL jobs, crawlers, databases, tables, connections, workflows, schema registry, data quality |
| Greengrass v2 | [`greengrassv2/overview.md`](references/greengrassv2/overview.md) | Core devices, components, deployments, client device associations, service role management |
| GuardDuty | [`guardduty/overview.md`](references/guardduty/overview.md) | Detectors, findings, filters, IP sets, threat intel sets, malware protection, members, organization |
| HealthLake | [`healthlake/overview.md`](references/healthlake/overview.md) | FHIR R4 data stores, FHIR import/export jobs, SSE encryption, SMART on FHIR authorization, waiters |
| IAM | [`iam/overview.md`](references/iam/overview.md) | Users, groups, roles, policies, instance profiles, access keys, MFA, identity providers |
| IAM Access Analyzer | [`accessanalyzer/overview.md`](references/accessanalyzer/overview.md) | Analyzers, findings, archive rules, access previews, policy tools |
| IAM Identity Center | [`identity-center/overview.md`](references/identity-center/overview.md) | Instances, permission sets, account assignments, applications, trusted token issuers, identity store |
| Inspector | [`inspector/overview.md`](references/inspector/overview.md) | Enablement, findings, filters, coverage, CIS scans, code security, SBOM export |
| Internet Monitor | [`internetmonitor/overview.md`](references/internetmonitor/overview.md) | Monitors, health events, internet events, performance/availability queries |
| IoT Core | [`iot/overview.md`](references/iot/overview.md) | Things, certificates, policies, rules, shadows, jobs, fleet indexing, security auditing, OTA updates, device defender, billing groups |
| IoT Device Advisor | [`iotdeviceadvisor/overview.md`](references/iotdeviceadvisor/overview.md) | Suite definitions, suite runs, test reports, endpoint management |
| IoT Events | [`iotevents/overview.md`](references/iotevents/overview.md) | Detector models, inputs, alarm models, runtime detector and alarm operations, logging |
| IoT FleetWise | [`iotfleetwise/overview.md`](references/iotfleetwise/overview.md) | Signal catalogs, model manifests, vehicles, campaigns, decoder manifests, fleets, state templates |
| IoT SiteWise | [`iotsitewise/overview.md`](references/iotsitewise/overview.md) | Asset models, assets, portals, dashboards, gateways, projects, time series data, bulk import, datasets |
| IoT TwinMaker | [`iottwinmaker/overview.md`](references/iottwinmaker/overview.md) | Workspaces, entities, component types, scenes, sync jobs, metadata transfer, property values, pricing |
| IoT Wireless | [`iotwireless/overview.md`](references/iotwireless/overview.md) | LoRaWAN/Sidewalk devices, wireless gateways, destinations, multicast groups, FUOTA tasks, network analyzer |
| IVS | [`ivs/overview.md`](references/ivs/overview.md) | Channels, streams, stream keys, stages, compositions, participants, chat rooms, recording, playback |
| Kendra | [`kendra/overview.md`](references/kendra/overview.md) | Intelligent search indexes, data sources, FAQs, thesauri, query suggestions, featured results, experiences, intelligent ranking |
| Keyspaces | [`keyspaces/overview.md`](references/keyspaces/overview.md) | Keyspaces, tables, user-defined types, auto scaling, point-in-time recovery |
| Kinesis | [`kinesis/overview.md`](references/kinesis/overview.md) | Data streams, shards, records, consumers, Kinesis Data Analytics applications |
| KMS | [`kms/overview.md`](references/kms/overview.md) | Encryption keys, key policies, grants, aliases, encrypt/decrypt, key rotation, multi-region |
| Lake Formation | [`lakeformation/overview.md`](references/lakeformation/overview.md) | Permissions, LF-tags, data cell filters, resource registration, transactions, credentials |
| Lambda | [`lambda/overview.md`](references/lambda/overview.md) | Functions, layers, event source mappings, aliases, versions, concurrency, URLs |
| Lex v2 | [`lex/overview.md`](references/lex/overview.md) | Conversational AI bots, intents, slots, locales, custom vocabulary, import/export, test sets, analytics, runtime sessions |
| License Manager | [`license-manager/overview.md`](references/license-manager/overview.md) | Licenses, grants, configurations, Linux subscriptions, user subscriptions |
| Lightsail | [`lightsail/overview.md`](references/lightsail/overview.md) | Instances, disks, load balancers, databases, containers, distributions, domains, buckets |
| Location Services | [`location/overview.md`](references/location/overview.md) | Maps, places, routes, geofences, trackers, API keys |
| Lookout for Equipment | [`lookoutequipment/overview.md`](references/lookoutequipment/overview.md) | Industrial equipment anomaly detection, datasets, models, inference schedulers, labels, retraining, sensor statistics |
| Lookout for Metrics | [`lookoutmetrics/overview.md`](references/lookoutmetrics/overview.md) | Metric anomaly detection, detectors, metric sets, alerts, anomaly groups |
| Lookout for Vision | [`lookoutvision/overview.md`](references/lookoutvision/overview.md) | Visual anomaly detection, projects, models, datasets, model packaging, anomaly detection |
| Macie | [`macie/overview.md`](references/macie/overview.md) | Classification jobs, findings, filters, allow lists, data identifiers, buckets, automated discovery |
| Managed Grafana | [`grafana/overview.md`](references/grafana/overview.md) | Workspaces, authentication, permissions, service accounts, API keys |
| Managed Prometheus | [`amp/overview.md`](references/amp/overview.md) | Workspaces, alert manager, rule groups, scrapers, logging, resource policies |
| Marketplace Catalog | [`marketplace-catalog/overview.md`](references/marketplace-catalog/overview.md) | Entities, change sets, resource policies |
| MediaConnect | [`mediaconnect/overview.md`](references/mediaconnect/overview.md) | Flows, sources, outputs, entitlements, media streams, VPC interfaces, bridges, gateways, routers |
| MediaConvert | [`mediaconvert/overview.md`](references/mediaconvert/overview.md) | Transcoding jobs, job templates, output presets, queues, policies, resource sharing |
| MediaLive | [`medialive/overview.md`](references/medialive/overview.md) | Channels, inputs, input security groups, multiplexes, clusters, networks, schedules, reservations, signal maps |
| MediaPackage | [`mediapackage/overview.md`](references/mediapackage/overview.md) | Channel groups, channels, origin endpoints, harvest jobs, VOD packaging groups, configurations, assets |
| MediaStore | [`mediastore/overview.md`](references/mediastore/overview.md) | Containers, container policies, CORS, lifecycle, metrics, object operations |
| Migration | [`migration/overview.md`](references/migration/overview.md) | MGN source servers, replication, launch config, cutover, waves, applications, connectors, actions, jobs, import/export, Migration Hub Config, Migration Hub Orchestrator workflows/steps/templates |
| MSK | [`msk/overview.md`](references/msk/overview.md) | Kafka clusters, configurations, topics, brokers, replicators, MSK Connect connectors |
| MWAA | [`mwaa/overview.md`](references/mwaa/overview.md) | Managed Apache Airflow environments, CLI tokens, web login, REST API |
| Neptune | [`neptune/overview.md`](references/neptune/overview.md) | DB clusters, instances, snapshots, global clusters, Neptune Analytics graphs, import/export |
| Network Firewall | [`network-firewall/overview.md`](references/network-firewall/overview.md) | Firewalls, firewall policies, rule groups, TLS inspection, logging, analysis |
| Network Manager | [`networkmanager/overview.md`](references/networkmanager/overview.md) | Global networks, core networks, sites, devices, links, connections, Transit Gateway, attachments, Connect peers, route analysis |
| OpenSearch | [`opensearch/overview.md`](references/opensearch/overview.md) | Domains, packages, VPC endpoints, indexes, data sources, Serverless collections/security |
| Organizations | [`organizations/overview.md`](references/organizations/overview.md) | Organization management, accounts, OUs, policies (SCPs, tag, backup, AI opt-out), handshakes, delegated admin |
| Outposts | [`outposts/overview.md`](references/outposts/overview.md) | Outpost management, sites, orders, capacity tasks, assets, catalog items |
| Payment Cryptography | [`payment-cryptography/overview.md`](references/payment-cryptography/overview.md) | Keys, encryption, PIN/MAC operations, card validation |
| Personalize | [`personalize/overview.md`](references/personalize/overview.md) | ML recommendations, dataset groups, schemas, solutions, campaigns, recommenders, batch jobs, event trackers, runtime recommendations |
| Pinpoint | [`pinpoint/overview.md`](references/pinpoint/overview.md) | Customer engagement campaigns, journeys, segments, messaging channels, templates, endpoints, SMS/voice v2 phone numbers, pools, registrations |
| Polly | [`polly/overview.md`](references/polly/overview.md) | Text-to-speech synthesis, speech marks, lexicons, voice descriptions |
| Pricing | [`pricing/overview.md`](references/pricing/overview.md) | Services, products, attribute values, price lists |
| Private CA | [`acm-pca/overview.md`](references/acm-pca/overview.md) | Certificate authorities, certificates, audit reports, permissions, policies |
| Proton | [`proton/overview.md`](references/proton/overview.md) | Environments, services, templates, components, repositories, sync configs |
| Q Connect | [`qconnect/overview.md`](references/qconnect/overview.md) | AI-powered contact center assistant, knowledge bases, AI agents, guardrails, prompts, sessions, messaging, quick responses, message templates |
| QLDB | [`qldb/overview.md`](references/qldb/overview.md) | Ledgers, journal exports, journal streams, blocks, revisions (end of support July 2025) |
| QuickSight | [`quicksight/overview.md`](references/quicksight/overview.md) | Dashboards, analyses, templates, data sets, data sources, users, groups, topics, embedding |
| RAM | [`ram/overview.md`](references/ram/overview.md) | Resource shares, invitations, permissions, organizations |
| RDS | [`rds/overview.md`](references/rds/overview.md) | DB instances, Aurora clusters, snapshots, parameter groups, subnet groups, replicas, proxies |
| Redshift | [`redshift/overview.md`](references/redshift/overview.md) | Provisioned clusters, snapshots, parameter groups, data sharing, Redshift Data API, Serverless namespaces/workgroups |
| Rekognition | [`rekognition/overview.md`](references/rekognition/overview.md) | Image/video analysis, face detection, collections, users, liveness, stream processors, media analysis, custom labels projects |
| Resilience Hub | [`resiliencehub/overview.md`](references/resiliencehub/overview.md) | Apps, resiliency policies, assessments, recommendations |
| Resource Explorer | [`resource-explorer-2/overview.md`](references/resource-explorer-2/overview.md) | Indexes, views, search, supported resource types |
| Resource Groups | [`resource-groups/overview.md`](references/resource-groups/overview.md) | Resource groups, queries, configurations, tag-based grouping, tag sync tasks |
| Resource Groups Tagging API | [`resourcegroupstaggingapi/overview.md`](references/resourcegroupstaggingapi/overview.md) | Cross-service tag management, resource discovery by tag, tag compliance reporting |
| Route 53 | [`route53/overview.md`](references/route53/overview.md) | Hosted zones, DNS records, health checks, routing policies, domain registration |
| Route 53 Recovery | [`route53-recovery/overview.md`](references/route53-recovery/overview.md) | Recovery clusters, control panels, routing controls, safety rules, readiness checks, recovery groups, cells |
| Route 53 Resolver | [`route53resolver/overview.md`](references/route53resolver/overview.md) | Resolver endpoints, forwarding rules, DNS Firewall, query logging, DNSSEC, Outpost Resolvers, Route 53 Profiles |
| S3 | [`s3/overview.md`](references/s3/overview.md) | Buckets, objects, storage classes, lifecycle, versioning, website hosting, presigned URLs |
| S3 Control | [`s3control/overview.md`](references/s3control/overview.md) | Access points, Object Lambda, Access Grants, Multi-Region Access Points, Batch Operations, Storage Lens, Outposts buckets |
| S3 Outposts | [`s3outposts/overview.md`](references/s3outposts/overview.md) | Endpoints, shared endpoints, Outposts with S3 capability |
| SageMaker | [`sagemaker/overview.md`](references/sagemaker/overview.md) | Training jobs, models, endpoints, processing, hyperparameter tuning, AutoML, pipelines, experiments, Feature Store, model registry, monitoring, notebooks, HyperPod clusters, Studio domains, MLflow, optimization, labeling, real-time/async inference |
| SageMaker A2I | [`sagemaker-a2i-runtime/overview.md`](references/sagemaker-a2i-runtime/overview.md) | Human-in-the-loop review, human loops, flow definitions |
| Savings Plans | [`savingsplans/overview.md`](references/savingsplans/overview.md) | Savings plans, rates, offerings |
| Secrets Manager | [`secretsmanager/overview.md`](references/secretsmanager/overview.md) | Secrets, versions, rotation, replication, resource policies, batch retrieval |
| Security Hub | [`securityhub/overview.md`](references/securityhub/overview.md) | Hub management, findings, insights, standards, security controls, automation rules, configuration policies |
| Security Lake | [`securitylake/overview.md`](references/securitylake/overview.md) | Data lake configuration, log sources, subscribers, organization |
| Service Catalog | [`servicecatalog/overview.md`](references/servicecatalog/overview.md) | Portfolios, products, provisioned products, constraints, service actions, tag options |
| Service Catalog AppRegistry | [`servicecatalog-appregistry/overview.md`](references/servicecatalog-appregistry/overview.md) | Applications, attribute groups, resource associations, configuration |
| Service Quotas | [`service-quotas/overview.md`](references/service-quotas/overview.md) | Quota lookups, increase requests, templates, auto-management, utilization reports |
| SES v2 | [`sesv2/overview.md`](references/sesv2/overview.md) | Email identities, configuration sets, contact lists, templates, sending, suppression |
| Shield | [`shield/overview.md`](references/shield/overview.md) | Subscription, protections, attacks, DRT access, proactive engagement, automatic response |
| Snow Family | [`snowball/overview.md`](references/snowball/overview.md) | Snowball/Snowball Edge/Snowcone jobs, clusters, addresses, long-term pricing, shipping |
| SNS | [`sns/overview.md`](references/sns/overview.md) | Topics, subscriptions, publishing, SMS, platform applications, message filtering |
| SQS | [`sqs/overview.md`](references/sqs/overview.md) | Standard and FIFO queues, messages, dead-letter queues, visibility timeout, long polling |
| Step Functions | [`stepfunctions/overview.md`](references/stepfunctions/overview.md) | State machines, executions, activities, map runs, versions |
| Storage Gateway | [`storagegateway/overview.md`](references/storagegateway/overview.md) | Gateways, file shares (NFS/SMB), iSCSI volumes, tape gateway, cache, bandwidth, file system associations |
| STS | [`sts/overview.md`](references/sts/overview.md) | Assume role, session tokens, federation, caller identity |
| SWF | [`swf/overview.md`](references/swf/overview.md) | Simple Workflow Service, domains, workflow types, activity types, executions, decision/activity tasks |
| Systems Manager | [`ssm/overview.md`](references/ssm/overview.md) | Parameter Store, documents, Run Command, Session Manager, patch baselines, state manager |
| Systems Manager Incidents | [`ssm-incidents/overview.md`](references/ssm-incidents/overview.md) | Response plans, incidents, timeline events, contacts, engagements, rotations |
| Textract | [`textract/overview.md`](references/textract/overview.md) | Document text detection, form/table analysis, expense analysis, ID analysis, lending analysis, custom adapters |
| Timestream | [`timestream/overview.md`](references/timestream/overview.md) | Databases, tables, write records, queries, scheduled queries |
| Transcribe | [`transcribe/overview.md`](references/transcribe/overview.md) | Speech-to-text transcription, call analytics, medical transcription, custom vocabularies, language models |
| Transfer Family | [`transfer/overview.md`](references/transfer/overview.md) | SFTP/FTPS/FTP/AS2 servers, users, access, connectors, agreements, workflows, host keys, certificates, web apps |
| Translate | [`translate/overview.md`](references/translate/overview.md) | Language translation, batch translation, custom terminologies, parallel data |
| Trusted Advisor | [`trustedadvisor/overview.md`](references/trustedadvisor/overview.md) | Recommendations, organization recommendations, support cases, Trusted Advisor checks |
| Verified Permissions | [`verifiedpermissions/overview.md`](references/verifiedpermissions/overview.md) | Policy stores, policies, policy templates, identity sources, authorization |
| WAF v2 | [`wafv2/overview.md`](references/wafv2/overview.md) | Web ACLs, rule groups, IP sets, regex pattern sets, logging |
| Well-Architected | [`wellarchitected/overview.md`](references/wellarchitected/overview.md) | Workloads, lenses, reviews, milestones, profiles |
| WorkMail | [`workmail/overview.md`](references/workmail/overview.md) | Organizations, users, groups, resources, mail domains, access control, impersonation, mobile devices, message flow |
| WorkSpaces | [`workspaces/overview.md`](references/workspaces/overview.md) | Virtual desktops, bundles, images, directories, pools, web portals, browser/network/user settings |
| X-Ray | [`xray/overview.md`](references/xray/overview.md) | Traces, service graphs, sampling rules, groups, insights, indexing, encryption |

**REQUIRED:** Read the overview file for the AWS service you are working with.

## General CLI Conventions

### Output Formats

```bash
--output json    # Default. Full JSON response.
--output text    # Tab-delimited. Good for scripting with awk/cut.
--output table   # Human-readable table.
--output yaml    # YAML format.
```

### Filtering with --query (JMESPath)

```bash
# Single field
aws ecs describe-clusters --query 'clusters[0].clusterArn'

# Multiple fields
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]'

# Filter by value
aws ecs list-services --query 'serviceArns[?contains(@,`my-service`)]'

# Flatten nested arrays
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId'
```

### Pagination

```bash
--no-paginate          # Disable automatic pagination (get first page only)
--max-items N          # Limit total items returned
--page-size N          # Items per API call (controls request size, not total)
--starting-token TOK   # Resume from previous NextToken
```

Most `list-*` and `describe-*` commands paginate automatically in CLI v2.

### Waiters

Wait for a resource to reach a specific state. Format: `aws <service> wait <waiter-name>`.

```bash
aws ecs wait services-stable --cluster my-cluster --services my-service
aws ecs wait tasks-running --cluster my-cluster --tasks arn:aws:ecs:...
aws ecs wait tasks-stopped --cluster my-cluster --tasks arn:aws:ecs:...
aws ec2 wait instance-running --instance-ids i-1234567890abcdef0
aws ec2 wait instance-terminated --instance-ids i-1234567890abcdef0
aws ec2 wait vpc-available --vpc-ids vpc-123
aws ec2 wait subnet-available --subnet-ids subnet-123
aws ec2 wait nat-gateway-available --nat-gateway-ids nat-123
```

Waiters poll at intervals and timeout after a set number of attempts. Use `--cli-read-timeout` and `--cli-connect-timeout` to adjust.

### Common Global Options

```bash
--region REGION        # Override default region
--profile PROFILE      # Use named profile from ~/.aws/config
--no-cli-pager         # Disable pager (useful in scripts)
--cli-input-json       # Read input from JSON file: --cli-input-json file://input.json
--cli-input-yaml       # Read input from YAML file
--generate-cli-skeleton # Output input skeleton (for building --cli-input-json files)
--debug                # Full debug logging
--dry-run              # Supported by some EC2 commands — validates without executing
```

### JSON Input Files

For commands with complex input, use `--cli-input-json`:

```bash
# Generate skeleton
aws ecs register-task-definition --generate-cli-skeleton output > task-def.json

# Edit the skeleton, then use it
aws ecs register-task-definition --cli-input-json file://task-def.json
```

### Error Handling in Scripts

```bash
# Check exit code
if aws ecs describe-clusters --clusters my-cluster --query 'clusters[0].status' --output text | grep -q ACTIVE; then
  echo "Cluster is active"
fi

# Capture errors
result=$(aws ecs create-service --cli-input-json file://service.json 2>&1) || {
  echo "Failed: $result"
  exit 1
}
```

### ARN Format

```
arn:aws:<service>:<region>:<account-id>:<resource-type>/<resource-name>
```

Examples:
- `arn:aws:ecs:us-east-1:123456789012:cluster/my-cluster`
- `arn:aws:ecs:us-east-1:123456789012:service/my-cluster/my-service`
- `arn:aws:ecs:us-east-1:123456789012:task-definition/my-task:1`
- `arn:aws:ecr:us-east-1:123456789012:repository/my-repo`

### Environment Variables

```bash
AWS_DEFAULT_REGION       # Default region
AWS_ACCESS_KEY_ID        # Access key
AWS_SECRET_ACCESS_KEY    # Secret key
AWS_SESSION_TOKEN        # Session token (temporary credentials)
AWS_PROFILE              # Named profile
AWS_DEFAULT_OUTPUT       # Default output format
```
