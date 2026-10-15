# 5.58.2 — Causa do site fora do ar (429) e correção

## Diagnóstico
A página "429 Too Many Requests" é da hospedagem: o servidor fica sem capacidade e passa a recusar requisições, inclusive do painel.

Revisei o tema inteiro e encontrei **dois comportamentos que, juntos, sobrecarregam o banco de dados**. Os dois já existiam antes da 5.58; foi por isso que **voltar para a 5.57.1 também derrubou o site**.

### 1. Consulta pesada para cada código de bateria que não existe na loja (desde a 5.53/5.54)
- Cada página de veículo mostra os códigos de bateria do catálogo (Moura, Heliar, Zetta, Excell, Eletran, Motobatt).
- **Quando um código não existe na loja**, o tema fazia **3 varreduras completas** das tabelas `wp_postmeta` e `wp_posts`:
  - `UPPER(TRIM(...))`;
  - `LIKE '%...%'` no SKU;
  - `LIKE '%...%'` no título.
- Varredura completa não usa índice: o banco lê a tabela inteira a cada vez.
- O resultado "não encontrado" ficava guardado **só 2 minutos**.
- Há mais de 65 mil páginas no sitemap (veículos, anos, cidades). Com Google, Bing e outros robôs visitando essas páginas, isso virava **milhares de varreduras por hora**, sem parar.

### 2. A cada versão nova do tema, todos os caches eram apagados de uma vez
- No primeiro acesso ao painel depois do upload, o tema:
  - limpava todo o cache de página (LiteSpeed, WP Rocket etc.);
  - apagava todos os caches do tema (produtos, lojas, sitemaps);
  - invalidava os 22 sitemaps.
- No minuto seguinte, **todas** as visitas e todos os robôs geravam as páginas do zero ao mesmo tempo, justamente as páginas com as varreduras do item 1.
- **É por isso que cada upload derrubava o site**: o da 5.58.0, a volta para a 5.57.1 e a 5.58.1.

## Correção
1. **Mapa único de SKUs da loja:**
   - 2 consultas leves a cada 12 horas, guardadas em cache, no lugar de 3 varreduras por código;
   - o mapa é refeito automaticamente quando um produto é criado, alterado, excluído ou vai para a lixeira;
   - **resultado:** 1.000 consultas de código, zero consultas ao banco (teste);
   - a regra de correspondência é a mesma: SKU exato, apelidos da tabela, SKU sem hífen/espaço/"MOTOBATT" e código no nome do produto. A polaridade nunca é trocada (M60GD ≠ M60GE).
2. **"Sob consulta" em cache por 1 hora**, como os demais, em vez de 2 minutos. A troca de preço ou produto continua aparecendo na hora, porque salvar um produto limpa o cache.
3. **Nova versão do tema não apaga mais caches.** Só regrava as rotas.
   - O cache de produtos e de sitemaps também deixou de depender da versão do tema; muda só quando o catálogo muda.
   - Limpeza completa agora é manual: Configurações → AWR Validação SEO → "Limpar caches do tema e regravar rotas", fora do horário de pico.
4. **Mantém as proteções da 5.58.1:** sem tarefa agendada nas visitas, pré-busca só no toque e trava de pedidos no navegador.

## Validação
- **Mapa de SKUs:**
  - exato, minúsculas e espaços, MBTX9U-BS, apelido com variação (pai), apelido Excell, nome do produto, polaridade, código inexistente, MBTX9UHD não casa com MBTX9U;
  - 1.000 consultas sem banco;
  - limpeza ao salvar produto.
- **Navegador:**
  - checkout: 76 testes;
  - reserva: 6 testes;
  - página de produto: 76 testes;
  - busca: 3 modelos de card e modo sem servidor;
  - seletor de moto.
- **PHP:** 79 testes de cotação/pedido; 333 buscas iguais.
- **Regressão:** 997 URLs do Search Console sem mudança; sitemap com 65.312 URLs; lint.

## Como instalar
1. **Primeiro, espere o site voltar.** O bloqueio 429 da hospedagem expira sozinho (normalmente de 5 a 30 min). Se não expirar, peça ao suporte da hospedagem para liberar a conta e o seu IP.
2. **Gerenciador de arquivos** da hospedagem, **não** o painel do WordPress, num horário de pouco movimento.
   - Em `wp-content/themes/`, renomeie `awr-baterias` para `awr-baterias-antigo`.
   - Envie este zip e use **Extrair**.
3. **Não** limpe o cache do site logo em seguida. Deixe o cache de página trabalhar e limpe só à noite, se necessário.
4. Se o painel da hospedagem tiver "Limite de requisições / proteção contra bots", confirme que Googlebot e Bingbot estão liberados. Se tiver Cloudflare, ative o "Bot Fight Mode" para robôs que não são de busca.

## Rollback
Pasta `awr-baterias-antigo`.
