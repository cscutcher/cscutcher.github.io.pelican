Title: Start google chrome with a socks proxy on linux
Tags: code

```bash
google-chrome --proxy-server="socks5://localhost:6666" --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost"
```
