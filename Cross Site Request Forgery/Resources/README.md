# CSRF (Cross-Site Request Forgery)

## Definition

CSRF (Cross-Site Request Forgery) is a web vulnerability that allows an attacker to force an authenticated user to perform unintended actions on a web application without their knowledge by forging HTTP requests.

---

## How It Works

A vulnerable application accepts requests without verifying that they genuinely originate from the legitimate user.

If the request uses the `GET` method with parameters directly in the URL, an attacker can forge it easily.

---

## Normal Example

A user requests a password reset by submitting their email:

```http
http://site.com/?page=recover&mail=user@example.com
```

The server sends a reset link to:

```txt
user@example.com
```

---

## Attack Example

An attacker forges the request and replaces the email with their own:

```http
http://site.com/?page=recover&mail=attacker@evil.com
```

The server sends the reset link to:

```txt
justsomething@gmail.com
```

This may allow the attacker to take control of the victim’s account.

---

# Stages of Operation

## 1. Identify a Vulnerable Form or Endpoint

Look for forms or actions that:

- Use the `GET` or `POST` method with parameters in the URL
- Do not include a CSRF token
- Require no additional confirmation from the user

---

## 2. Check for the Absence of a CSRF Token

Inspect the page source (`Ctrl + U`) and look for the form:

```html
<!-- Vulnerable form — no CSRF token -->
<form action="#" method="POST">
  <input type="text" name="mail">
  <input type="submit" value="Submit">
</form>
```

If there is no hidden field like:

```html
<input type="hidden" name="csrf_token" value="a1b2c3...">
```

the form may be vulnerable.

---

## 3. Exploit the Vulnerability

### Method 1 — Direct URL

Forge the URL directly in the browser:

```http
http://site.com/index.php?page=recover&mail=justsomething@gmail.com
```

If the server processes the request without verification, the vulnerability is confirmed.

---

## CSRF Attack

```txt
Attacker forges request
=> server sends reset link to attacker
=> attacker resets password
=> account takeover ❌

For us, the Flag will be displayed

```

---

# References

- OWASP CSRF
- CWE-352: Cross-Site Request Forgery
- OWASP CSRF Prevention Cheat Sheet