# Suporte KyberFood

Programa de suporte remoto da KyberFood (RustDesk com o nosso nome, logo e servidor).
O site `kyberfood.com.br/suporte` baixa o `SuporteKyberFood.exe` das *Releases* deste repositório.

- Sem senha fixa. A equipe entra com a **senha de uso único** que aparece na tela do cliente
  (ela muda sozinha depois de cada acesso) **ou** o cliente clica em "Aceitar".
- O cliente só **recebe** acesso e não consegue mudar as configurações.

## Gerar uma versão nova

1. Ajuste `kyberfood/gerar-config.py` (versão do RustDesk, `RELEASE_NUMBER`, etc.).
2. Rode `python3 kyberfood/gerar-config.py <branch>` e faça commit na branch.
3. Em **Actions → Custom Windows Client Generator → Run workflow**, escolha a branch e preencha
   `version` (ex.: `1.5.3`) e `zip_url` (o texto que o script imprimiu).
4. Leva de 45 a 60 minutos. O programa aparece em **Releases**.
5. No site, troque a versão em `src/lib/remote-support.ts` do repositório `kyberfood`.

Ícone e logo: `kyberfood/marca/` (fontes em SVG) e `kyberfood/icon/get_png`, `kyberfood/logo/get_png` (os PNG usados).
