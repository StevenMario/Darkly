# Open Redirect

## Definition

**Open redirection** vulnerabilities arise when an application incorporates user-controllable data into the target of a redirection in an unsafe way. An attacker can construct a URL within the application that causes a redirection to an arbitrary external domain. This behavior can be leveraged to facilitate phishing attacks against users of the application.

---

## How It Works

The application uses a URL parameter to determine where the user should be redirected. The server blindly trusts the value provided by the user and performs the redirection without verifying whether the destination belongs to the application.

### Normal Example

```http
http://site.com/index.php?page=redirect&site=facebook
```

The server redirects to `facebook.com`.

### Attack Example

```http
http://site.com/index.php?page=redirect&site=evil.com
```

An attacker replaces the legitimate URL with an arbitrary external domain. The server follows the redirection to the attacker's site.

---

## Stages of Operation

### 1. Identify the Vulnerable Parameter

Inspect the home page footer. You will find social media links that use a `site` parameter:

```html
<li><a href="index.php?page=redirect&site=facebook" class="icon fa-facebook"></a></li>
<li><a href="index.php?page=redirect&site=twitter" class="icon fa-twitter"></a></li>
<li><a href="index.php?page=redirect&site=instagram" class="icon fa-instagram"></a></li>
```

The `site` parameter controls the redirection destination.

### 2. Exploit the Vulnerability

Replace the `site` value with an arbitrary external domain:

```html
<li><a href="index.php?page=redirect&site=evil.com" class="icon fa-facebook"></a></li>
```

Alternatively, use `curl` directly:

```bash
curl -v "http://10.11.200.224/index.php?page=redirect&site=evil.com"
```

If the application redirects to `evil.com`, the vulnerability is confirmed.

---

## References

- [OWASP - Open Redirect](https://owasp.org/www-community/attacks/Open_Redirect)
- [CWE-601: URL Redirection to Untrusted Site](https://cwe.mitre.org/data/definitions/601.html)