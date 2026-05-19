# Hidden Content 1 — robots.txt & HTPasswd

## Definition

Hidden Content vulnerabilities occur when sensitive files or directories are left accessible on a web server. The `robots.txt` file, intended to guide search engine crawlers, can inadvertently reveal the location of hidden or sensitive directories.

## What is robots.txt?

`robots.txt` is a file placed at the root of a website that tells search engine bots (like Googlebot) which pages or directories they should not index.

```txt
User-agent: *
Disallow: /admin
Disallow: /private
```

The issue is that this file is publicly accessible by anyone. Instead of protecting sensitive content, it can unintentionally expose hidden paths to attackers.

---

# Exploit the Vulnerability

The first step is to access the `robots.txt` file directly from the browser:

```bash
http:///robots.txt
```

The file reveals hidden directories:

```txt
Disallow: /whatever
Disallow: /.hidden
```

Browsing to `/whatever/` shows that directory listing is enabled:

```bash
http://site.com/whatever/
```

Inside the directory, a file named `htpasswd` is accessible publicly.

Downloading the file reveals a username and an MD5 hashed password:

```bash
curl http://site.com/whatever/htpasswd
```

```txt
root:437394baff5aa33daa618be47b75cb49
```

The MD5 hash can then be cracked using an online hash database such as `crackstation.net`.

Once the plaintext password is recovered, the credentials can be used on the admin page:

```bash
http://site.com/index.php?page=admin
```

```txt
Username: root
Password: <cracked_password>
```

After authentication, the flag is displayed.

---

# Why It Is Vulnerable

- `robots.txt` exposes sensitive directory paths
- Directory listing is enabled
- The `htpasswd` file is publicly accessible
- MD5 is an outdated and insecure hashing algorithm
- MD5 hashes can be cracked quickly using rainbow tables or public databases

---

# References

- OWASP — Sensitive Data Exposure
- CWE-538 — Insertion of Sensitive Information into Externally-Accessible File
- robots.txt Specification