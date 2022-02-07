#!/bin/bash
docker build -f Dockerfile.basic_image_ARM . -t teaching_image
docker build -f Dockerfile.basic_image_Tensorflow_ARM . -t teaching_image_tensorflow