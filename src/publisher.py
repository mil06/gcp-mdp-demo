import argparse
import json

from flask import Flask, request
from google.cloud import pubsub_v1

app = Flask(__name__)

#Publishes a message to a Pub/Sub topic.
@app.route('/publish/<project_id>/<topic_name>', methods = ['POST'])
def publish_message(project_id, topic_name):

    print("LOG - INFO: " + "project_id: " + project_id + " topic_name: " + topic_name);
    print("LOG - INFO: " + "json payload: " + str(json.dumps(request.json)));
    data = str(json.dumps(request.json));

    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    # When you publish a message, the client returns a future.
    data = data.encode('utf-8');
    print(data);
    future = publisher.publish(topic_path, data=data)
    print(future.result())

    print('Published messages')
    return "Message Published";

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)



# SAMPLE JSON
# datatemp = u'{"name": "JULIE","id": "00000","nametype": "JULIE","recclass": "JULIE","masskg": "00000","fall": "JULIE","timestamp": "1881-01-01T00:00:00","date": "01","month": "-1","year": "1881-01-01T00:00:00","reclat": "23.24","reclong": "104.67"}';