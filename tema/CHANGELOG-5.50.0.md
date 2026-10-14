# 5.50.0 — Correção urgente: páginas de veículo + ano de volta ao sitemap

## Por que
O export do Search Console (3 meses, até 13/10/2026) mostra que as páginas /baterias/{marca}/{modelo}/{ano}/ são o tipo de página que mais traz tráfego: 572 páginas, 3.353 cliques (31% do site) e 311 mil impressões. A regra da 5.49.0 deixava no sitemap só os anos dos modelos populares e tirou 455 dessas páginas, somando 2.619 cliques. As páginas continuavam indexáveis, mas sair do sitemap atrasa o rastreamento.

## O que mudou
- Volta a regra da 5.48.0: todo ano com bateria compatível entra no sitemap (awr_sitemap_inclui_ano retorna true; o filtro awr_sitemap_veiculo_ano continua disponível).
- assets/data/indexaveis.json → paths_ano com as 572 URLs de ano do export. Essas URLs entram mesmo fora da faixa de 22 anos, desde que tenham bateria compatível (ex.: /baterias/honda/civic/2000/).
- Continua a velocidade da 5.49.0: arquivos pré-gerados e lista de veículos em ~0,1 s.

## Validação (simulador)
- 48.215 URLs no sitemap (5.48.0: 47.989). Nenhuma URL saiu.
- Entraram 226: anos de modelos com nome numérico (Peugeot 206/208, Agrale, Fiat 500…), corrigidos na 5.49.0, e o Civic 2000.
- 571 das 572 URLs de ano do Search Console estão no sitemap. A que ficou de fora usa o slug antigo "mercedes".
- Auditoria de 4.358 URLs (as 226 novas e amostras de todas as seções): 0 problemas.
- xmllint: todos os 19 arquivos válidos.

## Rollback
Reinstale awr-baterias-theme-v5.48.0.zip e apague wp-content/uploads/awr-sitemaps/. Não volte para a 5.49.0.
