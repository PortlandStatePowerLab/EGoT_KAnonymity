from sklearn import preprocessing
import numpy as np

class Transformer:
    '''
        A wrapper around sklearn label encoder. The goal is to transform categorical columns into numeric.
    '''
    def __init__(self,labels:list = []):
        '''
            Constructor: initializes the encoder & fits it to the passed labels
            Labels are empty by default.
        '''
        self.encoder = preprocessing.LabelEncoder()
        self.encoder.fit(labels)
        pass

    def transform(self,vals:list)->np.ndarray:
        '''
            Transforms the passed values to the corresponding encoding. 
            Fails if any of the values is one the tranformer has not fitted to.
        '''
        try:
            return self.encoder.transform(vals)
        except KeyError:
            return -1
        
    def add(self, keys:list) -> bool:
        '''
            Adds the passed keys to the encoder's list of classes
        '''
        labels = self.encoder.classes_
        labels = np.append(labels,keys)
        self.encoder.fit(labels)
        return True

    def reverse(self,vals) -> np.ndarray:
        '''
            Transforms the passed values inversely back to the corresponding keys. 
            Fails if any of the values cannot be converted back to one of the classes.
        '''
        return list(self.encoder.inverse_transform(vals))

