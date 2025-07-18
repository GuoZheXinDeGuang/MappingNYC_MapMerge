# Map Merging Process Instructions

## 1. Convert from Interactive SLAM format
First, run `convert2odomsaver.py`:

```python
map1_dir = "path/to/input/interactive_slam_format"    # Contains 000000/, 000001/, etc.
output_dir = "path/to/output/odom_saver_format"       # Will contain timestamp.pcd/.odom
```

## 2. Transform and Merge
Make sure you have converted 2 maps. Then, we run `transform.py`:

```python
map1_dir = "path/to/first/corrected_map"     # Directory with timestamp.pcd/.odom files
map2_dir = "path/to/second/corrected_map"    # Directory with timestamp.pcd/.odom files
output_dir = "path/to/merged/map"            # Output directory for merged map
```

## 3. Visualize using interactive_slam
Finally you can open the file you saved from the python code, run the following command:
```bash
rosrun interactive_slam odometry2graph
```
Open the file you just merged, and you can do further adjustment using InteractiveSlam.
