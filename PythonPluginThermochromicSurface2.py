from pyenergyplus.plugin import EnergyPlusPlugin


class Living_Zone_Surface_Control(EnergyPlusPlugin):

    def __init__(self):
        # init parent class
        super().__init__()
        self.need_to_get_handles = True
        self.Surf8_Tout_handle = None
        self.Surf8_Construct_handle = None
        self.WallExtInsFin1_handle = None
        self.WallExtInsFin2_handle = None
 
    def on_begin_timestep_before_predictor(self, state) -> int:
#BeginTimestepBeforePredictor: on_begin_timestep_before_predictor
#BeginZoneTimestepAfterInitHeatBalance: on_begin_zone_timestep_after_init_heat_balance
        # api is ready to execute
        if self.api.exchange.api_data_fully_ready(state):

            # get variable handles if needed
            if self.need_to_get_handles:
                self.Surf8_Tout_handle = self.api.exchange.get_variable_handle(
                    state,
                    "Surface Outside Face Temperature",
                    "Surface 8")

                self.Surf8_Construct_handle = self.api.exchange.get_actuator_handle(state,
                                                                                   "Surface",
                                                                                   "Construction State",
                                                                                   "Surface 8")
          
                self.WallExtInsFin1_handle = self.api.exchange.get_construction_handle(state, "WallExtInsFin1")
                
                self.WallExtInsFin2_handle = self.api.exchange.get_construction_handle(state, "WallExtInsFin2")

                self.need_to_get_handles = False

            # calculate
            if self.api.exchange.get_variable_value(state, self.Surf8_Tout_handle) <= 25.0:
                self.api.exchange.set_actuator_value(state, self.Surf8_Construct_handle, self.WallExtInsFin1_handle)

            else:
                self.api.exchange.set_actuator_value(state, self.Surf8_Construct_handle, self.WallExtInsFin2_handle)

            return 0

        else:
            # api not ready, return
            return 0
