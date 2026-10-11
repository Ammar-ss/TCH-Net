"""Rebuild partA_log.txt (text outputs of the executed Part A notebook), which make_numbers.py
reads for record counts, window counts, and the missingness test.

Usage: python extract_log.py ../notebooks/BRIDGE_rev2_partA.ipynb
"""
import json, os, sys
nb = json.load(open(sys.argv[1]))
text = ''
for c in nb['cells']:
    if c['cell_type'] != 'code':
        continue
    for o in c.get('outputs', []):
        text += ''.join(o.get('text', [])) + '\n'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partA_log.txt'), 'w').write(text)
print('wrote partA_log.txt')
