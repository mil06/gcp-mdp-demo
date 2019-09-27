# Example GCP Modern Data Pipeline

## Overview

This demo is intended to introduce a set of GCP products used to build modern data pipelines. Specifically, we will focus on processes related to ingestion (streaming & batch), data manipulation, and end user interactions (reporting). The personas in this lifecycle can be associated to their corresponding products of interest. 

Personas to Products:
- Business Report User - Data Studio
- Analyst / Data Engineer - Data Prep, Pub Sub, Dataflow
- Data Scientist - Datalab
- Developer - Cloud SDK

For this architecture, we've leveraged a publicly available data set from NASA which has recorded the meteors that have fallen to earth.

## Architecture
![GCP MDP Arch](/documents/gcp-mdp-arch-diagram.png)

## Getting Started (5 mins)

Navigate to the GCP console (https://console.cloud.google.com). You'll need a google account with billing enabled to continue building out your pipeline. First time GCP users may have free credits.

![GCP Console SS](documents/gcp%20ss/GCP%20Console%20SS.png)

Let's create a new project. We can click on the projects tab towards the top left (circled above in green). Here we'll see a pop up menu with a list of our projects and the option to create a new project. Click NEW PROJECT on the top right. 

![GCP Projects](documents/gcp%20ss/GCP%20Projects%20Menu%20SS.png)

Provide a name for your project and click CREATE.

![GCP New Project](documents/gcp%20ss/GCP%20New%20Proj%20SS.png)

## Batch Process (30 mins)

For the batch process we'll be using a combination of Cloud Storage, Dataprep, Dataflow, and BigQuery. We'll start by uploading our raw JSON file to Cloud Storage. Dataprep will then be able to connect to our JSON file to apply any data transformations and send the output to BigQuery. Dataflow helps to orchestrate this process and provide the required resources. 

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

We can continue in our newly created GCP project by using Cloud Storage to upload our JSON file. Click on the hamburger icon to expand the products menu (Top left of screen. You'll see the same menu expanded in the screen shots above). Under STORAGE we'll find the Storage product. Below is the Storage browser where we can create a new bucket for the file we'll upload. 

![GCP Storage Browser](documents/gcp%20ss/GCP%20Storage%20Browser%20SS.png)

1. Click CREATE BUCKET (circled in green above)
2. Provide a name for your new bucket (shown in image below)
3. Choose where you want to Store your data (Multi-region by default)
4. Choose storage class (Standard by default)
5. Choose control access for objects
6. Click CREATE

If we navigate back to the Storage browser, we can see the newly created bucket. (circled above in green (storage-sc-demo)). 

![GCP Storage Create A](documents/gcp%20ss/GCP%20Storage%20Create%20A%20SS.png)

![GCP Storage Create B](documents/gcp%20ss/GCP%20Storage%20Create%20B%20SS.png)

Lets go into our bucket and create a folder to place our JSON file. Use the create folder button (circled below in green). Give your folder a name and you'll see it be created (circled in green (data-prep)). Upload the JSON file, meteorsonearth.json, from the /data folder. You can now see the uploaded file in the dataprep folder (circled in green second image below). Now that we have completed the steps required in Cloud Storage, we can continue to Dataprep

![GCP Storage Bucket](documents/gcp%20ss/GCP%20Storage%20Bucket%20SS.png)

![GCP Storage Upload](documents/gcp%20ss/GCP%20Storage%20Upload%20SS.png)

#### Dataprep

Lets navigate to the dataprep console by once again using the hamburger icon on the top left. We can find Dataprep under BIG DATA. We can create a new flow by clicking the Create Flow button (circled in green below). Once we've given our flow a name and description we'll see it populated under the list of all flows (dataprep-sc-demo).  

![GCP Dataprep Console](documents/gcp%20ss/GCP%20Dataprep%20Browser%20SS.png)

If we click into our flow, we'll see a blank flow with an option to add a data set. Let's click Add Datasets and then click Import Data in the pop up menu. This will allow us to select our JSON file from GCS which we uploaded earlier.

![GCP Dataprep Create](documents/gcp%20ss/GCP%20Dataprep%20Create%20Flow%20SS.png)

Below, we can see the options to import data. GCS, BigQuery, and Upload. Our JSON file is in the GCS bucket path storage-sc-demo/dataprep/meteorsonearth.json which you can see we've navigated to in the image below. To have more control over the way Dataprep ingests your file, click Edit settings (Circled in green below). In the pop menu (2nd image below), you'll see an option to Detect structure. We'll want to deselect and save. Now we can click the Import & Add to Flow button (As circled in green in the 1st image below)

![GCP Dataprep Import](documents/gcp%20ss/GCP%20Dataprep%20Import%20SS.png)

![GCP Dataprep Import Edit](documents/gcp%20ss/GCP%20Dataprep%20Import%20Edit%20SS.png)

This brings us back to our updated flow. We can see our file is imported below (circled in green). If we hover over this step, we'll see three dots that open up a menu (as seen in the image below). Our next step will be to add a recipe which will be responsible for cleaning up the data so it can be translated to a row column format.

![GCP Dataprep Flow](documents/gcp%20ss/GCP%20Dataprep%20Updated%20Flow%20SS.png)

You can see below the recipe that we've added to our flow. We can give the recipe a name (meteorsonearth clean data). If we click Edit Recipe (circled in green below), we can start to add the transformation steps to clean the data as intended. On the right, you can see a preview of the steps that we'll be adding to this recipe.

![GCP Dataprep Updated Flow B](documents/gcp%20ss/GCP%20Dataprep%20Updated%20Flow%20B%20SS.png)

As mentioned, our intent here is to break apart the JSON and get it into a row column format. Since we have data in JSON format, we can use a provided function to convert the key value pairs to column values. In order to do this, we'll need to have each row represent a single object with the proper syntax. On import you'll notice that the JSON data is represented as one row in one column. 

1. The first step should be "Split into rows". Applied on column1 and split on \n. This will get us closer to having one object per row. 
2. The second step should be "Replace text or patterns". Applied on column1 and find /^\[/. Since our JSON data is an array of objects, we need to strip the leading and trailing '[' & ']'. 
3. The thrid step does the same as above, but for the trailing bracket ']'. "Replace text or patterns" for column1 and find /\]$/.
4. The Fourth step removes the comma at the end of the object, as this was an array of objects. "Replace text or patterns" for column1 and find /^,/
5. Now that we have a proper JSON object for each row, for step 5 we can use the "Unnest Object elements" step. Applied on column1. For 'Path to elements' we can provide all the keys we wish to turn into columns. This will take all the objects in column1 and pick out the values for each key and create a new column for that key. 
6. Lastly we can add a step to delete column1, and we'll be left with a row column format for our data. 

![GCP Dataprep recipe AA SS](documents/gcp%20ss/GCP%20Dataprep%20recipe%20AA%20SS.png)

![GCP Dataprep recipe AB SS](documents/gcp%20ss/GCP%20Dataprep%20recipe%20AB%20SS.png)

Now that we have completed the transformations required in our first step to clean the data, we can continue to the next recipe which will have more of the business logic transformations. Coming back to the flow, we can add another recipe after the first and name it (meteorsonearth transform). Once again we'll click edit recipe to start adding the steps for this transformation. 

![GCP Dataprep Updated Flow C SS](documents/gcp%20ss/GCP%20Dataprep%20%20Update%20Flow%20C%20SS.png)

1. Add a new step and search for the "New Formula" function. The Formula Type will be Multiple Row Formula. The Formula will be MULTIPLY(mass, 2.205). Here we're using the Multiply function to convert the mass column, currently in lbs to kgs. 
2. Add a second step and use the delete column function to remove the original mass column as we will no longer need that. 
3. Add a thrid step to rename the year column to timestamp, as it contains a time stamp and not just the year. 
4. Add another step with the "New Formula" function. The Formula Type will be Multiple Row Formula. The Formula will be DATEFORMAT(timestamp, 'yyyy'). The idea behind this, and the next couple steps, is to extract the year, date and month to their own columns.
5. Here we do the same as above, but for the month. DATEFORMAT(timestamp, 'MM'). 
6. Once again, we do the same as above to extract the date. DATEFORMAT(timestamp, 'dd').


![GCP Dataprep recipe BA SS](documents/gcp%20ss/GCP%20Dataprep%20recipe%20BA%20SS.png)

Now that we have completed the steps in our transformations recipe, we can come back to our flow and set an output destination. To set an output destination we can click on the arrow that appears over the step on hover (circled in green below). We can edit the destination details by clicking the Edit button under the Destinations tab (circled in green). Also keep in mind the Run Job button, which we'll use after configuring the output destination.

![GCP Dataprep Set Output A SS](documents/gcp%20ss/GCP%20Dataprep%20Set%20Output%20A%20SS.png)

The edit browser can be seen below. By default the output will be sent to GCS in the form of a .csv. We can click Edit here to modify the destination (circled in green).

![GCP Dataprep Set Output B SS](documents/gcp%20ss/GCP%20Dataprep%20Set%20Output%20B%20SS.png)

Since we want to set our destination to BigQuery, we'll first need to create a Dataset in BigQuery. In another tab, we can navigate to BigQuery using the hamburger icon and you'll find BigQuery under BIG DATA. We can CREATE DATASET (circled in green below). I've named mine (nasa). 

![GCP BigQuery Create Dataset SS](documents/gcp%20ss/GCP%20BigQuery%20Create%20Dataset%20SS.png)

Now we can go back to our dataprep console where we left off, and select our newly created dataset under BigQuery. You'll see we have the option to create a table on the fly and append for following executions.

![GCP Dataprep Set Output C SS](documents/gcp%20ss/GCP%20Dataprep%20Set%20Output%20C%20SS.png)

We can update our flow (as seen above). This will bring us back to our flow where we can now run the job. Behind the scenes, this is executed as a Dataflow job. We can navigate to Dataflow using the hamburger icon and we'll find Dataflow under BIGDATA. To see the execution of our flow, we can click into the job id, and we'll see the live execution of our job broken down into different steps.

![GCP Dataflow Execution SS](documents/gcp%20ss/GCP%20Dataflow%20Execution%20SS.png)

## Streaming Process (30 mins)

For our streaming process we'll be using a combination of Pub/Sub, Dataflow, and BigQuery. In our Pub/Sub model, the subscriber will directly relay received records to BigQuery. So any publisher who sends a message to the given Topic will then have it be picked up by the subscriber (listening to the same topic) who will send that data over to BigQuery. 

#### Quick Product Overview (as per GCP Documentation)

PubSub - Cloud Pub/Sub is a fully-managed real-time messaging service that allows you to send and receive messages between independent applications.

For more context, Pub/Sub consists of publishers, subscribers, and Topics. Topics are the central messaging components that for any given topic pass along all messages to it's subscribers. Publishers can publish to one or more topic. Subscribers can subscribe to one or more topic. 

#### Pub/Sub

If we navigate to the Pub/Sub console under BIGDATA we can create our Topic and Subscription. Lets start with creating a Topic. You'll see the option to CREATE TOPIC (cicled in green below). Just provide a name (topic-sc-demo), and create.

![GCP PubSub Topics SS](documents/gcp%20ss/GCP%20PubSub%20Topics%20SS.png)

Now lets create a subscription. We can click on the subscriptions tab on the left hand side. Click on the CREATE SUBSCRIPTIONS option on the top and you'll be prompted to fill out the following. 

1. We can provide any name for our SubscriptionID, such as NasaMeteorsSubscription. 
2. Provide the name of the Topic we just created in the format expected. 
3. Keep the delivery type as Pull
4. Feel free to adjust the other parameters as required and create when done. 

![GCP PubSub Sub Create A SS](documents/gcp%20ss/GCP%20PubSub%20Sub%20Create%20A%20SS.png)

![GCP PubSub Sub Create B SS](documents/gcp%20ss/GCP%20PubSub%20Sub%20Create%20B%20SS.png)

#### Dataflow 

Dataflow has a template set up that will help send the messages received by our subscriber over to our BigQuery Table. Lets navigate to Dataflow so we can set that up. Once you're on the Dataflow console page, you can click CREATE JOB FROM TEMPLATE on the top of the screen as shown in the image below. This will take us the the page as seen on the second image below. 

1. Provide a Job name
2. We'll want to select the "Cloud Pub/Sub Subscription to BigQuery" template
3. We can select our desired regional endpoint
4. Let's provide the full path of our Subscription we just created
5. Lastly, provide the BigQuery Table we've been using
6. We can keep the encryption as a Google-managed key
7. Run Job.

Now that this job is active, any messages received by our Subscriber will be directly sent over to our BigQuery Table. 

![GCP Dataflow Console SS](documents/gcp%20ss/GCP%20Dataflow%20Console%20SS.png)

![GCP Dataflow Template Create SS](documents/gcp%20ss/GCP%20Dataflow%20Template%20Create%20SS.png)

#### Local Setup

To send messages to our Subscriber, we'll need a Publisher. I've set up a python web service that acts as a Publisher. Once we complete the local setup and activate the Publisher we can send messages via the Publisher to our Topic. 

Note: My local machine is a Mac so instructions may vary for other OSs. 

You'll want to get the latest version of Cloud SDK for your machine. These set of tools helps you manage resources and applications hosted on GCP.

1. Cloud SDK requires Python 2 with a release number of Python 2.7.9 or higher.
2. You can find the appropriate SDK for you from the following link: https://cloud.google.com/sdk/docs/
3. Extract the contents of the file to any location on your file system.
4. Open a Terminal and navigate to that location.
5. To include Cloud SDK to your path you can run the command: `./google-cloud-sdk/install.sh`
6. To initialize the SDK run the following command: `./google-cloud-sdk/bin/gcloud init`

![GCP Local SDK install SS](documents/gcp%20ss/GCP%20Local%20SDK%20Install%20SS.png)

![GCP Local SDK init SS](documents/gcp%20ss/GCP%20Local%20SDK%20init%20SS%20.png)

7. You'll be prompted to login. Select Y and continue to the browser to login. You'll also be asked to select a compute region and zone. Select any that satisfies your needs. 
8. Now that we have our SDK installed and configured. We can continue with our local set up. Lets create a virtualenv with the command: `virtualenv env`
9. We can enter our virtual environments by using the command: `source env/bin/activate`
10. We want to navigate to our directory where we have our publisher.py and requirements.txt files. (You can find them in the /src folder here in this github project)
11. We'll want to install some dependencies for our code. Run the command: `pip install -r requirements.txt`

![GCP Local Reqs install SS](documents/gcp%20ss/GCP%20Local%20Reqs%20SS.png)

12. We'll need to create a service account in order to run our python script. Navigate to https://cloud.google.com/docs/authentication/getting-started
13. Click on the "GO TO THE CREATE SERVICE ACCOUNT KEY PAGE" button
14. From the Service account list, select New service account
15. In the Service account name field, enter a name
16. From the Role list, select Project > Owner
17. Click Create.  A JSON file that contains your key downloads to your computer. 
18. Set your environment variable by using the command: `export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"`

![GCP Service Account Page SS](documents/gcp%20ss/GCP%20Service%20Account%20Page%20SS.png)

![GCP Service Account Create SS](documents/gcp%20ss/GCP%20Service%20Account%20Create%20SS.png)

19. Now we're ready to run our python web service. We can run the command `python publisher.py`

![GCP Local Python Run SS](documents/gcp%20ss/GCP%20Local%20Run%20Py%20SS.png)

20. We can see above our python web service has been successfully started. Now we can publish a message using Postman. For those who are new to Postman, Postman is a Rest client that helps make GET and POST calls. We can use this to make a POST call through our publisher web service.

We'll want to make sure the url is in the proper format `localhost:8080/publish/slalom-gcp-demo/topic-sc-demo`.
- /publish is our webservice name.
- slalom-gcp-demo is our GCP project name.
- topic-sc-demo is our Pub/Sub Topic name.

![GCP Local Postman Publish SS](documents/gcp%20ss/GCP%20Postman%20Publish%20SS.png)

We can check in Big Query to verify that our message has been added to the table. We can run the query `SELECT * FROM nasa.meteorsonearth WHERE name LIKE "Mega%";`

You'll see the record populated in the image below.

![GCP BigQuery Verfiy SS](documents/gcp%20ss/GCP%20BigQuery%20Pub%20Messg%20Check%20SS.png)
