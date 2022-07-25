from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import datetime
import os
from data_load import DataLoader

import numpy as np
import tensorflow as tf

SEQ_LENGTH = 96  #number of lines in the data files

logdir = "output/logs/scalars/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)


def reshape_function(data, label):
    reshaped_data = tf.reshape(data, [-1, 3, 1])
    return reshaped_data, label


def calculate_model_size(model):
    print(model.summary())
    var_sizes = [
        np.product(list(map(int, v.shape))) * v.dtype.size
        for v in model.trainable_variables
    ]
    print("Model size:", sum(var_sizes) / 1024, "KB")


def build_cnn(seq_length):
    """Builds a convolutional neural network in Keras."""
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(
            12,  # filters
            (4, 3), # convolution window size
            padding="same", 
            activation="relu",
            input_shape=(seq_length, 3, 1)),  # output_shape=(batch, 96, 3, 12)
        tf.keras.layers.MaxPool2D((3, 3)),  # (batch, 32, 1, 12)
        tf.keras.layers.Dropout(0.1),  # (batch, 32, 1, 12)
        tf.keras.layers.Conv2D(24, (4, 1), padding="same",
                               activation="relu"),  # (batch, 32, 1, 24)
        tf.keras.layers.MaxPool2D((3, 1), padding="same"),  # (batch, 10, 1, 24)
        tf.keras.layers.Dropout(0.1),  # (batch, 10, 1, 24)
        tf.keras.layers.Flatten(),  # (batch, 240)
        tf.keras.layers.Dense(16, activation="relu"),  # (batch, 16)
        tf.keras.layers.Dropout(0.1),  # (batch, 16)
        tf.keras.layers.Dense(4, activation="softmax")  # (batch, 4)
    ])
    model_path = os.path.join("./netmodels", "CNN")
    print("Built CNN.")
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    #model.load_weights("./netmodels/CNN/weights.h5")
    return model, model_path


def load_data(train_data_path, valid_data_path, test_data_path, seq_length):
    data_loader = DataLoader(train_data_path,
                             valid_data_path,
                             test_data_path,
                             seq_length=seq_length)
    data_loader.format()
    return data_loader.train_len, data_loader.train_data, data_loader.valid_len, \
           data_loader.valid_data, data_loader.test_len, data_loader.test_data


def build_net(args, seq_length):
    if args.model == "CNN":
        model, model_path = build_cnn(seq_length)
    else:
        print("Please input correct model name.(CNN)")
    return model, model_path


def train_net(
        model,
        model_path,  # pylint: disable=unused-argument
        train_len,  # pylint: disable=unused-argument
        train_data,
        valid_len,
        valid_data,  # pylint: disable=unused-argument
        test_len,
        test_data,
        kind):
    """Trains the model."""
    calculate_model_size(model)
    epochs = 50
    batch_size = 64
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    if kind == "CNN":
        train_data = train_data.map(reshape_function)
        test_data = test_data.map(reshape_function)
        valid_data = valid_data.map(reshape_function)
    test_labels = np.zeros(test_len)
    idx = 0
    for data, label in test_data:  # pylint: disable=unused-variable
        test_labels[idx] = label.numpy()
        idx += 1
    train_data = train_data.batch(batch_size).repeat()
    valid_data = valid_data.batch(batch_size)
    test_data = test_data.batch(batch_size)
    model.fit(train_data,
              epochs=epochs,
              validation_data=valid_data,
              steps_per_epoch=1000,
              validation_steps=int((valid_len - 1) / batch_size + 1),
              callbacks=[tensorboard_callback])
    loss, acc = model.evaluate(test_data)
    pred = np.argmax(model.predict(test_data), axis=1)
    confusion = tf.math.confusion_matrix(labels=tf.constant(test_labels),
                                         predictions=tf.constant(pred),
                                         num_classes=4)
    print(confusion)
    print("Loss {}, Accuracy {}".format(loss, acc))
    # Convert the model to the TensorFlow Lite format without quantization
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the model to disk
    open("output/model.tflite", "wb").write(tflite_model)

    # Convert the model to the TensorFlow Lite format with quantization
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    # Save the model to disk
    open("output/model_quantized.tflite", "wb").write(tflite_model)

    basic_model_size = os.path.getsize("output/model.tflite")
    print("Basic model is %d bytes" % basic_model_size)
    quantized_model_size = os.path.getsize("output/model_quantized.tflite")
    print("Quantized model is %d bytes" % quantized_model_size)
    difference = basic_model_size - quantized_model_size
    print("Difference is %d bytes" % difference)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m")
    args = parser.parse_args()

    seq_length = SEQ_LENGTH

    print("Start to load data...")

    train_len, train_data, valid_len, valid_data, test_len, test_data = \
        load_data("./output/data/train", "./output/data/valid", "./output/data/test", seq_length)

    print("Start to build net...")
    model, model_path = build_net(args, seq_length)

    print("Start training...")
    train_net(model, model_path, train_len, train_data, valid_len, valid_data,
              test_len, test_data, args.model)

    print("Training finished!")
