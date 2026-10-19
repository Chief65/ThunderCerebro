import glob
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

files = [
    'creator/lab/bundle_recompensas_super_test.yml',
    'creator/lab/bundle_recompensas_rara_test.yml',
    'creator/lab/bundle_recompensas_epica_test.yml',
    'creator/lab/bundle_recompensas_mitica_test.yml',
    'creator/lab/bundle_recompensas_legend_test.yml'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    name_m = re.search(r"name:\s*['\"](.*)['\"]", text)
    mat_m = re.search(r"material:\s*([A-Z_]+)", text)
    upg_m = re.findall(r"(\d+):LOOP START: 1 \+\+\+ .*?title %player% title \"([^\"]+)\" \+\+\+ title %player% subtitle \"([^\"]+)\" \+\+\+ ei give %player% ([a-zA-Z0-9_]+)", text)
    jackpot_m = re.findall(r"(\d+):LOOP START: 1 \+\+\+ crates key give %player% ([a-zA-Z0-9_]+)", text)
    preview_m = re.search(r"dm open ([a-zA-Z0-9_]+)", text)
    
    print('=== FILE:', f)
    print('Name:', name_m.group(1) if name_m else 'N/A')
    print('Material:', mat_m.group(1) if mat_m else 'N/A')
    print('Preview GUI:', preview_m.group(1) if preview_m else 'N/A')
    print('Upgrades:', upg_m)
    print('Jackpots:', jackpot_m)
    # search rewards summary
    rewards_sec = re.findall(r"# APERTURA[^\n]*", text)
    print('Reward Sections:', rewards_sec)
    print('-----------------------------------------')
