# 🐧 Linux Setup — Arch + Hyprland + Hyde

> Documentação do processo completo de migração de Windows 11 para Arch Linux com Hyprland, realizado do zero em um Samsung NP530XBB (Intel Celeron N4000, 4GB RAM, 56GB).

---

## Contexto

Notebook antigo rodando Windows 11 com hardware limitado (4GB RAM, Celeron N4000), apresentando lentidão severa. A solução foi migrar completamente para Linux, explorando desde distros mais amigáveis até o Arch Linux puro com Hyprland como compositor Wayland.

---

## Desenvolvimento

### Fase 1 — Customização do Terminal no Windows
Antes da migração, o terminal do Windows foi customizado como introdução ao mundo do ricing:

- Configuração da **execution policy** do PowerShell
- Instalação e configuração do **Oh My Posh** para prompt customizado
- Instalação da fonte **JetBrains Mono Nerd Font**
- Configuração do **Fastfetch** para exibição de informações do sistema com ASCII art
- Criação e edição do `$PROFILE` do PowerShell

**Principais comandos:**
```powershell
winget install JanDeLaats.OhMyPosh
oh-my-posh font install JetBrainsMono
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Fase 2 — Linux Mint (Teste)
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

---

### Fase 3 — Arch Linux + Hyprland
Migração para setup definitivo após insatisfação com performance do Mint Cinnamon:

#### Instalação do Arch
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

#### Configuração do Hyprland
```bash
# Instalação do yay (AUR helper)
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si

# HyprDots (configuração completa)
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

---

## 🛠️ Stack Final

| Categoria | Ferramenta |
|---|---|
| OS | Arch Linux |
| Compositor | Hyprland (Wayland) |
| Tema/Dots | HyprDots (prasanthrangan) |
| Shell | Zsh |
| Terminal | Kitty |
| Bar | Waybar (via HyprDots) |
| Launcher | Rofi |
| Editor | Neovim + NvChad |
| Fetch | Fastfetch |
| Screenshots | Grim + Slurp |
| Áudio | PipeWire + WirePlumber |
| Fonte | JetBrains Mono Nerd Font |

---

## 📦 Pacotes Essenciais

```bash
# Sistema base
sudo pacman -S base-devel linux-headers git wget curl nano neovim \
               pipewire pipewire-alsa pipewire-pulse wireplumber \
               bluez bluez-utils grim slurp btop firefox

# AUR
yay -S visual-studio-code-bin spotify notion-app
```

---

## 🔧 Fixes e Workarounds

### DNS persistente
```bash
sudo nano /etc/systemd/resolved.conf
# Adicionar: DNS=8.8.8.8 8.8.4.4

sudo systemctl enable --now systemd-resolved
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```

### Wi-Fi automático no boot
```bash
sudo systemctl enable --now iwd
sudo systemctl enable --now NetworkManager
```

### Leitor de digital (sem suporte)
O sensor `Samsung 04e8:730a` não possui driver disponível no Linux. Tentativas realizadas:
- `fprintd` + `libpam-fprintd`
- `python-validity` via PPA `uunicorn/open-fprintd`
- O sensor é detectado via USB mas o protocolo proprietário não é suportado

---

## 💡 Aprendizados

- Diferença entre ambiente de desktop (KDE, Cinnamon) e compositor Wayland (Hyprland)
- Gerenciamento de pacotes com `pacman` e `yay` (AUR)
- Configuração manual de sistema via arquivos `.conf`
- Debugging de serviços com `systemctl` e `journalctl`
- Conceito de dotfiles e ricing no Linux
- Navegação e edição no terminal sem interface gráfica

---

## 📸 Screenshots

> *Em breve*

---

## 🔗 Referências

- [Arch Wiki — Installation Guide](https://wiki.archlinux.org/title/Installation_guide)
- [Hyprland Wiki](https://wiki.hyprland.org)
- [HyprDots — prasanthrangan](https://github.com/prasanthrangan/hyprdots)
- [python-validity — uunicorn](https://github.com/uunicorn/python-validity)
- [SleepyCatHey — Ultimate Win11 Setup](https://github.com/SleepyCatHey/Ultimate-Win11-Setup)
