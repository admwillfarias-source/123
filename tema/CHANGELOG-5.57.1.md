# 5.57.1 — Taxas de entrega por cidade e horário (tabela oficial)

## Tabela aplicada no checkout
O checkout mostra e o pedido cobra exatamente estes valores.

| Cidade | Segunda a sábado (e feriados) | Domingo |
|---|---|---|
| Porto Alegre | 06:30–08:00 plantão **R$ 60** · 08:00–18:00 **grátis** · 18:01–22:00 plantão **R$ 60** | 08:00–22:00 **R$ 90** |
| Canoas, Esteio, Gravataí, Cachoeirinha, São Leopoldo, Sapucaia do Sul, Novo Hamburgo | 08:00–18:00 **grátis**, sem plantão | fechado (agendar) |
| Alvorada, Viamão | 09:00–17:00 **R$ 20** | fechado (agendar) |
| Sapiranga | 09:00–17:00 **R$ 25** (entrega no mesmo dia) | fechado (agendar) |
| Demais cidades | sem mudança (Ivoti, Estância Velha, faixas de CEP "mesmo dia" R$ 20, transportadora R$ 50/75, fora do RS) | sem mudança |

## O que mudou em relação à 5.57.0
- **Porto Alegre:**
  - entrega grátis a partir das 8h (antes, 8h31);
  - **domingo agora custa R$ 90** (antes, R$ 60 só no plantão);
  - feriado segue a tabela de dia útil.
- **Cidades com loja:**
  - sábado e feriado passam a atender, das 8h às 18h (antes, fechados);
  - sem plantão;
  - não há mais taxa por distância.
- **Alvorada e Viamão:** R$ 20 em todo o horário de atendimento (9h às 17h).
- **Sapiranga:**
  - entra na entrega local com taxa de R$ 25;
  - antes, o CEP caía na faixa de transportadora (R$ 50, só Pix, sem instalação);
  - agora aceita todas as formas de pagamento, com instalação e troca da bateria usada.
- **Para essas 11 cidades, a tabela manda, acima das faixas de CEP.**
- **Fora do horário:**
  - o checkout explica o horário da cidade (ex.: "Em Alvorada atendemos das 9h às 17h, de segunda a sábado (taxa de R$ 20)");
  - oferece Agendar ou Retirar na loja;
  - o servidor recusa "o quanto antes" fora do horário e domingo fora de Porto Alegre.
- **Checkout antigo (reserva):** o pedido aceita R$ 25 e R$ 90. As telas desse checkout continuam com as regras antigas, porque ele só é usado se a chave do checkout novo for desligada.
- **Textos do site:**
  - FAQ de horários (home, bairros, SEO), FAQ de Porto Alegre e de Alvorada e texto da categoria atualizados com a tabela;
  - frases genéricas como "plantão das 6h30 às 22h" em posts antigos continuam como estavam (ainda valem de segunda a sábado).
- **Ajuste futuro sem editar o tema:** filtro `awr_co_regras_cidade` (inc/checkout-v2.php).

## Validação
- **79 testes PHP** com a tabela inteira:
  - Porto Alegre: 07h, 07h59, 08h, 17h59, 18h, 18h30, 22h, 22h30, 06h, sábado, domingo 07h, 10h, 21h e 23h, feriado 10h e 19h;
  - Canoas, Esteio e Novo Hamburgo: 07h, 10h, 19h e domingo;
  - Alvorada e Viamão: 08h30, 10h, 17h30, sábado e domingo;
  - Sapiranga: 10h e 18h;
  - Ivoti, Caxias e SP sem mudança;
  - pedidos de domingo em Porto Alegre (R$ 90) e Sapiranga (R$ 25);
  - domingo em Canoas recusado;
  - checkout antigo com R$ 25 e R$ 90.
- **Navegador:**
  - checkout: 76 testes;
  - página de produto: 76 testes;
  - reserva: 6 testes.
- **Regressão:**
  - as 997 URLs do Search Console estão iguais;
  - sitemap com 65.312 URLs;
  - lint de todos os PHP.

## Rollback
Reinstale awr-baterias-theme-v5.57.0.zip.
