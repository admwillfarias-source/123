# 5.55.0 — Jetpack Stats volta a contar as visitas

## Por que o Jetpack não contava
Duas regras do tema, criadas para deixar o celular mais rápido, bloqueavam a contagem:
1. **Desde a 5.11.0** (inc/perf-plugins.php), o script `jetpack-stats` era **removido em todas as páginas fora da loja e do checkout**: home, veículos, cidades, marcas, blog etc.
2. **Desde a 3.78.0** (inc/assets.php), o adiamento de scripts de medição trocava a tag inteira do Jetpack e **apagava o bloco inline com os dados da visita** (`_stq.push(["view", …])`). Por isso, até nas páginas da loja o arquivo carregava, mas a visita não era registrada.

## O que mudou
- O `jetpack-stats` saiu das duas listas.
- **Novo carregamento adiado** (inc/perf-plugins.php), em todas as páginas do site:
  - o bloco inline do Jetpack fica intacto;
  - só o arquivo `stats.wp.com/e-AAAASS.js` é pedido depois que a página termina de carregar (com o navegador ocioso, até 1,5 s), ou antes disso, no primeiro toque, rolagem ou tecla;
  - é pedido uma única vez, então a abertura da página e o PageSpeed não pioram.
- **Filtro `awr_jetpack_stats_modo`:** `adiado` (padrão), `normal` (como o Jetpack manda) ou `desligado`.

## Validação
- **Troca da tag** (formato real do Jetpack): o bloco inline com "view" fica intacto, a tag externa vira o carregador e os outros scripts continuam adiados como antes.
- **Navegador:**
  - sem interação, `stats.wp.com` é pedido 1 vez, logo após o load;
  - com um toque antes, é pedido na hora (310 ms);
  - nos dois casos `_stq` mantém "view" e "clickTrackerInit".
- **Regressão:** as 997 URLs do Search Console se comportam igual; lint ok.

## Importante
- A contagem volta **a partir da instalação**. O período anterior não pode ser recuperado no Jetpack; para ele, use o GA4.
- Teste em **janela anônima**: por padrão, o Jetpack não conta visitas de usuário logado.
- Limpe o cache do site e do Cloudflare. As páginas em cache (até 4 h) ainda estão sem o contador.

## Rollback
Reinstale awr-baterias-theme-v5.54.0.zip.
