from email.policy import default
import numpy as np
import cv2
import argparse
import os
import sys
import shutil
from pprint import pprint


# K is a (3 x 3) matrix
# world_points is a (3 x m) matrix,
# where is the number of world points
# returns a (2 x m) matrix
def world_to_image(K, world_points, image_height, image_width):
    print(image_height,image_width)
    K[0][2] = image_height / 2
    K[1][2] = image_width / 2
    pprint(K)
    image_points = K @ world_points
    image_points = np.true_divide(image_points[0:2, :], image_points[[-1], :])
    # return image_points[(image_points[:, 0] <= image_height) & (image_points[:,0] > 0) & (image_points[:, 1] <= image_width) & (image_points[:,1] > 0), :]
    return image_points

def annotate(args):
    os.makedirs(args.out_dir,exist_ok=True)

    for out_file in os.listdir(args.out_dir):
        shutil.rmtree(os.path.join(args.out_dir,out_file))

    episodes = os.listdir(args.dir)
    print(episodes)
    for episode in episodes:
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

        annotations = world_to_image(K,relative_coords.T,args.height,args.width).T
        print(annotations.shape)

        frames = sorted(os.listdir(os.path.join(args.dir,episode)))

        for i,frame in enumerate(frames):
            annotation = annotations[i]
            print(annotation)
            im = cv2.imread(os.path.join(args.dir,episode,frame))
            im = cv2.circle(im, (annotation[1],annotation[0]), 3, (0,255,0),thickness=-1)
            cv2.imwrite(os.path.join(args.out_dir,episode,frame),im)

        K = np.load(os.path.join(args.dir,episode,'vehicle_positions.txt'))

        image = cv2.imread()


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