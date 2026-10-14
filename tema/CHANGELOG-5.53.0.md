# 5.53.0 — Preço das baterias de moto Motobatt pelo SKU do WooCommerce

## Correção do que foi dito na 5.52.0
O tema já buscava o preço no WooCommerce pelo SKU, e desde a 5.52.0 os códigos Motobatt entravam nessa busca. A frase "nenhum código Motobatt está na loja" se baseou só na tabela de preços interna (inc/tabela-baterias.php), não no WooCommerce. Se o produto estiver cadastrado com o SKU exatamente igual ao código (ex.: MBTX9U), o preço já aparecia.

## O que mudou
- **Busca tolerante para códigos Motobatt** (inc/woo.php → awr_lookup_motobatt_id). Quando o SKU exato não existe, a busca tenta:
  1. o SKU igual ignorando hífen, espaço, ponto, a palavra "MOTOBATT" e o sufixo "-BS" (bateria com kit de ácido): MBTX9U encontra "MBTX9U-BS" e "MOTOBATT MBTX9U";
  2. o código no nome do produto, como palavra inteira: "Bateria Motobatt MBTZ10S 8,6Ah" encontra MBTZ10S.
  - Nunca confunde códigos parecidos: MBTX12U não pega MBTX12UHD, MBTX9U não pega MBTX9UHD.
  - Só vale para códigos Motobatt (MB…, ML…, MPL…, MTX…, MTZ…). As outras marcas continuam com a busca de antes.
- **Lítio:** os códigos Motobatt de lítio (MLX4U-HP, MPLX14AU-HP…) também buscam preço na loja.
- **Página da moto:** quando o produto é encontrado, mostra o card com preço, Pix e 10x, e a meta description diz "a partir de R$ X". Sem produto, continua pedindo o preço no WhatsApp.
- **Motos sem páginas de ano** (anteriores a 2004): os produtos e preços aparecem na própria página do modelo.
- **Novo painel Configurações → AWR Motobatt:** lista os 53 códigos Motobatt do catálogo (43 AGM e 10 de lítio), com quantas motos usam cada um, se o produto foi encontrado na loja, o SKU cadastrado e o preço.

## Validação (simulador)
- **Busca:** 9 casos testados (SKU exato, "-BS", "MOTOBATT …", código só no nome, código parecido, código inexistente, Moura sem mudança): todos certos.
- **Ponta a ponta:** a Aprilia 125 Mojito 2005 (MBTX9U), com o produto "MBTX9U-BS" na loja, mostra o card de R$ 449,90, e a descrição diz "a partir de R$ 450".
- **Regressão:** as 997 URLs do Search Console se comportam igual à 5.52.0. Sitemap com 65.312 URLs, gerado em 0,44 s. Todas as descrições de modelo têm entre 70 e 160 caracteres.

## Depois de instalar
Abra Configurações → AWR Motobatt e cadastre na loja os códigos marcados como "não encontrado", com o código no campo SKU. Comece pelos que atendem mais motos: MBTX20U (863), MBTX14AU (354), MBTX30U (305), MBTX9U (289), MBTX12U (289). O cache de produtos se renova em até 1 hora.

## Rollback
Reinstale awr-baterias-theme-v5.52.0.zip.
