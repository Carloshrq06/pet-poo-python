"""
=============================================================
SISTEMA DE GESTÃO DE PET SHOP
Disciplina: Programação Orientada a Objetos (POO)
Linguagem: Python 3
=============================================================

PROBLEMA REAL RESOLVIDO:
Um pet shop precisa cadastrar clientes e animais, agendar
serviços (banho, tosa, consulta) e calcular automaticamente
o valor cobrado de acordo com a espécie e o porte do animal,
além de registrar o faturamento total.

CONCEITOS DE POO APLICADOS:
- Abstração    : classe abstrata Animal (não pode ser instanciada)
- Herança      : Cachorro, Gato e Ave herdam de Animal
- Polimorfismo : cada subclasse calcula a taxa do serviço do seu jeito
- Encapsulamento: atributos privados com @property e @setter
- Composição   : Agendamento "tem um" Cliente e "tem um" Animal
"""

# ── Bibliotecas padrão do Python (não precisa instalar nada) ──────────────────
from abc import ABC, abstractmethod   # para criar classes e métodos abstratos
import json                            # para salvar/ler dados em arquivo .json
import os                              # para verificar se o arquivo já existe


# ══════════════════════════════════════════════════════════════════════════════
#  ABSTRAÇÃO + ENCAPSULAMENTO
#  Animal é uma classe ABSTRATA: serve como "molde" para as subclasses.
#  Não é possível fazer Animal() diretamente — só Cachorro(), Gato(), Ave().
# ══════════════════════════════════════════════════════════════════════════════
class Animal(ABC):
    """Classe abstrata que representa um animal cadastrado no pet shop."""

    especie = "Animal"  # cada subclasse vai sobrescrever esse valor

    def __init__(self, nome: str, idade: int, peso: float):
        # Os setters abaixo já fazem a validação dos dados
        self.nome  = nome
        self.idade = idade
        self.peso  = peso

    # @property: permite ler o atributo como se fosse público
    @property
    def nome(self):
        return self._nome

    # @setter: valida o valor antes de guardar no atributo privado _nome
    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("o nome do animal não pode ser vazio")
        self._nome = valor.strip().title()  

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("a idade não pode ser negativa")
        self._idade = valor

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        valor = float(valor)
        if valor <= 0:
            raise ValueError("o peso deve ser maior que zero")
        self._peso = valor

    #Métodos abstratos: cada subclasse É OBRIGADA a implementar
    @abstractmethod
    def calcular_taxa_servico(self, servico: str) -> float:
        """Retorna o valor cobrado por um serviço para este animal."""

    @abstractmethod
    def emitir_som(self) -> str:
        """Retorna o som característico da espécie."""

    def descricao(self) -> str:
        return f"{self.nome} ({self.especie}, {self.idade} anos, {self.peso}kg)"

    def __str__(self):
        return self.descricao()


# ══════════════════════════════════════════════════════════════════════════════
#  HERANÇA + POLIMORFISMO
#  Cachorro, Gato e Ave herdam de Animal e implementam os métodos abstratos
#  cada uma do seu jeito — isso é polimorfismo.
# ══════════════════════════════════════════════════════════════════════════════

class Cachorro(Animal):
    especie = "Cachorro"
    TAXAS = {"banho": 40.0, "tosa": 35.0, "consulta": 80.0}

    def calcular_taxa_servico(self, servico: str) -> float:
        servico = servico.lower().strip()
        if servico not in self.TAXAS:
            raise ValueError(f"serviço '{servico}' não existe para cachorros")
        valor = self.TAXAS[servico]
        if servico in ("banho", "tosa") and self.peso > 20:
            valor += 15.0
        return valor

    def emitir_som(self) -> str:
        return "Au au!"


class Gato(Animal):
    especie = "Gato"
    TAXAS = {"banho": 50.0, "tosa": 45.0, "consulta": 80.0}

    def calcular_taxa_servico(self, servico: str) -> float:
        servico = servico.lower().strip()
        if servico not in self.TAXAS:
            raise ValueError(f"serviço '{servico}' não existe para gatos")
        return self.TAXAS[servico]  

    def emitir_som(self) -> str:
        return "Miau!"


class Ave(Animal):
    especie = "Ave"
    TAXAS = {"banho": 25.0, "consulta": 60.0}

    def calcular_taxa_servico(self, servico: str) -> float:
        servico = servico.lower().strip()
        if servico not in self.TAXAS:
            raise ValueError(f"serviço '{servico}' não existe para aves")
        return self.TAXAS[servico]

    def emitir_som(self) -> str:
        return "Piu piu!"


# ══════════════════════════════════════════════════════════════════════════════
#  ENCAPSULAMENTO
#  Cliente também usa atributos privados com validação via @property
# ══════════════════════════════════════════════════════════════════════════════
class Cliente:
    def __init__(self, nome: str, telefone: str):
        self.nome     = nome
        self.telefone = telefone

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("o nome do cliente não pode ser vazio")
        self._nome = valor.strip().title()

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, valor):
        digitos = "".join(c for c in valor if c.isdigit())
        if len(digitos) < 8:
            raise ValueError("telefone inválido (use ao menos 8 números)")
        self._telefone = valor.strip()

    def __str__(self):
        return f"{self.nome} (tel: {self.telefone})"


# ══════════════════════════════════════════════════════════════════════════════
#  COMPOSIÇÃO
#  Agendamento NÃO herda de Cliente nem de Animal.
#  Ele "tem um" Cliente e "tem um" Animal como atributos — isso é composição.
# ══════════════════════════════════════════════════════════════════════════════
class Agendamento:
    def __init__(self, cliente: Cliente, animal: Animal, servico: str, data: str):
        self.cliente = cliente
        self.animal  = animal
        self.servico = servico.lower().strip()
        self.data    = data
        self.valor = animal.calcular_taxa_servico(self.servico)

    def to_dict(self) -> dict:
        return {
            "cliente" : self.cliente.nome,
            "telefone": self.cliente.telefone,
            "animal"  : self.animal.nome,
            "especie" : self.animal.especie,
            "servico" : self.servico,
            "data"    : self.data,
            "valor"   : self.valor,
        }

    def __str__(self):
        return (f"[{self.data}] {self.servico.title()} para {self.animal.nome} "
                f"({self.cliente.nome}) - R$ {self.valor:.2f}")


# ══════════════════════════════════════════════════════════════════════════════
#  CLASSE PRINCIPAL
#  PetShop orquestra tudo: mantém as listas de clientes, animais e
# ══════════════════════════════════════════════════════════════════════════════
class PetShop:
    ARQUIVO_DADOS = "agendamentos.json"  

    def __init__(self, nome: str):
        self.nome         = nome
        self.clientes     : list[Cliente]     = []
        self.animais      : list[Animal]      = []
        self.agendamentos : list[Agendamento] = []

    def cadastrar_cliente(self, nome: str, telefone: str) -> Cliente:
        cliente = Cliente(nome, telefone)
        self.clientes.append(cliente)
        return cliente

    def cadastrar_animal(self, especie: str, nome: str, idade, peso) -> Animal:
        especie_norm = especie.lower().strip()
        classes = {
            "cachorro" : Cachorro,
            "gato"     : Gato,
            "ave"      : Ave,
            "passaro"  : Ave,
            "pássaro"  : Ave,
        }
        if especie_norm not in classes:
            raise ValueError("espécie não suportada (use cachorro, gato ou ave)")
        animal = classes[especie_norm](nome, idade, peso)
        self.animais.append(animal)
        return animal

    def agendar_servico(self, cliente: Cliente, animal: Animal,
                        servico: str, data: str) -> Agendamento:
        agendamento = Agendamento(cliente, animal, servico, data)
        self.agendamentos.append(agendamento)
        self._salvar_dados()  
        return agendamento

    def faturamento_total(self) -> float:
        """Soma o valor de todos os agendamentos da sessão atual."""
        return sum(a.valor for a in self.agendamentos)

    def _salvar_dados(self):
        dados = [a.to_dict() for a in self.agendamentos]
        with open(self.ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def carregar_historico(self) -> list[dict]:
        if os.path.exists(self.ARQUIVO_DADOS):
            with open(self.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []


# ══════════════════════════════════════════════════════════════════════════════
#  INTERFACE DE LINHA DE COMANDO (CLI)
# ══════════════════════════════════════════════════════════════════════════════

def escolher_da_lista(lista, rotulo, rotulo_plural):
    if not lista:
        print(f"Nenhum {rotulo} cadastrado ainda.")
        return None
    print(f"\n-- {rotulo_plural} cadastrados --")
    for i, item in enumerate(lista, start=1):
        print(f"{i}. {item}")
    try:
        escolha = int(input(f"Escolha o número do {rotulo}: "))
        if escolha < 1 or escolha > len(lista):
            raise IndexError
        return lista[escolha - 1]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return None


def menu():
    petshop = PetShop("Pet Shop Amigo Fiel")

    opcoes = """
========== PET SHOP AMIGO FIEL ==========
1. Cadastrar cliente
2. Cadastrar animal
3. Agendar serviço
4. Listar agendamentos
5. Ver faturamento total
6. Ver histórico salvo (agendamentos.json)
0. Sair
==========================================
"""

    while True:
        print(opcoes)
        escolha = input("Escolha uma opção: ").strip()

        try:
            if escolha == "1":
                nome     = input("Nome do cliente: ")
                telefone = input("Telefone do cliente: ")
                cliente  = petshop.cadastrar_cliente(nome, telefone)
                print(f"-> Cliente cadastrado: {cliente}")

            elif escolha == "2":
                especie = input("Espécie (cachorro/gato/ave): ")
                nome    = input("Nome do animal: ")
                idade   = input("Idade (anos): ")
                peso    = input("Peso (kg): ")
                animal  = petshop.cadastrar_animal(especie, nome, idade, peso)
                print(f"-> Animal cadastrado: {animal} | som: {animal.emitir_som()}")

            elif escolha == "3":
                cliente = escolher_da_lista(petshop.clientes, "cliente", "Clientes")
                if not cliente:
                    continue
                animal = escolher_da_lista(petshop.animais, "animal", "Animais")
                if not animal:
                    continue
                servico = input("Serviço (banho/tosa/consulta): ")
                data    = input("Data (dd/mm/aaaa): ")
                ag      = petshop.agendar_servico(cliente, animal, servico, data)
                print(f"-> Agendamento criado: {ag}")

            elif escolha == "4":
                if not petshop.agendamentos:
                    print("Nenhum agendamento registrado nesta sessão.")
                for ag in petshop.agendamentos:
                    print(ag)

            elif escolha == "5":
                print(f"Faturamento total (sessão atual): "
                      f"R$ {petshop.faturamento_total():.2f}")

            elif escolha == "6":
                historico = petshop.carregar_historico()
                if not historico:
                    print("Nenhum histórico salvo ainda.")
                for item in historico:
                    print(f"[{item['data']}] {item['servico'].title()} - "
                          f"{item['animal']} ({item['especie']}) / "
                          f"{item['cliente']} - R$ {item['valor']:.2f}")

            elif escolha == "0":
                print("Até logo!")
                break

            else:
                print("Opção inválida, tente novamente.")

        except ValueError as e:
            print(f"Erro: {e}")


# ── Ponto de entrada do programa ──────────────────────────────────────────────
if __name__ == "__main__":
    menu()
