import dataclasses
import numpy as np
import logging

# Use dataclasses always, otherwise any small change or addition/deletion of attributes
# you would beed to rewite the entire thing.

@dataclasses.dataclass
class Resource:
	pass


