# Checkout 5.56.0 — arquitetura, telas e fluxo

Capturas em `checkout-5.56.0/`, a 390 px (celular) e a 1440 px (desktop).

## 1. Visão geral
```
Card "Comprar Online" ([data-awr-checkout])
  └─ awr-core.js: clique → carrega awr-checkout-v2.css + awr-checkout.js (só agora)
       └─ AWRCheckout.open(card)
            1 Bateria ──► 2 Entrega ──► 3 Pagamento ──► Confirmação
                              │  GET awr/v1/cotacao (CEP → endereço, prazo, taxa)
                              │  POST awr/v1/lead (só com aceite)
                              └──────────────► POST awr/v1/pedido (pedido_token)
                                                 └─ awr_create_order → WooCommerce "Processando"
```
- **Reserva:**
  - chave `awr_checkout_v2` desligada → checkout antigo (awr-search.js);
  - se o arquivo novo não carregar, o checkout antigo abre sozinho.
- **Busca com checkout automático:** a busca chama `AWRSearch.openCheckout`, que agora abre o novo.
- **Fonte única de preço, prazo e taxa:** o servidor (`awr_entrega_cotacao`). O navegador só exibe.

## 2. Layout
| | Celular (até 1023 px) | Desktop (1024 px ou mais) |
|---|---|---|
| Moldura | tela cheia | janela de até 1080 px, cantos arredondados |
| Topo | voltar · logo · "Compra 100% segura" · fechar | igual |
| Progresso | 1 Bateria · 2 Entrega · 3 Pagamento (`aria-current`) | igual |
| Conteúdo | coluna única | formulário à esquerda |
| Resumo | dentro da etapa 3 | coluna fixa à direita (340 px), em todas as etapas |
| Botão principal | fixo no rodapé (sticky) | ao fim do formulário |
| Folhas (alternativas, WhatsApp) | sobem do rodapé | centralizadas |

## 3. Componentes e campos por etapa
### Etapa 1 — Bateria
| Componente | Regra |
|---|---|
| Selo "✓ Compatível com o seu {veículo}" | só se o card tiver o veículo |
| Foto, selo de garantia, nome, modelo | do card (data-*) |
| Preço, "ou 10x de R$ X sem juros", "R$ Y no Pix — 3%" | preço do WooCommerce já carregado no card |
| Benefícios | instalação e teste grátis; garantia; nova e original com nota; preço na troca; "35 min\*" |
| Nota | "\*conforme o CEP e o horário, confirmado na próxima etapa" |
| **Botão principal** | "Quero esta bateria ›" (sem preço: "Pedir preço no WhatsApp ›") |
| Secundário | "Ver outras baterias compatíveis (N)": folha com escolha única e "Selecionar esta bateria" |

### Etapa 2 — Entrega
| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| CEP | `inputmode=numeric`, `autocomplete=postal-code`, máscara 00000-000 | sim (exceto retirada) | 8 dígitos → cotação no servidor; link "Não sei meu CEP" (Correios) |
| Seu nome | `autocomplete=name` | sim (3 letras ou mais) | |
| WhatsApp | `type=tel`, máscara (51) 99999-9999 | sim (10 ou 11 dígitos) | |
| Aceite de contato | checkbox, desmarcado | não | só com ele o lead vai para o servidor |
| Endereço (rua, bairro, cidade/UF) | preenchido pelo CEP | sim | "Editar endereço"; CEP geral abre os campos |
| Número | texto | sim | aceita "s/n" |
| Complemento | texto | não | |
| Cartão de prazo | — | — | **só aparece com a cotação**; verde quando é 35 min; laranja quando está fechado |
| "Prefere agendar ou retirar na loja?" | rádios: o quanto antes · agendar (dia/hora) · retirar (loja) | — | abre sozinho quando está fechado |
| **Botão principal** | "Continuar para pagamento ›" | | |

### Etapa 3 — Pagamento
| Componente | Regra |
|---|---|
| Pix (3%) · Crédito até 10x · Débito · Dinheiro (3%) | todos pagos na entrega; Pix pré-selecionado; fora da região rápida, só Pix |
| Parcelas | aparece com crédito; mostra o valor de cada parcela |
| "Vou entregar a bateria usada na troca" | marcado; desmarcar soma o casco. Sem instalação no local, o casco entra sempre |
| "Precisa de nota com CPF/CNPJ?" | recolhido; aberto e obrigatório no envio por transportadora |
| Resumo | bateria, veículo, endereço (Editar), entrega e taxa, instalação, casco, acréscimo, desconto, total, parcelas |
| **Botão principal** | "Finalizar pedido ›" (desativa no 1º clique; o mesmo token na nova tentativa) |
| Secundário | "Prefiro finalizar pelo WhatsApp": folha com resumo, "Comprar pelo WhatsApp" / "Continuar pelo site" |

### Confirmação
- "Pedido confirmado!" e "Pedido #N" (número do WooCommerce).
- Linha do tempo: recebido → em separação → sai para atendimento → chegada prevista. A previsão é a do servidor ou "Confirmamos o horário pelo WhatsApp".
- Botões "Acompanhar no WhatsApp" e "Ver detalhes do pedido" (`/pedido-confirmado/?pedido=N&k=chave`).

## 4. Fluxo pelo WhatsApp
1. Na etapa 3, "Prefiro finalizar pelo WhatsApp" → folha com bateria, veículo, endereço e total.
2. "Comprar pelo WhatsApp" abre o wa.me com o resumo (bateria, veículo, nome, endereço e CEP, prazo e taxa, pagamento, total).
3. **Nenhum pedido é criado e nenhuma compra é registrada.** Conta a conversão de WhatsApp de sempre (`generate_lead`), mais `checkout_whatsapp_enviado`.
4. "Continuar pelo site" fecha a folha e mantém tudo preenchido.

## 5. Servidor
| Endpoint | Método | Uso | Proteção |
|---|---|---|---|
| `awr/v1/cotacao` (e `/awr-busca/?action=cotacao`) | GET | CEP, tipo, data/hora, produto → endereço, região, prazo, taxa, regras | só leitura, `no-cache`, ViaCEP em cache por 30 dias |
| `awr/v1/pedido` | POST | cria o pedido | honeypot, limite por IP (9 a cada 10 min), `pedido_token` (30 min), trava de 60 s, validação de horário, preço e taxa recalculados |
| `awr/v1/lead` | POST | checkout abandonado | só com `aceite`, honeypot, 10 por IP a cada 10 min |

**Cotação — ordem das regras:**
1. retirada;
2. fora do RS;
3. faixa de CEP transportadora;
4. faixa de CEP mesmo dia;
5. agendado;
6. região rápida aberta (35 min);
7. região rápida fechada (agendar);
8. cidade "mesmo dia" ou "dia seguinte" (cidades.json);
9. consultar no WhatsApp.

**Taxa:** horário e distância (R$ 0/20/60) e, por cima, a faixa de CEP (R$ 20 / R$ 50 / R$ 75).

**Metas no pedido:** `_awr_prazo_informado`, `_awr_prazo_min`, `_awr_checkout=v2`, `complemento` e `loja_retirada`, mais as de antes (`carro_ano`, `cpf_cnpj`, `parcelas`, `tipo_entrega`).

## 6. Dados no aparelho (LGPD)
| Chave | Conteúdo | Validade |
|---|---|---|
| `awr_co_v2` (localStorage) | etapa, bateria, campos digitados, token | 7 dias; apagado ao concluir |
| `awr_tx_N` / `awr_pc_N` | marca de compra já contada | permanente (sem dados pessoais) |
| cookie `awr_consent` | `all` ou `min` | 180 dias |
