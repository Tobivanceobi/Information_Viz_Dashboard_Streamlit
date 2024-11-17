from .dashboard import Dashboard
from ..utils import Page
from typing import Dict, Type


PAGE_MAP: Dict[str, Type[Page]] = {
    Dashboard.NAME: Dashboard,
}

__all__ = ["PAGE_MAP"]