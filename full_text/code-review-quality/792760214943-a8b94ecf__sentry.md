---
name: sentry
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging sentry. Use this skill whenever modifying sentry configurations or adding related functionality.
---
# sentry

## File Tree

```text
sentry/
├── assets
├── modules
│   └── sentry-python (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

### AST Map: `modules/sentry-python`

```python
scripts\build_aws_lambda_layer.py:
⋮
│def build_packaged_zip(base_dir=None, out_zip_filename=None):
⋮

scripts\populate_tox\config.py:
⋮
│TEST_SUITE_CONFIG = {
│    "aiohttp": {
│        "package": "aiohttp",
│        "deps": {
│            "*": ["pytest-aiohttp"],
│            ">=3.8": ["pytest-asyncio"],
│        },
│        "python": ">=3.7",
│    },
│    "aiomysql": {
⋮

sentry_sdk\_compat.py:
⋮
│def check_uwsgi_thread_support() -> bool:
⋮
│    try:
│        from uwsgi import opt  # type: ignore
│    except ImportError:
⋮
│    def enabled(option: str) -> bool:
⋮

sentry_sdk\_lru_cache.py:
⋮
│class LRUCache:
│    def __init__(self, max_size: int) -> None:
│        if max_size <= 0:
│            raise AssertionError(f"invalid max_size: {max_size}")
│        self.max_size = max_size
│        self._data: "dict[Any, Any]" = {}
│        self.hits = self.misses = 0
⋮
│    def set(self, key: "Any", value: "Any") -> None:
⋮

sentry_sdk\_queue.py:
⋮
│class EmptyError(Exception):
⋮
│class FullError(Exception):
⋮
│class Queue:
│    """Create a queue object with a given maximum size.
│
│    If maxsize is <= 0, the queue size is infinite.
⋮
│    def join(self):
⋮

sentry_sdk\_types.py:
⋮
│class AnnotatedValue:
│    """
│    Meta information for a data field in the event payload.
│    This is to tell Relay that we have tampered with the fields value.
│    See:
│    https://github.com/getsentry/relay/blob/be12cd49a0f06ea932ed9b9f93a655de5d6ad6d1/relay-general/
⋮
│    @classmethod
│    def removed_because_over_size_limit(cls, value: "Any" = "") -> "AnnotatedValue":
⋮

sentry_sdk\ai\utils.py:
⋮
│def get_modality_from_mime_type(mime_type: str) -> str:
⋮

sentry_sdk\api.py:
⋮
│@scopemethod
│def get_client() -> "BaseClient":
⋮
│@scopemethod
│def get_global_scope() -> "Scope":
⋮
│@scopemethod
│def get_isolation_scope() -> "Scope":
⋮
│@scopemethod
│def get_current_scope() -> "Scope":
⋮
│@scopemethod
│def capture_message(
│    message: str,
│    level: "Optional[LogLevelStr]" = None,
│    scope: "Optional[Any]" = None,
│    **scope_kwargs: "Any",
⋮
│@scopemethod
│def capture_exception(
│    error: "Optional[Union[BaseException, ExcInfo]]" = None,
│    scope: "Optional[Any]" = None,
│    **scope_kwargs: "Any",
⋮
│@scopemethod
│def add_breadcrumb(
│    crumb: "Optional[Breadcrumb]" = None,
│    hint: "Optional[BreadcrumbHint]" = None,
│    **kwargs: "Any",
⋮
│@overload
│def push_scope() -> "ContextManager[Scope]":
⋮
│@overload
│def push_scope(  # noqa: F811
│    callback: "Callable[[Scope], None]",
⋮
│def push_scope(  # noqa: F811
│    callback: "Optional[Callable[[Scope], None]]" = None,
⋮
│@scopemethod
│def set_attribute(attribute: str, value: "Any") -> None:
⋮
│@scopemethod
│def set_context(key: str, value: "Dict[str, Any]") -> None:
⋮
│@scopemethod
│def set_user(value: "Optional[Dict[str, Any]]") -> None:
⋮
│@clientmethod
│async def flush_async(
│    timeout: "Optional[float]" = None,
│    callback: "Optional[Callable[[int, float], None]]" = None,
⋮
│@scopemethod
│def start_span(
│    **kwargs: "Any",
⋮
│@scopemethod
│def start_transaction(
│    transaction: "Optional[Transaction]" = None,
│    instrumenter: str = INSTRUMENTER.SENTRY,
│    custom_sampling_context: "Optional[SamplingContext]" = None,
│    **kwargs: "Unpack[TransactionKwargs]",
⋮
│def get_current_span(
│    scope: "Optional[Scope]" = None,
⋮
│def get_traceparent() -> "Optional[str]":
⋮
│def get_baggage() -> "Optional[str]":
⋮
│def continue_trace(
│    environ_or_headers: "Dict[str, Any]",
│    op: "Optional[str]" = None,
│    name: "Optional[str]" = None,
│    source: "Optional[str]" = None,
│    origin: str = "manual",
⋮
│@scopemethod
│def start_session(
│    session_mode: str = "application",
⋮
│@scopemethod
│def end_session() -> None:
⋮
│@scopemethod
│def set_transaction_name(name: str, source: "Optional[str]" = None) -> None:
⋮

sentry_sdk\client.py:
⋮
│class BaseClient:
│    """
│    .. versionadded:: 2.0.0
│
│    The basic definition of a client that is used for sending data to Sentry.
⋮
│    def should_send_default_pii(self) -> bool:
⋮
│    def is_active(self) -> bool:
⋮
│    if TYPE_CHECKING:
│
│        @overload
│        def get_integration(self, name_or_class: str) -> "Optional[Integration]": ...
│
│        @overload
│        def get_integration(self, name_or_class: "type[I]") -> "Optional[I]": ...
│
│    def get_integration(
│        self, name_or_class: "Union[str, type[Integration]]"
⋮
│    async def flush_async(self, *args: "Any", **kwargs: "Any") -> None:
⋮
│class NonRecordingClient(BaseClient):
⋮
│class _Client(BaseClient):
│    """
│    The client is internally responsible for capturing the events and
│    forwarding them to sentry through the configured transport.  It takes
│    the client options as keyword arguments and optionally the DSN as first
│    argument.
│
│    Alias of :py:class:`sentry_sdk.Client`. (Was created for better intelisense support)
⋮
│    def is_active(self) -> bool:
⋮
│    def should_send_default_pii(self) -> bool:
⋮
│    if TYPE_CHECKING:
│
│        @overload
│        def get_integration(self, name_or_class: str) -> "Optional[Integration]": ...
│
│        @overload
│        def get_integration(self, name_or_class: "type[I]") -> "Optional[I]": ...
│
│    def get_integration(
│        self,
│        name_or_class: "Union[str, Type[Integration]]",
⋮
│    async def flush_async(
│        self,
│        timeout: "Optional[float]" = None,
│        callback: "Optional[Callable[[int, float], None]]" = None,
⋮

sentry_sdk\crons\consts.py:
│class MonitorStatus:
⋮

sentry_sdk\envelope.py:
⋮
│def parse_json(data: "Union[bytes, str]") -> "Any":
⋮
│class Envelope:
│    """
│    Represents a Sentry Envelope. The calling code is responsible for adhering to the constraints
│    documented in the Sentry docs: https://develop.sentry.dev/sdk/envelopes/#data-model. In particu
│    each envelope may have at most one Item with type "event" or "transaction" (but not both).
⋮
│    def add_item(
│        self,
│        item: "Item",
⋮
│    def get_event(self) -> "Optional[Event]":
⋮
│    def get_transaction_event(self) -> "Optional[Event]":
⋮
│    def serialize_into(
│        self,
│        f: "Any",
⋮
│    @classmethod
│    def deserialize_from(
│        cls,
│        f: "Any",
⋮
│class PayloadRef:
│    def __init__(
│        self,
│        bytes: "Optional[bytes]" = None,
│        path: "Optional[Union[bytes, str]]" = None,
│        json: "Optional[Any]" = None,
⋮
│    def get_bytes(self) -> bytes:
⋮
│class Item:
│    def __init__(
│        self,
│        payload: "Union[bytes, str, PayloadRef]",
│        headers: "Optional[Dict[str, Any]]" = None,
│        type: "Optional[str]" = None,
│        content_type: "Optional[str]" = None,
│        filename: "Optional[str]" = None,
⋮
│    @property
│    def type(self) -> "Optional[str]":
⋮
│    def get_bytes(self) -> bytes:
⋮
│    def get_event(self) -> "Optional[Event]":
⋮
│    def get_transaction_event(self) -> "Optional[Event]":
⋮
│    def serialize_into(
│        self,
│        f: "Any",
⋮
│    @classmethod
│    def deserialize_from(
│        cls,
│        f: "Any",
⋮

sentry_sdk\feature_flags.py:
⋮
│class FlagBuffer:
│    def __init__(self, capacity: int) -> None:
│        self.capacity = capacity
│        self.lock = Lock()
│
│        # Buffer is private. The name is mangled to discourage use. If you use this attribute
│        # directly you're on your own!
⋮
│    def get(self) -> "list[FlagData]":
⋮
│    def set(self, flag: str, result: bool) -> None:
⋮

sentry_sdk\hub.py:
⋮
│class Hub(with_metaclass(HubMeta)):  # type: ignore
│    """
│    .. deprecated:: 2.0.0
│        The Hub is deprecated. Its functionality will be merged into :py:class:`sentry_sdk.scope.Sc
│
│    The hub wraps the concurrency management of the SDK.  Each thread has
│    its own hub but the hub might transfer with the flow of execution if
│    context vars are available.
│
│    If the hub is used with a with statement it's temporarily activated.
⋮
│    def get_integration(
│        self,
│        name_or_class: "Union[str, Type[Integration]]",
⋮
│    def capture_message(
│        self,
│        message: str,
│        level: "Optional[LogLevelStr]" = None,
│        scope: "Optional[Scope]" = None,
│        **scope_kwargs: "Any",
⋮
│    def capture_exception(
│        self,
│        error: "Optional[Union[BaseException, ExcInfo]]" = None,
│        scope: "Optional[Scope]" = None,
│        **scope_kwargs: "Any",
⋮
│    def add_breadcrumb(
│        self,
│        crumb: "Optional[Breadcrumb]" = None,
│        hint: "Optional[BreadcrumbHint]" = None,
│        **kwargs: "Any",
⋮
│    def start_span(
│        self, instrumenter: str = INSTRUMENTER.SENTRY, **kwargs: "Any"
⋮
│    def start_transaction(
│        self,
│        transaction: "Optional[Transaction]" = None,
│        instrumenter: str = INSTRUMENTER.SENTRY,
│        custom_sampling_context: "Optional[SamplingContext]" = None,
│        **kwargs: "Unpack[TransactionKwargs]",
⋮
│    def continue_trace(
│        self,
│        environ_or_headers: "Dict[str, Any]",
│        op: "Optional[str]" = None,
│        name: "Optional[str]" = None,
│        source: "Optional[str]" = None,
⋮
│    @overload
│    def push_scope(
│        self,
│        callback: "Optional[None]" = None,
⋮
│    @overload
│    def push_scope(  # noqa: F811
│        self,
│        callback: "Callable[[Scope], None]",
⋮
│    def push_scope(  # noqa
│        self,
│        callback: "Optional[Callable[[Scope], None]]" = None,
│        continue_trace: bool = True,
⋮
│    def start_session(
│        self,
│        session_mode: str = "application",
⋮
│    def end_session(self) -> None:
⋮
│    def get_traceparent(self) -> "Optional[str]":
⋮
│    def get_baggage(self) -> "Optional[str]":
⋮
│    def iter_trace_propagation_headers(
│        self, span: "Optional[Span]" = None
⋮

sentry_sdk\integrations\__init__.py:
⋮
│class DidNotEnable(Exception):  # noqa: N818
⋮

sentry_sdk\integrations\aws_lambda.py:
⋮
│class AwsLambdaIntegration(Integration):
⋮

sentry_sdk\integrations\clickhouse_driver.py:
⋮
│if TYPE_CHECKING:
⋮
│else:
│    # Fake ParamSpec
│    class ParamSpec:
│        def __init__(self, _):
│            self.args = None
⋮

sentry_sdk\integrations\django\transactions.py:
⋮
│def get_regex(resolver_or_pattern: "Union[URLPattern, URLResolver]") -> "Pattern[str]":
⋮

sentry_sdk\integrations\grpc\__init__.py:
⋮
│if TYPE_CHECKING:
│    from typing import Callable, ParamSpec
│else:
│    # Fake ParamSpec
│    class ParamSpec:
│        def __init__(self, _):
│            self.args = None
⋮

sentry_sdk\integrations\stdlib.py:
⋮
│def _install_httplib() -> None:
│    real_putrequest = HTTPConnection.putrequest
⋮
│    def read(self: "HTTPResponse", *args: "Any", **kwargs: "Any") -> "Any":
⋮

sentry_sdk\profiler\continuous_profiler.py:
⋮
│def try_autostart_continuous_profiler() -> None:
⋮
│def try_profile_lifecycle_trace_start() -> "Union[ContinuousProfile, None]":
⋮
│def teardown_continuous_profiler() -> None:
⋮
│def get_profiler_id() -> "Union[str, None]":
⋮

sentry_sdk\profiler\transaction_profiler.py:
⋮
│def teardown_profiler() -> None:
⋮
│class Profile:
│    def __init__(
│        self,
│        sampled: "Optional[bool]",
│        start_ns: int,
│        hub: "Optional[sentry_sdk.Hub]" = None,
│        scheduler: "Optional[Scheduler]" = None,
⋮
│    def write(self, ts: int, sample: "ExtractedSample") -> None:
⋮

sentry_sdk\scope.py:
⋮
│class Scope:
│    """The scope holds extra information that should be sent with all
│    events that belong to it.
⋮
│    @classmethod
│    def get_current_scope(cls) -> "Scope":
⋮
│    @classmethod
│    def get_isolation_scope(cls) -> "Scope":
⋮
│    @classmethod
│    def get_global_scope(cls) -> "Scope":
⋮
│    @classmethod
│    def get_client(cls) -> "sentry_sdk.client.BaseClient":
⋮
│    def set_client(
│        self, client: "Optional[sentry_sdk.client.BaseClient]" = None
⋮
│    def set_new_propagation_context(self) -> None:
⋮
│    def generate_propagation_context(
│        self, incoming_data: "Optional[Dict[str, str]]" = None
⋮
│    def get_traceparent(self, *args: "Any", **kwargs: "Any") -> "Optional[str]":
⋮
│    def get_baggage(self, *args: "Any", **kwargs: "Any") -> "Optional[Baggage]":
⋮
│    def get_trace_context(self) -> "Dict[str, Any]":
⋮
│    def iter_trace_propagation_headers(
│        self, *args: "Any", **kwargs: "Any"
⋮
│    def get_active_propagation_context(self) -> "PropagationContext":
⋮
│    def set_transaction_name(self, name: str, source: "Optional[str]" = None) -> None:
⋮
│    def set_user(self, value: "Optional[Dict[str, Any]]") -> None:
⋮
│    def set_context(
│        self,
│        key: str,
│        value: "Dict[str, Any]",
⋮
│    def clear_breadcrumbs(self) -> None:
⋮
│    def add_breadcrumb(
│        self,
│        crumb: "Optional[Breadcrumb]" = None,
│        hint: "Optional[BreadcrumbHint]" = None,
│        **kwargs: "Any",
⋮
│    def start_transaction(
│        self,
│        transaction: "Optional[Transaction]" = None,
│        instrumenter: str = INSTRUMENTER.SENTRY,
│        custom_sampling_context: "Optional[SamplingContext]" = None,
│        **kwargs: "Unpack[TransactionKwargs]",
⋮
│    def start_span(
│        self, instrumenter: str = INSTRUMENTER.SENTRY, **kwargs: "Any"
⋮
│    def continue_trace(
│        self,
│        environ_or_headers: "Dict[str, Any]",
│        op: "Optional[str]" = None,
│        name: "Optional[str]" = None,
│        source: "Optional[str]" = None,
│        origin: str = "manual",
⋮
│    def capture_message(
│        self,
│        message: str,
│        level: "Optional[LogLevelStr]" = None,
│        scope: "Optional[Scope]" = None,
│        **scope_kwargs: "Any",
⋮
│    def capture_exception(
│        self,
│        error: "Optional[Union[BaseException, ExcInfo]]" = None,
│        scope: "Optional[Scope]" = None,
│        **scope_kwargs: "Any",
⋮
│    def start_session(self, *args: "Any", **kwargs: "Any") -> None:
⋮
│    def end_session(self, *args: "Any", **kwargs: "Any") -> None:
⋮
│    def update_from_scope(self, scope: "Scope") -> None:
⋮
│    def set_attribute(self, attribute: str, value: "AttributeValue") -> None:
⋮
│@contextmanager
│def new_scope() -> "Generator[Scope, None, None]":
⋮
│@contextmanager
│def use_scope(scope: "Scope") -> "Generator[Scope, None, None]":
⋮
│@contextmanager
│def use_isolation_scope(isolation_scope: "Scope") -> "Generator[Scope, None, None]":
⋮
│def should_send_default_pii() -> bool:
⋮

sentry_sdk\traces.py:
⋮
│def start_span(
│    name: str,
│    attributes: "Optional[Attributes]" = None,
│    parent_span: "Optional[StreamedSpan]" = _DEFAULT_PARENT_SPAN,  # type: ignore[assignment]
│    active: bool = True,
⋮
│def continue_trace(incoming: "dict[str, Any]") -> None:
⋮
│class StreamedSpan:
│    """
│    A span holds timing information of a block of code.
│
│    Spans can have multiple child spans, thus forming a span tree.
│
│    This is the Span First span implementation that streams spans. The original
│    transaction-based span implementation lives in tracing.Span.
⋮
│    def set_attribute(self, key: str, value: "AttributeValue") -> None:
⋮
│class NoOpStreamedSpan(StreamedSpan):
│    __slots__ = (
│        "_finished",
│        "_unsampled_reason",
⋮
│    def set_attribute(self, key: str, value: "AttributeValue") -> None:
⋮
│def get_current_span(
│    scope: "Optional[sentry_sdk.Scope]" = None,
⋮

sentry_sdk\tracing.py:
⋮
│class Span:
│    """A span holds timing information of a block of code.
│    Spans can have multiple child spans thus forming a span tree.
│
│    :param trace_id: The trace ID of the root span. If this new span is to be the root span,
│        omit this parameter, and a new trace ID will be generated.
│    :param span_id: The span ID of this span. If omitted, a new span ID will be generated.
│    :param parent_span_id: The span ID of the parent span, if applicable.
│    :param same_process_as_parent: Whether this span is in the same process as the parent span.
│    :param sampled: Whether the span should be sampled. Overrides the default sampling decision
│        for this span when provided.
⋮
│    def start_child(
│        self, instrumenter: str = INSTRUMENTER.SENTRY, **kwargs: "Any"
⋮
│    def iter_headers(self) -> "Iterator[Tuple[str, str]]":
⋮
│    def to_traceparent(self) -> str:
⋮
│    def set_data(self, key: str, value: "Any") -> None:
⋮
│    def update_data(self, data: "Dict[str, Any]") -> None:
⋮
│    def set_profiler_id(self, profiler_id: "Optional[str]") -> None:
⋮
│    def get_trace_context(self) -> "Any":
⋮
│class Transaction(Span):
│    """The Transaction is the root element that holds all the spans
│    for Sentry performance instrumentation.
│
│    :param name: Identifier of the transaction.
│        Will show up in the Sentry UI.
│    :param parent_sampled: Whether the parent transaction was sampled.
│        If True this transaction will be kept, if False it will be discarded.
│    :param baggage: The W3C baggage header value.
│        (see https://www.w3.org/TR/baggage/)
│    :param source: A string describing the source of the transaction name.
⋮
│    def set_context(self, key: str, value: "dict[str, Any]") -> None:
⋮
│    def get_trace_context(self) -> "Any":
⋮
│    def get_baggage(self) -> "Baggage":
⋮
│class NoOpSpan(Span):
│    def __repr__(self) -> str:
⋮
│    def start_child(
│        self, instrumenter: str = INSTRUMENTER.SENTRY, **kwargs: "Any"
⋮
│    def to_traceparent(self) -> str:
⋮
│    def get_baggage(self) -> "Optional[Baggage]":
⋮
│    def iter_headers(self) -> "Iterator[Tuple[str, str]]":
⋮
│    def set_data(self, key: str, value: "Any") -> None:
⋮
│    def update_data(self, data: "Dict[str, Any]") -> None:
⋮
│    def get_trace_context(self) -> "Any":
⋮
│    def set_context(self, key: str, value: "dict[str, Any]") -> None:
⋮

sentry_sdk\tracing_utils.py:
⋮
│def has_tracing_enabled(options: "Optional[Dict[str, Any]]") -> bool:
⋮
│def has_span_streaming_enabled(options: "Optional[dict[str, Any]]") -> bool:
⋮
│class PropagationContext:
│    """
│    The PropagationContext represents the data of a trace in Sentry.
⋮
│    @property
│    def dynamic_sampling_context(self) -> "Optional[Dict[str, Any]]":
⋮
│    def to_traceparent(self) -> str:
⋮
│    def get_baggage(self) -> "Baggage":
⋮
│class Baggage:
│    """
│    The W3C Baggage header information (see https://www.w3.org/TR/baggage/).
│
│    Before mutating a `Baggage` object, calling code must check that `mutable` is `True`.
│    Mutating a `Baggage` object that has `mutable` set to `False` is not allowed, but
│    it is the caller's responsibility to enforce this restriction.
⋮
│    @classmethod
│    def from_incoming_header(
│        cls,
│        header: "Optional[str]",
│        *,
│        _sample_rand: "Optional[str]" = None,
⋮
│    def dynamic_sampling_context(self) -> "Dict[str, str]":
⋮
│def get_current_span(
│    scope: "Optional[sentry_sdk.Scope]" = None,
⋮

sentry_sdk\utils.py:
⋮
│def json_dumps(data: "Any") -> bytes:
⋮
│def get_git_revision() -> "Optional[str]":
⋮
│class CaptureInternalException:
⋮
│def capture_internal_exceptions() -> "ContextManager[Any]":
⋮
│def capture_internal_exception(exc_info: "ExcInfo") -> None:
⋮
│def format_timestamp(value: "datetime") -> str:
⋮
│def datetime_from_isoformat(value: str) -> "datetime":
⋮
│def event_hint_with_exc_info(
│    exc_info: "Optional[ExcInfo]" = None,
⋮
│def get_type_name(cls: "Optional[type]") -> "Optional[str]":
⋮
│def get_type_module(cls: "Optional[type]") -> "Optional[str]":
⋮
│def should_hide_frame(frame: "FrameType") -> bool:
⋮
│def iter_stacks(tb: "Optional[TracebackType]") -> "Iterator[TracebackType]":
⋮
│def get_lines_from_file(
│    filename: str,
│    lineno: int,
│    max_length: "Optional[int]" = None,
│    loader: "Optional[Any]" = None,
│    module: "Optional[str]" = None,
⋮
│def get_source_context(
│    frame: "FrameType",
│    tb_lineno: "Optional[int]",
│    max_value_length: "Optional[int]" = None,
⋮
│def safe_str(value: "Any") -> str:
⋮
│def safe_repr(value: "Any") -> str:
⋮
│def filename_for_module(
│    module: "Optional[str]", abs_path: "Optional[str]"
⋮
│def serialize_frame(
│    frame: "FrameType",
│    tb_lineno: "Optional[int]" = None,
│    include_local_variables: bool = True,
│    include_source_context: bool = True,
│    max_value_length: "Optional[int]" = None,
│    custom_repr: "Optional[Callable[..., Optional[str]]]" = None,
⋮
│def current_stacktrace(
│    include_local_variables: bool = True,
│    include_source_context: bool = True,
│    max_value_length: "Optional[int]" = None,
⋮
│def get_errno(exc_value: BaseException) -> "Optional[Any]":
⋮
│def get_error_message(exc_value: "Optional[BaseException]") -> str:
⋮
│def single_exception_from_error_tuple(
│    exc_type: "Optional[type]",
│    exc_value: "Optional[BaseException]",
│    tb: "Optional[TracebackType]",
│    client_options: "Optional[Dict[str, Any]]" = None,
│    mechanism: "Optional[Dict[str, Any]]" = None,
│    exception_id: "Optional[int]" = None,
│    parent_id: "Optional[int]" = None,
│    source: "Optional[str]" = None,
│    full_stack: "Optional[list[dict[str, Any]]]" = None,
⋮
│if HAS_CHAINED_EXCEPTIONS:
│
│    def walk_exception_chain(exc_info: "ExcInfo") -> "Iterator[ExcInfo]":
│        exc_type, exc_value, tb = exc_info
│
│        seen_exceptions = []
│        seen_exception_ids: "Set[int]" = set()
│
│        while (
│            exc_type is not None
│            and exc_value is not None
│            and id(exc_value) not in seen_exception_ids
⋮
│else:
│
│    def walk_exception_chain(exc_info: "ExcInfo") -> "Iterator[ExcInfo]":
⋮
│def exceptions_from_error(
│    exc_type: "Optional[type]",
│    exc_value: "Optional[BaseException]",
│    tb: "Optional[TracebackType]",
│    client_options: "Optional[Dict[str, Any]]" = None,
│    mechanism: "Optional[Dict[str, Any]]" = None,
│    exception_id: int = 0,
│    parent_id: int = 0,
│    source: "Optional[str]" = None,
│    full_stack: "Optional[list[dict[str, Any]]]" = None,
⋮
│def exceptions_from_error_tuple(
│    exc_info: "ExcInfo",
│    client_options: "Optional[Dict[str, Any]]" = None,
│    mechanism: "Optional[Dict[str, Any]]" = None,
│    full_stack: "Optional[list[dict[str, Any]]]" = None,
⋮
│def iter_event_stacktraces(event: "Event") -> "Iterator[Annotated[Dict[str, Any]]]":
⋮
│def set_in_app_in_frames(
│    frames: "Any",
│    in_app_exclude: "Optional[List[str]]",
│    in_app_include: "Optional[List[str]]",
│    project_root: "Optional[str]" = None,
⋮
│def exc_info_from_error(error: "Union[BaseException, ExcInfo]") -> "ExcInfo":
⋮
│def merge_stack_frames(
│    frames: "List[Dict[str, Any]]",
│    full_stack: "List[Dict[str, Any]]",
│    client_options: "Optional[Dict[str, Any]]",
⋮
│def event_from_exception(
│    exc_info: "Union[BaseException, ExcInfo]",
│    client_options: "Optional[Dict[str, Any]]" = None,
│    mechanism: "Optional[Dict[str, Any]]" = None,
⋮
│def strip_string(
│    value: str, max_length: "Optional[int]" = None
⋮
│def parse_version(version: str) -> "Optional[Tuple[int, ...]]":
⋮
│def _make_threadlocal_contextvars(local: type) -> type:
│    class ContextVar:
│        # Super-limited impl of ContextVar
│
│        def __init__(self, name: str, default: "Any" = None) -> None:
│            self._name = name
│            self._default = default
│            self._local = local()
│            self._original_local = local()
│
│        def get(self, default: "Any" = None) -> "Any":
⋮
│        def set(self, value: "Any") -> "Any":
⋮
│def qualname_from_function(func: "Callable[..., Any]") -> "Optional[str]":
⋮
│class ServerlessTimeoutWarning(Exception):  # noqa: N818
⋮
│Components = namedtuple("Components", ["scheme", "netloc", "path", "query", "fragment"])
│
⋮
│def sanitize_url(
│    url: str,
│    remove_authority: bool = True,
│    remove_query_values: bool = True,
│    split: bool = False,
⋮
│ParsedUrl = namedtuple("ParsedUrl", ["url", "query", "fragment"])
│
⋮
│def is_valid_sample_rate(rate: "Any", source: str) -> bool:
⋮
│def package_version(package: str) -> "Optional[Tuple[int, ...]]":
⋮
│if TYPE_CHECKING:
│
│    @overload
│    def ensure_integration_enabled(
│        integration: "type[sentry_sdk.integrations.Integration]",
│        original_function: "Callable[P, R]",
⋮
│    @overload
│    def ensure_integration_enabled(
│        integration: "type[sentry_sdk.integrations.Integration]",
⋮
│def ensure_integration_enabled(
│    integration: "type[sentry_sdk.integrations.Integration]",
│    original_function: "Union[Callable[P, R], Callable[P, None]]" = _no_op,
⋮
│if PY37:
│
│    def nanosecond_time() -> int:
⋮
│else:
│
│    def nanosecond_time() -> int:
⋮
│try:
⋮
│except ImportError:
⋮
│    def get_gevent_hub() -> "Optional[Hub]":  # type: ignore[misc]
⋮
│    def is_module_patched(mod_name: str) -> bool:
⋮
│def is_gevent() -> bool:
⋮
│def get_current_thread_meta(
│    thread: "Optional[threading.Thread]" = None,
⋮
│def safe_serialize(data: "Any") -> str:
│    """Safely serialize to a readable string."""
│
│    def serialize_item(
│        item: "Any",
⋮
│def has_logs_enabled(options: "Optional[dict[str, Any]]") -> bool:
⋮
│def format_attribute(val: "Any") -> "AttributeValue":
⋮

tests\conftest.py:
⋮
│@pytest.fixture
│def sentry_init(request):
⋮
│@pytest.fixture
│def capture_events(monkeypatch):
⋮
│@pytest.fixture
│def capture_envelopes(monkeypatch):
⋮
│@dataclass
│class UnwrappedItem:
⋮
│@pytest.fixture
│def capture_items(monkeypatch):
⋮
│@pytest.fixture
│def capture_events_forksafe(monkeypatch, capture_events, request):
│    def inner():
│        capture_events()
│
│        events_r, events_w = os.pipe()
│        events_r = os.fdopen(events_r, "rb", 0)
│        events_w = os.fdopen(events_w, "wb", 0)
│
│        test_client = sentry_sdk.get_client()
│
│        old_capture_envelope = test_client.transport.capture_envelope
│
│        def append(envelope):
⋮
│@pytest.fixture
│def capture_items_forksafe(monkeypatch, capture_items, request):
│    def inner(*types):
│        capture_items(*types)
│
│        items_r, items_w = os.pipe()
│        items_r = os.fdopen(items_r, "rb", 0)
│        items_w = os.fdopen(items_w, "wb", 0)
│
│        test_client = sentry_sdk.get_client()
│        old_capture_envelope = test_client.transport.capture_envelope
│
⋮
│        def append(envelope):
⋮
│class EventStreamReader:
⋮
│@pytest.fixture
│def render_span_tree():
│    def inner(spans, root_span=None):
│        streamed_spans = False
│        if root_span is None:
│            streamed_spans = True
│
│        by_parent = {}
│        for span in spans:
│            if "parent_span_id" not in span:
│                root_span = span
│                continue
│
⋮
│        def render_span(span):
⋮
│@pytest.fixture()
│def json_rpc_sse():
│    class StreamingASGITransport(ASGITransport):
│        """
│        Simple transport whose only purpose is to keep GET request alive in SSE connections, allowi
│        tests involving SSE interactions to run in-process.
│        """
│
│        def __init__(
│            self,
│            app: "Callable",
│            keep_sse_alive: "asyncio.Event",
⋮
│    def parse_sse_data_package(sse_chunk):
⋮

tests\integrations\bottle\test_bottle.py:
⋮
│@pytest.fixture
│def get_client(app):
⋮

tests\integrations\django\django_helpers\views.py:
⋮
│@csrf_exempt
│def postgres_select_orm(request, *args, **kwargs):
⋮

tests\integrations\django\myapp\routing.py:
⋮
│application = ProtocolTypeRouter({"http": django_asgi_app})

tests\integrations\django\myapp\wsgi.py:
⋮
│application = get_wsgi_application()

tests\integrations\grpc\grpc_test_service_pb2_grpc.py:
⋮
│class gRPCTestServiceServicer(object):
⋮
│class gRPCTestService(object):
⋮

tests\integrations\litellm\test_litellm.py:
⋮
│class MockMessage:
│    def __init__(self, role="assistant", content="Test response"):
│        self.role = role
│        self.content = content
⋮
│    def model_dump(self):
⋮

tests\integrations\opentelemetry\test_entry_points.py:
⋮
│def test_propagator_loaded_if_mentioned_in_environment_variable():
⋮

tests\integrations\pyramid\test_pyramid.py:
⋮
│@pytest.fixture
│def get_client(pyramid_config):
⋮

tests\integrations\sanic\test_sanic.py:
⋮
│def get_client(app):
⋮

tests\integrations\trytond\test_trytond.py:
⋮
│@pytest.fixture
│def get_client(app):
⋮

tests\integrations\wsgi\test_wsgi.py:
⋮
│class ExitingIterable:
│    def __init__(self, exc_func):
⋮
│    def next(self):
⋮

tests\profiler\test_transaction_profiler.py:
⋮
│current_thread = threading.current_thread()
⋮

tests\test_ai_monitoring.py:
⋮
│class TestTruncateAndAnnotateMessages:
│    def test_only_keeps_last_message(self, sample_messages):
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_id"
│                self.data = {}
│
│            def set_data(self, key, value):
│                self.data[key] = value
│
│        class MockScope:
⋮
│    def test_truncation_sets_metadata_on_scope(self, large_messages):
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_id"
│                self.data = {}
│
│            def set_data(self, key, value):
⋮
│    def test_scope_tracks_original_message_count(self, large_messages):
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_id"
│                self.data = {}
│
│            def set_data(self, key, value):
⋮
│    def test_empty_messages_returns_none(self):
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_id"
│                self.data = {}
│
│            def set_data(self, key, value):
⋮
│    def test_truncated_messages_newest_first(self, large_messages):
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_id"
│                self.data = {}
│
│            def set_data(self, key, value):
⋮
│    def test_preserves_original_messages_with_blobs(self):
│        """Test that truncate_and_annotate_messages doesn't mutate the original messages"""
│
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_id"
⋮
│            def set_data(self, key, value):
⋮
│class TestClientAnnotation:
│    def test_client_wraps_truncated_messages_in_annotated_value(self, large_messages):
│        """Test that client.py properly wraps truncated messages in AnnotatedValue using scope data
│        from sentry_sdk._types import AnnotatedValue
│        from sentry_sdk.consts import SPANDATA
│
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_123"
│                self.data = {}
│
│            def set_data(self, key, value):
⋮
│    def test_annotated_value_shows_correct_original_length(self, large_messages):
│        """Test that the annotated value correctly shows the original message count before truncati
⋮
│        class MockSpan:
│            def __init__(self):
│                self.span_id = "test_span_456"
⋮
│            def set_data(self, key, value):
⋮

tests\test_import.py:
⋮
│def test_import():
⋮

tests\test_types.py:
⋮
│@pytest.mark.skipif(
│    sys.version_info < (3, 10),
│    reason="Type hinting with `|` is available in Python 3.10+",
│)
│def test_event_or_none_runtime():
⋮
│@pytest.mark.skipif(
│    sys.version_info < (3, 10),
│    reason="Type hinting with `|` is available in Python 3.10+",
│)
│def test_hint_or_none_runtime():
⋮

tests\test_utils.py:
⋮
│def test_ensure_integration_enabled_integration_enabled(sentry_init):
│    def original_function():
⋮
│def test_ensure_integration_enabled_integration_disabled(sentry_init):
│    def original_function():
⋮
│def test_get_lines_from_file_handle_linecache_errors():
│    expected_result = ([], None, [])
│
│    class Loader:
│        @staticmethod
│        def get_source(module):
⋮

tests\utils\test_general.py:
⋮
│def test_normalize_data_with_pydantic_class():
│    """Test that _normalize_data handles Pydantic model classes"""
│
│    class TestClass:
│        name: str = None
│
⋮
│        def model_dump(self):
⋮
```
