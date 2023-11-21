from tkinter import *
from tkinter import ttk, messagebox
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import sqlite3 as sql

# Conectar ao banco de dados SQLite
con = sql.connect("FeedbackDB.db")
cur = con.cursor()

# Variável global para controlar o login do administrador
admin_logged_in = False


# Função para realizar o login
def login():
    global admin_logged_in
    username = username_var.get()
    password = password_var.get()
    cur.execute("SELECT * FROM Administrador WHERE NomeUsuario=? AND Senha=?", (username, password))
    if cur.fetchone():
        admin_logged_in = True
        login_win.destroy()  # Fecha a janela de login após o login bem-sucedido
        admin_window()
    else:
        messagebox.showerror(title='Login', message='Login failed')

# Função para a área de administração
def admin_window():
    global usuario_var
    global senha_var
    if admin_logged_in:
        admin_win = Toplevel(root)
        admin_win.title("Área de Admin")
        
        Label(admin_win, text="Empresa ID").grid(row=0, column=0)
        Label(admin_win, text="Nome Empresa").grid(row=1, column=0)
        Label(admin_win, text="Descricao Empresa").grid(row=2, column=0)
        Label(admin_win, text="Contato").grid(row=3, column=0)
        Label(admin_win, text="Usuario").grid(row=4, column=0)
        Label(admin_win, text="Senha").grid(row=5, column=0)
        
        empresa_id_var = StringVar()
        usuario_var = StringVar()
        senha_var = StringVar()
        
        empresa_id_entry = Entry(admin_win, textvariable=empresa_id_var)
        nome_empresa_entry = Entry(admin_win, textvariable=nome_empresa_var)
        descricao_empresa_entry = Entry(admin_win, textvariable=descricao_empresa_var)
        contato_entry = Entry(admin_win, textvariable=contato_var)
        usuario_entry = Entry(admin_win, textvariable=usuario_var)
        senha_entry = Entry(admin_win, textvariable=senha_var)
        
        empresa_id_entry.grid(row=0, column=1)
        nome_empresa_entry.grid(row=1, column=1)
        descricao_empresa_entry.grid(row=2, column=1)
        contato_entry.grid(row=3, column=1)
        usuario_entry.grid(row=4, column=1)
        senha_entry.grid(row=5, column=1 )
        
        Button(admin_win, text="Add Empresa", command=lambda: add_empresa(nome_empresa_var.get(), descricao_empresa_var.get(), contato_var.get(), usuario_var.get(), senha_var.get())).grid(row=6, column=0, columnspan=2)

    else:
        messagebox.showerror(title='Acesso Negado', message='Você deve fazer o login como administrador para acessar esta área.')


# Função para abrir a janela de login
def open_login_window():
    global login_win
    login_win = Toplevel(root)
    login_win.title("Login")
    
    Label(login_win, text="Username").grid(row=0, column=0)
    Label(login_win, text="Password").grid(row=1, column=0)
    
    global username_var
    global password_var
    username_var = StringVar()
    password_var = StringVar()
    
    username_entry = Entry(login_win, textvariable=username_var)
    password_entry = Entry(login_win, textvariable=password_var, show="*")
    
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)
    
    Button(login_win, text="Login", command=login).grid(row=2, column=0, columnspan=2)


# Função para adicionar uma empresa
def add_empresa(nome_empresa, descricao_empresa, contato, usuario, senha):
    nome_empresa = nome_empresa_var.get()
    descricao_empresa = descricao_empresa_var.get()
    contato = contato_var.get()
    usuario = usuario_var.get()  
    senha = senha_var.get()  

 
    cur.execute("INSERT INTO Empresa (NomeEmpresa, DescricaoEmpresa, Contato) VALUES (?, ?, ?)", (nome_empresa, descricao_empresa, contato))
    empresa_id = cur.lastrowid  

    
    cur.execute("INSERT INTO CredenciaisEmpresa (EmpresaID, NomeUsuario, Senha) VALUES (?, ?, ?)", (empresa_id, usuario, senha))
    
    con.commit()
    print("Empresa adicionada")
    
    #Função do botão Ler Comentarios
def ler_comentarios():
    
    cur.execute("SELECT * FROM Feedback")
    comentarios = cur.fetchall()

    
    pagina = Toplevel(root)
    pagina.title("Comentários")

   
    frame = Frame(pagina)
    frame.pack()


    label = Label(frame, text="Comentários")
    label.grid(row=0, column=0)

    
    table = ttk.Treeview(frame)
    table["columns"] = ["Nome", "Feedback", "Sentimento"]
    table.column("#0", width=0, stretch=NO)
    table.column("Nome", width=100)
    table.column("Feedback", width=300)
    table.column("Sentimento", width=100)

    table.heading("Nome", text="Nome")
    table.heading("Feedback", text="Feedback")
    table.heading("Sentimento", text="Sentimento")

    # não repetir linhas usando o ID
    comentario_ids = set()

 
    for comentario in comentarios:
   
        comentario_id = comentario[0]

        
        if comentario_id in comentario_ids:
            continue

        
        comentario_ids.add(comentario_id)

       
        sentimento = comentario[2]

        
        comentario_texto = comentario[3]


        nome = comentario[4]

        # Adiciona a entrada na tabela
        table.insert("", END, values=(nome, comentario_texto, sentimento))

    table.grid(row=1, column=0, columnspan=2)

    return pagina



# Função para traduzir o feedback do português para o inglês
def traduzir_para_ingles(texto):
    translator = Translator()
    translated = translator.translate(texto, src='pt', dest='en')
    return translated.text

# Função para análise de sentimento 
def analisar_sentimento(texto):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(texto)
    compound_score = sentiment['compound']
    
    if compound_score >= 0.05:
        return "positivo"
    elif compound_score <= -0.05:
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

    comentario_ingles = traduzir_para_ingles(comentario)
    
    sentimento = analisar_sentimento(comentario_ingles)
    
    # Armazena a análise de sentimento
    cur.execute(
        "INSERT INTO Feedback  (Comentarios, Classificacao, Nome, EMAIL  ) VALUES (?, ?, ?, ?)", (comentario, sentimento, nome, email),
        
    )
    con.commit()
    
    # Mensagem com base na análise de sentimento
    messagebox.showinfo(title='Enviar Feedback', message=f'Obrigado pelo seu feedback, seus comentários foram enviados.\nAnálise de Sentimento: {sentimento}')
    clear()
    
    #FRONT

root = Tk()
frame_header = ttk.Frame(root)
frame_header.pack()

#logo = PhotoImage(file='logo.gif').subsample(2, 2)
#logolabel = ttk.Label(frame_header, text='logomarca', image=logo)
#logolabel.grid(row=0, column=0, rowspan=2)
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
username_var = StringVar()
password_var = StringVar()
empresa_id_var = StringVar()
nome_empresa_var = StringVar()
descricao_empresa_var = StringVar()
contato_var = StringVar()

admin_button = ttk.Button(frame_content, text='Acesso Administradores', command=open_login_window).grid(row=5, column=1, sticky='w')
botao_leitura = ttk.Button(frame_content, text="Ler Comentários", command=ler_comentarios).grid(row=6, column=1, columnspan=2)
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



root.mainloop()