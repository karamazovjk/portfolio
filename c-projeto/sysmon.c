#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define RESET   "\033[0m"
#define BOLD    "\033[1m"
#define CYAN    "\033[36m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define RED     "\033[31m"
#define MAGENTA "\033[35m"
#define CLEAR   "\033[2J\033[H"
#define BAR_WIDTH 30

typedef struct {
    long user, nice, system, idle, iowait, irq, softirq;
} CpuTimes;

int read_cpu(CpuTimes *ct) {
    FILE *f = fopen("/proc/stat", "r");
    if (!f) return -1;
    int r = fscanf(f, "cpu %ld %ld %ld %ld %ld %ld %ld",
                   &ct->user, &ct->nice, &ct->system, &ct->idle,
                   &ct->iowait, &ct->irq, &ct->softirq);
    fclose(f);
    return (r == 7) ? 0 : -1;
}

double calc_cpu_usage(CpuTimes *prev, CpuTimes *curr) {
    long prev_idle  = prev->idle + prev->iowait;
    long curr_idle  = curr->idle + curr->iowait;
    long prev_total = prev->user + prev->nice + prev->system + prev_idle + prev->irq + prev->softirq;
    long curr_total = curr->user + curr->nice + curr->system + curr_idle + curr->irq + curr->softirq;
    long total_diff = curr_total - prev_total;
    long idle_diff  = curr_idle  - prev_idle;
    if (total_diff == 0) return 0.0;
    return 100.0 * (total_diff - idle_diff) / total_diff;
}

void read_mem(long *total_kb, long *avail_kb) {
    FILE *f = fopen("/proc/meminfo", "r");
    if (!f) return;
    char key[64];
    long val;
    *total_kb = 0; *avail_kb = 0;
    while (fscanf(f, "%63s %ld kB\n", key, &val) == 2) {
        if (strcmp(key, "MemTotal:")     == 0) *total_kb = val;
        if (strcmp(key, "MemAvailable:") == 0) *avail_kb = val;
        if (*total_kb && *avail_kb) break;
    }
    fclose(f);
}

void read_uptime(long *seconds) {
    FILE *f = fopen("/proc/uptime", "r");
    *seconds = 0;
    if (!f) return;
    double up = 0.0;
    if (fscanf(f, "%lf", &up) == 1)
        *seconds = (long)up;
    fclose(f);
}

void print_bar(double pct, const char *color) {
    int filled = (int)(pct / 100.0 * BAR_WIDTH);
    printf("%s[", color);
    for (int i = 0; i < BAR_WIDTH; i++)
        printf("%s", i < filled ? "█" : "░");
    printf("]" RESET);
}

const char *pct_color(double pct) {
    if (pct < 50) return GREEN;
    if (pct < 80) return YELLOW;
    return RED;
}

void fmt_uptime(long s, char *buf) {
    long d = s / 86400; s %= 86400;
    long h = s / 3600;  s %= 3600;
    long m = s / 60;    s %= 60;
    if (d > 0) sprintf(buf, "%ldd %02ldh %02ldm %02lds", d, h, m, s);
    else       sprintf(buf, "%02ldh %02ldm %02lds", h, m, s);
}

int main(void) {
    CpuTimes prev, curr;
    if (read_cpu(&prev) != 0) {
        fprintf(stderr, "Erro ao ler /proc/stat\n");
        return 1;
    }

    printf("Iniciando sysmon... aguarde 1s para leitura de CPU.\n");
    sleep(1);

    while (1) {
        read_cpu(&curr);
        double cpu_pct = calc_cpu_usage(&prev, &curr);
        prev = curr;

        long total_kb = 0, avail_kb = 0;
        read_mem(&total_kb, &avail_kb);
        long used_kb = total_kb - avail_kb;
        double mem_pct = total_kb ? 100.0 * used_kb / total_kb : 0;

        long uptime_s = 0;
        read_uptime(&uptime_s);
        char upbuf[64];
        fmt_uptime(uptime_s, upbuf);

        double mem_used_mb  = used_kb  / 1024.0;
        double mem_total_mb = total_kb / 1024.0;

        printf(CLEAR);
        printf(BOLD CYAN "╔══════════════════════════════════════════╗\n");
        printf(          "║         sysmon — monitor em tempo real   ║\n");
        printf(          "╚══════════════════════════════════════════╝\n" RESET);
        printf("\n");
        printf(BOLD "  ⏱  Uptime   " RESET MAGENTA "%s\n" RESET, upbuf);
        printf("\n");

        const char *cc = pct_color(cpu_pct);
        printf(BOLD "  CPU  " RESET);
        print_bar(cpu_pct, cc);
        printf("  %s%.1f%%\n" RESET, cc, cpu_pct);

        const char *mc = pct_color(mem_pct);
        printf(BOLD "  MEM  " RESET);
        print_bar(mem_pct, mc);
        printf("  %s%.1f%%  " RESET, mc, mem_pct);
        printf("(%.0f / %.0f MB)\n", mem_used_mb, mem_total_mb);

        printf("\n" CYAN "  atualiza a cada 1s — Ctrl+C para sair\n" RESET);

        sleep(1);
    }
    return 0;
}
