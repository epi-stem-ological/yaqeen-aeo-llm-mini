from typing import Optional
from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None
