---
name: tutoriais-em-video
description: Grava tutoriais em vídeo de um sistema web sozinho, sem gravador de tela — o navegador faz cada passo, uma voz neural narra, e sai um MP4 Full HD com abertura, legenda, cursor animado e destaques. Use quando pedirem vídeos de tutorial, aulas, demonstração de produto, onboarding em vídeo ou "grave um vídeo mostrando como usar a tela X".
---

# Tutoriais em vídeo, gravados por código

Cada aula é um **roteiro**: uma lista de passos, cada um com uma FALA (vira
narração e legenda) e AÇÕES no navegador (clicar, digitar, destacar). O motor:

1. gera a narração de cada fala com voz neural e mede a duração;
2. abre o sistema num Chromium invisível (Playwright) e grava a janela em
   1920×1080, fazendo as ações enquanto a fala toca — **cada passo dura o que a
   fala dura**, então voz e imagem andam juntas;
3. junta o vídeo e as falas no FFmpeg e entrega o MP4.

Uma camada visual injetada na página desenha o que não existe no sistema:
abertura e encerramento com a marca, legenda, cursor que anda até o botão com
uma onda no clique, foco que escurece o resto, e um celular na tela (para
mostrar o lado do cliente: um chat simulado ou uma página real num iframe).

Resultado típico: aulas de 40 s a 1 min 30 s, ~7 MB cada, regraváveis num
comando quando a tela muda.

## Arquivos desta skill

| Arquivo | O que é |
|---|---|
| `scripts/motor.py` | o motor: `Config`, `Aula`, `Passo` e as ações |
| `scripts/overlay.js` | a camada visual (marca, legenda, cursor, foco, celular) |
| `scripts/mapear.py` | lista títulos, botões, campos e abas de telas, para escrever roteiros |
| `scripts/folha.py` | folha de contato de um vídeo (um quadro a cada N s), para revisar |
| `exemplo/aula_exemplo.py` | uma aula completa de exemplo, para copiar |

## Instalar (uma vez)

```sh
pip install playwright edge-tts imageio-ffmpeg mutagen
python -m playwright install chromium
```

O FFmpeg vem do `imageio-ffmpeg` (o que vem com o Playwright é limitado e não
serve). A voz é do `edge-tts` (vozes neurais da Microsoft; em pt-BR:
`pt-BR-AntonioNeural`, `pt-BR-FranciscaNeural`, `pt-BR-ThalitaMultilingualNeural`;
liste todas com `python -m edge_tts --list-voices`).

## Como fazer, passo a passo

1. **Suba o sistema local com dados de demonstração** realistas e datados do mês
   corrente. Tela vazia não ensina nada. Se as aulas mudam os dados, tenha um
   comando que recria a demo e rode antes de CADA aula (`Config.recriar_demo`).
2. **Mapeie as telas** antes de escrever: `python scripts/mapear.py <url-base>
   clientes,pedidos --usuario <login> --senha <senha>` (rotas sem a barra
   inicial). Ele grava `mapa/mapa.txt` com os nomes exatos de botões, rótulos e
   placeholders, e um print de cada tela. Roteiro escrito "de memória" quebra.
3. **Configure a marca e o login** num `Config` (cores, nome, rodapés, como
   entrar, endereço local que deve aparecer como o de produção).
4. **Escreva a aula** copiando `exemplo/aula_exemplo.py`. Regras de roteiro
   abaixo.
5. **Grave**: `python minha_aula.py`. Sai em `videos/NN-slug.mp4`.
6. **Revise de verdade**: `python scripts/folha.py videos/NN-slug.mp4` gera uma
   folha de contato; abra e olhe. Depois extraia 2 ou 3 quadros em tamanho real
   nos momentos-chave (o resultado de cada ação) e confira se a tela mostra o
   que a fala diz. Fala que não bate com a tela é o erro mais comum.
7. **Grave as aulas em lote** em segundo plano, com um registro por aula, e
   deixe a que falhar para uma repescagem no fim — uma falha não para as outras.

## Regras de roteiro

- **Abertura padronizada** ("Nesta aula, você vai…") e **encerramento** com o
  que a pessoa aprendeu e a próxima aula. Mesmo formato em todas.
- **Uma ideia por passo**, 1 ou 2 frases. Passo longo vira legenda ilegível.
- **Fala por extenso, legenda com números**: a voz lê melhor "seiscentos e
  quarenta reais"; a legenda fica melhor como "R$ 640,00". Use `legenda=` no
  passo quando as duas forem diferentes.
- **Sempre mostre o resultado** da ação (o toast, o status que mudou) com um
  foco, antes de passar adiante.
- **Dados fictícios assumidos**: placas, CPFs e telefones de faixas reservadas
  ou obviamente falsas; chave Pix aleatória que não existe. Vídeo de tutorial
  vai para a internet.
- **O lado do cliente** (o link que ele recebe, a página que ele aprova) entra
  no celular da tela: `celular_chat` para a mensagem, `celular_url` para a
  página real.
- Cenário que a demo não tem (uma chave cadastrada, uma fila montada) vai no
  `preparo` da aula: roda antes da gravação, numa janela sem vídeo.

## Armadilhas (todas aconteceram)

- **O Playwright não estica o vídeo.** Viewport menor que o tamanho do vídeo
  sai com faixa cinza. Grave com viewport = vídeo (1920×1080) e amplie o
  sistema com CSS `zoom` (o motor usa 125%). A camada visual cancela o zoom
  (`zoom: 1/Z`) para as coordenadas do Playwright valerem 1:1 nela.
- **Login salvo morre na segunda navegação** quando o sistema gira o token de
  renovação. Entre numa janela SEM vídeo, salve o `storage_state` e feche na
  hora; a gravação começa já logada.
- **Login pode exigir a origem certa** (CORS/CSRF): grave pela mesma porta que
  o sistema espera.
- **Botão no pé de diálogo comprido** às vezes "não recebe" o clique com o zoom.
  O motor move o cursor e, se o clique não passar em 5 s, aciona
  `el.click()` direto. Confira no vídeo que a ação aconteceu.
- **Campo que já vem preenchido** emenda o texto digitado. O motor limpa antes.
- **Texto de opção de `<select>`** pode ter travessão ou espaço sem quebra
  (U+00A0). O motor escolhe a primeira opção que CONTÉM o texto, normalizado.
- **Cabeçalho fixo cobre o botão** depois do scroll automático. O motor
  centraliza o alvo (`scrollIntoView({block:'center'})`) antes de clicar.
- **Navegação completa recria a página** e a camada some por um instante; o
  motor espera ela voltar antes de cada comando e repõe o selo da aula.
- **Endereço de desenvolvimento na tela** (`localhost:5173`): a camada troca
  pelo de produção só na exibição (`Config.trocas`).
- **Nome acessível ≠ texto do botão** (ex.: o botão mostra "Iniciar" mas o
  `aria-label` é "Iniciar o cronômetro de…"). Use regex ou confira no mapa.
- **Link com cara de botão**: `get_by_role("button")` não acha um `<a>`.
- No **Windows** com Smart App Control, executáveis como `psql.exe` podem ser
  bloqueados; mexa no banco por um script em Node/Python.
- **Antes de culpar o motor, leia o erro inteiro**: guarde o detalhe completo da
  exceção no registro do lote. Mensagem cortada esconde a causa.

## Publicar

MP4 com H.264 + AAC e `+faststart` toca direto no navegador. Para hospedar no
próprio sistema, sirva a pasta de vídeos com suporte a Range (Caddy, Nginx) e,
se o player for um iframe do próprio site, troque `X-Frame-Options DENY` por
`SAMEORIGIN` só nessa rota. Ou suba no YouTube como não listado e use o link.
