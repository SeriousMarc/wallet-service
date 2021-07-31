"""
Validation Schemas
"""
from decimal import Decimal
# from typing import List, Dict
# from datetime import date

from pydantic import BaseModel


class Test(BaseModel):
    id: int
    amount: Decimal
