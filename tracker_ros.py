import triad_openvr
import time
import math
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

print("Recording Data")
count = 0

file_all_data = open("alldata.csv", "w")

while(True):
    txt = ""
    point = v.devices["tracker_1"].get_pose_euler()
    # try to get vel
    vel = v.devices["tracker_1"].get_velocity()
    print(vel)
    sensor_reading = {"x": point[0], "y": point[2], "theta": point[4]}
    x = (sensor_reading["x"]-origin[0])*a + (sensor_reading["y"]-origin[2])*b
    y = (sensor_reading["x"]-origin[0])*c + (sensor_reading["y"]-origin[2])*d
    theta = sensor_reading["theta"] - origin[4]
    # theta between (-180, 180)
    theta = (theta + 180)%360 -180

    #Convert to meters
    x = x * 0.3048
    y = y * 0.3048
    theta_rad = -(theta*math.pi)/180.0;
    #vel_x = - vel[0] * math.sin(theta_rad) * 0.3048
    #vel_y = vel[0] * math.cos(theta_rad) * 0.3048
    angle = -math.pi/4
    vel_x = vel[0] * math.cos(angle) - vel[2] * math.sin(angle)
    vel_y = vel[0] * math.sin(angle) + vel[2] * math.cos(angle)
    #vel_x = vel[0] * 0.3048
    #vel_y = vel[2] * 0.3048
    #vel_z = vel[2]
    #Shift to center
    #x_r = x + math.sin(theta_rad)*(16.5*0.015)
    #y_r = y - math.cos(theta_rad)*(16.5*0.015)

    file = open("data.txt", "w")
    file.write("{:.4f}".format(x)+", " + "{:.4f}".format(y) + ", " + "{:.4f}".format(theta_rad) + ", " + "{:.4f}".format(vel_x) \
         + ", " + "{:.4f}".format(vel_y));
    if count % 10000 == 0:
        file_all_data.write("{:.4f}".format(x)+", " + "{:.4f}".format(y) + ", " + "{:.4f}".format(theta_rad) + ", " + "{:.4f}".format(vel_x) \
         + ", " + "{:.4f}".format(vel_y) +  "\n")
        #print([x,y,-theta_rad,vel_x,vel_y])
