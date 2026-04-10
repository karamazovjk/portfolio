# PSPWrite — Modernização e Recompilação para ARK-4 CFW

> Projeto pessoal de modificação de homebrew para PSP, com foco em melhorar a usabilidade do teclado virtual e garantir compatibilidade com compiladores modernos.

---

## Contexto

O [PSPWrite](https://github.com/PSP-Archive/PSPWrite) é um editor de texto homebrew para PSP criado por Ludovic Jacomme (Zx-81) em 2009. Embora funcional, o código apresenta incompatibilidades com compiladores C modernos e o layout do teclado virtual (Danzeff OSK) é pouco intuitivo para quem está acostumado com o estilo T9 de celulares antigos.

Este projeto tem dois objetivos:
1. **Corrigir os erros de compilação** para que o PSPWrite compile com o toolchain `pspdev` atual (gcc 15+)
2. **Reorganizar o layout do teclado** para um estilo T9/numérico mais ergonômico

---

## Ambiente de Desenvolvimento

- **Sistema Operacional:** Arch Linux com Hyprland
- **Toolchain:** [pspdev](https://github.com/pspdev/pspdev) (psp-gcc 15.2.0)
- **Hardware:** PSP-3000 com ARK-4 CFW (cIPL permanente)
- **Compilador host:** gcc 15.2.1

### Instalação do pspdev

```bash
# Clonar o repositório
git clone https://github.com/pspdev/pspdev.git ~/pspdev

# Definir variáveis de ambiente
export PSPDEV=~/pspdev
export PATH=$PATH:$PSPDEV/bin

# Compilar (demora ~1-2h dependendo do hardware)
cd ~/pspdev
./build-all.sh 2>&1 | tee ~/pspdev-log.txt

# Tornar permanente no zshrc
echo 'export PSPDEV=~/pspdev' >> ~/.zshrc
echo 'export PATH=$PATH:$PSPDEV/bin' >> ~/.zshrc
source ~/.zshrc

# Verificar instalação
psp-gcc --version
```

---

## Modificações Realizadas

### 1. Reorganização do Teclado (`psp_danzeff.c`)

O teclado Danzeff original usa um grid 3x3 onde cada célula contém letras agrupadas de forma não intuitiva. A modificação reorganiza as letras no estilo T9, onde cada célula corresponde a uma sequência alfabética contínua:

**Antes (layout original):**
```
[,abc] [.def] [!ghi]
[-jkl] [DEL mno] [|opq]
[(rst] [:uvw] [)xyz]
```

**Depois (layout T9):**
```
[_abc] [.def] [!ghi]
[-jkl] [DEL mno] [?pqr]
[(stu] [:vwx] [)yz,]
```

**Localização no código:** `src/psp_danzeff.c`, array `modeChar[MAX_VKEYBOARD][3][3][5]`

### 2. Correções de Compatibilidade (`psp_menu.c`)

O compilador moderno é mais rigoroso com declarações implícitas e assinaturas de função. Erros corrigidos:

#### `myCtrlPeekBufferPositive` → `sceCtrlPeekBufferPositive`
Função renomeada/removida no SDK moderno. Ocorrências nas linhas 211, 278 e 321.

```c
// Antes
myCtrlPeekBufferPositive(&c, 1);

// Depois
sceCtrlPeekBufferPositive(&c, 1);
```

#### Assinaturas de função incompletas
Funções chamadas com argumento mas declaradas sem parâmetro:

```c
// Antes (declaração)
psp_edit_menu_filename_clear()
psp_edit_menu_filename_del()

// Depois (declaração)
psp_edit_menu_filename_clear(int key)
psp_edit_menu_filename_del(int key)

// Chamadas sem argumento corrigidas para
psp_edit_menu_filename_clear(0);
psp_edit_menu_filename_del(0);
```

#### `psp_recent_menu` não declarado
Adicionado include e declaração extern no `psp_recent.h`:

```c
extern int psp_recent_menu(void);
```

E adicionado no `psp_menu.c`:
```c
#include "psp_recent.h"
```

### 3. Correções em andamento (`psp_menu_set.c`)

- `psp_global_default()` → `psp_global_init()`
- `myCtrlPeekBufferPositive` → `sceCtrlPeekBufferPositive` (linha 378)
- `psp_syntax_go_next()` e `psp_syntax_go_previous()` — investigando nomes corretos

---

## Como Compilar

```bash
# Clonar o repositório
git clone https://github.com/PSP-Archive/PSPWrite ~/pspwrite
cd ~/pspwrite/src

# Compilar
make -f Makefile-5x
```

O binário `EBOOT.PBP` será gerado na pasta `src/`. Para instalar no PSP:

```bash
# Montar cartão de memória
sudo mount -o rw,uid=1000,gid=1000,umask=000 /dev/sda1 /mnt/psp

# Copiar para o PSP
cp -r fw5x/ /mnt/psp/PSP/GAME/PSPWrite/
```

---

## Status do Projeto

| Arquivo | Status |
|---------|--------|
| `psp_danzeff.c` | ✅ Layout T9 implementado |
| `psp_menu.c` | ✅ Erros corrigidos, compila |
| `psp_menu_set.c` | 🔧 Em progresso |
| `psp_menu_set.h` | ⏳ Pendente |
| Compilação final | ⏳ Pendente |
| Teste no hardware | ⏳ Pendente |

---

## Contexto Técnico

Este projeto surgiu de uma jornada maior de ressuscitar um PSP-3000 que ficou parado por anos. O processo completo incluiu:

- Instalação do ARK-4 CFW com cIPL permanente
- Configuração de plugins (PRXshot, Console, RemoteJoyLite)
- Diagnóstico e recuperação de filesystem FAT32 corrompido com `fsck.fat`
- Configuração de Wi-Fi manual no PSP (WPA2, IP estático, DNS do Google)
- Instalação e compilação do toolchain pspdev do zero no Arch Linux

A modificação do PSPWrite é a cereja do bolo: transformar uma ferramenta funcional mas desconfortável em algo que realmente se encaixe no fluxo de uso do console.

---

## Referências

- [PSP-Archive/PSPWrite](https://github.com/PSP-Archive/PSPWrite) — código fonte original
- [pspdev/pspdev](https://github.com/pspdev/pspdev) — toolchain moderno
- [PSP-Archive/ARK-4](https://github.com/PSP-Archive/ARK-4) — custom firmware usado
- [pspunk.com](https://www.pspunk.com/ark-guide/) — guia de referência para ARK-4
- [Danzeff OSK](http://www.danzel.org/) — teclado virtual original

---
