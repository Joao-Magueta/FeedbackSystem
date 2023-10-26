from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from textblob import TextBlob


#Analise de sentimento
def analisar_sentimento(texto):
    analysis = TextBlob(texto)
    polaridade = analysis.sentiment.polarity
    if polaridade > 0:
        return "positivo"
    elif polaridade < 0:
        return "negativo"
    else:
        return "neutro"

def clear():
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    textcomment.delete(1.0, END)

def submit():
    nome = myvar.get()
    email = var.get()
    comentario = textcomment.get(1.0, END)

    
    sentimento = analisar_sentimento(comentario)
# Mensagem com base na análise de sentimento
    messagebox.showinfo(title='Enviar Feedback', message=f'Obrigado pelo seu feedback, seus comentários foram enviados.\nAnálise de Sentimento: {sentimento}')
    clear()
    
    #FRONT

root = Tk()
frame_header = ttk.Frame(root)
frame_header.pack()
logo = PhotoImage(file='logo.gif').subsample(2, 2)
logolabel = ttk.Label(frame_header, text='logomarca', image=logo)
logolabel.grid(row=0, column=0, rowspan=2)
headerlabel = ttk.Label(frame_header, text='FEEDBACK DO CLIENTE', foreground='orange',
                        font=('Arial', 24))
headerlabel.grid(row=0, column=1)
messagelabel = ttk.Label(frame_header,
                         text='POR FAVOR, NOS DIGA O QUE VOCÊ PENSA',
                         foreground='purple', font=('Arial', 10))
messagelabel.grid(row=1, column=1)

frame_content = ttk.Frame(root)
frame_content.pack()

myvar = StringVar()
var = StringVar()

namelabel = ttk.Label(frame_content, text='Nome')
namelabel.grid(row=0, column=0, padx=5, sticky='sw')
entry_name = ttk.Entry(frame_content, width=18, font=('Arial', 14), textvariable=myvar)
entry_name.grid(row=1, column=0)

emaillabel = ttk.Label(frame_content, text='E-mail')
emaillabel.grid(row=0, column=1, sticky='sw')
entry_email = ttk.Entry(frame_content, width=18, font=('Arial', 14), textvariable=var)
entry_email.grid(row=1, column=1)

commentlabel = ttk.Label(frame_content, text='Comentário', font=('Arial', 10))
commentlabel.grid(row=2, column=0, sticky='sw')
textcomment = Text(frame_content, width=55, height=10)
textcomment.grid(row=3, column=0, columnspan=2)

textcomment.config(wrap='word')

submitbutton = ttk.Button(frame_content, text='Enviar', command=submit).grid(row=4, column=0, sticky='e')
clearbutton = ttk.Button(frame_content, text='Limpar', command=clear).grid(row=4, column=1, sticky='w')

mainloop()