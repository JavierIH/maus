import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import maus.maus

maus = Maus(servo_trims=[-15, 8, 0, -18, 21])
maus.run()
