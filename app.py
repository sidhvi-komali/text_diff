from flask import Flask, render_template, request
import difflib
import html

app = Flask(__name__)

def diff_highlight(text1, text2):
    matcher = difflib.SequenceMatcher(None, text1.split(), text2.split())
    result = ''
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            result += ' '.join(html.escape(word) for word in text1.split()[a0:a1]) + ' '
        elif opcode == 'delete':
            result += ' '.join(f'<span class="delete">{html.escape(word)}</span>' for word in text1.split()[a0:a1]) + ' '
        elif opcode == 'insert':
            result += ' '.join(f'<span class="insert">{html.escape(word)}</span>' for word in text2.split()[b0:b1]) + ' '
        elif opcode == 'replace':
            result += ' '.join(f'<span class="delete">{html.escape(word)}</span>' for word in text1.split()[a0:a1]) + ' '
            result += ' '.join(f'<span class="insert">{html.escape(word)}</span>' for word in text2.split()[b0:b1]) + ' '
    return result.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    highlighted = ''
    text1 = ''
    text2 = ''
    if request.method == 'POST':
        text1 = request.form['text1']
        text2 = request.form['text2']
        highlighted = diff_highlight(text1, text2)
    return render_template('index.html', result=highlighted, text1=text1, text2=text2)

if __name__ == '__main__':
    app.run(debug=True)
