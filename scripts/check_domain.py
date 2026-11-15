#!/usr/bin/env python3
"""Read-only diagnostics for the official site's DNS, HTTP routing and TLS."""
import concurrent.futures
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

DOMAIN = "hijikilabo.com"
PAGES_IPS = [f"185.199.{part}.153" for part in (108, 109, 110, 111)]


def command(args, timeout=25, stdin=None):
    try:
        p = subprocess.run(args, input=stdin, text=True, capture_output=True, timeout=timeout)
        return {"exit_code": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "timeout_seconds": timeout}


def dns_probe(args):
    return {"kind": "dns", "command": args, **command(args, timeout=12)}


def http_probe(url, ip=None):
    with tempfile.TemporaryDirectory(prefix="hijikilabo-check-") as directory:
        body = Path(directory) / "body"
        headers = Path(directory) / "headers"
        args = ["curl", "--silent", "--show-error", "--compressed", "--location",
                "--max-redirs", "5", "--connect-timeout", "8", "--max-time", "20",
                "--dump-header", str(headers), "--output", str(body), "--write-out", "%{json}"]
        if ip:
            # Connect to a documented Pages IP while preserving hostname and TLS verification.
            args += ["--resolve", f"{urlsplit(url).hostname}:443:{ip}"]
        args += [url]
        response = command(args)
        raw = response.pop("stdout", "")
        try:
            stats = json.loads(raw)
        except ValueError:
            stats = {}
        response["transfer"] = {k: stats.get(k) for k in (
            "http_code", "url_effective", "remote_ip", "ssl_verify_result", "time_total", "errormsg")}
        text = body.read_text(errors="replace") if body.exists() else ""
        title = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        response["page_title"] = title.group(1).strip() if title else None
        response["expected_brand_present"] = "HIJIKI LABO" in text
        response["locations"] = [line.strip() for line in headers.read_text(errors="replace").splitlines()
                                 if line.lower().startswith(("http/", "location:"))] if headers.exists() else []
        return {"kind": "http", "url": url, "direct_pages_ip": ip, **response}


def certificate_probe(host):
    result = command(["openssl", "s_client", "-connect", f"{host}:443", "-servername", host,
                      "-verify_hostname", host, "-verify_return_error", "-showcerts"], stdin="")
    output = result.get("stdout", "")
    match = re.search(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", output, re.S)
    summary = command(["openssl", "x509", "-noout", "-subject", "-issuer", "-dates", "-ext",
                       "subjectAltName"], stdin=match.group(0)) if match else None
    return {"kind": "certificate", "host": host, "handshake_exit_code": result.get("exit_code"),
            "handshake_error": result.get("stderr", result.get("error")), "certificate": summary}


def main():
    for name in ("dig", "curl", "openssl"):
        if not shutil.which(name):
            raise SystemExit(f"Missing diagnostic tool: {name}")
    queries = []
    for name, record in [(DOMAIN, "A"), (DOMAIN, "AAAA"), (DOMAIN, "NS"),
                         (DOMAIN, "DS"), ("www." + DOMAIN, "CNAME")]:
        queries.append(["dig", "+time=3", "+tries=1", "+noall", "+answer", "+authority",
                        "+comments", name, record])
    for server in ("ns1.xdomain.ne.jp", "ns2.xdomain.ne.jp", "ns3.xdomain.ne.jp"):
        for name, record in [(DOMAIN, "A"), ("www." + DOMAIN, "CNAME")]:
            queries.append(["dig", "@" + server, "+time=3", "+tries=1", "+norecurse", "+noall",
                            "+answer", "+authority", "+comments", name, record])
    queries.append(["dig", "@a.gtld-servers.net", "+time=3", "+tries=1", "+norecurse",
                    "+noall", "+authority", "+comments", DOMAIN, "NS"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for result in executor.map(dns_probe, queries):
            print(json.dumps(result, ensure_ascii=False), flush=True)
    probes = [(f"https://{DOMAIN}/", None), (f"http://{DOMAIN}/", None),
              (f"https://www.{DOMAIN}/", None), (f"https://{DOMAIN}/privacy.html", None),
              (f"https://{DOMAIN}/missing/deep-page", None)]
    probes += [(f"https://{host}/", ip) for host in (DOMAIN, "www." + DOMAIN) for ip in PAGES_IPS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for result in executor.map(lambda pair: http_probe(*pair), probes):
            print(json.dumps(result, ensure_ascii=False), flush=True)
    for host in (DOMAIN, "www." + DOMAIN):
        print(json.dumps(certificate_probe(host), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
