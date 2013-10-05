Um pouco sobre descritores em Python
####################################

:date: 2011-12-11
:tags: descriptors, descritores, meta-programação, programação, python, software
:category: Python
:slug: um-pouco-sobre-descritores-em-python
:author: Gustavo Fonseca
:summary: Blá
:lang: pt


Falae pessoal! Hoje pela manha, durante uma aula de Python (Oficinas Turing - 
por Luciano Ramalho), eu tive novamente a oportunidade de entrar em contato 
com um mecanismo de abstração fantástico da linguagem - os Descritores ou 
Descriptors em inglês. Não que tenha sido uma total novidade para mim, mas as 
discussões guiaram a aula para questões delicadas, que podem envolver desde 
implementações mais simples até as mais avançadas com metaclasses e outros 
fantasmas, e eu pensei que talvez fosse uma boa oportunidade para escrever
o primeiro blog post da minha vida =P

Então vamos lá, o que é um descritor?

Descritor é um atributo de classe que controla a semântica da atribuição e 
acesso a um atributo na instância da classe [*]_. Entendeu?

É basicamente um mecanismo de encapsulamento, que permite adicionar lógica 
nas ações de acesso, atribuição e exclusão de atributos dos objetos, com 
reuso de código e ao mesmo tempo mantendo sua API elegante.

E como eu faço isso?

A tarefa mínima para dar vida a um descritor é implementar o método 
``__get__``, assim você terá um descritor somente leitura.

Para usar como exemplo, temos uma classe Livro que possui 2 atributos: 
título e autor individual. Para o autor individual eu defini uma regra 
bem besta: somente serão aceitos nomes compostos por, pelo menos, duas 
partes, para que ao ser acessado o retorno seja: 
‘Gustavo Fonseca’ -> ‘FONSECA, Gustavo’.

Exemplo 0 (Descritor Somente Leitura): código aqui:
===================================================

.. code-block:: python
    :linenos: table

    class Autor(object):
        def __init__(self, nome_atr):
            self.nome_atr = '_'+nome_atr

        def __get__(self, instancia, classe):
            desmontado = getattr(instancia, self.nome_atr).split()
            sobrenome = desmontado[-1]
            restante = ' '.join(desmontado[:-1])
            return '%s, %s' % (sobrenome.upper(), restante)

    class Livro(object):
        autor_individual = Autor('autor_individual')

        def __init__(self, titulo, autor_individual):
            self.titulo = titulo
            if len(autor_individual.split()) < 2:
                raise ValueError('Deve ser informado o nome e sobrenome')
            self._autor_individual = autor_individual


Note que:

    * Descritores são **atributos de classe**
    * O valor deve ser **atribuído na instância**
    * O nome do atributo está sendo passado como argumento na instanciação 
      do descritor (bizarro né? mas o descritor precisa de um nome para usar 
      como identificador para o atributo que ele vai definir na instância, 
      por hora vamos fazer assim ok?)

Legal, agora a gente pode criar um novo papel de autor, por exemplo 
“Autor Organizador” e, com o descritor, já teríamos toda essa lógica de 
formatação implementada. Mas teríamos que implementar novamente o trecho 
que trata da atribuição no ``__init__``. Então vamos transformar o descritor em 
*leitura* e *escrita*:

Exemplo 1 (Descritor Leitura/Escrita): código aqui:
===================================================

.. code-block:: python
    :linenos: table

    class Autor(object):
        def __init__(self, nome_atr):
            self.nome_atr = '__'+nome_atr

        def __set__(self, instancia, valor):
            if len(valor.split()) < 2:
                raise ValueError('Deve ser informado o nome e sobrenome')

            setattr(instancia, self.nome_atr, valor)

        def __get__(self, instancia, classe):
            desmontado = getattr(instancia, self.nome_atr).split()
            sobrenome = desmontado[-1]
            restante = ' '.join(desmontado[:-1])
            return '%s, %s' % (sobrenome.upper(), restante)

    class Livro(object):
        autor_individual = Autor('autor_individual')

        def __init__(self, titulo, autor_individual):
            self.titulo = titulo
            self.autor_individual = autor_individual


Note que:

    * Todas as notas do exemplo anterior ainda estão valendo
    * Está bem feio esse nome do atributo sendo passado na instanciação do descritor, ein!

Então agora vamos resolver essa questão da passagem do nome do atributo:

Exemplo 2 (Descritor Leitura/Escrita sem passar o nome do atributo): código aqui:
=================================================================================

.. code-block:: python
    :linenos: table

    class Autor(object):
        def __set__(self, instancia, valor):
            if len(valor.split()) < 2:
                raise ValueError('Deve ser informado o nome e sobrenome')

            for nome_atr, valor_atr in instancia.__class__.__dict__.items():
                if valor_atr == self:
                    self.nome_atr = '__'+nome_atr
                    setattr(instancia, self.nome_atr, valor)
                    break

        def __get__(self, instancia, classe):
            desmontado = getattr(instancia, self.nome_atr).split()
            sobrenome = desmontado[-1]
            restante = ' '.join(desmontado[:-1])
            return '%s, %s' % (sobrenome.upper(), restante)

    class Livro(object):
        autor_individual = Autor()

        def __init__(self, titulo, autor_individual):
            self.titulo = titulo
            self.autor_individual = autor_individual


Para entender este exemplo é necessário se aprofundar um pouco mais no assunto. 
O método ``__set__`` de um descritor recebe os argumentos:

    * **self**: uma referência à instância do próprio descritor, no caso uma instância de Autor
    * **instancia**: a instância no qual o descritor foi definido, no caso uma instância de Livro
    * **valor**: o valor à ser atribuído

O que estamos fazendo é iterar sobre os atributos da classe (haja vista que descritores 
são atributos da classe), em busca do que possui a instância do descritor como valor. 
Quando achamos o cara, pegamos o nome do atributo e definimos, na instância, um 
atributo privado com o seu nome. Entendeu? =]

Espero ter ajudado! Até mais.


.. [*] Tradução livre da definição existente no livro Python in a Nutshell 2 ed. - Alex Martelli.

