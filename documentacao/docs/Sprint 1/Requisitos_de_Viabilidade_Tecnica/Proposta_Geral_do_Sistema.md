Esse projeto visa a construção de um sistema de manutenção preditiva para a linha de produção de carros T-Cross, um modelo da VolksWagen. O sistema visa prever quais carros na linha de produção têm maior probabilidade de possuir alguma falha, direcionando-os para os testes específicos a fim de realizar as manutenções de acordo.

Esse sistema desenvolvido será composto por uma **interface** acessível pelo usuário onde será possível visualizar as informações preditas, além de possibilitar o envio as informações adquiridas pelos sensores ao longo da produção dos carros, que serão utilizados para treinar o **modelo**, segunda parte desse sistema. O modelo será responsável por pegar as informações (os **inputs**), e devolver a classificação daquele carro correspondente, ou seja, se será necessário realizar o teste de rodagem ou não. 

Dentro da interface, além da classificação dos carros na linha de produção, também é possível acessar uma visualização dos dados a fim de permitir *insigths* aos gestores da linha de produção, ao conseguir visualizar numericamente quais são as falhas mais comuns, por exemplo, entre outros padrões identificados pelo modelo.



## Primeira Versão de Arquitetura do Sistema

Para uma melhor visualização da estrutura do sistema mencionado acima, é possível observar o diagrama de blocos abaixo, que ilustra como cada um dos componentes do sistema se comunica. 


<div align="center">

**Diagrama de Blocos**

![Diagrama de blocos](/img/diagrama-de-blocos.png)

**Fonte:** Elaborado pela equipe Cross The Line

</div>

### Frontend e Backend
Ambos constituem a formação da **interface**, sendo o Frontend a interface visual que o usuário consegue acessar e o Backend o responsável por gerir as informações, utilizando-se de APIs para a comunicação com o modelo e o frontend.
No **Frontend**, há a possibilidade de acessar tanto os **outputs** do modelo com a classificação dos carros, quanto adicionar  os **inputs**, que podem ser, por exemplo, o upload de informações para o treinamento do modelo, ou dados sobre um carro específico para poder classificá-lo (se há possíveis falhas ou não).

No **Backend**, os inputs recebidos pelo usuário serão ou repassados para o modelo através de uma API para serem processados, ou serão *armazenados em nuvem* para re-treinar o modelo posteriormente de maneira mensal, atualizando-o com novos dados. 

### Modelo
O **modelo** será o microsserviço de inteligência artificial que irá processar os dados e devolverá uma classificação dos carros, dizendo se há uma probabilidade alta ou baixa de falhas e qual o teste mais indicado para cada caso.
Esse **output** será repassado para o backend, que irá repassar para o frontend através de uma API, tornando o resultado visível para o usuário.


### Armazenamento de dados
Haverão duas formas: um **banco de dados** local e um **armazenamento de dados em nuvem.** No banco de dados, ficarão salvos os outputs (predições) do modelo, que serão comparados posteriormente com os dados reais a fim de re-treinar o modelo. Para haver a comparação com dados reais, o usuário poderá salvar em nuvem a cada mês os resultados das falhas nos carros em um arquivo *csv ou *xlsx, o que também irá contribuir para a melhora do modelo.
