## Overview

This demo is intended to introduce a set of GCP products used to build modern data pipelines. Specifically, we will focus on the personas in this lifecycle and thier coresponding products of interest. The demo should cover processes related to ingestion (streaming & batch), data manipulation (transformations), and end user interactions (reporting).

Personas to Products:
- Business Report User - Data Studio
- Analyst/Data Engineer - Data Prep, Pub Sub, Dataflow
- Data Scientest - Datalab
- Developer - Cloud SDK

For this sample architecture, we've leveraged a publicly available data set from NASA which has recorded the meteors that have fallen to earth.

## Architecture
![GCP MDP Arch](/documents/gcp-mdp-arch-diagram.png)

## Getting Started (5 mins)

Navigate to the GCP console (https://console.cloud.google.com). You'll need a google account with billing enabled to continue building out your MDP. First time GCP users may have free credits.

![GCP Console SS](documents/gcp%20ss/GCP%20Console%20SS.png)

Let's create a new project. We can click on the projects tab towards the top left. Here we'll see a pop up menu with a list of our projects and the option to create a new project. Click New Project on the top right. 

![GCP Projects](documents/gcp%20ss/GCP%20Projects%20Menu%20SS.png)

Provide a name for your project and click CREATE.

![GCP New Project](documents/gcp%20ss/GCP%20New%20Proj%20SS.png)

## Batch Process (30-40 mins)

For the batch process we'll be using a combination of Cloud Storage, Dataprep, Dataflow, and BigQuery. We'll start by uploading our raw JSON file to Cloud Storage. Dataprep will then be able to connect to our JSON file to apply any data transformations and send the output to BigQuery. Dataflow helps to orchestrate this process and provide the requried resources. 

#### Quick Product Overview (as per GCP documentation)

Cloud Storage - Cloud Storage allows world-wide storage and retrieval of any amount of data at any time. You can use Cloud Storage for a range of scenarios including serving website content, storing data for archival and disaster recovery, or distributing large data objects to users via direct download.

Dataprep - Use Cloud Dataprep to explore and transform raw data from disparate and/or large datasets into clean and structured data for further analysis and processing.

Dataflow - Cloud Dataflow is a managed service for executing a wide variety of data processing patterns. The documentation on this site shows you how to deploy your batch and streaming data processing pipelines using Cloud Dataflow, including directions for using service features.

BigQuery - BigQuery is Google's fully managed, petabyte scale, low cost analytics data warehouse. BigQuery is NoOps—there is no infrastructure to manage and you don't need a database administrator—so you can focus on analyzing data to find meaningful insights, use familiar SQL, and take advantage of our pay-as-you-go model.


As mentioned, our data is a set of records regarding meteors that have fallen to earth. Our file is in JSON format as an array of objects. The source file can be found under the /data folder. Ex:

```json
[{"name": "Aachen", "id": "1", "nametype": "Valid", "recclass": "L5", "mass": "21", "fall": "Fell", "year": "1880-01-01T00:00:00.000", "reclat": "50.775000", "reclong": "6.083330", "geolocation": {"type": "Point", "coordinates": [6.08333,50.775]}}, ...]
```
#### Cloud Storage

Click on the hamburger icon to expand the products menu. Under STORAGE we'll find the Storage product. Below is the Storage browser where we can create a new bucket for the file we'll upload. 

![GCP Storage Browser](documents/gcp%20ss/GCP%20Storage%20Browser%20SS.png)

1. Click CREATE BUCKET
2. Provide a name for your new bucket
3. Choose where you want to Store your data (Multi-region by defualt)
4. Choose storage class (Standard by defualt)
5. Choose control access for objects
