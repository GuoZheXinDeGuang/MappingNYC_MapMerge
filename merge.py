import os
import numpy as np
import shutil
from geometry_msgs.msg import PoseStamped
import tf.transformations as tf
from scipy.spatial.transform import Rotation as R

def apply_transform(matrix_ori, transform):
    """Apply a transformation matrix to a Pose."""
    transformed_matrix = np.dot(transform, matrix_ori)
    return transformed_matrix


def read_data(file_path):
    timestamp = None
    estimate_matrix = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        # 读取时间戳
        if line.startswith("stamp"):
            timestamp_parts = line.split()
            if len(timestamp_parts) == 3:
                timestamp = float(f"{timestamp_parts[1]}.{timestamp_parts[2]}")
       
        # 读取 estimate 部分的矩阵
        if line.strip() == "estimate":
            for j in range(1, 5):  # 下一行到第四行包含矩阵数据
                matrix_line = lines[i + j].strip()
                estimate_matrix.append([float(value) for value in matrix_line.split()])

    return timestamp, estimate_matrix

def save_matrix_to_file(timestamp, estimate_matrix, dest):
    """
    将估计矩阵保存到以时间戳命名的文件中。

    :param timestamp: 时间戳，作为文件名的一部分
    :param estimate_matrix: 估计矩阵,4x4的二维列表
    :param directory: 文件保存的目录，默认为当前目录
    """
    # 创建文件名
    filename = f"{timestamp}.odom"
    file_path = f"{dest}/{filename}"

    # 将矩阵写入文件
    with open(file_path, "w") as file:
        for row in estimate_matrix:
            file.write(" ".join(f"{value: .6f}" for value in row) + "\n")

def main(total_dir, dest):
    global_transform = np.eye(4)  # Start with an identity matrix for the first bag
    if not os.path.exists(dest):
        # 创建文件夹
        os.makedirs(dest)
    for i, dir in enumerate(total_dir):

        files = os.listdir(dir)
        if i > 0:
            global_transform = prev_matrix

        prev_time = 0
        for item in files:
            data_path = os.path.join(dir, item) + '/data'
            pcd_path = os.path.join(dir, item) + '/cloud.pcd'
            timestamp, estimate_matrix = read_data(data_path)
            transformed_matrix = apply_transform(estimate_matrix, global_transform)
            save_matrix_to_file(timestamp=timestamp, estimate_matrix= transformed_matrix, dest=dest)
            if timestamp > prev_time:
                prev_matrix = transformed_matrix
                prev_time = timestamp

            pcd_file_name = f"{timestamp}.pcd"
            pcd_file_path = f"{dest}/{pcd_file_name}"
            shutil.copy(pcd_path, pcd_file_path)

if __name__ == "__main__":
    input_dir = '/home/xl5444/dataset/'
    input_bags = ['15-46-20', '12-42-59']
    for i in range(len(input_bags)):
        input_bags[i] = input_dir + input_bags[i]

    dest = '/home/xl5444/dataset/test'
    main(input_bags, dest)