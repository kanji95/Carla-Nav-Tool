# Ground then Navigate: Language-guided Navigation in Dynamic Scenes (ICRA 2023)

Official Code | [Paper](https://arxiv.org/pdf/2209.11972.pdf) | [Video](https://youtu.be/bSwtb6APGns)

## Abstract
> We investigate the Vision-and-Language Navigation (VLN) problem in the context of autonomous driving in outdoor settings. We solve the problem by explicitly grounding the navigable regions corresponding to the textual command. At each timestamp, the model predicts a segmentation mask corresponding to the intermediate or the final navigable region. Our work contrasts with existing efforts in VLN, which pose this task as a node selection problem, given a discrete connected graph corresponding to the environment. We do not assume the availability of such a discretised map. Our work moves towards continuity in action space, provides interpretability through visual feedback and allows VLN on commands requiring finer manoeuvres like "park between the two cars". Furthermore, we propose a novel meta-dataset CARLA-NAV to allow efficient training and validation. The dataset comprises pre-recorded training sequences and a live environment for validation and testing. We provide extensive qualitative and quantitive empirical results to validate the efficacy of the proposed approach.

![Screenshot 2023-06-20 at 3 06 06 PM](https://github.com/kanji95/Carla-Nav/assets/30688360/3866fa1d-bd8c-47b4-89cc-13fb9966e4d4)
 
 
## Usage

Build Carla by following the instructions in this repo: https://github.com/carla-simulator/carla

Run the following Command to start the server
> CarlaUE4.exe -windowed -carla-server -quality-level=Low

Run the following command to start data collection on client side
> python data_collect.py --host <HOST_ID> --port <PORT_NUM> --map <MAP_ID> 

## Acknowledgements

Code borrowed from: https://github.com/carla-simulator/carla/tree/master/PythonAPI/examples
