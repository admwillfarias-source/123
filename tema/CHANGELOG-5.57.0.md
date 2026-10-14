# 5.57.0 — Página de produto que vende (compatibilidade → preço claro → checkout)

## Problemas corrigidos
- **H1 longo:** "… – Entrega e Instalação em Porto Alegre e Região" virou só "Bateria Moura 60Ah M60GD". A entrega foi para uma linha própria.
  - O `<title>`, a meta description, o canonical e a URL **não mudaram**.
  - Os H1 editoriais do lote de SEO continuam valendo.
- **Cartão quebrado** "R$ Preço com e sem a bateria usada na troca": substituído por benefícios com ícones e por uma linha clara de preço: "Sem a bateria usada na troca: R$ X (casco de R$ Y)".
- **Selo "● Compatível · disponível" fixo:**
  - agora mostra o estoque real do WooCommerce: "Em estoque", "Sob encomenda" ou "Consulte a disponibilidade";
  - "Compatível com {veículo}" aparece só depois que o cliente confirma o veículo.
- **Bateria de moto falava em carro:**
  - o título da lista de aplicações e a pergunta do FAQ agora dizem "na minha moto";
  - o texto da pergunta mudou também no schema FAQ.

## Novidades
- **Galeria:**
  - foto principal e fotos da galeria do WooCommerce;
  - celular com carrossel e setas; desktop com miniaturas;
  - clique amplia a foto;
  - 1ª foto com prioridade e tamanho fixo (sem salto de layout);
  - com uma única foto, nada muda.
- **Preço:** à vista com a troca, cartão "no Pix (3%)", 10x sem juros e valor sem a troca.
- **Botões:**
  - "Comprar agora com instalação" abre o checkout novo **com o veículo e o CEP já preenchidos**;
  - "Comprar pelo WhatsApp" manda produto, preço, veículo e CEP.
- **"Ver se essa bateria é compatível com minha moto / meu carro":**
  - seletor Marca → Modelo → Ano, com os dados do catálogo de aplicações;
  - se serve, mostra o selo verde e lembra o veículo neste aparelho para esta bateria;
  - "Outra marca" ou "Outro modelo" leva à busca da bateria certa e ao WhatsApp.
- **"Consultar entrega e instalação" por CEP:**
  - mesma cotação do checkout (prazo, taxa, transportadora, fora do RS);
  - o CEP fica salvo e é consultado de novo na próxima visita.
- **Barra de seções** (Descrição · Especificações · Aplicações · Perguntas · Avaliações) que só leva a cada seção. Todo o conteúdo continua visível no HTML (SEO).
- **Avaliações reais do WooCommerce:**
  - estrelas e lista só quando há avaliações aprovadas;
  - sem avaliações, aparece o convite "Avaliar esta bateria".
- **Celular:**
  - foto mais baixa, para preço e botão aparecerem na 1ª tela;
  - a barra fixa mostra "Com a troca";
  - o botão flutuante de WhatsApp some na página de produto, já que a barra tem o WhatsApp.
- **Eventos GA4:**
  - `compat_check` (serve / não encontrado);
  - `delivery_quote` (modo e taxa);
  - `view_item` continua o mesmo de antes;
  - nenhuma conversão nova do Ads.

## Arquivos
- novos:
  - inc/produto-pagina.php;
  - template-parts/produto-avaliacoes.php;
  - assets/css/awr-produto.css (só em produto);
  - assets/js/awr-produto.js (7,7 KB, só em produto; código legível em assets/js/src/);
- alterados:
  - routes/produto.php;
  - inc/woo.php (FAQ de moto);
  - footer.php;
  - assets/js/src/awr-checkout.js (recebe veículo e CEP da página).

## Validação
- **Simulador PHP** (Motobatt MBTX9U e Moura M60GD):
  - H1 curto;
  - sem o cartão quebrado;
  - textos de moto e carro corretos;
  - JSON de compatibilidade (MBTX9U: 24 marcas e 289 modelos, 8 KB);
  - estrelas e lista de avaliações só com avaliações reais.
- **Navegador, 390 px e 1440 px, 76 testes:**
  - deslocamento de layout (CLS) abaixo de 0,05;
  - botão de compra na 1ª tela;
  - galeria;
  - seletor (serve e outra marca);
  - veículo levado ao botão, à barra do celular e ao WhatsApp;
  - CEP de POA e de Caxias;
  - botão flutuante escondido no celular;
  - eventos;
  - checkout abre com veículo e CEP;
  - veículo lembrado ao voltar;
  - sem erro de JS.
- **Checkout 5.56:** 39 testes PHP, 76 de navegador e 6 da reserva, todos passando.
- **Regressão:**
  - as 997 URLs do Search Console estão iguais à 5.56;
  - sitemap com 65.312 URLs;
  - lint de todos os PHP.

## Observações
- **Fotos extras e avaliações** dependem do cadastro no WooCommerce. Para a galeria aparecer, cadastre mais fotos em "Galeria do produto". Vídeo não foi incluído.
- **Dimensões e polaridade** só aparecem quando a tabela oficial tiver esses dados. Para a MBTX9U a tabela não tem Ah nem CCA, por isso o subtítulo mostra só "12V — para motos".

## Rollback
Reinstale awr-baterias-theme-v5.56.0.zip.
