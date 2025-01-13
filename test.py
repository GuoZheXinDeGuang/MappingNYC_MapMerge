import open3d as o3d
import numpy as np

def visualize_two_pcds(pcd1_path, pcd2_path):
    """Visualize two PCDs to check their relative distance"""
    # Load PCDs
    pcd1 = o3d.io.read_point_cloud(pcd1_path)
    pcd2 = o3d.io.read_point_cloud(pcd2_path)
    
    # Color them differently
    pcd1.paint_uniform_color([1, 0, 0])  # Red for first pcd
    pcd2.paint_uniform_color([0, 0, 1])  # Blue for second pcd
    
    # Print some basic info
    print("PCD1 points:", np.asarray(pcd1.points).shape[0])
    print("PCD2 points:", np.asarray(pcd2.points).shape[0])
    
    # Calculate bounds
    points1 = np.asarray(pcd1.points)
    points2 = np.asarray(pcd2.points)
    
    print("\nPCD1 bounds:")
    print("Min:", points1.min(axis=0))
    print("Max:", points1.max(axis=0))
    
    print("\nPCD2 bounds:")
    print("Min:", points2.min(axis=0))
    print("Max:", points2.max(axis=0))
    
    # Visualize
    o3d.visualization.draw_geometries([pcd1, pcd2])

# Using some examples：
pcd1_path = "/home/lee/Desktop/Code_For_Data_Processing/part_1_interactiveslam/000000/cloud.pcd"
pcd2_path = "/home/lee/Desktop/Code_For_Data_Processing/odom1+2/1729784198_373063564.pcd"
# pcd2_path = "/home/lee/Desktop/Code_For_Data_Processing/odom2/1729784198_373063564.pcd"

visualize_two_pcds(pcd1_path, pcd2_path)
