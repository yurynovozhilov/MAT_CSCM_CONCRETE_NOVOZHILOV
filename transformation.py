from pyquaternion import Quaternion
import numpy as np

np.set_printoptions(suppress=True)

def rotateCurve(curve,axis,angle):
    newCurve = np.zeros_like(curve)
    for i, point in enumerate(curve.T):
        newCurve.T[i] = Quaternion(axis=axis,angle=np.deg2rad(theta)).rotate(point)
    return newCurve