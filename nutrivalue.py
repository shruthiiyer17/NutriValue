import cv2
import numpy as np
import requests
import io
import json
from sklearn.neighbors import KNeighborsClassifier

#Analysing risk of heart disease
train = np.loadtxt("/heart_disease_train_dataset.csv", delimiter=',', skiprows=1)

X_train, y_train = train[:, :-1], train[:, -1]

mean = np.mean(X_train, axis = 0, keepdims=True)
std = np.std(X_train, axis = 0, keepdims=True, ddof=1)
new_X_train = (X_train-mean)/(std)

model = KNeighborsClassifier(n_neighbors = 9)
model.fit(new_X_train, y_train)

# This data is gathered from the company's health database when the user inputs their name
# [age, gender, chest_pain_type, resting_BP, serum_cholestrol,
# diabetes, resting_ecg_abnormality, max_HR, exercise_induced_angina,
# exercise_induced_ST_depression, ST_slop_type, no. of major blood vessels blockages,
# myocardial_defect_type]
data_point = [34, 1, 0, 125, 198, 0, 0, 124, 1, 16, 0, 0, 1]

new_data_point = (data_point-mean)/(std)

y_pred = model.predict(new_data_point)

#if y_pred = 0, no heart disease, if y_pred=1, heart disease = True

heart_disease = int(y_pred[0])

newSodium=0
newChol=0
newTransfat=0
newTotalfat=0
newProtein=0
newTotalsugar=0

#User inputs image of the nutritional label (i.e foodlabel.jpg in this case)
img = cv2.imread("foodlabel.jpg")

#OCR (Using API)
#Reads the label and determines suitability of food
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", img, [1, 90])
file_bytes = io.BytesIO(compressedimage)

result = requests.post(url_api, 
              files={"foodlabel.jpg": file_bytes},
              data={"apikey": "23b69b24fb88957"})

result = result.content.decode()
result = json.loads(result)

text_detected = result.get("ParsedResults")[0].get("ParsedText")

file = open('nutrition.txt', 'w')
file.writelines(text_detected)
file.close()


file = open('nutrition.txt', 'r')
for line in file:
    data = line.split()
    if data[0] =='Sodium':
        Sodium = data[1]
        Sodium = Sodium[:-2]
        Sodium = float(Sodium)
    elif data[0] =='Protein':
        Protein = data[1]
        Protein = Protein[:-1]
        Protein = float(Protein)
    elif data[0] =='Cholesterol':
        Cholesterol = data[1]
        Cholesterol = Cholesterol[:-2]
        Cholesterol = float(Cholesterol)
    elif data[0] =='Trans':
        TransFat = data[2]
        TransFat = TransFat[:-1]
        TransFat = float(TransFat)
    elif data[0] =='Total' and data[1] =='Fat':
        TotalFat = data[2]
        TotalFat = TotalFat[:-1]
        TotalFat = float(TotalFat)
    elif data[0] =='Sugars':
        Sugar = data[1]
        Sugar = Sugar[:-1]
        Sugar = float(Sugar)
file.close()

cv2.waitKey(0)
cv2.destroyAllWindows()

if heart_disease == 1:
  if Sodium >=1500:
    print("Sodium level unsuitable for consumption !")
  elif Sodium >1000:
    newSodium= 1500-Sodium
    print("You can consume an additional "+str(newSodium)+"mg of Sodium today")
  elif Cholesterol>200:
    print("Cholesterol level unsuitable for consumption !")
  elif Cholesterol>=100 and Cholesterol<=200:
    newChol= 200-Cholesterol
    print("You can consume an additional "+str(newChol)+"mg of Cholesterol today")
  elif TransFat!=0:
    print("Trans Fat level unsuitable for consumption !")
  elif TotalFat>90:
    print("unsuitable for consumption !")
  elif TotalFat>=70 and TotalFat<=90:
    newTotalfat= 90 - TotalFat
    print("You can consume an additional "+str(newTotalfat)+"g of Total Fat today")
  elif Protein>56:
    print("Protein level unsuitable for consumption !")
  elif Protein>40 and Protein<=56:
    newProtein= 56 - Protein
    print("You can consume an additional "+str(newProtein)+"g of Protein today")
  elif Sugar>30:
    print("Sugar level unsuitable for consumption !")
  elif Sugar>=20 and Sugar<=30:
    newTotalsugar= 30 - Sugar
    print("You can consume an additional "+str(newTotalsugar)+"g of sugar today")
  else:
    print("It is safe for consumption!")

else:
  print("It is safe for consumption!")
