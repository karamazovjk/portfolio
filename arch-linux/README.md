<h1 align="center">🐧Linux Setup — Arch + Hyprland + HyDE</h1>

<p align="center"><i>Documentação do processo completo de migração de Windows 11 para Arch Linux com Hyprland, realizado do zero em um Samsung NP530XBB (Intel Celeron N4000, 4GB RAM, 56GB).</i></p>

<p align="center">Maiores detalhes estão no repositório do meu <a href="https://github.com/karamazovjk/dotfiles">dotfiles</a>.</p>

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Contexto</h2>

Notebook antigo rodando Windows 11 com hardware limitado (4GB RAM, Celeron N4000), apresentando lentidão severa. A solução foi migrar completamente para Linux, explorando desde distros mais amigáveis até o Arch Linux puro com Hyprland como compositor Wayland.

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Desenvolvimento</h2>

<h3 align="center">Fase 1 — Customização do Terminal no Windows</h3>

Antes da migração, o terminal do Windows foi customizado como introdução ao mundo do ricing:

- Configuração da **execution policy** do PowerShell
- Instalação e configuração do **Oh My Posh** para prompt customizado
- Instalação da fonte **JetBrains Mono Nerd Font**
- Configuração do **Fastfetch** para exibição de informações do sistema com ASCII art
- Criação e edição do `$PROFILE` do PowerShell

**Principais comandos:**
```powershell
winget install JanDeDobbeleer.OhMyPosh
oh-my-posh font install JetBrainsMono
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h3 align="center">Fase 2 — Linux Mint (Teste)</h3>

Primeiro contato com Linux via Live USB para validar compatibilidade de hardware:

- Criação de Live USB com **Rufus** + ISO do Linux Mint 22.3 Cinnamon
- Configuração da BIOS Samsung (Secure Boot off, ordem de boot)
- Testes de compatibilidade: Wi-Fi ✅ | Áudio ✅ | Touchpad ✅ | Vídeo 4K ✅
- Instalação completa substituindo o Windows
- Configuração de **fractional scaling** (125%) para tela do notebook
- Otimizações de performance: `preload`, `swappiness`, desativação de serviços
- Configuração do **Fastfetch** + **Oh My Posh** no ambiente Linux
- Investigação de suporte ao leitor de digital Samsung `04e8:730a` (sem suporte no kernel)

**Hardware incompatível:**
- Leitor de impressão digital Samsung (`04e8:730a`) — sensor sem driver disponível no Linux

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h3 align="center">Fase 3 — Arch Linux + Hyprland</h3>

Migração para o setup definitivo após insatisfação com a performance do Mint Cinnamon:

<h4 align="center">Instalação do Arch</h4>

```bash
# Boot pelo archiso, conexão Wi-Fi
iwctl
station wlan0 connect "REDE"

# Instalação via archinstall
archinstall
```

**Desafios encontrados e solucionados:**
- Arch instalado no pendrive por engano → reinstalação no HD interno
- Usuário sem permissões sudo → adição manual ao grupo `wheel` via `init=/bin/bash`
- DNS não persistindo → configuração do `systemd-resolved`
- Teclado sem layout ABNT2 → configuração via `hyprland.conf`
- Wi-Fi não conectando após reboot → habilitação do `iwd` via systemctl

<h4 align="center">Configuração do Hyprland</h4>

```bash
# Instalação do yay (AUR helper)
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si

# HyDE (HyprDots) — configuração completa
git clone --depth 1 https://github.com/prasanthrangan/hyprdots ~/HyprDots
cd ~/HyprDots/Scripts && ./install.sh
```

**Configurações do `hyprland.conf`:**
```ini
# Layout de teclado ABNT2
input {
    kb_layout = br
    kb_variant = abnt2
}

# Screenshots
bind = , Print, exec, grim ~/Pictures/screenshot-$(date +%Y%m%d-%H%M%S).png
bind = SUPER SHIFT, S, exec, grim -g "$(slurp)" ~/Pictures/screenshot-$(date +%Y%m%d-%H%M%S).png

# Gerenciador de tarefas
bind = CTRL ALT, Delete, exec, kitty btop
```

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Stack Final</h2>

<div align="center">

| Categoria | Ferramenta |
|---|---|
| OS | Arch Linux |
| Compositor | Hyprland (Wayland) |
| Tema/Dots | HyDE (HyprDots — prasanthrangan) |
| Shell | Zsh |
| Terminal | Kitty |
| Bar | Waybar (via HyDE) |
| Launcher | Rofi |
| Editor | Neovim + NvChad |
| Fetch | Fastfetch |
| Screenshots | Grim + Slurp |
| Áudio | PipeWire + WirePlumber |
| Fonte | JetBrains Mono Nerd Font |

</div>

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Pacotes Essenciais</h2>

```bash
# Sistema base
sudo pacman -S base-devel linux-headers git wget curl nano neovim \
               pipewire pipewire-alsa pipewire-pulse wireplumber \
               bluez bluez-utils grim slurp btop firefox

# AUR
yay -S visual-studio-code-bin spotify notion-app
```

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Fixes e Workarounds</h2>

<h3 align="center">DNS persistente</h3>

```bash
sudo nano /etc/systemd/resolved.conf
# Adicionar: DNS=8.8.8.8 8.8.4.4

sudo systemctl enable --now systemd-resolved
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```

<h3 align="center">Wi-Fi automático no boot</h3>

```bash
sudo systemctl enable --now iwd
sudo systemctl enable --now NetworkManager
```

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Próximo projeto: leitor de digital</h2>

<p align="center"><i>Possibilidade de reversing (registrado em jul/2026)</i></p>

**Sensor:** Samsung 04e8:730a (CanvasBio, driver proprietário Windows-only). Sem suporte no libfprint nem em forks/hubs comunitários atuais.

**Viabilidade:** boa, há precedentes reais de gente sem background formal fazendo esse tipo de reversing sozinha (ex: projeto goodix-fingerprint-reversing, Validity90/91, casos documentados usando IA como par de reversing). O nível de dificuldade varia muito — pode ser desde 1 linha de código (adicionar um device ID que já usa protocolo conhecido) até meses (protocolo com handshake criptográfico tipo TLS-PSK).

**Antes de começar, checar:** o fabricante real do chip por trás do rebrand "CanvasBio" (FCC ID / datasheet). Se já houver reversing feito sob outro nome comercial, economiza trabalho.

**Roteiro:**

- Aprender o básico de USB (endpoints, descriptors)
- Dual boot/VM com passthrough USB + Wireshark/usbmon para capturar o tráfego do driver Windows genuíno
- Analisar o dump: procurar handshake criptográfico vs. tráfego plano
- Prototipar em Python antes de pensar em driver C
- Recorrer a comunidades (Discord Goodix, issues do libfprint) e a IA como apoio se travar

**Estimativa:** projeto de hobby de 6–12 meses, dado meu nível atual (C, Linux internals, scripting).

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Aprendizados</h2>

- Diferença entre ambiente de desktop (KDE, Cinnamon) e compositor Wayland (Hyprland)
- Gerenciamento de pacotes com `pacman` e `yay` (AUR)
- Configuração manual de sistema via arquivos `.conf`
- Debugging de serviços com `systemctl` e `journalctl`
- Conceito de dotfiles e ricing no Linux
- Navegação e edição no terminal sem interface gráfica

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Screenshots</h2>

<p align="center"><i>Em breve</i></p>

<div align="center"><img src="https://www.gitskins.com/api/readme-reference/divider?username=karamazovjk&theme=neon&v=readme-reference-2" width="100%" alt="Section divider" /></div>

<h2 align="center">Referências</h2>

- [Arch Wiki — Installation Guide](https://wiki.archlinux.org/title/Installation_guide)
- [Hyprland Wiki](https://wiki.hyprland.org)
- [HyDE (HyprDots) — prasanthrangan](https://github.com/prasanthrangan/hyprdots)
- [python-validity — uunicorn](https://github.com/uunicorn/python-validity)
- [SleepyCatHey — Ultimate Win11 Setup](https://github.com/SleepyCatHey/Ultimate-Win11-Setup)
