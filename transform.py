import os
import numpy as np
import open3d as o3d
import shutil

def read_last_pose_from_map(map_dir):
   """Read the last pose from first map"""
   # Get sorted timestamps
   timestamps = sorted([f.split('.')[0] for f in os.listdir(map_dir) if f.endswith('.odom')])
   if not timestamps:
       raise Exception("No odom files found")
   
   # Read last odom
   last_ts = timestamps[-1]
   last_odom_path = os.path.join(map_dir, f"{last_ts}.odom")
   last_pose = np.loadtxt(last_odom_path)
   return last_pose, last_ts

def read_first_pose_from_map(map_dir):
   """Read the first pose from second map"""
   # Get sorted timestamps
   timestamps = sorted([f.split('.')[0] for f in os.listdir(map_dir) if f.endswith('.odom')])
   if not timestamps:
       raise Exception("No odom files found")
   
   # Read first odom
   first_ts = timestamps[0]
   first_odom_path = os.path.join(map_dir, f"{first_ts}.odom")
   first_pose = np.loadtxt(first_odom_path)
   return first_pose, first_ts

def transform_and_save_map(map1_dir, map2_dir, output_dir, transform_matrix):
   """Transform odoms and copy pcds directly"""
   print(f"Processing and merging maps...")
   os.makedirs(output_dir, exist_ok=True)
   
   # First, copy all files from map1
   print("Copying first map...")
   for filename in os.listdir(map1_dir):
       src_path = os.path.join(map1_dir, filename)
       dst_path = os.path.join(output_dir, filename)
       shutil.copy2(src_path, dst_path)
   
   # Then process map2: transform odom and copy pcd directly
   print("Processing second map...")
   for filename in os.listdir(map2_dir):
       if filename.endswith('.odom'):
           timestamp = filename[:-5]
           
           # Transform odom
           odom_path = os.path.join(map2_dir, filename)
           odom = np.loadtxt(odom_path)
           transformed_odom = transform_matrix @ odom
           
           # Save transformed odom
           output_odom_path = os.path.join(output_dir, filename)
           np.savetxt(output_odom_path, transformed_odom)
           print(f"Transformed odom: {filename}")
           
           # Just copy pcd file
           pcd_filename = f"{timestamp}.pcd"
           src_pcd_path = os.path.join(map2_dir, pcd_filename)
           dst_pcd_path = os.path.join(output_dir, pcd_filename)
           if os.path.exists(src_pcd_path):
               shutil.copy2(src_pcd_path, dst_pcd_path)
               print(f"Copied pcd: {pcd_filename}")

def main():
   # Set paths for both maps
   map1_dir = "/home/lee/Desktop/Code_For_Data_Processing/odom1/"     # Directory with timestamp.pcd/.odom files
   map2_dir = "/home/lee/Desktop/Code_For_Data_Processing/odom2/"    # Directory with timestamp.pcd/.odom files
   output_dir = "/home/lee/Desktop/Code_For_Data_Processing/odom1+2v2/"   # Output directory for merged map
   
   try:
       # Get connecting poses
       last_pose, last_ts = read_last_pose_from_map(map1_dir)
       first_pose, first_ts = read_first_pose_from_map(map2_dir)
       
       print(f"Last pose of map1 (timestamp {last_ts}):")
       print(last_pose)
       print(f"\nFirst pose of map2 (timestamp {first_ts}):")
       print(first_pose)
       
       # Calculate transform matrix: T = P1 @ inv(P2)
       transform_matrix = last_pose @ np.linalg.inv(first_pose)
       print("\nTransform matrix:")
       print(transform_matrix)
       
       # Transform and merge maps
       transform_and_save_map(map1_dir, map2_dir, output_dir, transform_matrix)
       
       print("\nMap merge completed successfully!")
       
   except Exception as e:
       print(f"Error during merge: {e}")

if __name__ == "__main__":
   main()