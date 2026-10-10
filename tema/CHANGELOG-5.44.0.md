# 5.44.0
- Foto nova no hero da home (técnico AWR com a bateria Moura AGM), recortada em quadrado para mostrar o rosto e a bateria inteiros.
- A foto agora fica dentro do próprio tema (assets/img/hero-awr-moura-640.webp, -960.webp e -960.jpg) — não depende mais do domínio do app. WebP de 43–69 KB; JPG só para navegador antigo.
- À prova de quebra: se o arquivo não existir, o bloco nem é impresso; se falhar ao carregar, ele some e a busca sobe. Nunca aparece ícone de imagem quebrada.
- Só o computador (≥1024px) baixa a foto; no celular nada é baixado.
- Corrigida uma regra antiga do awr-bundle.css que forçava a moldura em 16:9 (cortava a bateria e causaria salto de layout quando o CSS terminasse de carregar).
