from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
    index: int
    title_es: str
    content_es: str
    title_en: Optional[str] = None
    image_url: Optional[str] = None
    local_image_path: Optional[str] = None
