# Serviço de Recomendação de Pontos de Auriculoterapia/Acupressão

Microsserviço desenvolvido para a Avaliação Final da disciplina **Engineering Software
Development** (MBA FIAP — Prof. Rafael Matsuyama). O tema foi conectado ao TCC do grupo
(aplicativo de autocuidado com IA e terapias integrativas): dado um ou mais sintomas
informados pelo usuário, o serviço recomenda os pontos de auriculoterapia/acupressão
associados.

## Equipe

- **Caio Silva Alberto**  — RM 368446
- **Fábio Luiz de Barros** — RM 368580
- **Higor Robles de Freitas Pereira**  — RM 368316
- **Vitor Alencastro Pantoja** — RM 367683

## Stack

- **Python 3** + **Flask** — servidor e rotas
- **pytest** — testes automatizados
- Dados em arquivo **JSON** (sem banco de dados por enquanto)
- **HTML/CSS/JS** simples para uma página de testes manuais

## Estrutura do projeto

```
.
├── app.py                 # Rotas (controller)
├── service.py              # Regra de negócio (recomendação)
├── repository.py           # Acesso aos dados dos pontos
├── data/
│   └── pontos.json         # Base de pontos (id, nome, sintomas, localização, orientação)
├── templates/
│   └── index.html           # Página visual para testar o serviço no navegador
├── tests/
│   ├── test_repository.py   # Testes de unidade (lógica de matching)
│   └── test_app.py          # Testes de integração (endpoints via Flask test client)
└── requirements.txt
```

A separação em três camadas (rota → serviço → repositório) mantém a lógica de
recomendação isolada de onde os dados vêm — hoje é um arquivo JSON, mas poderia
virar um banco de dados sem alterar o `service.py` nem as rotas.

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

O servidor sobe em `http://127.0.0.1:5000`.

## Endpoints

| Método | Rota                  | Descrição                                                        |
|--------|------------------------|--------------------------------------------------------------------|
| GET    | `/`                    | Página visual para testar o serviço manualmente                   |
| GET    | `/pontos`              | Lista todos os pontos cadastrados                                  |
| GET    | `/pontos/<id>`         | Detalha um ponto específico                                        |
| POST   | `/pontos/recomendar`   | Recebe `{"sintomas": [...]}` e devolve os pontos recomendados      |
| POST   | `/pontos`              | Cadastra um novo ponto (uso administrativo/apoio)                  |

## Lógica de recomendação

O `repository.py` normaliza o texto (minúsculas, sem espaços nas pontas, sem acentos)
antes de comparar os sintomas recebidos com os sintomas cadastrados em cada ponto —
assim, "Dor de Cabeça", "dor de cabeça" e variações de acentuação são tratadas como o
mesmo sintoma. Um ponto nunca é retornado duplicado, mesmo que combine com mais de um
sintoma pesquisado.

## Base de pontos atual

4 pontos cadastrados em `data/pontos.json`, cobrindo sintomas como ansiedade aguda,
insônia, dor de cabeça/enxaqueca, estresse, náusea, entre outros. Novos pontos podem
ser adicionados diretamente nesse arquivo, seguindo a mesma estrutura de campos.

## Como testar

- **Pela página visual (deploy online):** https://qia-microsservice.vercel.app/ — conectado
  ao repositório do GitHub, atualiza automaticamente a cada mudança no repo.
- **Pela página visual (localmente):** acesse `http://127.0.0.1:5000/` — tem campo de busca
  por sintomas, botões de teste rápido com casos já validados, e um botão para listar todos
  os pontos.
- **Por linha de comando (PowerShell):**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:5000/pontos/recomendar" -Method Post -ContentType "application/json" -Body (@{sintomas=@("ansiedade aguda")} | ConvertTo-Json)
  ```

## Testes automatizados

Suíte com **7 testes** usando `pytest`, dividida em duas camadas:

- `tests/test_repository.py` (4 testes de unidade) — testam a lógica de matching de
  sintomas diretamente no `repository`: sintoma único, múltiplos pontos sem duplicar,
  normalização de maiúsculas/acentos e sintoma inexistente (lista vazia).
- `tests/test_app.py` (3 testes de integração) — testam os endpoints via
  `app.test_client()` do Flask: recomendação com sintoma válido, erro 400 quando o
  campo `sintomas` não é enviado, e listagem de todos os pontos.

Para rodar:

```bash
pytest -v
```

## Status da entrega

- [x] Microsserviço funcional (rotas, service, repository)
- [x] Base de dados real cadastrada (4 pontos)
- [x] Lógica de recomendação por sintomas implementada e testada
- [x] Página visual de apoio para testes manuais
- [x] Caminho da avaliação escolhido: **Test Suite** — 7 testes automatizados (unidade
      e integração), todos passando