---
title: Modelo de Classificação
sidebar_position: 1
---

# Modelo de classificação (S_GROUP_ID_1)

Como explicado anteriormente, a solução proposta pela equipe Cross The Line envolve a construção de um modelo principal capaz de detectar se ocorrerá ou não uma falha em um carro específico. Caso uma falha seja prevista, um modelo de classificação binário será acionado para identificar se um erro ocorrerá em uma classe específica de falhas. Nesta Sprint, focamos na avaliação do desempenho do modelo para a classe "S_GROUP_ID_1", com o objetivo de identificar o modelo com melhor performance. Com base nos resultados obtidos, aplicaremos os insights e aprimoramentos aos modelos de outras classes.

Para realizar os testes e comparar o desempenho dos modelos, utilizamos dois conjuntos de dados distintos. O primeiro não incluiu as informações de torque fornecidas pelo parceiro, enquanto o segundo incorporou esses dados para o treinamento e aplicação dos modelos.

Para ambos os conjuntos de dados, testamos as Redes Neurais Recorrentes (RNNs) LSTM e GRU, cujos funcionamentos foram detalhadamente explicados na documentação da Sprint 2, onde foram aplicadas ao modelo principal. Como essas RNNs apresentaram bom desempenho naquela etapa, decidimos utilizá-las como base para os testes desta Sprint.

Aplicamos as mesmas técnicas de preparação de dados e configuração das RNNs realizadas na Sprint 2, conforme documentado, e os detalhes podem ser acompanhados na sequência.

## Preparação dos dados

Antes de aplicar os modelo de RNNs, foi realizada a preparação dos dados da seguinte forma:

```python
# Importando o dataframe preparado, registrado no notebook anterior. 
# Caso seja necessário, o código para exportar esse dataframe está comentado e disponível no arquivo "preparacao_dados_modelo_principal.ipynb".
df = pd.read_csv('../data/preparacao_modelo_1.csv')
df

# Separando as features (X) e o target (y)
X = df.drop(columns=['FALHA', 'KNR'])  # 'KNR' é apenas um identificador, então deve ser removido
y = df['FALHA']

# Separando em dados de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Converte X_train e X_test para arrays NumPy, caso ainda não sejam.
X_train = np.array(X_train)
X_test = np.array(X_test)

# Reestrutura X_train e X_test para ter 3 dimensões.
# A nova forma do array será (n_samples, n_features, 1)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
```

Com a preparação descrita acima, garantimos que os dados estão no formato apropriado para serem utilizados pelos modelos.

## Modelo LSTM

Para realizar o treinamento e teste do modelo, utilizamos o Keras, uma API de alto nível para construir e treinar redes neurais que está integrada ao TensorFlow, uma biblioteca de aprendizado de máquina. A seguir é possível acompanhar esse processo

```python

# Construção do modelo com LSTM
model = Sequential()

model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

# Treinamento do modelo
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

#Prever os dados de teste
y_pred = model.predict(X_test)

# Converter as probabilidades em classes binárias (0 ou 1)
y_pred_classes = (y_pred > 0.5).astype(int)

# Calcular as principais métricas
accuracy = accuracy_score(y_test, y_pred_classes)
precision = precision_score(y_test, y_pred_classes)
recall = recall_score(y_test, y_pred_classes)
f1 = f1_score(y_test, y_pred_classes)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

# Matriz de Confusão
cm = confusion_matrix(y_test, y_pred_classes)

# Exibindo a Matriz de Confusão
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.show()
```

## Modelo GRU

Para realizar o treinamento e teste do modelo, utilizamos o Keras assim como no modelo LSTM. A seguir é possível acompanhar esse processo

```python 

# Construção do modelo com GRU
model = Sequential()

model.add(GRU(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(GRU(50, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy')
# Treinamento do modelo
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))
# Prever os dados de teste
y_pred = model.predict(X_test)

# Converter as probabilidades em classes binárias (0 ou 1)
y_pred_classes = (y_pred > 0.5).astype(int)

# Calcular as principais métricas
accuracy = accuracy_score(y_test, y_pred_classes)
precision = precision_score(y_test, y_pred_classes)
recall = recall_score(y_test, y_pred_classes)
f1 = f1_score(y_test, y_pred_classes)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
``` 

## Desempenho

Ao aplicar os diferentes modelos em cada conjunto de dados, obtivemos os seguintes resultados:

**Conjunto de dados sem dados de torque:**

- LSTM:
  - Acurácia: 0.6225
  - Precisão: 0.6225
  - Recall: 1.000
  - F1-score: 0.7673

- GRU:
  - Acurácia: 0.6197
  - Precisão: 0.6406
  - Recall: 0.8864
  - F1-score: 0.7437

**Conjunto de dados com dados de torque:**

- LSTM:
  - Acurácia: 0.6047
  - Precisão: 0.6207
  - Recall: 0.9388
  - F1-score: 0.7473

- GRU:
  - Acurácia: 0.6226
  - Precisão: 0.6227
  - Recall: 0.9994
  - F1-score: 0.7673

Com base nos resultados obtidos, observamos que tanto os modelos LSTM quanto GRU tiveram um bom desempenho em termos de recall. No entanto, outras métricas, como a acurácia, não apresentaram o mesmo nível de performance, tanto com os dados de torque quanto com o dataframe sem esses dados. Ao comparar os dois dataframes, notamos que ambos tiveram um desempenho muito similar, o que indica que ambos podem ser utilizados nos modelos. No entanto, para os próximos testes, optamos por trabalhar com o dataframe que inclui os dados de torque, pois ele apresentou métricas mais consistentes e fornece um conjunto mais rico de features que podem impactar positivamente nos próximos testes que iremos realizar.

Para melhorar as métricas observadas, pretendemos aplicar as seguintes técnicas na próxima Sprint:

- Diferentes testes de balanceamento
- Teste de outros tipos de modelos.
- Revisão e aprimoramento do tratamento dos dados

## Últimos testes realizados nessa Sprint

**Balanceamento por undersampling com clusterização**

Ainda essa Sprint, realizamos testes com o balanceamento por undersampling com clusterização, utilizando os centróides de cada cluster. Utilizamos essa tecnica a partir do código abaixo, utilizando X2_balanced e y2_balanced para treinar e aplicar os modelos GRU e LSTM. Entretanto, as métricas diminuiram drasticamente, indicando que devem ser realizadas melhorias ou na forma de balanceamento, ou no tramaento dos dados que estamos utilizando. 

```python

# Separando as classes majoritária e minoritária com base no target y2
X2_majority = X2[y2 == 0]
X2_minority = X2[y2 == 1]

# Definindo o número de clusters como o tamanho da classe minoritária
n_clusters = len(X2_minority)

# Aplicando o K-Means à classe majoritária
kmeans = KMeans(n_clusters=n_clusters, random_state=1)
kmeans.fit(X2_majority)

# Pegando os centróides dos clusters
X2_majority_centroids = kmeans.cluster_centers_

# Combinando os centróides com a classe minoritária
X2_balanced = np.vstack((X2_majority_centroids, X2_minority))
y2_balanced = np.hstack((np.zeros(len(X2_majority_centroids)), np.ones(len(X2_minority))))
```

**Teste de rede neural convolucional**

Além disso, tentamos também aplicar a seguinte rede neural convolucional, para testar a performance do modelo. Infelizmente, não obtivemos resultados tão positivos quanto os dos modelo GRU e LSTM, porém, pretendemos focar em pesquisar e aplicar novos tipos de rede neural convolucional que possam se adequar melhor ao problema e trazer melhores resultados na próxima Sprint.

```python
# Definir o modelo CNN
model_3 = Sequential()

# Primeira camada convolucional
model_3.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(X2_train.shape[1], 1)))
model_3.add(MaxPooling1D(pool_size=2))
model_3.add(Dropout(0.3))

# Segunda camada convolucional
model_3.add(Conv1D(filters=64, kernel_size=2, activation='relu'))
model_3.add(MaxPooling1D(pool_size=2))
model_3.add(Dropout(0.3))

# Flatten para converter dados 2D em 1D
model_3.add(Flatten())

# Camada totalmente conectada
model_3.add(Dense(64, activation='relu'))
model_3.add(Dropout(0.5))

# Camada de saída para classificação binária
model_3.add(Dense(1, activation='sigmoid'))

# Compilação do modelo
model_3.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Treinamento do modelo
model_3.fit(X2_train, y2_train, epochs=100, batch_size=32, validation_data=(X2_test, y2_test))

# Prever os dados de teste
y_pred_3 = model_3.predict(X2_test)

# Converter as probabilidades em classes binárias (0 ou 1)
y_pred_classes_3 = (y_pred_3 > 0.5).astype(int)

# Calcular as principais métricas
accuracy = accuracy_score(y2_test, y_pred_classes_3)
precision = precision_score(y2_test, y_pred_classes_3)
recall = recall_score(y2_test, y_pred_classes_3)
f1 = f1_score(y2_test, y_pred_classes_3)

# Exibir as métricas
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

```

## Conclusão e insights

Os resultados indicam que, ao contrário do que observamos com o modelo principal na Sprint anterior, os modelos de classificação não se adaptaram tão bem de imediato às Redes Neurais Recorrentes (RNNs) aplicadas nesta Sprint. Existem alguns fatores que podem explicar esse desempenho:

- O tratamento de dados realizado até o momento não resultou em métricas satisfatórias. Isso sugere que talvez seja necessário reavaliar as features utilizadas e a forma como os dados estão sendo estruturados.
- O método de balanceamento aplicado não foi o mais adequado para essa situação, indicando que outros tipos de balanceamento devem ser testados.
- As Redes Neurais Recorrentes podem não ser totalmente compatíveis com o conjunto de dados atual, sugerindo a necessidade de explorar outros tipos de modelos.
Com base nessas hipóteses, nossa estratégia para a próxima Sprint será mapear e organizar testes adicionais para validá-las e melhorar a performance do modelo. Assim, poderemos aplicar as melhorias às outras classes com maior segurança.