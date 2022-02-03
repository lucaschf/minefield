## Campo Minado

O presente projeto foi desenvolvido com o objetivo de colocar em prática os conceitos aprendidos na disciplina de Sistemas Distribuídos. Trata-se de uma adaptação do jogo Campo Minado, onde, conforme o proposto, a turma desenvolveu um jogo simples de rede com suporte para múltiplos jogadores, adaptando o jogo original para que fosse possível a participação de 1 a 4 jogadores, existindo um mecanismo de rodadas onde a ordem de jogada é definida pela ordem de chegada dos jogadores. Além disso, o tamanho do tabuleiro e a quantidade de bombas varia de acordo com o número de jogadores, os mesmos perdem o jogo caso excedam o tempo definido para sua jogada, percam a conexão ou cliquem em uma bomba, em caso de empate, a pontuação dos jogadores será o critério para definir o vencedor.

### Sobre

Trabalho prático desenvolvido no curso de Tecnologia em Sistemas para Internet pertencente ao Instituto Federal do Sudeste de Minas Gerais, campus Barbacena na disciplina de Sistemas Distribuídos, ministrada pelo professor [Rafael Alencar](https://github.com/rafjaa).

### Instruções


É necessário que seu ambiente tenha python 3 instalado.

No terminal, rode os seguintes comandos:

Para instalar os módulos:
```markdown
pip install -r requirements.txt
```
Para iniciar o servidor:
```markdown
python game_server.py
```
Para cada jogador que desejar conectar, com limite de 4 jogadores por rodada:
```markdown
python minesweeper_gui.py
```

Para iniciar o jogo, um dos jogadores deve selecionar a opção "Entrar na partida" no menu Jogo, a partir disso os jogadores terão um tempo limitado para entrar na partida.

### Vídeo 

Para ver um vídeo do jogo em funcionamento, [clique aqui](https://youtu.be/_LjcQSGbxI4).

