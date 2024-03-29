# Lint as: python3
# coding=utf-8
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
# Edited by Noé Chauveau and Romain Monier for the PIR-IDS project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Prepare data for further process.

Read data from "/train/wallet", "/train/negative" and save them
in "/output/data/complete_data" in python dict format.

It will generate a new file with the following structure:
├── output/data
│   └── complete_data
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from data_rotation import create_file_for_rotation
from data_rotation import data_in_list

import argparse
from data_norm import data_norm
from data_norm import data_in_list

import csv
import json
import os
import random

LABEL_NAME = "gesture"
DATA_NAME = "accel_ms2_xyz"
folders = ["wallet"]
nb_negative = 8
nb_positive = 7

nb_negative_norm = 2
nb_positive_norm = 7

taille_data = 96


def prepare_original_data(folder, name, data, file_to_read, squaresum = 0):  # pylint: disable=redefined-outer-name
    """Read collected data from files."""
    if folder != "negative":
        with open(file_to_read, "r") as f:
            lines = csv.reader(f)
            data_new = {}
            data_new[LABEL_NAME] = folder
            data_new[DATA_NAME] = []
            data_new["name"] = name
            for idx, line in enumerate(lines):
                if squaresum :
                    if len(line) == 2:
                        if line[0] == "-" and data_new[DATA_NAME]:  ## not sure about the  and line[0] == "-" condition
                            data.append(data_new)
                            data_new = {}
                            data_new[LABEL_NAME] = folder
                            data_new[DATA_NAME] = []
                            data_new["name"] = name
                        elif line[0] != "-":
                            data_new[DATA_NAME].append([float(i) for i in line[0:2]])
                else :
                    if len(line) == 3:
                        if line[2] == "-" and line[0] == "-" and data_new[DATA_NAME]: 
                            data.append(data_new)
                            data_new = {}
                            data_new[LABEL_NAME] = folder
                            data_new[DATA_NAME] = []
                            data_new["name"] = name
                        elif line[2] != "-":
                            data_new[DATA_NAME].append([float(i) for i in line[0:3]])  # pylint: disable=unused-variable,redefined-outer-name
            data.append(data_new)
    else:
        with open(file_to_read, "r") as f:
            lines = csv.reader(f)
            data_new = {}
            data_new[LABEL_NAME] = folder
            data_new[DATA_NAME] = []
            data_new["name"] = name
            for idx, line in enumerate(lines):
                if squaresum :
                    if len(line) == 2 and line[0] != "-":
                        if len(data_new[DATA_NAME]) == taille_data:
                            data.append(data_new)
                            data_new = {}
                            data_new[LABEL_NAME] = folder
                            data_new[DATA_NAME] = []
                            data_new["name"] = name
                        else:
                            data_new[DATA_NAME].append([float(i) for i in line[0:2]])
                else:
                    if len(line) == 3 and line[2] != "-":
                        if len(data_new[DATA_NAME]) == taille_data:
                            data.append(data_new)
                            data_new = {}
                            data_new[LABEL_NAME] = folder
                            data_new[DATA_NAME] = []
                            data_new["name"] = name
                        else:
                            data_new[DATA_NAME].append([float(i) for i in line[0:3]])
            data.append(data_new)


def generate_negative_data(data):  # pylint: disable=redefined-outer-name
    """Generate 3 more sets of negative data"""
    # Big movement -> around straight line
    for i in range(100):
        if i > 80:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+3}"}
        elif i > 60:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+2}"}
        else:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+1}"}
        start_x = (random.random() - 0.5) * 2000
        start_y = (random.random() - 0.5) * 2000
        start_z = (random.random() - 0.5) * 2000
        x_increase = (random.random() - 0.5) * 10
        y_increase = (random.random() - 0.5) * 10
        z_increase = (random.random() - 0.5) * 10
        for j in range(taille_data):
            dic[DATA_NAME].append([
                start_x + j * x_increase + (random.random() - 0.5) * 6,
                start_y + j * y_increase + (random.random() - 0.5) * 6,
                start_z + j * z_increase + (random.random() - 0.5) * 6
            ])
        data.append(dic)
    # Random
    for i in range(100):
        if i > 80:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+3}"}
        elif i > 60:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+2}"}
        else:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+1}"}
        for j in range(taille_data):
            dic[DATA_NAME].append([(random.random() - 0.5) * 1000,
                                   (random.random() - 0.5) * 1000,
                                   (random.random() - 0.5) * 1000])
        data.append(dic)
    # Stay still
    for i in range(100):
        if i > 80:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+3}"}
        elif i > 60:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+2}"}
        else:
            dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": f"negative{nb_negative+1}"}
        start_x = (random.random() - 0.5) * 2000
        start_y = (random.random() - 0.5) * 2000
        start_z = (random.random() - 0.5) * 2000
        for j in range(taille_data):
            dic[DATA_NAME].append([
                start_x + (random.random() - 0.5) * 40,
                start_y + (random.random() - 0.5) * 40,
                start_z + (random.random() - 0.5) * 40
            ])
        data.append(dic)


# Write data to file
def write_data(data_to_write, path):
    with open(path, "w") as f:
        for idx, item in enumerate(data_to_write):  # pylint: disable=unused-variable,redefined-outer-name
            dic = json.dumps(item, ensure_ascii=False)
            f.write(dic)
            f.write("\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode")
    args = parser.parse_args()
    if args.mode == "norm":
        for i in range(nb_positive_norm):
            data_norm("output/custom_train/wallet", data_in_list("train/wallet", f"output_wallet_gyroscope_test{i+1}.txt"),f"custom_output_wallet_norm_test{i+1}.txt" )
    else :
        for i in range(nb_positive):
            create_file_for_rotation("output/custom_train/wallet", data_in_list("train/wallet", f"output_wallet_gyroscope_test{i+1}.txt"),f"custom_output_wallet_test{i+1}.txt" )

    if args.mode == "norm":
        for i in range(nb_negative_norm):
            data_norm("output/custom_train/negative", data_in_list("train/negative", f"output_negative_gyroscope_test{i+1}.txt"), f"custom_output_negative_norm_{i+1}.txt")
    else:
        for i in range(nb_negative):
            create_file_for_rotation("output/custom_train/negative", data_in_list("train/negative", f"output_negative_gyroscope_test{i+1}.txt"), f"custom_output_negative_{i+1}.txt")
    
    data = []  # pylint: disable=redefined-outer-name

    for idx1, folder in enumerate(folders):
        if args.mode == "norm":
            for idx2 in range(nb_positive_norm):
                prepare_original_data(folder, "test%d" % (idx2 + 1), data, "./output/custom_train/%s/custom_output_%s_norm_test%d.txt" % (folder, folder, idx2 + 1), 1)
        else :
            for idx2 in range(nb_positive):
                prepare_original_data(folder, "test%d" % (idx2 + 1), data, "./output/custom_train/%s/custom_output_%s_test%d.txt" % (folder, folder, idx2 + 1))
    if args.mode == "norm":
        for idx in range(nb_negative_norm):
            prepare_original_data("negative", "negative%d" % (idx + 1), data,
                            "./output/custom_train/negative/custom_output_negative_norm_%d.txt" % (idx + 1),1)
    else:
        for idx in range(nb_negative):
            prepare_original_data("negative", "negative%d" % (idx + 1), data,
                            "./output/custom_train/negative/custom_output_negative_%d.txt" % (idx + 1))
                                
    if args.mode != "norm":
        generate_negative_data(data)
    print("data_length: " + str(len(data)))
    if not os.path.exists("./output/data"):
        os.makedirs("./output/data")
    write_data(data, "./output/data/complete_data")
