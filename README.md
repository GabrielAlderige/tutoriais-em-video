# Tutoriais em vídeo (skill do Claude Code)

Grava tutoriais em vídeo de um sistema web **sem gravador de tela e sem ninguém
na frente do computador**. Você escreve um roteiro com o que falar e o que fazer
em cada passo; o navegador executa, uma voz neural em português narra, e sai um
MP4 Full HD com abertura, legenda, cursor animado, destaques e até um celular na
tela mostrando o lado do cliente.

Foi criada para gravar o curso de 24 aulas do OficinaOS (sistema de gestão para
oficinas mecânicas) e generalizada para qualquer sistema web.

## Instalar

Como skill do Claude Code (o Claude passa a usar sozinho quando você pedir um
tutorial em vídeo):

```sh
git clone https://github.com/GabrielAlderige/tutoriais-em-video.git ~/.claude/skills/tutoriais-em-video
```

No Windows: `C:\Users\<você>\.claude\skills\tutoriais-em-video`.

E as dependências, uma vez:

```sh
pip install playwright edge-tts imageio-ffmpeg mutagen
python -m playwright install chromium
```

Depois é só pedir ao Claude Code: *"grave um tutorial em vídeo mostrando como
cadastrar um pedido no meu sistema"*. O sistema precisa estar rodando local,
com dados de demonstração.

## Usar sem o Claude

Também funciona sozinho: copie `exemplo/aula_exemplo.py`, ajuste a `Config`
(endereço, login, marca) e os passos, e rode `python aula_exemplo.py`.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `SKILL.md` | instruções da skill: passo a passo, regras de roteiro e as armadilhas conhecidas |
| `scripts/motor.py` | o motor (Playwright + voz neural + FFmpeg) |
| `scripts/overlay.js` | a camada visual: abertura, legenda, cursor, foco, celular |
| `scripts/mapear.py` | lista botões e campos das telas, para escrever roteiros |
| `scripts/folha.py` | folha de contato de um vídeo, para revisar |
| `exemplo/aula_exemplo.py` | uma aula completa para copiar |

## Como funciona

Cada passo tem uma FALA e AÇÕES. O motor gera a narração (edge-tts), mede a
duração e grava o navegador fazendo as ações enquanto a fala toca, então cada
passo dura o que a fala dura. No fim, o FFmpeg junta o vídeo e as falas nos
instantes certos. Detalhes e armadilhas em [`SKILL.md`](SKILL.md).

## Licença

MIT. Use, adapte e distribua à vontade.
