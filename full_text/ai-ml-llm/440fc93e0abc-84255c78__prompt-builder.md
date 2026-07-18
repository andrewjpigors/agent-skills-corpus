---
name: prompt-builder
description: Salesforce Prompt Builder reference — template types, metadata XML generation, Apex/LWC/Flow/REST API integration, merge fields, grounding, and deployment
scope: AGENTFORCE_PROMPT_BUILDER
---

# <span data-proof="authored" data-by="ai:claude">Salesforce Prompt Builder Reference</span>

**<span data-proof="authored" data-by="ai:claude">SCOPE: AGENTFORCE_PROMPT_BUILDER</span>** <span data-proof="authored" data-by="ai:claude">- This skill applies to building and integrating Prompt Builder templates.
**Use when:**</span> <span data-proof="authored" data-by="ai:claude">Creating prompt template metadata XML, writing Apex invocation/grounding classes, building LWC integrations, or deploying templates between orgs.</span>

***

<span data-proof="authored" data-by="ai:claude">Prompt Builder creates reusable prompt templates that merge CRM data with LLM calls. Templates are deployable metadata (`GenAiPromptTemplate`) that can be authored as XML, version-controlled, and deployed via</span> <span data-proof="authored" data-by="ai:claude">`sf`</span> <span data-proof="authored" data-by="ai:claude">CLI.</span>

***

## <span data-proof="authored" data-by="ai:claude">Template Types</span>

| <span data-proof="authored" data-by="ai:claude">Type</span>                 | <span data-proof="authored" data-by="ai:claude">API Value</span>                       | <span data-proof="authored" data-by="ai:claude">Inputs</span>                         | <span data-proof="authored" data-by="ai:claude">Surfaces At</span>                                                  |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **<span data-proof="authored" data-by="ai:claude">Field Generation</span>** | <span data-proof="authored" data-by="ai:claude">`einstein_gpt__fieldCompletion`</span> | <span data-proof="authored" data-by="ai:claude">Single object</span>                  | <span data-proof="authored" data-by="ai:claude">Record page edit sparkle icon, Flow, Apex, REST API, Copilot</span> |
| **<span data-proof="authored" data-by="ai:claude">Sales Email</span>**      | <span data-proof="authored" data-by="ai:claude">`einstein_gpt__salesEmail`</span>      | <span data-proof="authored" data-by="ai:claude">Contact/Lead + optional object</span> | <span data-proof="authored" data-by="ai:claude">Email Composer, Flow, Apex, REST API, Copilot</span>                |
| **<span data-proof="authored" data-by="ai:claude">Flex</span>**             | <span data-proof="authored" data-by="ai:claude">`FlexTemplate`</span>                  | <span data-proof="authored" data-by="ai:claude">Up to 5 objects</span>                | <span data-proof="authored" data-by="ai:claude">Flow, Apex, REST API, Copilot</span>                                |
| **<span data-proof="authored" data-by="ai:claude">Record Summary</span>**   | <span data-proof="authored" data-by="ai:claude">`einstein_gpt__recordSummary`</span>   | <span data-proof="authored" data-by="ai:claude">Single object</span>                  | <span data-proof="authored" data-by="ai:claude">Copilot only</span>                                                 |

**<span data-proof="authored" data-by="ai:claude">Choosing a type:</span>**

* **<span data-proof="authored" data-by="ai:claude">Field Generation</span>** <span data-proof="authored" data-by="ai:claude">— auto-fill a specific field (e.g., description, summary) on a record</span>

* **<span data-proof="authored" data-by="ai:claude">Sales Email</span>** <span data-proof="authored" data-by="ai:claude">— draft personalized outbound emails from Contact/Lead data</span>

* **<span data-proof="authored" data-by="ai:claude">Flex</span>** <span data-proof="authored" data-by="ai:claude">— general-purpose, multi-object reasoning; most powerful and flexible</span>

* **<span data-proof="authored" data-by="ai:claude">Record Summary</span>** <span data-proof="authored" data-by="ai:claude">— Copilot-only summaries; cannot be invoked from Flow/Apex/API</span>

***

## <span data-proof="authored" data-by="ai:claude">Metadata XML Structure</span>

### <span data-proof="authored" data-by="ai:claude">GenAiPromptTemplate</span>

<span data-proof="authored" data-by="ai:claude">File location:</span> <span data-proof="authored" data-by="ai:claude">`force-app/main/default/genAiPromptTemplates/<TemplateName>.genAiPromptTemplate-meta.xml`</span>

### <span data-proof="authored" data-by="ai:claude">Complete XML Schema</span>

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTYzMSwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
<?xml version="1.0" encoding="UTF-8"?>
<GenAiPromptTemplate xmlns="http://soap.sforce.com/2006/04/metadata">
    <activeVersion>{hash}_1</activeVersion>
    <createdInVersion>63.0</createdInVersion>
    <developerName>Template_Api_Name</developerName>
    <masterLabel>Template Display Label</masterLabel>
    <relatedEntity>ObjectApiName</relatedEntity>
    <templateVersions>
        <content>Your prompt instructions go here.
Use merge fields like {!$Input:Case.Subject} for dynamic data.
Use {!$Flow:FlowName.OutputVariable} for Flow-grounded data.
Use {!$RelatedList:Case.CaseComments.Records} for related records.</content>
        <inputs>
            <apiName>inputApiName</apiName>
            <definition>SOBJECT://ObjectApiName</definition>
            <referenceName>Input:ObjectApiName</referenceName>
            <required>true</required>
        </inputs>
        <primaryModel>sfdc_ai__DefaultGPT4Omni</primaryModel>
        <status>Published</status>
        <templateDataProviders>
            <definition>flow://FlowApiName</definition>
            <parameters>
                <definition>SOBJECT://ObjectApiName</definition>
                <isRequired>true</isRequired>
                <parameterName>inputApiName</parameterName>
                <valueExpression>{!$Input:ObjectApiName}</valueExpression>
            </parameters>
            <referenceName>Flow:FlowApiName</referenceName>
        </templateDataProviders>
        <versionIdentifier>{hash}_1</versionIdentifier>
    </templateVersions>
    <type>einstein_gpt__fieldCompletion</type>
    <visibility>Global</visibility>
</GenAiPromptTemplate>
```

### <span data-proof="authored" data-by="ai:claude">Metadata Field Reference</span>

| <span data-proof="authored" data-by="ai:claude">Element</span>                                  | <span data-proof="authored" data-by="ai:claude">Required</span> | <span data-proof="authored" data-by="ai:claude">Description</span>                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <span data-proof="authored" data-by="ai:claude">`developerName`</span>                          | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">API name (underscores, no spaces)</span>                                                                                                                                                                                                   |
| <span data-proof="authored" data-by="ai:claude">`masterLabel`</span>                            | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">Display label</span>                                                                                                                                                                                                                       |
| <span data-proof="authored" data-by="ai:claude">`relatedEntity`</span>                          | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">Primary Salesforce object (e.g.,</span> <span data-proof="authored" data-by="ai:claude">`Case`,</span> <span data-proof="authored" data-by="ai:claude">`Account`,</span> <span data-proof="authored" data-by="ai:claude">`Contact`)</span> |
| <span data-proof="authored" data-by="ai:claude">`type`</span>                                   | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">Template type enum (see Template Types table above)</span>                                                                                                                                                                                 |
| <span data-proof="authored" data-by="ai:claude">`visibility`</span>                             | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">`Global`</span> <span data-proof="authored" data-by="ai:claude">or scoped</span>                                                                                                                                                           |
| <span data-proof="authored" data-by="ai:claude">`createdInVersion`</span>                       | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">Minimum API version (use</span> <span data-proof="authored" data-by="ai:claude">`63.0`</span> <span data-proof="authored" data-by="ai:claude">or higher)</span>                                                                            |
| <span data-proof="authored" data-by="ai:claude">`activeVersion`</span>                          | <span data-proof="authored" data-by="ai:claude">Auto</span>     | <span data-proof="authored" data-by="ai:claude">Hash-based version ID (Salesforce-generated)</span>                                                                                                                                                                                        |
| <span data-proof="authored" data-by="ai:claude">`templateVersions`</span>                       | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">Container for version-specific content</span>                                                                                                                                                                                              |
| <span data-proof="authored" data-by="ai:claude">`templateVersions.content`</span>               | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">The prompt text with merge fields</span>                                                                                                                                                                                                   |
| <span data-proof="authored" data-by="ai:claude">`templateVersions.inputs`</span>                | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">Input object definitions</span>                                                                                                                                                                                                            |
| <span data-proof="authored" data-by="ai:claude">`templateVersions.primaryModel`</span>          | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">LLM model identifier</span>                                                                                                                                                                                                                |
| <span data-proof="authored" data-by="ai:claude">`templateVersions.status`</span>                | <span data-proof="authored" data-by="ai:claude">Yes</span>      | <span data-proof="authored" data-by="ai:claude">`Published`</span> <span data-proof="authored" data-by="ai:claude">or</span> <span data-proof="authored" data-by="ai:claude">`Draft`</span>                                                                                                |
| <span data-proof="authored" data-by="ai:claude">`templateVersions.templateDataProviders`</span> | <span data-proof="authored" data-by="ai:claude">No</span>       | <span data-proof="authored" data-by="ai:claude">Flow/Apex grounding definitions</span>                                                                                                                                                                                                     |
| <span data-proof="authored" data-by="ai:claude">`templateVersions.versionIdentifier`</span>     | <span data-proof="authored" data-by="ai:claude">Auto</span>     | <span data-proof="authored" data-by="ai:claude">Hash-based version ID (Salesforce-generated)</span>                                                                                                                                                                                        |

### <span data-proof="authored" data-by="ai:claude">Available Models</span>

| <span data-proof="authored" data-by="ai:claude">Model ID</span>                           | <span data-proof="authored" data-by="ai:claude">Description</span>          |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| <span data-proof="authored" data-by="ai:claude">`sfdc_ai__DefaultGPT4Omni`</span>         | <span data-proof="authored" data-by="ai:claude">GPT-4o (default)</span>     |
| <span data-proof="authored" data-by="ai:claude">`sfdc_ai__DefaultGPT4OmniMini`</span>     | <span data-proof="authored" data-by="ai:claude">GPT-4o Mini</span>          |
| <span data-proof="authored" data-by="ai:claude">`sfdc_ai__DefaultGPT35Turbo`</span>       | <span data-proof="authored" data-by="ai:claude">GPT-3.5 Turbo</span>        |
| <span data-proof="authored" data-by="ai:claude">`sfdc_ai__DefaultBedrockAnthropic`</span> | <span data-proof="authored" data-by="ai:claude">Claude (via Bedrock)</span> |

### <span data-proof="authored" data-by="ai:claude">Input Definition Patterns</span>

| <span data-proof="authored" data-by="ai:claude">Pattern</span>                  | <span data-proof="authored" data-by="ai:claude">Use For</span>                 |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| <span data-proof="authored" data-by="ai:claude">`SOBJECT://Case`</span>         | <span data-proof="authored" data-by="ai:claude">Salesforce object input</span> |
| <span data-proof="authored" data-by="ai:claude">`flow://MyFlowApiName`</span>   | <span data-proof="authored" data-by="ai:claude">Flow data provider</span>      |
| <span data-proof="authored" data-by="ai:claude">`apex://MyApexClassName`</span> | <span data-proof="authored" data-by="ai:claude">Apex data provider</span>      |

### <span data-proof="authored" data-by="ai:claude">package.xml</span>

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTYxLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
<types>
    <members>*</members>
    <name>GenAiPromptTemplate</name>
</types>
<types>
    <members>*</members>
    <name>GenAiPromptTemplateActv</name>
</types>
```

***

## <span data-proof="authored" data-by="ai:claude">Merge Fields</span>

### <span data-proof="authored" data-by="ai:claude">Syntax Reference</span>

| <span data-proof="authored" data-by="ai:claude">Merge Field Type</span> | <span data-proof="authored" data-by="ai:claude">Syntax</span>                                        | <span data-proof="authored" data-by="ai:claude">Example</span>                                     |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **<span data-proof="authored" data-by="ai:claude">Record field</span>** | <span data-proof="authored" data-by="ai:claude">`{!$Input:Object.FieldName}`</span>                  | <span data-proof="authored" data-by="ai:claude">`{!$Input:Case.Subject}`</span>                    |
| **<span data-proof="authored" data-by="ai:claude">Related list</span>** | <span data-proof="authored" data-by="ai:claude">`{!$RelatedList:Object.Relationship.Records}`</span> | <span data-proof="authored" data-by="ai:claude">`{!$RelatedList:Case.CaseComments.Records}`</span> |
| **<span data-proof="authored" data-by="ai:claude">Flow output</span>**  | <span data-proof="authored" data-by="ai:claude">`{!$Flow:FlowName.OutputVariable}`</span>            | <span data-proof="authored" data-by="ai:claude">`{!$Flow:GetExperiences.experienceList}`</span>    |
| **<span data-proof="authored" data-by="ai:claude">Apex output</span>**  | <span data-proof="authored" data-by="ai:claude">Referenced via data provider</span>                  | <span data-proof="authored" data-by="ai:claude">See Apex Grounding section</span>                  |
| **<span data-proof="authored" data-by="ai:claude">Organization</span>** | <span data-proof="authored" data-by="ai:claude">`{!$Organization.Name}`</span>                       | <span data-proof="authored" data-by="ai:claude">`{!$Organization.Name}`</span>                     |

### <span data-proof="authored" data-by="ai:claude">Merge Field Examples in Prompt Content</span>

```
You are a customer service representative at {!$Organization.Name}.

Summarize the following case:
- Subject: {!$Input:Case.Subject}
- Description: {!$Input:Case.Description}
- Priority: {!$Input:Case.Priority}
- Status: {!$Input:Case.Status}

Related comments:
{!$RelatedList:Case.CaseComments.Records}

Additional context from analysis:
{!$Flow:AnalyzeCase.caseContext}

Return your response as JSON with keys: summary, sentiment, suggestedAction.
```

***

## <span data-proof="authored" data-by="ai:claude">Grounding with Data Providers</span>

### <span data-proof="authored" data-by="ai:claude">Flow Grounding</span>

<span data-proof="authored" data-by="ai:claude">Create a</span> **<span data-proof="authored" data-by="ai:claude">Template-Triggered Prompt Flow</span>** <span data-proof="authored" data-by="ai:claude">bound to the template capability.</span>

**<span data-proof="authored" data-by="ai:claude">Flow elements:</span>**

1. **<span data-proof="authored" data-by="ai:claude">Start Element</span>** <span data-proof="authored" data-by="ai:claude">— configure with Prompt Template Type and input object</span>
2. **<span data-proof="authored" data-by="ai:claude">Get Records</span>** <span data-proof="authored" data-by="ai:claude">— query related data</span>
3. **<span data-proof="authored" data-by="ai:claude">Loop</span>** <span data-proof="authored" data-by="ai:claude">— iterate through records</span>
4. **<span data-proof="authored" data-by="ai:claude">Add Prompt Instructions</span>** <span data-proof="authored" data-by="ai:claude">— append text to the prompt (can be used multiple times)</span>

**<span data-proof="authored" data-by="ai:claude">XML data provider definition:</span>**

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MzgxLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
<templateDataProviders>
    <definition>flow://GetCaseAnalysis</definition>
    <parameters>
        <definition>SOBJECT://Case</definition>
        <isRequired>true</isRequired>
        <parameterName>myCase</parameterName>
        <valueExpression>{!$Input:Case}</valueExpression>
    </parameters>
    <referenceName>Flow:GetCaseAnalysis</referenceName>
</templateDataProviders>
```

### <span data-proof="authored" data-by="ai:claude">Apex Grounding</span>

<span data-proof="authored" data-by="ai:claude">Implement an</span> <span data-proof="authored" data-by="ai:claude">`@InvocableMethod`</span> <span data-proof="authored" data-by="ai:claude">annotated to a capability type.</span>

**<span data-proof="authored" data-by="ai:claude">Capability types:</span>**

| <span data-proof="authored" data-by="ai:claude">Template Type</span>    | <span data-proof="authored" data-by="ai:claude">Capability</span>                                           |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| <span data-proof="authored" data-by="ai:claude">Sales Email</span>      | <span data-proof="authored" data-by="ai:claude">`PromptTemplateType://einstein_gpt__salesEmail`</span>      |
| <span data-proof="authored" data-by="ai:claude">Field Generation</span> | <span data-proof="authored" data-by="ai:claude">`PromptTemplateType://einstein_gpt__fieldCompletion`</span> |
| <span data-proof="authored" data-by="ai:claude">Flex</span>             | <span data-proof="authored" data-by="ai:claude">`FlexTemplate://Template_Api_Name`</span>                   |
| <span data-proof="authored" data-by="ai:claude">Record Summary</span>   | <span data-proof="authored" data-by="ai:claude">`PromptTemplateType://einstein_gpt__recordSummary`</span>   |

**<span data-proof="authored" data-by="ai:claude">Apex grounding class:</span>**

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTMwNywiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
public with sharing class CaseContextProvider {

    @InvocableMethod(
        label='Get Case Context'
        capabilityType='PromptTemplateType://einstein_gpt__fieldCompletion'
    )
    public static List<Response> getCaseContext(List<Request> requests) {
        List<Response> responses = new List<Response>();

        for (Request req : requests) {
            Case c = req.myCase;

            // Query related data
            List<CaseComment> comments = [
                SELECT CommentBody, CreatedDate, CreatedBy.Name
                FROM CaseComment
                WHERE ParentId = :c.Id
                WITH SECURITY_ENFORCED
                ORDER BY CreatedDate DESC
                LIMIT 10
            ];

            // Build context string
            String context = 'Recent comments:\n';
            for (CaseComment cc : comments) {
                context += '- ' + cc.CreatedBy.Name + ': ' + cc.CommentBody + '\n';
            }

            Response res = new Response();
            res.prompt = context;
            responses.add(res);
        }

        return responses;
    }

    public class Request {
        @InvocableVariable(required=true)
        public Case myCase;
    }

    public class Response {
        @InvocableVariable
        public String prompt;
    }
}
```

**<span data-proof="authored" data-by="ai:claude">XML data provider for Apex:</span>**

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6Mzg5LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
<templateDataProviders>
    <definition>apex://CaseContextProvider</definition>
    <parameters>
        <definition>SOBJECT://Case</definition>
        <isRequired>true</isRequired>
        <parameterName>myCase</parameterName>
        <valueExpression>{!$Input:Case}</valueExpression>
    </parameters>
    <referenceName>Apex:CaseContextProvider</referenceName>
</templateDataProviders>
```

***

## <span data-proof="authored" data-by="ai:claude">Apex Invocation (Connect API)</span>

### <span data-proof="authored" data-by="ai:claude">Core Pattern</span>

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTM2MSwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
public with sharing class PromptTemplateController {

    @AuraEnabled
    public static String invokeTemplate(String recordId) {
        // 1. Build input parameters
        Map<String, String> recordMap = new Map<String, String>();
        recordMap.put('id', recordId);

        ConnectApi.WrappedValue wrappedRecord = new ConnectApi.WrappedValue();
        wrappedRecord.value = recordMap;

        Map<String, ConnectApi.WrappedValue> inputParams =
            new Map<String, ConnectApi.WrappedValue>();
        inputParams.put('Input:Case', wrappedRecord);

        // 2. Configure execution
        ConnectApi.EinsteinPromptTemplateGenerationsInput templateInput =
            new ConnectApi.EinsteinPromptTemplateGenerationsInput();
        templateInput.additionalConfig =
            new ConnectApi.EinsteinLlmAdditionalConfigInput();
        templateInput.additionalConfig.applicationName = 'PromptBuilderPreview';
        templateInput.isPreview = false;
        templateInput.inputParams = inputParams;

        // 3. Execute and return
        ConnectApi.EinsteinPromptTemplateGenerationsRepresentation result =
            ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(
                'My_Template_Api_Name',  // Template developer name
                templateInput
            );

        return result.generations[0].text;
    }
}
```

### <span data-proof="authored" data-by="ai:claude">Key Method</span>

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTQ3LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(
    String templateApiName,
    ConnectApi.EinsteinPromptTemplateGenerationsInput input
)
```

### <span data-proof="authored" data-by="ai:claude">Input Configuration Parameters</span>

| <span data-proof="authored" data-by="ai:claude">Parameter</span>                          | <span data-proof="authored" data-by="ai:claude">Type</span>    | <span data-proof="authored" data-by="ai:claude">Description</span>                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span data-proof="authored" data-by="ai:claude">`isPreview`</span>                        | <span data-proof="authored" data-by="ai:claude">Boolean</span> | <span data-proof="authored" data-by="ai:claude">`true`</span> <span data-proof="authored" data-by="ai:claude">= resolved prompt only (no LLM call),</span> <span data-proof="authored" data-by="ai:claude">`false`</span> <span data-proof="authored" data-by="ai:claude">= full generation</span> |
| <span data-proof="authored" data-by="ai:claude">`numGenerations`</span>                   | <span data-proof="authored" data-by="ai:claude">Integer</span> | <span data-proof="authored" data-by="ai:claude">Number of responses (default: 1)</span>                                                                                                                                                                                                            |
| <span data-proof="authored" data-by="ai:claude">`temperature`</span>                      | <span data-proof="authored" data-by="ai:claude">Decimal</span> | <span data-proof="authored" data-by="ai:claude">0.0–1.0 randomness (0 = deterministic)</span>                                                                                                                                                                                                      |
| <span data-proof="authored" data-by="ai:claude">`frequencyPenalty`</span>                 | <span data-proof="authored" data-by="ai:claude">Decimal</span> | <span data-proof="authored" data-by="ai:claude">Controls token repetition</span>                                                                                                                                                                                                                   |
| <span data-proof="authored" data-by="ai:claude">`inputParams`</span>                      | <span data-proof="authored" data-by="ai:claude">Map</span>     | <span data-proof="authored" data-by="ai:claude">Objects keyed as</span> <span data-proof="authored" data-by="ai:claude">`Input:ResourceApiName`</span>                                                                                                                                             |
| <span data-proof="authored" data-by="ai:claude">`additionalConfig.applicationName`</span> | <span data-proof="authored" data-by="ai:claude">String</span>  | <span data-proof="authored" data-by="ai:claude">Application context identifier</span>                                                                                                                                                                                                              |

### <span data-proof="authored" data-by="ai:claude">Response Structure</span>

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MzcyLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
// Response object
ConnectApi.EinsteinPromptTemplateGenerationsRepresentation result;

// Access generated text
String generatedText = result.generations[0].text;

// Access safety scores (Einstein Trust Layer)
ConnectApi.SafetyScoreRepresentation safety = result.safetyScoreRepresentation;

// Access resolved prompt (for debugging)
String resolvedPrompt = result.prompt;
```

### <span data-proof="authored" data-by="ai:claude">Multiple Input Objects (Flex Template)</span>

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6NjYyLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
// For Flex templates with multiple inputs
Map<String, ConnectApi.WrappedValue> inputParams =
    new Map<String, ConnectApi.WrappedValue>();

// First input
Map<String, String> contactMap = new Map<String, String>();
contactMap.put('id', contactId);
ConnectApi.WrappedValue contactValue = new ConnectApi.WrappedValue();
contactValue.value = contactMap;
inputParams.put('Input:Contact', contactValue);

// Second input
Map<String, String> accountMap = new Map<String, String>();
accountMap.put('id', accountId);
ConnectApi.WrappedValue accountValue = new ConnectApi.WrappedValue();
accountValue.value = accountMap;
inputParams.put('Input:Account', accountValue);
```

***

## <span data-proof="authored" data-by="ai:claude">LWC Integration</span>

### <span data-proof="authored" data-by="ai:claude">Controller + Component Pattern</span>

**<span data-proof="authored" data-by="ai:claude">Apex Controller:</span>**

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTI2NiwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
public with sharing class SocialMediaPostsController {

    @AuraEnabled
    public static String generateSocialMediaPosts(String experienceSessionId) {
        Map<String, String> session = new Map<String, String>();
        session.put('id', experienceSessionId);
        ConnectApi.WrappedValue sessionValue = new ConnectApi.WrappedValue();
        sessionValue.value = session;
        Map<String, ConnectApi.WrappedValue> inputParams =
            new Map<String, ConnectApi.WrappedValue>();
        inputParams.put('Input:experienceSession', sessionValue);

        ConnectApi.EinsteinPromptTemplateGenerationsInput executeInput =
            new ConnectApi.EinsteinPromptTemplateGenerationsInput();
        executeInput.additionalConfig =
            new ConnectApi.EinsteinLlmAdditionalConfigInput();
        executeInput.additionalConfig.applicationName = 'PromptBuilderPreview';
        executeInput.isPreview = false;
        executeInput.inputParams = inputParams;

        ConnectApi.EinsteinPromptTemplateGenerationsRepresentation output =
            ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(
                'Generate_Social_Media_Posts',
                executeInput
            );

        return output.generations[0].text;
    }
}
```

**<span data-proof="authored" data-by="ai:claude">LWC JavaScript:</span>**

```javascript proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTEzMCwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
import { api, LightningElement } from "lwc";
import generatePosts from "@salesforce/apex/SocialMediaPostsController.generateSocialMediaPosts";

export default class GenerateSocialMediaPosts extends LightningElement {
    @api recordId;
    twitterPost;
    linkedinPost;
    slackPost;
    error;
    showSpinner = false;

    get hasResult() {
        return this.twitterPost || this.linkedinPost;
    }

    async handleGenerate() {
        this.showSpinner = true;
        this.error = undefined;
        try {
            const response = await generatePosts({
                experienceSessionId: this.recordId
            });
            const parsed = JSON.parse(response);
            this.twitterPost = parsed.twitter;
            this.linkedinPost = parsed.linkedin;
            this.slackPost = JSON.stringify(parsed.blockkit);
        } catch (err) {
            this.error = err.body?.message || 'An error occurred';
            this.twitterPost = undefined;
            this.linkedinPost = undefined;
            this.slackPost = undefined;
        } finally {
            this.showSpinner = false;
        }
    }
}
```

**<span data-proof="authored" data-by="ai:claude">LWC HTML:</span>**

```html proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTc4MSwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
<template>
    <lightning-card title="Generate Social Media Posts"
                    icon-name="utility:socialshare">
        <div class="slds-var-p-around_small">
            <lightning-button onclick={handleGenerate}
                              label="Generate Posts"
                              variant="brand">
            </lightning-button>

            <template lwc:if={showSpinner}>
                <lightning-spinner alternative-text="Generating..."
                                   size="small">
                </lightning-spinner>
            </template>

            <template lwc:if={error}>
                <div class="slds-var-p-top_small slds-text-color_error">
                    {error}
                </div>
            </template>

            <template lwc:if={hasResult}>
                <div class="slds-var-p-top_small">
                    <lightning-textarea name="twitter" readonly
                                        value={twitterPost}
                                        label="Twitter Post">
                    </lightning-textarea>
                </div>
                <div class="slds-var-p-top_small">
                    <lightning-textarea name="linkedin" readonly
                                        value={linkedinPost}
                                        label="LinkedIn Post">
                    </lightning-textarea>
                </div>
                <div class="slds-var-p-top_small">
                    <lightning-textarea name="slack" readonly
                                        value={slackPost}
                                        label="Slack Post">
                    </lightning-textarea>
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

**<span data-proof="authored" data-by="ai:claude">LWC Meta XML:</span>**

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6NTUxLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>Generate Social Media Posts</masterLabel>
    <targets>
        <target>lightning__RecordPage</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightning__RecordPage">
            <objects>
                <object>Session__c</object>
            </objects>
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

***

## <span data-proof="authored" data-by="ai:claude">REST API Invocation</span>

### <span data-proof="authored" data-by="ai:claude">Endpoint</span>

```
POST /services/data/v60.0/einstein/prompt-templates/{templateApiName}/generations
```

### <span data-proof="authored" data-by="ai:claude">Request Body</span>

```json proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTY4LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
{
    "isPreview": false,
    "inputParams": {
        "Input:Case": {
            "value": {
                "id": "5001x000001a2bCAAQ"
            }
        }
    }
}
```

### <span data-proof="authored" data-by="ai:claude">Response Body</span>

```json proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MzE3LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
{
    "prompt": "Resolved prompt text with all merge fields replaced...",
    "generations": [
        {
            "id": "generation-id",
            "text": "The generated LLM response text...",
            "contentQuality": {
                "scanToxicity": { "isDetected": false }
            }
        }
    ]
}
```

### <span data-proof="authored" data-by="ai:claude">cURL Example</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6Mzk4LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
curl -X POST \
  "https://yourinstance.salesforce.com/services/data/v60.0/einstein/prompt-templates/My_Template_Name/generations" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "isPreview": false,
    "inputParams": {
        "Input:Case": {
            "value": {
                "id": "5001x000001a2bCAAQ"
            }
        }
    }
  }'
```

***

## <span data-proof="authored" data-by="ai:claude">Flow Integration</span>

### <span data-proof="authored" data-by="ai:claude">Invoking Templates from Flow</span>

1. <span data-proof="authored" data-by="ai:claude">Templates auto-expose as</span> **<span data-proof="authored" data-by="ai:claude">invocable actions</span>** <span data-proof="authored" data-by="ai:claude">once activated</span>
2. <span data-proof="authored" data-by="ai:claude">In Flow Builder, add an</span> **<span data-proof="authored" data-by="ai:claude">Action</span>** <span data-proof="authored" data-by="ai:claude">element</span>
3. <span data-proof="authored" data-by="ai:claude">Filter by category:</span> **<span data-proof="authored" data-by="ai:claude">Prompt Template</span>**
4. <span data-proof="authored" data-by="ai:claude">Select your template</span>
5. <span data-proof="authored" data-by="ai:claude">Pass the record as the related entity input</span>

### <span data-proof="authored" data-by="ai:claude">Record-Triggered Flow Pattern (Case Summarization)</span>

**<span data-proof="authored" data-by="ai:claude">Architecture:</span>**

1. <span data-proof="authored" data-by="ai:claude">Record-Triggered Flow fires on Case create/update</span>
2. <span data-proof="authored" data-by="ai:claude">Entry conditions:</span> <span data-proof="authored" data-by="ai:claude">`Type IS NULL`</span> <span data-proof="authored" data-by="ai:claude">OR</span> <span data-proof="authored" data-by="ai:claude">`Reason IS NULL`</span> <span data-proof="authored" data-by="ai:claude">OR</span> <span data-proof="authored" data-by="ai:claude">`Quick_Summary__c IS NULL`</span>
3. <span data-proof="authored" data-by="ai:claude">Action: Invoke prompt template → returns JSON</span>
4. <span data-proof="authored" data-by="ai:claude">Action: Call Apex</span> <span data-proof="authored" data-by="ai:claude">`@InvocableMethod`</span> <span data-proof="authored" data-by="ai:claude">to parse JSON</span>
5. <span data-proof="authored" data-by="ai:claude">Update Record: Set fields from parsed values</span>

**<span data-proof="authored" data-by="ai:claude">Apex JSON Parser for Flow:</span>**

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTAwMSwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
public with sharing class CaseSummarizationParser {

    @InvocableMethod(label='Parse Case Summary JSON')
    public static List<CaseSummary> parseSummary(List<String> jsonInputs) {
        List<CaseSummary> results = new List<CaseSummary>();

        for (String jsonInput : jsonInputs) {
            Map<String, Object> parsed =
                (Map<String, Object>) JSON.deserializeUntyped(jsonInput);

            CaseSummary summary = new CaseSummary();
            summary.caseType = (String) parsed.get('caseType');
            summary.reason = (String) parsed.get('reason');
            summary.summaryText = (String) parsed.get('summary');
            results.add(summary);
        }

        return results;
    }

    public class CaseSummary {
        @InvocableVariable(label='Case Type')
        public String caseType;

        @InvocableVariable(label='Reason')
        public String reason;

        @InvocableVariable(label='Summary Text')
        public String summaryText;
    }
}
```

***

## <span data-proof="authored" data-by="ai:claude">Batch Processing</span>

<span data-proof="authored" data-by="ai:claude">For bulk generation using</span> <span data-proof="authored" data-by="ai:claude">`AiJobRun`</span> <span data-proof="authored" data-by="ai:claude">and</span> <span data-proof="authored" data-by="ai:claude">`AiJobRunItem`</span> <span data-proof="authored" data-by="ai:claude">objects.</span>

### <span data-proof="authored" data-by="ai:claude">Limits</span>

| <span data-proof="authored" data-by="ai:claude">Constraint</span>          | <span data-proof="authored" data-by="ai:claude">Limit</span>                                                                                                                                           |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <span data-proof="authored" data-by="ai:claude">Standard batch size</span> | <span data-proof="authored" data-by="ai:claude">1,000 items per</span> <span data-proof="authored" data-by="ai:claude">`AiJobRun`</span>                                                               |
| <span data-proof="authored" data-by="ai:claude">Native batch models</span> | <span data-proof="authored" data-by="ai:claude">10,000 items per</span> <span data-proof="authored" data-by="ai:claude">`AiJobRun`</span>                                                              |
| <span data-proof="authored" data-by="ai:claude">Daily limit</span>         | <span data-proof="authored" data-by="ai:claude">5</span> <span data-proof="authored" data-by="ai:claude">`AiJobRun`</span> <span data-proof="authored" data-by="ai:claude">objects per 24 hours</span> |

### <span data-proof="authored" data-by="ai:claude">Batch Workflow</span>

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6Njc4LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
// 1. Create the batch job
AiJobRun job = new AiJobRun();
job.PromptTemplateApiName = 'Summarize_Case';
job.JobType = 'PromptTemplate';
job.Status = 'New';
insert job;

// 2. Create batch items
List<AiJobRunItem> items = new List<AiJobRunItem>();
for (Case c : cases) {
    AiJobRunItem item = new AiJobRunItem();
    item.AiJobRunId = job.Id;
    item.Input = JSON.serialize(new Map<String, Object>{
        'Input:Case' => new Map<String, String>{ 'id' => c.Id }
    });
    items.add(item);
}
insert items;

// 3. Start the job
job.Status = 'ReadyToStart';
update job;

// 4. Monitor via AiJobRunStatusEvent platform event
// Query AiJobRunItem.Response for completed results
```

### <span data-proof="authored" data-by="ai:claude">Monitoring</span>

<span data-proof="authored" data-by="ai:claude">Subscribe to the</span> <span data-proof="authored" data-by="ai:claude">`AiJobRunStatusEvent`</span> <span data-proof="authored" data-by="ai:claude">platform event for status changes:</span>

* <span data-proof="authored" data-by="ai:claude">`InProgress`</span> <span data-proof="authored" data-by="ai:claude">— processing started</span>

* <span data-proof="authored" data-by="ai:claude">`Completed`</span> <span data-proof="authored" data-by="ai:claude">— all items processed</span>

* <span data-proof="authored" data-by="ai:claude">`Failed`</span> <span data-proof="authored" data-by="ai:claude">— job failed</span>

***

## <span data-proof="authored" data-by="ai:claude">Agent Script Integration</span>

<span data-proof="authored" data-by="ai:claude">Prompt templates can be invoked as actions within Agent Script agents.</span>

### <span data-proof="authored" data-by="ai:claude">Action Definition</span>

```
action get_personalized_schedule:
  target: generatePromptResponse://Generate_Personalized_Schedule
  inputs:
    "Input:email": string
      description: "User's email address"
      is_required: True
  outputs:
    promptResponse: string
      is_used_by_planner: True
      is_displayable: True
```

### <span data-proof="authored" data-by="ai:claude">Topic Usage</span>

```
topic schedule_generation:
  description: Generates a personalized schedule for guests
  reasoning:
    | Ask the customer for their email address.
    -> @utils.set variable @variables.email
       description: The email address the customer provided
       ...
    -> if @variables.email is not None
      -> run @actions.get_personalized_schedule
         with "Input:email": @variables.email
         set @variables.schedule = @outputs.promptResponse
    | Here is your personalized schedule: {!@variables.schedule}
```

***

## <span data-proof="authored" data-by="ai:claude">Complete Examples</span>

### <span data-proof="authored" data-by="ai:claude">Example 1: Field Generation Template (XML)</span>

<span data-proof="authored" data-by="ai:claude">Generate a marketing description for a custom Experience object.</span>

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTQ0OCwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
<?xml version="1.0" encoding="UTF-8"?>
<GenAiPromptTemplate xmlns="http://soap.sforce.com/2006/04/metadata">
    <createdInVersion>63.0</createdInVersion>
    <developerName>Generate_Experience_Description</developerName>
    <masterLabel>Generate Experience Description</masterLabel>
    <relatedEntity>Experience__c</relatedEntity>
    <templateVersions>
        <content>You are a marketing copywriter for {!$Organization.Name}.

Write an 80-100 word marketing description for this experience:
- Name: {!$Input:Experience__c.Name}
- Type: {!$Input:Experience__c.Type__c}
- Location: {!$Input:Experience__c.Location__c}
- Duration: {!$Input:Experience__c.Duration_Hours__c} hours
- Activity Level: {!$Input:Experience__c.Activity_Level__c}
- Capacity: {!$Input:Experience__c.Capacity__c} guests

Write in an engaging, benefit-focused tone. Highlight what makes this
experience unique. Do not use generic filler phrases.</content>
        <inputs>
            <apiName>myExperience</apiName>
            <definition>SOBJECT://Experience__c</definition>
            <referenceName>Input:Experience__c</referenceName>
            <required>true</required>
        </inputs>
        <primaryModel>sfdc_ai__DefaultGPT4Omni</primaryModel>
        <status>Published</status>
        <versionIdentifier>1</versionIdentifier>
    </templateVersions>
    <type>einstein_gpt__fieldCompletion</type>
    <visibility>Global</visibility>
</GenAiPromptTemplate>
```

### <span data-proof="authored" data-by="ai:claude">Example 2: Flex Template with Apex Grounding (XML + Apex)</span>

<span data-proof="authored" data-by="ai:claude">Summarize and classify cases with structured JSON output.</span>

**<span data-proof="authored" data-by="ai:claude">Template XML:</span>**

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTg5OSwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
<?xml version="1.0" encoding="UTF-8"?>
<GenAiPromptTemplate xmlns="http://soap.sforce.com/2006/04/metadata">
    <createdInVersion>63.0</createdInVersion>
    <developerName>Summarize_Classify_Case</developerName>
    <masterLabel>Summarize and Classify Case</masterLabel>
    <relatedEntity>Case</relatedEntity>
    <templateVersions>
        <content>Analyze the following case and return a JSON response.

Case Details:
- Subject: {!$Input:Case.Subject}
- Description: {!$Input:Case.Description}
- Priority: {!$Input:Case.Priority}

Related Comments:
{!$RelatedList:Case.CaseComments.Records}

Additional Context:
{!$Flow:AnalyzeCaseContext.analysisResult}

Return ONLY valid JSON with these exact keys:
{
  "caseType": "one of: Mechanical, Electrical, Electronic, Structural, Other",
  "reason": "one of: Installation, Equipment Complexity, Equipment Design, Performance, Breakdown, Safety",
  "summary": "2-3 sentence summary of the case"
}</content>
        <inputs>
            <apiName>myCase</apiName>
            <definition>SOBJECT://Case</definition>
            <referenceName>Input:Case</referenceName>
            <required>true</required>
        </inputs>
        <primaryModel>sfdc_ai__DefaultGPT4Omni</primaryModel>
        <status>Published</status>
        <templateDataProviders>
            <definition>flow://AnalyzeCaseContext</definition>
            <parameters>
                <definition>SOBJECT://Case</definition>
                <isRequired>true</isRequired>
                <parameterName>myCase</parameterName>
                <valueExpression>{!$Input:Case}</valueExpression>
            </parameters>
            <referenceName>Flow:AnalyzeCaseContext</referenceName>
        </templateDataProviders>
        <versionIdentifier>1</versionIdentifier>
    </templateVersions>
    <type>FlexTemplate</type>
    <visibility>Global</visibility>
</GenAiPromptTemplate>
```

### <span data-proof="authored" data-by="ai:claude">Example 3: Sales Email Template (XML)</span>

```xml proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTgyMCwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
<?xml version="1.0" encoding="UTF-8"?>
<GenAiPromptTemplate xmlns="http://soap.sforce.com/2006/04/metadata">
    <createdInVersion>63.0</createdInVersion>
    <developerName>Welcome_Email_Upcoming_Trip</developerName>
    <masterLabel>Welcome Email for Upcoming Trip</masterLabel>
    <relatedEntity>Contact</relatedEntity>
    <templateVersions>
        <content>Craft a warm, personalized welcome email for an upcoming resort visit.

Sender: {!$Input:Sender.Name} from {!$Organization.Name}
Guest: {!$Input:Contact.Name}
Check-in Date: {!$Input:Contact.Next_Check_In_Date__c}

Recommended experiences based on guest interests:
{!$Flow:GetGuestExperiences.experienceList}

Tone: Warm, professional, excited. Keep under 200 words.
Include a personal touch based on their interests.
End with contact information for concierge services.</content>
        <inputs>
            <apiName>recipient</apiName>
            <definition>SOBJECT://Contact</definition>
            <referenceName>Input:Contact</referenceName>
            <required>true</required>
        </inputs>
        <primaryModel>sfdc_ai__DefaultGPT4Omni</primaryModel>
        <status>Published</status>
        <templateDataProviders>
            <definition>flow://GetGuestExperiences</definition>
            <parameters>
                <definition>SOBJECT://Contact</definition>
                <isRequired>true</isRequired>
                <parameterName>recipient</parameterName>
                <valueExpression>{!$Input:Contact}</valueExpression>
            </parameters>
            <referenceName>Flow:GetGuestExperiences</referenceName>
        </templateDataProviders>
        <versionIdentifier>1</versionIdentifier>
    </templateVersions>
    <type>einstein_gpt__salesEmail</type>
    <visibility>Global</visibility>
</GenAiPromptTemplate>
```

### <span data-proof="authored" data-by="ai:claude">Example 4: Full Apex + LWC Integration</span>

**<span data-proof="authored" data-by="ai:claude">Apex Controller for any template:</span>**

```apex proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MTI1MSwiYXR0cnMiOnsiYnkiOiJhaTpjbGF1ZGUifX1d
public with sharing class PromptTemplateInvoker {

    @AuraEnabled
    public static String invoke(String templateApiName, String recordId, String objectType) {
        Map<String, String> record = new Map<String, String>();
        record.put('id', recordId);

        ConnectApi.WrappedValue wrappedValue = new ConnectApi.WrappedValue();
        wrappedValue.value = record;

        Map<String, ConnectApi.WrappedValue> inputParams =
            new Map<String, ConnectApi.WrappedValue>();
        inputParams.put('Input:' + objectType, wrappedValue);

        ConnectApi.EinsteinPromptTemplateGenerationsInput templateInput =
            new ConnectApi.EinsteinPromptTemplateGenerationsInput();
        templateInput.additionalConfig =
            new ConnectApi.EinsteinLlmAdditionalConfigInput();
        templateInput.additionalConfig.applicationName = 'PromptBuilderPreview';
        templateInput.isPreview = false;
        templateInput.inputParams = inputParams;

        ConnectApi.EinsteinPromptTemplateGenerationsRepresentation result =
            ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(
                templateApiName,
                templateInput
            );

        return result.generations[0].text;
    }
}
```

***

## <span data-proof="authored" data-by="ai:claude">Deployment Guide</span>

### <span data-proof="authored" data-by="ai:claude">Retrieve from Org</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6NzUsImF0dHJzIjp7ImJ5IjoiYWk6Y2xhdWRlIn19XQ==
sf project retrieve start -m GenAiPromptTemplate -m GenAiPromptTemplateActv
```

### <span data-proof="authored" data-by="ai:claude">Deploy to Org</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6NzMsImF0dHJzIjp7ImJ5IjoiYWk6Y2xhdWRlIn19XQ==
sf project deploy start -m GenAiPromptTemplate -m GenAiPromptTemplateActv
```

### <span data-proof="authored" data-by="ai:claude">Deployment Order (When Dependencies Exist)</span>

<span data-proof="authored" data-by="ai:claude">If a template references a Flow that contains Apex:</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MzA2LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
# Step 1: Deploy Apex classes first
sf project deploy start -m ApexClass:CaseContextProvider -m ApexClass:CaseSummarizationParser

# Step 2: Deploy Flows
sf project deploy start -m Flow:AnalyzeCaseContext

# Step 3: Deploy templates
sf project deploy start -m GenAiPromptTemplate -m GenAiPromptTemplateActv
```

### <span data-proof="authored" data-by="ai:claude">Version Identifiers</span>

* <span data-proof="authored" data-by="ai:claude">`activeVersion`</span> <span data-proof="authored" data-by="ai:claude">and</span> <span data-proof="authored" data-by="ai:claude">`versionIdentifier`</span> <span data-proof="authored" data-by="ai:claude">use</span> **<span data-proof="authored" data-by="ai:claude">hash-based IDs</span>** <span data-proof="authored" data-by="ai:claude">(Salesforce-generated)</span>

* <span data-proof="authored" data-by="ai:claude">When creating new templates from scratch, use a placeholder like</span> <span data-proof="authored" data-by="ai:claude">`1`</span> <span data-proof="authored" data-by="ai:claude">— Salesforce will assign the hash on deploy</span>

* <span data-proof="authored" data-by="ai:claude">When modifying retrieved templates, preserve the existing hash values</span>

***

## <span data-proof="authored" data-by="ai:claude">Tips & Gotchas</span>

1. **<span data-proof="authored" data-by="ai:claude">API version 60+ required</span>** <span data-proof="authored" data-by="ai:claude">for all metadata operations with</span> <span data-proof="authored" data-by="ai:claude">`GenAiPromptTemplate`</span>
2. **<span data-proof="authored" data-by="ai:claude">Dependencies must exist first</span>** <span data-proof="authored" data-by="ai:claude">—</span> <span data-proof="authored" data-by="ai:claude">`relatedEntity`, referenced Flows, Apex classes must be in the target org or deployed together</span>
3. **<span data-proof="authored" data-by="ai:claude">Known bug</span>**<span data-proof="authored" data-by="ai:claude">: Templates referencing Flows that contain Apex fail on single-package deploy. Deploy Apex + Flow first, then the template</span>
4. **<span data-proof="authored" data-by="ai:claude">Hash version IDs</span>** <span data-proof="authored" data-by="ai:claude">can cause schema validation errors on scratch orgs — this is a known Salesforce issue</span>
5. **<span data-proof="authored" data-by="ai:claude">`isPreview: true`</span>** <span data-proof="authored" data-by="ai:claude">returns the resolved prompt without calling the LLM — useful for debugging merge field resolution</span>
6. **<span data-proof="authored" data-by="ai:claude">JSON output pattern</span>** <span data-proof="authored" data-by="ai:claude">— instruct the template to return structured JSON, then parse with</span> <span data-proof="authored" data-by="ai:claude">`@InvocableMethod`</span> <span data-proof="authored" data-by="ai:claude">in Apex for Flow consumption</span>
7. **<span data-proof="authored" data-by="ai:claude">Einstein Trust Layer</span>** <span data-proof="authored" data-by="ai:claude">— all template invocations pass through toxicity detection; access safety scores via</span> <span data-proof="authored" data-by="ai:claude">`safetyScoreRepresentation`</span>
8. **<span data-proof="authored" data-by="ai:claude">Record Summary is Copilot-only</span>** <span data-proof="authored" data-by="ai:claude">— cannot be invoked from Flow, Apex, or REST API</span>
9. **<span data-proof="authored" data-by="ai:claude">Temperature 0</span>** <span data-proof="authored" data-by="ai:claude">is the default and recommended for deterministic business outputs</span>
10. **<span data-proof="authored" data-by="ai:claude">Activation required</span>** <span data-proof="authored" data-by="ai:claude">— templates must be saved AND activated before they appear as invocable actions in Flow</span>
11. **<span data-proof="authored" data-by="ai:claude">Input key format</span>** <span data-proof="authored" data-by="ai:claude">— always prefix with</span> <span data-proof="authored" data-by="ai:claude">`Input:`</span> <span data-proof="authored" data-by="ai:claude">when passing parameters (e.g.,</span> <span data-proof="authored" data-by="ai:claude">`Input:Case`,</span> <span data-proof="authored" data-by="ai:claude">`Input:Contact`)</span>
12. **<span data-proof="authored" data-by="ai:claude">`GenAiPromptTemplateActv`</span>** <span data-proof="authored" data-by="ai:claude">is the activation metadata — always deploy alongside</span> <span data-proof="authored" data-by="ai:claude">`GenAiPromptTemplate`</span>