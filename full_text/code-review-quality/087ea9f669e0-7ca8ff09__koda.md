---
name: koda
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging koda. Use this skill whenever modifying koda configurations or adding related functionality.
---
# koda

## File Tree

```text
koda/
├── assets
├── modules
│   └── koda (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/koda`

```python
apps\koda-api\f\koda\batch_scrape.py:
⋮
│def main(
│    urls: List[str] = [],
│    requests: List[ScrapeRequest] = [],
│    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
│    onlyMainContent: bool = True,
│    actions: List[Action] = [],
│    timeout: int = 60000,
│    s3_resource: Optional[str] = "f/koda/default_s3",
│    webhook: Optional[Webhook] = None,
│    maxConcurrency: int = 10,
⋮

apps\koda-api\f\koda\crawl.py:
⋮
│def main(
│    url: str,
│    prompt: Optional[str] = None,
│    excludePaths: Optional[List[str]] = None,
│    includePaths: Optional[List[str]] = None,
│    maxDiscoveryDepth: int = 0,
│    sitemap: str = "include",
│    ignoreQueryParameters: bool = False,
│    regexOnFullURL: bool = False,
│    limit: int = 10000,
⋮

apps\koda-api\f\koda\scouts\scrape_youtube_profile.py:
⋮
│def main(
│    url: str,
│    formats: List[Union[str, Dict[str, Any]]] = ["screenshot"],
│    timeout: int = 600000,
│    webhook: Optional[Webhook] = None,
│    max_concurrency: int = 1,
⋮

apps\koda-api\f\koda\scrape.py:
⋮
│def main(
│    url: str,
│    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
│    onlyMainContent: bool = True,
│    actions: List[Action] = [],
│    timeout: int = 60000,
│    s3_resource: Optional[str] = "f/koda/default_s3",
│    webhook: Optional[Webhook] = None,
⋮

apps\koda-api\rt.d.ts:
⋮
│  type Abstractapi = {
│    apiKey: string
⋮
│  type Acumbamail = {
│    authToken: string
⋮
│  type AeroWorkflow = {
│    apiKey: string
⋮
│  type AgentInstructions = any
│
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
│  type Assemblyai = {
│    apiKey: string
⋮
│  type AwsBedrock = {
│    apiKey: string,
│    region: string,
│    awsAccessKeyId: string,
│    awsSessionToken: string,
│    awsSecretAccessKey: string
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
│  type Buttondown = {
│    token: string
⋮
│  type Cacertificate = {
│    certificate: string
⋮
│  type Calendly = {
│    token: string
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
│  type Clickhouse = {
│    host: string,
│    password: string,
│    username: string
⋮
│  type Cloudflare = {
│    key: string,
│    email: string,
│    token: string
⋮
│  type Cockroachdb = {
│    token: string
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
│  type DeepInfra = {
│    token: string
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
│  type Dynatrace = {
│    accessToken: string,
│    environmentId: string,
│    environmentUrl: string
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
│  type Ghostcms = {
│    apiKey: string,
│    apiUrl: string
⋮
│  type GitRepository = {
│    url: string,
│    branch: string,
│    folder: string,
│    gpg_key: any,
│    is_github_app: boolean
⋮
│  type Googleai = {
│    api_key: string,
│    base_url: string
⋮
│  type Gworkspace = {
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
│  type JsonSchema = {
│    schema: any
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
│  type Leonardoai = {
│    apiKey: string
⋮
│  type Linkding = {
│    token: string,
│    baseUrl: string
⋮
│  type Linkedin = {
│    token: string
⋮
│  type Localcontexts = {
│    api_key: string,
│    project_id: string,
│    server_url: string
⋮
│  type Mailchimp = {
│    server: string,
│    api_key: string
⋮
│  type Mailerlite = {
│    apiToken: string
⋮
│  type Mastodon = {
│    token: string,
│    baseUrl: string
⋮
│  type Matteroom = {
│    base_url: string,
│    password: string,
│    username: string
⋮
│  type Meteosource = {
│    tier: string,
│    apiKey: string
⋮
│  type MongodbRest = {
│    api_key: string,
│    endpoint: string
⋮
│  type Motimate = {
│    token: string
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
│  type Nextcloud = {
│    token: string,
│    userId: string,
│    baseUrl: string,
│    password: string,
│    username: string
⋮
│  type OauthClientCredentials = {
│    domain: string,
│    client_id: string,
│    client_secret: string
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
│  type Paylocity = {
│    token: string
⋮
│  type Personio = {
│    clientId: string,
│    clientSecret: string
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
│  type Quickbooks = {
│    token: string,
│    realmId: string,
│    isSandBox: boolean
⋮
│  type Replicate = {
│    token: string
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
│  type Sendgrid = {
│    token: string
⋮
│  type Sensortower = {
│    base_url: string,
│    auth_token: string
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
│  type Smartsheet = {
│    token: string,
│    baseUrl: string
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
│  type Supabase = {
│    key: string,
│    url: string
⋮
│  type Surrealdb = {
│    url: string,
│    token: string
⋮
│  type Telegram = {
│    token: string
⋮
│  type TheirStack = {
│    apiKey: string
⋮
│  type Togetherai = {
│    api_key: string,
│    base_url: string
⋮
│  type Tomorrow = {
│    apiKey: string
⋮
│  type Tripadvisor = {
│    apiKey: string
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
│  type Weatherapi = {
│    apiKey: string
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

packages\koda\src\koda\assets\posthog-monolith.js:
│!function(){"use strict";function t(t,e,i,r,n,s,o){try{var a=t[s](o),l=a.value}catch(t){return void
⋮

packages\koda\src\koda\client.py:
⋮
│class KodaClient:
│    """Primary interface for the Koda extraction infrastructure."""
│    
│    def __init__(self, s3_resource: dict | Any | None = None, **kwargs: Any) -> None:
⋮
│    async def __aenter__(self) -> KodaClient:
⋮
│    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
⋮

packages\koda\src\koda\config\main.py:
⋮
│class S3(BaseModel):
│    endpoint_url: Optional[str] = Field(default=None, validation_alias=AliasChoices("endpoint_url",
⋮
│    @classmethod
│    def from_dict(cls, data: dict) -> Optional["S3"]:
⋮
│class Settings(LoggingSettings, BaseSettings):
│    """
│    Centralized configuration for Koda.
│    Loads values from environment variables with sensible defaults.
⋮
│    @model_validator(mode="after")
│    def validate_browser(self) -> "Settings":
⋮

packages\koda\src\koda\exceptions.py:
⋮
│class Error(Exception):
⋮
│class ScrapeError(Error):
⋮
│class SessionExhaustedError(Error):
⋮
│class TimeoutError(Error):
⋮
│class BrowserLaunchError(Error):
⋮

packages\koda\src\koda\infrastructure\invisible_playwright.py:
⋮
│class BrowserLaunchError(Exception):
⋮
│async def launch_stealth_browser(headless: bool = True, **kwargs: Any) -> BrowserContext:
⋮
│async def stop_stealth_browser() -> None:
⋮

packages\koda\src\koda\infrastructure\pytest.py:
⋮
│def main():
│    """
│    Wrapper around pytest to run tests sequentially in completely isolated processes.
│    This prevents memory leaks and orphaned browser processes from accumulating.
│    It perfectly mimics the original pytest stdout.
⋮
│    def run_and_stream_test(cmd, test_id, current_idx):
⋮

packages\koda\src\koda\integrations\crawl4ai.py:
⋮
│class KodaBrowserManager(BrowserManager):
│    """
│    A custom BrowserManager for crawl4ai that bypasses its internal lifecycle management.
│    It creates new pages from the Playwright BrowserContext provided by Koda.
│    """
│    def __init__(self, context: BrowserContext, *args, **kwargs):
⋮
│    async def start(self):
⋮
│    async def close(self):
⋮
│    async def get_page(self, crawlerRunConfig: CrawlerRunConfig):
⋮
│class KodaAsyncWebCrawler(AsyncWebCrawler):
│    """
│    A custom AsyncWebCrawler that intercepts initialization to route browser
│    management through Koda's infrastructure if a `client` is provided.
│    """
│    def __init__(self, **kwargs):
⋮
│    async def start(self) -> "KodaAsyncWebCrawler":
⋮
│    async def close(self):
⋮
│    async def __aenter__(self):
⋮
│    async def __aexit__(self, exc_type, exc_val, exc_tb):
⋮
│class Crawl4AiTool(BrowserTool):
│    """
│    Adapter for crawl4ai that implements the BrowserTool protocol.
│    DEPRECATED: Use the native KodaAsyncWebCrawler wrapper instead.
│    """
│    def __init__(self, browser_config: Optional[BrowserConfig] = None):
⋮
│    async def execute(self, context_or_page: Any, request: Any) -> Any:
⋮

packages\koda\src\koda\integrations\crawlee.py:
⋮
│class KodaBrowserController(BrowserController):
│    """A browser controller that simply yields pages from a pre-existing Koda BrowserContext."""
│    
⋮
│    def __init__(self, context: BrowserContext):
⋮
│    async def new_page(
│        self,
│        browser_new_context_options: Mapping[str, Any] | None = None,
│        proxy_info: ProxyInfo | None = None,
⋮
│    async def close(self, *, force: bool = False) -> None:
⋮
│class KodaBrowserPlugin(BrowserPlugin):
│    """A browser plugin that returns a KodaBrowserController wrapped around a pre-existing Koda con
│    
⋮
│    def __init__(self, context: BrowserContext):
⋮
│    @property
│    def active(self) -> bool:
⋮
│    async def __aenter__(self) -> 'KodaBrowserPlugin':
⋮
│    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None
⋮
│    async def new_browser(self) -> BrowserController:
⋮
│class KodaPlaywrightCrawler(PlaywrightCrawler):
│    """
│    A Koda-integrated PlaywrightCrawler that injects the KodaClient and
│    wraps the entire crawl execution within Koda's BrowserSession.
│    """
│    def __init__(self, *args, **kwargs):
⋮
│    async def run(self, *args, **kwargs) -> None:  # type: ignore[override]
⋮

packages\koda\src\koda\integrations\posthog.py:
⋮
│def _get_otel_trace_id() -> str:
⋮
│async def flush_telemetry() -> None:
⋮
│async def _send_posthog_request(url: str, method: str, data: str, content_type: Optional[str] = Non
⋮
│async def setup_playwright_transport(context: BrowserContext) -> None:
⋮
│async def setup_network_capture(page: Page, posthog_api_key: str) -> None:
⋮
│async def inject_posthog_monolith(page: Page, api_key: str, host: str) -> None:
⋮

packages\koda\src\koda\integrations\stagehand.py:
⋮
│class KodaStagehand(BaseStagehand):  # type: ignore[misc]
│    """
│    A custom Stagehand wrapper that routes browser management through Koda's
│    infrastructure if a `client` is provided.
│    """
│    def __init__(self, **kwargs):
⋮
│    async def init(self, *args, **kwargs):
⋮
│    async def close(self, *args, **kwargs):
⋮
│class StagehandTool(BrowserTool):
│    """
│    Adapter for stagehand that implements the BrowserTool protocol.
│    DEPRECATED: Use the native KodaStagehand wrapper instead.
│    """
│    def __init__(self, **kwargs):
⋮
│    async def execute(self, context_or_page: Any, request: Any) -> Any:
⋮

packages\koda\src\koda\modules\browser\repositories\cloakbrowser.py:
⋮
│@asynccontextmanager
│async def launch(user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
⋮

packages\koda\src\koda\modules\browser\repositories\invisible_playwright.py:
⋮
│if InvisiblePlaywright is not None:
│    class KodaInvisiblePlaywright(InvisiblePlaywright):
│        def _default_context_kwargs(self) -> Dict[str, Any]:
│            kwargs = super()._default_context_kwargs()
│            # Force Playwright's native CSP bypass on the persistent context
│            kwargs["bypass_csp"] = True
⋮
│@asynccontextmanager
│async def launch(user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
⋮

packages\koda\src\koda\modules\browser\service.py:
⋮
│class BrowserTool(Protocol):
│    """Protocol for tools that operate on a Playwright Page or Context."""
│    async def execute(self, context_or_page: Any, request: Any) -> Any:
⋮
│async def _strip_csp_headers(route: Route):
⋮
│@dataclass(frozen=True)
│class CSPStrategy:
⋮
│async def _native_playwright_interceptor(context: BrowserContext) -> None:
⋮
│def _invisible_playwright_modifier(config: dict) -> dict:
⋮
│@asynccontextmanager
│async def BrowserSession(config: Optional[Dict[str, Any]] = None, user_data_dir: str = "") -> Async
│    """
│    Context manager that owns the browser lifecycle.
│    Launches the browser, injects telemetry into all pages, and ensures safe teardown.
⋮
│    async with launcher(user_data_dir, config) as browser_or_context:
│            # Handle both Browser and persistent BrowserContext yields
│            if hasattr(browser_or_context, 'new_context'):
│                kwargs = {"permissions": ["geolocation", "notifications"]}
│                kwargs.update(strategy.context_kwargs)
│                context = await browser_or_context.new_context(**kwargs)
│            else:
│                context = browser_or_context
│                await context.grant_permissions(["geolocation", "notifications"])
│                # Note: strategy.context_kwargs cannot be passed to a persistent context natively.
│                # CSP bypassing relies on extra_prefs (e.g. security.csp.enable=False)
⋮
│            if settings.posthog_api_key and settings.posthog_host:
│                await setup_playwright_transport(context)
│                
│                async def on_page(page: Page):
⋮

packages\koda\src\koda\modules\cache\repositories\windmill.py:
⋮
│def _get_state_path() -> str:
⋮
│async def _fetch_state() -> Dict[str, Any]:
⋮
│async def get(key: str) -> Optional[CacheEntry]:
⋮
│async def set(entry: CacheEntry) -> None:
⋮

packages\koda\src\koda\modules\cache\schema.py:
⋮
│class CacheEntry(BaseModel):
⋮

packages\koda\src\koda\modules\cache\service.py:
⋮
│class CacheService:
│    """Service for managing cache operations."""
│
│    def __init__(self, cache_repo: Any):
⋮
│    async def get(self, key: str) -> Optional[Any]:
⋮
│    async def set(self, key: str, value: Any) -> None:
⋮

packages\koda\src\koda\modules\session\repositories\email\imap.py:
⋮
│async def get_latest_email(address: str) -> Optional[str]:
⋮

packages\koda\src\koda\modules\session\repositories\email\jmap.py:
⋮
│async def get_latest_email(address: str) -> Optional[str]:
⋮

packages\koda\src\koda\modules\session\repositories\lock\consul.py:
⋮
│async def acquire_lock(
│    lock_name: str,
│    ttl_seconds: int = 30,
│    timeout_seconds: int = 10,
⋮
│async def release_lock(lock_name: str, session_id: str) -> bool:
⋮
│def start_heartbeat(session_id: str, interval_seconds: int = 15) -> asyncio.Task:
⋮
│async def _renew_session_loop(session_id: str, interval_seconds: int) -> None:
⋮

packages\koda\src\koda\modules\session\repositories\lock\redis.py:
⋮
│def _get_client() -> Redis:
⋮
│async def acquire_lock(
│    lock_name: str,
│    ttl_seconds: int = 30,
│    timeout_seconds: int = 10,
⋮
│async def release_lock(lock_name: str, token: str) -> bool:
⋮
│def start_heartbeat(lock_name: str, token: str, ttl_seconds: int = 30) -> asyncio.Task:
⋮
│async def _renew_lock_loop(lock_name: str, token: str, ttl_seconds: int) -> None:
⋮

packages\koda\src\koda\modules\session\schema.py:
⋮
│class BrowserParam(BaseModel):
⋮
│class MFAParam(BaseModel):
⋮
│class UserDataParam(BaseModel):
⋮
│class SessionModel(BaseModel):
⋮
│@dataclass
│class Session:
│    """
│    A lightweight wrapper around SessionModel providing an Apify-style API.
│    Delegates I/O and orchestration to service functions.
⋮
│    @property
│    def id(self) -> str:
⋮
│    @property
│    def user_data(self) -> UserDataParam:
⋮
│    @property
│    def error_score(self) -> float:
⋮
│    @property
│    def usage_count(self) -> int:
⋮
│    @property
│    def expires_at(self) -> datetime:
⋮
│    @property
│    def is_blocked(self) -> bool:
⋮
│    @property
│    def is_expired(self) -> bool:
⋮
│    @property
│    def is_max_usage_count_reached(self) -> bool:
⋮
│    @property
│    def is_usable(self) -> bool:
⋮
│    def mark_good(self) -> None:
⋮
│    def mark_bad(self) -> None:
⋮
│    def retire(self) -> None:
⋮
│    def is_blocked_status_code(self, status_code: int) -> bool:
⋮
│    def get_state(self, as_dict: bool = False) -> SessionModel | dict:
⋮
│    @classmethod
│    def from_model(cls, model: SessionModel) -> Session:
⋮

packages\koda\src\koda\modules\session\service.py:
⋮
│class SessionService:
│    """Service for managing browser sessions, including locking, storage, and MFA resolution."""
│
│    def __init__(
│        self,
│        storage_repo: Any,
│        lock_repo: Any,
│        email_repo_imap: Any,
│        email_repo_jmap: Any,
│        s3_repo: Any,
⋮
│    async def get_session(self, metadata: dict[str, Any]) -> Tuple[Session, str]:
⋮
│    async def release_session(self, session: Session, lock_token: str) -> None:
⋮
│    @asynccontextmanager
│    async def browser_session_scope(self, metadata: dict[str, Any]) -> AsyncGenerator[Tuple[Session
⋮
│    async def resolve_mfa(self, session: Session) -> str:
⋮

packages\koda\src\koda\use_cases\batch_scrape\schema.py:
⋮
│class BatchScrapeRequest(BaseModel):
⋮
│class BatchScrapeResponse(BaseModel):
⋮

packages\koda\src\koda\use_cases\batch_scrape\service.py:
⋮
│class BatchScrapeJob:
│    def __init__(self, request: BatchScrapeRequest):
│        self.request = request
│        self.action_results: Dict[str, Dict[str, list]] = {}
│        self.target_requests: Dict[str, ScrapeRequest] = {}
│        if self.request.requests:
│            for req in self.request.requests:
⋮
│    def _init_url_action_results(self, url: str):
⋮
│    async def execute_actions_hook(self, page, context, **kwargs):
⋮
│    async def run(self) -> BatchScrapeResponse:
⋮
│@webhook_dispatch
│async def batch_scrape(request: BatchScrapeRequest) -> BatchScrapeResponse:
⋮

packages\koda\src\koda\use_cases\crawl\schema.py:
⋮
│class ScrapeOptions(BaseModel):
⋮
│class CrawlRequest(BaseModel):
⋮
│class CrawlResponse(BaseModel):
⋮

packages\koda\src\koda\use_cases\crawl\service.py:
⋮
│class CrawlJob:
│    def __init__(self, request: CrawlRequest):
│        self.request = request
│        self.base_url = str(request.url)
⋮
│    async def execute_actions_hook(self, page, context, **kwargs):
⋮
│    async def run(self) -> CrawlResponse:
⋮
│@webhook_dispatch
│async def crawl(request: CrawlRequest) -> CrawlResponse:
⋮

packages\koda\src\koda\use_cases\schema.py:
⋮
│class Action(BaseModel):
⋮

packages\koda\src\koda\use_cases\scrape\schema.py:
⋮
│class ScrapeRequest(BaseModel):
⋮
│class ScrapeResponse(BaseModel):
⋮
│class ScrapeResult(BaseModel):
⋮

packages\koda\src\koda\use_cases\scrape\service.py:
⋮
│class ScrapeJob:
│    def __init__(self, request: ScrapeRequest):
│        self.request = request
│        self.action_results: Dict[str, list] = {
│            "screenshots": [],
│            "scrapes": [],
│            "javascriptReturns": [],
│            "pdfs": [],
│            "errors": [],
⋮
│    async def execute_actions_hook(self, page, context, **kwargs):
⋮
│    async def run(self) -> ScrapeResponse:
⋮
│@webhook_dispatch
│async def scrape(request: ScrapeRequest) -> ScrapeResult:
⋮

packages\koda\src\koda\use_cases\scrape_youtube_profile\recording.py:
⋮
│def run(playwright: Playwright) -> None:
│    browser = playwright.chromium.launch(headless=False)
⋮
│    def _wait_for_network():
⋮

packages\koda\src\koda\use_cases\scrape_youtube_profile\schema.py:
⋮
│class ScrapeYoutubeProfileRequest(BaseModel):
⋮
│class ScrapeYoutubeProfileResponse(BaseModel):
⋮

packages\koda\src\koda\use_cases\scrape_youtube_profile\service.py:
⋮
│async def _push_screenshot_data(
│    context: PlaywrightCrawlingContext, url: str, screenshot_bytes: bytes | str
⋮
│async def _validate_redirect(page: Page, expected_slug: str | None) -> bool:
⋮
│@router.handler("TAB")
│async def tab_handler(context: PlaywrightCrawlingContext) -> None:
⋮
│@webhook_dispatch
│async def scrape_youtube_profile(
│    request: ScrapeYoutubeProfileRequest,
⋮

packages\koda\src\koda\use_cases\service.py:
⋮
│async def wait_for_networkidle(
│    page: Page, wait_for_timeout: int = 1000, timeout_ms: int = 10000
⋮
│async def scroll_to(
│    page: Page,
│    y: Optional[int] = None,
│    viewport_height: int = 768,
│    wait_callback: Optional[Callable[[], Awaitable[None]]] = None,
⋮
│async def screenshot(page: Page, max_height: int = 3072) -> bytes:
⋮
│async def execute_actions(
│    page, actions: List[Action], action_results: Dict[str, list]
⋮

packages\koda\src\koda\utils\__init__.py:
⋮
│def images_are_identical(img1: Image.Image, img2: Image.Image) -> bool:
⋮
│def sanitize_filename(url: str) -> str:
⋮

packages\koda\src\koda\utils\file\main.py:
⋮
│class File:
│    """
│    A wrapper around a local temporary file, with a mandatory filename and mimetype.
│    Supports lazy uploading to S3 to generate a presigned URL.
│    """
│    def __init__(self, path: str, filename: str, mimetype: str, url: Optional[str] = None):
⋮
│    def __enter__(self) -> "File":
⋮
│    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
⋮
│    def cleanup(self) -> None:
⋮
│    @property
│    def bytes(self) -> bytes:
⋮
│    @property
│    def base64(self) -> str:
⋮
│    @property
│    def presigned_url(self) -> Optional[str]:
⋮
│    def to_playwright_input(self) -> dict:
⋮
│    @classmethod
│    def _get_temp_path(cls, filename: str) -> str:
⋮
│    @classmethod
│    def create_empty(cls, filename: str, mimetype: Optional[str] = None, touch: bool = False) -> "F
⋮
│    @classmethod
│    def from_bytes(cls, data: bytes, filename: str, mimetype: Optional[str] = None) -> "File":
⋮
│    @classmethod
│    def from_base64(cls, base64_string: str, filename: str, mimetype: Optional[str] = None) -> "Fil
⋮
│    @classmethod
│    def from_url(cls, url: str, filename: Optional[str] = None, mimetype: Optional[str] = None) -> 
⋮
│    @classmethod
│    def from_path(cls, source_path: str, filename: Optional[str] = None) -> "File":
⋮
│    @classmethod
│    async def from_playwright_download(cls, download: any, filename: Optional[str] = None) -> "File
⋮

packages\koda\src\koda\utils\file\service.py:
⋮
│def upload(data: Union[bytes, str], object_name: str, mimetype: str) -> None:
⋮
│def generate_presigned_url(object_name: str, expires_in: int = 3600) -> str:
⋮
│def _get_client():
⋮

packages\koda\src\koda\utils\webhook\schema.py:
⋮
│class WebhookEvent(str, Enum):
⋮
│class Webhook(BaseModel):
⋮

packages\koda\src\koda\utils\webhook\service.py:
⋮
│def _serialize_files(obj: Any) -> Any:
⋮
│async def dispatch_webhook(
│    webhook: Optional[Webhook], event: WebhookEvent, payload: Dict[str, Any]
⋮

packages\koda\tests\conftest.py:
⋮
│class AsyncioFilter(logging.Filter):
│    def filter(self, record):
│        if record.levelno >= logging.ERROR and "TargetClosedError" in record.getMessage():
│            return False
⋮
│def get_child_processes():
⋮
│class TestServerThread(threading.Thread):
│    def __init__(self, directory):
│        super().__init__()
│        self.directory = directory
│        self.server = None
│        self.port = None
⋮
│    def run(self):
│        # Capture directory in closure
│        directory = self.directory
│        
│        class Handler(SimpleHTTPRequestHandler):
│            def __init__(self, *args, **kwargs):
⋮
│    def stop(self):
⋮

packages\koda\tests\integration\test_crawlee.py:
⋮
│@pytest.mark.asyncio
│async def test_crawlee_headed_propagation(monkeypatch, local_test_server):
│    """Test that KODA_HEADLESS=false propagates successfully to the browser config."""
⋮
│    class MockContext:
│        async def grant_permissions(self, *args, **kwargs):
│            pass
│        async def close(self):
│            pass
│        def on(self, *args, **kwargs):
│            pass
│        async def route(self, *args, **kwargs):
⋮

packages\koda\tests\integration\test_crawlee_timeout_and_crash.py:
⋮
│@pytest.mark.asyncio
│async def test_koda_browser_controller_crash():
│    """Test that KodaBrowserController catches TargetClosedError and marks _is_closed."""
│    
⋮
│    class PlaywrightError(Exception):
⋮
│@pytest.mark.asyncio
│async def test_koda_browser_controller_protocol_error():
│    """Test that KodaBrowserController catches protocol errors and marks _is_closed."""
│    
⋮
│    class PlaywrightError(Exception):
⋮

packages\koda\tests\integration\test_csp_bypass.py:
⋮
│async def start_local_server(port=8081):
⋮

packages\koda\tests\integration\test_s3_storage.py:
⋮
│@pytest.fixture(autouse=True)
│def setup_s3_settings():
⋮
│@pytest.fixture
│def dummy_profile_dir(tmp_path):
⋮
│@pytest.mark.asyncio
│async def test_s3_upload_download_flow(dummy_profile_dir, tmp_path):
⋮

packages\koda\tests\integration\test_stagehand.py:
⋮
│@pytest.mark.asyncio
│async def test_stagehand_integration(local_test_server):
│    """Test that Stagehand can successfully use a BrowserSession to extract elements via KodaClient
⋮
│    class StagehandMock:
│        def __init__(self, **kwargs):
│            self.client = kwargs.get("client")
│        async def init(self, *args, **kwargs):
│            pass
│        async def close(self, *args, **kwargs):
⋮

packages\koda\tests\manual\use_cases\scrape_youtube_profile\test_scrape_youtube_profile.py:
⋮
│def save_base64_image(base64_string: str, filename: str, output_dir: str = "output") -> str:
⋮
│async def main():
│    
⋮

packages\koda\tests\unit\conftest.py:
⋮
│@pytest.fixture(autouse=True)
│def mock_launch_browser():
⋮

packages\koda\tests\unit\modules\session\test_service.py:
⋮
│def create_mock_session_model(
│    id: str,
│    provider: str = "test_provider",
│    usage_count: int = 0,
│    error_score: float = 0.0,
│    is_blocked: bool = False,
│    mfa: Optional[MFAParam] = None,
│    browser: Optional[BrowserParam] = None
⋮

packages\koda\tests\unit\use_cases\test_crawl_service.py:
⋮
│@pytest.mark.asyncio
│async def test_crawl_success_stream(mock_crawl4ai, mock_koda_client):
│    client_instance = AsyncMock()
⋮
│    async def mock_stream():
⋮

packages\koda\tests\unit\utils\webhook\test_service.py:
⋮
│class MockRequest(BaseModel):
⋮
│class MockResponse(BaseModel):
⋮
│@webhook_dispatch
│async def dummy_success_func(request, webhook=None):
⋮
│@webhook_dispatch
│async def dummy_failure_func(request, webhook=None):
⋮
│@webhook_dispatch
│async def dummy_exception_func(request, webhook=None):
⋮
```