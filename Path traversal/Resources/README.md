# Path Traversal

## Definition

Path Traversal (also called Directory Traversal) is a web vulnerability that allows an attacker to read files outside the directory intended by the application by manipulating file paths using `../` sequences.

---

## How It Works

A vulnerable application uses user input to construct a file path without properly validating it.

### Normal Example

```http
http://site.com/?file=document.pdf
```

The server reads:

```bash
/var/www/files/document.pdf
```

### Attack Example

An attacker replaces the file name with `../` sequences to move up the directory tree:

```http
http://site.com/?file=../../../etc/passwd
```

The server then reads:

```bash
/etc/passwd
```

This is a sensitive file on Linux systems.

---

## Stages of Operation

### 1. Identify Vulnerable Parameters

Look for parameters that load files, such as:

- `?file=`
- `?page=`
- `?path=`
- `?include=`

---

### 2. Target `/etc/passwd`

Why target this file?

- It exists on almost all Linux systems
- It is readable without special privileges
- Its content is easily recognizable
- It reveals usernames useful for further attacks

---

### 3. Test the Vulnerability

```http
http://site.com/?page=../../../../../../../../etc/passwd
```

If the content of the file is displayed, the vulnerability is confirmed.

For us, the Flag will be displayed instead of the content.

---

## References

- OWASP Path Traversal
- CWE-22: Path Traversal