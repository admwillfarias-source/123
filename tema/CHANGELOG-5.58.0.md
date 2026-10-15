# 5.58.0 — Busca instantânea e páginas mais leves

## Números (simulação: celular com 4G lento, CPU 4x mais lenta, servidor de 600 ms por requisição)
| Medida | 5.57.1 | 5.58.0 |
|---|---|---|
| Da última tecla ("onix 2018") até a sugestão aparecer | 880 ms | **50 ms** |
| Do toque na sugestão até os cards de bateria | 1.070 ms | **190 ms** |
| Requisições ao servidor ao digitar | 1 a cada pausa na digitação | **0** |
| HTML das páginas de moto (hub, marca e cidade) | 386 KB (75 KB comprimido) | **74 KB (17 KB comprimido)** |

## O que mudou

### 1. Sugestões respondem no próprio navegador
- **Antes:** cada pausa na digitação subia o WordPress inteiro, com plugins e WooCommerce, só para sugerir veículos.
- **Agora:**
  - um índice compacto (`awr-sugest.json`, 59 KB comprimido) é baixado no primeiro toque na busca, ou no ocioso nas páginas com busca;
  - as sugestões saem em cerca de 2 ms por letra, sem servidor.
- **Mesmo resultado do servidor:** a pontuação foi copiada do PHP (sinônimos, erros de digitação, ano, "parcial quando nada casa"). Em 333 buscas de teste, as listas saíram idênticas às do servidor (veículos, ordem, slug e ano).
- **Reserva:** se o índice não carregar, a busca volta a consultar o servidor, como antes.

### 2. Resultado mais rápido
- **Pré-busca:** quando a lista de sugestões para de mudar, o resultado da 1ª sugestão já é pedido; ao encostar ou passar o mouse numa sugestão, o dela também. O toque encontra o resultado pronto ou a caminho.
  - Custo: em média 1 pedido extra ao servidor por busca, quando a pessoa pausa a digitação antes de terminar.
- **Cache no navegador:** resultado guardado por 10 minutos. Voltar ou repetir a busca é imediato.
- **Servidor:**
  - o canal `/awr-busca/` responde já no `init` do WordPress, sem montar a consulta principal nem o roteamento de templates;
  - as respostas de sugestão e de produtos podem ficar 2 minutos no cache do navegador: um preço alterado na loja aparece em até 2 minutos.
- **Digitação:** o intervalo para reagir à digitação caiu de 180 ms para 70 ms quando o índice local está ativo.

### 3. Páginas de moto 5x mais leves
- O seletor Marca > Modelo > Ano embutia um índice de 310 KB no HTML de todas as páginas que mostram o seletor de moto (hub de motos, marcas e cidades).
- Agora o índice vem de um arquivo em cache (`awr-moto.json`), baixado só quando a pessoa usa o seletor.

### 4. Arquivos dos índices
- Gerados no tema e regerados no site por uma tarefa agendada, com o próprio WordPress, em `uploads/awr-busca/`.
- O nome do arquivo leva o hash do conteúdo, para o cache durar 1 ano.
- Regerar na mão: `wp awr indice-busca`.

### 5. Outros
- **Pré-carga no ocioso:** o JS da busca e o índice entram como prefetch depois que a página carrega. Não roda com economia de dados ou rede 2G.
- **Fontes:** Inter e Plus Jakarta Sans (75 KB) saíram do tema. Não eram carregadas por nenhuma página. O zip ficou do mesmo tamanho, porque os dois índices novos entraram no lugar.
- **JS minificado em ASCII puro**, sem risco de acento quebrado se o servidor não informar a codificação.
- **CSS crítico conferido nas páginas principais** (home, veículo, ano, cidade, bairro, marca, categoria, SKU, produto, blog, moto, caminhão, estacionária e busca), a 390 px e a 1440 px:
  - 437 das 464 regras são usadas; ele já estava enxuto e não foi alterado;
  - o que ainda pesa no carregamento é o servidor (WordPress, plugins e hospedagem).

## Validação
- **Busca:**
  - 333 buscas iguais no navegador e no servidor;
  - testes da busca (3 modelos de card e modo sem servidor) passando;
  - seletor de moto carrega o índice só quando usado (Honda: 576 modelos).
- **Checkout:** 76 testes de navegador, 6 da reserva e 79 testes PHP, todos passando.
- **Página de produto:** 76 testes passando.
- **Regressão:**
  - as 997 URLs do Search Console estão iguais;
  - sitemap com 65.312 URLs;
  - lint de PHP e JS.

## Depois de instalar
- Limpe o cache do site e do Cloudflare.
- Em até 1 minuto (ou ao rodar `wp awr indice-busca`), os índices são regerados pelo WordPress do site em `uploads/awr-busca/`.
- Se o cron do WordPress estiver desligado, o tema segue usando os índices que vêm no zip, que já funcionam.

## Rollback
Reinstale awr-baterias-theme-v5.57.1.zip.
