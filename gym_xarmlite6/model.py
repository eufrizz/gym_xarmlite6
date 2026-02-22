from pathlib import Path
from typing import Any, Dict

MODEL_DIR = Path(__file__).parent.resolve() / "models"
ASSETS_DIR = Path(__file__).parent.resolve() / "assets"


def update_assets(
  assets: Dict[str, Any],
  path: str | Path,
  meshdir: str | None = None,
  glob: str = "*",
  recursive: bool = False,
):
  """Update assets dictionary with files from a directory.

  This function reads files from a directory and adds them to an assets dictionary,
  with keys formatted to include the meshdir prefix when specified.

  Args:
    assets: Dictionary to update with file contents. Keys are asset paths, values are
      file contents as bytes.
    path: Path to directory containing asset files.
    meshdir: Optional mesh directory prefix, typically `spec.meshdir`. If provided,
      will be prepended to asset keys (e.g., "mesh.obj" becomes "custom_dir/mesh.obj").
    glob: Glob pattern for file matching. Defaults to "*" (all files).
    recursive: If True, recursively search subdirectories.
  """
  for f in Path(path).glob(glob):
    if f.is_file():
      asset_key = f"{meshdir}/{f.name}" if meshdir else f.name
      assets[asset_key] = f.read_bytes()
    elif f.is_dir() and recursive:
      update_assets(assets, f, meshdir, glob, recursive)

def get_assets(meshdir: str) -> dict[str, bytes]:
  assets: dict[str, bytes] = {}
  for subdir in ("visual", "collision"):
    update_assets(assets, ASSETS_DIR / subdir, f"{meshdir}/{subdir}", glob="*.stl")
  return assets

def get_spec(name: str = "lite6_gripper.xml") -> "mujoco.MjSpec":
  import mujoco
  spec = mujoco.MjSpec.from_file(str(MODEL_DIR / name))
  spec.assets = get_assets(spec.meshdir)
  return spec
  

def get_model(name: str):
  model = get_spec(name).compile()
  # Disable group 2 (velocity) actuator forces — actuatorgroupdisable in the XML
  # only controls viewer visibility, not force computation. disableactuator has no
  # XML equivalent, so it must be set here after compilation.
  model.opt.disableactuator = 1 << 2
  return model

