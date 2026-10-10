# 5.48.0 — Auditoria funcional do pedido

## Pedido (inc/woo.php → awr_create_order) — crítico
Preço, desconto, casco, taxa e acréscimo vinham do navegador sem limite: um pedido com desconto_pct=100 chegava ao WooCommerce com total zero; preço R$ 1 virava pedido de R$ 1 em item avulso.
Agora:
- Preço = o do produto no WooCommerce (ou da tabela oficial em inc/tabela-baterias.php). Só item fora do catálogo usa o preço enviado, com nota "confirmar".
- Desconto à vista: só 3%, só Pix ou dinheiro.
- Casco: valor oficial do modelo (awr_valor_casco).
- Acréscimo fora do RS: 4% do preço oficial.
- Taxa de entrega sem CEP: só R$ 0, R$ 20 (distância) ou R$ 60 (plantão).
- Toda diferença vira nota no pedido ("Conferência de valores"), inclusive total mostrado ao cliente ≠ total do pedido.
Pedidos legítimos fecham com o mesmo total de antes (testado).

## Limite de pedidos por IP (inc/rest.php)
Atrás de Cloudflare/proxy, REMOTE_ADDR é o IP do proxy, compartilhado por muitos clientes: o limite de 8 pedidos/10 min podia bloquear compras reais. Agora usa também CF-Connecting-IP / X-Real-IP / X-Forwarded-For.

## Outros
- /home/ (página antiga do WordPress) → 301 para a página inicial (sem loop quando "home" é a própria página inicial).
- GA4: evento view_item nas páginas de produto.
- WhatsApp reserva da calculadora estacionária trocado pelo número oficial (5551993199486).

## Rollback
Reinstalar awr-baterias-theme-v5.47.0.zip e limpar o cache.
