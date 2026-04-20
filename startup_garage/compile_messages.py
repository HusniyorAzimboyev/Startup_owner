#!/usr/bin/env python
"""
Simple script to compile .po files to .mo files using polib
"""
import os
import sys
import polib

locale_dir = os.path.dirname(__file__)

for lang_dir in os.listdir(locale_dir):
    lang_path = os.path.join(locale_dir, lang_dir, 'LC_MESSAGES')
    
    if not os.path.isdir(lang_path):
        continue
    
    po_file = os.path.join(lang_path, 'django.po')
    mo_file = os.path.join(lang_path, 'django.mo')
    
    if not os.path.exists(po_file):
        continue
    
    print(f"Compiling {po_file}...")
    
    try:
        po = polib.pofile(po_file)
        po.save_as_mofile(mo_file)
        print(f"✓ Successfully compiled to {mo_file}")
    except Exception as e:
        print(f"✗ Error compiling {po_file}: {e}")
        sys.exit(1)

print("\nAll translation files compiled successfully!")
