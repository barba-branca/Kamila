Set WshShell = CreateObject("WScript.Shell")
' Sintaxe correta para executar: pythonw.exe [espaço] script.py
' O '0' esconde a janela e 'False' não espera o script terminar
WshShell.Run """D:\Projetos\kamila\.venv\Scripts\pythonw.exe"" ""D:\Projetos\kamila\.kamila\main.py""", 0, False
Set WshShell = Nothing