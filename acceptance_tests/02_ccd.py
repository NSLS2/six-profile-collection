# In case rixscam is at room temperature, run:
# RE(rixscam.set_LS_RT()) 
# To set voltages back for low temperature (normal operating condition), run:
# RE(rixscam.set_LS())
from bluesky.plans import count


RE(count([rixscam]))
