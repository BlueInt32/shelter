from flask import Flask
app = Flask(__name__)

print(__name__)

gems = [
    {
        'id': 1,
        'title': 'Gem number 1'
    },
    {
        'id': 2,
        'title': 'Gem number 2'
    }
]

@app.route('/')
def index():
    return 'coucou'

@app.route('/gems')
def get_gems():
    return {'gems':gems}

@app.route('/gems/<int:gemId>')
def get_gem_by_id(gemId):
    return_value = {}
    for gem in gems:
        if gem["id"] == gemId:
            return_value = gem
            return return_value

if __name__ == "__main__":
    app.run(port=5001)