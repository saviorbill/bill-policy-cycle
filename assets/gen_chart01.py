# -*- coding: utf-8 -*-
"""
示例图：政策定调分组下的沪深300年均收益（2005-2025）
用途：验证 chart_template.py 骨架 + 防重叠规范
数据：models/政策与资产相关性矩阵.md（datahubco tushare index_daily 复算）
运行：CHART_OUT_DIR=<输出目录> python gen_chart01.py
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chart_template import (new_fig, style_ax, add_title, add_source, save_fig,
                            C_PRIMARY, C_SECONDARY, C_GOLD, C_DARK, C_GOLD_BG,
                            FS_BASE)

# 政策与资产相关性矩阵 · 分组验证（n=21）
cats = ['宽松年\n(指数>0, n=10)', '收紧年\n(指数<0, n=7)']
vals = [10.8, 36.3]
colors = [C_SECONDARY, C_PRIMARY]   # 收紧年为反直觉焦点项，用深红

fig, ax = new_fig()
bars = ax.bar(cats, vals, color=colors, edgecolor='white', width=0.45, alpha=0.9)

for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2,
            f'+{val}%', ha='center', fontsize=FS_BASE, fontweight='bold', color=C_DARK)

# 金色注释框：解释反直觉结论（放在左上空白区，避开柱体与数值）
ax.text(0.02, 0.72, '反直觉但稳健：\n宽松常发生在弱市、收紧常在牛市后期\n——政策是逆周期的"果"，要看拐点而非水平',
        transform=ax.transAxes, fontsize=FS_BASE, ha='left', va='top',
        color=C_GOLD, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=C_GOLD_BG, edgecolor=C_GOLD))

ax.set_ylabel('沪深300 年度平均收益 (%)', fontsize=FS_BASE, color=C_DARK)
ax.set_ylim(0, 46)          # 顶部留白，避免数值标注顶到标题
ax.tick_params(axis='x', labelsize=FS_BASE)
add_title(ax, '宽松年 vs 收紧年：沪深300平均收益（2005 — 2025）')
style_ax(ax)
add_source(fig, 'datahubco tushare index_daily（沪深300），政策宽松度指数为人工打分')
save_fig(fig, 'chart01_policy_hs300.png')
