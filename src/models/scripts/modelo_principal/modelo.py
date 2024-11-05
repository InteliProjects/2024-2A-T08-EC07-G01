import models.scripts.preparacao as preparacao
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense


def executable(df ):
    X_train, X_test, y_train, y_test = preparacao.preparacao_dados(df)
    # Construção do modelo com GRU
    model = Sequential()

    model.add(GRU(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(GRU(50, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy')

    # Treinamento do modelo
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

    return model


  