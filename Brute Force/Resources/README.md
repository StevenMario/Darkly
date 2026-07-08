# Brute Force Attack

## Definition

A brute force attack is a cybersecurity method where hackers use trial-and-error automation to systematically guess passwords, encryption keys, or login credentials. Instead of exploiting software vulnerabilities, attackers use computational power to guess thousands of combinations per minute until they find the right one

## How it works
A vulnerable login page accepts authentication request without rate-limiting, account lockout , or CAPTCHA. This allows an attacker to submit thousands of password attempts in rapid succession using a wordlist.



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

## Exploit the vulnerability

### Vulnerable Page

```
http://10.11.200.86/?page=signin
```
A login form requiring a username and password.

### Steps

** 1. Analyse the request **

Open the browser and navigate to the sign-in page. Inspect the page and follow these steps:

- Open the Network tab in the browser developer tools.
- Click the Submit button on the sign-in form.
- Locate the network request triggered by the submission.
- You should see the request shown in the screenshot below:

![Request](./Screenshot%20from%202026-07-08%2014-56-22.png)


Analyzing the request shows that the form submits via **GET**:

```
GET /?page=signin&username=[username]&password=[p]&Login=Login
```

When wrong credentials are submitted, the server responds with an empty `<h2>` and a `WrongAnswer.gif` image. A successful login instead displays `The flag is : <hash>` with a `win.png` image.

** 2. Write a brute-force script **

The script `bruteforce.py` in this directory does the following:

1. **Probe**: sends a request with wrong credentials to capture the failure response.
2. **Iterate**: loops over 3 usernames (`root`, `admin`, `administrator`) and 63 passwords from `wordlist.txt`.
3. **Detect**: compares each response length against the failure baseline; a different length or the presence of "flag" marks a success.
4. **Report**: prints the valid credentials and the flag.

Key observations from building the script:
- The form uses `method="GET"`, not POST — parameters go in the URL.
- Required parameters: `page=signin`, `username`, `password`, `Login=Login`.
- No rate-limiting or CAPTCHA — the server accepts rapid sequential requests.

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

## References

- [OWASP - Brute Force Attack](https://owasp.org/www-community/attacks/Brute_force_attack)
- [CWE-307: Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html)

