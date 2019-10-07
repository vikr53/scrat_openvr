import triad_openvr
import time
import sys
import signal, os

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise OSError("Couldn't open device!")

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

interval = 1/1000

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

while(True):
    start = time.time()
    txt = ""
    point = v.devices["tracker_1"].get_pose_euler()
    sensor_reading = {"x": point[0], "y": point[2], "theta": point[4]}
    x = (sensor_reading["x"]-origin[0])*a + (sensor_reading["y"]-origin[2])*b
    y = (sensor_reading["x"]-origin[0])*c + (sensor_reading["y"]-origin[2])*d
    theta = sensor_reading["theta"] - origin[4]
    for each in [x,y,theta]:
        txt += "%.4f" % each
        txt += " "
    print("\r" + txt, end="")
    sleep_time = interval-(time.time()-start)
    if sleep_time>0:
        time.sleep(sleep_time)