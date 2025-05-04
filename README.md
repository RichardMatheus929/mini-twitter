# Mini-twitter

Essa documentação visa explicar um pouco sobre como foi desenvolvido cada requisito, decisões técnicas e explicações gerais.

### Intruções para rodar
Na pasta do projeto:
```
docker compose up --build
```
Lembre de deixar a sessão aberta no terminal ou usar o -d

**Consideração:** Não consegui resolver um problema que causa um delay na inicialização do service do db, e dá erro no container do django. Se isso acontecer, feche a sessão e rode novamente o docker compose após buildar as imagens, deve funcionar.

## Arquitetura geral
O projeto possui 4 apps - accounts,follow,likes,posts - Cada app possui suas lógicas de serializers, tests, models, urls, views etc...
O painel de admin com django está configurado para os apps também, você pode entrar no container e criar um superuser para ter acesso.
A documentação das rotas está disponível no postman enviado. Instruções sobre o frontend devem estar disponíveis no repositório: 
https://github.com/RichardMatheus929/mini-twitter-react 

## Diagrama simplificado
![image](https://github.com/user-attachments/assets/89b90f3a-4b37-49a5-82d7-a5b2b9ab5274)

accounts_user - Tabela de usários baseada no AbstractUser do django.

posts_post - Armazena quem criou o post(User), data de criação, e o conteúdo em imagem do post

follow_follow - Relacionada com usuários, armazena o seguidor(User) seguindo(User), também armazena a data de criação

likes_like - Relaciona o user que deu like em qual post, também armazena a data de criação

## Requisitos

**⚙️ [TC.1] API Development**

Desenvolvida a partir do DRF. Usado ApiView nas rotas de signin e signup e viewsets no restante. Implementa muita das funcionalidades built-in do DRF como a paginação, as lógicas de permissions, ModelViewSet, Serializer de validação entre outros. 

**🔐 [TC.2] Authentication**

A autenticação é feita nas rotas fornecidas no app de accounts. Usa a [djangorestframework-simplejwt](https://pypi.org/project/djangorestframework-simplejwt/) para trabalhar a lógica de token e autentiicação. A criação de usuários é feito a partir de um model user personalizado a partir do AbstrctUser do django.

**💽 [TC.3.1] Database**

Usa postgres, disponível no docker-compose do projeto. O database está configurado para ser criado a partir das informações no .env, com o volume setado para ser criado na mesma pasta do projeto.

**🔋 [TC.3.2] Caching & Scalability**

Utiliza cache em duas principais rotas

- A rota que retorna a listagem de posts possui um campo um pouco mais pesado, que é a lista de usuários que curtiram esse post, isso permite que o front visualize quem curtiu o post, e exiba uma interface diferente caso ele mesmo tenha curtido. Essa informação é cacheada, e só é atualizada quando é feita qualquer alteração na quantidade de likes do post, para não retornar dados desatualizado.
- A outra rota é as informações de follow de um user, para ser exibido no front quantos seguidores um usário tem, quem ele segue ou quem segue ele. Essa é uma informação um pouco mais pesada também, por isso é cacheada e atualizada quando há alterações nos follow de um user.

**📄 [TC.4.] Pagination**

A paginação é utilizada na rota de listagem dos posts usando a paginação built-in do DRF. Sem muitas alterações personalizadas. O page_size está configurado para 10.

**🧪 [TC.5] Testing**

Os testes estão escritos por apps, cada app possui testes para suas rotas e funcionalidades. Eles são pensados nas funcionalidades mais críticas e regras de negócio. 

**📝 [TC.6] Documentation**

A descrição de cada rota e implementação resumida dos apps está no postman. Cada rota possui um exemplo de payload e descrição de sua função e se há necessidade de autorização.

**🐳 [TC.7] Docker**

A descrição de como rodar o projeto via docker deve estar acima desssa documentação. A descrição de como rodar o frontend com docker também deve estar no readME do repositório do front.

**📂 [TC.8] Git**

O projeto completo possui dois repositórios.

https://github.com/RichardMatheus929/mini-twitter

https://github.com/RichardMatheus929/mini-twitter-react
