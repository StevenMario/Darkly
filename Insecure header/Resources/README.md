# Insecure Headers

## Definition

An "insecure header" usually refers to a missing or misconfigured HTTP response header that fails to implement essential client-side security protections. HTTP headers are metadata sent by servers to browsers that control how the browser behaves. Missing or poorly configured security headers leave applications vulnerable to attacks such as XSS (Cross-Site Scripting), clickjacking, MIME-sniffing, and other client-side exploits.

## How it Works

1. **Server Response**: When a web server responds to a request, it includes HTTP headers that provide instructions to the browser.
2. **Missing Headers**: If security headers are not configured, the browser applies default (often permissive) behavior.
3. **Default Browser Behavior**: Without headers like Content-Security-Policy or X-Frame-Options, browsers allow potentially dangerous actions.
4. **Attacker Exploitation**: An attacker exploits this by using techniques like clickjacking, XSS injection, or MIME-sniffing.
5. **Successful Attack**: The browser executes the malicious code or action because no security headers prevented it.

## Normal Example

A secure web application includes proper security headers:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'; script-src 'self'
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

**Key Security Headers:**
- **X-Content-Type-Options: nosniff** - Prevents MIME-sniffing attacks
- **X-Frame-Options: DENY** - Prevents clickjacking
- **Content-Security-Policy** - Controls where scripts and resources can be loaded from
- **X-XSS-Protection** - Enables browser XSS filtering
- **Strict-Transport-Security** - Forces HTTPS connections

## Attack Example

An attacker exploits missing security headers:

```
1. Vulnerable server responds without security headers:
   HTTP/1.1 200 OK
   Content-Type: text/html
   (No X-Frame-Options header)
   (No Content-Security-Policy header)

2. Attacker creates a malicious webpage that frames the vulnerable site:
   <iframe src="https://vulnerable-app.com/admin"></iframe>

3. Attacker tricks a user into clicking on a button positioned over the iframe
   User clicks, but the click goes to the framed application

4. The vulnerable application processes the unintended action
   Admin function executes without explicit user consent (Clickjacking)

5. Alternatively, attacker injects malicious script:
   <script>
   fetch('https://vulnerable-app.com/transfer', {
     method: 'POST',
     body: 'amount=10000&to=attacker'
   })
   </script>

6. Without Content-Security-Policy, the browser executes the script
   Unauthorized action is performed
```

## Stage of Operation

### 1. Identify Missing Security Headers

- Navigate to the footer page:
    `http://10.11.200.224/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f`
- Inspect the page using browser DevTools (F12)
- You will see comments indicating required headers:
    ![Referer](./Screenshot%20from%202026-05-26%2013-29-36.png)
    ![User Agent](./Screenshot%20from%202026-05-26%2013-33-01.png)
- The comments reveal that the page expects specific `Referer` and `User-Agent` headers

### 2. Exploit the Vulnerability

- Use curl to modify the `Referer` header and the `User-Agent` header:
    ```bash
    curl -v "http://10.11.200.224/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f" -H "Referer: https://www.nsa.gov/" -H "User-Agent: ft_bornToSec"
    ```
- The server validates these headers and returns the flag in the response if the headers match expected values

## References

- [OWASP - Missing Security Headers](https://owasp.org/www-project-secure-headers/)
- [MDN - HTTP Headers Security](https://developer.mozilla.org/en-US/docs/Glossary/Response_header)
- [OWASP - Clickjacking Defense](https://owasp.org/www-community/attacks/Clickjacking)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
