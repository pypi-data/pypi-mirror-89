
import joblib
import traceback
import pandas as pd
import pkg_resources


def getGenderByNames(names):
    knnPath = pkg_resources.resource_stream(__name__, 'src/mlData/model.pkl')
    knn = joblib.load(knnPath)

    count_vectPath = pkg_resources.resource_stream(__name__, 'src/mlData/vectorizer.pickle')
    count_vect = joblib.load(count_vectPath)

    tfidf_transformerPath = pkg_resources.resource_stream(__name__, 'src/mlData/idf.pickle')
    tfidf_transformer = joblib.load(tfidf_transformerPath)

    if type(names) == str:
        return print("please enter a list only")
    outPutNames = []
    outPutGender = []
    print (names)
    for name in names:
        predicted = []
        docs_new = [name]
        # building up feature vector of our input
        X_new_counts = count_vect.transform(docs_new)
        # We call transform instead of fit_transform because it's already been fit
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        predicted = knn.predict(X_new_tfidf)
        outPutNames.append(name)
        outPutGender.append(predicted[0])

    return pd.DataFrame.from_dict({ "name": outPutNames, "gender":outPutGender })


if __name__ == "__main__":
    knn = joblib.load("../src/mlData/model.pkl") # Load "model.pkl"
    print ('Model loaded')

    count_vect = joblib.load("../src/mlData/vectorizer.pickle")
    print('Vector loaded')

    tfidf_transformer = joblib.load("../src/mlData/idf.pickle")
    print('idf loaded')


