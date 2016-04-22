from sklearn import datasets
import numpy
import glob

female_dir = 'C:\\Users\\wddlz\\Documents\\GitHub\\CSC720\\Files\\ResFemale\\'
male_dir = 'C:\\Users\\wddlz\\Documents\\GitHub\\CSC720\\Files\\ResMale\\'
read_files_f = glob.glob(female_dir + '*.txt')
read_files_m = glob.glob(male_dir + '*.txt')
with open('science.txt', 'w') as outfile:
    for f in read_files_f:
        with open(f, 'rb') as infile:
            outfile.write(infile.read())
            outfile.write('\n')
    for f in read_files_m:
        with open(f, 'rb') as infile:
            outfile.write(infile.read())
            outfile.write('\n')

iris = datasets.load_iris()
digits = datasets.load_digits()

data_set = numpy.genfromtxt(
    'C:\\Users\\wddlz\\PycharmProjects\\AiGenderCode\\science.txt',
    delimiter=',')
print (data_set)
