# Plano de testes A/B do checkout (a partir da 5.56.0)

## Como medir
- **Métrica principal:** taxa de pedido = pedidos `purchase` ÷ `begin_checkout` (GA4, por sessão).
- **Métricas de apoio:**
  - abandono por etapa: `begin_checkout` → `checkout_etapa_bateria` → `add_shipping_info` → `add_payment_info` → `purchase`;
  - ticket médio;
  - taxa de `checkout_whatsapp_enviado`;
  - `checkout_erro` por campo.
- **Tamanho:** com cerca de 5% de conversão, detectar +20% relativo exige uns 7.500 `begin_checkout` por variante (95%/80%). Abaixo disso, rode por pelo menos 2 semanas completas e trate o resultado como direção, não prova.
- **Um teste por vez.** Todos os eventos já levam `card_modelo` e `checkout: v2`.
- **Antes do A/B:** rode 2 semanas o checkout novo contra o antigo, pela chave do painel e pelo histórico.

## Fila sugerida
| # | Hipótese | Variante A | Variante B | Métrica | Por que primeiro |
|---|---|---|---|---|---|
| 1 | Pix pré-selecionado puxa o total para baixo e aumenta a conclusão | Pix marcado (atual) | nenhum marcado | taxa de pedido; mix de pagamento | mexe só no padrão, sem risco |
| 2 | Um texto de ação com serviço converte mais | "Quero esta bateria ›" | "Comprar com instalação grátis ›" | `checkout_etapa_bateria` ÷ `begin_checkout` | etapa de maior volume |
| 3 | Mostrar as alternativas já na etapa 1 reduz a saída de quem acha caro | link recolhido (atual) | 2 alternativas visíveis abaixo do botão | taxa de pedido; ticket médio | pode baixar o ticket: medir os dois |
| 4 | Modelo de card da busca | A (app) | B (recomendada) e C (econômica/recomendada/premium) | `begin_checkout` ÷ busca; taxa de pedido | já existe no painel (Configurações → AWR Busca) |
| 5 | Pedir o WhatsApp antes do CEP | CEP · nome · WhatsApp | WhatsApp · nome · CEP | `add_shipping_info` ÷ `checkout_etapa_bateria`; leads com aceite | afeta a recuperação de abandono |
| 6 | O aceite de contato marcado por padrão aumenta a recuperação | desmarcado (atual) | **não testar marcado**: a LGPD pede aceite livre | — | registrar como decisão, não teste |
| 7 | A folha do WhatsApp canibaliza pedidos do site | link visível na etapa 3 | link só depois de um erro ou de 60 s parado | `purchase` + `checkout_whatsapp_enviado` | medir a soma dos dois canais |

## Como implementar a divisão
- A variante pode ser sorteada no navegador (50/50, salva em `localStorage`) e enviada em todos os eventos como `ab_checkout`.
- O ponto natural é `assets/js/src/awr-checkout.js`.
- Peça a mudança quando quiser começar. Cada teste é uma alteração pequena.

## Leitura do resultado
- Compare a taxa de pedido por variante no GA4 (Explorar → Funil, segmentado por `ab_checkout`).
- Só declare vencedora com o intervalo de confiança sem cruzar zero e com o ticket médio igual ou maior.
