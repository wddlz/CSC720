from sklearn import preprocessing, metrics, cross_validation, decomposition
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier  # , DecisionTreeRegressor
from sklearn.svm import SVC
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from matplotlib import pyplot as plt
import numpy
import glob
# import pylab as pl

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

data_set = numpy.genfromtxt(
    'C:\\Users\\wddlz\\PycharmProjects\\AiGenderCode\\science.txt',
    delimiter=',')

x = data_set[:, 1:74]
y = data_set[:, 0]
normalized_x = preprocessing.normalize(x)
standardized_x = preprocessing.scale(x)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.4, random_state=0)
X_train_processed = preprocessing.scale(X_train)


print ("\nCROSS VALIDATION")
crossed = SVC(kernel='poly', C=2)  # .fit(X_train_processed, y_train)
crossed_scores = cross_validation.cross_val_score(crossed, standardized_x, y, cv=10)
print (crossed_scores)
print("Accuracy: %0.2f (+/- %0.2f), MAX: %0.2f" % (crossed_scores.mean(), crossed_scores.std() * 2,
                                                   crossed_scores.max()))
print ("TRAIN SHAPE X, y")
print (str(X_train.shape) + ', ' + str(y_train.shape))
print ("TEST SHAPE X, y")
print (str(X_test.shape) + ', ' + str(y_test.shape))
# print (crossed.score(X_test, y_test))


print ("\nCLF")
clf = SVC(kernel='linear', C=2)
scores = cross_validation.cross_val_score(clf, standardized_x, y, cv=10)
print (scores)
print("Accuracy: %0.2f (+/- %0.2f), MAX: %0.2f" % (scores.mean(), scores.std() * 2, scores.max()))

model_tree_classy = ExtraTreesClassifier()
model_tree_classy.fit(x, y)

print ("\nREG")
reg = LogisticRegression()
scores = cross_validation.cross_val_score(reg, standardized_x, y, cv=10)
print (scores)
print("Accuracy: %0.2f (+/- %0.2f), MAX: %0.2f" % (scores.mean(), scores.std() * 2, scores.max()))


print ("\nLogisticRegression")
model_logistic_regress = LogisticRegression()
rfe = RFE(model_logistic_regress, 5)
rfe = rfe.fit(x, y)
model_logistic_regress.fit(X_train, y_train)
print (model_logistic_regress)
expected = y_test
predicted = model_logistic_regress.predict(X_test)
print (metrics.classification_report(expected, predicted))
print (metrics.confusion_matrix(expected, predicted))

# Graph
pca = decomposition.PCA(n_components=2)
# lda = LinearDiscriminantAnalysis(n_components=2)
# pca.fit(normalized_x)
# decomp_X = pca.transform(normalized_x)
# pl.scatter(decomp_X[:, 0], decomp_X[:, 1], c=y)
# pl.show()
X_r = pca.fit(normalized_x).transform(normalized_x)
h = .02
logreg = LogisticRegression(C=1e5)

# we create an instance of Neighbours Classifier and fit the data.
logreg.fit(X_r, y)

# Plot the decision boundary. For that, we will assign a color to each
# point in the mesh [x_min, m_max]x[y_min, y_max].
x_min, x_max = X_r[:, 0].min() - .5, X_r[:, 0].max() + .5
y_min, y_max = X_r[:, 1].min() - .5, X_r[:, 1].max() + .5
xx, yy = numpy.meshgrid(numpy.arange(x_min, x_max, h), numpy.arange(y_min, y_max, h))
Z = logreg.predict(numpy.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1, figsize=(4, 3))
plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

# Plot also the training points
plt.scatter(X_r[:, 0], X_r[:, 1], c=y, edgecolors='k', cmap=plt.cm.Paired)
plt.xlabel('X')
plt.ylabel('Y')

plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())

plt.show()

# X_l = lda.fit(x, y).transform(x)
# plt.figure()
# for c, i in zip("rb", [-1, 1]):
#     plt.scatter(X_r[y == i, -1], X_r[y == i, 1], c=c)
# plt.title('PCA')
#
# # plt.figure()
# # for c, i in zip("rb", [-1, 1]):
# #     plt.scatter(X_l[y == i, -1], X_l[y == i, 1], c=c)
# plt.show()

print ("\nNaiveBayes")
model_gauss = GaussianNB()
model_gauss.fit(X_train, y_train)
print (model_gauss)
expected_gauss = y_test
predicted_gauss = model_gauss.predict(X_test)
print (metrics.classification_report(expected_gauss, predicted_gauss))
print (metrics.confusion_matrix(expected_gauss, predicted_gauss))


print ("\nKNeighborsClassifier")
model_kn = KNeighborsClassifier()
model_kn.fit(X_train, y_train)
print (model_kn)
expected_kn = y_test
predicted_kn = model_kn.predict(X_test)
print (metrics.classification_report(expected_kn, predicted_kn))
print (metrics.confusion_matrix(expected_kn, predicted_kn))


print ("\nCART, Decision Tree Classifier")
model_dtc = DecisionTreeClassifier()
model_dtc.fit(X_train, y_train)
print (model_dtc)
expected_dtc = y_test
predicted_dtc = model_dtc.predict(X_test)
print (metrics.classification_report(expected_dtc, predicted_dtc))
print (metrics.confusion_matrix(expected_dtc, predicted_dtc))


print ("\nSVM")
model_svc = SVC()
model_svc.fit(X_train, y_train)
print (model_svc)
expected_svc = y_test
predicted_svc = model_svc.predict(X_test)
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
