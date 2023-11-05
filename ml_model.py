from google.cloud import storage
import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Set the path to your Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/vishn/Desktop/FlaskGoogleBackend/glossy-fastness-404223-4f353d9f4ab3.json'

# Initialize the Google Cloud Storage client
gcs = storage.Client()

# Specify the name of your GCS bucket
bucket_name = 'important_data_renovision'

# Specify the name of the blob in your GCS bucket
blob_name = 'processed_property_conditions.csv'

# Specify the local path where you want to download the CSV file
local_file_path = 'new_processed_property_conditions.csv'

# Download the file from GCS
bucket = gcs.get_bucket(bucket_name)
blob = bucket.blob(blob_name)
blob.download_to_filename(local_file_path)


# Load the CSV data into a TensorFlow Dataset
raw_dataset = tf.data.experimental.make_csv_dataset(
    local_file_path,
    batch_size=32,
    label_name='RATING',
    na_value="?",
    num_epochs=1,
    ignore_errors=True,
    header=True
)

# This function will rename the columns by replacing spaces with underscores
def rename_columns(features, label):
    renamed_features = {header.replace(" ", "_"): value for header, value in features.items()}
    return renamed_features, label

# Apply the function to rename columns in the dataset
dataset = raw_dataset.map(rename_columns)

# Now you can define the feature columns using the renamed columns
feature_columns = [tf.feature_column.numeric_column(header) for header in next(iter(dataset))[0].keys()]

# Create a feature layer from the feature columns
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)


# Build, compile, and train the model
model = models.Sequential([
    feature_layer,
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Convert the dataset into a format that contains a dictionary with feature names mapping to tensor values
train_dataset = dataset.map(lambda features, label: (features, label))

# Train the model
model.fit(train_dataset, epochs=10)

# Save the trained model to a local file
model_save_path = 'saved_model.h5'
model.save(model_save_path)

# Upload the saved model to GCS
model_blob = bucket.blob('saved_model/saved_model.h5')
model_blob.upload_from_filename(model_save_path)