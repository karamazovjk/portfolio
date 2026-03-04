import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

BG       = "#0F1117"
CARD     = "#181C27"
GRID_C   = "#252A38"
TEXT_PRI = "#F0F2FA"
TEXT_SEC = "#7B82A0"
ACCENT   = "#5B8DEF"
PALETTE  = ["#5B8DEF", "#A78BFA", "#34D399", "#F472B6", "#FBBF24", "#60A5FA"]
MEAN_C   = "#F472B6"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "text.color": TEXT_PRI,
    "axes.facecolor": CARD, "axes.edgecolor": GRID_C,
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlepad": 14,
    "axes.labelsize": 9, "figure.facecolor": BG,
    "grid.color": GRID_C, "grid.linewidth": 0.6,
    "xtick.color": TEXT_SEC, "ytick.color": TEXT_SEC,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
})

# ── Sample data (replace with your df) ────────────────────────────────────────
np.random.seed(7)
n = 4000
df = pd.DataFrame({
    'Daily_Phone_Hours':         np.random.gamma(3, 1.5, n).clip(0.5, 14),
    'Weekend_Screen_Time_Hours': np.random.gamma(3.5, 1.8, n).clip(0.5, 16),
    'Social_Media_Hours':        np.random.gamma(2, 1.2, n).clip(0, 8),
    'Occupation': np.random.choice(
        ['Tecnologia', 'Saúde', 'Educação', 'Finanças', 'Varejo', 'Outros'],
        n, p=[0.25, 0.18, 0.15, 0.14, 0.13, 0.15]
    ),
    'Device_Type': np.random.choice(['Android', 'iOS'], n, p=[0.54, 0.46]),
})
# inject mild correlation
df['Weekend_Screen_Time_Hours'] += df['Daily_Phone_Hours'] * 0.4

# ── Figure & layout ───────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 11))
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.06, right=0.97, top=0.84, bottom=0.09,
                    hspace=0.44, wspace=0.36)

gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_facecolor(CARD)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_C)

# ── Header ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.965, 'PADRÕES DE USO DE SMARTPHONE',
         ha='center', va='top', fontsize=15, fontweight='bold', color=TEXT_PRI)
fig.text(0.5, 0.908, f'Base: {len(df):,} usuários  ·  Análise de comportamento digital  ·  2025',
         ha='center', va='top', fontsize=8.5, color=TEXT_SEC)
fig.add_artist(plt.Line2D([0.20, 0.80], [0.900, 0.900],
               transform=fig.transFigure, color=ACCENT, linewidth=0.8, alpha=0.5))

# ── Chart 1 · Daily Hours Histogram ──────────────────────────────────────────
hours = df['Daily_Phone_Hours']
bins  = np.linspace(hours.min(), hours.max(), 30)
n_vals, edges, patches = ax1.hist(hours, bins=bins, color=ACCENT,
                                   edgecolor=BG, linewidth=0.4, zorder=3)
norm_vals = n_vals / n_vals.max()
for patch, nv in zip(patches, norm_vals):
    patch.set_alpha(0.4 + 0.6 * nv)

mean_h = hours.mean()
ax1.axvline(mean_h, color=MEAN_C, linewidth=1.6, linestyle='--', zorder=4)
ax1.text(mean_h + 0.15, ax1.get_ylim()[1] * 0.93,
         f'Média\n{mean_h:.1f}h', color=MEAN_C, fontsize=7.5,
         fontweight='bold', va='top')

ax1.set_title('Horas de Uso Diário', color=TEXT_PRI)
ax1.set_xlabel('Horas / dia', color=TEXT_SEC)
ax1.set_ylabel('Frequência', color=TEXT_SEC)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax1.tick_params(colors=TEXT_SEC)
ax1.grid(axis='y', color=GRID_C, linewidth=0.6, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ── Chart 2 · Social Media by Occupation ─────────────────────────────────────
sm_occ      = df.groupby('Occupation')['Social_Media_Hours'].mean().sort_values()
bar_colors2 = [PALETTE[i % len(PALETTE)] for i in range(len(sm_occ))]

# track bars
ax2.barh(sm_occ.index, [sm_occ.max() * 1.18] * len(sm_occ),
         color=GRID_C, height=0.6, zorder=1, alpha=0.35)
bars2 = ax2.barh(sm_occ.index, sm_occ.values, color=bar_colors2,
                  height=0.6, zorder=3)

for bar, val in zip(bars2, sm_occ.values):
    ax2.text(val + sm_occ.max() * 0.025,
             bar.get_y() + bar.get_height() / 2,
             f'{val:.2f}h', va='center', fontsize=8, color=TEXT_SEC)

ax2.set_title('Média de Redes Sociais por Ocupação', color=TEXT_PRI)
ax2.set_xlabel('Horas / dia', color=TEXT_SEC)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.1f}'))
ax2.set_xlim(0, sm_occ.max() * 1.38)
ax2.tick_params(colors=TEXT_SEC)
ax2.tick_params(axis='y', length=0)
ax2.grid(axis='x', color=GRID_C, linewidth=0.6, zorder=0)
ax2.set_axisbelow(True)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)

# ── Chart 3 · Scatter: Weekday vs Weekend ────────────────────────────────────
# hex-bin density for legibility over raw scatter
hb = ax3.hexbin(df['Daily_Phone_Hours'], df['Weekend_Screen_Time_Hours'],
                gridsize=38, cmap='Blues', mincnt=1,
                linewidths=0.2)
hb.set_clim(0, hb.get_array().max() * 0.75)   # boost contrast

# regression line
m, b = np.polyfit(df['Daily_Phone_Hours'], df['Weekend_Screen_Time_Hours'], 1)
x_line = np.linspace(hours.min(), hours.max(), 120)
ax3.plot(x_line, m * x_line + b, color=MEAN_C, linewidth=1.6,
         linestyle='--', zorder=5, label='Tendência')

corr = df['Daily_Phone_Hours'].corr(df['Weekend_Screen_Time_Hours'])
ax3.text(0.05, 0.91, f'r = {corr:.2f}',
         transform=ax3.transAxes, fontsize=9, fontweight='bold',
         color=TEXT_PRI,
         bbox=dict(boxstyle='round,pad=0.4', facecolor=GRID_C,
                   edgecolor=ACCENT, linewidth=1.0, alpha=0.85))

ax3.set_title('Uso Diário vs Fim de Semana', color=TEXT_PRI)
ax3.set_xlabel('Horas / dia (semana)', color=TEXT_SEC)
ax3.set_ylabel('Horas / dia (fim de semana)', color=TEXT_SEC)
ax3.tick_params(colors=TEXT_SEC)
ax3.grid(color=GRID_C, linewidth=0.5, zorder=0)
ax3.set_axisbelow(True)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# ── Chart 4 · Device Type Donut ───────────────────────────────────────────────
device_counts = df['Device_Type'].value_counts()
dev_colors    = [PALETTE[0], PALETTE[2]]

wedges, _, autotexts = ax4.pie(
    device_counts,
    labels=None,
    autopct='%1.1f%%',
    colors=dev_colors,
    startangle=90,
    pctdistance=0.72,
    wedgeprops={'edgecolor': BG, 'linewidth': 3.0, 'width': 0.50},
)
for at in autotexts:
    at.set_fontsize(9.5)
    at.set_fontweight('bold')
    at.set_color(TEXT_PRI)

ax4.text(0, 0, f'{len(df):,}\nusuários', ha='center', va='center',
         fontsize=9, color=TEXT_PRI, fontweight='bold', linespacing=1.6)

legend_patches = [
    mpatches.Patch(color=c, label=f'{lbl}  {cnt:,}')
    for c, lbl, cnt in zip(dev_colors, device_counts.index, device_counts.values)
]
ax4.legend(handles=legend_patches, loc='lower center',
           bbox_to_anchor=(0.5, -0.12), ncol=2,
           frameon=False, fontsize=8.5, labelcolor=TEXT_SEC)
ax4.set_title('Distribuição por Tipo de Dispositivo', color=TEXT_PRI)

# ── Export ────────────────────────────────────────────────────────────────────
plt.savefig('/mnt/user-data/outputs/smartphone_usage.png',
            dpi=160, bbox_inches='tight', facecolor=BG)
plt.show()
print("Saved → smartphone_usage.png")
