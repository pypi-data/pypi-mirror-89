import math
from .general_wh_processes import Functional_module


class Gtp_module(Functional_module):
    '''
    The GTP_module class represents a pick environment of an
    automated pick process according the goods to picker principle.

        Inputs:
        - required order lines per hour
        - required required units_per_hour

        Outputs:
        - Sizing in required GTP units
        - Investment price in Euros
        - FTE requirement in FTEs per shift
    '''

    def __init__(self, req_units_per_hour, req_lines_per_hour):

        Functional_module.__init__(
            self, req_units_per_hour, req_lines_per_hour)

        # Following are module-specific constants
        self.cost_per_unit = 100000  # per station
        self.capacity_per_unit = 500  # order lines per picker (station)

    def sizer(self):
        '''
        The sizer is calculating the required amount of units to fulfill the needed capacity.

        Inputs: None

        Outputs: Amount of needed GTP units
        '''
        
        self.number_of_units = math.ceil(
            self.req_lines_per_hour / self.capacity_per_unit)
        return self.number_of_units

    def update_module_capacity(self):
        '''Updates the module specific capacity'''

        self.capacity_per_unit = int(
            input('Current capacity is 600. Enter new amount: '))

    def __repr__(self):
        self.sizer()
        self.calculate_cost()
        return "Functional module: Goods to picker\n \
            Requirement: {} order line per hour\n \
            Needed units: {}\n \
            Total cost: {}".format(
                self.req_lines_per_hour,
                self.number_of_units,
                self.total_cost
                )

class Batch_pick_to_cart(Functional_module):
    '''
    The Batch_pick_to_cart class represents a pick environment of
    a manual pick process according the picker to goods principle.

        Inputs:
        - required order lines per hour
        - required required units_per_hour

        Outputs:
        - Sizing in required GTP units
        - Investment price in Euros
        - FTE requirement in FTEs per shift
    '''

    def __init__(self, req_units_per_hour, req_lines_per_hour):

        Functional_module.__init__(self, req_units_per_hour, req_lines_per_hour)

        # Following are module-scecific constants.
        self.cost_per_unit = 5000
        self.capacity_per_unit = 60
        self.sort_rate_per_hour = 240

    def sizer(self):
        '''
        The sizer is calculating the required amount of carts to fulfill the needed capacity.

        Inputs: None

        Outputs: Amount of needed carts
        '''
        
        self.number_of_units = math.ceil(
            self.req_lines_per_hour / self.capacity_per_unit)

        self.number_of_putwalls = math.ceil(
            self.req_units_per_hour / self.sort_rate_per_hour) # In our simple example we ignore the cost for this equipment

        return self.number_of_units

    def update_module_capacity(self):
        '''Updates the module specific capacity'''

        self.capacity_per_unit = int(
            input('Current capacity is 60. Enter new amount: '))

        self.sort_rate_per_hour = int(
            input('Current capacity is 240. Enter new amount: '))
        
    def __repr__(self):
        self.sizer()
        self.calculate_cost()
        return "Functional module: Batch-pick to cart\n \
            Requirement: {} order lines per hour\n \
            Needed units: {}\n \
            Total cost: {}".format(
                self.req_lines_per_hour,
                self.number_of_units,
                self.total_cost
                )

