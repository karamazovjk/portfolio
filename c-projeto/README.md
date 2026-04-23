# sysmon

Monitor de sistema em tempo real escrito em **C puro**, sem dependências externas.

Lê diretamente do kernel via `/proc`:
- `/proc/stat` → uso de CPU (%)
- `/proc/meminfo` → RAM usada / total
- `/proc/uptime` → tempo ligado

## Como usar

```bash
make
./sysmon
```

## Como funciona

| Fonte           | O que extrai                        |
|-----------------|-------------------------------------|
| `/proc/stat`    | ticks de CPU (user/idle/system...)  |
| `/proc/meminfo` | MemTotal e MemAvailable em kB       |
| `/proc/uptime`  | segundos desde o boot               |

O uso de CPU é calculado como a diferença entre dois snapshots com 1 segundo de intervalo — mesmo método do `top`.

## Demo

```
╔══════════════════════════════════════════╗
║         sysmon — monitor em tempo real   ║
╚══════════════════════════════════════════╝

  ⏱  Uptime   01h 23m 45s

  CPU  [████████░░░░░░░░░░░░░░░░░░░░░░]  26.3%
  MEM  [████████████████░░░░░░░░░░░░░░]  54.1%  (2181 / 4026 MB)

  atualiza a cada 1s — Ctrl+C para sair
```

Feito sem `top`, `htop`, `sysinfo` ou qualquer lib de terceiros.
