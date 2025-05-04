from flask import Flask, render_template, request

app = Flask(__name__)


requests_db = [] # Позже все заявки будем хранить в БД 

@app.route('/', methods=['GET'])
def show_form():
    """Возвращает HTML форму для заявок"""
    return render_template('form.html')

@app.route('/api/requests', methods=['POST'])
def handle_request():
    """Обрабатывает отправку формы и сохраняет заявку"""
    if not request.is_json:
        return {'error': 'Request must be JSON'}, 400
    
    data = request.get_json()
    app.logger.debug(data)
    
    # Проверка обязательных полей
    required_fields = ['student_info', 'room', 'request_text']
    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    # Добавляем заявку в "БД"
    request_id = len(requests_db) + 1
    new_request = {
        'id': request_id,
        'status': 0,
        **data
    }
    requests_db.append(new_request)
    
    return {
        'status': 'success',
        'request_id': request_id,
        'message': 'Заявка успешно создана'
    }, 201

@app.route('/api/requests', methods=['GET'])
def get_requests():
    """Возвращает список всех заявок (для тестирования)"""
    return requests_db

@app.route('/admin')
def admin_panel():
    """Страница администрирования заявок"""
    return render_template('admin.html', requests=requests_db)

@app.route('/api/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    """Обновление статуса заявки"""
    data = request.get_json()
    
    # Находим заявку
    request_to_update = next((r for r in requests_db if r['id'] == request_id), None)
    if not request_to_update:
        return {"error": "Заявка не найдена"}, 404
    
    # Обновляем статус
    if 'status' in data:
        request_to_update['status'] = data['status']
    
    return {"status": "success", "request": request_to_update}    