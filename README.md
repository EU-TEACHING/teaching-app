# teaching-app
Repository for TEACHING application startup and deployment. This can be taken as the main access point for the TEACHING plaform developed within the EU TEACHING 2020 project.

In this repository you will find a set of TEACHING applications defined as docker compose configuration files following a parallel and distributed micro-services architecture. *Five different applications* showcasing the main features of the platform can be found in [scenarios](https://github.com/EU-TEACHING/teaching-app/tree/main/scenarios).

## Main Application Logic

The application logic is defined at the docker compose level with a graph connecting several nodes (docker images) and arcs (communications link).
Nodes can be *producers*, *consumers* or *both* and communicate via RabbitMQ. Following the INPUT_TOPIC and OUTPUT_TOPIC variables (often hardcoded within each node) is possible to understand the graph composition.

Nevertheless, every node is agnostic with respect to the graph composition and technology used in other nodes. Every node only implements a single function and process each *DataPacket* (a JSON based object) made available trought the INPUT_TOPIC.

Data flow and processing is mostly abstracted to the end TEACHING app designer and implemented in the main repository:

- [teaching-base](https://github.com/EU-TEACHING/teaching-base): Project for the base image(s) and classes.

## Implement your own TEACHING app

In order to implement a new TEACHING application, first it is important to understand if the nodes available are enough to fit your needs. 
In particular you may want to check the following repos:

- [teaching-sensors](https://github.com/EU-TEACHING/teaching-sensors): Project for all the sensors that can be instantiated, from "file" sensors to cameras and wearables.
- [teaching-data](https://github.com/EU-TEACHING/teaching-data): Project for persistent storage, e.g., the influxdb instance.
- [teaching-ai-toolkit](https://github.com/EU-TEACHING/teaching-ai-toolkit): AI-Toolkit collecting and implementing the AI modules for a TEACHING application.
- [model-transfer-service](model-transfer-service): services to encrypt and transfer parametric models.

We also offer an indipendend service (that can be run in parallel) that can be useful to model Federated Learning use-cases:

- [teaching-model-aggregator](https://github.com/EU-TEACHING/teaching-model-aggregator): Module devoted to federated model aggregation.

If these repos, do not provide the producing or consuming nodes you need. Then you can implement your own following the guidelines provided within each report.
