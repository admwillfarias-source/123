# 5.51.0 — Páginas de venda guiadas pelo Search Console

Base: export do Search Console (3 meses, até 13/10/2026: 10,7 mil cliques, 1,2 milhão de impressões). Página nova só existe quando há dado real por trás. Nenhuma URL com tráfego mudou de endereço, canonical ou indexação.

## Páginas novas (239 URLs no sitemap)

### 1. Família de modelo — /baterias/{marca}/{familia}/ (179 páginas)
- **Evidência:** buscas sem versão ficavam nas posições 8 a 11 e caíam em páginas de uma versão + ano.
  - "bateria hb20 1.0": 532 impressões, posição 11,3
  - "bateria kwid": 425 impressões, posição 11
  - "bateria creta": 392 impressões, posição 9,5
  - "bateria peugeot 208": 453 impressões
  - "bateria nissan kicks": 422 impressões
  - "bateria renegade start stop": 592 impressões
- **Exemplos:** /baterias/hyundai/creta/, /baterias/hyundai/hb20/ (13 versões), /baterias/jeep/renegade/, /baterias/volkswagen/t-cross/, /baterias/chevrolet/onix/.
- **Conteúdo, todo montado do catálogo:**
  - tabela versão × anos × bateria (Moura, Heliar, Zetta, Excell) × amperagem × tipo (AGM, EFB, start-stop);
  - produtos;
  - versões e anos;
  - FAQ com as respostas da tabela;
  - botão "Pedir" por versão.
- **Schema:** BreadcrumbList, FAQPage e ItemList.
- **Regras:**
  - Só famílias com 2 ou mais versões e pelo menos 2 linhas diferentes na tabela.
  - Quando o slug da família já é uma página de versão (Kwid, Kicks, 208…), não há URL nova; a página existente ganha o bloco "Todas as versões".
- Toda página de versão e de ano ganhou o bloco "Todas as versões do {modelo}", com link para a família (link interno).

### 2. /baterias-carros-eletricos-e-hibridos/ (bateria auxiliar 12V)
- **Evidência:** /baterias/peugeot/e-expert-eletrico/2025/ é a página com mais cliques depois da inicial (176 cliques, posição 3,9). Kwid E-Tech teve 3.625 impressões e "bateria fusion hybrid" 1.065 impressões.
- **Conteúdo:** 49 modelos elétricos e híbridos do catálogo, com a bateria 12V de cada um, explicação e FAQ.

### 3. Marca × amperagem — /marca/{marca}/{n}ah/ (56 páginas)
- **Evidência:**
  - "bateria heliar 60 amperes": 563 impressões
  - "zetta 50ah": 471 impressões
  - "zetta 70 amperes": 452 impressões
  - "moura 180 amperes": 419 impressões
  - "zetta 180 amperes": 414 impressões
  - "eletran 60ah": 933 impressões
  - "heliar 150": 249 impressões
- **Conteúdo:** só combinações que existem na tabela oficial (inc/tabela-baterias.php):
  - modelos com CCA, garantia e preço à vista;
  - carros compatíveis;
  - comparação com as outras marcas na mesma amperagem;
  - FAQ.
- No celular, a tabela vira cartões com preço e botão visíveis.
- A tabela oficial cadastra o HELIAR EFB72PD com ah=60. A página usa o número do nome do modelo (72).

### 4. /marca/eletran/
- **Evidência:** "bateria eletran" + "eletran 60ah" somam cerca de 1.550 impressões; o produto Eletran 60APD tem 5.443 impressões.
- **Conteúdo:** só fatos da tabela oficial (60Ah, 450 A, 12 meses).
- A marca foi adicionada em assets/data/marcas.json e em assets/data-php/marcas.php, mantendo as demais marcas idênticas.

### 5. /baterias-grande-porto-alegre/
- As 16 cidades de entrega local, com o prazo real de cada uma (awr_city_prazo: 35 ou 40 min, mesmo dia, dia seguinte) e a loja que atende.
- Inclui as zonas de Porto Alegre.

### 6. /entrega-por-transportadora/
- As 120 cidades atendidas por envio (RS 45, SC 25, PR 25, SP 25), agrupadas por estado.
- Explica como funciona, prazo, frete por CEP e pagamento, com os mesmos textos que as páginas de cidade de envio já usam.
- Essas páginas agora têm breadcrumb apontando para cá.

## Reforço de páginas existentes
- **/baterias-em/porto-alegre/:** ganhou a tabela "Preço de bateria em Porto Alegre por marca e amperagem", com link para cada página marca × amperagem, e os links das 5 zonas de Porto Alegre.
- **Páginas das cidades de entrega local:** ganharam link para o hub da Grande Porto Alegre.
- **/baterias-de-carro/:** ganhou a mesma tabela de preço por marca e amperagem. O title continua o da lista editorial (inc/seo-lote.php).

## Validação (simulador)
- **Sitemap:** 48.454 URLs. Nenhuma saiu e entraram as 239 novas, sem duplicadas. Geração completa em 0,29 s; xmllint ok nos 19 arquivos.
- **Auditoria:** 2.839 URLs (as 239 novas e amostras de todas as seções). 0 problemas: todas com status 200, indexáveis e canonical própria.
- **Titles das páginas novas:** nenhum duplicado e nenhum com title acima de 62 caracteres ou descrição acima de 160.
- **Família:** as 196 candidatas renderizaram sem erro de PHP; 179 passaram na regra de conteúdo.
- **Celular (390px, CSS real do tema):** nenhuma página rola na horizontal. Tabelas em cartões; a matriz de preços cabe na tela.
- **GA4:** os botões "Pedir" levam data-awr-source (familia_*, marca_amp_*, eletricos, grande_poa) e são rastreados pelo listener de WhatsApp.

## Pendências e hipóteses (não alteradas)
- **Econ** ("bateria econ" 983 impressões; produto Econ 60Ah EFB 4.746 impressões): os dados se contradizem. A tabela chama o ECON60 de "EXCELL EFB60HD", e os códigos ECON aparecem na coluna Zetta do catálogo. Falta confirmar qual é a marca/linha para criar /marca/econ/.
- **Garantias que divergem entre páginas:**
  - O texto da Zetta em marcas.json diz 12 meses e o campo garantiaMeses diz 18.
  - A tabela de routes/cidade_venda.php diz Heliar 15 meses; a tabela oficial diz 24 em vários modelos.
- **Páginas antigas do WordPress** (/sao-leopoldo/, /novo-hamburgo/, /baterias-moura-porto-alegre/) rankeiam melhor que /baterias-em/{cidade}/. Pode haver disputa entre elas pela mesma busca. Mantidas como estão: não há evidência para redirecionar.

## Depois de instalar
- Abra **Aparência → Temas** uma vez como administrador. O tema regrava as rotas sozinho na troca de versão.
- Regenere o sitemap com `wp awr sitemap` ou aguarde o cron.
- **Search Console:**
  - Inspeção de URL em /baterias/hyundai/creta/, /marca/heliar/60ah/, /baterias-carros-eletricos-e-hibridos/ e /baterias-grande-porto-alegre/;
  - reenvie awr-sitemap.xml.
- **Acompanhamento:** em 3 a 4 semanas, compare as consultas "bateria {modelo}", "{marca} {n} amperes" e "baterias porto alegre".

## Rollback
Reinstale awr-baterias-theme-v5.50.0.zip. As páginas novas deixam de existir (404) e o resto volta ao que era.
