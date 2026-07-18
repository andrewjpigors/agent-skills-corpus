---
name: mox
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging mox. Use this skill whenever modifying mox configurations or adding related functionality.
---
# mox

## File Tree

```text
mox/
├── assets
├── modules
│   └── mox (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/mox`

```python
.github\pull_request_template.md

.github\workflows\release.yaml

.python-version

.roo\rules\language-python\anti-patterns.md

.roo\rules\language-python\architecture-and-structure.md

.roo\rules\language-python\code-style-and-formatting.md

.roo\rules\language-python\configuration-and-environment.md

.roo\rules\language-python\dependency-management.md

.roo\rules\language-python\documentation-and-comments.md

.roo\rules\language-python\error-handling.md

.roo\rules\language-python\logging-and-observability.md

.roo\rules\language-python\naming-conventions.md

.roo\rules\language-python\performance-and-optimization.md

.roo\rules\language-python\security-and-validation.md

.roo\rules\language-python\testing-standards.md

.roo\rules\language-python\type-safety.md

.roo\rules\package-mox\anti-patterns.md

.roo\rules\package-mox\architecture-and-structure.md

.roo\rules\package-mox\code-style-and-formatting.md

.roo\rules\package-mox\configuration-and-environment.md

.roo\rules\package-mox\dependency-management.md

.roo\rules\package-mox\documentation-and-comments.md

.roo\rules\package-mox\error-handling.md

.roo\rules\package-mox\logging-and-observability.md

.roo\rules\package-mox\naming-conventions.md

.roo\rules\package-mox\performance-and-optimization.md

.roo\rules\package-mox\security-and-validation.md

.roo\rules\package-mox\testing-standards.md

.roo\rules\package-mox\type-safety.md

.vscode\launch.json

.vscode\settings.json

CHANGELOG.md

LICENSE

README.md

apps\mox-api\.claude\skills\cli-commands\SKILL.md

apps\mox-api\.claude\skills\raw-app\SKILL.md

apps\mox-api\.claude\skills\resources\SKILL.md

apps\mox-api\.claude\skills\schedules\SKILL.md

apps\mox-api\.claude\skills\triggers\SKILL.md

apps\mox-api\.claude\skills\write-flow\SKILL.md

apps\mox-api\.claude\skills\write-script-bash\SKILL.md

apps\mox-api\.claude\skills\write-script-bigquery\SKILL.md

apps\mox-api\.claude\skills\write-script-bun\SKILL.md

apps\mox-api\.claude\skills\write-script-bunnative\SKILL.md

apps\mox-api\.claude\skills\write-script-csharp\SKILL.md

apps\mox-api\.claude\skills\write-script-deno\SKILL.md

apps\mox-api\.claude\skills\write-script-duckdb\SKILL.md

apps\mox-api\.claude\skills\write-script-go\SKILL.md

apps\mox-api\.claude\skills\write-script-graphql\SKILL.md

apps\mox-api\.claude\skills\write-script-java\SKILL.md

apps\mox-api\.claude\skills\write-script-mssql\SKILL.md

apps\mox-api\.claude\skills\write-script-mysql\SKILL.md

apps\mox-api\.claude\skills\write-script-nativets\SKILL.md

apps\mox-api\.claude\skills\write-script-php\SKILL.md

apps\mox-api\.claude\skills\write-script-postgresql\SKILL.md

apps\mox-api\.claude\skills\write-script-powershell\SKILL.md

apps\mox-api\.claude\skills\write-script-python3\SKILL.md

apps\mox-api\.claude\skills\write-script-rlang\SKILL.md

apps\mox-api\.claude\skills\write-script-rust\SKILL.md

apps\mox-api\.claude\skills\write-script-snowflake\SKILL.md

apps\mox-api\AGENTS.md

apps\mox-api\CLAUDE.md

apps\mox-api\README.md

apps\mox-api\app\mox_api\__init__.py

apps\mox-api\f\mox\README.md

apps\mox-api\pyproject.toml

apps\mox-cli\README.md

apps\mox-cli\pyproject.toml

apps\mox-cli\src\mox_cli\__init__.py

apps\mox-cli\src\mox_cli\client.py

apps\mox-cli\src\mox_cli\commands\__init__.py

apps\mox-cli\src\mox_cli\commands\composite.py:
⋮
│@composite_app.command("render")
│def _composite_render_cmd(
│    template: Optional[str] = typer.Option(None, help="The .mox template file path"),
│    mod: Optional[List[str]] = typer.Option(None, "--mod", "--modification", help="Modifications in
│    output: Optional[str] = typer.Option(None, help="The final output image path")
⋮
│@composite_app.command("recolor")
│def _composite_recolor_cmd(
│    base: Optional[str] = typer.Option(None, help="The base image path"),
│    alpha: Optional[str] = typer.Option(None, help="The alpha mask image path"),
│    hex_color: Optional[str] = typer.Option(None, "--hex", "--color", help="The HEX color code (e.g
│    output: Optional[str] = typer.Option(None, "--output", help="The final output image path")
⋮

apps\mox-cli\src\mox_cli\commands\config.py:
⋮
│@config_app.callback(invoke_without_command=True)
│def config_main(
│    ctx: typer.Context,
│    key: Optional[str] = typer.Argument(None, help="The configuration key (e.g. blur_radius)"),
│    value: Optional[str] = typer.Argument(None, help="The value to set")
⋮
│@config_app.command("setup")
│def config_setup():
⋮

apps\mox-cli\src\mox_cli\commands\template.py:
⋮
│@template_app.command("build")
│def _template_build_cmd(
│    width: Optional[int] = typer.Option(None, "--width", help="The real width of the print area"),
│    height: Optional[int] = typer.Option(None, "--height", help="The real height of the print area"
│    scene: Optional[str] = typer.Option(None, help="Scene name (e.g. front, back)"),
│    placement: Optional[str] = typer.Option(None, help="Placement name for individual mode"),
│    color: Optional[str] = typer.Option(None, help="Color name for individual mode"),
│    psd: Optional[str] = typer.Option(None, help="The path to the source PSD file for automated bui
│    obj: Optional[str] = typer.Option(None, "--obj", "--wavefront", help="The path to a 3D OBJ file
│    base_color: Optional[str] = typer.Option(None, help="The base color image path"),
│    alpha: Optional[str] = typer.Option(None, help="The alpha mask image path"),
⋮

apps\mox-cli\src\mox_cli\commands\texture.py:
⋮
│@texture_app.command("bake")
│def _texture_bake(
│    base_color: Optional[str] = typer.Option(None, "--base-color", help="The base color image path"
│    alpha: Optional[str] = typer.Option(None, "--alpha", help="The alpha mask image path"),
│    obj: Optional[str] = typer.Option(None, "--obj", "--wavefront", help="The 3D mesh OBJ file path
│    type: str = typer.Option("all", help="Type of texture: occlusion, emissive, normal, or all (def
│    output: Optional[str] = typer.Option(None, help="The output image path (if omitted, derives fro
│    blur: Optional[float] = typer.Option(None, "--blur", help="Blur radius for normal map (override
⋮

apps\mox-cli\src\mox_cli\main.py

apps\mox-cli\src\mox_cli\utils.py:
⋮
│def get_image_files():
⋮
│def get_obj_files():
⋮

apps\mox-mcp\README.md

apps\mox-mcp\pyproject.toml

apps\mox-mcp\src\mox_mcp\__init__.py

packages\mox\.python-version

packages\mox\README.md

packages\mox\pdm.lock

packages\mox\pyproject.toml

packages\mox\src\mox\__init__.py

packages\mox\src\mox\client.py:
⋮
│class MoxClient:
│    def __init__(self, **kwargs):
│        """
│        Initialize the Mox SDK.
│        :param kwargs: Optional overrides for settings (e.g., log_level, organization_name, s3_buck
│        """
│        # Update global settings with any provided kwargs
│        updated = False
│        for k, v in kwargs.items():
│            if hasattr(settings, k) and v is not None:
│                setattr(settings, k, v)
⋮
│    def render(self, request: RenderRequest) -> File:
⋮
│    def render_batch(self, batch_request: BatchRenderRequest) -> List[File]:
⋮
│    def bake_occlusion_map(self, base_color_path: str, alpha_path: str, output_path: str) -> None:
⋮
│    def bake_emissive_map(self, base_color_path: str, alpha_path: str, output_path: str, brightness
⋮
│    def bake_normal_map_from_image(self, base_color_path: str, alpha_path: str, output_path: str, *
⋮
│    def bake_normal_map_from_obj(self, obj_path: str, base_color_no_bg_path: str, alpha_path: str, 
⋮
│    def extract_psd(self, psd_path: str) -> Dict[str, Any]:
⋮
│    def bake_all_maps(self, base_color: str, alpha: str, obj: Optional[str] = None, type: str = "al
⋮
│    def build_template_from_psd(self, psd_path: str, output_dir: str, scene: str, obj_path: Optiona
⋮
│    def build_template_from_images(self, name: str, base_color: str, alpha: str, normal: str, emiss
⋮
│    def get_placements(self, template_path: str) -> List[str]:
⋮
│    def recolor(self, base_path: str, alpha_path: str, hex_color: str, output_path: str) -> None:
⋮

packages\mox\src\mox\config\__init__.py

packages\mox\src\mox\config\main.py:
⋮
│def get_config_path() -> Path:
⋮
│def _load_json_config() -> dict:
⋮
│class Settings(LoggingSettings, BaseSettings):
│    im_bin_path: str = Field(default_factory=lambda: get_bin_path()[0])
⋮
│    @classmethod
│    def load(cls, **kwargs) -> "Settings":
⋮
│    def save(self) -> None:
⋮

packages\mox\src\mox\core\__init__.py

packages\mox\src\mox\core\file.py:
⋮
│class File:
│    """
│    A wrapper around a local temporary file, with a mandatory filename and mimetype.
│    Supports lazy uploading to S3 to generate a presigned URL.
│    If created within a Workspace context, the file is placed in the workspace's directory.
│    """
│    def __init__(self, path: str, filename: str, mimetype: str):
⋮
│    @property
│    def presigned_url(self) -> Optional[str]:
⋮
│    def cleanup(self) -> None:
⋮
│    def __enter__(self) -> 'File':
⋮
│    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
⋮
│    @classmethod
│    def _get_temp_path(cls, filename: str) -> str:
⋮
│    @classmethod
│    def create_empty(cls, filename: str, mimetype: Optional[str] = None, touch: bool = False) -> 'F
⋮
│    @classmethod
│    def from_extension(cls, ext: str) -> 'File':
⋮
│    @classmethod
│    def from_bytes(cls, data: bytes, filename: str, mimetype: Optional[str] = None) -> 'File':
⋮
│    @classmethod
│    def from_url(cls, url: str, filename: Optional[str] = None, mimetype: Optional[str] = None) -> 
⋮
│    @classmethod
│    def from_path(cls, source_path: str, filename: Optional[str] = None) -> 'File':
⋮
│    @classmethod
│    def generate_render_filename(cls) -> str:
⋮
│    @classmethod
│    def generate_template_filename(cls) -> str:
⋮
│    @classmethod
│    def generate_texture_filename(cls, type: str, blur: Optional[float] = None) -> str:
⋮

packages\mox\src\mox\core\template.py:
⋮
│class BaseTemplate(ABC):
│    """
│    Universal contract for all templates (GLTF, SVG, Video, etc.).
⋮
│    @classmethod
│    @abstractmethod
│    def load(cls, source: Union[str, BinaryIO]) -> "BaseTemplate":
⋮
│    @abstractmethod
│    def build(self, output_path: str) -> str:
⋮
│    @abstractmethod
│    def extract_asset(self, name_or_uri: str) -> File:
⋮
│    @abstractmethod
│    def get_dimensions(self, scene_name: str) -> Tuple[int, int]:
⋮
│    @abstractmethod
│    def add_asset(self, file_path: str, uri: Optional[str] = None) -> Any:
⋮
│class TemplateFactory:
│    """
│    Registry and factory for templates.
⋮
│    @classmethod
│    def register(cls, extension: str, template_class: Type[BaseTemplate]) -> None:
⋮
│    @classmethod
│    def load(cls, source: Union[str, BinaryIO]) -> BaseTemplate:
⋮

packages\mox\src\mox\core\workspace.py:
⋮
│class Workspace:
│    """
│    An implicit environment builder that manages a temporary directory for an execution context.
│    It uses contextvars to make the directory available to File objects created within the context.
│    """
│    def __init__(self):
⋮
│    def __enter__(self) -> 'Workspace':
⋮
│    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
⋮

packages\mox\src\mox\exceptions\__init__.py

packages\mox\src\mox\exceptions\mockup.py:
│class ImageMagickError(Exception):
⋮

packages\mox\src\mox\integrations\__init__.py

packages\mox\src\mox\integrations\gltf\__init__.py

packages\mox\src\mox\integrations\gltf\service.py:
⋮
│def pack_gltf_to_glb(gltf_path: str, glb_path: str) -> str:
⋮

packages\mox\src\mox\integrations\imagemagick\__init__.py

packages\mox\src\mox\integrations\imagemagick\service.py:
⋮
│def get_bin_path() -> List[str]:
⋮
│def run_im(args: List[Union[str, File]], capture_output: bool = False) -> Optional[str]:
⋮

packages\mox\src\mox\integrations\photoshop\__init__.py

packages\mox\src\mox\integrations\photoshop\service.py:
⋮
│def get_psd_config_path() -> Path:
⋮
│def load_psd_config() -> dict:
⋮
│def extract_psd_to_tempdir(psd: File) -> Dict[str, Any]:
│    if win32com is None:
⋮
│    try:
│        # We replace \\ with / for JSX path parsing
│        safe_temp = temp_dir.replace("\\", "/")
│        
⋮
│        def sanitize(s: str) -> str:
⋮

packages\mox\src\mox\modules\__init__.py

packages\mox\src\mox\modules\image\__init__.py

packages\mox\src\mox\modules\image\modules\__init__.py

packages\mox\src\mox\modules\image\modules\composite\__init__.py

packages\mox\src\mox\modules\image\modules\composite\service.py:
⋮
│def _prepare_decal_area(mod: PlacementRequest, decal_def: Any, output_file: File) -> None:
⋮
│def _get_uri(template: GLTFTemplate, index: int) -> str:
⋮
│def _resolve_scene(gltf: Any, perspective: str) -> Tuple[Any, Any, Any, Any]:
⋮
│def _resolve_material(gltf: Any, prim: Any, color: str, template: GLTFTemplate) -> Tuple[int, str]:
⋮
│def _apply_decal(
│    template: GLTFTemplate,
│    decal_def: Any,
│    mod: PlacementRequest,
│    active_layer: File,
│    magic_pixel_cache: File,
│    idx: int,
│    first_rendered_slot: bool
⋮
│def bake_recolor_textures(base: File, alpha: File, occlusion: File, emissive: File) -> None:
⋮
│def apply_recolor(base: File, alpha: File, occlusion: File, emissive: File, hex_color: str, output:
⋮
│def recolor(base: File, alpha: File, hex_color: str, output: File) -> None:
⋮
│@webhook_response
│def render(request: RenderRequest) -> File:
⋮
│@webhook_response
│def render_batch(batch_request: BatchRenderRequest) -> List[File]:
⋮

packages\mox\src\mox\modules\image\modules\template\__init__.py

packages\mox\src\mox\modules\image\modules\template\schemas.py:
⋮
│class PlacementRequest(BaseModel):
⋮
│class RenderRequest(BaseModel):
│    template: Union[File, str]
⋮
│    @field_validator("perspective", "color", mode="before")
│    @classmethod
│    def flatten_name(cls, v):
⋮
│class BatchRenderRequest(BaseModel):
⋮

packages\mox\src\mox\modules\image\modules\template\service.py:
⋮
│class GLTFTemplate(BaseTemplate):
│    def __init__(self, name: Optional[str] = None, version: str = "2.0", definition: Optional[GLTFM
│        self.name = name
│        self._def = definition
│        self._gltf2 = gltf2
│        
│        if definition is None:
│            self.asset_info = Asset(version=version, generator="mox-builder")
│            self.images: List[GLTFImage] = []
│            self.textures: List[Texture] = []
│            self.materials: List[Material] = []
⋮
│    @classmethod
│    def load(cls, source: Union[str, BinaryIO]) -> "GLTFTemplate":
│        logger.debug(f"Loading GLTFTemplate from {source}")
│        
⋮
│        def clean_dict(d):
⋮
│    @property
│    def gltf(self) -> GLTFModel:
⋮
│    def extract_asset(self, name_or_uri: str) -> File:
⋮
│    def get_dimensions(self, scene_name: str) -> Tuple[int, int]:
⋮
│    def close(self):
⋮
│    def add_asset(self, file_path: str, uri: Optional[str] = None) -> int:
⋮
│    def add_texture(self, image_index: int, name: Optional[str] = None) -> int:
⋮
│    def add_material(self, name: str, base_color_texture_index: int) -> int:
⋮
│    def add_mesh(
│        self, 
│        name: str, 
│        material_mappings: List[Tuple[int, int]], # list of (material_index, variant_index)
│        decal_mappings: List[Tuple[int, int]] = None # list of (decal_index, variant_index)
⋮
│    def add_node(self, name: str, mesh_index: int) -> int:
⋮
│    def add_scene(self, name: str, node_indices: List[int], alphaTexture: Optional[int] = None, dim
⋮
│    def register_color_variant(self, name: str) -> int:
⋮
│    def register_decal(
│        self, 
│        name: str, 
│        dimensions: Tuple[int, int],
│        alignment: Alignment = Alignment.CENTER,
│        texCoordUTexture: Optional[int] = None,
│        texCoordVTexture: Optional[int] = None,
│        alphaTexture: Optional[int] = None,
│        normalTexture: Optional[int] = None,
│        emissiveTexture: Optional[int] = None,
⋮
│    @classmethod
│    def merge(cls, builders: List['GLTFTemplate'], name: str = "MergedTemplate") -> 'GLTFTemplate':
⋮
│    def build(self, output_path: str) -> str:
⋮
│def get_placements(template_path: str) -> List[str]:
⋮
│def build_template_from_psd(psd_path: str, output_dir: str, scene: str, obj_path: Optional[str] = N
│    """Builds a .glb template from a PSD file."""
⋮
│    def sanitize(s: str) -> str:
⋮
│def build_template_from_images(name: str, base_color: str, alpha: str, normal: str, emissive: str, 
⋮

packages\mox\src\mox\modules\image\modules\tex_coord\__init__.py

packages\mox\src\mox\modules\image\modules\tex_coord\service.py:
⋮
│def _resample_curve(curve_points: list[list[int]], num_points: int) -> list[list[float]]:
⋮
│def _get_contour_segment(pts: list[list[int]], start_idx: int, end_idx: int) -> list[list[int]]:
⋮
│def _create_source_edge(start_pt: list[float], end_pt: list[float], num_points: int) -> list[list[f
⋮
│def from_image(image_file: File, src_width: int, src_height: int, pixel_step: int = 4) -> list[list
⋮
│def generate(tex_coord_file: File, canvas_w: int, canvas_h: int, slot_name: str, src_w: int = None,
⋮

packages\mox\src\mox\modules\image\modules\texture\__init__.py

packages\mox\src\mox\modules\image\modules\texture\service.py:
⋮
│def bake_occlusion_map(base_color: File, alpha: File, output: File) -> None:
⋮
│def bake_emissive_map(base_color: File, alpha: File, output: File, brightness_delta: float = 30.0) 
⋮
│def bake_normal_map_from_image(base_color: File, alpha: File, output: File, brightness_delta: Optio
⋮
│def bake_normal_map_from_obj(obj: File, base_color_no_bg: File, alpha: File, output: File, resoluti
⋮
│def bake_all_maps(base_color: File, alpha: File, obj: Optional[File] = None, type: str = "all", out
⋮

packages\mox\src\mox\modules\vector\__init__.py

packages\mox\src\mox\modules\video\__init__.py

packages\mox\src\mox\schemas\__init__.py

packages\mox\src\mox\schemas\gltf.py:
⋮
│@unique
│class Alignment(str, Enum):
⋮
│class Asset(BaseModel):
⋮
│class Image(BaseModel):
⋮
│class Texture(BaseModel):
⋮
│class TextureInfo(BaseModel):
⋮
│class PBRMetallicRoughness(BaseModel):
⋮
│class Material(BaseModel):
⋮
│class VariantDef(BaseModel):
⋮
│class VariantMapping(BaseModel):
⋮
│class KHRMaterialsVariantsExtension(BaseModel):
⋮
│class SNAPPDecalVariantMapping(BaseModel):
⋮
│class SNAPPDecalsExtension(BaseModel):
⋮
│class PrimitiveExtensions(BaseModel):
⋮
│class Primitive(BaseModel):
⋮
│class Mesh(BaseModel):
⋮
│class Node(BaseModel):
⋮
│class SNAPPSceneExtension(BaseModel):
⋮
│class SceneExtensions(BaseModel):
⋮
│class Scene(BaseModel):
⋮
│class KHRMaterialsVariantsRoot(BaseModel):
⋮
│class DecalDef(BaseModel):
⋮
│class SNAPPDecalsRoot(BaseModel):
⋮
│class GLTFExtensions(BaseModel):
⋮
│class Buffer(BaseModel):
⋮
│class BufferView(BaseModel):
⋮
│class Accessor(BaseModel):
⋮
│class GLTFModel(BaseModel):
⋮

packages\mox\src\mox\services\__init__.py

packages\mox\src\mox\utils\__init__.py

packages\mox\src\mox\utils\s3.py:
⋮
│class S3Config(BaseModel):
⋮
│def upload_and_presign(file_path: str, object_name: str, mimetype: str, s3_config: Dict[str, Any]) 
⋮

packages\mox\src\mox\utils\webhook.py:
⋮
│class WebhookSuccessPayload(BaseModel):
⋮
│class WebhookErrorPayload(BaseModel):
⋮
│def _send_webhook(url: str, payload: dict) -> None:
⋮
│def webhook_response(func: Callable) -> Callable:
│    """
│    Decorator that intercepts the return value or exception of a function
│    and sends it to a webhook URL if `callback_url` is present in the first argument.
│    """
│    @wraps(func)
│    def wrapper(request, *args, **kwargs):
⋮

packages\mox\tests\conftest.py:
⋮
│class MockLoggingSettings:
⋮

packages\mox\tests\data\golden\renders\complex_render.jpg

packages\mox\tests\data\golden\renders\render.jpg

packages\mox\tests\data\golden\templates\complex-item-complex-cust-front-center-white-test-org.glb

packages\mox\tests\data\golden\templates\test-item-test-cust-front-center-white-test-org.glb

packages\mox\tests\data\golden\tex_coord\complex_points.json

packages\mox\tests\data\golden\tex_coord\points.json

packages\mox\tests\data\golden\textures\base_adjustment.jpg

packages\mox\tests\data\golden\textures\base_displacement.png

packages\mox\tests\data\golden\textures\base_lighting.png

packages\mox\tests\data\golden\textures\complex_adjustment.jpg

packages\mox\tests\data\golden\textures\complex_displacement.png

packages\mox\tests\data\golden\textures\complex_lighting.png

packages\mox\tests\data\inputs\base.png

packages\mox\tests\data\inputs\complex_base.png

packages\mox\tests\data\inputs\complex_design.png

packages\mox\tests\data\inputs\complex_mask.png

packages\mox\tests\data\inputs\complex_tex_coord.png

packages\mox\tests\data\inputs\design.png

packages\mox\tests\data\inputs\mask.png

packages\mox\tests\data\inputs\sample.psd

packages\mox\tests\data\inputs\tex_coord.png

packages\mox\tests\e2e\test_composite_render.py:
⋮
│def compare_images(img1_path, img2_path, threshold=0.1):
⋮
│@pytest.fixture
│def client():
⋮
│def test_composite_render(client, tmp_path):
⋮
│def test_composite_complex_render(client, tmp_path):
⋮

packages\mox\tests\e2e\test_recolor_pipeline.py:
⋮
│def create_test_image(path, color, size=(100, 100)):
⋮
│def create_test_mask(path, size=(100, 100)):
⋮
│def test_cli_recolor():
⋮
│@patch("mox.integrations.photoshop.service.extract_psd_to_tempdir")
│def test_template_generation_dynamic_priority(mock_extract_psd):
│    # Test that P_INDEX = 1 forces dynamic generation
│    settings.p_index = 1
│    
│    with tempfile.TemporaryDirectory() as tmpdir:
│        # Create mock PSD structure
│        client = MoxClient()
│        
⋮
│        def side_effect(psd):
⋮

packages\mox\tests\e2e\test_template_build.py:
⋮
│@pytest.fixture
│def client():
⋮
│def test_build_template(client, tmp_path):
⋮
│def test_build_complex_template(client, tmp_path):
⋮

packages\mox\tests\e2e\test_texture_generation.py:
⋮
│def compare_images(img1_path, img2_path, threshold=0.1):
⋮
│@pytest.fixture
│def client():
⋮
│def test_bake_occlusion_map(client, tmp_path):
⋮
│def test_bake_emissive_map(client, tmp_path):
⋮
│def test_bake_normal_map_from_image(client, tmp_path):
⋮

packages\mox\tests\integration\test_blender_integration.py:
⋮
│def test_bpy_import_and_basic_ops():
⋮

packages\mox\tests\integration\test_config_management.py:
⋮
│def test_settings_load_and_save(tmp_path):
⋮
│def test_settings_env_vars(tmp_path, monkeypatch):
⋮
│def test_im_bin_path_precedence(tmp_path, monkeypatch):
⋮
│def test_psd_config_load_and_save(tmp_path):
⋮

packages\mox\tests\integration\test_gltf_integration.py:
⋮
│def test_pack_gltf_to_glb(tmp_path):
⋮
│def test_pack_gltf_to_glb_file_not_found(tmp_path):
⋮

packages\mox\tests\integration\test_imagemagick_integration.py:
⋮
│def test_get_bin_path_fallback():
⋮
│def test_imagemagick_basic_operation(tmp_path):
⋮

packages\mox\tests\integration\test_s3_uploads.py:
⋮
│def test_upload_and_presign(tmp_path):
⋮
│def test_upload_and_presign_gcs(tmp_path):
⋮

packages\mox\tests\integration\test_webhooks.py:
⋮
│@patch("mox.modules.image.modules.composite.service.TemplateFactory.load")
⋮
│def test_render_template_webhook(mock_post, mock_run_im, mock_workspace, mock_load):
⋮
│@patch("mox.modules.image.modules.composite.service.render")
│@patch("mox.utils.webhook.requests.post")
│def test_render_batch_webhook(mock_post, mock_render):
⋮

packages\mox\tests\unit\core\test_template.py:
⋮
│class MockTemplate(BaseTemplate):
│    @classmethod
│    def load(cls, source):
⋮
│    def build(self, output_path):
⋮
│    def extract_asset(self, name_or_uri):
⋮
│    def get_dimensions(self, scene_name):
⋮
│    def add_asset(self, file_path, uri=None):
⋮
│def test_template_factory_register_and_load():
⋮
│def test_template_factory_load_bytes():
⋮

packages\mox\tests\unit\integrations\imagemagick\test_service.py:
⋮
│@patch("mox.integrations.imagemagick.service.subprocess.run")
│def test_run_im_success(mock_run):
⋮
│@patch("mox.integrations.imagemagick.service.subprocess.run")
│def test_run_im_called_process_error(mock_run):
⋮
│@patch("mox.integrations.imagemagick.service.subprocess.run")
│def test_run_im_file_not_found_error(mock_run):
⋮

packages\mox\tests\unit\modules\image\modules\composite\__init__.py

packages\mox\tests\unit\modules\image\modules\composite\test_service.py:
⋮
│def create_test_image(path, color, size=(100, 100)):
⋮
│def create_test_mask(path, size=(100, 100)):
⋮
│def test_prepare_decal_area_local_file():
⋮
│@patch("mox.modules.image.modules.composite.service.File.from_url")
│def test_prepare_decal_area_uri(mock_from_url):
⋮
│def test_prepare_decal_area_missing_data():
⋮
│def test_resolve_scene_success():
⋮
│def test_resolve_scene_fallback():
⋮
│def test_resolve_scene_not_found():
⋮
│def test_resolve_material_success():
⋮
│def test_resolve_material_not_found():
⋮
│@patch("mox.modules.image.modules.composite.service._prepare_decal_area")
⋮
│def test_apply_decal_full(mock_load, mock_imread, mock_remap, mock_imwrite, mock_run_im, mock_prepa
⋮
│@patch("mox.modules.image.modules.composite.service._prepare_decal_area")
│@patch("mox.modules.image.modules.composite.service.run_im")
│def test_apply_decal_flat(mock_run_im, mock_prepare):
⋮
│@patch("mox.modules.image.modules.composite.service.TemplateFactory.load")
⋮
│def test_render_success(mock_run_im, mock_apply, mock_res_mat, mock_res_scene, mock_load):
⋮
│@patch("mox.modules.image.modules.composite.service.TemplateFactory.load")
│def test_render_invalid_template(mock_load):
⋮
│@patch("mox.modules.image.modules.composite.service.render")
│def test_render_batch_success(mock_render):
⋮
│@patch("mox.modules.image.modules.composite.service.render")
│def test_render_batch_failure(mock_render):
⋮
│@patch("mox.modules.image.modules.composite.service.run_im")
│@patch("mox.modules.image.modules.composite.service.subprocess.run")
│def test_bake_recolor_textures(mock_run, mock_run_im):
⋮
│@patch("mox.modules.image.modules.composite.service.run_im")
│@patch("mox.modules.image.modules.composite.service.subprocess.run")
│def test_bake_recolor_textures_failure(mock_run, mock_run_im):
⋮
│@patch("mox.modules.image.modules.composite.service.run_im")
│@patch("mox.modules.image.modules.composite.service.subprocess.run")
│def test_apply_recolor(mock_run, mock_run_im):
⋮
│@patch("mox.modules.image.modules.composite.service.run_im")
│@patch("mox.modules.image.modules.composite.service.subprocess.run")
│def test_apply_recolor_failure(mock_run, mock_run_im):
⋮
│@patch("mox.modules.image.modules.composite.service.bake_recolor_textures")
│@patch("mox.modules.image.modules.composite.service.apply_recolor")
│def test_recolor(mock_apply, mock_bake):
⋮

packages\mox\tests\unit\modules\image\modules\template\__init__.py

packages\mox\tests\unit\modules\image\modules\template\test_service.py:
⋮
│def test_template_builder(tmp_path):
⋮
│def test_template_extractor(tmp_path):
⋮

packages\mox\tests\unit\modules\image\modules\tex_coord\__init__.py

packages\mox\tests\unit\modules\image\modules\tex_coord\test_service.py:
⋮
│def test_from_image(tmp_path):
⋮
│@patch("subprocess.run")
│@patch("numpy.save")
│def test_generate(mock_save, mock_run, tmp_path):
│    # Create a real image
│    img_path = str(tmp_path / "tex_coord.png")
⋮
│    def mock_run_side_effect(cmd, *args, **kwargs):
⋮

packages\mox\tests\unit\modules\image\modules\texture\__init__.py

packages\mox\tests\unit\modules\image\modules\texture\test_service.py:
⋮
│@patch("mox.modules.image.modules.texture.service.run_im")
│def test_bake_occlusion_map(mock_run_im):
⋮
│@patch("mox.modules.image.modules.texture.service.run_im")
│def test_bake_emissive_map(mock_run_im):
⋮
│@patch("mox.modules.image.modules.texture.service.run_im")
│def test_bake_normal_map_from_image_default(mock_run_im):
⋮
│@patch("mox.modules.image.modules.texture.service.run_im")
│def test_bake_normal_map_from_image_explicit_delta(mock_run_im):
⋮
│@patch("mox.modules.image.modules.texture.service.run_im")
│def test_bake_normal_map_from_image_zero_alpha(mock_run_im):
⋮
│@patch("mox.modules.image.modules.texture.service.run_im")
│def test_bake_normal_map_from_obj_success(mock_run_im):
│    mock_run_im.side_effect = ["100x100+0+0", "100x100", None]
│    
⋮
│    class MockMatrix:
│        def __matmul__(self, other):
⋮
│    class MockCam:
│        def __init__(self):
│            class Loc:
│                x = 0
│                y = 0
│                z = 0
⋮
│        @property
│        def location(self):
⋮
│        @location.setter
│        def location(self, val):
⋮
│    class MockVector:
│        def __init__(self, v):
│            self.x = v[0]
│            self.y = v[1]
⋮
│@patch("mox.modules.image.modules.texture.service.run_im")
│@patch("mox.modules.image.modules.texture.service.shutil.copy")
│def test_bake_normal_map_from_obj_no_match(mock_copy, mock_run_im):
│    mock_run_im.return_value = "invalid"
│    
⋮
│    class MockMatrix:
│        def __matmul__(self, other):
⋮
│    class MockCam:
│        def __init__(self):
│            class Loc:
│                x = 0
│                y = 0
│                z = 0
⋮
│        @property
│        def location(self):
⋮
│        @location.setter
│        def location(self, val):
⋮
│    class MockVector:
│        def __init__(self, v):
│            self.x = v[0]
│            self.y = v[1]
⋮
│def test_bake_normal_map_from_obj_no_mesh():
⋮
│@patch("mox.modules.image.modules.texture.service.bake_occlusion_map")
⋮
│def test_bake_maps_all_no_obj(mock_norm_obj, mock_norm_img, mock_emi, mock_occ):
⋮
│@patch("mox.modules.image.modules.texture.service.bake_occlusion_map")
⋮
│def test_bake_maps_all_with_obj(mock_norm_obj, mock_norm_img, mock_emi, mock_occ):
⋮
│@patch("mox.modules.image.modules.texture.service.bake_occlusion_map")
│def test_bake_maps_occlusion(mock_occ):
⋮
│@patch("mox.modules.image.modules.texture.service.bake_emissive_map")
│def test_bake_maps_emissive(mock_emi):
⋮
│@patch("mox.modules.image.modules.texture.service.bake_normal_map_from_image")
│def test_bake_maps_normal(mock_norm):
⋮

packages\mox\tests\unit\test_client.py:
⋮
│@patch("mox.modules.image.modules.composite.service.render")
│def test_render(mock_render):
⋮
│@patch("mox.modules.image.modules.composite.service.render_batch")
│def test_render_batch(mock_render_batch):
⋮
│@patch("shutil.copy2")
⋮
│def test_bake_occlusion_map(mock_create, mock_create_empty, mock_from_path, mock_copy):
⋮
│@patch("shutil.copy2")
⋮
│def test_bake_emissive_map(mock_create, mock_create_empty, mock_from_path, mock_copy):
⋮
│@patch("shutil.copy2")
⋮
│def test_bake_normal_map_from_image(mock_render, mock_create_empty, mock_from_path, mock_copy):
⋮
│@patch("shutil.copy2")
⋮
│def test_bake_normal_map_from_obj(mock_render, mock_create_empty, mock_from_path, mock_copy):
⋮
│@patch("mox.client.File.from_path")
│@patch("mox.integrations.photoshop.service.extract_psd_to_tempdir")
│def test_extract_psd(mock_extract, mock_from_path):
⋮

packages\mox\tests\unit\utils\test_s3.py:
⋮
│def test_workspace_context():
⋮
│def test_file_creation_outside_workspace():
⋮

pdm.lock

pdm.toml

pyproject.toml
```