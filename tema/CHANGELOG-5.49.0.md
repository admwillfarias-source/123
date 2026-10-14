# 5.49.0 — Sitemap rápido e enxuto

## Problema (Search Console: awr-sitemap.xml com 0 URLs lidas e tempo esgotado)
O índice /awr-sitemap.xml contava as URLs de veículos a cada acesso, sem cache. Montar essa lista levava 61–65 s (medido), porque awr_vehicle_variants() varria a base inteira de baterias para cada modelo e cada ano. O Google desistia antes da resposta.

## O que mudou
- **Busca de veículos (inc/search.php):** novo awr_vehicle_index() (marca → modelo → itens), montado uma vez por requisição. A lista de veículos caiu de 61,6 s para 0,09 s, e as páginas de veículo também ficam mais leves.
  - Também corrige um bug antigo: modelos de nome numérico (Fiat 500, Peugeot 206, Agrale 1600…) não tinham variantes nem anos no sitemap.
- **Sitemaps gerados antes (inc/seo.php):** todos os arquivos ficam prontos em wp-content/uploads/awr-sitemaps/, com um manifest.json. O acesso público só lê o arquivo (índice em ~1 ms no teste).
  - Geração automática: WP-Cron duas vezes ao dia e quando muda a versão dos dados, o domínio canônico ou o modo de indexação.
  - Geração manual: comando `wp awr sitemap`.
  - Se a pasta não puder ser gravada, cada arquivo é gerado na hora (~0,1 s) e guardado em cache temporário (transient).
- **5.000 URLs por arquivo** (antes 1.000). São 16 arquivos em vez de cerca de 55. Páginas antigas (ex.: veiculos-12) respondem com um urlset vazio e status 200, sem 404.
- **Cabeçalhos:** sai o nocache_headers. Entram Cache-Control public com s-maxage=86400, Last-Modified e ETag (com resposta 304), e lastmod no índice. Continua sem noindex no sitemap (regra da v5.12.0).
- **Veículo + ano no sitemap:** só entram os modelos populares (awr_idx_populares_set) e as URLs listadas em `paths_ano` do assets/data/indexaveis.json, a preencher com o export do Search Console. Filtro: awr_sitemap_veiculo_ano.
  - **As demais páginas continuam no ar e indexáveis** (status 200, sem noindex, canonical própria). Só deixam de ser listadas no sitemap.

## Antes x depois
| | 5.48.0 | 5.49.0 |
|---|---|---|
| URLs no sitemap | 47.988 | 33.984 |
| URLs de veículo | 16.535 | 2.531 |
| Arquivos | ~55 | 16 |
| Tempo do índice | 61–65 s | 0,001 s (arquivo) / 0,11 s (sem arquivo) |
| Geração completa | — | 0,15 s (sem produtos Woo; no site real, alguns segundos) |

Validação:
- Nenhuma URL nova entrou. Saíram 14.004 URLs, todas de veículo + ano.
- Auditoria de 4.935 URLs do sitemap novo (todas as seções, mais 1 a cada 30 de veículo + cidade): 0 com noindex, redirecionamento, 404 ou canonical de outra URL.
- Amostra de 350 URLs que saíram: todas 200, indexáveis e com canonical própria.
- xmllint: todos os arquivos válidos.

## Depois de instalar
1. Abra https://awrbaterias.com.br/awr-sitemap.xml. A primeira geração roda sozinha. Se tiver WP-CLI, `wp awr sitemap` gera na hora.
2. Cloudflare → Caching → Cache Rules: crie uma regra para "URI Path" que comece com `/awr-sitemap`, com "Eligible for cache" e Edge TTL "Use cache-control header". Sem essa regra, o Cloudflare não guarda XML.
3. Search Console → Sitemaps:
   - Remova sitemap.xml, sitemap.rss e /feed/.
   - Reenvie awr-sitemap.xml e bateria-estacionaria-sitemap.xml.
4. bateria-estacionaria-sitemap.xml (115 URLs em vez de 820) vem do plugin de estacionárias, não do tema. Confira se ele está na v1.6.0 e regenere o sitemap no próprio plugin.

## Rollback
Reinstale awr-baterias-theme-v5.48.0.zip e apague a pasta wp-content/uploads/awr-sitemaps/.
