#!/bin/bash
echo "Start building Basic Image"
docker build -f Dockerfile.basic_image_ARM . -t teaching_image
echo "Basic Image Finished!"
echo "Start building Tensorflow Image"
docker build -f Dockerfile.basic_image_Tensorflow_ARM . -t teaching_image_tensorflow
echo "Tensorflow Image Finished!"
echo "Create Image for video server"
docker pull ajeetraina/nginx-rtmp-arm
docker image tag ajeetraina/nginx-rtmp-arm rtmp_server
echo "Video server Finished!"