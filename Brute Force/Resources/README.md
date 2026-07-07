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

