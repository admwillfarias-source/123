# 5.59.0 — Busca sem depender do servidor, menos requisições e menos memória

## O que estava acontecendo

### 1. A busca mostrava as baterias sem o produto da loja
Aparecia "Bateria Moura M60GD · Preço sob consulta", sem foto e sem preço.
- **Não era erro na ligação código → produto.** Ela é a mesma da 5.57.1, quando funcionava, comparada linha a linha.
- **Era o modo reserva da busca.** Quando o pedido ao servidor falha, o navegador mostra os códigos de um índice reserva, que não tem nome do produto, foto nem preço. O pedido falhava por três motivos:
  - 429 ou 503 da hospedagem;
  - falta de memória;
  - resposta acima de 6 s.

### 2. O tema multiplicava as requisições quando o servidor ficava lento
Isso existia desde a 5.49.
- Cada busca tentava 3 caminhos em sequência e depois repetia tudo: **até 6 processos PHP por busca**.
- O navegador desistia depois de 6 s, mas o servidor continuava executando cada processo até o fim.

Medido no simulador, com o servidor em 429:

| Versão | Requisições por busca |
|---|---|
| 5.58.3 | 6 |
| 5.59.0 | 1, e depois pausa |

Com o servidor demorando 11 s:

| Versão | Requisições por busca | Espera até o resultado sem preço |
|---|---|---|
| 5.58.3 | 6 | 37 s |
| 5.59.0 | 1 | 10 s |

### 3. "Acima da memória" na HostGator
- **O limite é da conta inteira:** a soma de todos os processos PHP rodando ao mesmo tempo. Cada processo carrega WordPress + WooCommerce + plugins (60–120 MB).
- **O tema sozinho é leve:** cerca de 13 MB por página; o sitemap de 65 mil URLs tem pico de 34 MB.
- **O que estourava era a quantidade de processos simultâneos:**
  - a cascata de 6 tentativas por busca;
  - robôs visitando as páginas de veículo, e cada uma consultava o WooCommerce;
  - robôs de ferramentas de SEO, que não trazem vendas;
  - até a 5.58.2, varreduras do banco (já corrigido).

## O que mudou

### Vitrine de produtos em arquivo (inc/vitrine.php)
- **O que é:** o catálogo tem só 182 códigos de bateria. O tema grava o produto de cada um num arquivo `wp-content/uploads/awr-busca/vitrine.json` (cerca de 75 KB), com nome, foto, preço e estoque.
- **Quando é regerado:**
  - 1 minuto depois de qualquer alteração de produto, preço ou estoque;
  - duas vezes ao dia;
  - ao atualizar o tema;
  - pelo botão no painel.
- **Arquivo vazio nunca substitui um bom:** se nenhum produto for encontrado (banco fora do ar), o arquivo anterior é mantido.
- **Uso no servidor:** as páginas de veículo também usam a vitrine. **Zero consultas ao WooCommerce** por página quando ela existe.
- **O valor cobrado no pedido continua vindo do WooCommerce.**

### Busca montada no navegador
- **Novo índice veículo → códigos** (`assets/js/awr-vskus.json`).
- Do digitar ao resultado com preço: **nenhuma requisição PHP** (antes, 1 ou mais).
- **Resultado idêntico ao do servidor:** 11.878 buscas comparadas, 0 diferenças.
- **Sugestões:** as primeiras letras esperam o índice local em vez de ir ao servidor.
- **O servidor só é usado quando:**
  - a vitrine ainda não existe;
  - a vitrine tem mais de 26 h;
  - a busca é por amperagem.

### Fim da cascata
- **429, 5xx e tempo esgotado não tentam outro caminho.**
- **Depois de um 429/503, a aba fica 60 s sem chamar o servidor.** Vale o `Retry-After`, se vier.
- **Tempo limite:** de 6 s para 10 s.

### Robôs
- **robots.txt pede para não rastrear:** AhrefsBot, SemrushBot, MJ12bot, DotBot, BLEXBot, DataForSeoBot, PetalBot, Bytespider, SeekportBot, Barkrowler, serpstatbot, MegaIndex, ImagesiftBot.
- **Continuam liberados:** Google (inclusive Storebot), Bing, Apple e buscas de IA. A indexação não muda.
- **Bloqueio opcional no .htaccess:**
  - fica no painel e vem desligado;
  - responde 403 sem carregar o WordPress, para quem ignora o robots.txt;
  - guarda cópia em `.htaccess-awr-backup`.

### Página de produto
- **A cotação de entrega de quem já tem CEP salvo fica guardada 10 min.** Antes, era 1 requisição a cada visita.
- **429/5xx não tentam um segundo caminho.**

### Atualização do tema
- **Ao entrar no painel pela primeira vez depois de instalar,** o tema gera a vitrine e apaga só os pacotes antigos de produto (`awr_prods_*`).
- **O cache de página não é limpo.**

## Instalação
1. **Gerenciador de arquivos da HostGator:** envie o zip para `wp-content/themes/`, extraia substituindo a pasta `awr-baterias` e apague o zip.
2. **Entre no painel do WordPress.** Na primeira visita, a vitrine é gerada (alguns segundos).
3. **Configurações → AWR Busca:** confira "**Vitrine: X de 182 códigos com produto na loja**".
   - A lista "Códigos sem produto na loja" mostra o que aparece como "sob consulta".
   - Se a vitrine não tiver sido gerada, clique em **Regerar vitrine agora**.
4. **Opcional:** no mesmo painel, **Ligar bloqueio no .htaccess**.
5. **Não é preciso limpar o cache de página.**

## Testes
- **Busca, navegador × PHP:**
  - 11.878 buscas idênticas, todos os veículos e anos;
  - 52 buscas por código idênticas;
  - PHP com vitrine × PHP sem vitrine: 0 diferenças e 0 consultas ao banco com vitrine.
- **Navegador (Playwright):**
  - com vitrine: 0 requisições PHP, resultado com preço em menos de 0,1 s;
  - sem vitrine: 1 requisição;
  - 429: 1 requisição e depois pausa.
- **Regressões:**
  - checkout 76/76;
  - checkout antigo 6/6;
  - produto 76/76;
  - consentimento 8/8;
  - seletor de moto;
  - busca e2e;
  - cotação/pedido 79/79;
  - mapa de SKUs 13/13 + 2/2;
  - sugestões 333/333;
  - 997 URLs do Search Console sem diferença;
  - sitemap com 65.312 URLs;
  - lint PHP/JS.
