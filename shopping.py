import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        def normalize(row):
            # convert to int: Month [10], VisitorType [15], Weekend [16]
            months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month = months.index(row[10])
            row[10] = month

            row[15] = 1 if row[15] == "Returning_Visitor" else 0

            row[16] = 1 if row[16] == "TRUE" else 0

            # convert to int: Administrative [0], Informational [2], ProductRelated [4], OperatingSystems [11], Browser [12], Region [13], TrafficType [14]
            for i in [0, 2, 4, 11, 12, 13, 14]:
                row[i] = int(row[i])

            # convert to float: Administrative_Duration [1], Informational_Duration [3], ProductRelated_Duration [5], BounceRates [6], ExitRates [7], PageValues [8], SpecialDay [9]
            for i in [1, 3, 5, 6, 7, 8, 9]:
                row[i] = float(row[i])

            return row

        data = []
        for row in reader:
            data.append({
                "evidence": normalize(row[:17]),
                "labels" : 1 if row[17] == "TRUE" else 0
            })
        
        evidence = [row["evidence"] for row in data]
        labels = [row["labels"] for row in data]

        return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity_true = 0
    sensitivity_all = 0
    specificity_true = 0
    specificity_all = 0
    for label, prediction in zip(labels, predictions):
        if label == 1:
            sensitivity_all += 1
            if label == prediction:
                sensitivity_true += 1
        else:
            specificity_all += 1
            if label == prediction:
                specificity_true += 1
    
    sensitivity = sensitivity_true / sensitivity_all
    specificity = specificity_true / specificity_all
    return sensitivity, specificity


if __name__ == "__main__":
    main()
