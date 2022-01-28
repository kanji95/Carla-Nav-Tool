from email.policy import default
import numpy as np
import cv2
import argparse
import os
import sys
import shutil
from pprint import pprint


# K is a (3 x 3) matrix
# world_2_camera (4, 4) matrix transforms the points from world to sensor coordinates.
# world_points is a (3 x m) matrix,
# where is the number of world points
# returns a (2 x m) matrix
def world_to_image(K,world_2_camera, world_points):
    
    world_points = np.vstack([world_points,np.ones((1,world_points.shape[1]))])
    # Transform the points from world space to camera space.
    sensor_points = np.dot(world_2_camera, world_points)

    sensor_points = np.true_divide(sensor_points[0:3, :], sensor_points[[-1], :])

    # (x, y ,z) -> (y, -z, x)
    point_in_camera_coords = np.array([
        sensor_points[1],
        sensor_points[2] * -1,
        sensor_points[0]
    ])

    # Finally we can use our K matrix to do the actual 3D -> 2D.
    points_2d = np.dot(K, point_in_camera_coords)

    # Remember to normalize the x, y values by the 3rd value.
    points_2d = np.array([points_2d[0, :] / points_2d[2, :],points_2d[1, :] / points_2d[2, :]])

    return points_2d

def annotate(args):
    os.makedirs(args.out_dir,exist_ok=True)

    for out_file in os.listdir(args.out_dir):
        shutil.rmtree(os.path.join(args.out_dir,out_file))

    episodes = os.listdir(args.dir)
    print(episodes)
    for episode in episodes:
        os.makedirs(os.path.join(args.out_dir,episode),exist_ok=True)
        print(f'Episode {episode}')
        with open(os.path.join(args.dir,episode,'vehicle_positions.txt')) as f:
            coordinates = f.readlines()
        float_coordinates = np.array([[float(x.strip()) for x in last_coordinate.split(',')] for last_coordinate in coordinates])
        target_coordinate = float_coordinates[-1]

        print(float_coordinates.shape)
        print(target_coordinate.shape)

        relative_coords = target_coordinate - float_coordinates
        print(relative_coords)

        K = np.load(os.path.join(args.dir,episode,'camera_intrinsic.npy'))


        frames = sorted(os.listdir(os.path.join(args.dir,episode,'images')))

        for i,frame in enumerate(frames):
            name = '.'.join(frame.split('.')[:-1])
            try:
                inverse_matrix = np.load(os.path.join(args.dir,episode,'inverse_matrix',name+'.npy')) 
            except:
                print('NOT FOUND:',os.path.join(args.dir,episode,'inverse_matrix',name+'.npy'))
            annotation = world_to_image(K,inverse_matrix,relative_coords[i].reshape(-1,1)).T[0]
            print(annotation)
            im = cv2.imread(os.path.join(args.dir,episode,'images',frame))
            im = cv2.circle(im, (round(annotation[0]),round(annotation[1])), 10, (0,255,0),thickness=-1)
            cv2.imwrite(os.path.join(args.out_dir,episode,frame),im)



def main():
    argparser = argparse.ArgumentParser(
        description='VLN data annotater')
    argparser.add_argument(
        '-d', '--dir',
        default='_out/',
        help='Input Data Directory Path')
    argparser.add_argument(
        '-o', '--out_dir',
        default='_annotated_out',
        help='Output Data Directory Path')
    argparser.add_argument(
        '-n', '--height',
        default=720,
        help='input image height')
    argparser.add_argument(
        '-m', '--width',
        default=1280,
        help='input image width')
    args = argparser.parse_args()
    annotate(args)

if __name__=='__main__':
    main()