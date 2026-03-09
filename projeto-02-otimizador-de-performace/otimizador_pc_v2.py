"""
Otimizador do PC  v2.0
Requer: pip install psutil
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import os, sys, shutil, glob, tempfile, platform, ctypes, time, json
from collections import deque
from datetime import datetime, timedelta
import psutil

# ══════════════════════════════════════════════════════
#  TEMA  (verde-terminal)
# ══════════════════════════════════════════════════════
BG       = "#0d0d0d"
PANEL    = "#111111"
PANEL2   = "#161616"
BORDER   = "#1e1e1e"
ACCENT   = "#00ff88"
ACCENT2  = "#00ccff"
WARN     = "#ffaa00"
DANGER   = "#ff4455"
TEXT     = "#d8d8d8"
MUTED    = "#444444"
GRID     = "#1a1a1a"

F_MONO  = ("Consolas", 9)
F_UI    = ("Segoe UI", 10)
F_SMALL = ("Segoe UI", 8)
F_TITLE = ("Segoe UI", 12, "bold")
F_BIG   = ("Segoe UI", 20, "bold")

IS_WIN   = platform.system() == "Windows"
IS_ADMIN = ctypes.windll.shell32.IsUserAnAdmin() if IS_WIN else False

SCHEDULE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "otimizador_schedule.json")

# ══════════════════════════════════════════════════════
#  FUNÇÕES DE LIMPEZA
# ══════════════════════════════════════════════════════

def log(w, msg, color=TEXT):
    w.configure(state="normal")
    tag = color
    w.insert(tk.END, msg + "\n", tag)
    w.see(tk.END)
    w.configure(state="disabled")

def limpar_temp(lw):
    total = 0
    pastas = [tempfile.gettempdir()]
    if IS_WIN:
        pastas += [
            os.path.join(os.environ.get("WINDIR","C:\\Windows"), "Temp"),
            os.path.join(os.environ.get("LOCALAPPDATA",""), "Temp"),
        ]
    for p in filter(os.path.exists, pastas):
        for item in glob.glob(os.path.join(p, "*")):
            try:
                if os.path.isfile(item): os.remove(item)
                else: shutil.rmtree(item, ignore_errors=True)
                total += 1
            except: pass
    log(lw, f"  ✓ Temporários removidos: {total}", ACCENT)

def limpar_cache_nav(lw):
    app = os.environ.get("LOCALAPPDATA","")
    roam = os.environ.get("APPDATA","")
    caches = [
        os.path.join(app, r"Google\Chrome\User Data\Default\Cache"),
        os.path.join(app, r"Google\Chrome\User Data\Default\Code Cache"),
        os.path.join(app, r"BraveSoftware\Brave-Browser\User Data\Default\Cache"),
        os.path.join(app, r"Microsoft\Edge\User Data\Default\Cache"),
        os.path.join(roam, r"Mozilla\Firefox\Profiles"),
    ] if IS_WIN else [
        os.path.expanduser("~/.cache/google-chrome"),
        os.path.expanduser("~/.cache/mozilla"),
    ]
    total = sum(1 for c in caches if os.path.exists(c) and not shutil.rmtree(c, ignore_errors=True))
    log(lw, f"  ✓ Caches de navegadores limpos: {total} pastas", ACCENT)

def limpar_prefetch(lw):
    if not IS_WIN: return log(lw, "  ⚠ Prefetch só no Windows.", WARN)
    if not IS_ADMIN: return log(lw, "  ⚠ Requer admin.", WARN)
    p = r"C:\Windows\Prefetch"
    total = 0
    if os.path.exists(p):
        for f in glob.glob(os.path.join(p,"*.pf")):
            try: os.remove(f); total += 1
            except: pass
    log(lw, f"  ✓ Prefetch: {total} arquivos", ACCENT)

def limpar_dns(lw):
    if not IS_WIN: return log(lw, "  ⚠ Só no Windows.", WARN)
    r = subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
    log(lw, "  ✓ Cache DNS limpo." if r.returncode==0 else "  ✗ Falha no DNS.", ACCENT if r.returncode==0 else DANGER)

def limpar_minidumps(lw):
    if not IS_WIN: return log(lw, "  ⚠ Só no Windows.", WARN)
    if not IS_ADMIN: return log(lw, "  ⚠ Requer admin.", WARN)
    p = r"C:\Windows\Minidump"; total = 0
    if os.path.exists(p):
        for f in glob.glob(os.path.join(p,"*.dmp")):
            try: os.remove(f); total += 1
            except: pass
    log(lw, f"  ✓ Minidumps removidos: {total}", ACCENT)

def fechar_apps(lw):
    if not IS_WIN: return log(lw, "  ⚠ Só no Windows.", WARN)
    alvos = ["OneDrive.exe","Teams.exe","Skype.exe","spotify.exe",
             "Discord.exe","slack.exe","steam.exe","epicgameslauncher.exe"]
    enc = []
    for a in alvos:
        r = subprocess.run(f"taskkill /F /IM {a}", shell=True, capture_output=True)
        if r.returncode == 0: enc.append(a.replace(".exe",""))
    log(lw, f"  ✓ Encerrados: {', '.join(enc)}" if enc else "  ℹ Nenhum app-alvo rodando.", ACCENT if enc else MUTED)

def energia_desempenho(lw):
    if not IS_WIN: return log(lw, "  ⚠ Só no Windows.", WARN)
    r = subprocess.run("powercfg /s 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c", shell=True, capture_output=True)
    log(lw, "  ✓ Plano de energia → Alto Desempenho." if r.returncode==0 else "  ✗ Falha (tente como admin).", ACCENT if r.returncode==0 else DANGER)

def limpar_lixeira(lw):
    if IS_WIN:
        subprocess.run('powershell -command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"', shell=True, capture_output=True)
    else:
        subprocess.run("rm -rf ~/.local/share/Trash/files/*", shell=True)
    log(lw, "  ✓ Lixeira esvaziada.", ACCENT)

def info_disco(lw):
    t,u,f = shutil.disk_usage("/")
    gb = 1024**3
    log(lw, f"  💾 Disco | Total: {t/gb:.1f} GB | Usado: {u/gb:.1f} GB | Livre: {f/gb:.1f} GB", ACCENT2)
    if f/t < 0.10: log(lw, "  ⚠ Menos de 10% livre!", DANGER)

TAREFAS = [
    ("🗑  Arquivos temporários",         limpar_temp),
    ("🌐 Cache de navegadores",          limpar_cache_nav),
    ("🧹 Prefetch (Windows)",            limpar_prefetch),
    ("📡 Cache DNS",                      limpar_dns),
    ("💀 Minidumps",                      limpar_minidumps),
    ("🚫 Fechar apps em segundo plano",  fechar_apps),
    ("⚡ Plano de energia → Desempenho", energia_desempenho),
    ("🗂  Esvaziar lixeira",              limpar_lixeira),
    ("💾 Verificar espaço em disco",     info_disco),
]

# ══════════════════════════════════════════════════════
#  CANVAS SPARKLINE  (gráfico de linha leve)
# ══════════════════════════════════════════════════════
class Sparkline(tk.Canvas):
    MAX = 60  # pontos históricos

    def __init__(self, parent, color=ACCENT, **kw):
        super().__init__(parent, bg=PANEL2, bd=0, highlightthickness=0, **kw)
        self.color = color
        self.data  = deque([0]*self.MAX, maxlen=self.MAX)

    def push(self, value):
        self.data.append(value)
        self._draw()

    def _draw(self):
        self.delete("all")
        W = self.winfo_width()
        H = self.winfo_height()
        if W < 2 or H < 2: return

        # grid lines
        for pct in (25, 50, 75):
            y = H - int(H * pct / 100)
            self.create_line(0, y, W, y, fill=GRID, dash=(2,4))

        # line
        pts = list(self.data)
        n   = len(pts)
        xs  = [int(i * W / (n-1)) for i in range(n)]
        ys  = [H - max(1, int(H * v / 100)) for v in pts]
        coords = []
        for x, y in zip(xs, ys):
            coords += [x, y]
        if len(coords) >= 4:
            self.create_line(*coords, fill=self.color, width=1, smooth=True)
        # fill
        poly = [0, H] + coords + [W, H]
        self.create_polygon(*poly, fill=self.color, stipple="gray25", outline="")
        # last value label
        self.create_text(W-4, 4, text=f"{pts[-1]:.0f}%",
                         anchor="ne", fill=self.color, font=F_SMALL)


# ══════════════════════════════════════════════════════
#  BARRA + LABEL  (widget reutilizável)
# ══════════════════════════════════════════════════════
class MetricBar(tk.Frame):
    def __init__(self, parent, label, color=ACCENT, **kw):
        super().__init__(parent, bg=PANEL2, **kw)
        self.color = color

        top = tk.Frame(self, bg=PANEL2)
        top.pack(fill="x", pady=(0,2))
        tk.Label(top, text=label, font=F_SMALL, bg=PANEL2, fg=MUTED).pack(side="left")
        self.lbl_val = tk.Label(top, text="–", font=("Consolas",9,"bold"), bg=PANEL2, fg=color)
        self.lbl_val.pack(side="right")

        self.canvas = tk.Canvas(self, height=6, bg=BORDER, bd=0, highlightthickness=0)
        self.canvas.pack(fill="x")

    def set(self, pct, label_text):
        self.lbl_val.configure(text=label_text)
        self.canvas.update_idletasks()
        W = self.canvas.winfo_width()
        if W < 2: W = 200
        self.canvas.delete("all")
        fill_color = DANGER if pct > 85 else WARN if pct > 65 else self.color
        self.canvas.create_rectangle(0, 0, int(W * pct / 100), 6, fill=fill_color, outline="")


# ══════════════════════════════════════════════════════
#  PAINEL MONITOR
# ══════════════════════════════════════════════════════
class MonitorPanel(tk.Frame):
    INTERVAL_MS = 1000

    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)
        self._running = False
        self._build()

    def _build(self):
        # título
        hdr = tk.Frame(self, bg=PANEL)
        hdr.pack(fill="x", padx=14, pady=(12,6))
        tk.Label(hdr, text="MONITOR EM TEMPO REAL", font=("Segoe UI",8,"bold"),
                 bg=PANEL, fg=MUTED).pack(side="left")
        self.lbl_time = tk.Label(hdr, text="", font=F_SMALL, bg=PANEL, fg=MUTED)
        self.lbl_time.pack(side="right")

        # ── CPU ──
        sec_cpu = tk.Frame(self, bg=PANEL2, padx=10, pady=8)
        sec_cpu.pack(fill="x", padx=14, pady=4)
        tk.Label(sec_cpu, text="CPU", font=F_TITLE, bg=PANEL2, fg=ACCENT).pack(anchor="w")
        self.bar_cpu = MetricBar(sec_cpu, "Uso total", ACCENT)
        self.bar_cpu.pack(fill="x", pady=(4,6))
        self.spark_cpu = Sparkline(sec_cpu, color=ACCENT, height=48)
        self.spark_cpu.pack(fill="x")

        # núcleos (até 8)
        self.core_bars = []
        cores_frame = tk.Frame(sec_cpu, bg=PANEL2)
        cores_frame.pack(fill="x", pady=(6,0))
        n_cores = min(psutil.cpu_count(logical=True) or 4, 8)
        cols = 2
        for i in range(n_cores):
            b = MetricBar(cores_frame, f"Core {i}", ACCENT2)
            b.grid(row=i//cols, column=i%cols, sticky="ew", padx=(0,8), pady=1)
            self.core_bars.append(b)
        for c in range(cols): cores_frame.columnconfigure(c, weight=1)

        # ── RAM ──
        sec_ram = tk.Frame(self, bg=PANEL2, padx=10, pady=8)
        sec_ram.pack(fill="x", padx=14, pady=4)
        tk.Label(sec_ram, text="MEMÓRIA RAM", font=F_TITLE, bg=PANEL2, fg=ACCENT).pack(anchor="w")
        self.bar_ram = MetricBar(sec_ram, "Em uso", ACCENT)
        self.bar_ram.pack(fill="x", pady=(4,6))
        self.spark_ram = Sparkline(sec_ram, color=ACCENT, height=48)
        self.spark_ram.pack(fill="x")
        self.lbl_ram_detail = tk.Label(sec_ram, text="", font=F_SMALL, bg=PANEL2, fg=MUTED)
        self.lbl_ram_detail.pack(anchor="w", pady=(4,0))

        # ── DISCO ──
        sec_disk = tk.Frame(self, bg=PANEL2, padx=10, pady=8)
        sec_disk.pack(fill="x", padx=14, pady=4)
        tk.Label(sec_disk, text="DISCO", font=F_TITLE, bg=PANEL2, fg=ACCENT).pack(anchor="w")
        self.bar_disk = MetricBar(sec_disk, "Espaço usado", ACCENT)
        self.bar_disk.pack(fill="x", pady=(4,0))
        self.lbl_disk_detail = tk.Label(sec_disk, text="", font=F_SMALL, bg=PANEL2, fg=MUTED)
        self.lbl_disk_detail.pack(anchor="w", pady=(4,0))
        self.bar_disk_io = MetricBar(sec_disk, "I/O leitura+escrita", ACCENT2)
        self.bar_disk_io.pack(fill="x", pady=(6,0))

        tk.Frame(self, bg=PANEL, height=10).pack()

    def start(self):
        self._running = True
        self._prev_io = psutil.disk_io_counters()
        self._tick()

    def stop(self):
        self._running = False

    def _tick(self):
        if not self._running: return
        try:
            # CPU
            cpu_total = psutil.cpu_percent(interval=None)
            cpu_cores = psutil.cpu_percent(interval=None, percpu=True)
            self.bar_cpu.set(cpu_total, f"{cpu_total:.1f}%")
            self.spark_cpu.push(cpu_total)
            for i, b in enumerate(self.core_bars):
                v = cpu_cores[i] if i < len(cpu_cores) else 0
                b.set(v, f"{v:.0f}%")

            # RAM
            mem = psutil.virtual_memory()
            used_gb  = mem.used  / 1024**3
            total_gb = mem.total / 1024**3
            self.bar_ram.set(mem.percent, f"{mem.percent:.1f}%")
            self.spark_ram.push(mem.percent)
            self.lbl_ram_detail.configure(
                text=f"{used_gb:.1f} GB usados de {total_gb:.1f} GB  |  disponível: {mem.available/1024**3:.1f} GB")

            # DISCO espaço
            disk = shutil.disk_usage("/")
            disk_pct = disk.used / disk.total * 100
            self.bar_disk.set(disk_pct, f"{disk_pct:.1f}%")
            self.lbl_disk_detail.configure(
                text=f"{disk.used/1024**3:.1f} GB usados de {disk.total/1024**3:.1f} GB  |  livre: {disk.free/1024**3:.1f} GB")

            # DISCO I/O (MB/s simulado como % de 200 MB/s referência)
            cur_io = psutil.disk_io_counters()
            if cur_io and self._prev_io:
                delta_r = (cur_io.read_bytes  - self._prev_io.read_bytes)  / 1024**2
                delta_w = (cur_io.write_bytes - self._prev_io.write_bytes) / 1024**2
                total_io = delta_r + delta_w
                io_pct = min(total_io / 2, 100)  # escala: 200 MB/s = 100%
                self.bar_disk_io.set(io_pct, f"{total_io:.1f} MB/s")
            self._prev_io = cur_io

            # hora
            self.lbl_time.configure(text=datetime.now().strftime("%H:%M:%S"))

        except Exception as e:
            pass

        self.after(self.INTERVAL_MS, self._tick)


# ══════════════════════════════════════════════════════
#  PAINEL LIMPEZA
# ══════════════════════════════════════════════════════
class LimpezaPanel(tk.Frame):
    def __init__(self, parent, on_run_done=None):
        super().__init__(parent, bg=PANEL)
        self.on_run_done = on_run_done
        self.checks = []
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=PANEL)
        hdr.pack(fill="x", padx=14, pady=(12,6))
        tk.Label(hdr, text="LIMPEZA DO SISTEMA", font=("Segoe UI",8,"bold"),
                 bg=PANEL, fg=MUTED).pack(side="left")
        adm = "🔓 Admin" if IS_ADMIN else "🔒 Usuário"
        tk.Label(hdr, text=adm, font=F_SMALL, bg=PANEL,
                 fg=ACCENT if IS_ADMIN else WARN).pack(side="right")

        # checkboxes
        chk_frame = tk.Frame(self, bg=PANEL2, padx=12, pady=10)
        chk_frame.pack(fill="x", padx=14)

        self.var_all = tk.BooleanVar(value=True)
        tk.Checkbutton(chk_frame, text="  Selecionar tudo", variable=self.var_all,
                       font=F_UI, bg=PANEL2, fg=ACCENT, activebackground=PANEL2,
                       activeforeground=ACCENT, selectcolor=BG, cursor="hand2",
                       command=self._toggle_all).pack(anchor="w")
        tk.Frame(chk_frame, bg=BORDER, height=1).pack(fill="x", pady=6)

        for nome, func in TAREFAS:
            v = tk.BooleanVar(value=True)
            tk.Checkbutton(chk_frame, text=f"  {nome}", variable=v,
                           font=F_UI, bg=PANEL2, fg=TEXT,
                           activebackground=PANEL2, activeforeground=ACCENT2,
                           selectcolor=BG, cursor="hand2").pack(anchor="w", pady=1)
            self.checks.append((v, func, nome))

        # log
        tk.Label(self, text="LOG", font=("Segoe UI",8,"bold"),
                 bg=PANEL, fg=MUTED).pack(anchor="w", padx=14, pady=(10,2))
        self.logw = scrolledtext.ScrolledText(
            self, state="disabled", bg="#080808", fg=TEXT,
            font=F_MONO, relief="flat", bd=0, height=10, wrap="word")
        self.logw.pack(fill="both", expand=True, padx=14)
        for c in [ACCENT, ACCENT2, WARN, DANGER, MUTED, TEXT]:
            self.logw.tag_config(c, foreground=c)

        # botão
        self.btn = tk.Button(
            self, text="▶  INICIAR LIMPEZA",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT, fg=BG, activebackground="#00dd77", activeforeground=BG,
            relief="flat", cursor="hand2", padx=16, pady=8,
            command=self._run)
        self.btn.pack(pady=12)

        log(self.logw, "Pronto. Selecione as tarefas e clique em Iniciar.\n", MUTED)

    def _toggle_all(self):
        v = self.var_all.get()
        for var, _, _ in self.checks: var.set(v)

    def _run(self):
        sel = [(v,f,n) for v,f,n in self.checks if v.get()]
        if not sel: return log(self.logw, "⚠ Nenhuma tarefa selecionada.", WARN)
        self.btn.configure(state="disabled", text="⏳ Executando…")
        threading.Thread(target=self._worker, args=(sel,), daemon=True).start()

    def _worker(self, tarefas):
        log(self.logw, "─"*48, MUTED)
        log(self.logw, f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  |  {len(tarefas)} tarefas\n", ACCENT2)
        for _, func, nome in tarefas:
            log(self.logw, f"▸ {nome}", TEXT)
            try: func(self.logw)
            except Exception as e: log(self.logw, f"  ✗ {e}", DANGER)
        log(self.logw, "\n  ✅ Concluído! Reiniciar o PC potencializa os efeitos.", ACCENT)
        log(self.logw, "─"*48 + "\n", MUTED)
        self.btn.configure(state="normal", text="▶  INICIAR LIMPEZA")
        if self.on_run_done: self.on_run_done()

    def run_silent(self):
        """Chamado pelo agendador — roda todas as tarefas marcadas sem interação."""
        sel = [(v,f,n) for v,f,n in self.checks if v.get()]
        if sel:
            threading.Thread(target=self._worker, args=(sel,), daemon=True).start()


# ══════════════════════════════════════════════════════
#  PAINEL AGENDADOR
# ══════════════════════════════════════════════════════
class AgendadorPanel(tk.Frame):
    def __init__(self, parent, on_schedule_change=None):
        super().__init__(parent, bg=PANEL)
        self.on_change = on_schedule_change
        self._build()
        self._load()

    def _build(self):
        hdr = tk.Frame(self, bg=PANEL)
        hdr.pack(fill="x", padx=14, pady=(12,6))
        tk.Label(hdr, text="AGENDAMENTO AUTOMÁTICO", font=("Segoe UI",8,"bold"),
                 bg=PANEL, fg=MUTED).pack(side="left")

        card = tk.Frame(self, bg=PANEL2, padx=16, pady=16)
        card.pack(fill="x", padx=14, pady=4)

        # ativar/desativar
        self.var_ativo = tk.BooleanVar(value=False)
        tk.Checkbutton(card, text="  Ativar limpeza automática", variable=self.var_ativo,
                       font=F_UI, bg=PANEL2, fg=ACCENT, activebackground=PANEL2,
                       activeforeground=ACCENT, selectcolor=BG, cursor="hand2",
                       command=self._toggle).pack(anchor="w")

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", pady=10)

        # intervalo
        row1 = tk.Frame(card, bg=PANEL2)
        row1.pack(fill="x", pady=4)
        tk.Label(row1, text="Repetir a cada", font=F_UI, bg=PANEL2, fg=TEXT).pack(side="left")

        self.var_n = tk.StringVar(value="1")
        spin = tk.Spinbox(row1, from_=1, to=999, textvariable=self.var_n,
                          width=5, font=F_UI, bg=BG, fg=ACCENT, buttonbackground=PANEL,
                          relief="flat", insertbackground=ACCENT)
        spin.pack(side="left", padx=8)

        self.var_unit = tk.StringVar(value="horas")
        menu = ttk.Combobox(row1, textvariable=self.var_unit,
                            values=["minutos","horas","dias"],
                            width=8, font=F_UI, state="readonly")
        menu.pack(side="left")
        menu.configure(style="Dark.TCombobox")

        # próxima execução
        self.lbl_prox = tk.Label(card, text="", font=F_SMALL, bg=PANEL2, fg=MUTED)
        self.lbl_prox.pack(anchor="w", pady=(10,0))

        # botão salvar
        row2 = tk.Frame(card, bg=PANEL2)
        row2.pack(fill="x", pady=(14,0))
        tk.Button(row2, text="💾  Salvar configuração",
                  font=F_UI, bg=BORDER, fg=ACCENT,
                  activebackground=ACCENT, activeforeground=BG,
                  relief="flat", cursor="hand2", padx=12, pady=6,
                  command=self._save).pack(side="left")

        # histórico de execuções
        tk.Label(self, text="HISTÓRICO", font=("Segoe UI",8,"bold"),
                 bg=PANEL, fg=MUTED).pack(anchor="w", padx=14, pady=(16,4))
        self.hist = scrolledtext.ScrolledText(
            self, state="disabled", bg="#080808", fg=TEXT,
            font=F_MONO, relief="flat", bd=0, height=8, wrap="word")
        self.hist.pack(fill="both", expand=True, padx=14, pady=(0,14))
        self.hist.tag_config(ACCENT,  foreground=ACCENT)
        self.hist.tag_config(MUTED,   foreground=MUTED)
        self.hist.tag_config(ACCENT2, foreground=ACCENT2)

        self._update_prox_label()

    # ── persistência ──
    def _load(self):
        try:
            if os.path.exists(SCHEDULE_FILE):
                data = json.loads(open(SCHEDULE_FILE).read())
                self.var_ativo.set(data.get("ativo", False))
                self.var_n.set(str(data.get("n", 1)))
                self.var_unit.set(data.get("unit", "horas"))
                for ts in data.get("historico", []):
                    self._hist_add(ts, reload=True)
                self._update_prox_label()
        except: pass

    def _save(self):
        try: n = max(1, int(self.var_n.get()))
        except: n = 1
        self.var_n.set(str(n))
        data = {"ativo": self.var_ativo.get(), "n": n,
                "unit": self.var_unit.get(), "historico": self._get_hist_list()}
        open(SCHEDULE_FILE,"w").write(json.dumps(data, indent=2))
        self._update_prox_label()
        if self.on_change: self.on_change()

    def _toggle(self):
        self._save()

    def _get_interval_seconds(self):
        try: n = int(self.var_n.get())
        except: n = 1
        u = self.var_unit.get()
        return n * {"minutos":60,"horas":3600,"dias":86400}.get(u,3600)

    def get_interval(self):
        return self._get_interval_seconds()

    def is_active(self):
        return self.var_ativo.get()

    def _update_prox_label(self):
        if not self.var_ativo.get():
            self.lbl_prox.configure(text="Agendamento desativado.")
            return
        try: n = int(self.var_n.get())
        except: n = 1
        u = self.var_unit.get()
        prox = datetime.now() + timedelta(seconds=self._get_interval_seconds())
        self.lbl_prox.configure(
            text=f"Próxima execução em  {n} {u}  →  {prox.strftime('%d/%m/%Y %H:%M')}")

    def record_run(self):
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._hist_add(ts)
        self._save()
        self._update_prox_label()

    def _hist_add(self, ts, reload=False):
        self.hist.configure(state="normal")
        if not reload:
            self.hist.insert("1.0", f"  ✓ Limpeza automática executada em {ts}\n", ACCENT)
        else:
            self.hist.insert(tk.END, f"  · {ts}\n", MUTED)
        self.hist.configure(state="disabled")

    def _get_hist_list(self):
        txt = self.hist.get("1.0", tk.END)
        return [l.strip() for l in txt.splitlines() if l.strip()][:50]


# ══════════════════════════════════════════════════════
#  JANELA PRINCIPAL
# ══════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ Otimizador do PC  v2.0")
        self.geometry("960x700")
        self.minsize(860, 600)
        self.configure(bg=BG)
        self._sched_after = None
        self._build()
        self._start_monitor()
        self._sched_tick()

    # ── estilo ttk ──
    def _ttk_style(self):
        s = ttk.Style(self)
        s.theme_use("default")
        s.configure("Dark.TCombobox",
                    fieldbackground=BG, background=PANEL,
                    foreground=ACCENT, selectbackground=PANEL,
                    selectforeground=ACCENT, arrowcolor=ACCENT)

    def _build(self):
        self._ttk_style()

        # ── sidebar ──
        sidebar = tk.Frame(self, bg=PANEL, width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="⚡", font=("Segoe UI Emoji",24),
                 bg=PANEL, fg=ACCENT).pack(pady=(20,0))
        tk.Label(sidebar, text="OTIMIZADOR", font=("Segoe UI",8,"bold"),
                 bg=PANEL, fg=MUTED).pack()

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=16)

        self.nav_btns = []
        self._active_tab = tk.StringVar(value="monitor")
        for icon, label, key in [
            ("📊","Monitor",   "monitor"),
            ("🧹","Limpeza",   "limpeza"),
            ("📅","Agendar",   "agendar"),
        ]:
            b = tk.Button(sidebar, text=f"{icon}  {label}",
                          font=F_UI, bg=PANEL, fg=TEXT, bd=0, relief="flat",
                          activebackground=PANEL2, activeforeground=ACCENT,
                          cursor="hand2", anchor="w", padx=18, pady=10,
                          command=lambda k=key: self._switch(k))
            b.pack(fill="x")
            self.nav_btns.append((key, b))

        # versão no rodapé da sidebar
        tk.Label(sidebar, text="v2.0", font=F_SMALL, bg=PANEL, fg=MUTED).pack(side="bottom", pady=10)

        # ── área de conteúdo ──
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        # scroll wrapper para monitor
        self._frames = {}

        # Monitor (com scroll)
        mon_outer = tk.Frame(self.content, bg=BG)
        mon_canvas = tk.Canvas(mon_outer, bg=BG, bd=0, highlightthickness=0)
        mon_scroll = ttk.Scrollbar(mon_outer, orient="vertical", command=mon_canvas.yview)
        mon_canvas.configure(yscrollcommand=mon_scroll.set)
        mon_scroll.pack(side="right", fill="y")
        mon_canvas.pack(side="left", fill="both", expand=True)
        self.monitor_panel = MonitorPanel(mon_canvas)
        mon_win = mon_canvas.create_window((0,0), window=self.monitor_panel, anchor="nw")
        def _resize_mon(e):
            mon_canvas.itemconfig(mon_win, width=e.width)
        def _scroll_region(e):
            mon_canvas.configure(scrollregion=mon_canvas.bbox("all"))
        mon_canvas.bind("<Configure>", _resize_mon)
        self.monitor_panel.bind("<Configure>", _scroll_region)
        mon_canvas.bind_all("<MouseWheel>", lambda e: mon_canvas.yview_scroll(-1*(e.delta//120),"units"))
        self._frames["monitor"] = mon_outer

        self._frames["limpeza"] = LimpezaPanel(self.content, on_run_done=None)
        self._frames["agendar"] = AgendadorPanel(self.content, on_schedule_change=self._sched_tick)

        self._switch("monitor")

    def _switch(self, key):
        for k, frame in self._frames.items():
            frame.pack_forget()
        self._frames[key].pack(fill="both", expand=True)
        for k, b in self.nav_btns:
            b.configure(bg=PANEL2 if k==key else PANEL,
                        fg=ACCENT if k==key else TEXT)

    def _start_monitor(self):
        # inicializa psutil percpu antes de começar
        psutil.cpu_percent(interval=None, percpu=True)
        self.monitor_panel.start()

    # ── agendador ──
    def _sched_tick(self):
        if self._sched_after:
            self.after_cancel(self._sched_after)
        ag: AgendadorPanel = self._frames["agendar"]
        if ag.is_active():
            secs = ag.get_interval()
            ms   = max(secs * 1000, 60_000)  # mínimo 1 min para não travar
            self._sched_after = self.after(ms, self._sched_run)

    def _sched_run(self):
        ag: AgendadorPanel = self._frames["agendar"]
        lp: LimpezaPanel   = self._frames["limpeza"]
        ag.record_run()
        lp.run_silent()
        self._sched_tick()  # reagenda

    def on_close(self):
        self.monitor_panel.stop()
        self.destroy()


# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
