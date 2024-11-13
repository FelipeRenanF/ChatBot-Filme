import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
import sqlite3

# Configuração do banco de dados de filmes
def initialize_database():
    conn = sqlite3.connect("filmes.db")
    cursor = conn.cursor()
    
    # Criar a tabela de filmes se ela não existir
    cursor.execute('''CREATE TABLE IF NOT EXISTS filmes (
                      titulo TEXT PRIMARY KEY,
                      ano INTEGER,
                      genero TEXT,
                      sinopse TEXT)''')
    
    # Inserir uma lista ampliada de filmes
    filmes_exemplo = [
        ("O Poderoso Chefão", 1972, "Crime, Drama", "A saga da família mafiosa Corleone."),
        ("Clube da Luta", 1999, "Drama", "Um homem deprimido forma um clube de luta secreto."),
        ("Inception", 2010, "Ação, Sci-Fi", "Um ladrão entra nos sonhos das pessoas para roubar segredos."),
        ("Matrix", 1999, "Ação, Sci-Fi", "Um hacker descobre a verdade sobre sua realidade."),
        ("Forrest Gump", 1994, "Drama, Romance", "A vida extraordinária de um homem com baixa QI."),
        ("Pulp Fiction", 1994, "Crime, Drama", "Histórias entrelaçadas de violência e redenção em Los Angeles."),
        ("O Senhor dos Anéis: A Sociedade do Anel", 2001, "Aventura, Fantasia", "A jornada de Frodo para destruir o Um Anel."),
        ("Gladiador", 2000, "Ação, Drama", "Um general romano se torna um gladiador em busca de vingança."),
        ("Titanic", 1997, "Drama, Romance", "Uma história de amor no trágico naufrágio do Titanic."),
        ("A Origem", 2010, "Ação, Sci-Fi", "Um especialista em sonhos tenta realizar o golpe perfeito."),
        ("Interstellar", 2014, "Aventura, Drama, Sci-Fi", "Exploração espacial em busca de um novo lar para a humanidade."),
        ("Coringa", 2019, "Crime, Drama, Suspense", "A história da origem do vilão Joker."),
    ]
    
    # Inserir filmes no banco de dados, ignorando duplicatas
    cursor.executemany("INSERT OR IGNORE INTO filmes (titulo, ano, genero, sinopse) VALUES (?, ?, ?, ?)", filmes_exemplo)
    
    conn.commit()
    conn.close()

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Artemis")
        master.geometry("600x600")
        
        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)
        master.grid_rowconfigure(3, weight=0)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Olá! Eu sou a Artemis, sua assistente virtual. Como posso te ajudar hoje?\n")
        self.text_area.configure(state="disabled")
        
        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite sua pergunta aqui...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)
        
        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)
        
        # Botão de limpar
        self.clear_button = ctk.CTkButton(master, text="Limpar", fg_color="red", command=self.clear_text)
        self.clear_button.grid(row=3, column=0, padx=20, pady=10)

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return
        
        # Exibir a entrada do usuário
        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Você: " + user_input + "\n")
        
        # Obter e exibir a resposta do chatbot
        response = self.get_response(user_input)
        self.text_area.insert(ctk.END, "Artemis: " + response + "\n")
        self.text_area.configure(state="disabled")
        
        # Limpar o campo de entrada
        self.entry.delete(0, ctk.END)

    def get_response(self, user_input):
        # Verificar se a entrada do usuário se refere a um filme no banco de dados
        response = self.consultar_filme(user_input)
        if response:
            return response
        
        return "Desculpe, não consegui encontrar informações sobre isso."

    def consultar_filme(self, titulo):
        # Conectar ao banco de dados e procurar o filme
        conn = sqlite3.connect("filmes.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM filmes WHERE titulo LIKE ?", (f"%{titulo}%",))
        resultado = cursor.fetchone()
        
        conn.close()
        
        if resultado:
            titulo, ano, genero, sinopse = resultado
            return f"Título: {titulo}\nAno: {ano}\nGênero: {genero}\nSinopse: {sinopse}"
        else:
            return "Filme não encontrado no banco de dados."

    def clear_text(self):
        # Limpa a área de texto do chatbot
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", ctk.END)
        self.text_area.insert(ctk.END, "Chat limpo. Como posso te ajudar?\n")
        self.text_area.configure(state="disabled")

if __name__ == "__main__":
    initialize_database()  # Inicializar o banco de dados de filmes com dados de exemplo
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
