# Sistema de Gestão de Pet Shop (POO em Python)

## 📌 O que o programa faz

É um sistema de linha de comando (CLI) para um pet shop. Permite:

- Cadastrar **clientes**
- Cadastrar **animais** (cachorro, gato ou ave)
- **Agendar serviços** (banho, tosa, consulta) — o valor cobrado é calculado
  automaticamente de acordo com a espécie (e, no caso de cães, também o porte)
- Listar os agendamentos feitos na sessão
- Ver o **faturamento total**
- Consultar o **histórico salvo** em `agendamentos.json` (os agendamentos
  são gravados em disco automaticamente, então persistem entre execuções)

Problema real resolvido: um pet shop precisa controlar quem são seus clientes,
quais animais atende, quais serviços foram agendados e quanto isso representa
em receita — sem precisar de planilha ou papel.

## ▶️ Como executar

Requer apenas Python 3 (sem bibliotecas externas):

```bash
python3 petshop.py
```

Use o menu numérico exibido no terminal para navegar entre as opções.

## 🧩 Conceitos de POO utilizados

| Conceito | Onde aparece |
|---|---|
| **Abstração** | `Animal` é uma classe abstrata (`ABC`), com os métodos `calcular_taxa_servico` e `emitir_som` marcados como `@abstractmethod`. Não é possível instanciar `Animal` diretamente — só suas subclasses. |
| **Herança** | `Cachorro`, `Gato` e `Ave` herdam de `Animal` e reaproveitam atributos/comportamentos comuns (nome, idade, peso, validações). |
| **Polimorfismo** | O código chama `animal.calcular_taxa_servico(servico)` da mesma forma para qualquer animal, mas cada subclasse executa essa lógica de um jeito diferente (cachorro grande paga mais no banho/tosa, ave não tem tosa, etc.). O mesmo vale para `emitir_som()`. |
| **Encapsulamento** | Atributos como `_nome`, `_idade`, `_peso` (em `Animal`) e `_telefone` (em `Cliente`) são privados e só podem ser alterados através de `@property`/`@setter`, que validam os dados (ex: peso não pode ser negativo, telefone precisa ter dígitos suficientes). |
| **Composição** | `Agendamento` não herda de `Cliente` nem de `Animal` — ele **tem um** `Cliente` e **tem um** `Animal` como atributos. Isso é uma relação de composição/associação entre classes. |

## 🗂️ Estrutura do código

- `Animal` (abstrata) → `Cachorro`, `Gato`, `Ave`
- `Cliente`
- `Agendamento` (composto por `Cliente` + `Animal`)
- `PetShop` (classe que orquestra tudo: listas de clientes/animais/agendamentos
  e persistência em JSON)
- Funções de CLI (`menu`, `escolher_da_lista`) que só cuidam da interação com
  o usuário, sem misturar regra de negócio com interface

## ✅ Tratamento de erros

Todas as entradas passam por validação (nomes vazios, idade/peso negativos,
telefone curto, espécie ou serviço inexistente, escolha de menu fora do
intervalo). Erros não derrubam o programa — apenas mostram uma mensagem e
voltam ao menu.
