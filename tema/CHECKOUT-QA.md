# Checklist de QA — checkout 5.56.0 (no site, depois de instalar)

Teste em **janela anônima**, primeiro no celular, depois no desktop. Limpe o cache antes. Use `?awr_debug=1` para ver os eventos no GA4 → DebugView.

## Compra (WooCommerce)
- [ ] Busca → card → "Comprar Online" abre o checkout novo na etapa 1, com o veículo no selo.
- [ ] Preço, 10x e Pix iguais aos do card e do produto no WooCommerce.
- [ ] Pedido com CEP de POA, em horário comercial, é concluído e aparece em WooCommerce → Pedidos como **Processando**.
- [ ] No pedido: nota "Prazo informado ao cliente" e taxa igual à da tela.
- [ ] O estoque do produto baixa como antes (se a gestão de estoque estiver ligada).
- [ ] E-mails do WooCommerce (novo pedido e cliente) chegam como antes.
- [ ] Produto sem preço: o botão vira "Pedir preço no WhatsApp".

## Pagamentos
- [ ] Pix: desconto de 3% no resumo e no pedido.
- [ ] Dinheiro: desconto de 3%.
- [ ] Crédito 10x: sem desconto; o pedido grava parcelas = 10.
- [ ] Débito: sem desconto.
- [ ] Desmarcar "Vou entregar a bateria usada": o casco entra no resumo e no pedido.

## CEP e região
- [ ] CEP de POA (ex.: 90010-000), em horário comercial: "em até 35 minutos", taxa grátis.
- [ ] POA às 07h ou às 19h: taxa de plantão R$ 60 na tela e no pedido.
- [ ] POA depois das 22h: sem 35 min; pede para agendar; "o quanto antes" não avança.
- [ ] Canoas no sábado: fechado, oferece agendar.
- [ ] CEP de faixa "mesmo dia" (ex.: Ivoti 93900-000): "no mesmo dia", R$ 20.
- [ ] CEP de transportadora (ex.: Caxias 95010-000): R$ 50, só Pix, casco no total, CPF obrigatório, sem "35 min".
- [ ] CEP fora do RS (ex.: 01310-100): frete a cotar, +4%, só Pix.
- [ ] CEP inexistente: mensagem clara, não avança.
- [ ] CEP geral (sem rua): os campos de rua e bairro aparecem para digitar.

## Agendar e retirar
- [ ] Agendar para amanhã, 09:00: o pedido grava "Entrega e instalação agendadas — Em dd/mm às 09:00".
- [ ] Agendar para um horário que já passou: recusado.
- [ ] Retirar na loja: escolher a loja; taxa grátis; o pedido grava `loja_retirada`.

## Duplicidade e falhas
- [ ] Dois cliques rápidos em "Finalizar pedido": **1 pedido**.
- [ ] Rede lenta: o botão mostra "Registrando seu pedido…" e não aceita outro clique.
- [ ] Erro na finalização: mensagem com a opção de WhatsApp; "Tentar de novo" não duplica.

## Dados preservados
- [ ] Voltar da etapa 3 para a 2: tudo preenchido.
- [ ] Trocar de bateria na folha "outras compatíveis": nome, WhatsApp e endereço continuam.
- [ ] Fechar o checkout e abrir de novo: volta na mesma etapa.
- [ ] Depois de concluir, abrir de novo: começa limpo.

## WhatsApp
- [ ] "Prefiro finalizar pelo WhatsApp": a folha mostra bateria, veículo, endereço e total.
- [ ] "Comprar pelo WhatsApp" abre a conversa com o resumo; **nenhum pedido criado** no WooCommerce.
- [ ] "Continuar pelo site" volta para a etapa 3 com tudo preenchido.

## Checkouts abandonados
- [ ] Marcar "Pode me chamar no WhatsApp…", preencher nome e WhatsApp, avançar e fechar: aparece em WooCommerce → Checkouts abandonados.
- [ ] Sem marcar o aceite: não aparece nada.
- [ ] Concluir um pedido com o mesmo WhatsApp: o registro some.

## Eventos (GA4 DebugView / Tag Assistant)
- [ ] Abrir o checkout: `begin_checkout` 1x; **nenhuma conversão do Ads**.
- [ ] Fechar e reabrir: `begin_checkout` não repete.
- [ ] Sair da etapa 2: `add_shipping_info`. Escolher o pagamento: `add_payment_info`.
- [ ] Concluir: `purchase` com `transaction_id` e conversão "Pedido concluído - Site" 1x.
- [ ] Abrir "Ver detalhes do pedido" e recarregar: `purchase_confirm` **não** dispara de novo.
- [ ] Clique no WhatsApp: `whatsapp_click` / `generate_lead`, sem `purchase`.

## Consentimento
- [ ] Primeira visita: a faixa "Aceitar / Só essenciais" aparece no rodapé e não cobre o botão principal do checkout.
- [ ] Tag Assistant: consentimento padrão `denied`. Ao aceitar, vira `granted`.
- [ ] Recarregar: a faixa não volta e a escolha é mantida.

## Teclado e acessibilidade
- [ ] Tab percorre só o checkout; Shift+Tab volta; Esc fecha (primeiro a folha, depois o checkout).
- [ ] Ao fechar, o foco volta ao botão "Comprar".
- [ ] Erros são lidos pelo leitor de tela (TalkBack/VoiceOver).
- [ ] Zoom de 200% no desktop: nada cortado.

## Desempenho
- [ ] PageSpeed da home e de uma página de veículo igual ao de antes da instalação (o checkout só carrega no clique).
- [ ] Nenhum salto de layout ao abrir o checkout (imagem com tamanho fixo).

## Reserva
- [ ] Configurações → AWR Busca → desmarcar "Usar o checkout novo": o checkout antigo volta (limpe o cache).
