[![Requirements Status](https://requires.io/github/fabric-testbed/ControlFramework/requirements.svg?branch=cicd)](https://requires.io/github/fabric-testbed/ControlFramework/requirements/?branch=master)

# Control Framework
This repository contains Fabric Control Framework and Actor implementations.

## Overview
Fabric Control Framework has 3 actors
- Controller
- Broker
- Aggregate Manager

## Broker
Broker is an agent of CF that collects resource availability information from multiple aggregate managers and can make resource promises on their behalf. More details can be found [here](fabric_cf/broker/Readme.md)

## Aggregate Manager
AM is a CF agent responsible for managing aggregate resources. Is under the control of the owner of the aggregate. Provides promises of resources to brokers and controllers/ orchestrators. More details can be found [here](fabric_cf/authority/Readme.md)

## Orchestrator
Orchestrator is an agent of CF that makes allocation decisions (embedding) of user requests into available resources. Communicates with user to collect slice requests, communicates with broker or aggregate managers to collect resource promises, communicates with aggregate managers to provision promised resources. Creates slices, configures resources, maintains their state, modifies slices and slivers. More details can be found [here](fabric_cf/orchestrator/Readme.md)  

## Requirements
Python 3.7+

## Configuration
Example configuration files for Network AM, VM AM and Broker can be found under config directory:
```
$ ls -ltr config
total 40
-rw-r--r--  1 komalthareja  staff  4312 Jul 14 14:38 config.net-am.yaml
-rw-r--r--  1 komalthareja  staff  7277 Jul 14 14:38 config.vm-am.yaml
-rw-r--r--  1 komalthareja  staff  3746 Jul 14 14:38 config.broker.yaml
-rw-r--r--  1 komalthareja  staff  3746 Jul 14 14:38 config.orchestrator.yaml
```

## Build Docker Images

### Authority Docker Image
```
docker build -f Dockerfile-auth -t authority .
```

### Broker Docker Image
```
docker build -f Dockerfile-broker -t broker .
```

### Orchestrator Docker Image
```
docker build -f Dockerfile-orchestrator -t orchestrator .
```

## Devlopment Deployment
Development Deployment requires local Kafa cluster. Below steps specify how to bring up development Kafka Cluster
### Kafka Cluster
#### Generate Credentials
You must generate CA certificates (or use yours if you already have one) and then generate a keystore and truststore for brokers and clients.
```
cd $(pwd)/secrets
./create-certs.sh
cd -
```
Set the environment variable for the docker-compose. Copy `env.template` as `.env`. Below is shown an example configuration in `.env`
```
# docker-compose environment file
#
# When you set the same environment variable in multiple files,
# here’s the priority used by Compose to choose which value to use:
#
#  1. Compose file
#  2. Shell environment variables
#  3. Environment file
#  4. Dockerfile
#  5. Variable is not defined

# Kafka configuration
KAFKA_SSL_SECRETS_DIR=./secrets
```
#### Bring up the containers
You can use the docker-compose-kafka.yaml file to bring up a simple Kafka cluster containing
- broker
- zookeeper 
- schema registry

Use the below command to bring up the cluster
```
docker-compose -f docker-compose-kafka.yaml up -d
```

This should bring up following containers:
```
     NAMES
df0e3be0b641        confluentinc/cp-schema-registry:latest   "/etc/confluent/dock…"   7 minutes ago       Up 7 minutes        0.0.0.0:8081->8081/tcp                             schemaregistry
82a0a59c117b        confluentinc/cp-kafka:latest             "/etc/confluent/dock…"   7 minutes ago       Up 7 minutes        0.0.0.0:9092->9092/tcp, 0.0.0.0:19092->19092/tcp   broker1
1fea39fedf6a        fabrictestbed/postgres:12.3              "docker-entrypoint.s…"   7 minutes ago       Up 7 minutes        0.0.0.0:8432->5432/tcp                             actordb
c6b824b7d3c6        confluentinc/cp-zookeeper:latest         "/etc/confluent/dock…"   7 minutes ago       Up 7 minutes        2888/tcp, 0.0.0.0:2181->2181/tcp, 3888/tcp         zookeeper
```
