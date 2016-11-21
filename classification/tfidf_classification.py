# coding: utf-8

# ------ IMPORTS -----
import warnings

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from loadAndCleanData import LoadCleanData
from processTextData import ProcessText

warnings.filterwarnings("ignore")

p = ProcessText()
l = LoadCleanData()


class Classification:

    def __init__(self):
        self

    @staticmethod
    def rf_pipeline_classif(df, params_grid, num_folds=3):
        """
        :param df: Raw DataFrame
        :param params_grid: Grid of parameters
        :param num_folds: Number of folds for CV
        :return: fitted model / results of CV
        """
        X_df = p.clean_text_data(df)['merge_final']
        y = df['cat_purchease']
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=0.005, ngram_range=(1, 2))
        rf = RandomForestClassifier(n_estimators=10, random_state=123)
        pipe = Pipeline([('tfidf', vectorizer), ('rf', rf)])
        model = GridSearchCV(pipe, param_grid=params_grid, n_jobs=1, cv=num_folds, verbose=1, refit=True)

        return model.fit(X_df, y), model.cv_results_


# Load all dataset
df = l.load_and_concat()
print "Size of df :", df.shape

params_grid = {'tfidf__min_df': [0, 0.0005, 0.001],
               'rf__min_samples_leaf': [1, 3, 5],
               }

(model, results) = Classification().rf_pipeline_classif(df, params_grid, num_folds=3)
print results
print model.predict(['pain maxi burger', 'HAR. VERT XF'])
