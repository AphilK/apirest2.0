# API Rest para um E-Commerce

Esse projeto foi feito com o intuito de aprender mais sobre APIs Rest feitos com FastAPI e um banco de dados PostgreSQL, além de contaneirizá-los com Docker, **o projeto não está completo**, mais abaixo há uma lista com *features* que implementarei, aumentando a complexidade do projeto a medida que aprendo mais e mais sobre.

**Importante salientar que como esse projeto tem um caráter de aprendizado, não utilizarei IA generativa, todo código aqui foi feito por mim, com base em pesquisas e leituras de documentações e fórums na internet.**

Toda e qualquer crítica construtiva é bem-vinda!

## Como instalar e rodar o projeto

**Caso não possua Docker ou Python instalados, a aplicação não funcionará**

1. Abra o terminal (de preferência Linux ou WSL)
2. `git clone git@github.com:AphilK/apirest2.0.git`
3. `cd apirest2.0`
4. `pip install -r requirements.txt` ou `uv sync` caso use uv, que é minha preferência
5. `docker compose build`
6. `docker compose up` pode adicionar o `-d` caso não deseje ler todos os logs no terminal

Então a documentação da API poderá ser aberta no navegador em http://127.0.0.1/docs

## Como usar o projeto

Você pode consumir a API por meio de métodos HTTP: `GET` `POST` `PUT` ou `DELETE`, em caso de dúvidas, na própria documentação (http://127.0.0.1/docs) há mais informações como a API funciona, e pode testar em tempo real seu funcionamento.

## Como contribuir

Como o caráter do projeto é puramente o aprendizado, ao final deste arquivo tem meu e-mail e linkedin para contato.

## Licença

⚖️️ MIT Licence

## TO-DOs (Próximos passos)

- Implementar mais regras de negócio de modo a aumentar o realismo dessa API;
- Uma interface front-end para consumir a API e torná-la mais visual;
- Implementar microsserviços e protocolo de mensageria para descentralizar a aplicação;
- Cumprimento de princípios de cybersegurança;
- Colocar a aplicação na WEB para acesso público.

## Contato

- Email: joaosilvanascimento.jops@gmail.com
- Linked-in: https://www.linkedin.com/in/joao-pedro-n/