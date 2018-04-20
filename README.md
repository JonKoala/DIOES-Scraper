# diariobot-scraper
Ferramenta para automatizar a busca e extração de artigos do [Diário Oficial do Espírito Santo](http://ioes.dio.es.gov.br/portal/visualizacoes/diario_oficial).

### Requisitos
 - [Python](https://www.python.org/) >= 3.6
   - [lxml](http://lxml.de/)
   - [PyYAML](http://pyyaml.org/wiki/PyYAML)
   - [SQLAlchemy](https://www.sqlalchemy.org/)

### Configuração
O projeto depende de um arquivo `appconfig.yml`, na sua raiz, contendo algumas configurações locais. Crie uma cópia do arquivo `appconfig.yml.example` e coloque as configurações do seu ambiente.

Exemplo de `appconfig.yml`:
``` yaml
db:
  connectionstring: '[My PyODBC connection string]'
```
Note que o valor informado para a `connectionstring` deve seguir o padrão do [PyODBC](http://docs.sqlalchemy.org/en/latest/dialects/mssql.html#pass-through-exact-pyodbc-string).

### Execução
Para buscar os artigos de um mês específico, execute o script `ondemand.py` informado o ano e o mês da busca.
``` bash
python ondemand.py 2016 1
```
Para buscar artigos do Diário Oficial a partir da última data de execução do Scraper, execute o script `routine.py`.
``` bash
python routine.py
```
Ao final da execução, os dois scripts devem salvar os artigos encontrados no banco de dados.
