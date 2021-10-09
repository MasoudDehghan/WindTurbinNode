class WindTurbineData:
    def __init__(self,ID):
        self.ID = ID

    def __init__(self,ID,Time_Stamp,Wind_Turbine_ID,Wind_Speed,RPM,Temperature,Rain,Visibility,Status,Expected_Status,Sub_Status):
        self.ID = ID
        self.Time_Stamp = Time_Stamp
        self.Wind_Turbine_ID = Wind_Turbine_ID
        self.Wind_Speed = Wind_Speed
        self.RPM = RPM
        self.Temperature = Temperature
        self.Rain = Rain
        self.Visibility = Visibility
        self.Status = Status
        self.Expected_Status = Expected_Status
        self.Sub_Status = Sub_Status

    # def __init__(self,Time_Stamp,Wind_Turbine_ID,Wind_Speed,RPM,Temperature,Rain,Visibility,Status,Expected_Status,Sub_Status):
    #     self.Time_Stamp = Time_Stamp
    #     self.Wind_Turbine_ID = Wind_Turbine_ID
    #     self.Wind_Speed = Wind_Speed
    #     self.RPM = RPM
    #     self.Temperature = Temperature
    #     self.Rain = Rain
    #     self.Visibility = Visibility
    #     self.Status = Status
    #     self.Expected_Status = Expected_Status
    #     self.Sub_Status = Sub_Status

