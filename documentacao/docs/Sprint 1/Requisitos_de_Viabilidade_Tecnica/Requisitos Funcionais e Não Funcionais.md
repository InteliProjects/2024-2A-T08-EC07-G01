---
sidebar_position: 1
slug: /requisitos
---

Nesta documentação, apresentamos uma solução tecnológica projetada para atender às necessidades e requisitos específicos da Volkswagen. A eficácia e o sucesso de qualquer solução tecnológica dependem grandemente da clareza, precisão e compreensão de seus requisitos. Portanto, é fundamental definir e entender adequadamente os requisitos funcionais e não funcionais.

## 1 - Requisitos Funcionais

Os requisitos funcionais descrevem as funcionalidades específicas e as operações que a solução deve realizar. Eles são a base para o desenvolvimento e a implementação da solução, delineando as capacidades e os comportamentos esperados do sistema.

---

**1.1 RF-1:** O sistema deve receber progressivamente as informações provenientes da planta e ir preenchendo as informações de montagem de cada um dos carros na linha de montagem.

**Casos de teste:**
- Fazer input de dados separados e verificar se o sistema consegue preencher e organizar as informações corretamente.

---

**1.2 RF-2:** O modelo deve prever e identificar prováveis erros antes que o carro seja levado para o test-drive.

**Casos de teste:**
- Simular se o modelo consegue divulgar um resultado preciso com as informações adquiridas até a etapa especificada da linha de montagem.

---

**1.3 RF-3:** O modelo deve identificar as inconsistências mais prováveis para serem checadas durante o teste e indicar qual tipo de teste é mais adequado para cada situação, de acordo com as informações de montagem dos carros.

**Casos de teste:**
- Testar o output do modelo e verificar se este é personalizado para cada veículo e se realmente contém as principais inconsistências encontradas e os testes recomendados.

---

**1.4 RF-4:** O sistema deve possuir uma área destinada à disponibilização de informações importantes para o usuário, como o status de cada carro registrado, os processos pelos quais já passou e se algum problema foi encontrado até então.

**Casos de teste:**
- Checar se as informações disponibilizadas na interface correspondem diretamente às informações que estão sendo fornecidas pelo modelo de previsão.

---

## 2 - Requisitos Não Funcionais

Os requisitos não funcionais referem-se às características e qualidades do sistema que não estão diretamente relacionadas às funcionalidades específicas, mas que são cruciais para garantir seu desempenho, segurança, escalabilidade e usabilidade. Estes incluem aspectos como desempenho, confiabilidade, segurança, usabilidade e manutenibilidade.

---

**2.1 RNF-1:** O sistema deve apresentar uma predição após a submissão dos dados necessários em até 5 segundos.

**Casos de teste:**
- Fazer inputs de dados corretos para o modelo e monitorar o tempo de predição, cronometrando quanto tempo o modelo demora para apresentar o resultado correto.

---

**2.2 RNF-2:** O modelo deve apresentar uma precisão mínima de 95%.

**Casos de teste:**
- Analisar as métricas a partir de vários testes com dados específicos e entender como o modelo reage no processo.

---

**2.3 RNF-3:** O sistema deve apresentar dashboards com entendimento claro e boa visibilidade, trabalhando de maneira correta o contraste, espaçamento e como as informações são apresentadas.

**Casos de teste:**
- Realizar vários testes de UX na plataforma final.
- Colher métricas como Sucess-rate, Feedback, Consistência...

---

**2.4 RNF-4:** Deve ser possível visualizar claramente o status de cada carro e os problemas encontrados até a etapa atual da linha de montagem.

**Casos de teste:**
- Realizar teste de usabilidade com uma pessoa que nunca utilizou a plataforma antes e verificar se ela consegue cumprir todas as funções da plataforma de maneira fácil e rápida.

---

**2.5 RNF-5:** O sistema deve possuir uma área destinada a receber mais dados para que ele possa adicioná-los ao seu banco de dados e ser retreinado com novas informações.

**Casos de teste:**
- Após adicionar um arquivo para implementar o modelo, o sistema deve retornar uma mensagem sobre o sucesso ou falha da ação por parte do usuário.

---

**2.6 RNF-6:** O sistema deve ser implantado na AWS.

**Casos de teste:**
- Testar a implantação do sistema na AWS e verificar se todas as funcionalidades estão operando corretamente.

---
