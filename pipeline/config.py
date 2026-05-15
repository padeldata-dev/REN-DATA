"""Configuración global del pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = ROOT / "pipeline"
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
PROCESSED_DIR = DATA_DIR / "processed"
RENDATA_DIR = ROOT / "rendata_beta"

CITIES_MASTER = PIPELINE_DIR / "data" / "cities_master.csv"

# Asegurar que existan
for d in (RAW_DIR, SNAPSHOTS_DIR, PROCESSED_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Doctrina ROI (acordada en sesión previa)
SUP_M2 = 100  # superficie de cálculo del ROI

# User agent para fetches HTTP (identificarnos honestamente)
USER_AGENT = "RenDataPipeline/0.1 (+https://rendata.es; contacto@rendata.es) educational/research"

# Mapping CCAA name → slug (consistente con el sitio)
CCAA_SLUG = {
    "Andalucía": "andalucia", "Aragón": "aragon", "Asturias": "asturias",
    "Islas Baleares": "baleares", "Canarias": "canarias", "Cantabria": "cantabria",
    "Castilla-La Mancha": "castilla-la-mancha", "Castilla y León": "castilla-y-leon",
    "Cataluña": "cataluna", "C. Valenciana": "comunitat-valenciana",
    "Extremadura": "extremadura", "Galicia": "galicia", "La Rioja": "la-rioja",
    "C. de Madrid": "madrid", "R. de Murcia": "murcia",
    "Navarra": "navarra", "País Vasco": "pais-vasco",
}
