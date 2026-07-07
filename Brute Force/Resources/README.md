# Brute Force Attack

## Definition

A brute force attack is a cybersecurity method where hackers use trial-and-error automation to systematically guess passwords, encryption keys, or login credentials. Instead of exploiting software vulnerabilities, attackers use computational power to guess thousands of combinations per minute until they find the right one

## How it works
A vulnerable login page accepts authentication request without rate-limiting,account lockout , or CAPTCHAT. This allows an attacker to submit thousands of password attempts in rapid succession using a wordlist.



## Attack Example

A user logs in by entering their correct username and password once:

```
POST /index.php?page=admin
username=root&password=secretpassword
→ Access granted
```

An attacker uses a wordlist of common passwords, trying each one until a successful login is found:

```
POST /index.php?page=admin
username=root&password=123456       → Access denied
username=root&password=password    → Access denied
username=root&password=qwerty      → Access denied
...
username=root&password=<match>     → Access granted ✅
```

## Exploite the vulnerability

### Vulnerable Page

```
http://10.11.200.86/?page=signin
```
A login form requiring a username and password.

### Steps

** 1. Analyse the request **

Install *Burp-Suite comunity edition* and open the page in the burpsuite browser.
Go to the page and try to sigin with randomn value to see the request

** 2. Write a brute-force script **

Analyzing the request shows that the form submits via **GET**:

```
GET /?page=signin&username=test&password=test&Login=Login
```

No error message appears on failure — the server just re-renders the same login form. A successful login would return a different page (different HTML length, contains the flag).

The script `bruteforce.py` in this directory does the following:

1. **Probe**: sends a request with obviously wrong credentials to record the failure response size (≈1990 bytes).
2. **Iterate**: loops over 3 usernames (`root`, `admin`, `administrator`) and 63 passwords from `wordlist.txt`.
3. **Detect**: for each attempt, compares the response size against the failure baseline. Any response with a different length or containing the word "flag" is a match.
4. **Report**: prints the valid credentials and the flag.

Key observations from building the script:
- The form uses `method="GET"`, not POST — parameters go in the URL.
- Required parameters: `page=signin`, `username`, `password`, `Login=Login`.
- No rate-limiting or CAPTCHA — the server accepts rapid sequential requests.
- The failure response is always 1990 bytes; the success response is noticeably different.

** 3. Run the exploit **

```
$ python3 bruteforce.py
[*] Probing failure response …
[*] Failure baseline: 1990 bytes
[*] Loaded 63 passwords, trying 3 username(s)

[+] SUCCESS after 20 attempts (38.7s)
    username = root
    password = shadow
    -> The flag is : b3a6e43ddf8b4bbb4125e5e7d23040433827759d4de1c04ea63907479a80a6b2
```

The credentials are `root` / `shadow`. The flag is the 64-character SHA-256 hash displayed in the success response.

## Mitigation

- **Rate limiting**: limit the number of requests per IP per minute.
- **Account lockout**: lock the account after N failed attempts.
- **CAPTCHA**: require solving a CAPTCHA after a few failed logins.
- **Strong password policy**: enforce minimum complexity to resist wordlist attacks.

