with open('src/pages/Verification.jsx', 'r') as f:
    content = f.read()
content = content.replace(r'setProgress(1/\);', 'setProgress(1/);')
with open('src/pages/Verification.jsx', 'w') as f:
    f.write(content)
