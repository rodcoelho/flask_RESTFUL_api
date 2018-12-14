#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request

app = Flask(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


# ------------------------------------------------------------- #
# ---------------------------- GET ---------------------------- #
# ------------------------------------------------------------- #
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    """curl -i http://localhost:5000/todo/api/v1.0/tasks"""
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """curl -i http://localhost:5000/todo/api/v1.0/tasks/3"""
    task = [task for task in tasks if task_id == task['id']]
    if len(task) == 0:
        return jsonify({'error': 'Not Found'})
    return jsonify({'task': task[0]})


# ------------------------------------------------------------- #
# ---------------------------- POST --------------------------- #
# ------------------------------------------------------------- #
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    """curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks"""  # noqa
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'null'})
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get("description", ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


# ------------------------------------------------------------- #
# ------------------------- PUT/UPDATE ------------------------ #
# ------------------------------------------------------------- #
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2"""  # noqa
    task = [task for task in tasks if task['id'] == task_id]

    # -------------- catch mistakes -------------- #
    if len(task) == 0:
        return jsonify({'error': 'null'})
    if not request.json:
        return jsonify({'error': 'null'})
    if 'title' in request.json and not isinstance(request.json['title'], str):
        return jsonify({'error': 'null'})
    if 'description' in request.json and not isinstance(request.json['description'], str):
        return jsonify({'error': 'null'})
    if 'done' in request.json and type(request.json['done']) is not bool:
        return jsonify({'error': 'null'})

    # --------------- update dict --------------- #
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


# ------------------------------------------------------------- #
# --------------------------- DELETE -------------------------- #
# ------------------------------------------------------------- #
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """curl -X "DELETE"  http://localhost:5000/todo/api/v1.0/tasks/1"""  # noqa
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': 'null'})
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == "__main__":
    app.run(debug=True)

    """https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask"""

