#!/bin/bash
docker build -f Dockerfile.basic_image . -t teaching_image
docker build -f Dockerfile.basic_image_Tensorflow . -t teaching_image_tensorflow