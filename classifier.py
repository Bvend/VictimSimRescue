import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.tree import export_text
from sklearn.metrics import ConfusionMatrixDisplay


class Classifier:
    def __init__(self, train_data_file):
        """
        @param train_data_file: the absolute path to the file with training data"""

        # Import data

        data_path = train_data_file
        col_names = ["i","s1","s2","s3","s4","s5","g","y"]
        use_cols = ["s3","s4","s5","y"]
        df = pd.read_csv(data_path, names=col_names, usecols=use_cols)
        x = df.drop("y", axis="columns").copy()
        y = df["y"].copy() - 1


        # Build decision trees

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
        clf = DecisionTreeClassifier(criterion="entropy")
        path = clf.cost_complexity_pruning_path(x_train, y_train)
        ccp_alphas = path.ccp_alphas
        ccp_alphas = ccp_alphas[:-1]

        clfs = []
        scores = []
        for ccp_alpha in ccp_alphas:
            clf = DecisionTreeClassifier(criterion="entropy", ccp_alpha=ccp_alpha)
            clf.fit(x_train, y_train)
            precision = cross_val_score(clf, x_train, y_train, cv=5, scoring="precision_weighted")
            recall = cross_val_score(clf, x_train, y_train, cv=5, scoring="recall_weighted")
            f_measure = cross_val_score(clf, x_train, y_train, cv=5, scoring="f1_weighted")
            accuracy = cross_val_score(clf, x_train, y_train, cv=5, scoring="accuracy")
            scores.append([np.mean(precision), np.mean(recall), np.mean(f_measure), np.mean(accuracy)])
            clfs.append(clf)


        # Print trees performance

        print("Decision tree pruning performance:")
        scores = pd.DataFrame(scores, columns=["precision","recall","f-measure","accuracy"])
        print(scores)


        # Choose the most accurate tree

        idx_best = 0
        for idx, ccp_alpha in enumerate(ccp_alphas):
            if scores.loc[idx].at["accuracy"] >= scores.loc[idx_best].at["accuracy"]:
                idx_best = idx

        print(f"Best tree: {idx_best}")

        clf_pruned = DecisionTreeClassifier(criterion="entropy", ccp_alpha=ccp_alphas[idx_best])
        clf_pruned = clf_pruned.fit(x_train, y_train)

        #plt.figure(figsize=(16,16))
        #plot_tree(clf_pruned)
        #plt.show()
        #r = export_text(clf_pruned, feature_names=["qPA","pulso","resp"])
        #print(r)
        #ConfusionMatrixDisplay.from_estimator(clf_pruned, x_test, y_test)
        self.dtr = clf_pruned

    def classify(self, qp, pf, rf):
        """
        @param qp: quality of pression (s3)
        @param pf: pulse frequency (s4)
        @param rf: respiratory frequency (s5)"""
        return self.dtr.predict([[qp, pf, rf]])[0] + 1
