import PyKDL as kdl
import numpy as np

class MausKinematics(object):

    def __init__(self):
        self.left_leg = kdl.Chain()
        self.left_leg.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotY), kdl.Frame(kdl.Vector(0,0,-50))))
        self.left_leg.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotY), kdl.Frame(kdl.Vector(0,0,-50))))

        self.ik_solver = kdl.ChainIkSolverPos_LMA(self.left_leg)

	self.left_alpha1=45
	self.left_alpha2=-45
	self.left_beta=self.left_alpha2-self.left_alpha1

    def getJoints(self, x, y, z):
        target_frame = kdl.Frame(kdl.Vector(x,y,z))
	current_angles = kdl.JntArray(self.left_leg.getNrOfJoints())
	result_angles = kdl.JntArray(self.left_leg.getNrOfJoints())
        current_angles[0] = np.deg2rad(self.left_alpha1)
        current_angles[1] = np.deg2rad(self.left_beta)

        self.ik_solver.CartToJnt(current_angles, target_frame, result_angles)
	result_angles[1] = result_angles[0] + result_angles[1]
	result_angles[0] = np.rad2deg(result_angles[0])
	result_angles[1] = np.rad2deg(result_angles[1])
	return result_angles
