# -*- coding: utf-8 -*-
"""House_price_ANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mp4IwBppFKhPghpK5bJZEgoQB6q8vk8_

**Importing the libreries**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import graphviz

# Import tensorflow and keras
import tensorflow as tf
import keras

# For creating ANN model
from keras.layers import Dense, Dropout
from keras.models import Sequential

# For splitting 
from sklearn.model_selection import train_test_split

# For scaling and encoding
from sklearn.preprocessing import LabelEncoder, StandardScaler

# For selecting the best features
from sklearn.feature_selection import SelectKBest, f_regression

# %matplotlib inline

from google.colab import files
uploaded = files.upload()

import io
df = pd.read_csv(io.BytesIO(uploaded['kc_house_data.csv']))

df.head(10)

df.info()

df.isnull().sum()



"""**Encoding the categorical columns.**"""

df[['id', 'date', 'price', 'zipcode', 'lat', 'long', 'bathrooms', 'floors']] = df[['id', 'date', 'price', 'zipcode', 'lat', 'long', 'bathrooms', 'floors']].apply(LabelEncoder().fit_transform)



df.head()



"""**Data visualization.**"""

_, ax = plt.subplots(1, 3, figsize=(20, 8))
sns.countplot(x = "bedrooms", hue="grade", data = df, ax= ax[0])
sns.countplot(x = "bathrooms", hue="grade", data = df, ax = ax[1])
sns.countplot(x = "floors", hue="grade", data = df, ax = ax[2])

_, ax = plt.subplots(1, 3, figsize=(20, 8))
sns.scatterplot(x = "price", y = "sqft_living", data = df, hue="condition", ax = ax[0])
sns.scatterplot(x = "price", y = "sqft_above", data = df, hue="condition", ax = ax[1])
sns.scatterplot(x = "price", y = "yr_built", data = df, hue="condition", ax = ax[2])



plt.figure(figsize=(20,8))
bplot = df.boxplot(patch_artist=True)
plt.xticks(rotation=40)       
plt.ylim(0,25000)
plt.show()

df.corr()

plt.figure(figsize = (20,20))
sns.heatmap(df.corr(), annot = True, cmap = 'PuBu')

df.corr().loc[:, 'price'].abs().sort_values(ascending = False)

df.corr().loc[:, 'price'].abs().sort_values(ascending = False).plot.bar(color = 'black')



"""**Dividing the above dataset into X and y.**"""

y = np.array(df['price'])
y = y.reshape(-1,1)

X = df.iloc[:, df.columns != 'price']



"""**To select important features.**"""

fs = SelectKBest(score_func=f_regression, k=15)
X_selected = fs.fit_transform(X, y)

X_selected.shape

X_selected



"""**Splitting of the dataset.**"""

X_train_full, X_test, y_train_full, y_test = train_test_split(X_selected, y, random_state = 42)
X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, random_state = 42)

X_train_full.shape



"""**Standardizing of the dataset.**"""

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)



np.random.seed(42)
tf.random.set_seed(42)



"""**Creation of ANN model.**"""

model = Sequential()

model.add(Dense(32, activation = 'relu', input_shape = (15, ), name = 'Input'))
model.add(Dense(64, activation = 'relu', name = 'Dense_1'))
model.add(Dense(128, activation = 'relu', name = 'Dense_2'))
model.add(Dropout(0.25))

model.add(Dense(1, name = 'Output'))

model.compile(loss = 'mean_squared_error',
              optimizer = keras.optimizers.Adam(learning_rate = 0.001),
              metrics = ['mae'])

model.summary()

model_history = model.fit(X_train, y_train, epochs = 60, validation_data = (X_valid, y_valid), batch_size = 64)

plt.plot(model_history.history['loss'])
plt.title('Mean squared error')
plt.grid(True)

plt.plot(model_history.history['mae'])
plt.title('Mean absolute error')
plt.grid(True)

mae_test = model.evaluate(X_test, y_test)
print("Loss = ",mae_test[0])
print('MAE = ', mae_test[1])

X_selected[1]

df.head(2)



X_selected[1]

"""**Prediction of the below data.**"""

'''
Bedrooms = 3,
Bathrooms = 8,
sqft_living = 2520,
sqft_lot = 7242,
floors = 2,
waterfront = 0,
view = 0
grade = 7, 
sqft_above = 2170,
sqft_basement = 400, 
yr_built = 1951,
yr_renovated = 1991,
lat = 4478, 
sqft_living15 = 1690,
sqft_lot15 = 7639

'''

model.predict(scaler.transform(np.array([[ 3,8, 2570, 7242,2,0, 0, 7, 2170,  400, 1951,1991, 4478, 1690, 7639]])))

y[1]

y_pred = model.predict(X_test)

y_pred

pd.DataFrame(model_history.history).plot(figsize = (15, 7))
plt.gca()
plt.grid(True)
plt.show()

