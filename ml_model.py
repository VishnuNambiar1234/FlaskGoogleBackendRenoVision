# 'gs://important_data_renovision/property_conditions.csv',
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Set the path to your CSV file stored in Google Cloud Storage
csv_file_path = 'gs://important_data_renovision/property_conditions.csv'

# Load the CSV data into a TensorFlow Dataset
def get_dataset(file_path, label_name, batch_size=32):
    dataset = tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size=batch_size,
        label_name=label_name,
        na_value="?",
        num_epochs=1,
        ignore_errors=True
    )
    return dataset

# Use the utility function to create the dataset
train_dataset = get_dataset(csv_file_path, label_name='RATING')

# Define the neural network model
model = Sequential([
    Dense(64, activation='relu', input_shape=[len(train_dataset.element_spec[0].keys())]),
    Dense(64, activation='relu'),
    Dense(1)
])

# Compile the model with the Adam optimizer and mean squared error loss function
model.compile(optimizer=Adam(), loss='mean_squared_error')

# Train the model
model.fit(train_dataset, epochs=10)

# Save the trained model to Google Cloud Storage
model_save_path = 'gs://important_data_renovision/saved_model'
model.save(model_save_path)
