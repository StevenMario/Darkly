# Stored XSS (Cross-Site Scripting)

## Definition

Stored XSS is a vulnerability where malicious JavaScript code is permanently saved in the database and executed every time a user visits the affected page.

Unlike Reflected XSS which executes once, Stored XSS affects all visitors.

---

## Difference Between Reflected and Stored XSS

| Type | Behavior |
|---|---|
| **Reflected XSS** | Payload in URL or form => executes **ONCE** for the attacker |
| **Stored XSS** | Payload saved in database => executes for **EVERY** visitor |

---

## How It Works

A vulnerable application saves user input (comment, name, message) directly into the database without sanitizing it.

When the page loads, the stored content is rendered as raw HTML — executing any injected JavaScript.

---

# Exploit the Vulnerability

## Vulnerable Page

```text
http://site.com/index.php?page=feedback
```

## Steps

1. Go to the feedback page in the browser.

2. In the **Name** field, type exactly:

```html
<script>al
```

> The field has a `maxlength="10"` limit — this prevents typing the complete `alert` keyword, which is intentional: the server detects the beginning of `<script>alert` as an XSS attempt and triggers the flag.

3. In the **Message** field, type anything:

```text
just a message or something isn't important
```

4. Click **Sign Guestbook**.

5. The flag will be displayed.

---

## Why It Works

- The **Name** field reflects input directly into the page without escaping.
- The server detects `<script>al` as the beginning of `<script>alert`.
- A complete alert payload is blocked — an incomplete one triggers the flag.
- In a real attack without the limit, the full payload would execute:

```html
<script>alert(document.cookie)</script>
```

=> steals session cookies of every visitor.

---

## Why It Is Stored XSS and Not Reflected

- The payload is saved in the database when the form is submitted.
- Every time the feedback page loads, the stored payload is rendered.
- It affects **ALL** visitors — not just the attacker.

---

# References

- OWASP XSS
- CWE-79: Improper Neutralization of Input During Web Page Generation
- OWASP XSS Prevention Cheat Sheet