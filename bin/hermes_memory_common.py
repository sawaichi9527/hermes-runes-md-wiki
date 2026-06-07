#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

BIN_DIR = Path(__file__).resolve().parent
REPO_ROOT = BIN_DIR.parent

IMPORTER_DIR = REPO_ROOT / "tools" / "importer"

if str(IMPORTER_DIR) not in sys.path:
    sys.path.insert(0, str(IMPORTER_DIR))

from root_resolver import resolve_root
import hashlib
import subprocess

VERSION = "0.3.0-m3.1"

EXIT_OK = 0
EXIT_GENERAL_FAIL = 1
EXIT_ARG_ERROR = 2
EXIT_CONFIG_ERROR = 3
EXIT_DB_ERROR = 4
EXIT_SOURCE_ERROR = 5
EXIT_EMBED_ERROR = 6
EXIT_EVAL_FAIL = 7
EXIT_BACKUP_RESTORE_ERROR = 8
EXIT_SAFETY_BLOCKED = 9

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def result(tool, project, status="PASS", exit_code=0, summary=None, items=None, warnings=None, errors=None):
    return {
        "tool": tool,
        "version": VERSION,
        "project": project,
        "status": status,
        "exit_code": exit_code,
        "summary": summary or {},
        "items": items or [],
        "warnings": warnings or [],
        "errors": errors or [],
        "created_at": now_iso(),
    }

def emit(obj, as_json=False, quiet=False):
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
        return
    if quiet:
        print(obj.get("status", "UNKNOWN"))
        return
    print(f"tool: {obj.get('tool')}")
    print(f"version: {obj.get('version')}")
    print(f"project: {obj.get('project')}")
    print(f"status: {obj.get('status')}")
    for k, v in obj.get("summary", {}).items():
        print(f"{k}: {v}")
    for w in obj.get("warnings", []):
        print(f"[WARN] {w.get('code', 'WARNING')}: {w.get('message', '')}")
    for e in obj.get("errors", []):
        print(f"[FAIL] {e.get('code', 'ERROR')}: {e.get('message', '')}")

def repo_root_from_cwd():
    if os.environ.get("HERMES_MEMORY_ROOT"):
        return resolve_root()

    p = Path.cwd()
    if (p / "wiki").exists() or (p / "imports").exists() or (p / "config").exists():
        return p

    return resolve_root()

def read_config_path(args):
    if getattr(args, "config", None):
        return Path(args.config).expanduser()
    root = repo_root_from_cwd()
    return root / "config" / "hermes-memory.yaml"

def parse_simple_config(path):
    # Minimal YAML reader for this known config shape.
    # Avoids requiring PyYAML during M3.1 bootstrap.
    cfg = {
        "default_project": "freelancer",
        "projects": {
            "freelancer": {
                "root": str(resolve_root()),
                "source_paths": ["wiki/freelancer", "imports"],
                "eval_path": "eval/freelancer",
                "backup_path": "backups",
                "database_url_env": "HERMES_MEMORY_DATABASE_URL",
            }
        }
    }
    if not path.exists():
        return cfg
    text = path.read_text(encoding="utf-8")
    # Keep bootstrap intentionally conservative.
    if "root:" in text:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("root:"):
                cfg["projects"]["freelancer"]["root"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("url_env:"):
                cfg["projects"]["freelancer"]["database_url_env"] = stripped.split(":", 1)[1].strip()
    return cfg

def get_project_cfg(args):
    cfg_path = read_config_path(args)
    cfg = parse_simple_config(cfg_path)
    project = getattr(args, "project", None) or cfg.get("default_project", "freelancer")
    pcfg = cfg["projects"].get(project)
    if not pcfg:
        raise RuntimeError(f"Unknown project: {project}")
    pcfg = dict(pcfg)
    pcfg["project"] = project
    pcfg["config_path"] = str(cfg_path)
    pcfg["root_path"] = Path(pcfg["root"]).expanduser()
    return pcfg

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b=""):
            h.update(chunk)
    return h.hexdigest()

def markdown_files(paths):
    out = []
    for base in paths:
        b = Path(base)
        if not b.exists():
            continue
        if b.is_file() and b.suffix.lower() == ".md":
            out.append(b)
        elif b.is_dir():
            out.extend(sorted(p for p in b.rglob("*.md") if p.is_file()))
    return sorted(set(out))

def run_cmd(cmd, timeout=10):
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

def psql_available():
    try:
        r = run_cmd(["psql", "--version"])
        return r.returncode == 0, (r.stdout or r.stderr).strip()
    except Exception as e:
        return False, str(e)

def database_url():
    return os.environ.get("HERMES_MEMORY_DATABASE_URL") or os.environ.get("DATABASE_URL") or ""

def psql_scalar(sql, timeout=10):
    url = database_url()
    if not url:
        return None, "HERMES_MEMORY_DATABASE_URL is not set"
    try:
        r = run_cmd(["psql", url, "-Atqc", sql], timeout=timeout)
        if r.returncode != 0:
            return None, r.stderr.strip()
        return r.stdout.strip(), ""
    except Exception as e:
        return None, str(e)

def base_parser(description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--project", default=None)
    p.add_argument("--config")
    p.add_argument("--json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    return p
