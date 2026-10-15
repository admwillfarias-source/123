# 5.58.1 — Versão segura da 5.58.0 (depois do erro 429)

## O que aconteceu
- Depois do upload da 5.58.0, o site e o painel mostraram "429 Too Many Requests".
- Essa página é da **hospedagem ou do firewall**: o servidor recebeu mais requisições do que o limite.
- **A causa ainda não está confirmada:** é preciso o log de acesso do horário.

**O que a 5.58.0 trouxe que gera requisições ou trabalho sozinho:**
1. **Tarefa agendada (cron) a cada visita:**
   - enquanto os índices da busca não estavam gravados em `uploads/awr-busca/`, cada página aberta agendava uma tarefa no cron do WordPress, e cada tarefa dispara uma chamada interna (`wp-cron.php`);
   - se a gravação falhasse no servidor, isso se repetia sem parar. **Principal suspeito.**
2. **Canal da busca no gancho `init`:** mudança de comportamento no servidor.
3. **Pré-busca automática no navegador:** ao passar o mouse, quando a lista parava de mudar, e pré-carga no ocioso.

## O que a 5.58.1 faz
- **Nenhuma visita de página agenda cron ou grava arquivo.** Os índices vêm só do tema; para regerar, use **Configurações → AWR Busca → "Regerar índices agora"** ou `wp awr indice-busca`.
- **Canal `/awr-busca/` de volta ao `template_redirect`**, igual à 5.57.1.
- **Pré-busca só no toque ou clique na sugestão.** Sem pedidos ao passar o mouse, sem pedido automático e sem pré-carga do índice no ocioso.
- **Trava no navegador:** no máximo 20 pedidos de busca por minuto por aba; acima disso, espera.
- **Debounce da digitação de volta a 180 ms**, para não aumentar requisições se o índice local não carregar.
- **Mantido:**
  - **sugestões no navegador:** zero requisições por letra, ou seja, menos carga do que a 5.57.1;
  - **índice do seletor de moto fora do HTML** (páginas de moto de 386 KB para 74 KB);
  - **cache dos resultados:** 10 min no navegador e 2 min nas respostas.

## Medido (celular 4G lento, CPU 4x, servidor de 600 ms)
| | 5.57.1 | 5.58.1 |
|---|---|---|
| Página parada por 30 s: requisições à busca, ao cron ou ao índice | 0 | **0** |
| Requisições de sugestão ao digitar "onix 2018" | 1 | **0** |
| Requisições de produto ao escolher | 1 | **1** |
| Requisições extras ao passar o mouse nas sugestões | 0 | **0** |
| Da última tecla até a sugestão | 1.000 ms | **200 ms** |

**Validação:**
- paridade de 333 buscas;
- checkout: 76 testes de navegador, 6 da reserva e 79 testes PHP;
- página de produto: 76 testes;
- seletor de moto;
- regressão: 997 URLs do Search Console sem mudança, sitemap e lint.

## Como instalar (pela hospedagem, NÃO pelo painel do WordPress)
1. Espere o site estar normal com a 5.57.1, de preferência num horário de pouco movimento.
2. **Gerenciador de arquivos** → `wp-content/themes/`:
   - renomeie `awr-baterias` para `awr-baterias-5571`;
   - envie este zip e use **Extrair**.
3. Limpe o cache do plugin e do Cloudflare.
4. Acompanhe por 10 minutos. Se aparecer 429 de novo:
   - renomeie a pasta nova e devolva `awr-baterias-5571` para `awr-baterias`;
   - me envie o log de acesso.

## Rollback
Pasta `awr-baterias-5571`, ou o zip da 5.57.1.
