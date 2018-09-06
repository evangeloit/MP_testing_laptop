import PythonModel3dTracker.PythonModelTracker.TrackingResults.ModelTrackingResults as Mtr
import numpy as np
import json
from scipy.ndimage import gaussian_filter

input_dir = "/home/evangeloit/Desktop/GitBlit_Master/PythonModel3dTracker/Data/rs/Human_tracking/alex_far_01_ldm.json"
model_name = "mh_body_male_custom"

##### Implementation with ModelTrackingResults scripts #####

# results = Mtr.ModelTrackingResults()
# results.load(input_dir)
# ldm3d = results.landmarks

# frames = -1
# for i in ldm3d:
#     print(ldm3d[i])
#     frames = frames + 1

# print(frames)

##### My implementation / Import json #####
with open(input_dir) as f:
    data = json.load(f)

##### Check First frame for insuficient landmarks #####
LandSize = len(data['landmarks']['0'][model_name])
LandDesired = len(data['landmark_names'][model_name])

if LandSize == LandDesired:
    print("You have Imported:", LandSize, "Landmarks")
else:
    print('Insufficient Landmarks at import')
    exit()

##### Create 3D points List #####
points = []
for i in range(0, len(data['landmarks'])):
    strnum = str(i)
    # print(strnum)
    for item in data['landmarks'][strnum][model_name]:
            points.append(item)
            # print(point3d)

#### Convert to numpy array for calculations ####
point3d = np.array(points)
point3d = np.transpose(point3d)

### Normalization of 3d points with Gaussian filter [5 1]####
# GFpoint3d = gaussian_filter(point3d, sigma=1)
# print(GFpoint3d[2,28])


#### Derivatives Calculation ####
sz = point3d.shape
t1 = LandSize
t2 = 2*LandSize
StartFrame = 2*LandSize # Start from 3rd Frame's 3D points
Pt0 = []
Pt1 = []
Pt2 = []
PtMinus1 = []
PtMinus2 = []
for col in range(StartFrame, sz[1] - StartFrame):
    for row in range(0, sz[0]):
        Pt0.extend([point3d[row, col]]) # Current Frame
        Pt1.extend([point3d[row, col + t1]])
        Pt2.extend([point3d[row, col + t2]])
        PtMinus1.extend([point3d[row, col - t2]])
        PtMinus2.extend([point3d[row, col - t2]])


#Derivatives
vel = np.asarray(Pt1) - np.asarray(PtMinus1)
acc = np.asarray(Pt2) + np.asarray(PtMinus2) - (2*(np.asarray(Pt0)))

f_vector = np.column_stack((Pt0, vel, acc))
# f_vector = np.transpose(f_vector)
print(f_vector[:, 2])
print(acc)

# print(len(PtMinus1),len(PtMinus2),len(Pt0),len(Pt1),len(Pt2))
# vel = np.array(vel)
# print(vel.shape)

# Save Feature data into json...