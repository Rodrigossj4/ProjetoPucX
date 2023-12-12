import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler


class Model:

    def carrega_modelo(path):
        pickle_in = open(path, 'rb')
        model = pickle.load(pickle_in)
        pickle_in.close()
        return model

    def preditor(model, paciente):

        X_input = {'Age':  [paciente['age']],
                   'Sex': [paciente['sex']],
                   'Chest pain type': [paciente['Chest_pain_type']],
                   'bp': [paciente['BP']],
                   'Cholesterol': [paciente['Cholesterol']],
                   'FBS over 120': [paciente['FBS_over_120']],
                   'EKG results': [paciente['EKG_results']],
                   'Max HR': [paciente['Max_HR']],
                   'Exercise angina': [paciente['Exercise_angina']],
                   'ST depression': [paciente['ST_depression']],
                   'Slope of ST': [paciente['Slope_of_ST']],
                   'Number of vessels fluro': [paciente['Number_of_vessels_fluro']],
                   'Thallium': [paciente['Thallium']]
                   }

        atributos = ['Age', 'Sex', 'Chest pain type', 'bp', 'Cholesterol', 'FBS over 120', 'EKG results',
                     'Max HR', 'Exercise angina', 'ST depression', 'Slope of ST', 'Number of vessels fluro', 'Thallium']

        entrada = pd.DataFrame(X_input, columns=atributos)
        array_entrada = entrada.values
        X_entrada = array_entrada[:, 0:13].astype(float)

        # scaler = StandardScaler().fit(X_entrada)

        # rescaledEntradaX = scaler.transform(X_entrada)
        diagnosis = model.predict(X_entrada)

        return diagnosis[0]
