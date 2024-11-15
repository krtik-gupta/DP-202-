import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance

imgleft = cv.imread(r"D:\Projects\DP Projecrt\DepthEst\try[1]\try\Photo\photo_2024-11-10_16-06-18.jpg", 0)
imgright = cv.imread(r"D:\Projects\DP Projecrt\DepthEst\try[1]\try\Photo\photo_2024-11-10_16-06-21.jpg", 0)

stereo = cv.StereoSGBM_create(
    minDisparity=0,
    numDisparities=128,
    blockSize=11,
    P1=8 * 3 * 11 ** 2,
    P2=32 * 3 * 11 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32
)
disparity = stereo.compute(imgleft, imgright).astype(np.float32) / 16.0
disparity[disparity <= 0] = 0.1

f = 1.8  
B = 1.2  
depth_map = (f * B) / (disparity + 1e-5)

points = []

def calculate_depth_between_points(p1, p2):
    dist = distance.euclidean(p1, p2)
    depth_values = []
    
    x_vals = np.linspace(p1[0], p2[0], int(dist))
    y_vals = np.linspace(p1[1], p2[1], int(dist))
    
    for x, y in zip(x_vals, y_vals):
        depth_values.append(depth_map[int(y), int(x)])
    
    avg_depth = np.mean(depth_values)
    print(f"Average depth between {p1} and {p2}: {avg_depth:.2f} meters")
    return avg_depth

def on_click(event):
    if event.inaxes:
        x, y = int(event.xdata), int(event.ydata)
        depth = depth_map[y, x]
        points.append((x, y))
        
        if len(points) == 2:
            avg_depth = calculate_depth_between_points(points[0], points[1])
            ax.set_title(f"Depth between {points[0]} and {points[1]}: {avg_depth:.2f} meters")
            fig.canvas.draw()
            points.clear()
        else:
            ax.set_title(f"Depth at ({x}, {y}): {depth:.2f} meters")
        
        fig.canvas.draw()

fig, ax = plt.subplots(figsize=(10, 5))
real_img_disp = ax.imshow(imgleft, cmap='gray')
plt.axis('off')
ax.set_title("Click on the real image to display depth")
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
