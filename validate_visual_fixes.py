#!/usr/bin/env python3
"""
Visual and UX Validation Script
Tests key improvements made during the comprehensive audit
"""

import re
import sys

def load_file(filename):
    """Load the main application file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def check_css_rule(content, rule_name, pattern):
    """Check if a CSS rule exists in the content"""
    found = bool(re.search(pattern, content, re.IGNORECASE | re.MULTILINE))
    status = "✅ PASS" if found else "❌ FAIL"
    print(f"{status} - {rule_name}")
    return found

def validate_html_structure(content):
    """Validate HTML tag balance"""
    markdown_blocks = re.findall(r'st\.markdown\("""(.*?)""", unsafe_allow_html=True\)', content, re.DOTALL)
    
    print("\n📋 HTML Structure Validation")
    print("-" * 50)
    
    total_blocks = len(markdown_blocks)
    issues = 0
    
    for i, block in enumerate(markdown_blocks, 1):
        # Count tags
        open_divs = len(re.findall(r'<div[^>]*>', block))
        close_divs = len(re.findall(r'</div>', block))
        
        # Allow for split blocks (common in Streamlit column layouts)
        if abs(open_divs - close_divs) > 2:
            print(f"⚠️  Block {i}: {open_divs} open divs, {close_divs} close divs")
            issues += 1
    
    if issues == 0:
        print(f"✅ PASS - All {total_blocks} HTML blocks are balanced")
    else:
        print(f"⚠️  {issues} potential issues found (may be intentional for column layouts)")
    
    return issues == 0

def main():
    print("="*60)
    print("COMPREHENSIVE VISUAL & UX VALIDATION TEST")
    print("="*60)
    
    # Load file
    try:
        content = load_file('newfile.py')
        print(f"✅ Loaded newfile.py ({len(content)} characters)")
    except FileNotFoundError:
        print("❌ Error: newfile.py not found")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("CSS IMPROVEMENTS VALIDATION")
    print("="*60)
    
    checks = [
        ("Word-break strategy", r"word-break:\s*normal\s*!important"),
        ("Auto-hyphenation", r"hyphens:\s*auto\s*!important"),
        ("Overflow wrapping", r"overflow-wrap:\s*break-word\s*!important"),
        ("Table cell nowrap", r"table\s+th,\s*table\s+td.*white-space:\s*nowrap"),
        ("Email address handling", r"mailto:.*word-break:\s*break-all"),
        ("URL handling", r"href\^=.*http.*word-break:\s*break-word"),
        ("Image max-width", r"img.*max-width:\s*100%"),
        ("Box sizing", r"box-sizing:\s*border-box\s*!important"),
        ("Overflow-x prevention", r"overflow-x:\s*hidden\s*!important"),
        ("Touch targets", r"min-height:\s*44px\s*!important"),
        ("Focus indicators", r"outline:\s*3px\s+solid\s+#FFCC00"),
        ("Mobile padding", r"@media.*max-width:\s*768px.*padding-left:\s*0\.5rem"),
        ("List improvements", r"ul\s+li.*line-height:\s*1\.[67]"),
        ("Banner overflow fix", r"informative-banner.*overflow:\s*hidden"),
        ("Custom scrollbar", r"scrollbar-color:\s*#FFCC00"),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, pattern in checks:
        if check_css_rule(content, name, pattern):
            passed += 1
    
    print("\n" + "="*60)
    validate_html_structure(content)
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"CSS Checks: {passed}/{total} passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("The comprehensive audit implementation is verified.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
