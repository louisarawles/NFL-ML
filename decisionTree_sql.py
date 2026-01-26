import pandas as pd
import sqlite3
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

##### Function to get data #####
    # Params: database file, table name
    # Returns: data frame
def get_data(sqlite_file, table):
    conn = sqlite3.connect(sqlite_file)
    base_query = "SELECT * FROM "
    query = base_query + table
    df = pd.read_sql_query(query, conn)
    return df

##### Function to split data into features and target #####
    # Params: data frame, target column, and any additional excluded features
        # *excluded features passed as a list unless it's only one, then just pass as a string
    # Returns: features and target train and test datasets
def split_data(df,target_col,excluded_features=None):
    features = df.drop(columns=target_col)
    if excluded_features is not None:
        if type(excluded_features) is not list:
            features = features.drop(columns=excluded_features)
        else:
            for i in excluded_features:
                features = features.drop(columns=i)
    target = df[target_col]
    features_train, features_test, target_train, target_test = train_test_split(
        features, target, test_size=0.3, random_state=100)
    return features_train, features_test, target_train, target_test

##### Functions to train the classifier #####
    # Params: features and target training sets
    # Returns: trained classifier
def train_using_gini(features_train, target_train):
    # Gini classifier
    clf_gini = DecisionTreeClassifier(criterion="gini",
                                      random_state=100, max_depth=3, min_samples_leaf=5)
    # Performing training
    clf_gini.fit(features_train, target_train)
    return clf_gini

def train_using_entropy(features_train, target_train):
    # Entropy classifier
    clf_entropy = DecisionTreeClassifier(
        criterion="entropy", random_state=100,
        max_depth=3, min_samples_leaf=5)
    # Performing training
    clf_entropy.fit(features_train, target_train)
    return clf_entropy

##### Function to make predictions #####
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

##### Function to plot the decision tree #####
def plot_decision_tree(clf_object, features, target):
    feature_names = list(features.columns)
    class_names = [str(c) for c in clf_object.classes_]

    plt.figure(figsize=(18, 10))
    plot_tree(
        clf_object,
        filled=True,
        feature_names=feature_names,
        class_names=class_names,
        rounded=True
    )
    plt.show()

if __name__ == "__main__":
    sqlite_file = 'NFL_stats.sqlite'
    table = 'GameStats'
    df = get_data(sqlite_file,table)
    target = 'outcome'
    excl_features = ['gameStatId','gameId','teamAbbr']
    features_train, features_test, target_train, target_test = split_data(df,target,excluded_features=excl_features)
    clf_gini = train_using_gini(features_train, target_train)
    print(clf_gini)
    target_pred = prediction(features_test, clf_gini)
    cal_accuracy(target_test, target_pred)
    plot_decision_tree(clf_gini, features_test, target_test)



