from flask import request, make_response, jsonify
from SRC.server.instance import server
from flask_pydantic_spec import Response, Request
from SRC.model.Paciente.Paciente import Paciente
from SRC.model.Paciente.Pacientes import Pacientes
from Model import Model
from SRC.model.Erro import Erro
from db import conn


@server.app.get('/Pacientes')
@server.api.validate(resp=Response(HTTP_200=Pacientes), tags=['Pacientes'])
def getProdutos():
    """
    Retorna todos os Pacientes da base de dados

    """
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, Name, Sex, age, Chest_pain_type, BP, Cholesterol, FBS_over_120, EKG_results, Max_HR, Exercise_angina, ST_depression, Slope_of_ST, Number_of_vessels_fluro, Thallium, Heart_Disease FROM Pacientes order by id desc')
    pacientes = cursor.fetchall()

    cursor.close()

    pacientesVO = list()
    for pd in pacientes:
        pacientesVO.append({
            'id': pd[0],
            'name': pd[1],
            'sex': pd[2],
            'age': pd[3],
            'Chest_pain_type': pd[4],
            'BP': pd[5],
            'Cholesterol': pd[6],
            'FBS_over_120': pd[7],
            'EKG_results': pd[8],
            'Max_HR': pd[9],
            'Exercise_angina': pd[10],
            'ST_depression': pd[11],
            'Slope_of_ST': pd[12],
            'Number_of_vessels_fluro': pd[13],
            'Thallium': pd[14],
            'Heart_Disease': pd[15]
        })

    return make_response(
        jsonify(Pacientes(Pacientes=pacientesVO).dict()))


@server.app.post('/Pacientes')
@server.api.validate(body=Request(Paciente), resp=Response(HTTP_200=Paciente, HTTP_400=Erro,  HTTP_500=Erro), tags=['Pacientes'])
def postProduto():
    """
    Insere um Paciente da base de dados

    """
    try:

        body = request.context.body.dict()
        paciente = request.json

        # validar se o cara tem problema
        # Carregando modelo
        # C:\Projetos\Python\ProjetoPucX\Modelo\Modelo_treinado.pkl
        ml_path = 'Modelo\classificador.pkl'
        modelo = Model.carrega_modelo(ml_path)
        condicao = Model.preditor(modelo, paciente)
        if condicao == "Absence":
            condicao = "Ausencia"
        else:
            condicao = "Presença"

        # incluir o resultado no paciente
        # persistir o dado
        cursor = conn.cursor()
        sql = f"INSERT INTO Pacientes(Name, Sex, age, Chest_pain_type, BP, Cholesterol, FBS_over_120, EKG_results, Max_HR, Exercise_angina, ST_depression, Slope_of_ST, Number_of_vessels_fluro, Thallium, Heart_Disease) VALUES('{paciente['name']}', {paciente['sex']}, {paciente['age']}, {paciente['Chest_pain_type']}, {paciente['BP']}, {paciente['Cholesterol']}, {paciente['FBS_over_120']}, {paciente['EKG_results']}, {paciente['Max_HR']}, {paciente['Exercise_angina']}, {paciente['ST_depression']}, {paciente['Slope_of_ST']}, {paciente['Number_of_vessels_fluro']}, {paciente['Thallium']},'" + condicao + "')"
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        return body

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Houve um erro ao cadastrar o paciente").dict())), 500
