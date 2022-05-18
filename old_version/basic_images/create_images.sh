#!/bin/bash
echo "Start building Basic Image"
docker build -f Dockerfile.basic_image . -t teaching_image
echo "Basic Image Finished!"
echo "Start building Tensorflow Image"
docker build -f Dockerfile.basic_image_Tensorflow . -t teaching_image_tensorflow
echo "Tensorflow Image Finished!"
echo "Create Image for video server"
docker pull tiangolo/nginx-rtmp
docker image tag tiangolo/nginx-rtmp rtmp_server
echo "Video server Finished!"