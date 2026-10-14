# 5.56.0 — Checkout novo em 3 etapas (Bateria → Entrega → Pagamento)

O checkout foi refeito com base no mockup: 3 etapas, um botão principal por etapa, prazo e taxa calculados pelo servidor e proteção contra pedido duplicado. O checkout anterior continua no tema como reserva, com uma chave no painel para voltar a ele.

## Diagnóstico do checkout anterior (5.55)
| # | Problema | Impacto |
|---|---|---|
| 1 | 4 etapas, CEP só na 3ª, 5 campos na etapa 2, dois botões que parecem principais na última etapa | atrito e abandono |
| 2 | "Em até 35 minutos" aparecia antes de saber o CEP | promessa que nem sempre se cumpre |
| 3 | Taxa calculada no navegador (R$ 20/R$ 60) e **trocada no servidor** pela faixa de CEP (R$ 20 mesmo dia, R$ 50/75 transportadora) | o cliente via um total e o pedido gravava outro |
| 4 | Sem proteção contra duplo clique ou reenvio | pedidos duplicados |
| 5 | Fechar o modal ou trocar de modelo apagava o que foi digitado | retrabalho e abandono |
| 6 | **A conversão "Pedido concluído" do Google Ads disparava ao abrir o checkout**, e de novo ao concluir; `purchase_confirm` repetia a cada recarga | Ads contando intenção como venda, lance otimizado errado |
| 7 | A confirmação pelo WhatsApp mostrava um número falso ("W######") e "35 min" fixo | informação errada ao cliente |
| 8 | Consentimento forçado como "granted", sem aviso de cookies | risco de LGPD |
| 9 | Sem foco inicial e sem focus trap; erros não anunciados | acessibilidade |

## O que mudou

### Checkout novo
- **Arquivos próprios, carregados só no clique:**
  - `assets/js/awr-checkout.js`: 28,9 KB, 10,6 KB com gzip;
  - `assets/css/awr-checkout-v2.css`: 13 KB;
  - código legível em `assets/js/src/awr-checkout.js`.
  - Nada novo no primeiro carregamento da página. O clique em "Comprar" nem baixa mais a busca (awr-search.js, 70 KB).
- **Etapa 1 — Bateria:**
  - selo "Compatível com o seu {veículo}";
  - foto, garantia, preço, 10x e Pix 3%;
  - benefícios, com "35 min\*" e a nota "\*conforme CEP e horário";
  - **"Quero esta bateria ›"**;
  - "Ver outras baterias compatíveis" abre uma folha com escolha única.
- **Etapa 2 — Entrega:**
  - começa com CEP, nome e WhatsApp;
  - o CEP chama o servidor, que devolve endereço, prazo e taxa;
  - depois aparecem número e complemento;
  - **o cartão de prazo só aparece calculado**;
  - fora da área: aviso de transportadora;
  - em horário fechado: "Agendar horário";
  - "Retirar na loja" continua disponível;
  - **"Continuar para pagamento ›"**.
- **Etapa 3 — Pagamento ("pague só na entrega"):**
  - Pix 3% (pré-selecionado), crédito em até 10x, débito e dinheiro 3%;
  - casco;
  - CPF/CNPJ recolhido, ou obrigatório no envio por transportadora;
  - resumo completo;
  - **"Finalizar pedido ›"**;
  - "Prefiro finalizar pelo WhatsApp" abre uma folha com o resumo e **não cria pedido**.
- **Confirmação:**
  - número real do pedido WooCommerce;
  - linha do tempo, com a previsão só quando calculada;
  - "Acompanhar no WhatsApp" e "Ver detalhes do pedido".
- **Layout:**
  - celular em tela cheia, com o botão principal fixo no rodapé;
  - desktop com formulário à esquerda e resumo fixo à direita.
- **Dados preservados:** voltar, trocar de bateria, fechar e reabrir (salvo no aparelho por 7 dias, apagado ao concluir).
- **Acessibilidade:**
  - `role=dialog` e foco inicial no título;
  - Tab preso no diálogo e Esc fecha (primeiro a folha, depois o checkout);
  - o foco volta ao botão de origem;
  - erros com `role=alert` e `aria-invalid`;
  - `aria-current` na etapa atual;
  - `autocomplete` e `inputmode` nos campos;
  - alvos de 44 px ou mais.

### Servidor (inc/checkout-v2.php — novo)
- **Cotação única `awr_entrega_cotacao()`**, endpoints `awr/v1/cotacao` e `/awr-busca/?action=cotacao`. **A tela mostra exatamente o que o pedido cobra.**
- **Pedido (`awr_create_order`, inc/woo.php):**
  - `pedido_token`: o mesmo token devolve o mesmo pedido por 30 minutos;
  - trava de 60 s contra dois envios simultâneos (resposta 409, e o navegador tenta de novo sozinho);
  - recalcula a cotação no envio, grava "Prazo informado ao cliente" (meta `_awr_prazo_informado`) e recebe `uf` e complemento;
  - **recusa "o quanto antes" fora do horário e agendamento no passado** (validação no servidor).
  - Preço oficial, Pix 3%, casco, +4% fora do RS, status "Processando", estoque e limite por IP **ficam como estavam**.
- **Checkouts abandonados (só com aceite):**
  - caixa "Pode me chamar no WhatsApp se eu não concluir" na etapa 2;
  - endpoint `awr/v1/lead`, com honeypot e limite de 10 por IP a cada 10 min;
  - tela **WooCommerce → Checkouts abandonados**, com botão "Chamar no WhatsApp";
  - apagado em 30 dias ou quando o mesmo WhatsApp conclui um pedido.
  - Sem aceite, nada sai do aparelho.
- **Chave no painel:** Configurações → AWR Busca → "Usar o checkout novo em 3 etapas" (ligada por padrão).

### Regras de entrega unificadas (o que já existia, agora num lugar só)
| Regra | Origem antes | Agora |
|---|---|---|
| Região rápida: 12 cidades (POA, Canoas, Gravataí…) | navegador | servidor, mesma lista |
| Horário: POA 06:30–22:00 todos os dias; demais cidades 09:00–18:00 em dia útil (feriados 2026–2028) | navegador | servidor, mesma lista |
| Plantão POA R$ 60 (06:30–08:30 e 18:01–22:00) | navegador | servidor |
| Mais de 12 km da loja: R$ 20 | navegador | servidor |
| Faixa de CEP "mesmo dia": R$ 20 | só no servidor (sobrescrevia em silêncio) | servidor, **e agora aparece na tela** |
| Faixa de CEP transportadora: R$ 50 (R$ 75 acima de 20 kg) | só no servidor (sobrescrevia em silêncio) | servidor, **e agora aparece na tela** |
| Fora do RS: transportadora, Pix, +4%, frete a cotar | navegador + servidor | servidor |
| Fora da região rápida: só Pix, casco cobrado, CPF obrigatório | navegador | servidor |

**Divergência encontrada:**
- O navegador mostrava "Grátis" (ou R$ 20/R$ 60) para CEPs das faixas "mesmo dia" e "transportadora", e o pedido gravava R$ 20 ou R$ 50/75.
- Mantive o valor que **o pedido já cobrava**: nenhuma regra comercial mudou.
- A diferença é que agora o cliente vê esse valor antes de finalizar.

### Eventos e consentimento
- **Abrir o checkout** dispara só `begin_checkout`, uma vez por checkout (não repete ao reabrir).
- **Saiu a conversão "Pedido concluído" do Ads na abertura**, inclusive no checkout antigo.
- `add_shipping_info` ao sair da etapa 2 e `add_payment_info` ao escolher o pagamento.
- `purchase` com `transaction_id` e a conversão do Ads (agora também com `transaction_id`) **uma vez por pedido**.
- `/pedido-confirmado/`:
  - não repete `purchase_confirm` ao recarregar;
  - não conta de novo o pedido já contado no checkout;
  - mostra os dados reais do pedido (com `?k=`);
  - não mostra mais número falso nem "35 min" fixo.
- WhatsApp: a conversão de WhatsApp de sempre (`generate_lead`), nunca `purchase`.
- **Consent Mode v2:**
  - padrão negado até a escolha;
  - faixa "Aceitar / Só essenciais", de cerca de 2 KB inline, que lembra a escolha por 180 dias;
  - quem aceitou volta com tudo liberado.
  - Para usar um plugin de cookies próprio: `add_filter( 'awr_consent_banner', '__return_false' )`, que volta ao padrão "granted" anterior.

## Validação
- **PHP com WooCommerce simulado, 39 testes:**
  - cotação: POA 14h (grátis, 35 min); 07h e 19h30 (R$ 60); 23h (fechado); sábado e feriado em Canoas; Ivoti, faixa mesmo dia (R$ 20); Caxias, transportadora (R$ 50, só Pix, casco, CPF); SP (+4%, frete a cotar); CEP inválido; retirada;
  - endereço do CEP em cache;
  - pedido: **mesmo token 2x = 1 pedido**; trava simultânea (409); taxa do pedido = cotação; Pix 3%; casco; agendamento válido e no passado; "agora" às 23h30 recusado; retirada; checkout antigo intacto (plantão R$ 60);
  - lead: sem aceite recusado; honeypot; atualização do mesmo WhatsApp; apagado ao concluir o pedido; limite por IP.
- **Navegador (Playwright), 390 px e 1440 px, 76 testes, com a cotação feita pelo PHP real do tema:**
  - fluxo completo, com um botão principal por etapa;
  - voltar, trocar de bateria e reabrir mantêm os dados;
  - "35 min" só depois da cotação rápida;
  - Caxias com transportadora;
  - 23h30 pede agendamento;
  - folha do WhatsApp sem pedido;
  - **duplo clique = 1 pedido**;
  - erro de rede com nova tentativa = mesmo token e 1 pedido;
  - eventos: `begin_checkout` 1x, `add_shipping_info`, `add_payment_info`, `purchase` 1x e nenhuma conversão do Ads na abertura;
  - Tab preso e Esc;
  - foco volta ao botão.
- **Reserva:**
  - com a chave desligada, abre o checkout antigo;
  - se o arquivo novo não carregar, cai sozinho no antigo, sem erro de JS e sem conversão na abertura.
- **Faixa de cookies, 8 testes:** padrão negado, Aceitar concede, Só essenciais mantém negado, escolha lembrada.
- **Regressão de SEO:**
  - as 997 URLs do Search Console estão iguais à 5.55 (756 indexáveis);
  - sitemap com 65.312 URLs;
  - lint de todos os PHP.

## Depois de instalar
1. Limpe o cache do site e do Cloudflare.
2. Faça um pedido de teste completo (CEP de POA) e confira no WooCommerce:
   - status "Processando";
   - nota "Prazo informado ao cliente";
   - taxa igual à da tela.
3. **Google Ads:**
   - a conversão "Pedido concluído - Site" passa a contar só pedidos reais. É esperada uma **queda no número de conversões**, que antes incluíam aberturas do checkout.
   - Se a estratégia de lance usa essa conversão, acompanhe por 2 semanas antes de mudar o CPA alvo.
4. **GA4:** marque `purchase` como evento-chave, se ainda não estiver.
5. Se usar um plugin de cookies (CookieYes, Complianz…), desligue a faixa do tema com o filtro acima.

## Rollback
- **Só o checkout:** desmarque a chave em Configurações → AWR Busca.
- **Tudo:** reinstale awr-baterias-theme-v5.55.0.zip.
