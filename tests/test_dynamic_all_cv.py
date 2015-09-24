import numpy as np
from sklearn import datasets
from sklearn.preprocessing import label_binarize, MultiLabelBinarizer, LabelEncoder
from NeuralNetDynamicOSI import DynamicOSI
from sklearn import cross_validation as cv
from sklearn.metrics import mean_squared_error, accuracy_score


def xval(clf, x, y, train_index, test_index):
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    clf.fit(x_train, y_train)
    y_pred = clf.predict_proba(x_test)
    if len(clf.classes_) > 2:
        mse = mean_squared_error(label_binarize(y_test, clf.classes_), y_pred)
    else:
        mlb = MultiLabelBinarizer()
        mse = mean_squared_error(mlb.fit_transform(label_binarize(y_test, clf.classes_)), y_pred)
    acc = accuracy_score(y_test, y_pred.argmax(axis=1))
    evals = clf.get_num_evals()
    return mse, acc, evals


def test_iris():
    f = open("../results/dynamic_iris_cv_results.txt", 'w')
    rng = np.random.RandomState()
    params = {'method': ['random', 'round-robin', 'iterative', 'worst-first'],
              'num_swarms': [2, 3, 5, 7, 10, 12, 15, 17, 20],
              'window': [5, 10, 15, 20, 25, 30],
              'num_particles': [5, 10, 15, 20]}

    iris = datasets.load_iris()

    for m in params['method']:
        for s in params['num_swarms']:
            for w in params['window']:
                for p in params['num_particles']:
                    # do a 5x2 cross val
                    sss = cv.StratifiedShuffleSplit(iris.target, n_iter=5, test_size=0.5, random_state=rng)
                    mses, accs, evals = [], [], []
                    for train_index, test_index in sss:
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[3], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            iris.data, iris.target, train_index, test_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[3], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            iris.data, iris.target, test_index, train_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                    print ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)]))
                    f.write("\n" + ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)])))
                    f.write("\n" + ",".join(map(str, mses)))
                    f.write("\n" + ",".join(map(str, accs)))
                    f.write("\n" + ",".join(map(str, evals)))
                    f.flush()
    f.close()


def test_ionosphere():
    f = open("../results/dynamic_ionosphere_cv_results.txt", 'w')
    rng = np.random.RandomState()
    params = {'method': ['random', 'round-robin', 'iterative', 'worst-first'],
              'num_swarms': [2, 3, 5, 7, 10, 12, 15, 17, 20],
              'window': [5, 10, 15, 20, 25, 30],
              'num_particles': [5, 10, 15, 20]}

    X = np.genfromtxt('../data/ionosphere.data', delimiter=',')[:, :-1]
    Y = np.genfromtxt('../data/ionosphere.data', delimiter=',', usecols=[-1], dtype='str')
    le = LabelEncoder()
    y = le.fit_transform(Y)

    for m in params['method']:
        for s in params['num_swarms']:
            for w in params['window']:
                for p in params['num_particles']:
                    # do a 5x2 cross val
                    sss = cv.StratifiedShuffleSplit(y, n_iter=5, test_size=0.5, random_state=rng)
                    mses, accs, evals = [], [], []
                    for train_index, test_index in sss:
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[5], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            X, y, train_index, test_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[5], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            X, y, test_index, train_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                    print ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)]))
                    f.write("\n" + ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)])))
                    f.write("\n" + ",".join(map(str, mses)))
                    f.write("\n" + ",".join(map(str, accs)))
                    f.write("\n" + ",".join(map(str, evals)))
                    f.flush()
    f.close()


def test_glass():
    f = open("../results/dynamic_glass_cv_results.txt", 'w')
    rng = np.random.RandomState()
    params = {'method': ['random', 'round-robin', 'iterative', 'worst-first'],
              'num_swarms': [2, 3, 5, 7, 10, 12, 15, 17, 20],
              'window': [5, 10, 15, 20, 25, 30],
              'num_particles': [5, 10, 15, 20]}

    X = np.genfromtxt('../data/glass.data', delimiter=',')[:, :-1]
    Y = np.genfromtxt('../data/glass.data', delimiter=',', usecols=[-1], dtype='str')
    le = LabelEncoder()
    y = le.fit_transform(Y)

    for m in params['method']:
        for s in params['num_swarms']:
            for w in params['window']:
                for p in params['num_particles']:
                    # do a 5x2 cross val
                    sss = cv.StratifiedShuffleSplit(y, n_iter=5, test_size=0.5, random_state=rng)
                    mses, accs, evals = [], [], []
                    for train_index, test_index in sss:
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[6], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            X, y, train_index, test_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[6], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            X, y, test_index, train_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                    print ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)]))
                    f.write("\n" + ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)])))
                    f.write("\n" + ",".join(map(str, mses)))
                    f.write("\n" + ",".join(map(str, accs)))
                    f.write("\n" + ",".join(map(str, evals)))
                    f.flush()
    f.close()


def test_4bit():
    f = open("../results/4bit_cv_results.txt", 'w')
    rng = np.random.RandomState()
    params = {'method': ['random', 'round-robin', 'iterative', 'worst-first'],
              'num_swarms': [2, 3, 5, 7, 10, 12, 15, 17, 20],
              'window': [5, 10, 15, 20, 25, 30],
              'num_particles': [5, 10, 15, 20]}

    X = np.genfromtxt('../data/4bit.data', delimiter=',')[:, :-1]
    y = np.genfromtxt('../data/4bit.data', delimiter=',', usecols=[-1])

    for m in params['method']:
        for s in params['num_swarms']:
            for w in params['window']:
                for p in params['num_particles']:
                    # do a 5x2 cross val
                    sss = cv.StratifiedShuffleSplit(y, n_iter=5, test_size=0.5, random_state=rng)
                    mses, accs, evals = [], [], []
                    for train_index, test_index in sss:
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[4, 3, 2], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            X, y, train_index, test_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                        mse, acc, ev = xval(
                            DynamicOSI(n_hidden=[4, 3, 2], num_dynamic_swarms=s, num_particles=p, window=w, random_state=rng,
                                       method=m, validation_size=0.33, verbose=False),
                            X, y, test_index, train_index)
                        mses.append(mse)
                        accs.append(acc)
                        evals.append(ev)
                    print ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)]))
                    f.write("\n" + ",".join(map(str, [m, s, w, p, np.mean(mses), np.mean(accs), np.mean(evals)])))
                    f.write("\n" + ",".join(map(str, mses)))
                    f.write("\n" + ",".join(map(str, accs)))
                    f.write("\n" + ",".join(map(str, evals)))
                    f.flush()
    f.close()


if __name__ == '__main__':
    test_iris()
    test_ionosphere()
    test_glass()
    test_4bit()
