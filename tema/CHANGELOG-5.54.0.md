# 5.54.0 — Busca com preço do WooCommerce, resultado igual ao app e 3 modelos de card

## Causa dos cards "sem preço"
Comparando com o app (BatterySearch.tsx e woo-upstream no Lovable):
- **Como o produto é encontrado:**
  - O app procura o produto em 3 etapas: API do WooCommerce, depois Store API, depois **busca pelo código no nome do produto**.
  - O tema só aceitava o `_sku` idêntico ao código da tabela (mais os apelidos, que são os mesmos do app).
  - Com o SKU da loja escrito diferente ("HE60-HD", "M60GD " com espaço) ou com o código só no título, o tema mostrava "Preço sob consulta".
- **Produto variável** sem preço no produto pai também caía em "sob consulta".
- **Índice reserva:** quando o servidor de busca falhava, o navegador usava um índice desatualizado (10/10, 2.011 itens) e sempre sem preço.

## O que mudou
- **Preço pelo SKU, para todas as marcas** (inc/woo.php → awr_lookup_tolerante_id):
  - procura o SKU ignorando espaço, hífen, ponto, "-BS" e a palavra MOTOBATT;
  - depois procura o código no nome do produto, como palavra inteira;
  - a polaridade nunca é trocada (M60GD não casa M60GE; Z50ED não casa Z50EE);
  - produto variável usa o menor preço das variações;
  - o Pix do produto passou a 3%, igual ao checkout e ao app (a função de produto calculava 5%).
- **Índice reserva** (assets/js/awr-vindex.json) regerado do catálogo atual: 6.365 itens, com Motobatt e as correções da 5.52.0.
  - Se o servidor falhar, a busca tenta de novo antes de usar o índice e avisa no console ("awr: busca offline").
  - Card sem preço nunca abre o checkout automático.
- **Card igual ao app** (template-parts/card-bateria.php e o card do JavaScript):
  - botões "Comprar Online" (dourado, abre o checkout), "Fale com um Atendente" (contorno verde, WhatsApp) e "Ligar e pedir agora" (contorno azul-marinho);
  - sem preço: "Pedir preço no WhatsApp";
  - nome do produto em H3; título do resultado em H2.
  - No celular, carrossel com cards de 82% e "Arraste para o lado para ver mais opções"; no desktop, grade automática.
- **3 modelos de card** (Configurações → AWR Busca; o padrão é o A):
  - **A — Igual ao app.**
  - **B — Recomendada em destaque:** cards com preço primeiro; o primeiro ganha a fita "★ Recomendada para o seu {veículo}", borda dourada e o botão "Comprar agora com instalação".
  - **C — Econômica / Recomendada / Premium:** até 3 opções com preço, cada uma com uma linha dizendo para quem é. A Recomendada fica no centro, em destaque. O resto fica em "Ver todas as compatíveis".
  - O checkout automático abre a Recomendada (ou o primeiro card com preço).
  - Os eventos do GA4 da busca levam `card_modelo`, para comparar a conversão de cada modelo.
  - **Prévia dos 3 modelos:** /awr-previa-cards/?veiculo=onix 2018 (só para administrador, noindex).
- **Painel Configurações → AWR Busca** (substitui o "AWR Motobatt"):
  - escolha do modelo de card;
  - teste de busca por veículo (código da tabela → produto da loja → SKU → preço);
  - relatório de todos os códigos do catálogo (com preço, sem preço, não encontrados), ordenado pelo número de veículos atendidos.
- **SEO e textos de venda:**
  - /buscar/: H1 "Busque a bateria certa para o seu veículo", lead do app, H2 "Como funciona a busca…" com 3 H3, e H2 "Não encontrou seu modelo?".
  - Título do resultado: "Baterias recomendadas · a partir de R$ X" (busca e páginas de veículo).
  - Depois da busca, o título da aba mostra "Bateria para {veículo} — a partir de R$ X", como no app. O canonical não muda.
  - Meta description de carro com preço da loja: "Compre bateria para {veículo} a partir de R$ X: instalação grátis em até 35 min em Porto Alegre. Garantia de fábrica e 10x sem juros."
  - Os titles das páginas com tráfego não mudaram.

## Validação
- **Busca de preço com WooCommerce simulado:** 9 casos certos (SKU com espaço ou hífen, apelido, código só no título, polaridade errada que não casa).
- **Navegador, fluxo real** ("Onix 2018" com API simulada):
  - modelos A, B e C renderizam como esperado;
  - o checkout automático abre a Recomendada;
  - eventos com `card_modelo`;
  - servidor fora do ar: nova tentativa, índice reserva e nenhum checkout para card sem preço.
- **Sem rolagem lateral** a 390px e 1440px.
- **SEO:** /buscar com 1 H1, 2 H2 e 3 H3; páginas de veículo com 1 H1, H2 e H3; as 5.940 meta descriptions de modelo entre 70 e 160 caracteres.
- **Regressão:** as 997 URLs do Search Console se comportam igual à 5.53.0. Sitemap com 65.312 URLs, gerado em 0,69 s.

## Depois de instalar
1. Limpe o cache do site e do Cloudflare.
2. Abra **Configurações → AWR Busca → Gerar relatório**. A lista "não encontrados na loja" mostra quais códigos precisam de produto ou de SKU corrigido no WooCommerce.
3. Para escolher o modelo de card, veja a prévia (/awr-previa-cards/) e salve no painel.

## Rollback
Reinstale awr-baterias-theme-v5.53.0.zip.
