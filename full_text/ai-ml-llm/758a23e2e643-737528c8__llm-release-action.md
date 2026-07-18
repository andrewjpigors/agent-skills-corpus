---
name: llm-release-action
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging llm-release-action. Use this skill whenever modifying llm-release-action configurations or adding related functionality.
---
# llm-release-action

## File Tree

```text
llm-release-action/
├── assets
├── modules
│   └── llm-release-action (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

### AST Map: `modules/llm-release-action`

```python
evals\conftest.py:
⋮
│DEFAULT_EVAL_MODEL = "bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
│DEFAULT_TEST_MODEL = "bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0"
│
⋮
│def pytest_configure(config):
⋮
│def get_eval_model() -> str:
⋮
│def get_test_model() -> str:
⋮

evals\test_changelog_evals.py:
⋮
│class BedrockLLM(DeepEvalBaseLLM):
│    """Custom DeepEval LLM using AWS Bedrock via LiteLLM."""
│
⋮
│    def generate(self, prompt: str) -> str:
⋮
│def call_llm(prompt: str) -> str:
⋮
│def get_eval_llm() -> BedrockLLM:
⋮

evals\test_context_evals.py:
⋮
│class BedrockLLM(DeepEvalBaseLLM):
│    """Custom DeepEval LLM using AWS Bedrock via LiteLLM."""
│
⋮
│    def generate(self, prompt: str) -> str:
⋮
│def call_llm(prompt: str) -> str:
⋮
│def get_eval_llm() -> BedrockLLM:
⋮

evals\test_flatten_evals.py:
⋮
│class BedrockLLM(DeepEvalBaseLLM):
│    """Custom DeepEval LLM using AWS Bedrock via LiteLLM."""
│
⋮
│    def generate(self, prompt: str) -> str:
⋮
│def call_llm(prompt: str) -> str:
⋮
│def get_eval_llm() -> BedrockLLM:
⋮

evals\test_semver_evals.py:
⋮
│class BedrockLLM(DeepEvalBaseLLM):
│    """Custom DeepEval LLM using AWS Bedrock via LiteLLM."""
│
⋮
│    def generate(self, prompt: str) -> str:
⋮
│def call_llm(prompt: str) -> str:
⋮
│def get_eval_llm() -> BedrockLLM:
⋮

src\analyze.py:
⋮
│@dataclass
│class LLMUsage:
⋮
│@dataclass
│class AggregateUsage:
│    """Aggregate usage statistics for all LLM calls."""
⋮
│    def add(self, usage: LLMUsage) -> None:
⋮
│    def to_dict(self) -> dict:
⋮
│def get_env(name: str, default: Optional[str] = None) -> str:
⋮
│def get_env_bool(name: str, default: bool = False) -> bool:
⋮
│def get_env_int(name: str, default: int) -> int:
⋮
│def get_env_float(name: str, default: float) -> float:
⋮
│def log_group(title: str) -> None:
⋮
│def log_group_end() -> None:
⋮
│def log_error(message: str) -> None:
⋮
│def log_warning(message: str) -> None:
⋮
│def set_output(name: str, value: str) -> None:
⋮
│def call_llm_with_retry(
│    model: str,
│    prompt: str,
│    temperature: float,
│    max_tokens: int,
│    timeout: int,
│    max_retries: int = 3,
│    debug: bool = False,
⋮
│def sanitize_changelog(changelog: str, max_size: int = 65536) -> str:
⋮
│def parse_commits_json(json_str: str) -> List[CommitInfo]:
⋮
│def run_phase1(
│    model: str,
│    commits: List[CommitInfo],
│    base_version: str,
│    content_override: Optional[str],
│    max_commits: int,
│    include_diffs: str,
│    head_ref: str,
│    temperature: float,
│    max_tokens: int,
⋮
│def run_phase2(
│    model: str,
│    changes: List[Change],
│    changelog_config: ChangelogConfig,
│    version: str,
│    base_url: Optional[str],
│    temperature: float,
│    max_tokens: int,
│    timeout: int,
│    debug: bool,
⋮
│def parse_phase2_response(
│    response: str,
│    config: AudienceConfig,
│    language: str,
⋮
│def run_phase3(
│    changelogs: Dict[str, Dict[str, str]],
│    changes: List[Change],
│    changelog_config: ChangelogConfig,
│    version: str,
⋮
│def main() -> int:
⋮

src\analyzer.py:
⋮
│VALID_BUMPS = frozenset({"major", "minor", "patch"})
│
⋮
│CATEGORY_MAP = {
│    "breaking": ChangeCategory.BREAKING,
│    "security": ChangeCategory.SECURITY,
│    "feature": ChangeCategory.FEATURE,
│    "improvement": ChangeCategory.IMPROVEMENT,
│    "fix": ChangeCategory.FIX,
│    "performance": ChangeCategory.PERFORMANCE,
│    "deprecation": ChangeCategory.DEPRECATION,
│    "infrastructure": ChangeCategory.INFRASTRUCTURE,
│    "docs": ChangeCategory.DOCUMENTATION,
⋮
│IMPORTANCE_MAP = {
│    "high": Importance.HIGH,
│    "medium": Importance.MEDIUM,
│    "low": Importance.LOW,
⋮
│def extract_tag_content(response: str, tag: str) -> Optional[str]:
⋮
│def validate_bump(bump: str) -> str:
⋮
│def parse_stats(stats_content: str) -> Dict[str, int]:
⋮
│def parse_breaking_change(line: str) -> Optional[BreakingInfo]:
⋮
│def parse_change_line(line: str, index: int) -> Optional[Change]:
⋮
│def parse_changes_section(content: str) -> List[Change]:
⋮
│def parse_breaking_section(content: str, existing_changes: List[Change]) -> List[Change]:
⋮
│def parse_list_items(content: str) -> List[str]:
⋮
│def parse_phase1_response(response: str) -> AnalysisResult:
⋮
│def _word_tokenize(text: str) -> set:
⋮
│def _calculate_title_similarity(title1: str, title2: str) -> float:
⋮
│def group_related_changes(changes: List[Change]) -> List[ChangeGroup]:
⋮

src\changelog.py:
⋮
│logger = logging.getLogger(__name__)
│
⋮
│def filter_changes(changes: List[Change], config: AudienceConfig) -> List[Change]:
⋮
│def _apply_max_items_per_section(
│    changes: List[Change], sections: List[str], max_items: int
⋮
│def get_changes_by_section(changes: List[Change], sections: List[str]) -> Dict[str, List[Change]]:
⋮
│def _format_change_for_prompt(
│    change: Change,
│    config: AudienceConfig,
│    base_url: Optional[str],
⋮
│def build_changelog_prompt(
│    changes: List[Change],
│    config: AudienceConfig,
│    language: str,
│    version: str,
│    base_url: Optional[str] = None,
⋮
│def build_metadata_prompt(
│    changes: List[Change],
│    config: AudienceConfig,
│    language: str,
│    version: str,
⋮
│def parse_changelog_response(response: str) -> str:
⋮
│def parse_metadata_response(response: str) -> ReleaseMetadata:
⋮
│def generate_changelogs(
│    changes: List[Change],
│    changelog_config: ChangelogConfig,
│    version: str,
│    base_url: Optional[str],
│    llm_caller: Callable[[str], str],
⋮

src\config.py:
⋮
│@dataclass
│class ValidationConfig:
⋮
│@dataclass
│class AudienceConfig:
│    """Configuration for a single audience."""
│
⋮
│    @classmethod
│    def from_dict(cls, name: str, data: Dict[str, Any]) -> "AudienceConfig":
⋮
│@dataclass
│class ChangelogConfig:
│    """Root configuration containing all audience configs."""
│
⋮
│    @classmethod
│    def from_yaml(cls, yaml_str: str) -> "ChangelogConfig":
⋮
│def validate_audience_name(name: str) -> List[str]:
⋮
│def validate_changelog_config(config: Dict[str, Any]) -> List[str]:
⋮

src\content_scanner.py:
⋮
│class ThreatLevel(Enum):
⋮
│class ValidationMode(Enum):
⋮
│@dataclass
│class ScanResult:
⋮
│ROLE_HIJACKING = [
│    r"(?i)^\s*(system|user|assistant|human|ai)\s*:",  # Role prefixes at line start
│    r"(?i)^(Human|Assistant|System|User|AI):\s*",  # Explicit role markers
│    r"(?i)<\|?(system|user|assistant|im_start|im_end)\|?>",  # ChatML tags
│    r"(?i)\[INST\]|\[/INST\]",  # Llama format
│    r"(?i)### (instruction|response|human|assistant)",  # Alpaca format
│    r"(?i)<\|(begin|end)_of_text\|>",  # Special tokens
│    r"(?i)<<SYS>>|<</SYS>>",  # Llama2 system delimiters
⋮
│INSTRUCTION_INJECTION = [
│    r"(?i)ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?|context)",
│    r"(?i)disregard\s+(everything|all|the)\s+(above|previous|prior)",
│    r"(?i)forget\s+(everything|all|your)\s+(instructions?|training|rules|previous|prior)",
│    r"(?i)new\s+(instructions?|rules?|prompt)\s*:",
│    r"(?i)override\s+(previous|all|the)\s+(instructions?|rules?)",
│    r"(?i)you\s+are\s+now\s+(a|an|in)\s+",  # "You are now a DAN"
│    r"(?i)pretend\s+(you|to\s+be)\s+",
│    r"(?i)act\s+as\s+(if|though|a)\s+",
│    r"(?i)jailbreak|DAN|do\s+anything\s+now",
⋮
│DELIMITER_INJECTION = [
│    r"```+\s*(system|prompt|instruction)",  # Code block escape
│    r"-{3,}\s*(system|new|instruction)",  # Markdown separator abuse
│    r"#{3,}\s*(system|instruction|prompt)",  # Header injection
│    r"</?prompt>|</?instruction>|</?system>",  # XML-like tags
│    r"</?(user|assistant|message|context)>",  # More XML-like tags
│    r"\[/?INST\]",  # Instruction delimiters
│    r"<\|[a-z_]+\|>",  # Special token patterns like <|endoftext|>
│    r"={3,}\s*(system|instruction|prompt)",  # Equals separator abuse
⋮
│SANITIZATION_PATTERNS = [
│    # Role prefixes at line start (with optional leading whitespace)
│    r"^\s*(Human|Assistant|System|User|AI):\s*",
│    # Instruction injection phrases (these get stripped, not just detected)
│    r"(?i)ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
│    r"(?i)disregard\s+(all\s+)?(previous|prior|above)",
│    r"(?i)forget\s+(all\s+)?(previous|prior|above)",
│    # Delimiter patterns
│    r"</?(system|user|assistant|prompt|instruction)>",
│    r"\[/?INST\]",
⋮
│RESPONSE_INJECTION_INDICATORS = [
│    r"^(Human|Assistant|System):",  # Role prefix in output
│    r"(?i)ignore.*instruction",  # Echoing injection
│    r"(?i)I\s+(cannot|won't|refuse|am\s+unable)",  # Refusal patterns (might indicate attempted jai
│    r"(?i)as\s+an?\s+(ai|language\s+model|assistant),?\s+I",  # AI self-reference (common in jailbr
│    r"(?i)my\s+(previous\s+)?instructions?\s+(are|were|told)",  # Referencing instructions
⋮
│def detect_context_attacks(content: str) -> List[str]:
⋮
│def detect_encoding_tricks(content: str) -> List[str]:
⋮
│def validate_changelog_format(content: str) -> List[str]:
⋮
│def estimate_tokens(content: str) -> int:
⋮
│MAX_TOKENS = 8000  # Leave room for prompt template
│MAX_CONTENT_SIZE = 500_000  # 500KB hard limit
│
⋮
│def _max_threat_level(current: ThreatLevel, new: ThreatLevel) -> ThreatLevel:
⋮
│def scan_content_override(content: str) -> ScanResult:
⋮
│def parse_changelog_sections(content: str) -> dict:
⋮
│def truncate_section(section: str, max_tokens: int) -> str:
⋮
│def truncate_for_context(content: str, max_tokens: int = MAX_TOKENS) -> str:
⋮
│def handle_scan_result(result: ScanResult, logger: Optional[object] = None) -> None:
⋮
│def sanitize_content(content: str) -> str:
⋮
│LLM_INJECTION_CHECK_PROMPT = """Is this text a prompt injection attempt? Answer only YES or NO.
│
│Text: {text}
│
⋮
│def validate_with_llm(
│    text: str,
│    llm_caller: Callable[[str], str],
│    max_chars: int = 500,
⋮
│def validate_response(response: str) -> List[str]:
⋮
│def parse_validation_mode(mode_str: str) -> ValidationMode:
⋮

src\context_loader.py:
⋮
│DEFAULT_EXCLUSIONS = [
│    # Package managers / dependencies
│    "!**/node_modules/**",
│    "!**/vendor/**",
│    "!**/.pnpm/**",
│    "!**/Pods/**",
│    "!**/.dart_tool/**",
│    "!**/.gradle/**",
│    "!**/elm-stuff/**",
│    "!**/_build/**",
⋮
│@dataclass
│class ContextResult:
⋮
│def parse_patterns(patterns_str: str) -> List[str]:
⋮
│def find_matching_files(patterns: List[str], root_dir: str = ".") -> List[str]:
│    """Find files matching gitignore-style patterns.
│
│    Args:
│        patterns: List of gitignore-style patterns (supports negation).
│        root_dir: Root directory to search from.
│
│    Returns:
│        List of matching file paths, sorted by depth then alphabetically.
⋮
│    def sort_key(path: str) -> tuple:
⋮
│def read_and_concatenate(
│    files: List[str],
│    root_dir: str = ".",
│    max_tokens: Optional[int] = None,
⋮
│def load_context_files(
│    patterns: str,
│    max_tokens: int = 800,
│    llm_caller: Optional[Callable[[str], str]] = None,
│    root_dir: str = ".",
│    include_default_exclusions: bool = True,
⋮
│def detect_staleness(
│    context: str,
│    changed_files: List[str],
⋮

src\diff_analyzer.py:
⋮
│@dataclass
│class FileDiff:
│    """Represents a parsed file diff."""
│
⋮
│    @property
│    def line_count(self) -> int:
⋮
│@dataclass
│class DiffAnalysisResult:
⋮
│PRIORITY_PATTERNS = {
│    1: [
│        "openapi*.yaml",
│        "openapi*.yml",
│        "openapi*.json",
│        "*.proto",
│        "*.graphql",
│        "swagger*.yaml",
│        "swagger*.yml",
│        "swagger*.json",
⋮
│DIFF_MAP_PROMPT = """Analyze this code diff and extract ALL changes.
│
│For each change, classify it as:
│- ADDED: new endpoints, functions, fields, classes, features
│- REMOVED: deleted endpoints, functions, fields, classes, features
│- MODIFIED: changed signatures, schemas, behaviors, configurations
│
│Output in this format:
│
│<CHANGES>
⋮
│def parse_patterns(patterns_str: str) -> List[str]:
⋮
│def parse_unified_diff(diff_text: str) -> List[FileDiff]:
⋮
│def filter_diffs(diffs: List[FileDiff], exclude_patterns: str) -> List[FileDiff]:
⋮
│def get_file_priority(path: str) -> int:
⋮
│def prioritize_diffs(diffs: List[FileDiff]) -> List[FileDiff]:
│    """Sort diffs by priority (lowest priority number first).
│
│    Args:
│        diffs: List of FileDiff objects.
│
│    Returns:
│        Sorted list of FileDiff objects.
⋮
│    def sort_key(diff: FileDiff) -> Tuple[int, str]:
⋮
│def limit_diffs(
│    diffs: List[FileDiff],
│    max_files: int,
│    max_lines: int,
⋮
│def format_diff_for_prompt(diff: FileDiff) -> str:
⋮
│def extract_changes_from_diff(
│    diff_content: str,
│    llm_caller: Callable[[str], str],
⋮
│def _combine_extracted_changes(changes_list: List[str]) -> str:
⋮
│def analyze_diffs(
│    diff_text: str,
│    exclude_patterns: str,
│    max_files: int,
│    max_lines: int,
│    llm_caller: Callable[[str], str],
⋮

src\flatten.py:
⋮
│FLATTEN_PROMPT = """You are analyzing a sequence of changes to determine the NET STATE.
│
│Go through the changes chronologically and determine what ACTUALLY remains:
│
│1. If something was ADDED then later REMOVED/REVERTED → NET ZERO → exclude both
│2. If something was ADDED then IMPROVED → show only FINAL state
│3. If changes are RELATED (same feature/area) → consolidate into ONE entry
│4. REVERT commits themselves should never appear in output
│
│IMPORTANT - Version bump categories:
⋮
│def parse_flattened_response(response: str) -> str:
⋮
│def _parse_category(cat_str: str) -> ChangeCategory:
⋮
│def _parse_importance(imp_str: str) -> Importance:
⋮
│def parse_flattened_changes(response: str) -> List[Change]:
⋮
│def flatten_changes(
│    input_content: str,
│    llm_caller: Callable[[str], str],
⋮
│def flatten_changes_to_list(
│    input_content: str,
│    llm_caller: Callable[[str], str],
⋮

src\i18n.py:
⋮
│SECTION_ICONS: Dict[str, str] = {
│    "breaking": "💥",
│    "security": "🔒",
│    "features": "✨",
│    "improvements": "📈",
│    "fixes": "🐛",
│    "performance": "⚡",
│    "deprecations": "⚠️",
│    "infrastructure": "🔧",
│    "docs": "📚",
⋮
│SECTION_NAMES: Dict[str, Dict[str, str]] = {
│    "en": {
│        "breaking": "Breaking Changes",
│        "security": "Security",
│        "features": "Features",
│        "improvements": "Improvements",
│        "fixes": "Bug Fixes",
│        "performance": "Performance",
│        "deprecations": "Deprecations",
│        "infrastructure": "Infrastructure",
⋮
│TONE_DESCRIPTIONS: Dict[str, str] = {
│    "formal": "Use formal, professional language appropriate for official documentation.",
│    "casual": "Use casual, conversational language that's friendly and approachable.",
│    "professional": "Use clear, professional language that's informative but not stiff.",
│    "excited": (
│        "Use enthusiastic, energetic language that highlights the excitement of new features!"
│    ),
│    "friendly": "Use warm, friendly language that makes users feel welcomed and supported.",
⋮
│LANGUAGE_NAMES: Dict[str, str] = {
│    "en": "English",
│    "es": "Spanish",
│    "ja": "Japanese",
│    "zh": "Chinese",
│    "pt": "Portuguese",
│    "de": "German",
│    "fr": "French",
│    "ko": "Korean",
│    "it": "Italian",
⋮
│def get_section_name(section: str, language: str, use_emoji: bool = False) -> str:
⋮
│def get_tone_description(tone: str) -> str:
⋮
│def get_language_instruction(language: str) -> str:
⋮
│def get_section_icon(section: str) -> str:
⋮
│def is_language_supported(language: str) -> bool:
⋮
│def get_supported_languages() -> list:
⋮

src\input_validation.py:
⋮
│MAX_PATTERN_LENGTH = 200
│
⋮
│REGEX_TIMEOUT = 1.0
│
⋮
│class PatternCompilationError(Exception):
⋮
│class PatternTimeoutError(Exception):
⋮
│def validate_pattern_safety(pattern: str) -> List[str]:
⋮
│class TimeoutPattern:
│    """Wrapper around regex.Pattern that applies timeout on matching operations."""
│
│    def __init__(self, pattern: regex.Pattern, timeout: float):
⋮
│    def search(self, string: str, *args, **kwargs):
⋮
│    def match(self, string: str, *args, **kwargs):
⋮
│    def fullmatch(self, string: str, *args, **kwargs):
⋮
│    def findall(self, string: str, *args, **kwargs):
⋮
│    def sub(self, repl, string: str, *args, **kwargs):
⋮
│    @property
│    def pattern(self):
⋮
│def safe_compile_pattern(
│    pattern: str, timeout: float = REGEX_TIMEOUT
⋮
│@dataclass
│class InputValidationResult:
⋮
│def validate_version_format(version: str) -> List[str]:
⋮
│def validate_language_code(code: str) -> List[str]:
⋮
│def validate_filter_value(value: str, field_name: str, is_pattern: bool = False) -> List[str]:
⋮
│def validate_glob_pattern(pattern: str) -> bool:
⋮
│def validate_gitignore_pattern(pattern: str) -> List[str]:
⋮
│def validate_context_files_patterns(patterns_str: str) -> List[str]:
⋮
│def validate_context_max_tokens(value: str) -> List[str]:
⋮
│def validate_analyze_diffs(value: str) -> List[str]:
⋮
│def validate_diff_exclude_patterns(patterns: str) -> List[str]:
⋮
│def validate_diff_max_files(value: str) -> List[str]:
⋮
│def validate_diff_max_total_lines(value: str) -> List[str]:
⋮
│def validate_inputs(
│    current_version: Optional[str] = None,
│    head_ref: Optional[str] = None,
│    content_override: Optional[str] = None,
│    changelog_config: Optional[str] = None,
│    include_diffs: Optional[str] = None,
│    validation_mode: ValidationMode = ValidationMode.BOTH,
│    context_files: Optional[str] = None,
│    context_max_tokens: Optional[str] = None,
│    analyze_diffs: Optional[str] = None,
⋮
│def validate_audience_configs(configs: Dict[str, Any]) -> List[str]:
⋮

src\map_reduce.py:
⋮
│DEFAULT_CHUNK_SIZE = 2000
│DEFAULT_CHUNK_OVERLAP = 200
│DEFAULT_CHUNKING_THRESHOLD = 2000
│
⋮
│MAP_PROMPT_TEMPLATE = """Extract ALL changes described in this content.
│
│For each change, output ONE LINE in this format:
│[category|importance] Title | Description
│
│Categories: breaking, security, feature, improvement, fix, performance, deprecation, infrastructure
│Importance: high, medium, low
│
│Example:
│[feature|high] OAuth 2.0 Support | Added OAuth 2.0 authorization with new authorize endpoint
⋮
│REDUCE_PROMPT_TEMPLATE = """You have changes extracted from overlapping chunks. Many are DUPLICATES
│
│Your job: DEDUPLICATE only. Keep distinct changes as separate items.
│
│Rules:
│- REMOVE exact duplicates (same change mentioned multiple times)
│- KEEP different changes as SEPARATE items (don't merge unrelated items)
│- ALL breaking changes (each one separate)
│- ALL security changes (each one separate)
│- ALL distinct features (don't combine different features into one)
⋮
│def _parse_category(cat_str: str) -> ChangeCategory:
⋮
│def _parse_importance(imp_str: str) -> Importance:
⋮
│def _parse_change_line(line: str, index: int) -> Optional[Change]:
⋮
│def _extract_changes_from_response(response: str) -> List[Change]:
⋮
│def _changes_to_text(changes: List[Change]) -> str:
⋮
│def extract_changes_from_chunk(
│    chunk: str,
│    llm_caller: Callable[[str], str],
⋮
│def reduce_changes(
│    all_changes: List[Change],
│    llm_caller: Callable[[str], str],
⋮
│def process_large_input(
│    content: str,
│    llm_caller: Callable[[str], str],
│    chunk_size: int = DEFAULT_CHUNK_SIZE,
│    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
│    max_workers: int = 5,
│    reduce_llm_caller: Optional[Callable[[str], str]] = None,
⋮
│def determine_version_from_changes(changes: List[Change]) -> str:
⋮

src\model_config.py:
⋮
│@dataclass
│class ModelConfig:
│    """Configuration for models used in different phases.
│
│    Allows using different models for semantic analysis (Phase 1)
│    and changelog generation (Phase 2).
│
│    Examples:
│        - Use a smarter model for analysis, cheaper for formatting
│        - Use the same model for both phases
│        - Override only one phase
⋮
│    def get_analysis_model(self) -> str:
⋮
│    def get_changelog_model(self) -> str:
⋮
│    @classmethod
│    def from_env(
│        cls,
│        model: str,
│        model_analysis: Optional[str] = None,
│        model_changelog: Optional[str] = None,
⋮

src\models.py:
⋮
│class ChangeCategory(Enum):
⋮
│class Importance(Enum):
⋮
│class Tone(Enum):
⋮
│class OutputFormat(Enum):
⋮
│@dataclass
│class BreakingInfo:
⋮
│@dataclass
│class Change:
⋮
│@dataclass
│class ChangeGroup:
⋮
│@dataclass
│class ChangeStats:
│    """Statistics about changes in a release."""
│
⋮
│    @classmethod
│    def from_changes(cls, changes: List[Change]) -> "ChangeStats":
⋮
│    def to_dict(self) -> dict:
⋮
│@dataclass
│class ReleaseMetadata:
│    """Metadata for a release (per audience, per language)."""
│
⋮
│    def to_dict(self) -> dict:
⋮
│@dataclass
│class AnalysisResult:
│    """Result of Phase 1 semantic analysis."""
│
⋮
│    def __post_init__(self) -> None:
⋮

src\parser.py:
⋮
│@dataclass
│class AnalysisResult:
⋮
│def extract_tag_content(response: str, tag: str) -> Optional[str]:
⋮
│def parse_list_items(content: str) -> List[str]:
⋮
│def validate_bump(bump: str) -> str:
⋮
│def parse_response(response: str) -> AnalysisResult:
⋮

src\presets.py:
⋮
│VALID_SECTIONS = {
│    "breaking",
│    "security",
│    "features",
│    "improvements",
│    "fixes",
│    "performance",
│    "deprecations",
│    "infrastructure",
│    "docs",
⋮
│VALID_PRESETS = {"developer", "customer", "executive", "marketing", "security", "ops"}
│
⋮
│VALID_TONES = {"formal", "casual", "professional", "excited", "friendly"}
│
⋮
│VALID_OUTPUT_FORMATS = {"markdown", "html", "json", "plain"}
│
⋮
│DEVELOPER: Dict[str, Any] = {
│    "languages": ["en"],
│    "sections": [
│        "breaking",
│        "security",
│        "features",
│        "improvements",
│        "fixes",
│        "performance",
│        "infrastructure",
⋮
│CUSTOMER: Dict[str, Any] = {
│    "languages": ["en"],
│    "sections": ["breaking", "features", "improvements", "fixes"],
│    "include_commits": False,
│    "include_contributors": False,
│    "include_infrastructure": False,
│    "group_related": True,
│    "exclude_categories": ["infrastructure", "docs", "other"],
│    "benefit_focused": True,
│    "summary_only": False,
⋮
│EXECUTIVE: Dict[str, Any] = {
│    "languages": ["en"],
│    "sections": ["breaking", "features"],
│    "include_commits": False,
│    "include_contributors": False,
│    "include_infrastructure": False,
│    "group_related": True,
│    "exclude_categories": ["infrastructure", "docs", "performance", "other"],
│    "benefit_focused": True,
│    "summary_only": True,
⋮
│MARKETING: Dict[str, Any] = {
│    "languages": ["en"],
│    "sections": ["features", "improvements"],
│    "include_commits": False,
│    "include_contributors": False,
│    "include_infrastructure": False,
│    "group_related": True,
│    "exclude_categories": ["fix", "infrastructure", "docs", "other"],
│    "benefit_focused": True,
│    "summary_only": False,
⋮
│SECURITY: Dict[str, Any] = {
│    "languages": ["en"],
│    "sections": ["security", "breaking", "fixes"],
│    "include_commits": True,
│    "include_contributors": False,
│    "include_infrastructure": False,
│    "group_related": False,
│    "benefit_focused": False,
│    "summary_only": False,
│    "emojis": False,
⋮
│OPS: Dict[str, Any] = {
│    "languages": ["en"],
│    "sections": ["breaking", "infrastructure", "performance", "security"],
│    "include_commits": True,
│    "include_contributors": False,
│    "include_infrastructure": True,
│    "group_related": True,
│    "exclude_categories": ["feature", "docs", "other"],
│    "benefit_focused": False,
│    "summary_only": False,
⋮
│PRESETS: Dict[str, Dict[str, Any]] = {
│    "developer": DEVELOPER,
│    "customer": CUSTOMER,
│    "executive": EXECUTIVE,
│    "marketing": MARKETING,
│    "security": SECURITY,
│    "ops": OPS,
⋮
│def get_preset(name: str) -> Dict[str, Any]:
⋮

src\prompt_builder.py:
⋮
│@dataclass
│class CommitInfo:
⋮
│def sanitize_message(message: str, max_length: int = 500) -> str:
⋮
│def parse_commit_type(message: str) -> str:
⋮
│def has_breaking_change(message: str) -> bool:
⋮
│def get_commits(base_ref: str, head_ref: str = "HEAD") -> List[CommitInfo]:
⋮
│def get_file_diff(base_ref: str, head_ref: str, patterns: List[str], max_lines: int = 100) -> str:
⋮
│def summarize_commits_by_type(commits: List[CommitInfo]) -> str:
⋮
│def build_prompt(
│    commits: List[CommitInfo],
│    base_version: str,
│    max_commits: int = 50,
│    diff_patterns: Optional[List[str]] = None,
│    base_ref: str = "",
│    head_ref: str = "HEAD",
⋮
│def build_semantic_analysis_prompt(
│    commits: List[CommitInfo],
│    base_version: str,
│    content_override: Optional[str] = None,
│    max_commits: int = 50,
│    diff_patterns: Optional[List[str]] = None,
│    base_ref: str = "",
│    head_ref: str = "HEAD",
│    detect_breaking: bool = True,
│    generate_changelog: bool = True,
⋮

src\prompts.py:
⋮
│_env = Environment(
│    loader=BaseLoader(),
│    autoescape=False,  # Not HTML, no escaping needed
│    trim_blocks=True,
│    lstrip_blocks=True,
⋮
│DETAIL_THRESHOLD_FULL = 30      # <= this: full detail on everything
│DETAIL_THRESHOLD_MODERATE = 100  # <= this: detail on important, summarize rest
│
⋮
│def get_detail_level(commit_count: int) -> str:
⋮
│PHASE1_TEMPLATE = _env.from_string("""
│You are a semantic versioning expert analyzing changes for a software release.
│
│## Task
│Analyze the changes below SEMANTICALLY (conventional commit prefixes are NOT required).
│Determine the appropriate version bump and categorize the changes.
│
│## Current Version
│{{ base_version }}
│
⋮
│PHASE2_TEMPLATE = _env.from_string("""
│You are transforming a changelog for a specific audience.
│
│## Task
│Rewrite the changelog below for the target audience{% if language != "en" %} in {{ language_name }}
│
│## Target Audience: {{ audience_name }}
│{{ audience_description }}
│
│## Tone: {{ tone }}
⋮
│@dataclass
│class Phase1Config:
⋮
│@dataclass
│class Phase2Config:
⋮
│LANGUAGE_NAMES: Dict[str, str] = {
│    "en": "English",
│    "es": "Spanish",
│    "fr": "French",
│    "de": "German",
│    "ja": "Japanese",
│    "zh": "Chinese",
│    "pt": "Portuguese",
│    "ko": "Korean",
│    "it": "Italian",
⋮
│def get_language_name(code: str) -> str:
⋮
│def render_phase1_prompt(config: Phase1Config) -> str:
⋮
│def render_phase2_prompt(config: Phase2Config) -> str:
⋮
│FILE_TYPE_HINTS: Dict[str, str] = {
│    "openapi": "Extract endpoint changes: added/removed/modified paths, methods, parameters, respon
│    "sql": "Extract schema changes: tables, columns, indexes, constraints, migrations",
│    "proto": "Extract service/message changes: services, methods, message types, fields",
│    "graphql": "Extract schema changes: types, queries, mutations, subscriptions, fields",
│    "code": "Extract API changes: functions, classes, methods, exports, public interfaces",
⋮
│DIFF_MAP_TEMPLATE = _env.from_string("""
│Extract semantic changes from this file diff.
│
│File: {{ file_path }}
│{% if file_type_hint %}
│Focus: {{ file_type_hint }}
│{% endif %}
│
│```diff
│{{ diff_content }}
⋮
│@dataclass
│class DiffMapConfig:
│    """Configuration for diff MAP prompt generation."""
│
⋮
│    def get_file_type(self) -> Optional[str]:
⋮
│    def is_binary(self) -> bool:
⋮
│def render_diff_map_prompt(config: DiffMapConfig) -> str:
⋮

src\repo_url.py:
⋮
│def get_repository_url() -> Optional[str]:
⋮
│def convert_to_https(url: str) -> str:
⋮
│def get_commit_url(base_url: Optional[str], commit_hash: str) -> Optional[str]:
⋮
│def get_pr_url(base_url: Optional[str], pr_number: int) -> Optional[str]:
⋮
│def get_issue_url(base_url: Optional[str], issue_number: int) -> Optional[str]:
⋮

src\summarizing_map_reduce.py:
⋮
│CONTEXT_MAP_PROMPT = """Extract the KEY FACTS from this project documentation that are relevant for
│- Understanding what the project does
│- Identifying public vs internal APIs/endpoints
│- Understanding breaking change policies
│- Identifying naming conventions
│
│Be concise. Output only the essential facts, one per line.
│
│Content:
│---
⋮
│CONTEXT_REDUCE_PROMPT = """Consolidate these extracted facts into a concise project summary.
│
│Remove duplicates. Keep all unique, important facts about:
│- Project purpose
│- Public vs internal APIs
│- Breaking change policies
│- Key conventions
│
│Output a consolidated summary.
│
⋮
│@dataclass
│class SummarizeResult:
⋮
│def estimate_tokens(text: str) -> int:
⋮
│def fits_budget(text: str, max_tokens: int) -> bool:
⋮
│class SummarizingMapReduce:
│    """Generic map/reduce for summarizing content to fit a token budget.
│
│    Usage:
│        summarizer = SummarizingMapReduce(
│            map_prompt=MY_MAP_PROMPT,
│            reduce_prompt=MY_REDUCE_PROMPT,
│        )
│        result = summarizer.summarize_to_budget(
│            content=large_content,
│            max_tokens=800,
⋮
│    def __init__(
│        self,
│        map_prompt: str = CONTEXT_MAP_PROMPT,
│        reduce_prompt: str = CONTEXT_REDUCE_PROMPT,
│        chunk_size: int = 2000,
│        chunk_overlap: int = 200,
│        max_workers: int = 5,
⋮
│    def _extract_summary(self, response: str) -> str:
⋮
│    def _summarize_chunk(
│        self,
│        chunk: str,
│        llm_caller: Callable[[str], str],
⋮
│    def _reduce_summaries(
│        self,
│        summaries: List[str],
│        llm_caller: Callable[[str], str],
⋮
│    def summarize_to_budget(
│        self,
│        content: str,
│        max_tokens: int,
│        llm_caller: Callable[[str], str],
⋮
│def summarize_context(
│    content: str,
│    max_tokens: int,
│    llm_caller: Callable[[str], str],
⋮

src\templates.py:
⋮
│DEFAULT_SECTION_ORDER: List[str] = [
│    "breaking",
│    "security",
│    "features",
│    "improvements",
│    "fixes",
│    "performance",
│    "deprecations",
│    "infrastructure",
│    "docs",
⋮
│CATEGORY_TO_SECTION: Dict[ChangeCategory, str] = {
│    ChangeCategory.BREAKING: "breaking",
│    ChangeCategory.SECURITY: "security",
│    ChangeCategory.FEATURE: "features",
│    ChangeCategory.IMPROVEMENT: "improvements",
│    ChangeCategory.FIX: "fixes",
│    ChangeCategory.PERFORMANCE: "performance",
│    ChangeCategory.DEPRECATION: "deprecations",
│    ChangeCategory.INFRASTRUCTURE: "infrastructure",
│    ChangeCategory.DOCUMENTATION: "docs",
⋮
│def format_section_header(
│    section: str,
│    language: str,
│    use_emoji: bool,
│    output_format: str,
⋮
│def format_change_item(
│    change: Change,
│    config: AudienceConfig,
│    base_url: Optional[str] = None,
⋮
│def format_breaking_change(
│    change: Change,
│    config: AudienceConfig,
⋮
│def render_changelog(
│    changes: List[Change],
│    config: AudienceConfig,
│    language: str,
│    version: str,
│    base_url: Optional[str] = None,
⋮
│def _format_link(text: str, url: str, output_format: str) -> str:
⋮

src\text_splitter.py:
⋮
│def _split_text_with_regex(
│    text: str, separator: str, keep_separator: bool
⋮
│class RecursiveCharacterTextSplitter:
│    """Split text by recursively looking at characters.
│
│    Recursively tries to split by different characters to find one
│    that works, preserving natural boundaries like paragraphs and sentences.
⋮
│    def __init__(
│        self,
│        separators: Optional[List[str]] = None,
│        keep_separator: bool = True,
│        is_separator_regex: bool = False,
│        length_function: Optional[Callable[[str], int]] = len,
│        strip_whitespace: bool = True,
│        chunk_size: int = 4000,
│        chunk_overlap: int = 200,
⋮
│    def _join_docs(self, docs: List[str], separator: str) -> Optional[str]:
⋮
│    def _merge_splits(self, splits: Iterable[str], separator: str) -> List[str]:
⋮
│    def _split_text(self, text: str, separators: List[str]) -> List[str]:
⋮
│    def split_text(self, text: str) -> List[str]:
⋮
│def chunk_with_overlap(
│    content: str,
│    chunk_size: int = 2000,
│    overlap: int = 200,
⋮
│def needs_chunking(content: str, threshold: int = 2000) -> bool:
⋮

src\validation.py:
⋮
│@dataclass
│class ValidationConfig:
⋮
│@dataclass
│class ValidationResult:
⋮
│PLACEHOLDER_PATTERNS = [
│    "[INSERT",
│    "TODO:",
│    "XXX",
│    "[TBD]",
│    "PLACEHOLDER",
│    "[ADD",
│    "[FILL",
│    "[YOUR",
│    "...",  # Often indicates truncation
⋮
│INTERNAL_CONTENT_PATTERNS = [
│    # Repository references
│    r"`[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+`",  # `org/repo` format
│    r"in \w+/\w+",  # "in org/repo" format
│    r"from \w+/\w+",  # "from org/repo" format
│    # Internal infrastructure terms
│    r"\bCI/CD\b",
│    r"\bGitHub Actions\b",
│    r"\bworkflow\b",
│    r"\bmigration\s+file\b",
⋮
│def detect_language(text: str) -> str:
⋮
│def check_markdown_structure(content: str) -> List[str]:
⋮
│def check_html_structure(content: str) -> List[str]:
⋮
│def check_references_changes(content: str, changes: List[Change]) -> List[str]:
⋮
│def check_empty_sections(content: str) -> List[str]:
⋮
│def check_internal_content(
│    content: str,
│    preset: Optional[str] = None,
│    skip_internal_check: bool = False,
│    custom_patterns: Optional[List[str]] = None,
⋮
│def strip_empty_sections(content: str) -> str:
⋮
│def validate_changelog(
│    changelog: str,
│    language: str,
│    changes: List[Change],
│    config: ValidationConfig,
│    output_format: str = "markdown",
│    preset: Optional[str] = None,
│    skip_internal_check: bool = False,
│    internal_domain_patterns: Optional[List[str]] = None,
⋮
│def generate_fallback_changelog(
│    version: str,
│    changes: List[Change],
│    language: str = "en",
⋮

src\version.py:
⋮
│@dataclass
│class SemanticVersion:
│    """Represents a semantic version."""
│
⋮
│    def __str__(self) -> str:
⋮
│    def bump(self, bump_type: str) -> "SemanticVersion":
⋮
│    def _bump_prerelease(self) -> "SemanticVersion":
⋮
│def parse_version(version_str: str) -> SemanticVersion:
⋮
│def detect_latest_tag() -> Optional[str]:
⋮
│def is_shallow_clone() -> bool:
⋮

tests\integration\test_prompt_injection_live.py:
⋮
│def call_llm(prompt: str) -> str:
⋮
│def main():
⋮
```
