#!/usr/bin/env python
"""
Test script to verify translations are loaded correctly
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import translation
from django.utils.translation import gettext as _

# Test Uzbek translations
with translation.override('uz'):
    print("Testing Uzbek (uz) translations:")
    print(f"  'Active Users' = '{_('Active Users')}'")
    print(f"  'Revenue' = '{_('Revenue')}'")
    print(f"  'Milestones' = '{_('Milestones')}'")
    print(f"  'Connect with Expert Mentors' = '{_('Connect with Expert Mentors')}'")
    print(f"  'Daily Focus' = '{_('Daily Focus')}'")
    print(f"  'Dashboard' = '{_('Dashboard')}'")

# Test Russian translations
with translation.override('ru'):
    print("\nTesting Russian (ru) translations:")
    print(f"  'Active Users' = '{_('Active Users')}'")
    print(f"  'Revenue' = '{_('Revenue')}'")
    print(f"  'Milestones' = '{_('Milestones')}'")
    print(f"  'Dashboard' = '{_('Dashboard')}'")

# List available languages in the gettext translations
print("\nChecking .mo file contents for Uzbek:")
mo_path = 'locale/uz/LC_MESSAGES/django.mo'
if os.path.exists(mo_path):
    import gettext
    try:
        uz_trans = gettext.GNUTranslations(open(mo_path, 'rb'))
        test_strings = [
            'Active Users',
            'Revenue',
            'Milestones',
            'Connect with Expert Mentors',
            'Daily Focus',
            'Dashboard'
        ]
        for s in test_strings:
            result = uz_trans.gettext(s)
            print(f"  '{s}' -> '{result}' (found: {result != s})")
    except Exception as e:
        print(f"  Error reading .mo file: {e}")
else:
    print(f"  .mo file not found at {mo_path}")
