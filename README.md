## Overview

This demo is intended to introduce a set of GCP products used to build modern data pipelines. Specifically, we will focus on processes related to ingestion (streaming & batch), data manipulation, and end user interactions (reporting). The personas in this lifecycle can be associated to thier coresponding products of interest. 

Personas to Products:
- Business Report User - Data Studio
- Analyst / Data Engineer - Data Prep, Pub Sub, Dataflow
- Data Scientest - Datalab
- Developer - Cloud SDK

For this architecture, we've leveraged a publicly available data set from NASA which has recorded the meteors that have fallen to earth.

## Architecture
![GCP MDP Arch](/documents/gcp-mdp-arch-diagram.png)

## Getting Started (5 mins)

Navigate to the GCP console (https://console.cloud.google.com). You'll need a google account with billing enabled to continue building out your MDP. First time GCP users may have free credits.

![GCP Console SS](documents/gcp%20ss/GCP%20Console%20SS.png)

Let's create a new project. We can click on the projects tab towards the top left (Circled above in green). Here we'll see a pop up menu with a list of our projects and the option to create a new project. Click NEW PROJECT on the top right. 

![GCP Projects](documents/gcp%20ss/GCP%20Projects%20Menu%20SS.png)

Provide a name for your project and click CREATE.

![GCP New Project](documents/gcp%20ss/GCP%20New%20Proj%20SS.png)

## Batch Process (30 mins)

For the batch process we'll be using a combination of Cloud Storage, Dataprep, Dataflow, and BigQuery. We'll start by uploading our raw JSON file to Cloud Storage. Dataprep will then be able to connect to our JSON file to apply any data transformations and send the output to BigQuery. Dataflow helps to orchestrate this process and provide the requried resources. 

#### Quick Product Overview (as per GCP documentation)

Cloud Storage - Cloud Storage allows world-wide storage and retrieval of any amount of data at any time. You can use Cloud Storage for a range of scenarios including serving website content, storing data for archival and disaster recovery, or distributing large data objects to users via direct download.

Dataprep - Use Cloud Dataprep to explore and transform raw data from disparate and/or large datasets into clean and structured data for further analysis and processing.

Dataflow - Cloud Dataflow is a managed service for executing a wide variety of data processing patterns. The documentation on this site shows you how to deploy your batch and streaming data processing pipelines using Cloud Dataflow, including directions for using service features.

BigQuery - BigQuery is Google's fully managed, petabyte scale, low cost analytics data warehouse. BigQuery is NoOps—there is no infrastructure to manage and you don't need a database administrator—so you can focus on analyzing data to find meaningful insights, use familiar SQL, and take advantage of our pay-as-you-go model.


As mentioned, our data is a set of records regarding meteors that have fallen to earth. Our file is in JSON format as an array of objects. A sample object from the list can be seen below. The source file can be found under the /data folder. Ex:

```json
[{"name": "Aachen", "id": "1", "nametype": "Valid", "recclass": "L5", "mass": "21", "fall": "Fell", "year": "1880-01-01T00:00:00.000", "reclat": "50.775000", "reclong": "6.083330", "geolocation": {"type": "Point", "coordinates": [6.08333,50.775]}}, ...]
```
#### Cloud Storage

Click on the hamburger icon to expand the products menu (Top left of screen). Under STORAGE we'll find the Storage product. Below is the Storage browser where we can create a new bucket for the file we'll upload. 

![GCP Storage Browser](documents/gcp%20ss/GCP%20Storage%20Browser%20SS.png)

1. Click CREATE BUCKET
2. Provide a name for your new bucket
3. Choose where you want to Store your data (Multi-region by defualt)
4. Choose storage class (Standard by defualt)
5. Choose control access for objects
6. Click CREATE

![GCP Storage Create A](documents/gcp%20ss/GCP%20Storage%20Create%20A%20SS.png)

![GCP Storage Create B](documents/gcp%20ss/GCP%20Storage%20Create%20B%20SS.png)

If we navigagte back to the Storage browser, we can see the newly created bucket. (Circled above in green). Lets go into our bucket and create a folder to place our JSON file. Use the create folder button (Circled below in green). Give your folder a name and you'll see it be created (Circled in green (data-prep)). Upload the JSON file, meteorsonearth.json, from the /data folder. You can now see the uploaded file in the dataprep folder (Circled in green second image below). Now that we have completed the steps required in Cloud Storage, we can continue to Dataprep

![GCP Storage Bucket](documents/gcp%20ss/GCP%20Storage%20Bucket%20SS.png)

![GCP Storage Upload](documents/gcp%20ss/GCP%20Storage%20Upload%20SS.png)

#### Dataprep

Lets navigate to the dataprep console by once again using the hamburger icon on the top left. We can find Dataprep under BIG DATA. We can create a new flow by clicking the Create Flow button (Circled in green below). Once we've given our flow a name and description we'll see it populated under the list of all flows (dataprep-sc-demo). If we click into our flow, we'll see a blank flow with an option to add a data set. Let's click Add Datasets and then Import Data in the pop up menu. This will allow us to select our JSON file from GCS which we uploaded earlier. 

![GCP Dataprep Console](documents/gcp%20ss/GCP%20Dataprep%20Browser%20SS.png)

![GCP Dataprep Create](documents/gcp%20ss/GCP%20Dataprep%20Create%20Flow%20SS.png)

Below, we can see the options to import data. GCS, BigQuery, and Upload. Our JSON file is in the GCS bucket path storage-sc-demo/dataprep/meteorsonearth.json which you can see we've navigated to in the image below. To have more control over the way Dataprep ingests your file, click Edit settings (Circled in green below). In the pop menu (2nd image below), you'll see an option to Detect structure. We'll want to deselect and save. Now we can click the Import & Add to Flow button (As circled in green in the 1st image below)

![GCP Dataprep Import](documents/gcp%20ss/GCP%20Dataprep%20Import%20SS.png)

![GCP Dataprep Import Edit](documents/gcp%20ss/GCP%20Dataprep%20Import%20Edit%20SS.png)

This brings us back to our updated flow. We can see our file is imported below as a step (Circled in green). If we hover over this step, we'll see three dots that open up a menu (as seen in the image below). Our next step will be to add a recipie which will be responsible for cleaning up the data so it can be translated to a row column format.

![GCP Dataprep Flow](documents/gcp%20ss/GCP%20Dataprep%20Updated%20Flow%20SS.png)

NEW TEXT

![GCP Dataprep Updated Flow B](documents/gcp%20ss/GCP%20Dataprep%20Updated%20Flow%20B%20SS.png)

![GCP Dataprep recipe AA SS](documents/gcp%20ss/GCP%20Dataprep%20recipe%20AA%20SS.png)

![GCP Dataprep recipe AB SS](documents/gcp%20ss/GCP%20Dataprep%20recipe%20AB%20SS.png)

![GCP Dataprep Updated Flow C SS](documents/gcp%20ss/GCP%20Dataprep%20%20Update%20Flow%20C%20SS.png)

![GCP Dataprep recipe BA SS](documents/gcp%20ss/GCP%20Dataprep%20recipe%20BA%20SS.png)
