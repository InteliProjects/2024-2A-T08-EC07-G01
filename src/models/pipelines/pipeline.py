import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import json

def aggregate_by_id(df, id_value):
    subset = df[df['ID'] == id_value]   
    return subset.groupby('KNR').agg(
        NAME=('NAME', 'count'),
        SOK=('STATUS', lambda x: (x == 10).sum()),
        SNOK=('STATUS', lambda x: (x == 13).sum()),
        DATA=('DATA', lambda x: (x.max() - x.min()).total_seconds() / (3600*24))
    ).rename(columns={
        'NAME': f'ID{id_value}NAME',
        'SOK': f'ID{id_value}SOK',
        'SNOK': f'ID{id_value}SNOK',
        'DATA': f'ID{id_value}DATA'
    })

def preprocess_data(data):
    
    '''
    data format example:
    data = '[{"Col A":"Val","Col B":10,"Col C":1},{"Col A":"Val","Col B":4,"Col C":0}]'
    '''

    data = json.loads(data)
    data = pd.DataFrame(data)
    data = data.drop(columns=['Unnamed: 0'], axis=1, errors='ignore')
    data = data.dropna()
    data = data.drop_duplicates()
    data = data.drop(columns=['UNIT', 'VALUE_ID', 'VALUE'], axis=1, errors='ignore')
    data['DATA'] = pd.to_datetime(data['DATA'], errors='coerce')
    
    id1 = aggregate_by_id(data, 1)
    id2 = aggregate_by_id(data, 2)
    id718 = aggregate_by_id(data, 718)
    final_data = id1.join(id2, on='KNR', how='outer').join(id718, on='KNR', how='outer').reset_index()
    final_data = final_data[['KNR','ID1NAME', 'ID1SOK', 'ID1SNOK', 'ID1DATA', 'ID2NAME', 'ID2SOK', 'ID2SNOK', 'ID2DATA', 'ID718NAME', 'ID718SOK', 'ID718SNOK', 'ID718DATA']]
    final_data = final_data.fillna(0)
    cols_to_normalize = ['ID1NAME','ID1SOK', 'ID1SNOK', 'ID1DATA', 'ID2NAME', 'ID2SOK', 'ID2SNOK', 'ID2DATA', 'ID718NAME', 'ID718SOK', 'ID718SNOK', 'ID718DATA']
    scaler = MinMaxScaler()
    final_data[cols_to_normalize] = scaler.fit_transform(final_data[cols_to_normalize])
    x_test = np.array(final_data).reshape((final_data.shape[0], final_data.shape[1], 1))
    print(x_test)
    return x_test

def predict(x_test):
    '''with open('./Keras_YN_1000.h5', 'rb') as model_file:
        model = load_model(model_file)'''
    model = load_model("Keras_YN_1000.h5", custom_objects={'mse': 'mse'}) 
    x_test = np.asarray(x_test).astype(np.float32)
    y_pred = model.predict(x_test)
    y_pred_classes = (y_pred > 0.5).astype(int)
    return y_pred_classes

def pipeline(data):
    x_test = preprocess_data(data)
    Y_pred = predict(x_test)
    return Y_pred

if __name__ == '__main__':
    prediction = pipeline('[{"Unnamed: 0": "NaN", "KNR": "20235076008", "NAME": "SECTION_ZP8_00000001", "ID": 718, "STATUS": 13, "UNIT": "V", "VALUE_ID": 80, "VALUE": 12.479, "DATA": "2024-02-02 08:03:03"}]')
    print('Resultado: ', prediction)


