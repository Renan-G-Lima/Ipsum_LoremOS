import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox

#Botao Super
#Abre o menu principal do sistema (ainda com opções placeholder)
menu_open = False

#Config visual do "desktop"
TASKBAR_HEIGHT = 45
MENU_HEIGHT = 140
MENU_WIDTH = 220
BACKGROUND_COLOR = "#0078D7"
TASKBAR_COLOR = "#2d2d2d"
MENU_COLOR = "#333333"
SELECTION_COLOR = "#ff0000"  # cor sólida para retângulo de seleção

#inicia a janela principal do sistema
root = tk.Tk()
root.title("WCA Operacional System")
root.geometry("900x600")
root.configure(bg=BACKGROUND_COLOR)

#desktop (área principal onde ícones/janelas vão aparecer)
desktop = tk.Canvas(root, bg=BACKGROUND_COLOR, highlightthickness=0)
desktop.pack(fill="both", expand=True)

#taskbar (barra inferior)
taskbar = tk.Frame(root, bg=TASKBAR_COLOR, height=TASKBAR_HEIGHT)
taskbar.pack(side="bottom", fill="x")


#Botao Super
#Abre o menu (ainda vazio, com placeholders para funcionalidades futuras)
def super_button_action():
    global menu_open
    if menu_open:
        menu_frame.place_forget()
        menu_open = False
    else:
        x = 10
        y = root.winfo_height() - TASKBAR_HEIGHT - MENU_HEIGHT
        menu_frame.place(x=x, y=y, width=MENU_WIDTH, height=MENU_HEIGHT)
        menu_open = True

menu_button = tk.Button(
    taskbar,
    text="SUPER",
    bg="#3a3a3a",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    activebackground="#4a4a4a",
    command=super_button_action
)
menu_button.pack(side="left", padx=10, pady=5)

#Botao Camera
#Abre o app de câmera (tem modos: normal, gestos)
def abrir_camera():
    # tenta importar o detector de mãos (cvzone -> mediapipe)
    try:
        from cvzone.HandTrackingModule import HandDetector # --- não descobri como resolver
    except Exception:
        messagebox.showerror(
            "Dependência faltando",
            "cvzone/mediapipe não disponível neste Python.\n"
            "Use o venv com python3.11 onde instalou mediapipe/cvzone."
        )
        return

    #janela da camera
    janela_camera = tk.Toplevel(root)
    janela_camera.title("Câmera - We_OS")
    janela_camera.geometry("800x600")
    janela_camera.configure(bg="black")

    #modo atual da camera: normal ou gestos
    modo = tk.StringVar(value="normal")

    #topo com botões de modo
    frame_top = tk.Frame(janela_camera, bg="#2d2d2d")
    frame_top.pack(fill="x")

    tk.Radiobutton(frame_top, text="Normal", variable=modo, value="normal",
                   bg="#2d2d2d", fg="white", selectcolor="#0078D7",
                   indicatoron=0, width=10).pack(side="left", padx=5, pady=5)

    tk.Radiobutton(frame_top, text="Gestos", variable=modo, value="gestos",
                   bg="#2d2d2d", fg="white", selectcolor="#0078D7",
                   indicatoron=0, width=10).pack(side="left", padx=5, pady=5)

    #aqui vai: mais controles (ex.: salvar, configurações de detector)

    #area onde o vídeo vai ser mostrado
    label_video = tk.Label(janela_camera, bg="black")
    label_video.pack(fill="both", expand=True)

    #inicia captura da webcam e detector de mãos
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.7, maxHands=1)

    #verifica se a câmera abriu
    ret, frame0 = cap.read()
    if not ret:
        messagebox.showerror("Câmera", "Não foi possível abrir a câmera.")
        cap.release()
        janela_camera.destroy()
        return

    #captura os frames da webcam de forma horizontal (espelho)
    def atualizar_frame():
        ret, frame = cap.read()
        if not ret:
            label_video.after(50, atualizar_frame)
            return

        frame = cv2.flip(frame, 1)  # espelha o frame (como um espelho)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #modo normal: apenas preview bruto (aqui dá pra adicionar filtros)
        if modo.get() == "normal":
            pass  #aqui vai: filtros, ajuste brilho/contraste

        #modo gestos: desenha o esqueleto da mão e mostra ponta do indicador
        elif modo.get() == "gestos":
            hands, frame_rgb = detector.findHands(frame_rgb, draw=True)
            if hands:
                try:
                    lmList = hands[0]['lmList']  #lista de landmarks [x, y]
                    x8, y8 = int(lmList[8][0]), int(lmList[8][1])  #ponta do indicador
                    cv2.circle(frame_rgb, (x8, y8), 12, (255, 0, 0), -1)  #marca a ponta
                except Exception:
                    #se algo falhar no parsing dos landmarks, ignora e segue
                    pass

        #converte para imagem do Tk e mostra
        try:
            imagem = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            label_video.configure(image=imagem)
            label_video.image = imagem
        except Exception:
            pass

        label_video.after(15, atualizar_frame)

    atualizar_frame()

    #fecha a camera ao sair da janela
    def ao_fechar():
        try:
            cap.release()
        except Exception:
            pass
        janela_camera.destroy()

    janela_camera.protocol("WM_DELETE_WINDOW", ao_fechar)


camera_button = tk.Button(
    taskbar,
    text="Câmera",
    bg="#3a3a3a",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    activebackground="#4a4a4a",
    command=abrir_camera
)
camera_button.pack(side="left", padx=5, pady=5)

#Menu invisivel por enquanto
#aqui vai: opções do menu principal (explorador, terminal, configs, etc.)
menu_frame = tk.Frame(desktop, bg=MENU_COLOR, bd=1, relief="solid")

#Relogio do sistema
#mostra hora na taskbar
clock_label = tk.Label(taskbar, bg=TASKBAR_COLOR, fg="white", font=("Segoe UI", 10))
clock_label.pack(side="right", padx=15)
def update_clock():
    clock_label.config(text=time.strftime("%H:%M:%S"))
    root.after(1000, update_clock)
update_clock()

#Selecao de area
#cria retangulo de seleção ao arrastar na área de trabalho
selection_rect = None
start_x = None
start_y = None

def start_selection(event):
    global start_x, start_y, selection_rect
    if event.y > root.winfo_height() - TASKBAR_HEIGHT:
        return
    start_x = desktop.canvasx(event.x)
    start_y = desktop.canvasy(event.y)
    #cria retângulo (só contorno)
    selection_rect = desktop.create_rectangle(start_x, start_y, start_x, start_y,
                                              outline=SELECTION_COLOR, width=1)

def update_selection(event):
    global selection_rect
    if selection_rect:
        cur_x = desktop.canvasx(event.x)
        cur_y = desktop.canvasy(event.y)
        desktop.coords(selection_rect, start_x, start_y, cur_x, cur_y)

def end_selection(event):
    global selection_rect
    if selection_rect:
        desktop.delete(selection_rect)
        selection_rect = None

desktop.bind("<ButtonPress-1>", start_selection)
desktop.bind("<B1-Motion>", update_selection)
desktop.bind("<ButtonRelease-1>", end_selection)

#ajusta posicao do menu quando a janela for redimensionada
def update_menu_position(event):
    if menu_open:
        x = 10
        y = event.height - TASKBAR_HEIGHT - MENU_HEIGHT
        menu_frame.place(x=x, y=y, width=MENU_WIDTH, height=MENU_HEIGHT)

root.bind("<Configure>", update_menu_position)

#aqui vai: painel do explorador de arquivos (futura implementação)
#aqui vai: terminal integrado (futura implementação)
#aqui vai: painel de configuracoes do We_OS (futura implementação)
#aqui vai: gerenciador de janelas simples (futura implementação)
#aqui vai: integração com gestos para clicar/arrastar (futura implementação)

#inicia o loop principal do sistema
root.mainloop()
