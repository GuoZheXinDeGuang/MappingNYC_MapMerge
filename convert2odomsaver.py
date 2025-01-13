import os
import numpy as np
import shutil
def convert_interactive_to_odom(input_dir, output_dir):
   """
   Convert from interactive_slam format to odom_saver format
   
   input_dir format:
       000000/
           cloud.pcd
           data (contains estimate & odom matrices)
       000001/
           ...
           
   output_dir format:
       timestamp.pcd
       timestamp.odom
       ...
   """
   print(f"Converting from {input_dir} to {output_dir}")
   os.makedirs(output_dir, exist_ok=True)

   # Iterate through numbered directories
   for node_dir in sorted(os.listdir(input_dir)):
       if not node_dir.isdigit():
           continue
           
       node_path = os.path.join(input_dir, node_dir)
       if not os.path.isdir(node_path):
           continue
           
       print(f"\nProcessing node {node_dir}")
       
       # Read data file
       data_path = os.path.join(node_path, 'data')
       try:
           with open(data_path, 'r') as f:
               lines = f.readlines()
               
           # Get timestamp
           stamp_line = lines[0].strip()
           if stamp_line.startswith('stamp'):
               sec, nsec = stamp_line.split()[1:]
               timestamp = f"{sec}_{nsec}"
           
           # Output paths for this node
           pcd_output = os.path.join(output_dir, f"{timestamp}.pcd")
           odom_output = os.path.join(output_dir, f"{timestamp}.odom")
           
           # Copy pcd file
           pcd_input = os.path.join(node_path, 'cloud.pcd')
           if os.path.exists(pcd_input):
               shutil.copy2(pcd_input, pcd_output)
               print(f"Copied PCD: {pcd_output}")
           
           # Get estimate matrix and save as odom
           estimate_matrix = []
           in_estimate = False
           for line in lines[1:]:  # Skip stamp line
               line = line.strip()
               if line == 'estimate':
                   in_estimate = True
                   continue
               elif line == 'odom':
                   break
                   
               if in_estimate and line:
                   matrix_row = [float(x) for x in line.split()]
                   estimate_matrix.append(matrix_row)
           
           # Save estimate matrix as odom
           if estimate_matrix:
               estimate_matrix = np.array(estimate_matrix)
               np.savetxt(odom_output, estimate_matrix)
               print(f"Saved odom: {odom_output}")
               
       except Exception as e:
           print(f"Error processing {node_dir}: {e}")

def main():
   input_dir = "/home/lee/Desktop/Code_For_Data_Processing/part_2_interactiveslam/"    # Contains 000000/, 000001/, etc.
   output_dir = "/home/lee/Desktop/Code_For_Data_Processing/odom2/"            # Will contain timestamp.pcd/.odom
   
   convert_interactive_to_odom(input_dir, output_dir)

if __name__ == "__main__":
   main()