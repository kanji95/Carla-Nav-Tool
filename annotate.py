from email.policy import default
import numpy as np
import cv2
import argparse
import os
import sys
import shutil
from pprint import pprint


def world_to_pixel(K, rgb_matrix, destination,  curr_position):

    point_3d = np.ones((4, destination.shape[1]))
    point_3d[0] = destination[0]
    point_3d[1] = destination[1]
    point_3d[2] = curr_position[2]

    # point_3d = np.array([destination[0], destination[1], curr_position[2], 1])
    point_3d = np.round(point_3d, decimals=2)
    # print("3D world coordinate: ", point_3d)

    cam_coords = rgb_matrix @ point_3d
    # cam_coords = rgb_matrix @ point_3d[:, None]
    cam_coords = np.array([cam_coords[1], cam_coords[2]*-1, cam_coords[0]])
    points_2d = np.dot(K, cam_coords)

    points_2d = np.array([
        points_2d[0, :] / points_2d[2, :],
        points_2d[1, :] / points_2d[2, :],
        points_2d[2, :]]
    )
    points_2d = points_2d.reshape(3, -1)
    points_2d = np.round(points_2d, decimals=2)
    return points_2d


def annotate(args):
    os.makedirs(args.out_dir, exist_ok=True)

    for out_file in os.listdir(args.out_dir):
        shutil.rmtree(os.path.join(args.out_dir, out_file))

    episodes = os.listdir(args.dir)
    print(episodes)
    for episode in episodes:
        os.makedirs(os.path.join(args.out_dir, episode), exist_ok=True)
        print(f'Episode {episode}')
        with open(os.path.join(args.dir, episode, 'vehicle_positions.txt')) as f:
            coordinates = f.readlines()
        float_coordinates = np.array([[float(x.strip()) for x in last_coordinate.split(
            ',')] for last_coordinate in coordinates])
        target_coordinate = float_coordinates[-1]

        print(float_coordinates.shape)
        print(target_coordinate.shape)

        relative_coords = target_coordinate - float_coordinates
        print(relative_coords)

        K = np.load(os.path.join(args.dir, episode, 'camera_intrinsic.npy'))

        frames = sorted(os.listdir(os.path.join(args.dir, episode, 'images')))

        for i, frame in enumerate(frames):
            name = '.'.join(frame.split('.')[:-1])
            try:
                inverse_matrix = np.load(os.path.join(
                    args.dir, episode, 'inverse_matrix', name+'.npy'))
            except:
                print('NOT FOUND:', os.path.join(
                    args.dir, episode, 'inverse_matrix', name+'.npy'))

            # annotation = world_to_pixel(
            #     K, inverse_matrix, target_coordinate, relative_coords[i])
            im = cv2.imread(os.path.join(args.dir, episode, 'images', frame))

            x_offsets = np.linspace(-2, 2, num=150)
            y_offsets = np.linspace(-2, 2, num=150)
            X, Y = np.meshgrid(x_offsets, y_offsets)

            mesh = np.dstack([X, Y])

            mesh = mesh.reshape(-1, 2)

            mesh = np.hstack([mesh, np.zeros((mesh.shape[0], 1))]).T

            annotations = world_to_pixel(
                K, inverse_matrix, target_coordinate.reshape(3, 1)+mesh, relative_coords[i]).T

            for i in range(annotations.shape[0]):
                im = cv2.circle(im, (round(annotations[i, 0]), round(
                    annotations[i, 1])), 3, (0, 255, 0), thickness=-1)

            # for x_offset in np.linspace(-2, 2, num=150):
            #     for y_offset in np.linspace(-2, 2, num=150):
            #         annotation = world_to_pixel(
            #             K, inverse_matrix, target_coordinate+np.array([x_offset, y_offset, 0]), relative_coords[i])
            #         im = cv2.circle(im, (round(annotation[0]), round(
            #             annotation[1])), 2, (0, 255, 0), thickness=-1)
            cv2.imwrite(os.path.join(args.out_dir, episode, frame), im)


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


if __name__ == '__main__':
    main()
