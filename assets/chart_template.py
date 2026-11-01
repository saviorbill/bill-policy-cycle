# -*- coding: utf-8 -*-
"""
制图模版骨架（配套《制图模版说明.md》使用）
用法：复制本文件 → 修改数据与标题 → python 运行即可出图
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

import matplotlib.pyplot as plt
import numpy as np

# ===================== 统一配色常量 =====================
C_PRIMARY   = '#8B0000'   # 深红 · 主数据系列
C_SECONDARY = '#4A4A4A'   # 深灰 · 次数据系列 / 文字
C_GOLD      = '#C9A227'   # 金色 · 第三系列 / 特殊标注
C_DARK      = '#1a1a1a'   # 标题黑
C_RED2      = '#B22222'   # 辅助红
C_GRAY_L    = '#999999'   # 网格 / 普通项
C_BG_LIGHT  = '#F5F5F5'   # 极淡阶段背景
C_GOLD_BG   = '#FFF8E1'   # 金色注释框底色
C_RED_BG    = '#FFEBEE'   # 红色标记底色

# ===================== 统一字号常量（2026.11 更新：正文15 / 标题16） =====================
FS_BASE  = 15   # 正文 / 轴标签 / 刻度 / 数值标注 / 注释 / 图例 / 数据来源
FS_TITLE = 16   # 图表标题

# 输出目录：默认当前工作目录，可用环境变量 CHART_OUT_DIR 覆盖
OUT_DIR = os.environ.get('CHART_OUT_DIR', './')


def new_fig(figsize=(12, 7)):
    """标准画布初始化（每张图必走此流程）"""
    setup_plot()
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')
    ax.set_facecolor('white')
    return fig, ax


def style_ax(ax, grid_axis='y'):
    """通用样式：网格在数据层下方 + 隐藏上右边框 + 统一刻度字号"""
    ax.grid(axis=grid_axis, alpha=0.25, color=C_GRAY_L, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', labelsize=FS_BASE)


def add_title(ax, title, pad=15):
    ax.set_title(title, fontsize=FS_TITLE, fontweight='bold', color=C_DARK, pad=pad)


def add_legend(ax):
    ax.legend(loc='upper left', fontsize=FS_BASE, framealpha=0.9,
              facecolor='white', edgecolor='#cccccc')


def add_source(fig, text, y=-0.02):
    """数据来源：图表外部、时间轴正下方"""
    fig.text(0.5, y, f'数据来源：{text}', ha='center', fontsize=FS_BASE, color=C_SECONDARY)


def save_fig(fig, filename):
    fig.savefig(OUT_DIR + filename, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'已生成: {OUT_DIR}{filename}')


# ============================================================
# 模版 1：折线/时序图（宏观月报最常用）
# ============================================================
def demo_line():
    months = ['2025.01', '2025.04', '2025.07', '2025.10', '2026.01', '2026.04', '2026.07']
    x = np.arange(len(months))
    y1 = [49.5, 50.2, 49.8, 50.5, 51.0, 50.3, 50.8]   # 示例：PMI
    y2 = [48.0, 48.5, 49.0, 49.2, 49.5, 49.0, 49.6]   # 示例：新订单

    fig, ax = new_fig()
    ax.plot(x, y1, color=C_PRIMARY, linewidth=2.2, marker='o', markersize=4, label='制造业PMI')
    ax.plot(x, y2, color=C_SECONDARY, linewidth=2.0, linestyle='--', label='新订单指数')
    ax.axhline(y=50, color=C_GRAY_L, linewidth=1, linestyle=':', alpha=0.6)  # 荣枯线
    # 阶段背景（极淡，置于数据下方）
    ax.axvspan(0, 2, color=C_BG_LIGHT, alpha=0.5, zorder=0)

    # 关键节点标注：上下交替 + 引线
    ax.annotate('节点标注示例', xy=(4, y1[4]), xytext=(4, y1[4] + 1.2),
                fontsize=FS_BASE, ha='center', color=C_SECONDARY,
                arrowprops=dict(arrowstyle='->', color=C_GRAY_L, lw=0.8),
                bbox=dict(boxstyle='round,pad=0.3', facecolor=C_BG_LIGHT, edgecolor='#cccccc'))

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=FS_BASE)
    ax.set_ylabel('指数 (%)', fontsize=FS_BASE, color=C_DARK)
    add_title(ax, '指标走势（2025.01 — 2026.07）')
    add_legend(ax)
    style_ax(ax)
    add_source(fig, '国家统计局，截至2026年7月')
    plt.tight_layout()
    save_fig(fig, 'demo_line.png')


# ============================================================
# 模版 2：分组柱状图
# ============================================================
def demo_grouped_bar():
    names = ['类别A', '类别B', '类别C', '类别D', '类别E']
    v1 = [17.5, 32.5, 4.0, 0.5, 0.5]
    v2 = [60.5, 44.7, 75.0, 64.0, 30.0]

    fig, ax = new_fig()
    x = np.arange(len(names))
    w = 0.35
    bars1 = ax.bar(x - w/2, v1, w, label='系列一(%)', color=C_PRIMARY, edgecolor='white')
    bars2 = ax.bar(x + w/2, v2, w, label='系列二(%)', color=C_SECONDARY, edgecolor='white', alpha=0.7)

    for bars, color in ((bars1, C_PRIMARY), (bars2, C_SECONDARY)):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', fontsize=FS_BASE, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=FS_BASE)
    ax.set_ylabel('占比 (%)', fontsize=FS_BASE, color=C_DARK)
    ax.set_ylim(0, 90)
    add_title(ax, '分组对比图标题')
    add_legend(ax)
    style_ax(ax)
    add_source(fig, '各公司年报（截至2025年）')
    plt.tight_layout()
    save_fig(fig, 'demo_grouped_bar.png')


# ============================================================
# 模版 3：横向条形图（排名类）
# ============================================================
def demo_barh():
    names = ['第一名', '第二名', '第三名', '第四名', '第五名', '第六名']
    values = [167, 95, 75, 60, 28, 22]

    fig, ax = new_fig()
    colors = [C_PRIMARY if i == 0 else C_SECONDARY if i < 4 else C_GRAY_L
              for i in range(len(names))]
    bars = ax.barh(names[::-1], values[::-1], color=colors[::-1], edgecolor='white', height=0.6)

    for bar, val in zip(bars, values[::-1]):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}',
                va='center', fontsize=FS_BASE, color=C_DARK)

    ax.set_xlabel('数值 (单位)', fontsize=FS_BASE, color=C_DARK)
    ax.set_xlim(0, max(values) * 1.2)
    add_title(ax, '排名图标题（2025年）')
    style_ax(ax, grid_axis='x')
    add_source(fig, '机构名称，截至2025年')
    plt.tight_layout()
    save_fig(fig, 'demo_barh.png')


# ============================================================
# 模版 4：对比柱状图 + 金色注释框
# ============================================================
def demo_bar_annotation():
    cats = ['供给', '需求', '缺口']
    vals = [18, 100, 82]
    colors = [C_SECONDARY, C_PRIMARY, C_GOLD]

    fig, ax = new_fig()
    bars = ax.bar(cats, vals, color=colors, edgecolor='white', width=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{val}%',
                ha='center', fontsize=FS_BASE, fontweight='bold', color=C_DARK)

    # 金色注释框
    ax.text(2, 60, '关键说明\n放在这里', fontsize=FS_BASE, ha='center',
            color=C_GOLD, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=C_GOLD_BG, edgecolor=C_GOLD))

    ax.set_ylabel('占比 (%)', fontsize=FS_BASE, color=C_DARK)
    ax.set_ylim(0, 120)
    add_title(ax, '供需对比图标题')
    style_ax(ax)
    add_source(fig, '研究机构综合估算（2025-2026年）')
    plt.tight_layout()
    save_fig(fig, 'demo_bar_annotation.png')


# ============================================================
# 模版 5：饼图（份额类）
# ============================================================
def demo_pie():
    labels = ['企业A', '企业B', '企业C', '企业D', '其他']
    shares = [22, 18, 8, 6, 46]
    colors_pie = [C_PRIMARY, C_SECONDARY, C_RED2, '#696969', '#E8E8E8']

    fig, ax = new_fig()
    wedges, texts, autotexts = ax.pie(
        shares, labels=labels, autopct='%1.1f%%', colors=colors_pie,
        startangle=90, pctdistance=0.75, labeldistance=1.15,
        textprops={'fontsize': FS_BASE, 'color': C_DARK})
    for at in autotexts:
        at.set_fontsize(FS_BASE)
        at.set_color('white' if at.get_text() != '46.0%' else C_SECONDARY)  # 浅色扇区用深字

    add_title(ax, '份额分布图标题（2025年）', pad=20)
    add_source(fig, '研究机构《报告名称》', y=0.02)
    plt.tight_layout()
    save_fig(fig, 'demo_pie.png')


# ============================================================
# 模版 6：时间线图（政策窗口 / 事件演进）
# ============================================================
def demo_timeline():
    phases = ['阶段一', '阶段二', '阶段三', '阶段四', '阶段五']
    positions = [0, 1, 2, 3, 4]
    colors_phase = [C_SECONDARY, C_PRIMARY, C_RED2, C_GOLD, C_SECONDARY]
    annotations = ['说明文字\n上下交替', '说明文字\n上下交替', '说明文字\n上下交替',
                   '关键节点', '最终状态']

    fig, ax = new_fig(figsize=(12, 5))
    ax.plot(positions, [0.5]*5, color=C_SECONDARY, linewidth=3, zorder=1)
    for i, (phase, pos) in enumerate(zip(phases, positions)):
        ax.scatter(pos, 0.5, s=200, color=colors_phase[i], zorder=2,
                   edgecolors='white', linewidth=2)
        ax.text(pos, 0.65, phase, ha='center', fontsize=FS_BASE,
                fontweight='bold', color=C_DARK)
    for i, (ann, pos) in enumerate(zip(annotations, positions)):
        y_off = 0.2 if i % 2 == 0 else -0.15
        ax.annotate(ann, xy=(pos, 0.5), xytext=(pos, y_off),
                    fontsize=FS_BASE, ha='center', color=C_SECONDARY,
                    arrowprops=dict(arrowstyle='->', color=C_GRAY_L, lw=0.8),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=C_BG_LIGHT, edgecolor='#cccccc'))

    # 当前时点标记
    ax.annotate('', xy=(1.5, 0.5), xytext=(1.5, 0.85),
                arrowprops=dict(arrowstyle='->', color=C_PRIMARY, lw=2))
    ax.text(1.5, 0.92, '当前\n2026.10', ha='center', fontsize=FS_BASE,
            fontweight='bold', color=C_PRIMARY,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=C_RED_BG, edgecolor=C_PRIMARY))

    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.3, 1.15)
    ax.axis('off')
    add_title(ax, '事件时间线标题（截至YYYY年M月）')
    add_source(fig, '公告及会议纪要，截至2026年10月')
    plt.tight_layout()
    save_fig(fig, 'demo_timeline.png')


if __name__ == '__main__':
    demo_line()
    demo_grouped_bar()
    demo_barh()
    demo_bar_annotation()
    demo_pie()
    demo_timeline()
    print('\n全部模版示例图生成完毕')
