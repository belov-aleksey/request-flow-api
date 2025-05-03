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
        'status': 'new',
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