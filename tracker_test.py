import triad_openvr
import time
import sys

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

interval = 1/100

origin = list()
a = float()
b = float()
c = float()
d = float()

input("Put the tracker on (0,0) and press ENTER: \n")
origin = v.devices["tracker_1"].get_pose_euler()
input("Put the tracker on (6,0) and press ENTER: \n")
point = v.devices["tracker_1"].get_pose_euler()
x_point = (point[0]-origin[0], point[2]-origin[2])
input("Put the tracker on (0,6) and press ENTER: \n")
point = v.devices["tracker_1"].get_pose_euler()
y_point = (point[0]-origin[0], point[2]-origin[2])

b = 6/(x_point[1] - ((x_point[0]*y_point[1])/y_point[0]))
a = -b*(y_point[1]/y_point[0])
d = 6/(y_point[1] - ((y_point[0]*x_point[1])/x_point[0]))
c = -d*(x_point[1]/x_point[0])

input("Press ENTER when you want to start recording the data")
start_time = time.time()
start_time2 = start_time
file = open("data.csv", "w")

file.write("x(ft), y(ft), theta(degrees), time(s)" + "\n")
print("Recording Data")

while(True):
    if time.time() - start_time2 < interval:
        continue
    else:
        start_time2 += interval

    txt = ""
    point = v.devices["tracker_1"].get_pose_euler()
    sensor_reading = {"x": point[0], "y": point[2], "theta": point[4]}
    x = (sensor_reading["x"]-origin[0])*a + (sensor_reading["y"]-origin[2])*b
    y = (sensor_reading["x"]-origin[0])*c + (sensor_reading["y"]-origin[2])*d
    theta = sensor_reading["theta"] - origin[4]
    theta = (theta + 360)%360
    current_time = time.time()-start_time
    file.write(str(x)+", " + str(y) + ", " + str(theta) + ", " + str(current_time) + "\n")
