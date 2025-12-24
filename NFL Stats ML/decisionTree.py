import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt


# Functions to import the dataset
def importdata(filename, features, target):
    if filename.endswith(".csv"):
        data = pd.read_csv(filename)
    else:
        data = pd.read_excel(filename)
    features = data.loc[:, features]
    # Displaying dataset information
    print("Dataset Length: ", len(data))
    print("Dataset Shape: ", data.shape)
    print("Dataset: ", data.head())

    return data, features, target

# Function to split the dataset into features and target variables
def splitdataset(data, target, features):

    # Separating the target variable
    target = data[target]
    print(type(target), target.shape)
    #features = features.to_frame()
    # Splitting the dataset into train and test
    features_train, features_test, target_train, target_test = train_test_split(
        features, target, test_size=0.3, random_state=100)

    return features_train, features_test, target_train, target_test

def train_using_gini(features_train, target_train):

    # Creating the classifier object
    clf_gini = DecisionTreeClassifier(criterion="gini",
                                      random_state=100, max_depth=3, min_samples_leaf=5)

    # Performing training
    clf_gini.fit(features_train, target_train)
    return clf_gini

def train_using_entropy(features_train, target_train):

    # Decision tree with entropy
    clf_entropy = DecisionTreeClassifier(
        criterion="entropy", random_state=100,
        max_depth=3, min_samples_leaf=5)

    # Performing training
    clf_entropy.fit(features_train, target_train)
    return clf_entropy

# Function to make predictions
def prediction(features_test, clf_object):
    target_pred = clf_object.predict(features_test)
    print("Predicted values:")
    print(target_pred)
    return target_pred

# Placeholder function for cal_accuracy
def cal_accuracy(target_test, target_pred):
    print("Confusion Matrix: ",
          confusion_matrix(target_test, target_pred))
    print("Accuracy : ",
          accuracy_score(target_test, target_pred)*100)
    print("Report : ",
          classification_report(target_test, target_pred))

from sklearn import tree
# Function to plot the decision tree
def plot_decision_tree(clf_object, feature_names, class_names):
    plt.figure(figsize=(25, 15))
    plot_tree(clf_object, filled=True, feature_names=feature_names, class_names=class_names, rounded=True)
    plt.show()

class main:
    if __name__ == "__main__":
        file = input("Enter file path: ")
        try:
            with open(file, "r") as f:
                file_path = f.readline()
                file_path = file_path.rstrip("\n")
                target = f.readline()
                target = target.replace("\n", "")
                features = f.readline().rstrip("\n").split(",")
                feature_names = features.copy()
                class_names = f.readline().split(",")
                print(target)
                print(features)
                data, features, target = importdata(file_path, features, target)
        except Exception as e:
            print(e)
        else:
            features_train, features_test, target_train, target_test = splitdataset(data, target, features)
            clf_gini = train_using_gini(features_train, target_train)
            print(clf_gini)
            print(type(clf_gini))
            # clf_entropy = train_using_entropy(features_train, target_train)
            target_pred = prediction(features_test, clf_gini)
            cal_accuracy(target_test, target_pred)
            # Visualizing the Decision Trees

            plot_decision_tree(clf_gini, feature_names, class_names)
        # plot_decision_tree(clf_entropy, ["Logged GDP per capita", "Social support", "Healthy life expectancy", "Freedom to make life choices", "Generosity", "Perceptions of corruption"], ['Low', 'Middle', 'High'])
        finally:
            print("Execution complete.")