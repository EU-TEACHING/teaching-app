# base
Repository for the base image(s), classes and communication of the TEACHING plaform

## Introduction

This repository implements the base image(s), classes and communication of the TEACHING plaform.
It is the most important repository of the platform since it implements the node abstraction and its communication. 
As such this repository should be amended with extra care. As a TEACHING user (that defines app) or contributors (that implements additional node) we do not expect you will need to change the content of this repo, so take it mostly as a reference.

The most important classes are defined in:

- [node](https://github.com/EU-TEACHING/teaching-base/blob/main/node.py): general definition of a node in the computational graph defining a TEACHING app.
- [communication/](https://github.com/EU-TEACHING/teaching-base/tree/main/communication): directory containing all the basic classes related to the communication via RabbitMQ.

## Contact

If you want to operate some change in this repo we recommand to contact Christos Chronis (chronis@hua.gr).
