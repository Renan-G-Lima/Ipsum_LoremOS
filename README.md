O objetivo é criar um sistema operacional simulado em Python com interface gráfica, que funcione como um desktop real, permitindo interação via mouse, teclado, câmera e possivelmente gestos no futuro. O foco é aprendizado e prototipagem de interfaces, automação e visão computacional.

A estrutura do Projeto é simples

1. Desktop Principal

Canvas principal que simula área de trabalho.

Taskbar com relógio, botões de acesso rápido (Super, Câmera, etc.).

Sistema de seleção de áreas com mouse.

2. Menu “Super”

Abre um menu lateral.

Aqui vão os atalhos para módulos do OS.

Menu deve ser flutuante e se reposicionar automaticamente.

3. Botão Câmera

Abre janela separada com feed de webcam.

Modos:

Normal: mostra vídeo puro da webcam.

Gestos: detecta mãos e exibe pontos de referência.

Escrita aérea: futura funcionalidade para desenhar ou escrever com o dedo no ar.

4. Seleção de Área

Permite clicar e arrastar para selecionar regiões do desktop.

Reforçar que é apenas visual, sem ação real por enquanto.

5. Clock

Relógio atualizado a cada segundo no taskbar.

6. Futuro/Extras

Explorar integração com:

Gestos mais avançados.

Manipulação de arquivos virtuais.

Terminal embutido.

Pequenas animações ou notificações.

Comunicação com rede local e/ou APIs.
