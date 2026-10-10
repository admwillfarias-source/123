# 5.46.0 — Auditoria e correções de SEO

## Promessa de prazo correta nas cidades sem entrega rápida (crítico)
Alvorada, Viamão, Sapiranga, Estância Velha, Nova Santa Rita (entrega no mesmo dia, pedidos até 17h) e Eldorado do Sul e Guaíba (dia seguinte) tinham `tempoEntregaMin = 0`.
- 12.320 páginas veículo × cidade mostravam no Google "Entrega em 0 min" / "instalação grátis em até 0 min".
- 28 páginas marca × cidade e 33 de bairro prometiam "35 min" / "Troca no Local Hoje".
- Novo helper `awr_city_prazo()` (inc/city-delivery.php) usado em inc/vehicle-city.php, inc/seo.php (bairro, marca × cidade, FAQ e schema da cidade), routes/marca_cidade.php, routes/bairro.php, routes/hub_bairros.php e routes/hub_cidades.php ("Entrega em até 0 minutos" no hub).
- Nas cidades com entrega rápida o texto gerado é idêntico ao anterior (verificado por comparação).

## Títulos cortados no meio
`awr_seo_trim()` descarta o complemento depois de " | " quando o título não cabe, em vez de cortar no meio ("| Troca no", "... em"), e remove preposições soltas no fim. Veículo × cidade sempre mantém a cidade (`awr_vc_titulo_base()`). Na amostra auditada, títulos quebrados caíram de ~600 para 0.

## Sitemaps
- SKUs com espaço/vírgula/barra ("HTX14 12", "MA8,6E", "HE60HD / H65HD") geravam URL inválida no sitemap, com canonical diferente e página "SKU não encontrado". Novo par `awr_sku_slug()` / `awr_sku_from_slug()`: URL limpa (/bateria/htx14-12/) e página resolvida. SKUs comuns mantêm a URL de sempre.
- 110 URLs /baterias/{marca}/{modelo}/{ano}/ que respondem 301 para o modelo saíram do sitemap.
- Nova seção `awr-sitemap-produtos.xml`: produtos publicados do WooCommerce fora da tabela de aplicação (estacionárias, moto, acessórios), com a mesma URL do canonical do produto.

## Dados estruturados
- Product: `areaServed` movido para a Offer (não existe em Product); `returnFees: FreeReturn` na política de devolução (CDC art. 49).
- LocalBusiness: `image` e `priceRange`.
- og:image: o arquivo assets/img/og-awr.jpg não existia (404 em todo compartilhamento). Criado 1200×630.

## Produtos
Título e H1 do SKU com amperagem também para SKUs com prefixo de letras (M60GD → "Bateria Moura 60Ah M60GD"). Não altera busca nem hubs de amperagem.

## Estacionárias — páginas comerciais novas
/baterias-estacionarias/nobreak-e-ups/, /alarme-e-seguranca/, /energia-solar/, /condominios-e-empresas/, /60ah/, /150ah/, /220ah/ — texto, FAQ (FAQPage), tabela de modelos reais, produtos da loja e CTA próprios; linkadas a partir do hub estacionário e dos guias do blog sobre nobreak. 70Ah e 100Ah não foram criadas: não há modelo no catálogo.
Após instalar: salvar Configurações → Links permanentes uma vez.

## GA4
Evento padrão `purchase` (transaction_id, value, currency, items) quando o pedido é criado no WooCommerce pelo checkout do tema. Pedido via WhatsApp continua como lead.

## Sem mudança
Nenhum canonical mudou. Robots mudou só nos 4 SKUs que agora existem (noindex → index). URLs estratégicas, checkout, formulários e integrações preservados.

## Rollback
1. Reinstalar awr-baterias-theme-v5.45.0.zip (Aparência → Temas → Enviar → Substituir).
2. Configurações → Links permanentes → Salvar (remove a rota das páginas estacionárias novas).
3. Limpar cache do plugin/CDN. Os transients do sitemap expiram em 12 h ou mudam de chave com a versão.
