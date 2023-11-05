from google.cloud import storage
import tensorflow as tf
import os

# Set the path to your Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/vishn/Desktop/FlaskGoogleBackend/glossy-fastness-404223-4f353d9f4ab3.json'

# Initialize the Google Cloud Storage client
gcs_client = storage.Client()

# Specify the name of your GCS bucket and the path of the model file in the bucket
bucket_name = 'important_data_renovision'
model_file_path = 'saved_model/saved_model.h5'

# Create a bucket object
bucket = gcs_client.get_bucket(bucket_name)

# Create a blob object
blob = bucket.blob(model_file_path)

# Download the model file to a local file (temporarily)
local_model_path = 'saved_model.h5'
blob.download_to_filename(local_model_path)

# Load the model
model = tf.keras.models.load_model(local_model_path)

# Assuming you have new data to predict on in the form of a NumPy array or a TensorFlow tensor
# For example, let's say you have one sample with 5 features
new_data = [[1,1,1,1,1,1,1,1,1,1]]

# Convert the new data to a numpy array if it's not already
new_data = np.array(new_data)

# Use the model to make predictions
predictions = model.predict(new_data)

# Print out the predictions
print(predictions)


