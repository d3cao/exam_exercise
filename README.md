# Aurora: laboratório de evolução de software

A Aurora é uma empresa fictícia de logística que começou atendendo lojas do Recife. Seu sistema cresceu por meio de correções rápidas: cada contrato novo acrescentava condicionais, cada cliente copiava um fluxo e cada equipe mantinha sua própria configuração. Agora a empresa quer operar em outras regiões e oferecer serviços mais flexíveis.

Você recebeu o código existente e as solicitações de evolução abaixo. Seu trabalho é identificar os problemas de projeto, escolher uma organização orientada a objetos e implementar as features preservando os contratos de negócio.

O laboratório cobre 12 desafios de revisão de padrões criacionais e estruturais. Os nomes das soluções não aparecem aqui: decidir quais conceitos aplicar faz parte do exercício. Os módulos são independentes e podem ser resolvidos em qualquer ordem.

## Preparação

Requisitos: Python 3.11 ou superior e `pip`. Apenas a instalação das dependências exige acesso ao índice de pacotes; o código e os testes executam localmente, sem APIs reais, credenciais ou arquivos externos.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest
```

No Windows, ative o ambiente com `.venv\Scripts\activate`.

Para selecionar um exercício:

```sh
python -m pytest tests/test_d06_legacy.py -v
```

Para separar regressão e aceitação:

```sh
python -m pytest -m 'not xfail'
python -m pytest -m xfail
```

Os testes comuns documentam comportamentos que já funcionam. Os testes marcados com `@pytest.mark.xfail(strict=True, reason=...)` descrevem features pendentes. Inicialmente a suíte deve terminar sem falhas comuns, com esses casos como `XFAIL`.

Ao implementar uma feature, remova a marca dos testes correspondentes. `XPASS(strict)` é uma falha proposital: indica que um teste passou, mas sua marca de pendência ainda existe. Uma marca colocada em um teste parametrizado se aplica a todos os seus casos; termine todos eles antes de removê-la. Para ver as falhas pendentes sem o tratamento de expectativa:

```sh
python -m pytest tests/test_d06_legacy.py --runxfail
```

Não altere as expectativas para acomodar a implementação. Você pode criar classes, separar responsabilidades e reorganizar internamente cada módulo. Preserve as entradas públicas listadas e seus resultados; elas representam os clientes existentes. Os testes verificam comportamento e algumas propriedades observáveis, mas não garantem por si só a qualidade do projeto. Depois de fazê-los passar, revise duplicação, acoplamento e facilidade de extensão.

Valores monetários e pesos usam números simples neste laboratório, sem conversão de moedas ou requisitos de arredondamento. Campos adicionais e casos não descritos não precisam de novas políticas. Os argumentos usam identificadores em inglês; textos de negócio estão em português, exceto documentos regionais especificados.

## 01 — Mais uma modalidade de entrega

**Código:** `aurora/d01_delivery.py` · **Testes:** `tests/test_d01_delivery.py`

**Hoje:** cotação, despacho e rastreamento conhecem diretamente as modalidades rodoviária e aérea. A equipe precisa editar três trechos parecidos toda vez que entra um veículo.

**Solicitação:** atender entregas de bicicleta. As três operações precisam usar a modalidade escolhida sem espalhar novas decisões de criação pelos fluxos de negócio.

**Contrato:** `quote(mode, weight)`, `dispatch(mode, order_id)` e `track(mode, code)`. A nova modalidade é `bike`: tarifa `4 + weight`, código `BIKE-{order_id}` e veículo `bicycle`. Preserve `road` e `air`.

**Exemplo:** `quote('bike', 3)` → `7`; `dispatch('bike', '42')` → `'BIKE-42'`; `track('bike', 'BIKE-42')` → `{'code': 'BIKE-42', 'vehicle': 'bicycle'}`.

**Aceite:** todos os fluxos funcionam para os três veículos; pesos não positivos na cotação e modalidades desconhecidas levantam `ValueError`. O ponto de decisão para novas modalidades não deve ficar copiado nos três fluxos.

## 02 — Abertura de operações regionais

**Código:** `aurora/d02_regions.py` · **Testes:** `tests/test_d02_regions.py`

**Hoje:** a região da etiqueta vem da solicitação, mas comprovante e frete usam o Brasil explicitamente. As escolhas são independentes, permitindo misturar produtos incompatíveis.

**Solicitação:** preparar conjuntos coerentes para Brasil, Estados Unidos e Portugal. Uma operação americana não pode entregar etiqueta americana com comprovante brasileiro ou frete em reais.

**Contrato:** `prepare(country, order_id, weight)` retorna um dicionário com `label`, `receipt` e `freight`. Preserve também `label(country, order_id)`, `receipt(country, order_id)` e `freight(country, weight)`. Todos os produtos têm `country`; os documentos têm `text`; o frete tem `currency` e `amount`.

| País | Texto da etiqueta | Texto do comprovante | Moeda | Frete |
| --- | --- | --- | --- | --- |
| `BR` | `Entrega {id}` | `Comprovante {id}` | `BRL` | `10 + 2 * weight` |
| `US` | `Delivery {id}` | `Receipt {id}` | `USD` | `5 + 3 * weight` |
| `PT` | `Entrega {id}` | `Recibo {id}` | `EUR` | `6 + 2 * weight` |

**Exemplo:** `prepare('US', '42', 2)` → `{'label': {'country': 'US', 'text': 'Delivery 42'}, 'receipt': {'country': 'US', 'text': 'Receipt 42'}, 'freight': {'country': 'US', 'currency': 'USD', 'amount': 11}}`.

**Aceite:** produtos da mesma região em toda solicitação, inclusive ao alternar países; `ValueError` para país desconhecido ou peso não positivo. A montagem de um conjunto não deve depender de escolhas regionais desconectadas.

## 03 — Formulários de pedidos personalizados

**Código:** `aurora/d03_orders.py` · **Testes:** `tests/test_d03_orders.py`

**Hoje:** um construtor extenso recebe campos opcionais posicionais. O código aceita seguro negativo e mantém os itens do formulário por referência, permitindo que a edição de uma tela altere um pedido já criado.

**Solicitação:** oferecer uma montagem clara de pedidos, com opcionais e validação antes de disponibilizar o resultado. A estrutura interna e a forma de organizar as etapas são parte do exercício.

**Contrato:** `build_order(data)` recebe `recipient`, `address`, `items` e opcionais `insurance=0`, `instructions=''`, `priority=False`. Retorna um objeto com esses atributos. Preserve `create_order(recipient, address, items, insurance=0, instructions='', priority=False)` como entrada compatível. Cada item possui `sku` e `quantity`.

**Exemplo:** `build_order({'recipient': 'Ana', 'address': 'Rua A', 'items': [{'sku': 'KIT', 'quantity': 1}], 'insurance': 100, 'instructions': 'Portaria', 'priority': True})` → pedido com os mesmos valores e itens próprios.

**Aceite:** destinatário/endereço em branco, lista vazia, quantidades não positivas e seguro negativo levantam `ValueError`. Alterações nos itens do formulário ou de outro pedido não afetam o pedido criado, inclusive dicionários dentro da lista. Chamadores não devem precisar compreender uma longa sequência de opcionais posicionais.

## 04 — Pedidos de campanhas recorrentes

**Código:** `aurora/d04_campaigns.py` · **Testes:** `tests/test_d04_campaigns.py`

**Hoje:** campanhas armazenam diretamente a entrada do cliente e geram pedidos com uma cópia apenas da camada externa. Alterar quantidade ou cidade de uma entrega contamina outras entregas.

**Solicitação:** reutilizar modelos de pedidos completos sem reconstruir manualmente todos os seus campos e sem compartilhar os dados mutáveis dos pedidos derivados.

**Contrato:** `Campaigns().save(name, order)` registra um dicionário de modelo; `spawn(name)` retorna um novo dicionário. Existe o modelo `welcome` com destinatário `Cliente`, endereço em `Recife`, rua `Rua A` e um item `KIT`, quantidade `1`. Campos adicionais do modelo devem ser preservados.

**Exemplo:** `first = campaigns.spawn('welcome')`; depois de `first['address']['city'] = 'Natal'`, uma nova chamada a `spawn('welcome')` ainda retorna cidade `Recife`.

**Aceite:** pedidos independentes entre si e do modelo; alterações na entrada passada a `save` não mudam o registro; campos arbitrários do modelo são preservados. Modelo inexistente levanta `KeyError`. Cada instância de `Campaigns` possui seus próprios registros.

## 05 — Uma configuração operacional coerente

**Código:** `aurora/d05_settings.py` · **Testes:** `tests/test_d05_settings.py`

**Hoje:** cada acesso constrói uma configuração, incrementando `Settings.loads`. Cotação e despacho podem operar com limites e moedas diferentes depois de uma atualização.

**Solicitação:** todos os serviços do mesmo processo devem consultar a mesma configuração, inicializada somente uma vez quando acessada pela primeira vez.

**Contrato:** `get_settings()` retorna um objeto com `currency='BRL'`, `max_weight=30` e `update(*, currency=None, max_weight=None)`. `QuoteService().settings` e `DispatchService().settings` acessam essa mesma configuração. `Settings.loads` continua sendo um contador observável de carregamentos.

**Exemplo:** `QuoteService().settings.update(currency='USD', max_weight=50)` → uma instância posterior de `DispatchService` observa `USD` e `50`, assim como as instâncias anteriores.

**Aceite:** identidade compartilhada por todas as entradas de serviço e por `get_settings`; somente um carregamento por ciclo do módulo; limite não positivo levanta `ValueError` sem alterar moeda ou limite. Os testes recarregam o módulo entre casos para simular processos independentes. Acesso concorrente e multiprocessamento ficam fora do exercício.

## 06 — Conectar a transportadora legada

**Código:** `aurora/d06_legacy.py` · **Testes:** `tests/test_d06_legacy.py`

**Hoje:** a plataforma usa `send(dict)`, mas a transportadora legada disponibiliza `submit(str)`. Seu protocolo recebe `order_id|weight|postal_code` e responde XML. O fluxo atual não consegue utilizá-la.

**Solicitação:** a mesma entrada de negócio deve aceitar os dois fornecedores, preservando o protocolo legado e o formato da plataforma.

**Contrato:** `ship(payload, carrier)` recebe um dicionário serializável em JSON com `order_id`, `weight`, `postal_code`; retorna `{'tracking': str, 'status': 'accepted'}`. `ModernCarrier` mantém o prefixo `MOD-`; `LegacyCarrier` mantém `LEG-`. Não modifique as assinaturas nem o protocolo das classes dos fornecedores: representam sistemas fora do controle da Aurora.

**Exemplo:** `ship({'order_id': '42', 'weight': 2, 'postal_code': '05000'}, legacy)` envia exatamente `'42|2|05000'` e retorna `{'tracking': 'LEG-42', 'status': 'accepted'}`. `legacy.requests` registra as chamadas.

**Aceite:** conversão de entrada e saída sem modificar o dicionário recebido; XML com caracteres escapados é interpretado corretamente; código postal conserva zeros iniciais. Antes de chamar o legado, rejeite peso não positivo e `|` no identificador ou código postal com `ValueError`. Não use rede nem substitua o simulador por uma API real.

## 07 — Documentos em mais canais

**Código:** `aurora/d07_documents.py` · **Testes:** `tests/test_d07_documents.py`

**Hoje:** classes misturam o tipo de documento com seu canal. Há etiqueta em texto/HTML e comprovante em texto. Cada combinação tende a exigir uma nova classe completa.

**Solicitação:** completar comprovantes HTML e adicionar manifestos em texto e HTML, permitindo evoluir tipos de documento e canais separadamente.

**Contrato:** `render(kind, channel, order)` recebe tipos `label`, `receipt`, `manifest`, canais `text`, `html` e pedido com `id`, `recipient`. Prefixos: `Etiqueta`, `Comprovante`, `Manifesto`. Texto: `{prefix}: {id} - {recipient}`; HTML: o mesmo conteúdo envolvido por `<p>...</p>`.

**Exemplo:** `render('manifest', 'html', {'id': '42', 'recipient': 'Ana'})` → `'<p>Manifesto: 42 - Ana</p>'`.

**Aceite:** todas as seis combinações; escape dos valores dinâmicos em HTML, preservando texto simples; `ValueError` para tipo ou canal desconhecido. Adicionar um canal não deve exigir reimplementar o conteúdo de cada documento.

## 08 — Caixas dentro de pallets e caixas

**Código:** `aurora/d08_cargo.py` · **Testes:** `tests/test_d08_cargo.py`

**Hoje:** o somatório de uma caixa assume que todos os filhos são itens. O código não reconhece pallets e ignora validação dos valores dentro de caixas.

**Solicitação:** tratar cargas individuais e agrupadas de forma uniforme, permitindo agrupamentos em vários níveis.

**Contrato:** `totals(cargo)` retorna `{'weight': number, 'price': number}`. Item: `{'kind': 'item', 'weight': 2, 'price': 10}`. Grupo: `{'kind': 'box' | 'pallet', 'children': [...]}`. Os dados de entrada continuam sendo dicionários; você pode convertê-los internamente em objetos.

**Exemplo:** um pallet contendo um item de peso `2`/preço `10` e uma caixa com item de peso `3`/preço `20` retorna `{'weight': 5, 'price': 30}`.

**Aceite:** caixas e pallets aceitam itens ou outros grupos; grupos vazios totalizam zero; peso ou preço negativo em qualquer item e tipos desconhecidos levantam `ValueError`, em qualquer profundidade. O cálculo não modifica a carga e não adiciona peso ou preço da embalagem. Entradas cíclicas ficam fora do exercício.

## 09 — Adicionais combináveis

**Código:** `aurora/d09_extras.py` · **Testes:** `tests/test_d09_extras.py`

**Hoje:** o cálculo só contempla preço base e duas combinações específicas. Acrescentar serviços multiplica os casos a manter.

**Solicitação:** adicionar aviso de recebimento e permitir composição de serviços sem enumerar todas as combinações possíveis.

**Contrato:** `quote(base, extras=())` retorna `{'total': number, 'lines': [(name, amount), ...]}`. Valores fixos: `insurance=5`, `priority=12`, `notification=2`. A primeira linha é sempre `('base', base)`; as seguintes respeitam a ordem solicitada.

**Exemplo:** `quote(20, ('priority', 'insurance', 'notification'))` → `{'total': 39, 'lines': [('base', 20), ('priority', 12), ('insurance', 5), ('notification', 2)]}`.

**Aceite:** serviços individuais e combinações em qualquer ordem; preço base preservado; chamadas independentes. Base negativa, serviço desconhecido ou serviço repetido levantam `ValueError`. Não há percentual, desconto nem cobrança duplicada.

## 10 — Despacho por uma única operação

**Código:** `aurora/d10_dispatch.py` · **Testes:** `tests/test_d10_dispatch.py`

**Hoje:** cada cliente precisa conhecer a ordem das chamadas de estoque, pagamento, etiqueta e coleta, como mostra `manual_dispatch`.

**Solicitação:** disponibilizar uma entrada de negócio que encapsule a coordenação, de modo que novos clientes não precisem conhecer os detalhes dos subsistemas.

**Contrato:** `dispatch(order_id, operations)` deve reservar estoque, cobrar pagamento, emitir etiqueta e agendar coleta, exatamente nessa ordem. Retorna `{'label': 'LABEL-{id}', 'pickup': 'PICKUP-{id}'}`. O objeto `operations` oferece `reserve`, `charge`, `label`, `collect`; o simulador `Operations` registra `(step, order_id)` em `events`.

**Exemplo:** `dispatch('42', Operations())` → `{'label': 'LABEL-42', 'pickup': 'PICKUP-42'}`; eventos `stock`, `payment`, `label`, `collection` para o pedido `42`.

**Aceite:** sucesso coordena cada etapa uma vez; uma falha interrompe o fluxo antes das etapas posteriores e propaga a exceção original. `Operations(fail_at='payment')` permite simular esse cenário. Preserve `manual_dispatch` como cliente antigo. Compensações, estornos, repetição automática e transações distribuídas estão fora desta feature.

## 11 — Catálogo compartilhado de embalagens

**Código:** `aurora/d11_packaging.py` · **Testes:** `tests/test_d11_packaging.py`

**Hoje:** mil caixas idênticas geram mil objetos de especificação. Material e dimensões são repetidos junto aos dados de cada embalagem física.

**Solicitação:** reutilizar especificações imutáveis, conservando os dados individuais de cada embalagem.

**Contrato:** `Warehouse().create(identifier, material, dimensions, position, contents)` retorna objeto com `identifier`, `specification`, `position`, `contents`. A especificação possui `material`, `width`, `height`, `depth`. `dimensions` aceita lista ou tupla de três valores positivos. `specifications_created` conta especificações efetivamente criadas.

**Exemplo:** duas embalagens de `cardboard` com dimensões `(10, 20, 30)` no mesmo armazém referenciam a mesma especificação, mas podem ocupar `A1` e `B1`, contendo itens diferentes.

**Aceite:** mil embalagens iguais criam uma especificação; material e cada dimensão compõem a identidade da especificação; lista e tupla equivalentes reutilizam a mesma entrada; especificações não podem ser alteradas. Identificação, posição e lista de conteúdo continuam individuais; a lista fornecida pelo chamador não pertence à embalagem. Dimensões inválidas levantam `ValueError`. O catálogo é por instância de armazém, sem persistência global; conteúdos são identificadores de itens em texto.

## 12 — Rastreamento com acesso controlado

**Código:** `aurora/d12_tracking.py` · **Testes:** `tests/test_d12_tracking.py`

**Hoje:** o fornecedor é carregado na criação do serviço, todas as consultas chamam a API simulada e o argumento de autorização é ignorado.

**Solicitação:** economizar carregamentos e consultas repetidas sem permitir que o cache contorne a autorização.

**Contrato:** `Tracking(loader).lookup(code, authorized=True)` retorna `{'code': code, 'status': 'in_transit'}`. O carregador é chamável e retorna um fornecedor com `fetch(code)`. `ProviderLoader.loads` e `Provider.calls` permitem observar o trabalho realizado. `Provider.fail_next=True` simula uma única falha com `ConnectionError`.

**Exemplo:** criar `Tracking(loader)` não carrega o fornecedor; duas consultas autorizadas de `'42'` carregam uma vez e chamam `fetch('42')` uma vez.

**Aceite:** verificar autorização antes de inicializar ou consultar o cache; negar com `PermissionError`; carregar no primeiro acesso autorizado e reutilizar o fornecedor. Cache por código e por instância de `Tracking`, somente para sucessos. Falhas propagam e permitem nova tentativa. Alterar o dicionário devolvido não contamina respostas posteriores. Expiração, concorrência e autenticação real ficam fora do exercício.

## Como revisar sua solução

Para cada desafio, escreva um pequeno diagnóstico próprio: qual alteração seria difícil no código original, quais responsabilidades estavam misturadas e como sua solução reduz esse problema. Faça os testes da feature passarem, remova suas marcas de pendência e confirme que os comportamentos anteriores continuam funcionando.

A conclusão do laboratório é uma suíte inteira sem falhas e sem `XFAIL`, acompanhada de código que possa receber novas variantes sem espalhar alterações pelos clientes. Não há gabarito no repositório.
