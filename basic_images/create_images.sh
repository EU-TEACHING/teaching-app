#!/bin/bash
echo "Start building Basic Image"
docker build -f Dockerfile.basic_image . -t teaching_image
echo "Basic Image Finished!"
echo "Start building Tensorflow Image"
docker build -f Dockerfile.basic_image_Tensorflow . -t teaching_image_tensorflow
echo "Tensorflow Image Finished!"