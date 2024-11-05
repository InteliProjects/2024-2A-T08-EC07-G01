---
title: "Modelo Principal"
sidebar_position: 1
---

Considerando o escopo do projeto e a proposta de valor que a equipe Cross The Line deseja entregar ao parceiro, a arquitetura do modelo foi reestruturada. Com isso, serão desenvolvidos 10 modelos distintos: um modelo principal, responsável por prever se o carro apresentará ou não falhas, e outros 9 modelos auxiliares, que irão classificar o tipo de falha entre as nove possíveis, caso o modelo principal indique a presença de falhas.

Com isso em mente, é possível acompanhar a documentação relacionada ao desenvlvimento do modelo principal a seguir:

## RNN

Na Sprint 1, realizamos a exploração e o tratamento dos dados, além de aplicarmos o primeiro modelo (KNN). Nesta Sprint, aproveitamos o tratamento realizado anteriormente e testamos modelos utilizando Redes Neurais Recorrentes (RNNs).

Redes Neurais Recorrentes (RNNs) são um tipo de rede neural projetada para reconhecer padrões em sequências de dados. Elas são particularmente eficazes no processamento de séries temporais e dados sequenciais, pois possuem laços internos que permitem a retenção de informações de estados anteriores, facilitando a modelagem de dependências temporais.

Ao aplicar modelos de Redes Neurais Recorrentes (RNNs), esperamos um desempenho superior, uma vez que esses modelos têm a capacidade de analisar os dados de maneira mais profunda. Isso permite a identificação de padrões mais complexos, o que pode aprimorar significativamente as métricas do modelo preditivo.

### Preparação dos dados

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

### Modelo LSTM

LSTM (Long Short-Term Memory) é um tipo de rede neural recorrente (RNN) projetada para lidar com o problema de "vanishing gradient" que afeta as RNNs tradicionais. Ele é especialmente eficaz para modelar sequências de dados, como séries temporais, textos ou qualquer dado onde a ordem e a dependência temporal são importantes.

A LSTM utiliza células de memória que podem armazenar e acessar informações por longos períodos de tempo. Cada célula possui três portas principais:

- **Porta de entrada (Input Gate):** Controla a quantidade de nova informação que deve ser armazenada na célula de memória.

- **Porta de esquecimento (Forget Gate):** Decide quanta informação antiga deve ser descartada da célula de memória.

- **Porta de saída (Output Gate):** Determina qual parte da informação armazenada na célula deve ser utilizada para gerar a saída.

Essa arquitetura permite que as LSTMs capturem dependências de longo prazo em sequências, tornando-as adequadas para tarefas como previsão de séries temporais, tradução automática, e processamento de linguagem natural (NLP).

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

Com o código acima, foi possível aplicar o modelo LSTM e analisar sua performance. Os resultados das métricas associadas ao modelo, conforme descrito, são os seguintes:

- **Acurácia:** 0.8520
- **Precisão:** 0.8088
- **Recall:** 0.9049
- **F1-Score:** 0.8542

Observa-se que o modelo apresentou um desempenho sólido, com métricas superiores em relação à Sprint anterior. Destaca-se especialmente o recall, que é nosso principal foco, pois é crucial minimizar a ocorrência de falsos negativos. Falsos negativos referem-se a casos em que o modelo não previu uma falha, embora ela realmente estivesse presente.

### Modelo GRU

O GRU (Gated Recurrent Unit) é outro tipo de rede neural recorrente (RNN) que, assim como a LSTM, foi projetado para lidar com o problema de "vanishing gradient" e modelar dependências de longo prazo em sequências de dados. No entanto, o GRU é uma versão simplificada do LSTM, com uma estrutura menos complexa.

A estrutura do GRU combina a célula de estado e a saída em uma única unidade e utiliza duas portas principais:

- **Porta de atualização (Update Gate):** Controla a quantidade de nova informação que deve ser armazenada e decide quanta informação da etapa anterior deve ser esquecida ou mantida.

- **Porta de reset (Reset Gate):** Decide quanta da informação anterior deve ser esquecida ao calcular a nova entrada.

Devido à sua simplicidade, as GRUs tendem a ser mais rápidas de treinar e podem ser igualmente eficazes para muitas tarefas que envolvem dados sequenciais, como previsão de séries temporais e tradução de textos. Além disso, a GRU pode ser preferida quando o objetivo é reduzir a complexidade computacional, pois ela requer menos recursos comparado ao LSTM.

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

Com o código acima, foi possível aplicar o modelo GRU e analisar sua performance. Os resultados das métricas associadas ao modelo, conforme descrito, são os seguintes:

- **Acurácia:** 0.8611
- **Precisão:** 0.8187
- **Recall:** 0.9119
- **F1-Score:** 0.8628

Observa-se que o modelo apresentou um ótimo desempenho, com métricas ligeiramente superiores em relação ao modelo LSTM, sendo o recall um ponto de destaque. 

### Considerações finais

Os resultados obtidos com os dois modelos de Redes Neurais Recorrentes (RNNs) demonstram uma melhoria significativa em comparação ao modelo da Sprint anterior, conforme evidenciado pelas métricas apresentadas. Esses resultados sugerem que a exploração de diferentes arquiteturas de redes neurais pode ser uma estratégia promissora para otimizar ainda mais o desempenho preditivo.

Atualmente, o modelo GRU (Gated Recurrent Unit) mostrou-se o mais eficaz e será adotado como referência para futuras análises e testes. Continuaremos a avaliar outras abordagens para maximizar a performance do modelo e oferecer a melhor solução preditiva possível.

