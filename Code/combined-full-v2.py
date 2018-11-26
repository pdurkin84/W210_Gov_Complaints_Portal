from finetune import Classifier
import pandas
from sklearn.model_selection import train_test_split
import time
import re, string
from imblearn.over_sampling import RandomOverSampler

print("Import of packages done")

filePath = "/W210_Gov_Complaints_Portal/Datasets/combined_trainingdata_filtered_20181108.tsv"
data = pandas.read_csv(filePath,sep='\t')
print(data.shape)
print(data.loc[:5])
print("Loaded the data")

# get mapping from sub to main category
labelsMap = data[["CATEGORY_MAIN", "CATEGORY_SUB"]].drop_duplicates()
labelsMap = labelsMap.set_index("CATEGORY_SUB").to_dict()["CATEGORY_MAIN"]
print("Calculated Mapping from SUB to MAIN category")
print(labelsMap)

trainingData = data[["complaint", "CATEGORY_SUB"]]
del data
print(type(trainingData))
print(trainingData.shape)
print("Prepared training data")

# _, sampleX, _, sampleY = train_test_split(trainingData.complaint, trainingData.CATEGORY_SUB, test_size=0.1, random_state=42, stratify=trainingData.CATEGORY_SUB)
# del trainingData
# print(sampleY.shape)
print("No stratified sample.")

trainX, testX, trainY, testY = train_test_split(trainingData.complaint, trainingData.CATEGORY_SUB, test_size=0.2, random_state=42, stratify=trainingData.CATEGORY_SUB)
print(trainX.shape)
print("Split into train and test")

# ros = RandomOverSampler(sampling_strategy= "minority", random_state=42)
# trainX_res, trainY_res = ros.fit_resample(trainX.values.reshape(-1, 1), trainY)
# print(trainX_res.shape)
# print(trainY_res.shape)
print("No Oversampled training data minority")

# trainX_res_list = [sample[0] for sample in trainX_res.tolist()]
# trainY_res_list = trainY_res.tolist() #[sample[0] for sample in trainY_res.tolist()]
# print(trainX_res_list[0])
# print(trainY_res_list[0])
print("No Stupid array to list conversion done.")

print("Starting training")
start = time.time()
model = Classifier(max_length=512, 
                    val_interval=1000,  
                    n_epochs=3, 
                    l2_reg=0.0, 
                    lr=6.25E-05,
                    lm_loss_coef = 0.25,
#                     eval_acc = True, # doesn't work
#                     oversample = True, # oversamples too much, so I am doing it separately
                    params_device = 0,
                    autosave_path = "/W210_Gov_Complaints_Portal/models/",
                    verbose = True,
                  )
model.fit(trainX.tolist(), trainY.tolist())          # Finetune base model on custom data
duration = time.time()-start
print("Training Done")
print("It took :"+str(duration)+ " seconds")

model.save("/W210_Gov_Complaints_Portal/models/combined_model_full_no_oversample_20181123")                   # Serialize the model to disk
print("Model Saved")

print("Starting testing")
# model = Classifier.load("/W210_Gov_Complaints_Portal/models/combined_model_full_no_oversample_20181123")
print(testX.shape)
print(model)
start = time.time()
predictions = model.predict(testX.tolist())
duration = time.time() - start
print("Predictions done")
print("It took :"+str(duration)+ " seconds")

print("Evaluating accuracy")
mainPredictions = []
for pred in predictions:
    mainPredictions.append(labelsMap[pred])

mainTestY = []
for testLabel in testY.tolist():
    mainTestY.append(labelsMap[testLabel])
    
correctMain = 0
countMain = 0
for i, complaint in enumerate(testX.tolist()):
    correctMain += int(mainPredictions[i] == mainTestY[i])
    countMain +=1
print(correctMain)
print(countMain)
print("Accuracy on Main: "+str(correctMain*1.0/countMain))

correct = 0
count = 0
testYList = testY.tolist()
for i, complaint in enumerate(testX.tolist()):
    correct += int(predictions[i] == testYList[i])
    count +=1
print(correct)
print(count)
print("Accuracy on Sub: "+str(correct*1.0/count))