# robotframework-compareimage

======================================
Robot Framework Compare Images Keyword
======================================

Robot Framework keywords to compare two images.

Background
==========

What brought us to here, was the need of a way of performing UI tests on web applications using robotframework. We wanted to go with the approach based on screenshot regression tests, i.e. take screenshots of the views, validate them as 'good' and use them as references. Later, perform regression tests comparing the new screenshots against the references to detect problems in the layout of the views.

The basis of this is an image comparison tool and after some research we decided to use with PerceptualDiff.

Requirements
============

- Perceptual diff

Usage
=====

The keyword Compare Images can be use in a robot framework test as a normal keyword.

It takes two arguments: the reference image path and the test image path.

.. code:: robotframework
	...
	Compare Images		ref.png		test.png
	...

If the reference does not exists, the test image is stored in the given location as reference and the test pass.

If both images looks the same, the test pass.

If the images are different, the test fails and in the html report is shown the reference image with the problematic pixels highlighted.
	
Notes
===== 

The keyword expects that the reference and test images have the same size.

