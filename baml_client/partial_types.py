###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional, Union, Literal

from . import types
from .types import Checked, Check

###############################################################################
#
#  These types are used for streaming, for when an instance of a type
#  is still being built up and any of its fields is not yet fully available.
#
###############################################################################


class Receipt(BaseModel):
    line_items: List["ReceiptItem"]
    total_amount: Optional[float] = None
    date: Optional[str] = None
    time: Optional[str] = None
    business: Optional[str] = None
    currency_code: Optional[str] = None
    address: Optional[str] = None
    payment_method: Optional[str] = None

class ReceiptItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[int] = None
    quantity_unit: Optional[str] = None
    price: Optional[float] = None
