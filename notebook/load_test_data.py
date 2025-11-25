# Load Test/Validation Data
test_ds = tf.keras.utils.image_dataset_from_directory(
    directory=f'{DATA_DIR}Validation',
    labels='inferred',
    label_mode='categorical',
    image_size=(IMG_SIZE, IMG_SIZE),
    interpolation='nearest',
    batch_size=BATCH_SIZE,
    shuffle=False,  # Don't shuffle test data
    seed=SEED
)