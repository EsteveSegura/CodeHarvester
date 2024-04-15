import subprocess
import sys
import webbrowser

def open_url_in_browser(url):
    try:
        if sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        elif sys.platform.startswith('win'):
            subprocess.run(['start', url], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        else:
            print(f"Plataforma no soportada: {sys.platform}")
            return False
        return True
    except Exception as e:
        print(f"Error al abrir el navegador: {e}")
        return False