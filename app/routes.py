from flask import render_template, request, current_app as app
from business import BusinessLogic
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    fecha = None
    error = None
    tipo_cambio = None
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        business_logic = BusinessLogic()
        try:
          
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            
            fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            tipo_cambio = business_logic.consultar_tipo_cambio(fecha_formateada)
            print(tipo_cambio)
        except Exception as e:
            error = str(e)
    return render_template('index.html', error=error, fecha=fecha, tipo_cambio=tipo_cambio)

if __name__ == '__main__':
    app.run(debug=True)

