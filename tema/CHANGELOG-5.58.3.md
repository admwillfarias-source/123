# 5.58.3 — Busca volta a mostrar os produtos do WooCommerce

## Problema
Com a 5.58.2 a busca mostrava os códigos de bateria, mas sem o produto da loja (nome, foto, preço): tudo aparecia como "sob consulta".

## Causa
O mapa de SKUs da 5.58.2, criado para acabar com as varreduras pesadas do banco:
- **Mapa vazio preso no cache:** era montado uma vez e guardado por 12 h. Montado logo depois da instalação, com o banco ainda sobrecarregado, as consultas voltaram vazias, e esse **mapa vazio ficou no cache**.
- **Busca exata fora do índice do WooCommerce:** a busca exata passou a depender só desse mapa e não usava mais o índice do WooCommerce (`wc_get_product_id_by_sku`).
- **Resultado sem produto guardado por mais tempo:** pacotes "sob consulta" passaram a ficar 1 h, e o navegador guardava o resultado ruim por 10 min.

## Correção
1. **Busca exata de novo pelo índice do WooCommerce** (`wc_get_product_id_by_sku`), como até a 5.57.1. É rápida e não varre tabela.
2. **O mapa só cobre os casos tolerantes:** SKU com hífen, espaço ou "MOTOBATT" e código no nome do produto.
3. **O mapa nunca fica vazio por 12 h:** com erro de banco ou sem SKUs, fica no máximo 5 min. Usa uma chave nova, o que descarta o mapa ruim que estiver no site.
4. **Pacotes de produtos:**
   - chave nova, o que descarta os pacotes ruins;
   - completo: 1 h;
   - com algum código sem produto: 10 min.
5. **Navegador:**
   - só guarda o resultado quando há ao menos uma bateria com preço;
   - chave nova, para quem ficou com o resultado ruim aberto.
6. **Botão novo:** Configurações → AWR Busca → **"Limpar cache de produtos"**.
7. **Continua da 5.58.2:**
   - nenhuma varredura completa do banco por código;
   - nova versão não apaga caches.

## Validação
- **Mapa:**
  - exato, tolerante (MBTX9U-BS), apelido com variação, nome do produto, polaridade e código inexistente;
  - 1.000 buscas sem consultar o banco;
  - com o banco falhando: sem produto, sem quebrar, e o mapa guardado só 5 min.
- **Navegador:**
  - resultado só "sob consulta" não é guardado; resultado com preço é guardado;
  - testes da busca, checkout (76), reserva (6), página de produto (76) e seletor de moto.
- **PHP e busca:** 79 testes de cotação/pedido; 333 buscas iguais.
- **Regressão:** 997 URLs do Search Console sem mudança, sitemap e lint.

## Instalar
1. Instale pelo Gerenciador de arquivos:
   - em `wp-content/themes/`, renomeie `awr-baterias` para `awr-baterias-antigo`;
   - envie este zip e use **Extrair**.
2. Logado como administrador, abra `https://awrbaterias.com.br/?awr_flush_produtos=1` (ou use o botão em Configurações → AWR Busca).
3. **Não** limpe o cache de página.
