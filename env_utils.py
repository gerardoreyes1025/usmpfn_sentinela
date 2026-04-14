"""Utilidad ligera para cargar variables desde un archivo .env.

Intenta usar python-dotenv si está instalado. Si no, hace un parse sencillo
del archivo `.env` ubicado en la carpeta del proyecto y exporta las
variables a os.environ (sin sobreescribir variables ya existentes).
"""
from __future__ import annotations
import os
from pathlib import Path


def load_dotenv(path: str | Path | None = None) -> None:
    """Carga variables desde `path` (por defecto ./ .env del repo) en os.environ.

    No sobreescribe variables ya presentes en el entorno.
    """
    project_root = Path(__file__).parent
    env_path = Path(path) if path else project_root / ".env"

    # Preferir python-dotenv si está disponible
    try:
        from dotenv import load_dotenv as _load_dotenv

        _load_dotenv(dotenv_path=str(env_path))
        return
    except Exception:
        # continuar con el cargador simple
        pass

    if not env_path.exists():
        return

    try:
        with env_path.open("r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                # No sobreescribir variables ya presentes
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception:
        # No elevar errores aquí — cargar .env es una conveniencia.
        return
