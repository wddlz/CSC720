from sklearn import preprocessing, metrics, cross_validation, svm
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import numpy
import glob

female_dir = 'C:\\Users\\wddlz\\Documents\\GitHub\\CSC720\\Files\\ResFemale\\'
male_dir = 'C:\\Users\\wddlz\\Documents\\GitHub\\CSC720\\Files\\ResMale\\'
read_files_f = glob.glob(female_dir + '*.txt')
read_files_m = glob.glob(male_dir + '*.txt')

with open('science.txt', 'w') as outfile:
    for f in read_files_f:
        with open(f, 'rb') as infile:
            outfile.write('-1,')
            outfile.write(infile.read())
            outfile.write('\n')
    for f in read_files_m:
        with open(f, 'rb') as infile:
            outfile.write('1,')
            outfile.write(infile.read())
            outfile.write('\n')

# iris = datasets.load_iris()
# digits = datasets.load_digits()

data_set = numpy.genfromtxt(
    'C:\\Users\\wddlz\\PycharmProjects\\AiGenderCode\\science.txt',
    delimiter=',')
x = data_set[:, 1:74]
y = data_set[:, 0]
X_train, X_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.4, random_state=0)

print ("\nCrossed\n")
X_train_processed = preprocessing.scale(X_train)
crossed = SVC().fit(X_train, y_train)
print ("\nCROSS VALIDATION")
print ("TRAIN SHAPE X, y")
print (str(X_train.shape) + ', ' + str(y_train.shape))
print ("TEST SHAPE X, y")
print (str(X_test.shape) + ', ' + str(y_test.shape))
print (crossed.score(X_test, y_test))

print ("\nCLF\n")
clf = SVC()
scores = cross_validation.cross_val_score(clf, x, y, cv=5)
print (scores)

normalized_x = preprocessing.normalize(x)
standardized_x = preprocessing.scale(x)
model_tree_classy = ExtraTreesClassifier()
model_tree_classy.fit(x, y)

model_logistic_regress = LogisticRegression()
rfe = RFE(model_logistic_regress, 5)
rfe = rfe.fit(x, y)
model_logistic_regress.fit(x, y)
print ("\nLogisticRegression")
print (model_logistic_regress)
expected = y
predicted = model_logistic_regress.predict(x)
print (metrics.classification_report(expected, predicted))
print (metrics.confusion_matrix(expected, predicted))

print ("\nNaiveBayes")
model_gauss = GaussianNB()
model_gauss.fit(x, y)
print (model_gauss)
expected_gauss = y
predicted_gauss = model_gauss.predict(x)
print (metrics.classification_report(expected_gauss, predicted_gauss))
print (metrics.confusion_matrix(expected_gauss, predicted_gauss))

print ("\nKNeighborsClassifier")
model_kn = KNeighborsClassifier()
model_kn.fit(x, y)
print (model_kn)
expected_kn = y
predicted_kn = model_kn.predict(x)
print (metrics.classification_report(expected_kn, predicted_kn))
print (metrics.confusion_matrix(expected_kn, predicted_kn))

print ("\nCART")
model_dtc = DecisionTreeClassifier()
model_dtc.fit(x, y)
print (model_dtc)
expected_dtc = y
predicted_dtc = model_dtc.predict(x)
print (metrics.classification_report(expected_dtc, predicted_dtc))
print (metrics.confusion_matrix(expected_dtc, predicted_dtc))

print ("\nSVM")
model_svc = SVC()
model_svc.fit(x, y)
print (model_svc)
expected_svc = y
predicted_svc = model_svc.predict(x)
print (metrics.classification_report(expected_svc, predicted_svc))
print (metrics.confusion_matrix(expected_svc, predicted_svc))

print ("\nOTHERS")
print ("\nDATA SET")
print (data_set)
print ("\nDATA")
print (x)
print ("\nNORMALIZED")
print (normalized_x)
print ("\nSTANDARDIZED")
print (standardized_x)
print ("\nTARGET")
print (y)
print ("\nDATA SET SHAPE")
print (data_set.shape)
print ("\nFEATURE IMPORTANCES")
print (model_tree_classy.feature_importances_)
print ("\nFEATURE SELECTION SUPPORT")
print (rfe.support_)
print ("\n FEATURE SELECTION RANKING")
print (rfe.ranking_)
# print (data_set.target.shape)
