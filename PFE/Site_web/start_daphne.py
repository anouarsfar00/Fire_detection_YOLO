import subprocess
import os

# Définir les variables d’environnement Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Site_web.settings")

# Lancer Daphne comme si on tapait la commande dans le terminal
subprocess.run([
    "daphne",
    "-b", "127.0.0.1",
    "-p", "8010",
    "Site_web.asgi:application"
])
