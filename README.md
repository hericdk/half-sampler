# ½ sampler (FM-½ Sampler)

Um sampler grátis que roda no navegador. Toque com o teclado do computador, o celular, um controle de videogame ou qualquer teclado MIDI.
Ele foi feito para o **M-VAVE FM-1**: o nome quer dizer que ele é *meio* sampler, e a outra metade é o FM-1.

**Abra e toque, sem instalar: https://sampler.half.social**

*A free sampler that runs in the browser. Play it with your computer keyboard, your phone, a gamepad or any MIDI keyboard. Made for the M-VAVE FM-1: it is "half" a sampler, the FM-1 is the other half.*

## O que ele faz
- 48 pads em 4 grupos, com fatias, notas (KEYS), envelope, filtros e afinação.
- Grave pelo microfone ou importe áudio; corte, junte e fatie os sons.
- Biblioteca de sons sintetizados aqui mesmo, por estilo (Trap, Techno, Hip-Hop, Jazz, RPG...), e bases prontas que tocam em loop.
- Faixas para gravar o que você toca, efeitos (eco, reverb, PUNCH, PARTY...) e visualizadores.
- Atalhos de teclado, MIDI e gamepad que você mesmo configura.
- Manda samples e temas para o FM-1 pela USB (SysEx).
- Interface em português, inglês, espanhol, francês, japonês e coreano.

## Rodar no seu computador
```bash
python3 serve.py
```
Depois abra http://localhost:5217/.

O `serve.py` é opcional. A página funciona sozinha, mas com ele você ganha:
- trechos de vídeos do YouTube e do Instagram, que precisam do [yt-dlp](https://github.com/yt-dlp/yt-dlp) e do ffmpeg;
- separação de instrumentos com o [Demucs](https://github.com/adefossez/demucs), instalado num venv em `~/.local/share/fm1-stems`;
- sua própria biblioteca de sons: arquivos de áudio numa pasta `sons/` (cada subpasta vira uma categoria).

Para gerar a versão de publicar (a pasta `online/`), rode `python3 build-online.py`.

## Arquivos
- `index.html`: o app inteiro, num arquivo só (estilo, HTML e JS).
- `sampler-i18n.js`: as traduções. Cada linha é `[pt, en, es, fr, ja, ko]`.
- `vis/`: os visualizadores.
- `serve.py`: o servidor local.
- `build-online.py`: gera a versão de publicar.

## Licença
[AGPL-3.0](LICENSE). Use, estude, mude e compartilhe à vontade.
O que nasce daqui continua livre: se você distribuir uma versão modificada, ou colocar uma no ar como site, o código dela também tem que ser aberto, com a mesma licença.
