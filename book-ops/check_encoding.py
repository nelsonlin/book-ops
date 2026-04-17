import sys
with open('sites/taiwan_library.py', 'rb') as f:
    content = f.read()
    # Find NO_RESULT_PATTERNS line
    start = content.find(b'NO_RESULT')
    if start >= 0:
        # Print 300 bytes around it
        snippet = content[start:start+350]
        print('Raw bytes:', repr(snippet[:200]))
        print()
        # Try utf-8 decode
        try:
            print('UTF8 decoded:')
            print(snippet.decode('utf-8')[:200])
        except Exception as e:
            print('UTF8 decode failed:', e)