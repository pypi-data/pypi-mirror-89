import os
import sys

import numpy as np
import pandas as pd

import tqdm
import tensorflow_addons as tfa

import aibias.dataset as ds

from time import time

import tensorflow as tf
from tensorflow import keras
'''
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
'''
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


#======================================
#           PREJUDICE REMOVER
#======================================

class PR_remover():
    """
    Creates and trains a linear regression model that utilizes
    the 'Prejudice Remover' regularizer as is described in the paper

    'Fairness-aware Classifier with Prejudice Remover Regularizer'
    Toshihiro Kamishima et al. (2012)
    """

    def __init__(self,dataset,epochs=1,eta=5):
        """
        Arguments:
            dataset - (aibias.dataset.Dataset) Object containing the
                      dataset to be trained
            epochs  - (int) Number of epochs to train the model
                      Default: 1
            eta     - (float/int) Scalar for the PR regularizer
        """

        self.dataset = dataset
        self.epochs  = epochs
        self.eta     = eta
        self.num_samples = len(dataset.dataframe)
        self.num_f   = len(self.dataset.train_features)
        self.process_data()

    def process_data(self):
        """
        Processes the data from the Dataset object so that it
        is compatible with the training model.
        """
        
        if not self.dataset.train_features:
            raise ValueError("Dataset must contain designated training features")

        self.df = self.dataset.dataframe.copy()

        self.X  = self.df[self.dataset.train_features]
        self.Y  = self.df['Label_binary']

        X_val   = self.X.values.copy()
        Y_val   = self.Y.values.copy()

        prot_idx   = self.df[self.df['Label_binary']==1].index.values
        unprot_idx = self.df[self.df['Label_binary']==0].index.values
        prot_row   = np.random.choice(prot_idx,6000)
        unprot_row = np.random.choice(unprot_idx,6000)
        rows       = np.concatenate((prot_row, unprot_row))
        
        self.samples = self.df.loc[rows]
        X_val = self.samples[self.dataset.train_features].values.copy()
        Y_val = self.samples['Label_binary'].values.copy()

        LE      = LabelEncoder()
        Y_val   = LE.fit_transform(Y_val)

        scaler = StandardScaler()
        '''
        X_tmp = list()
        Y_tmp = list()
        num_p = num_u = 0
        for i in range(self.num_samples):
            if num_p >= 1000 and num_u >= 1000:
                break

            if self.df.loc[i]['Protected'] == 1:
                if num_p <= 1000:
                    X_tmp.append(X_val[i])
                    Y_tmp.append(Y_val[i])
                    num_p += 1
            else:
                if num_u <= 1000:
                    X_tmp.append(X_val[i])
                    Y_tmp.append(Y_val[i])
                    num_u += 1
        X_val = np.ndarray(X_tmp)
        Y_val = np.ndarray(Y_tmp)
        '''
        X_val = scaler.fit_transform(X_val)

        is_numeric = self.X.apply(lambda s: pd
                                           .to_numeric(s, errors='coerce')
                                           .notnull().all()
                                 )
        if any(res == False for res in is_numeric):
            raise ValueError("Training features must be numeric")

        self.X_val = np.array(X_val,dtype='float32')
        self.Y_val = np.array(Y_val,dtype='float32')

        self.num_p_u = [
                self.dataset.Statistics['Unprotected']['Number'],
                self.dataset.Statistics['Protected']['Number']
                ]

        self.S = self.samples['Protected'].values.copy().astype(int)


    def PR_regularizer(self,weights):
        """
        Prejudice remover regularizer. Punishes model for
        relying too much on sensitive variables.

        Arguments:
            weights - (tensor) Weights of the model

        returns:
            PR regularization along with l2 regularization
        """

        def sigmoid(x,w):

            dot = np.dot(x,w)

            return 1 / (1 + np.exp(-dot))

        weights = weights.numpy().reshape([2,self.num_f])
        
        # p = Pr[y|x,s] = sigmoid(w(s)^T,x)
        # p = np.ndarray, len: num_f
        p = np.array([sigmoid(self.X_val[i,:],weights[self.S[i],:])
                            for i in range(len(self.X_val))])

        # q = Pr[y|s} = \sum_({xi,si)in D st si=s} sigma(xi,si) / |D[s]|
        # q = np.ndarray, len: 2
        q = np.array([np.sum(p[self.S == si])
                            for si in [0,1]]) / self.num_p_u

        # r = Pr[y] = \sum_{(xi.si) in D} sigma(xi,si) / |D|
        # r = numpy.float64
        r = np.sum(p) / len(self.X_val)


        # f = \sum_{x,s,y in D} 
        #            sigma(x,x)  [log(q(s)    - log(r)] +
        #       (1 - sigma(x,s)  [log(1-q(s)) - log(1-r)]
        # f = numpy.float64
        f = np.sum(p * (np.log(q[self.S]) - np.log(r))
                            + (1.0-p) * (np.log(1.0-q[self.S])
                            - np.log(1.0-r))
                  )

                            
        # l2reg = numpy.float64
        l2_reg = np.sum(0.5*np.square(weights))

        return self.eta*f + l2_reg

    
    def fit(self):

        tqdm_callback = tfa.callbacks.TQDMProgressBar()

        def build_model():
            model = Sequential()
            model.add(Dense(60,activation='relu'))
            model.add(Dense(60,activation='relu'))
            #model.add(Dense(30,activation='relu'))
            #model.add(Dense(30,activation='relu'))
            model.add(Dense(self.num_f,activation='relu'))
            model.add(Dense(2,
                            activation='relu',
                            kernel_regularizer=self.PR_regularizer
                     ))
            model.add(Dense(1,activation= 'sigmoid'))
            model.compile(optimizer     = 'adam',
                          loss          = 'binary_crossentropy',
                          metrics       = ['accuracy'],
                          run_eagerly   = True)
            return model

        self.model  = build_model()
        history     = self.model.fit(self.X_val, self.Y_val,
                            batch_size  = 5,
                            callbacks   = [tqdm_callback],
                            epochs      = self.epochs)
        return history
        '''
        estimators = []
        estimators.append(('standardize',StandardScaler()))
        estimators.append(('mlp',KerasClassifier(
                                    build_fn=self.model,
                                    epochs = self.epochs,
                                    batch_size = 5,
                                    #callbacks = [tqdm_callback]
                                    )))
        pipeline = Pipeline(estimators)
        kfold = StratifiedKFold(n_splits=10, shuffle=True)
        self.results = cross_val_score(pipeline, self.X_val, self.Y_val, cv=kfold)
        return self.results
        '''


    def transform(self):

        if not hasattr(self,'model'):
            raise AttributeError("Transform should not be called before fit")

        scalar = StandardScaler()
        X_val       = self.X.values.copy()
        X_val = scalar.fit_transform(X_val)
        predictions = self.model.predict(X_val)

        transformed_dataset = ds.Dataset(
                self.df,
                label_names = self.dataset.label_names,
                protected_attribute_names=self.dataset.protected_attribute_names,
                title = self.dataset.title + ' (PrejudiceRemover)',
                predictions = predictions,
                categorical_features = self.dataset.cat_features,
                training_features = self.dataset.train_features,
                model = self.model,
                alter_dataframe = False)

        return transformed_dataset
        

        

def PrejudiceRemover(dataset,epochs,eta=5):

    if not isinstance(dataset,ds.Dataset):
        raise TypeError("Dataset must be of type aibias.dataset.Dataset")

    print('Preparing data')
    pr_remover = PR_remover(dataset,epochs,eta)

    print('Starting training session')
    pr_remover.fit()

    return pr_remover.transform()
