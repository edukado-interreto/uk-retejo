from collections import OrderedDict
from typing import Any, Dict

class BaseBlock:
    base_blocks: OrderedDict[str, BaseBlock]

Block = BaseBlock
