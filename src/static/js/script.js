document.getElementById('requestForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Получаем данные формы
    const formData = {
        student_info: document.getElementById('student_info').value,
        room: document.getElementById('room').value,
        request_text: document.getElementById('request_text').value
    };

    // Вывод данных формы в консоль
    console.log('Данные формы:', formData);
    
    try {
        // Отправляем данные на сервер
        const response = await fetch('/api/requests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            alert(`Заявка #${data.request_id} успешно создана!`);
            document.getElementById('requestForm').reset();
        } else {
            alert(`Ошибка: ${data.error || 'Неизвестная ошибка'}`);
        }
    } catch (error) {
        console.error('Ошибка при отправке:', error);
        alert('Ошибка соединения с сервером');
    }
});