# CIS 400 ML project
# libraries
import pandas
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


names = ['County', 'Anti-Transgender', 'Anti-Black', 'Anti-Asian']
with open("hateCrime2018.csv", 'r') as csvfile:
	dataset = pandas.read_csv(csvfile, names=names)

#Preprocessing
Y = dataset.iloc[1:, 0].values # NY counties
X = dataset.iloc[1:, [1,2,3]].values # anti-(asian, black, transgender)

print("Printing Counties: ",Y)
print("Printing the discrimination: ", X)

#Train Test Split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.85)

#knn
knn_clf = KNeighborsClassifier(n_neighbors=30)
knn_clf = knn_clf.fit(X,Y)
knn_prediction = knn_clf.predict(X_test)
print(knn_prediction)

#random forest
rfc_clf = RandomForestClassifier()
rfc_clf.fit(X,Y)
rfc_prediction = rfc_clf.predict(X_test)
print(rfc_prediction)

# logistic regression
l_clf = LogisticRegression()
l_clf.fit(X,Y)
l_prediction = l_clf.predict(X_test)
print(l_prediction)


print('\n -----')
print('Accuracy Scores:')
knn_acc = accuracy_score(knn_prediction,Y_test)
print('K-Nearest Neighbors (10): ' + str(knn_acc))

rfc_acc = accuracy_score(rfc_prediction,Y_test)
print('Random Forest: ' + str(rfc_acc))

l_acc = accuracy_score(l_prediction,Y_test)
print('Logistic Regression: ' + str(l_acc))
print('-----------------\n')

classifiers = ['K Nearest Neighbors', 'Random Forest', 'Logistic Regression']
accuracy = np.array([knn_acc, rfc_acc, l_acc])
max_acc = np.argmax(accuracy)
print(classifiers[max_acc] + ' is the most accurate classifier for this dataset')
