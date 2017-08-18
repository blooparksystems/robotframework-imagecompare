import os
import re
import shutil
import subprocess

from PIL import Image
from robot.api import logger


def compare_images(baseline_img, test_img):
    """
    :param baseline_img: baseline image to compare with
    :param test_img: image to be tested against the baseline image
    :return: True if the images are very similar, raise an error otherwise

    Compare images as in a regression test.
    If the baseline_img does not exist, but the folder for them does, the
    test image is saved as baseline image.
    """

    # Check that the testing image exists
    if not os.path.exists(test_img):
        raise AssertionError('Unexisting test image')

    # Check if the baseline image and folder exists
    if not os.path.exists(baseline_img):

        baseline_path, baseline_file = os.path.split(baseline_img)
        # Check if the baseline folder exists
        if not os.path.exists(baseline_path):
            raise AssertionError('Unexisting baseline folder')

        # If there was not a baseline image, adopt the testing image
        shutil.copy(test_img, baseline_img)

    # check if there is a reference for this image
    if os.path.exists(baseline_img):

        # check if the diff files were not deleted
        diff_ppm = test_img.replace(".png", ".diff.ppm")
        diff_png = diff_ppm.replace("diff.ppm", "diff.png")
        for img in [diff_ppm, diff_png]:
            if os.path.exists(img):
                os.remove(img)

        # parameters to perceptualdiff
        vals = {
            'output': diff_ppm,
            'baseline': baseline_img,
            'test_img': test_img,
        }
        cmd = "perceptualdiff -output {output} {baseline} {test_img}".\
            format(**vals)

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        perceptualdiff_stdout, _ = process.communicate()

        process.wait()

        # Check how to know when the perceptualdiff crashed
        if process.returncode != 0:

            # When the output is 'Images are visibly different'
            # the diff image should have been created
            if not re.match('.*Images are visibly different.*',
                            perceptualdiff_stdout):

                if os.path.exists(diff_ppm):
                    os.remove(diff_ppm)
                raise AssertionError('An error ocurred while comparing '
                                     'the images: ' + perceptualdiff_stdout)

        # if the diff_ppm was created, differences were found
        if os.path.exists(diff_ppm):
            # convert image form ppm to png
            diff_img = Image.open(diff_ppm)
            R, G, B = diff_img.split()
            base_img = Image.open(baseline_img)
            # The diff image is black with differences pixels in blue
            # Use the blue band to create a mask, and put on the base image
            Image.composite(diff_img, base_img, B).save(diff_png)
            os.remove(diff_ppm)
            logger.info("<img src='%s' width='800px'>" % diff_png, html=True)
            raise AssertionError('Images missmatched')

    return True
