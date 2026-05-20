# Cookies Tampering

## Definition

Cookies tampering refers to the unauthorized modification or manipulation of cookies by an attacker. Cookies are small files stored by web applications on a user's computer to store information used to identify returning users or track user activity. They often contain sensitive data such as session IDs, user preferences, authentication information, and user roles. An attacker can intercept, modify, or replace these cookies to gain unauthorized access, escalate privileges, or manipulate application behavior.

## How it Works

1. **Cookie Storage**: Web applications store cookies in the browser for various purposes (authentication, preferences, tracking).
2. **Interception**: An attacker uses tools like browser developer tools, proxy interceptors, or network sniffers to capture cookies.
3. **Modification**: The attacker modifies the cookie values (e.g., changing a user ID, role, or session token).
4. **Replacement**: The modified cookie is sent back to the server with subsequent requests.
5. **Exploitation**: The server accepts the tampered cookie, allowing the attacker to impersonate a user, escalate privileges, or bypass security controls.

## Normal Example

In a normal scenario, a web application uses cookies securely:

```
User logs in to www.example.com
→ Server creates a secure session cookie: 
  Set-Cookie: sessionid=a7f3d9e2c5b1; HttpOnly; Secure; SameSite=Strict
→ Browser stores the cookie
→ User makes subsequent requests with the cookie intact
→ Server validates the sessionid and grants appropriate access
→ User can only access resources based on their role
```

**Example Cookie Header:**
```
Cookie: sessionid=a7f3d9e2c5b1; role=user; preferences=dark_mode
```

The server trusts this cookie because it was set securely.

## Attack Example

An attacker tampers with cookies to gain unauthorized access:

```
1. Legitimate User logs in as "user"
   Set-Cookie: role=user; userid=123

2. Attacker inspects cookies using browser DevTools or proxy
   Sees: role=user; userid=123

3. Attacker modifies the cookie before sending request:
   Original: role=user; userid=123
   Modified: role=admin; userid=456

4. Attacker sends request with tampered cookie:
   GET /dashboard HTTP/1.1
   Cookie: role=admin; userid=456

5. Vulnerable server doesn't validate server-side session data
   Server sees role=admin and grants admin access

6. Attacker successfully escalates privileges and accesses admin panel
```

**Attack Variations:**
- **Privilege Escalation**: Changing `role=user` to `role=admin`
- **Session Hijacking**: Stealing and modifying valid session IDs
- **User Impersonation**: Changing `userid=123` to `userid=999`
- **Bypassing Authentication**: Setting `loggedIn=true` when it should be false

## Prevention

To prevent cookies tampering:
- Use **HttpOnly** flag to prevent JavaScript access
- Use **Secure** flag to transmit only over HTTPS
- Use **SameSite** flag to prevent CSRF attacks
- **Validate** all cookie data server-side, never trust client-side data
- Use **signed/encrypted** cookies with server-side secrets
- Implement **strong session management** with server-side storage
- Use **cryptographic signatures** to detect tampering