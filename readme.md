# Tech Samples

<h2>Tabela de Conteúdos</h2>

1. [ Sobre ](#sobre)
2. [ Links Relevantes ](#links)
3. [ O Problema a ser solucionado ](#problema)
4. [ A Solução ](#solucao)
5. [ Descrição das rotas](#techs)
6. [ Instalação ](#install)
7. [ Desenvolvedores ](#devs)
8. [ termos de uso ](#termos)

<a name="sobre"></a>

## 1. Sobre

O projeto foi desenvolvido no quarto módulo curso de Desenvolvimento Full Stack da Kenzie Academy Brasil, e colocou em prática tanto nossos conhecimentos técnicos quanto a capacidade de trabalho em equipe dos alunos desenvolvedores. A aplicação é uma API que permite funções como Cadastro e Login com diferentes perfis de usuário, criação de classes de amostra, cadastro de análises com base nas classes existentes , gerenciamento de estoque e mais.

<a name="links"></a>

## 2. Links Relevantes

- <a name="documentação-api" href="https://documenter.getpostman.com/view/20266812/UVypxwW4#15df286a-7568-4320-97b9-34ef7be08195" target="_blank">Documentação API</a>

<a name="problema"></a>

## 3. O Problema A Ser Solucionado

Identificamos uma escassez de propostas que visam soluções na automatização dos processos de análise e emissão de laudos com foco em laboratórios industriais e particulares.
Atualmente a emissão de laudos é feita em sua maioria de forma manual através de uma planilha padrão de excel e exportado para PDF gerando os seguintes problemas:

- Grande probabilidade de falha operacional ( falhas de digitação, despadronização da planilha, validação manual dos resultados das análises )
- Probabilidade de indisponibilidade do arquivo padrão parando todo o fluxo de análise ( exclusão acidental da planilha, perda do histórico de análises caso o arquivo seja corrompido )
- Dificuldade em levantamentos a assertividade de indicadores ( quantidade de análises mensais, análises mais solicitadas)
- Planilha centralizada, duas análises não conseguem ser feitas ao mesmo tempo por pessoas diferentes podendo travar o fluxo de análise de um colaborador

<a name="solucao"></a>

## 4. A Solução

Uma API que permite o gerenciamento de todo o fluxo de análise e visa resolver ou mitigar os problemas citados acima focando em disponibilidade de dados, agilidade, confidencialidade e garantia dos resultados.

<a name="techs"></a>

## 5. Descrição das rotas

|   Método	|               Caminho  	               |                  Responsabilidade	               |                       Regra de Negócio 	          |
|   :-:	    |                 :-:	                   |                    :-:	                           |                             :-:	                  |	
|   POST  	|               signup/	                   |            Criação de um usuário adm.  	       | Não precisa de autenticação                   	      |
|   POST	|             admin/analyst/  	           |            Criação de um usuário analista.        | Apenas administradores podem realizar essa operação. |   
|   POST	|               login/	                   |            Login do usuário. 	                   | Não precisa de autenticação.  	                      |   
|   PATCH	|            profile/<user_id>/	           |            Alteração de senha do usuário. 	       | O usuário precisa estar autenticado.              	  |   
|   GET	    |            admin/analyst/	               |            Lista todos os usuários. 	           | Apenas administradores podem realizar essa operação. |   
|   :-:	    |   	                                   |   	                                               |                                                      |  
|   GET	    |               classes/ 	               |        Lista todas as classes cadastradas  	   | O usuário precisa estar autenticado.                 | 
|   POST	|               classes/	               |                    Cria as classes 	           | Apenas administradores podem realizar essa operação. |   
|   :-:	    |   	                                   |   	                                               |   	                                                  |   
|   POST	|        classes/<class_id>/types/	       |            Cria um novo tipo de análise  	       | Apenas administradores podem realizar essa operação. |  
|   PATCH	|        classes/types/<type_id>/	       |            Pode alterar o nome do type  	       | Apenas administradores podem realizar essa operação. | 
|   :-:	    |   	                                   |   	                                               |                                                      |
|   POST	| classes/types/<type_id>/parameters/  	   |                Cria um novo parâmetro 	           | Apenas administradores podem realizar essa operação. | 
|   DELETE	| classes/types/parameters/<parameter_id>/ |                Remove um parâmetro. 	           | Apenas administradores podem realizar essa operação. | 
|   :-:	    |   	                                   |   	                                               |   	                                                  |
|   POST	|     analysis/classes/<class_id>/ 	       |                Cria uma análise  	               | Apenas analistas podem realizar essa operação.    	  |   
|   PATCH	|              analysis/	               |    Pode alterar o type, o parameter e o result    | Apenas analistas podem realizar essa operação.  	  |   
|   GET		|              analysis/	               |            Lista todas as análises 	           |  Apenas analistas podem realizar essa operação. 	  |   
|   GET		|           analysis/<analysis_id>/	       |            Retorna a análise específica 	       |Apenas analistas podem realizar essa operação.  	  |   
|   :-:	    |   	                                   |   	                                               |   	                                                  |   
|   POST	|               stock/	                   |        Cria o estoque do item consumível. 	       | Apenas administradores podem realizar essa operação. | 
|   POST	|     stock/<stock_id>/consumables/        |  Adiciona a quantidade de consumíveis no estoque. | Apenas administradores podem realizar essa operação. |
|   GET	    |     stock/<stock_id>/consumables/ 	   |        Lista os dados do item consumível 	       | Apenas administradores podem realizar essa operação. | 

<a name="install"></a>

## 6. Instalação e uso

### 6.1 Requisitos:

- Python a partir da versão 3.9.6
- Gerenciador de pacotes <a name="pip" href="https://pip.pypa.io/en/stable/" target="_blank">PIP</a>


### 6.2 Instalação:


6.2.1 - Após o clone no repositório crie um ambiente virtual na pasta do projeto

`python -m venv venv`

6.2.2 - Para ativar o ambiente virtual utilize:

`source venv/bin/activate`

6.2.3 - Instale as dependências necessárias para o projeto utilizando o PIP:

`pip install -r requirements.txt`

6.2.5 - Para rodar as migrations do projeto utilize o comando `python manage.py migrate` no terminal



6.2.5 - Para rodar o projeto utilize o comando `python manage.py runserver` no terminal, caso de tudo certo recebera uma mensagem parecida com essa:

```
    March 31, 2022 - 21:34:12
    Django version 4.0.3, using settings 'tech_samples.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
```

<a name="devs"></a>

## 7. Deselvolvedores

- <a name="alex" href="https://www.linkedin.com/in/alesilva-dev/" target="_blank">Alexander Silva</a>
- <a name="eduardo" href="https://www.linkedin.com/in/eduardoparraga/" target="_blank">Eduardo Parraga</a>
- <a name="felipe" href="https://www.linkedin.com/in/felipe-silva-98ads/" target="_blank">Felipe Silva</a>
- <a name="fernando" href="https://www.linkedin.com/in/nandorodrigo/" target="_blank">Fernando Rodrigo</a>


<a name="termos"></a>

## 8. Termos de uso

Este é um projeto Open Source para fins educacionais e não comerciais, **Tipo de licença** - <a name="mit" href="https://opensource.org/licenses/MIT" target="_blank">MIT</a>
