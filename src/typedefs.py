from typing import *

from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
Headers = Union[CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy, Dict[str, str]]
Json = Union[Dict[str, Any], List[Any], str, int, float, bool, None]
