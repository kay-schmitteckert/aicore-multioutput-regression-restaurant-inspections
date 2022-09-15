# Digitizing Criticality Assessments using SAP AI Core and SAP AI Launchpad

## Use Case

Assessing risk or criticality often requires manual input from experts and rarely benefits
from past assessments. This makes the overall process time-consuming and potentially leads
to inconsistency over time. To digitize the computation of the criticality, we propose a
machine learning (ML) service for criticality assessments in this mission. The
assessments that are used throughout this mission are exemplary and based on restaurant
inspections where a health inspector, the expert, screens a restaurant and protocols
violations. In the end the inspector comes up with a suitable score for the
restaurant. The provided data comes from a publicly available dataset
(Restaurant Scores - LIVES Standard in San Francisco published by Public Health) which has
been restructured to fit the ML approach of multi-output-regression. Since the SAP Data Attribute Recommendation service
(DAR) does not support multi-output-regression yet, this mission showcases a solution
leveraging SAP AI Core and open source. The approach of this mission can be easily adapted
to similar kinds of criticality assessments.
 
This mission is based on a real customer use case about criticality assessments which is currently in productization.

## Current Position - What is the challenge?

Organizations can have complex rules for their criticality assessments. Many times, the
assessment is dominated by manual input, which is prone to errors and can be time-consuming.
Besides that, due to individual approaches of different processors, inconsistencies can
arise over the time, yielding different results for similar inputs.

## Destination - What is the outcome?

The solution uses ML to assist the processor of criticality assessments by translating descriptions and details of a criticality assessment to multiple scores necessary to conclude the assessment.

## How You Get There - What is the solution?

A machine learning service that leverages the capabilities of SAP Business Technology Platform
(SAP AI Core and SAP AI Launchpad). The service assesses the criticality based on the descriptions of the criticality
assessment itself. In this case the descriptions are the violations the
inspector protocols during the inspections. Since the descriptions consist of unstructured
text, they first will be transformed to vectors, so-called embeddings. Finally,
a multi-output-regression can be performed to determine multiple scores.

## Mandatory steps

1. [Upload training data to Amazon S3 bucket](mission/upload-data-s3.md)
2. [Build and push Docker images for training and serving](mission/build-push-docker-imgs.md)
3. [Register general artifacts](mission/register-general-artifacts.md)
4. [Setup and execute training](mission/setup-execution-training.md)
5. [Setup and deploy inference service](mission/setup-deployment-inference-service.md)
6. [Test inference service](mission/test-deployed-service.md)

## Boilerplate for AI Core

This is to have a starting point to use AI Core through the AI Core Python SDK.

### Usage instructions

- Install the requirements listed in ./requirements.txt
- Look at lifecycle.py to get an overview. Here the interaction with the AI Core instance takes place,
  and the ML lifecycle is managed.
- In resources/
    - Insert the service key of the AI Core instance into aic_service_key.json
    - Add docker credentials to docker_secret.json. It is recommended to use a Docker Hub personal access
      token here instead of the original Docker Hub password.
    - Add details for the repository that will be onboarded later and synced to AI Core
        - Also specify a name for the application
    - Add credentials for Amazon S3 bucket to s3_service_key.json
    - *Make sure to not publish the resources/ directory as it includes secrets and credentials.*
- Integrate your own training script into code/train/train.py.
    - `environ["DATA_SOURCE"]` is the path in the docker container file system to load the dataset from.
    - Notice that the training dataset has to be uploaded manually to the Amazon S3 bucket.
    See https://developers.sap.com/tutorials/ai-core-aiapi-clientsdk-resources.html#45dcbe5b-a94f-461e-b9eb-54f2d965e930
    - `environ["OUTPUT_PATH"]` is the path the trained model should be saved to after training.
- In code/infer/infer.py
    - Change model_name to the name used when the trained model was previously saved to
      `environ["OUTPUT_PATH"]`
    - For the prediction route: Replace `regrmodel` with the model name specified in
      workflows/serving_workflow.yaml
    - Based on what the model expects as input for the prediction select the correct field from the inference
      request => Adjust `[input_data["text"]]`
- Add to code/train/requirements.txt the requirements to run the train.py training script. Do the equivalent
  for code/infer/requirements.txt with respect to the infer.py script.
- Build the Dockerfiles and upload the images to a Docker Hub repository. Tags can be used to differentiate between
  different Docker images here. See
  https://developers.sap.com/tutorials/ai-core-aiapi-clientsdk-workflows.html#f824a41d-efe8-4883-8238-caef4ac5f789
  Adjust the URLs for the Docker images in workflows/serving_workflow.yaml and
  workflows/training_workflow.yaml as necessary. 
- Take a look at the Dockerfiles in code/train/ and code/infer/. Make sure the python base image specified at
  line 3 is compatible with the python version used locally to install the required python packages. If
  python 3.8.10 was used to install the required packages and the requirements.txt file was created with
  `pip freeze > requirements.txt` one will want to use for example `FROM python:3.8-slim` as python base image
  instead. Otherwise, the versions of some packages might not be available when the requirements are installed
  in the docker container based on the python version of the specified Docker python base image.
- Adjust the naming in workflows/serving_workflow.yaml and workflows/training_workflow.yaml as appropriate for
  the AI Scenario.
- Execute each step in lifecycle.py