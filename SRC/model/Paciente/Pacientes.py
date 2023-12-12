from pydantic import BaseModel
from SRC.model.Paciente.Paciente import Paciente

class Pacientes(BaseModel): 
    Pacientes:list[Paciente] 