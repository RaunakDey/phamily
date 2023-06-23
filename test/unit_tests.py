import sys
import logging

sys.path.append('./../src/')

from resources import Resource

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

# Create an instance of the Resource class
resource = Resource()

# Call the type_I method
result_type_I = resource.type_I(linear_model_mult_constant=2.5, resource=3)
print("Result of type_I method:", result_type_I)

# Call the monod method
result_monod = resource.monod(monod_mult_constant=0.8, half_conc=1.5, resource=4)
print("Result of monod method:", result_monod)

# Call the print_units method
resource.print_units()
