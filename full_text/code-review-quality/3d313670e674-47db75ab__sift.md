---
name: sift
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging sift. Use this skill whenever modifying sift configurations or adding related functionality.
---
# sift

## File Tree

```text
sift/
├── assets
├── modules
│   └── sift (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/sift`

```python
apps\sift-api\f\sift\agents.py:
⋮
│def main(
│    agent_name: Optional[str] = None,
│    agent_card_params: Optional[Dict] = None,
│    litellm_params: Optional[Dict] = None,
│    dspy_params: Optional[Dict] = None,
│    object_permission: Optional[Dict] = None,
│    labels: Optional[List] = None,
│    webhook: Optional[Dict] = None,
⋮

apps\sift-api\f\sift\responses.py:
⋮
│def main(
│    model: str,
│    input: Union[str, List[Dict]],
│    background: bool = False,
│    webhook: Optional[Dict] = None,
⋮

apps\sift-api\rt.d.ts:
⋮
│  type Ably = {
│    apiKye: string
⋮
│  type Abstractapi = {
│    apiKey: string
⋮
│  type Accelo = {
│    clientId: string,
│    deployment: string,
│    clientSecret: string
⋮
│  type Actimo = {
│    apiKey: string
⋮
│  type Acumbamail = {
│    authToken: string
⋮
│  type Adhook = {
│    token: string
⋮
│  type Adrapid = {
│    apiToken: string
⋮
│  type AeroWorkflow = {
│    apiKey: string
⋮
│  type AgentInstructions = any
│
│  type Ai21 = {
│    apiKey: string
⋮
│  type Airtable = {
│    apiKey: string
⋮
│  type AirtableTable = {
│    baseId: string,
│    tableName: string
⋮
│  type AnsibleInventory = {
│    content: string
⋮
│  type Anthropic = {
│    apiKey: string,
│    base_url: string,
│    platform: string,
│    enable_1M_context: boolean
⋮
│  type Apify = {
│    token: string
⋮
│  type ApifyApiKey = {
│    api_key: string
⋮
│  type ApifyWebhookConfig = {
│    url: string,
│    token: string
⋮
│  type ApiKeyAuth = {
│    api_key_header: string,
│    api_key_secret: string
⋮
│  type Apollo = {
│    apiKey: string
⋮
│  type Appwrite = {
│    key: string,
│    project: string,
│    endpoint: string,
│    self_signed: boolean
⋮
│  type ArcgisAccount = {
│    password: string,
│    username: string
⋮
│  type Asana = {
│    token: string
⋮
│  type Assemblyai = {
│    apiKey: string
⋮
│  type Attio = {
│    token: string
⋮
│  type Aws = {
│    region: string,
│    awsAccessKeyId: string,
│    awsSecretAccessKey: string
⋮
│  type AwsBedrock = {
│    apiKey: string,
│    region: string,
│    awsAccessKeyId: string,
│    awsSessionToken: string,
│    awsSecretAccessKey: string
⋮
│  type AwsOidc = {
│    region: string,
│    roleArn: string
⋮
│  type Azure = {
│    azureClientId: string,
│    azureTenantId: string,
│    azureClientSecret: string
⋮
│  type AzureBlob = {
│    useSSL: boolean,
│    endpoint: string,
│    accessKey: string,
│    accountName: string,
│    containerName: string
⋮
│  type AzureOauth = {
│    token: string
⋮
│  type AzureOpenai = {
│    apiKey: string,
│    baseUrl: string
⋮
│  type AzureWorkloadIdentity = {
│    useSSL: boolean,
│    accountName: string,
│    containerName: string
⋮
│  type BambooHr = {
│    apiKey: string,
│    companyDomain: string
⋮
│  type Baremetrics = {
│    apiKey: string
⋮
│  type Baserow = {
│    token: string,
│    base_url: string
⋮
│  type BaserowTable = {
│    table_id: number,
│    database_id: number
⋮
│  type BasicHttpAuth = {
│    password: string,
│    username: string
⋮
│  type BasisTheory = {
│    apiKey: string
⋮
│  type Beamer = {
│    apiKey: string
⋮
│  type Bigquery = {
│    type: string,
│    auth_uri: string,
│    client_id: string,
│    token_uri: string,
│    project_id: string,
│    private_key: string,
│    client_email: string,
│    private_key_id: string,
│    client_x509_cert_url: string,
⋮
│  type Bitbucket = {
│    password: string,
│    username: string
⋮
│  type Bitly = {
│    token: string
⋮
│  type Bluesky = {
│    password: string,
│    username: string
⋮
│  type Botify = {
│    token: string
⋮
│  type Box = {
│    token: string
⋮
│  type Brevo = {
│    apiKey: string
⋮
│  type Brex = {
│    token: string
⋮
│  type Buttondown = {
│    token: string
⋮
│  type Cacertificate = {
│    certificate: string
⋮
│  type Calendly = {
│    token: string
⋮
│  type Campayn = {
│    apiKey: string
⋮
│  type Certopus = {
│    apiKey: string
⋮
│  type Chromadb = {
│    ssl: boolean,
│    host: string,
│    port: number,
│    tenant: string,
│    database: string
⋮
│  type Circleci = {
│    token: string
⋮
│  type Clerk = {
│    apiKey: string
⋮
│  type Clickhouse = {
│    host: string,
│    password: string,
│    username: string
⋮
│  type Clickup = {
│    token: string
⋮
│  type Cloudflare = {
│    key: string,
│    email: string,
│    token: string
⋮
│  type Cockroachdb = {
│    token: string
⋮
│  type Codat = {
│    encodedKey: string
⋮
│  type Cohere = {
│    apiKey: string
⋮
│  type ComapeoServer = {
│    server_url: string,
│    access_token: string
⋮
│  type Confluence = {
│    email: string,
│    baseUrl: string,
│    apiToken: string
⋮
│  type Contentful = {
│    spaceId: string,
│    accessToken: string,
│    environment: string
⋮
│  type Contiguity = {
│    token: string
⋮
│  type Convertkit = {
│    apiSecret: string
⋮
│  type Currencyapi = {
│    apiKey: string
⋮
│  type Customai = {
│    api_key: string,
│    base_url: string
⋮
│  type Datadog = {
│    apiKey: string,
│    appKey: string,
│    apiBase: string
⋮
│  type Datocms = {
│    apiKey: string
⋮
│  type Deel = {
│    apiKey: string
⋮
│  type DeepInfra = {
│    token: string
⋮
│  type Deepl = {
│    apiKey: string,
│    baseUrl: string
⋮
│  type Deepseek = {
│    api_key: string,
│    base_url: string
⋮
│  type Digitalocean = {
│    token: string
⋮
│  type DiscordBotConfiguration = {
│    public_key: string,
│    application_id: string
⋮
│  type DiscordWebhook = {
│    webhook_url: string
⋮
│  type Discourse = {
│    apiKey: string,
│    apiUsername: string,
│    defaultHost: string
⋮
│  type Docspring = {
│    tokenId: string,
│    tokenSecret: string
⋮
│  type Dust = {
│    apiKey: string,
│    workspaceId: string
⋮
│  type Dynatrace = {
│    accessToken: string,
│    environmentId: string,
│    environmentUrl: string
⋮
│  type Edgedb = {
│    dsn: string,
│    host: string,
│    port: number,
│    user: string,
│    database: string,
│    password: string,
│    secretKey: string,
│    instanceName: string
⋮
│  type Enode = {
│    token: string
⋮
│  type Exa = {
│    apiKey: string
⋮
│  type Faunadb = {
│    region: string,
│    secret: string
⋮
│  type Figma = {
│    token: string
⋮
│  type Firebase = {
│    appId: string,
│    apiKey: string,
│    projectId: string,
│    authDomain: string,
│    measurementId: string,
│    storageBucket: string,
│    messagingSenderId: string
⋮
│  type Fly = {
│    token: string
⋮
│  type Formstack = {
│    token: string
⋮
│  type Foxentry = {
│    apiKey: string
⋮
│  type Freshdesk = {
│    apiKey: string,
│    baseUrl: string
⋮
│  type Funkwhale = {
│    token: string,
│    baseUrl: string
⋮
│  type Gcal = {
│    token: string
⋮
│  type Gcloud = {
│    type: string,
│    auth_uri: string,
│    client_id: string,
│    token_uri: string,
│    project_id: string,
│    private_key: string,
│    client_email: string,
│    private_key_id: string,
│    client_x509_cert_url: string,
⋮
│  type GcloudStorage = {
│    bucket: string,
│    serviceAccountKey: any
⋮
│  type GcpServiceAccount = {
│    type: string,
│    auth_uri: string,
│    client_id: string,
│    token_uri: string,
│    project_id: string,
│    private_key: string,
│    client_email: string,
│    private_key_id: string,
│    client_x509_cert_url: string,
⋮
│  type Gdocs = {
│    token: string
⋮
│  type Gdrive = {
│    token: string
⋮
│  type Gforms = {
│    token: string
⋮
│  type Gfw = {
│    api_key: string
⋮
│  type Ghostcms = {
│    apiKey: string,
│    apiUrl: string
⋮
│  type Gitbook = {
│    token: string
⋮
│  type Github = {
│    token: string
⋮
│  type Gitlab = {
│    token: string,
│    baseUrl: string
⋮
│  type GitRepository = {
│    url: string,
│    branch: string,
│    folder: string,
│    gpg_key: any,
│    is_github_app: boolean
⋮
│  type Gmail = {
│    token: string
⋮
│  type Googleai = {
│    api_key: string,
│    base_url: string
⋮
│  type Gorgias = {
│    apiKey: string,
│    domain: string,
│    username: string
⋮
│  type GpgKey = {
│    email: string,
│    passphrase: string,
│    private_key: string
⋮
│  type Graphql = {
│    base_url: string,
│    bearer_token: string,
│    custom_headers: any
⋮
│  type Greip = {
│    apiKey: string
⋮
│  type Grist = {
│    host: string,
│    apiKey: string
⋮
│  type Groq = {
│    api_key: string,
│    base_url: string
⋮
│  type Groqai = {
│    api_key: string
⋮
│  type Gsheets = {
│    token: string
⋮
│  type Gworkspace = {
│    token: string
⋮
│  type Holded = {
│    apiKey: string
⋮
│  type Hubspot = {
│    token: string
⋮
│  type IfsCloudOidc = {
│    server: string,
│    clientId: string,
│    oidcPath: string,
│    clientSecret: string
⋮
│  type Intercom = {
│    token: string,
│    apiVersion: string
⋮
│  type Ipinfo = {
│    token: string
⋮
│  type Jira = {
│    domain: string,
│    password: string,
│    username: string
⋮
│  type Jotform = {
│    apiKey: string,
│    baseUrl: string
⋮
│  type JsonSchema = {
│    schema: any
⋮
│  type Kafka = {
│    brokers: string[],
│    security: any
⋮
│  type Klaviyo = {
│    apiKey: string
⋮
│  type Kobotoolbox = {
│    api_key: string,
│    server_url: string
⋮
│  type Kustomer = {
│    apiKey: string
⋮
│  type Langfuse = {
│    base_url: string,
│    public_key: string,
│    secret_key: string
⋮
│  type Ldap = {
│    server: string,
│    use_ssl: boolean,
│    bind_user: string,
│    ssl_validate: boolean,
│    bind_password: string
⋮
│  type Leonardoai = {
│    apiKey: string
⋮
│  type Linear = {
│    apiKey: string
⋮
│  type Linkding = {
│    token: string,
│    baseUrl: string
⋮
│  type Linkedin = {
│    token: string
⋮
│  type Linode = {
│    token: string
⋮
│  type Localcontexts = {
│    api_key: string,
│    project_id: string,
│    server_url: string
⋮
│  type Lumaai = {
│    apiKey: string
⋮
│  type Magento = {
│    accessToken: string,
│    consumerKey: string,
│    consumerSecret: string,
│    accessTokenSecret: string
⋮
│  type Mailchimp = {
│    server: string,
│    api_key: string
⋮
│  type Mailerlite = {
│    apiToken: string
⋮
│  type Mailgun = {
│    api_key: string
⋮
│  type Mapbox = {
│    username: string,
│    access_token: string
⋮
│  type Mastodon = {
│    token: string,
│    baseUrl: string
⋮
│  type Matrix = {
│    token: string,
│    baseUrl: string
⋮
│  type Matteroom = {
│    base_url: string,
│    password: string,
│    username: string
⋮
│  type Mcp = {
│    url: string,
│    name: string,
│    token: string,
│    headers: any
⋮
│  type Meteosource = {
│    tier: string,
│    apiKey: string
⋮
│  type Mezmo = {
│    apiKey: string
⋮
│  type Miro = {
│    token: string
⋮
│  type Mistral = {
│    apiKey: string,
│    base_url: string
⋮
│  type Mollie = {
│    token: string
⋮
│  type Mongodb = {
│    db: string,
│    tls: boolean,
│    servers: any,
│    credential: any
⋮
│  type MongodbRest = {
│    api_key: string,
│    endpoint: string
⋮
│  type Motimate = {
│    token: string
⋮
│  type Mqtt = {
│    tls: {
│    enabled: boolean,
│    ca_certificate: string,
│    pkcs12_client_certificate: string,
│    pkcs12_certificate_password: string
│  },
│    port: number,
│    broker: string,
│    credentials: {
⋮
│  type MsSqlServer = {
│    host: string,
│    port: number,
│    user: string,
│    dbname: string,
│    ca_cert: string,
│    encrypt: boolean,
│    password: string,
│    aad_token: any,
│    trust_cert: boolean,
⋮
│  type MsTeamsWebhook = {
│    webhook_url: string
⋮
│  type Mysql = {
│    ssl: boolean,
│    host: string,
│    port: number,
│    user: string,
│    database: string,
│    password: string,
│    root_certificate_pem: string
⋮
│  type Nats = {
│    auth: any,
│    servers: string[],
│    require_tls: boolean
⋮
│  type Neondb = {
│    apiKey: string
⋮
│  type Netbox = {
│    url: string,
│    token: string
⋮
│  type Netlify = {
│    token: string
⋮
│  type Newsapi = {
│    apiKey: string
⋮
│  type Nextcloud = {
│    token: string,
│    userId: string,
│    baseUrl: string,
│    password: string,
│    username: string
⋮
│  type Nocodb = {
│    table: string,
│    apiUrl: string,
│    xc_token: string,
│    workspace: string
⋮
│  type Notion = {
│    token: string
⋮
│  type OauthClientCredentials = {
│    domain: string,
│    client_id: string,
│    client_secret: string
⋮
│  type Odk = {
│    base_url: string,
│    password: string,
│    username: string,
│    default_project_id: number
⋮
│  type Openai = {
│    api_key: string,
│    base_url: string,
│    organization_id: string
⋮
│  type Openrouter = {
│    api_key: string,
│    base_url: string
⋮
│  type Oracledb = {
│    user: string,
│    database: string,
│    password: string
⋮
│  type Pandadoc = {
│    apiKey: string
⋮
│  type Paychex = {
│    client_id: string,
│    client_secret: string
⋮
│  type Paylocity = {
│    token: string
⋮
│  type Paypal = {
│    clientId: string,
│    clientSecret: string
⋮
│  type Persona = {
│    apiKey: string
⋮
│  type Personio = {
│    clientId: string,
│    clientSecret: string
⋮
│  type Phrase = {
│    token: string,
│    baseUrl: string
⋮
│  type Pinecone = {
│    apiKey: string,
│    environment: string
⋮
│  type Pinterest = {
│    token: string
⋮
│  type Pipedrive = {
│    apiToken: string
⋮
│  type Planetscale = {
│    serviceToken: string,
│    serviceTokenId: string
⋮
│  type Postgresql = {
│    host: string,
│    port: number,
│    user: string,
│    dbname: string,
│    sslmode: string,
│    password: string,
│    root_certificate_pem: string
⋮
│  type Pushover = {
│    user: string,
│    token: string
⋮
│  type Qovery = {
│    apiKey: string
⋮
│  type Quickbooks = {
│    token: string,
│    realmId: string,
│    isSandBox: boolean
⋮
│  type Readme = {
│    apiKey: string
⋮
│  type Recraft = {
│    apiKey: string
⋮
│  type Reddit = {
│    clientId: string,
│    password: string,
│    username: string,
│    userAgent: string,
│    clientSecret: string
⋮
│  type Render = {
│    apiKey: string
⋮
│  type Replicate = {
│    token: string
⋮
│  type Resend = {
│    token: string
⋮
│  type Rss = {
│    url: string
⋮
│  type S3 = {
│    port: number,
│    bucket: string,
│    region: string,
│    useSSL: boolean,
│    endPoint: string,
│    accessKey: string,
│    pathStyle: boolean,
│    secretKey: string
⋮
│  type S3AwsOidc = {
│    bucket: string,
│    region: string,
│    roleArn: string
⋮
│  type SageIntacct = {
│    token: string
⋮
│  type Salesflare = {
│    apiKey: string
⋮
│  type Segment = {
│    token: string,
│    baseUrl: string
⋮
│  type Sendgrid = {
│    token: string
⋮
│  type Sensortower = {
│    base_url: string,
│    auth_token: string
⋮
│  type Sentry = {
│    token: string,
│    region: string,
│    organizationSlug: string
⋮
│  type Shopify = {
│    token: string,
│    store_name: string
⋮
│  type Shutterstock = {
│    token: string
⋮
│  type SignatureAuth = {
│    secret_key: string,
│    signature_provider: string,
│    authentication_config: {
│    encoding: string,
│    algorithm: string,
│    signature_prefix: string,
│    signature_header_name: string
│  }
⋮
│  type Signoz = {
│    apiKey: string,
│    baseUrl: string
⋮
│  type Slack = {
│    token: string
⋮
│  type Smartsheet = {
│    token: string,
│    baseUrl: string
⋮
│  type Smtp = {
│    host: string,
│    port: number,
│    user: string,
│    password: string
⋮
│  type Snowflake = {
│    role: string,
│    schema: string,
│    database: string,
│    username: string,
│    warehouse: string,
│    public_key: string,
│    private_key: string,
│    account_identifier: string
⋮
│  type Speechify = {
│    token: string
⋮
│  type Spotify = {
│    token: string
⋮
│  type Square = {
│    token: string
⋮
│  type Stripe = {
│    token: string
⋮
│  type Supabase = {
│    key: string,
│    url: string
⋮
│  type Surrealdb = {
│    url: string,
│    token: string
⋮
│  type Taskade = {
│    token: string
⋮
│  type Telegram = {
│    token: string
⋮
│  type Telnyx = {
│    apiKey: string
⋮
│  type Terra = {
│    devId: string,
│    apiKey: string
⋮
│  type TheirStack = {
│    apiKey: string
⋮
│  type Todoist = {
│    token: string
⋮
│  type Togetherai = {
│    api_key: string,
│    base_url: string
⋮
│  type Toggl = {
│    token: string
⋮
│  type Tomorrow = {
│    apiKey: string
⋮
│  type Trello = {
│    key: string,
│    token: string
⋮
│  type Tripadvisor = {
│    apiKey: string
⋮
│  type Turso = {
│    apiToken: string
⋮
│  type Twilio = {
│    token: string,
│    accountSid: string
⋮
│  type TwilioMessageTemplate = {
│    auth_token: string,
│    recipients: string[],
│    account_sid: string,
│    content_sid: string,
│    origin_number: string,
│    message_service_sid: string
⋮
│  type Typeform = {
│    token: string,
│    baseUrl: string
⋮
│  type Ultravox = {
│    apiKey: string
⋮
│  type Vectara = {
│    apiKey: string
⋮
│  type Vercel = {
│    token: string
⋮
│  type Visma = {
│    token: string
⋮
│  type Weatherapi = {
│    apiKey: string
⋮
│  type Webflow = {
│    token: string
⋮
│  type Webscrapingai = {
│    apiKey: string
⋮
│  type Woocommerce = {
│    url: string,
│    version: string,
│    consumerKey: string,
│    consumerSecret: string,
│    queryStringAuth: boolean
⋮
│  type Xata = {
│    apiKey: string
⋮
│  type Xero = {
│    token: string
⋮
│  type Yelp = {
│    apiKey: string
⋮
│  type Ynab = {
│    token: string
⋮
│  type Zendesk = {
│    password: string,
│    username: string,
│    subdomain: string
⋮
│  type Zixflow = {
│    apiKey: string
⋮
│  type Zoho = {
│    token: string
⋮
│  type Zoom = {
│    accountId: string,
│    oauthClientId: string,
│    oauthClientSecret: string,
│    webhookSecretToken: string
⋮
│  type Zuplo = {
│    apiKey: string
⋮

apps\sift-api\tests\manual\test_agents.py:
⋮
│@pytest.fixture(autouse=True)
│def check_env():
⋮
│def test_windmill_full_configuration():
⋮
│def test_windmill_zero_config():
⋮
│def test_windmill_multimodal():
⋮
│def test_windmill_deep_merge():
⋮
│def test_windmill_async_webhook():
⋮

apps\sift-api\tests\manual\test_responses.py:
⋮
│@pytest.fixture(autouse=True)
│def check_env():
⋮
│@pytest.fixture(scope="module")
│def setup_test_agent():
⋮
│def test_windmill_simple_text(setup_test_agent):
⋮
│def test_windmill_conversational(setup_test_agent):
⋮
│def test_windmill_multimodal(setup_test_agent):
⋮
│def test_windmill_structured_json(setup_test_agent):
⋮
│def test_windmill_async_background(setup_test_agent):
⋮

packages\sift\src\sift\client.py:
⋮
│class SiftClient:
│    """Lightweight client facade for Sift API."""
│
│    def __init__(self, **kwargs: Any) -> None:
⋮
│    def get_agent(self, agent_name: str, version: Optional[int] = None) -> "Agent":
⋮
│    def save_agent(self, agent: "Agent") -> None:
⋮
│    def compile_and_save_agent(self, payload: Dict[str, Any]) -> None:
⋮
│    def predict_response(
│        self,
│        agent_id: str,
│        input: Union[str, List[Dict[str, Any]]],
│        background: bool = False,
│        **kwargs: Any
⋮

packages\sift\src\sift\config.py:
⋮
│class Settings(LoggingSettings, BaseSettings):
⋮

packages\sift\src\sift\integrations\langfuse\service.py:
⋮
│def get_langfuse_client() -> Langfuse:
⋮

packages\sift\src\sift\modules\agents\repository\langfuse.py:
⋮
│def get_agent(agent_name: str, version: Optional[int] = None) -> Agent:
⋮
│def get_agent_safe(agent_name: str, version: Optional[int] = None) -> Optional[Agent]:
⋮
│def save_agent(agent: Agent) -> None:
⋮

packages\sift\src\sift\modules\agents\schema.py:
⋮
│class DSPySignatureState(BaseModel):
⋮
│class DSPyTrainingExample(BaseModel):
⋮
│class DSPyPredictorState(BaseModel):
⋮
│class DSPyParams(BaseModel):
⋮
│class Agent(BaseModel):
⋮
│class AgentRequest(Agent):
⋮
│class AgentResponse(LiteLLMAgentResponse):
⋮
│class AgentpredictRequest(BaseModel):
⋮

packages\sift\src\sift\modules\agents\service.py:
⋮
│def _hydrate_multimodal_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
⋮
│class LlmAsAJudge(dspy.Signature):
⋮
│def dynamic_api_metric(example: dspy.Example, pred: dspy.Prediction, trace: Optional[Any] = None) -
⋮
│class AgentModule(dspy.Module):
│    def __init__(self, state_dict: Dict[str, Any]):
│        super().__init__()
│        for key, pred_state in state_dict.items():
│            if not isinstance(pred_state, dict):
│                continue
│
│            sig_state = pred_state.get("signature", {})
│            instructions = sig_state.get("instructions", "")
│            fields = sig_state.get("fields", [])
│
⋮
│    def load_state(self, state: Dict[str, Any], allow_unsafe_lm_state: bool = False, **kwargs: Any)
⋮
│    def forward(self, **kwargs):
⋮
│def compile_and_save_agent(payload: Dict[str, Any]) -> None:
⋮

packages\sift\src\sift\modules\responses\schema.py:
⋮
│class ResponseRequest(BaseModel):
⋮
│class ResponseResponse(ResponsesAPIResponse):
⋮

packages\sift\src\sift\modules\responses\service.py:
⋮
│def predict_response(request: ResponseRequest) -> ResponsesAPIResponse:
⋮

packages\sift\src\sift\use_cases\agents\service.py:
⋮
│def _deep_merge(base: Dict, update: Dict) -> Dict:
⋮
│@webhook_dispatch(event_prefix="agent")
│def main(
│    agent_name: Optional[str] = None,
│    agent_card_params: Optional[Dict] = None,
│    litellm_params: Optional[Dict] = None,
│    dspy_params: Optional[Dict] = None,
│    object_permission: Optional[Dict] = None,
│    labels: Optional[List] = None,
│    webhook: Optional[Dict] = None,
⋮

packages\sift\src\sift\use_cases\responses\service.py:
⋮
│@webhook_dispatch(event_prefix="response")
│def main(
│    model: str,
│    input: Union[str, List[Dict]],
│    background: bool = False,
│    webhook: Optional[Dict] = None,
│    **kwargs: Any
⋮

packages\sift\src\sift\utils\webhook\schema.py:
⋮
│class WebhookEvent(str, Enum):
⋮
│class WebhookRequest(BaseModel):
⋮
│class WebhookResponse(BaseModel):
⋮

packages\sift\src\sift\utils\webhook\service.py:
⋮
│def dispatch_webhook(
│    webhook: Optional[WebhookRequest], payload: WebhookResponse
⋮
│def webhook_dispatch(event_prefix: str = "") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
│    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED)."""
│
│    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
│        @functools.wraps(func)
│        def wrapper(*args: Any, **kwargs: Any) -> Any:
│            sig = inspect.signature(func)
│            bound_args = sig.bind(*args, **kwargs)
│            bound_args.apply_defaults()
│            
│            webhook_data = bound_args.arguments.get("webhook")
│            webhook = None
│            if isinstance(webhook_data, dict):
│                webhook = WebhookRequest(**webhook_data)
⋮

packages\sift\tests\conftest.py:
⋮
│def filter_response(response):
⋮
│def _get_vcr_config():
⋮
│@pytest.fixture(scope="module")
│def vcr_config():
⋮
│def _setup_environment():
⋮
│@pytest.fixture(scope="session", autouse=True)
│def setup_environment():
⋮

packages\sift\tests\integration\external\test_agents.py:
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_full_configuration():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_zero_config_auto_inference():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_multimodal_vision_training():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_update_agent_deep_merge():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_async_compilation_with_webhook():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_windmill_sparse_payload_compilation():
⋮
│def test_completely_empty_payload():
⋮
│def test_explicit_null_overrides():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_multiple_custom_predictor_states():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_partial_nested_missing_fields():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_non_destructive_partial_updates():
⋮

packages\sift\tests\integration\external\test_responses.py:
⋮
│@pytest.fixture(scope="module")
│def setup_test_agent():
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_simple_text_input(setup_test_agent):
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_conversational_messages_array_input(setup_test_agent):
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_multimodal_vision_input(setup_test_agent):
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_structured_json_schema_output(setup_test_agent):
⋮
│@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
│def test_async_background_request(setup_test_agent):
⋮

packages\sift\tests\integration\internal\test_hydration.py:
⋮
│def test_end_to_end_hydration(mocker):
⋮
│def test_end_to_end_hydration_multimodal(mocker):
⋮

packages\sift\tests\integration\use_cases\test_agents_integration.py:
⋮
│@patch("dspy.teleprompt.BootstrapFewShot")
│@patch("sift.modules.agents.repository.langfuse.get_langfuse_client")
│def test_full_optimization_flow_existing_agent(mock_get_langfuse_client, mock_bootstrap):
⋮
│@patch("dspy.LM")
⋮
│def test_full_compilation_loop_with_llm_judge(mock_get_langfuse_client, mock_bootstrap, mock_lm):
⋮
│@patch("dspy.teleprompt.BootstrapFewShot")
│@patch("sift.modules.agents.repository.langfuse.get_langfuse_client")
│def test_implicit_vs_explicit_param_merging_integration(mock_get_langfuse_client, mock_bootstrap):
⋮

packages\sift\tests\integration\use_cases\test_responses_integration.py:
⋮
│@patch("sift.modules.responses.service.get_agent")
│def test_responses_main_structured_format_integration(mock_get_agent):
⋮

packages\sift\tests\unit\sift\integrations\langfuse\test_service.py:
⋮
│def test_get_langfuse_client_singleton():
⋮

packages\sift\tests\unit\sift\modules\agents\repository\test_langfuse.py:
⋮
│@pytest.fixture
│def mock_langfuse_client(mocker):
⋮
│def test_save_agent_instruction_extraction(mock_langfuse_client):
⋮
│def test_save_agent_empty_state(mock_langfuse_client):
⋮
│def test_get_agent_reads_from_config(mock_langfuse_client):
⋮
│def test_get_agent_defaults_agent_name(mock_langfuse_client):
⋮
│def test_legacy_config_parsing(mock_langfuse_client):
⋮
│def test_get_agent_safe_returns_agent(mock_langfuse_client):
⋮
│def test_get_agent_safe_returns_none_on_exception(mock_langfuse_client):
⋮

packages\sift\tests\unit\sift\modules\agents\test_schema.py:
⋮
│def test_dspy_training_example_valid_schema():
⋮
│def test_dspy_training_example_missing_extras():
⋮
│def test_dspy_training_example_messages():
⋮
│def test_dspy_training_example_string_messages_and_structured_response():
⋮
│def test_agent_name_auto_generation():
⋮
│def test_agent_sparse_parsing():
⋮
│def test_dspy_predictor_state_sparse_parsing():
⋮

packages\sift\tests\unit\sift\modules\agents\test_service.py:
⋮
│def _create_payload(trainset_size: int, optimizer: str | None = None) -> dict:
⋮
│def _mock_compiled_module():
⋮
│@patch("sift.modules.agents.repository.langfuse.save_agent")
│@patch("dspy.teleprompt.BootstrapFewShot")
│def test_implicit_mode_tiny_dataset(mock_optimizer_class, mock_save_agent):
⋮
│@patch("sift.modules.agents.repository.langfuse.save_agent")
│@patch("dspy.teleprompt.BootstrapFewShotWithRandomSearch")
│def test_implicit_mode_medium_dataset(mock_optimizer_class, mock_save_agent):
⋮
│@patch("sift.modules.agents.repository.langfuse.save_agent")
│@patch("dspy.teleprompt.MIPROv2")
│def test_implicit_mode_large_dataset(mock_optimizer_class, mock_save_agent):
⋮
│@patch("sift.modules.agents.repository.langfuse.save_agent")
│@patch("dspy.teleprompt.COPRO")
│def test_explicit_optimizer_mode_override(mock_optimizer_class, mock_save_agent):
⋮
│def test_hydrate_multimodal_messages_missing_url():
⋮

packages\sift\tests\unit\sift\modules\responses\test_schema.py:
⋮
│def test_response_request_allows_litellm_fields():
⋮
│def test_response_request_extra_fields():
⋮

packages\sift\tests\unit\sift\modules\responses\test_service.py:
⋮
│@patch("sift.modules.responses.service.get_agent")
│@patch("dspy.LM")
│def test_predict_response_multimodal_passthrough(mock_lm, mock_get_agent):
⋮
│@patch("sift.modules.responses.service.get_agent")
│@patch("dspy.LM")
│def test_predict_response_structured_responses_and_kwargs(mock_lm, mock_get_agent):
⋮
│@patch("sift.modules.responses.service.get_agent")
│@patch("dspy.LM")
│def test_predict_response_no_predictors(mock_lm, mock_get_agent):
⋮
│@patch("sift.modules.responses.service.get_agent")
│@patch("dspy.LM")
│def test_predict_response_no_input_fields_and_dict_fields(mock_lm, mock_get_agent):
│    from sift.modules.responses.schema import ResponseRequest
│    
⋮
│    class DummyModuleWithState:
│        captured_kwargs = {}
│        def __init__(self, raw_state):
⋮
│        def load_state(self, state):
│            pass
│        def __call__(self, **kwargs):
⋮

packages\sift\tests\unit\sift\test_client.py:
⋮
│def test_sift_client_initialization_overrides_settings() -> None:
⋮
│def test_sift_client_routing_properties(mocker) -> None:
⋮
│def test_sift_client_save_agent(mocker) -> None:
⋮

packages\sift\tests\unit\sift\test_config.py:
⋮
│def test_settings_default_dspy_cachedir():
⋮
│def test_settings_propagates_dspy_cachedir():
⋮
│def test_settings_propagates_default_to_environ():
⋮

packages\sift\tests\unit\sift\test_conftest.py:
⋮
│def test_filter_response():
⋮
│def test_vcr_config():
⋮
│@patch("dotenv.load_dotenv", autospec=True)
│@patch.dict(os.environ, clear=True)
│def test_setup_environment_sets_dummies(mock_load_dotenv):
⋮
│@patch("dotenv.load_dotenv", autospec=True)
⋮
│def test_setup_environment_preserves_existing(mock_load_dotenv):
⋮

packages\sift\tests\unit\sift\test_init.py:
⋮
│def test_public_api_exports():
⋮

packages\sift\tests\unit\sift\use_cases\test_agents.py:
⋮
│def test_deep_merge():
⋮
│@patch("sift.use_cases.agents.service.client")
│@patch("sift.use_cases.agents.service.get_agent_safe")
│def test_agents_new_agent(mock_get_agent_safe, mock_client):
⋮
│@patch("sift.use_cases.agents.service.client")
│@patch("sift.use_cases.agents.service.get_agent_safe")
│def test_agents_existing_agent_merge(mock_get_agent_safe, mock_client):
⋮
│@patch("sift.use_cases.agents.service.client")
⋮
│def test_agents_main_optional_args_populated(mock_dispatch_webhook, mock_get_agent_safe, mock_clien
⋮
│@patch("sift.use_cases.agents.service.client")
⋮
│def test_agents_main_catches_exception(mock_dispatch_webhook, mock_get_agent_safe, mock_client):
⋮

packages\sift\tests\unit\sift\use_cases\test_responses.py:
⋮
│@patch("sift.use_cases.responses.service.client")
│def test_responses_main_extracts_agent_name(mock_client):
⋮
│@patch("sift.use_cases.responses.service.client")
│@patch("sift.utils.webhook.service.dispatch_webhook")
│def test_responses_main_catches_exception(mock_dispatch_webhook, mock_client):
⋮

packages\sift\tests\unit\sift\utils\webhook\test_service.py:
⋮
│@pytest.fixture
│def webhook():
⋮
│def test_dispatch_webhook_success(webhook):
⋮
│def test_dispatch_webhook_no_webhook():
⋮
│def test_dispatch_webhook_http_error(webhook, caplog):
⋮
│class MockResponse:
│    def __init__(self, success=True, data="resp_data"):
│        self.success = success
⋮
│    def model_dump(self):
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_success_func(data: str, webhook: Optional[dict] = None):
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_failure_func(data: str, webhook: Optional[dict] = None):
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_exception_func(data: str, webhook: Optional[dict] = None):
⋮
│@patch("uuid.uuid4")
│@patch("os.getenv")
│def test_webhook_dispatch_success(mock_getenv, mock_uuid4, webhook):
⋮
│@patch("uuid.uuid4")
│@patch("os.getenv")
│def test_webhook_dispatch_handled_failure(mock_getenv, mock_uuid4, webhook):
⋮
│@patch("uuid.uuid4")
│@patch("os.getenv")
│def test_webhook_dispatch_unhandled_exception(mock_getenv, mock_uuid4, webhook):
⋮
│def test_webhook_dispatch_no_webhook():
⋮
│def test_webhook_dispatch_webhook_object(webhook):
⋮
│class MockResponseWithOutput:
│    def __init__(self, success=True, output=[{"result": "ok"}]):
│        self.success = success
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_output_func(data: str, webhook: Optional[dict] = None):
⋮
│def test_webhook_dispatch_with_output(webhook):
⋮
```