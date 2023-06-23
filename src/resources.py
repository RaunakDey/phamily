import dataclasses
import numpy as np
import logging

# Use dataclasses always, otherwise any small change or addition/deletion of attributes
# you would beed to rewite the entire thing.

@dataclasses.dataclass
class Resource:
	linear_model_mult_constant: float = 1.0
	monod_mult_constant: float = 1.0
	half_conc: float = 2
	units: str = '/ml'

	def type_I(self,
		linear_model_mult_constant = None,
		resource = 1 
		):
		linear_model_mult_constant = self.linear_model_mult_constant if linear_model_mult_constant is None else linear_model_mult_constant
		type_I_resource = linear_model_mult_constant * resource
		logging.debug("The multiplicative constant is {}".format(linear_model_mult_constant))
		return type_I_resource


	def monod(self,
		monod_mult_constant = None,
		half_conc = None,
		resource =1
		):
		increasing_model_mult_constant = self.monod_mult_constant if monod_mult_constant is None else monod_mult_constant
		half_conc = self.half_conc if half_conc is None else half_conc
		monod_res = monod_mult_constant * resource/(half_conc + resource)
		logging.debug("The half concentration is {} {} and the multiplicative monod_mult_constant is {} ".format( half_conc, self.units), monod_mult_constant)
		return monod_res


	def units(self,
		):
		logging.debug("The units of resources is".format(self.units))
		pass


