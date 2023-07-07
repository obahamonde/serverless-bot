from datetime import datetime
from typing import *
from uuid import uuid4

from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy

from src.lib import *

T = TypeVar("T")
Headers = Union[
    CIMultiDictProxy, CIMultiDict, MultiDictProxy, MultiDict, Dict[str, str]
]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]
Json = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

Vector = List[float]
Scalar = Union[float, int, str, bool]
Context = Dict[str, str]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
