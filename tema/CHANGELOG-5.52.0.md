# 5.52.0 — Catálogo de busca atualizado + páginas de carro, moto e caminhão com SEO completo

## Análise das planilhas
| Planilha | Resultado |
|---|---|
| site_busca_baterias.xlsx (1.616 linhas úteis e 994 vazias) | Subconjunto do site. Os 1.404 modelos já estavam no catálogo, que é mais completo (1.790 modelos). |
| HELIAR_Tabelas_Aplicacoes_2025.xlsx (1.798 linhas, algumas com colunas deslocadas) | 26 modelos que faltavam foram adicionados: tratores John Deere, caminhões Mercedes Atron/Arocs, MF 9150/9170, Agrale 4100 e motos grandes (Honda CB/CBR/VFR/VTR, Suzuki GSX, Yamaha XJR, BMW R 1250). O código HD75LD da Heliar 2025 não está na tabela de preços; o site mantém o H75LD. |
| Catalogo Motobatt AGM 2023-2025 (4.763 linhas, mercado americano) | **Importado inteiro**, por decisão sua. Foram 4.365 variantes novas, e outras 342 foram mescladas em modelos que já existiam. 56 linhas sem código ficaram de fora. |

## Catálogo (assets/data/batteries.json + assets/data-php/batteries.php)
- **Tamanho:** de 2.011 para 6.365 itens; 5.940 modelos e 148 marcas.
- **Códigos corrigidos (200):**
  - sujeira removida: "HTX14 12", "HTZ10S-BS 8,6", "NONE";
  - "HE60HD / H65HD" separado em Heliar e H65;
  - Moura MA70LD que estava na coluna Heliar dos BMW X1/X2;
  - Motobatt que estava na coluna Moura e Moura moto que estava na coluna Excell, nas motos.
- **Modelos falsos removidos (cópias por autopreenchimento de planilha), com 301 para o modelo verdadeiro:**
  - BMW R 1201 → R 1200 GS
  - BMW R 1202 → R 1200 GS Adventure
  - BMW R 1203 → R 1250 GS
  - BMW K 1201 → K 1200 RS
  - BMW K 1202 → K 1200 S
  - BMW S 1001 → S 1000 RR
- **Marcas duplicadas unificadas, com 301:**
  - JOHN → JOHN DEERE
  - NEW → NEW HOLLAND
  - HARLEY → HARLEY DAVIDSON
  - "AGCO / MASSEY FERGUSON" → AGCO
  - AGRALE TRATORES → AGRALE
  - O mapa fica em assets/data/veiculos-redirects.json.
- **Motos Kawasaki com código Yuasa (YTX9-BS):** não eram reconhecidas como moto e agora são.
- **Veículo × cidade:** os itens só com código Motobatt não geram essas páginas. Sem essa regra, seriam cerca de 67 mil páginas de cidade sem produto; o total ficou em 30.371 (eram 30.051).

## SEO das páginas de veículo
- **Tipo do veículo** (awr_vehicle_tipo) por modelo: carro (1.088), moto (3.558), quadriciclo/UTV (709), jet ski (232) e caminhão/máquina (353).
- **H1 com o tipo e o nome em caixa normal:**
  - "Bateria para moto Honda CG 160 Titan 2022"
  - "Bateria para caminhão e máquina Ford Cargo 1319"
  - "Bateria para Hyundai Creta 2.0 2020"
  - Os titles das páginas com tráfego não mudaram.
- **H2 e H3:**
  - Marca: H2 "Modelos {Marca}" com a lista visível e um H3 por família ou letra (Hyundai: 13 H3; Honda: 96).
  - Modelo: H2 "Escolha o ano" e um H3 por década.
  - Ano: os nomes dos produtos viraram H3, com o mesmo visual (16px, peso 800 e mesma altura, conferido no navegador).
  - Família: um H3 por versão.
- **Meta description por tipo:**
  - Moto, quadriciclo, jet ski e caminhão não dizem mais "Carro não liga?".
  - Motos sem preço cadastrado (Motobatt) pedem "preço no WhatsApp" em vez de prometer "preço no Pix".
  - A segunda frase só entra se couber inteira.
  - Todas as 5.940 descrições de modelo têm entre 70 e 160 caracteres.
- **Title de nome longo:** o ano fica sempre no fim. Titles repetidos no sitemap de veículos caíram de 184 (1.208 URLs) para 73 (146 URLs).
- **FAQ "Em quanto tempo vocês entregam?":** a resposta (visível e no JSON-LD) varia por tipo; por exemplo, caminhão explica 24V com duas baterias.

## Validação (simulador)
- **URLs do Search Console (997):** comportamento idêntico ao da 5.51.0 (756 indexáveis, mesmas exceções).
- **Sitemap:** 65.294 URLs em 22 arquivos, geradas em 0,52 s; xmllint ok.
  - Entraram 18.030 URLs.
  - Saíram 1.190, todas com 301; os 1.185 destinos respondem 200, indexáveis e com canonical própria.
- **Amostra de 1.254 URLs novas** (1 a cada 15, mais as 52 marcas novas): 0 problemas.
- **Celular (390px):** nenhuma página rola na horizontal.

## Pendências (não alteradas)
- 3 URLs do Search Console já davam 404 antes desta versão: /baterias-para/chevrolet-omega/ivoti/, /baterias-para/ford-maverick-exceto-hibrido/ivoti/ e /baterias/mercedes/benz-e-class-e350/2010/.
  - As URLs /bateria-estacionaria/{uf}/{cidade}/ vêm do plugin de estacionárias e precisam ser conferidas no site real.
- Nenhum código Motobatt está na tabela de preços nem no WooCommerce: essas páginas pedem cotação no WhatsApp. Cadastre os produtos Motobatt para mostrar preço.
- A Heliar 2025 usa o código HD75LD; a tabela de preços do site ainda usa H75LD.
- O catálogo Motobatt é do mercado americano: inclui jet ski, quadriciclo e modelos não vendidos no Brasil. Acompanhe a cobertura no Search Console e, se o Google marcar muitas páginas como "rastreada, não indexada", reduza o escopo.

## Depois de instalar
1. Abra o painel do WordPress uma vez, para as rotas serem regravadas.
2. Regenere o sitemap com `wp awr sitemap` ou aguarde o cron.
3. Reenvie awr-sitemap.xml no Search Console.

## Rollback
Reinstale awr-baterias-theme-v5.51.0.zip. As URLs das marcas antigas voltam a abrir e as novas deixam de existir.
