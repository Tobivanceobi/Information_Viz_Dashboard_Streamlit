from .dashboard_1 import Dashboard1
from .dashboard_2 import Dashboard2
from .dashboard_3 import Dashboard3
from ..utils import Page
from typing import Dict, Type


PAGE_MAP: Dict[str, Type[Page]] = {
    Dashboard1.NAME: Dashboard1,
    Dashboard2.NAME: Dashboard2,
    Dashboard3.NAME: Dashboard3,
}

__all__ = ["PAGE_MAP"]