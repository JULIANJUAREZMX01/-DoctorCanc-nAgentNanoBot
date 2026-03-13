"""Price Engine — Device model extraction and price lookup from business_rules.yaml."""

import re
from pathlib import Path

import yaml

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

RULES_PATH = Path("data/business_rules.yaml")

# Common device model patterns (normalized)
MODEL_PATTERNS = {
    # iPhone
    r"iphone\s*se": "iphone_se",
    r"iphone\s*6": "iphone_6",
    r"iphone\s*7": "iphone_7",
    r"iphone\s*8": "iphone_8",
    r"iphone\s*x\b": "iphone_x",
    r"iphone\s*xs": "iphone_xs",
    r"iphone\s*xr": "iphone_xr",
    r"iphone\s*11(?:\s*pro)?(?:\s*max)?": "iphone_11",
    r"iphone\s*12(?:\s*pro)?(?:\s*max)?": "iphone_12",
    r"iphone\s*13(?:\s*pro)?(?:\s*max)?": "iphone_13",
    r"iphone\s*14(?:\s*pro)?(?:\s*max)?": "iphone_14",
    r"iphone\s*15(?:\s*pro)?(?:\s*max)?": "iphone_15",
    r"iphone\s*16(?:\s*pro)?(?:\s*max)?": "iphone_16",
    # Samsung
    r"samsung\s*a\s*14": "samsung_a14",
    r"samsung\s*a\s*15": "samsung_a15",
    r"samsung\s*a\s*34": "samsung_a34",
    r"samsung\s*a\s*35": "samsung_a35",
    r"samsung\s*a\s*54": "samsung_a54",
    r"samsung\s*a\s*55": "samsung_a55",
    r"samsung\s*s\s*23": "samsung_s23",
    r"samsung\s*s\s*24": "samsung_s24",
    r"galaxy\s*a\s*14": "samsung_a14",
    r"galaxy\s*a\s*54": "samsung_a54",
    r"galaxy\s*s\s*23": "samsung_s23",
    r"galaxy\s*s\s*24": "samsung_s24",
    # Huawei
    r"huawei\s*p\s*30": "huawei_p30",
    r"huawei\s*p\s*40": "huawei_p40",
    r"huawei\s*y\s*9": "huawei_y9",
    r"huawei\s*nova": "huawei_nova",
    # Xiaomi
    r"xiaomi|redmi|poco": "xiaomi_generic",
    # Motorola
    r"moto\s*g|motorola": "motorola_generic",
    # iPad
    r"ipad\s*(?:air|pro|mini)?": "ipad_generic",
    # Laptop
    r"laptop|computadora|compu|macbook|notebook": "laptop_generic",
}


class PriceEngine:
    """Look up repair prices by device model."""

    def __init__(self, rules_path: Path = RULES_PATH):
        self.services: dict = {}
        self._load_rules(rules_path)

    def _load_rules(self, path: Path) -> None:
        """Load business rules from YAML."""
        if not path.exists():
            logger.warning(f"Business rules not found: {path}")
            return

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.services = data.get("services", {})
        logger.info(f"Loaded {len(self.services)} service categories")

    def extract_model(self, text: str) -> str | None:
        """Extract device model from free-form text."""
        text_lower = text.lower()
        for pattern, model_key in MODEL_PATTERNS.items():
            if re.search(pattern, text_lower):
                return model_key
        return None

    def detect_service_type(self, text: str) -> str:
        """Detect what service the user is asking about."""
        text_lower = text.lower()
        if any(w in text_lower for w in ["pantalla", "display", "pantaya", "screen"]):
            return "screen_repair"
        if any(w in text_lower for w in ["bateria", "batería", "pila", "battery"]):
            return "battery_replacement"
        if any(w in text_lower for w in ["carga", "puerto", "charging"]):
            return "charging_port"
        if any(w in text_lower for w in ["agua", "mojó", "water"]):
            return "water_damage"
        if any(w in text_lower for w in ["desbloqueo", "desbloquear", "liberar", "icloud", "frp"]):
            return "unlock"
        return "screen_repair"  # Default — most common

    def lookup(self, model_key: str, service_type: str | None = None) -> dict:
        """Look up price for a device model and service type.

        Returns:
            dict with keys: found, model, service, price_min, price_max,
                           time_estimate, warranty
        """
        if not service_type:
            service_type = "screen_repair"

        service_data = self.services.get(service_type, {})
        prices = service_data.get("prices", {})
        model_price = prices.get(model_key)

        if model_price:
            if isinstance(model_price, dict):
                return {
                    "found": True,
                    "model": model_key.replace("_", " ").title(),
                    "service": service_data.get("name", service_type),
                    "price_min": model_price.get("min"),
                    "price_max": model_price.get("max"),
                    "time_estimate": model_price.get("time", service_data.get("time_estimate", "")),
                    "warranty": model_price.get("warranty", service_data.get("warranty", "")),
                }
            elif isinstance(model_price, (int, float)):
                return {
                    "found": True,
                    "model": model_key.replace("_", " ").title(),
                    "service": service_data.get("name", service_type),
                    "price_min": model_price,
                    "price_max": model_price,
                    "time_estimate": service_data.get("time_estimate", ""),
                    "warranty": service_data.get("warranty", ""),
                }

        return {
            "found": False,
            "model": model_key.replace("_", " ").title(),
            "service": service_data.get("name", service_type),
        }
