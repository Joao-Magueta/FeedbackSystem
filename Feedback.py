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
    if admin_logged_in:
        admin_win = Toplevel(root)
        admin_win.title("Área de Admin")
        
        Label(admin_win, text="Empresa ID").grid(row=0, column=0)
        Label(admin_win, text="Nome Empresa").grid(row=1, column=0)
        Label(admin_win, text="Descricao Empresa").grid(row=2, column=0)
        Label(admin_win, text="Contato").grid(row=3, column=0)
        
        empresa_id_var = StringVar()
        nome_empresa_var = StringVar()
        descricao_empresa_var = StringVar()
        contato_var = StringVar()
        
        empresa_id_entry = Entry(admin_win, textvariable=empresa_id_var)
        nome_empresa_entry = Entry(admin_win, textvariable=nome_empresa_var)
        descricao_empresa_entry = Entry(admin_win, textvariable=descricao_empresa_var)
        contato_entry = Entry(admin_win, textvariable=contato_var)
        
        empresa_id_entry.grid(row=0, column=1)
        nome_empresa_entry.grid(row=1, column=1)
        descricao_empresa_entry.grid(row=2, column=1)
        contato_entry.grid(row=3, column=1)
        
        Button(admin_win, text="Add Empresa", command=add_empresa).grid(row=4, column=0, columnspan=2)
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


# Função para registrar um usuário
def register_user():
    username = username_var.get()
    password = password_var.get()
    cur.execute("SELECT COUNT(*) FROM CredenciaisEmpresa")
    count = cur.fetchone()[0] + 1
    cur.execute("INSERT INTO CredenciaisEmpresa (EmpresaID, NomeUsuario, Senha) VALUES (?, ?, ?)", (count, username, password))
    cur.execute("INSERT INTO Empresa (EmpresaID) VALUES (?)", (count,))
    con.commit()
    messagebox.showinfo(title='Register User', message='User registered successfully')

# Função para adicionar uma empresa
def add_empresa():
    empresa_id = empresa_id_var.get()
    nome_empresa = nome_empresa_var.get()
    descricao_empresa = descricao_empresa_var.get()
    contato = contato_var.get()
    cur.execute("UPDATE Empresa SET NomeEmpresa=?, DescricaoEmpresa=?, Contato=? WHERE EmpresaID=?", (nome_empresa, descricao_empresa, contato, empresa_id))
    con.commit()
    print("Empresa added successfully")

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
    
    # Mensagem com base na análise de sentimento
    messagebox.showinfo(title='Enviar Feedback', message=f'Obrigado pelo seu feedback, seus comentários foram enviados.\nAnálise de Sentimento: {sentimento}')
    clear()

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
username_var = StringVar()
password_var = StringVar()
empresa_id_var = StringVar()
nome_empresa_var = StringVar()
descricao_empresa_var = StringVar()
contato_var = StringVar()

admin_button = ttk.Button(frame_content, text='Area dos Administradores', command=open_login_window).grid(row=5, column=1, sticky='w')
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