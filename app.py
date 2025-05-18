from flask import Flask, render_template, request, redirect, url_for
import json, os, uuid

app = Flask(__name__)
DATA_FILE = '/usr/var/stores/items.json'

def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []

def save_items(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=4)

@app.route('/')
def index():
    items = load_items()
    return render_template('list.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        items = load_items()
        items.append({
            'id': str(uuid.uuid4()),
            'name': request.form['name'],
            'code': request.form['code'],
            'price': request.form['price'],
            'description': request.form['description']
        })
        save_items(items)
        return redirect(url_for('index'))
    return render_template('form.html', item=None)

@app.route('/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    items = load_items()
    item = next((x for x in items if x['id'] == item_id), None)
    if not item:
        return redirect(url_for('index'))
    if request.method == 'POST':
        item['name'] = request.form['name']
        item['code'] = request.form['code']
        item['price'] = request.form['price']
        item['description'] = request.form['description']
        save_items(items)
        return redirect(url_for('index'))
    return render_template('form.html', item=item)

@app.route('/delete/<item_id>')
def delete_item(item_id):
    items = load_items()
    items = [x for x in items if x['id'] != item_id]
    save_items(items)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

