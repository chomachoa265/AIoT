import argparse
import cv2
import numpy as np
import torch
from torchvision import models
import sys
np.set_printoptions(threshold=sys.maxsize)

from pytorch_grad_cam import GradCAM, \
                             ScoreCAM, \
                             GradCAMPlusPlus, \
                             AblationCAM, \
                             XGradCAM, \
                             EigenCAM, \
                             EigenGradCAM

from pytorch_grad_cam import GuidedBackpropReLUModel
from pytorch_grad_cam.utils.image import show_cam_on_image, \
                                         deprocess_image, \
                                         preprocess_image

from .stitcher import *                                         

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-cuda', action='store_true', default=False,
                        help='Use NVIDIA GPU acceleration')
    parser.add_argument('--image-path', type=str, default='./examples/both.png',
                        help='Input image path')
    parser.add_argument('--aug_smooth', action='store_true',
                        help='Apply test time augmentation to smooth the CAM')
    parser.add_argument('--eigen_smooth', action='store_true',
                        help='Reduce noise by taking the first principle componenet'
                        'of cam_weights*activations')
    parser.add_argument('--method', type=str, default='gradcam',
                        help='Can be gradcam/gradcam++/scorecam/xgradcam'
                             '/ablationcam/eigencam/eigengradcam')

    args = parser.parse_args()
    args.use_cuda = args.use_cuda and torch.cuda.is_available()
    if args.use_cuda:
        print('Using GPU for acceleration')
    else:
        print('Using CPU for computation')

    return args

def gradCAM(image):
    args = get_args()
    methods = \
        {"gradcam": GradCAM, 
         "scorecam": ScoreCAM, 
         "gradcam++": GradCAMPlusPlus,
         "ablationcam": AblationCAM,
         "xgradcam": XGradCAM,
         "eigencam": EigenCAM,
         "eigengradcam": EigenGradCAM}

    if args.method not in list(methods.keys()):
        raise Exception(f"method should be one of {list(methods.keys())}")

    model = models.resnet50(pretrained=True)
    target_layer = model.layer4[-1]


    if args.method not in methods:
        raise Exception(f"Method {args.method} not implemented")
    print(args.method)
    cam = methods[args.method](model=model, 
                               target_layer=target_layer,
                               use_cuda=args.use_cuda)
    # input images are as follows:
    # panorama = run_main(images)
    # paths = [path]
    # img_num = 1
    # img_dir = "./media/53/results/panorama"
    # for i in range(img_num):
    #     img_name = img_dir + ".jpg"
    #     paths.append(img_name)
    rgb_images = []
    input_tensors = []
    # for path in paths:
        # rgb_img = cv2.imread(path, 1)[:, :, ::-1]
    rgb_img = cv2.resize(image, (224, 224))
    rgb_img = np.float32(rgb_img) / 255
    rgb_images.append(rgb_img.copy())
    input_tensor = preprocess_image(rgb_img, mean=[0.485, 0.456, 0.406], 
                                                std=[0.229, 0.224, 0.225])
    input_tensors.append(input_tensor)

    input_tensor = torch.cat(input_tensors)
    target_category = None
    cam.batch_size = 32
    grayscale_cam = cam(input_tensor=input_tensor,
                        target_category=target_category,
                        aug_smooth=args.aug_smooth,
                        eigen_smooth=args.eigen_smooth)

    for index, (cam, rgb_img) in enumerate(zip(grayscale_cam, rgb_images)):
        cam_image = show_cam_on_image(rgb_img, cam)
        # cv2.imwrite("./output_imgs/grad_cam_panorama.jpg", cam_image)
    return cam_image
   