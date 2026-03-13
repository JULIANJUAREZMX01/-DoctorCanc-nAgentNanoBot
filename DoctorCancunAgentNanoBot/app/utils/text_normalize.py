"""WhatsApp text normalization."""
import re
ABBR = {" x ":" por "," d ":" de "," q ":" que "," cel ":" celular "," lap ":" laptop "}
TYPOS = {"pantaya":"pantalla","samsun ":"samsung ","sansung":"samsung","huawey":"huawei","aifon":"iphone","xiomi":"xiaomi"}

def normalize_whatsapp_text(text):
    r = re.sub(r"[^\w\sáéíóúñü¿?¡!.,/$]", "", text.strip(), flags=re.UNICODE)
    lo = f" {r.lower()} "
    for a, b in ABBR.items(): lo = lo.replace(a, b)
    for a, b in TYPOS.items(): lo = lo.replace(a, b)
    return lo.strip()
