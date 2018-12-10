from skimage.io import imread, imsave
from skimage.transform import resize
import skimage.color as color
import scipy.ndimage.interpolation as sni
import numpy as np
import caffe

PROTOTXT_PATH = 'models/colorization_deploy_v2.prototxt'
MODEL_PATH = 'models/colorization_release_v2.caffemodel'
H_in, W_in = 224, 224
H_out, W_out = 56, 56


def init_model():
    net = caffe.Net(PROTOTXT_PATH, MODEL_PATH, caffe.TEST)
    pts_in_hull = np.load('models/pts_in_hull.npy')  # load cluster centers
    net.params['class8_ab'][0].data[:, :, 0, 0] = pts_in_hull.transpose(
        (1, 0))  # populate cluster centers as 1x1 convolution kernel
    print('Annealed-Mean Parameters populated')
    return net


def _preprocess_image(img_rgb):
    img_lab = color.rgb2lab(img_rgb)
    img_lab_bw = img_lab.copy()
    img_lab_bw[:, :, 1:] = 0
    img_rgb_bw = color.lab2rgb(img_lab_bw)
    return img_rgb_bw


def preprocess_image(inputfile, outputfile):
    img = imread(inputfile)
    img = _preprocess_image(img)
    imsave(outputfile, img)
    return True


def colorize_image(img_gray, net):
    (H_orig, W_orig) = img_gray.shape[:2]  # original image size
    img_lab = color.rgb2lab(img_gray)  # convert image to lab color space
    img_l = img_lab[:, :, 0]

    # resize image to network input size
    img_rs = (resize(img_gray, (H_in, W_in)) * 255).astype(np.uint8)
    img_lab = color.rgb2lab(img_rs)
    img_lab_intensity = img_lab[:, :, 0]

    net.blobs['data_l'].data[0, 0, :, :] = img_lab_intensity - 50  # subtract 50 for mean-centering
    net.forward()  # run network

    ab_dec = net.blobs['class8_ab'].data[0, :, :, :].transpose((1, 2, 0))  # this is our result
    ab_dec_us = sni.zoom(ab_dec,
                         (H_orig / H_out, W_orig / W_out, 1))  # upsample to match size of original image L
    img_lab_out = np.concatenate((img_l[:, :, np.newaxis], ab_dec_us),
                                 axis=2)  # concatenate with original image L
    img_rgb_out = (255 * np.clip(color.lab2rgb(img_lab_out), 0, 1)).astype('uint8')  # convert back to rgb

    return img_rgb_out


def save_image(img_rgb_out, fname):
    imsave(fname, img_rgb_out)


def process_image(inputfile, outputfile, net):
    img = imread(inputfile)
    colorized_img = colorize_image(img, net)
    imsave(outputfile, colorized_img)
    return True
