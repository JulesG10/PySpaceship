# Spaceship


> Lancer le jeu

```
python -m spaceship
```

Ou

```
python run.py
```

| Argument   |         Action         | type |
| ---------- | :--------------------: | :--: |
| width      | largeur de la fenêtre  | int  |
| height     | hauteur de la fenêtre  | int  |
| fullscreen |      plein ecran       | bool |
| server     | démarer en mode server | bool |

> Lancer le build


```cmd
python -m PyInstaller --clean --windowed --noconsole --collect-all=spaceship run.py
```

## Rapport des versions

> 1.0.0

- udp server en cours de création
- udp client bug socket no close
- udp bug thread not close
- gameover screen

> 1.1.0

- changement udp vers tcp (optimisation pour le thread render count)
- tcp fix thread no close
  - 1.1.1
- tcp fix client - server kill socket
  - 1.1.2
- args parser custom option en cour
  - 1.1.3
- calcul du viewport pour le fullscreen
  - ajustement
  - render optimisation avec la strech resolution
  - render avec custom resolution
  - 1.1.4

> 1.2.0

- fix tcp client - server exption handling error
  - 1.2.1
- fix back button pour le menu solo multi
  - 1.2.3

> 1.3.0 (no backup)
- camera client test
- fix encoding bug (bytearray)
  - 1.3.1
- game sync entity
  - 1.3.2
- solo game
  - score
  - kill + (fix kill bug)
  - 1.3.3
- new player velocity system
  - utilise équation de mouvement newton
  - 1.3.4

> 1.4.0

- map
  - chunk system optimisation
  - tile rendering optimisation
  - sync map loading
  - sprite optimisation
  - 1.4.1
- player
  - velocity system
  - angle + mouvement
  - 1.4.2
- settings update
  - 1.4.3
-  gui key input fix (space)
  - 1.4.4

> 1.5.0

- tcp bug fix
  - packet recieve & send bug
  - 1.5.1
- filter packet optimisation
  - large buffer
  - 1.5.2
- bullet entity + player state management
  - 1.5.3
- server/client ticks system
  - 1.5.4

> 1.6.0

- fix multiplayer bug
  - 1.6.1
- fix engine vec, calc bug
  - 1.6.2
- midleware + share components
  - 1.6.3
- optimise entity state client/server
  - 1.6.4
- (beta) multi level
  - 1.6.5
- jeux multi (alpha)
  - 1.6.6
- build to exe 
  - 1.6.7


> TODO

- particules system
- plugin system
- collision multi
- fix release console bug
- ~~gestion input/output client/server~~
- ~~camera~~
- ~~screen flip, update optimisation~~


## Licence

MIT License

Copyright (c) 2020 Jules GARCIA

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
