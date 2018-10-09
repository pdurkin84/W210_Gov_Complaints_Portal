from finetune import Classifier, config
import tensorflow as tf
import csv
import pandas
import numpy as np
from sklearn.model_selection import train_test_split
import sklearn
print('The scikit-learn version is {}.'.format(sklearn.__version__))

filePath = "Processing_eda/Bloomington_311_processed_3.csv"
data3 = pandas.read_csv(filePath)
print(data3.shape)
print(data3.loc[82480])

mask = (data3['description'].str.len() >=20) & (data3['description'].str.len() <=512)
dataFiltered = data3.loc[mask]
print(dataFiltered.shape)

dataFiltered.columns[dataFiltered.isna().any()].tolist()
# ourLabel doesn't have NaN values, so that is good. 

trainingData = dataFiltered[["description", "OurLabel"]]
print(type(trainingData))
print(trainingData.shape)
trainX, testX, trainY, testY = train_test_split(trainingData.description, trainingData.OurLabel, test_size=0.2, random_state=42)
# bigMask = (trainingData["description"].str.len() >=1000)
# print(trainingData.loc[bigMask].shape)
# Split in train and test 80/20
print(trainX.shape)
print(type(trainX))
print(trainY.shape)

model = Classifier(max_length=512, val_interval=3000, verbose = True)               # Load base model
model.fit(trainX, trainY)          # Finetune base model on custom data

model.save("newModel")                   # Serialize the model to disk
