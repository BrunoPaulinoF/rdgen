#!/usr/bin/env python3
"""Gera a configuracao do programa "Suporte KyberFood" para o workflow do rdgen.

O workflow `generator-windows.yml` baixa as configuracoes de `<url>/get_zip?...` e os
desenhos de `<url>/get_png?...`. Aqui eles moram no PROPRIO repositorio (pasta
`kyberfood/`), servidos pelo raw.githubusercontent.com, que ignora o `?...` do fim.
Assim nao precisa do servidor do rdgen.

Nada aqui e segredo: o servidor e a chave PUBLICA (id_ed25519.pub) ja vao dentro do
programa. Por isso o zip vai SEM senha (o passo "Load Secrets" abre zip sem senha
quando o segredo ZIP_PASSWORD nao existe).

Uso (da raiz do repositorio):
    python3 kyberfood/gerar-config.py <branch>
e depois rode o workflow "Custom Windows Client Generator" nessa mesma branch com:
    version = 1.5.3
    zip_url = (o texto que este script imprime)
"""

import base64
import json
import sys
import zipfile
from pathlib import Path

REPO = "BrunoPaulinoF/rdgen"
RUSTDESK_VERSION = "1.5.3"
RELEASE_NUMBER = "2"  # suba quando gerar de novo com a MESMA versao do RustDesk

SERVER = "148.230.73.219"
SERVER_PORT = "21116"
KEY = "kmssTvstGSYcIl2sreiH0qaP6uEKmelwOCj2p8xnZ4A="
API_SERVER = f"{SERVER}:21114"

APP_NAME_DISPLAY = "Suporte KyberFood"
APP_NAME = APP_NAME_DISPLAY.replace(" ", "")  # nome interno/arquivo, sem espaco
FILE_NAME = "SuporteKyberFood"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("uso: python3 kyberfood/gerar-config.py <branch>")
    branch = sys.argv[1]
    base = f"https://raw.githubusercontent.com/{REPO}/refs/heads/{branch}/kyberfood"

    override = {
        "hide-powered-by-me": "Y",
        "theme": "light",  # a logo tem texto escuro: tema claro sempre
        "enable-lan-discovery": "N",
        "allow-auto-disconnect": "N",
        "access-mode": "custom",
        "enable-keyboard": "Y",
        "enable-clipboard": "Y",
        "enable-file-transfer": "Y",
        "enable-audio": "Y",
        "enable-tunnel": "Y",
        "enable-remote-restart": "Y",
        "enable-record-session": "Y",
        "enable-block-input": "Y",
        "allow-remote-config-modification": "N",
        "direct-server": "N",
        # Sem senha FIXA (nenhum "password" no topo): so a senha de USO UNICO, aleatoria, que o
        # RustDesk troca sozinho assim que alguem entra com ela (e apos 10 erros seguidos).
        "verification-method": "use-both-passwords",
        # Entra com a senha de uso unico (o cliente manda a foto e pode sair de perto) OU com o
        # clique em "Aceitar" quando a equipe conecta sem a senha.
        "approve-mode": "password-click",
        "allow-hide-cm": "N",
        "allow-remove-wallpaper": "Y",
        "enable-remote-printer": "Y",
        "enable-camera": "N",
        "enable-terminal": "Y",
        "custom-rendezvous-server": SERVER,
        "api-server": API_SERVER,
    }
    custom = {
        "conn-type": "incoming",  # o cliente so RECEBE acesso, nao controla ninguem
        "disable-settings": "Y",  # o cliente nao consegue trocar o servidor sem querer
        "app-name": APP_NAME_DISPLAY,
        "override-settings": override,
        "default-settings": {},
    }

    secrets = {
        "server": SERVER,
        "serverPort": SERVER_PORT,
        "key": KEY,
        "apiServer": API_SERVER,
        "custom": base64.b64encode(json.dumps(custom).encode("ascii")).decode("ascii"),
        "uuid": "kyberfood-suporte",
        "iconlink_url": f"{base}/icon",
        "iconlink_uuid": "kyberfood",
        "iconlink_file": "icon.png",
        "logolink_url": f"{base}/logo",
        "logolink_uuid": "kyberfood",
        "logolink_file": "logo.png",
        "privacylink_url": "false",
        "privacylink_uuid": "false",
        "privacylink_file": "false",
        "appname": APP_NAME,
        "genurl": "",
        "themeColor": "#FF6B35",
        "themeSurfaceLight": "",
        "themeSurfaceDark": "",
        "themeMeColor": "",
        "urlLink": "https://kyberfood.com.br",
        "downloadLink": "https://kyberfood.com.br/suporte",
        "delayFix": "false",
        # Nem 'true' nem 'false': o workflow NAO tenta mandar o programa para um servidor
        # do rdgen; o passo "Publicar no GitHub Releases (KyberFood)" publica no repositorio.
        "rdgen": "kyberfood",
        "xOffline": "false",
        "removeNewVersionNotif": "true",
        "update_public_key": "",
        "compname": "KyberFood",
        "androidappid": "com.carriez.flutter_hbb",
        "filename": FILE_NAME,
        "release_tag": f"suporte-kyberfood-{RUSTDESK_VERSION}-{RELEASE_NUMBER}",
    }

    out_dir = Path(__file__).resolve().parent / "config"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "secrets.json").write_text(json.dumps(secrets, indent=2) + "\n", encoding="utf-8")
    with zipfile.ZipFile(out_dir / "get_zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("secrets.json", json.dumps(secrets))

    print(json.dumps({"url": f"{base}/config", "file": "config.zip"}))


if __name__ == "__main__":
    main()
