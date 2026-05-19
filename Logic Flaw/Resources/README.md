# Survey / Logic Flaw

## Definition

A **Logic Flaw** is a vulnerability where an application enforces input validation only on the client side (browser), but not on the server side.  
An attacker can bypass these restrictions by directly modifying the HTML values before submitting the form.

---

## How It Works

The application expects a grade between **1 and 10** via a dropdown menu.  
This restriction exists only in the HTML — the server accepts any value without verification.

---

# Exploit the Vulnerability

## Vulnerable Page

```text
http://site.com/index.php?page=survey

```
=> Open F12 -> inspector
=> Find the dropdown menu: 
```html
<select name="sujet">
  <option value="1">1</option>
  <option value="2">2</option>
  ...
  <option value="10">10</option>
</select>
```
=> Double-click on a value attribute, for example change value="9" to value="999999"
=>Select that option to the dropdown menu
=> The Flag will be displayed