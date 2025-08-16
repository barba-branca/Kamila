import webbrowser
import subprocess
import os

def abrir_site(url):
    webbrowser.open(url)

def abrir_programa(nome_arquivo):
    caminho = f"C:\\Program Files\\{nome_arquivo}"
    subprocess.Popen(caminho)

def pesquisar_na_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
