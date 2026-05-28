from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Listas en memoria con tipado estricto 
lista_clientes: list["Cliente"] = []
lista_facturas: list["Factura"] = []
lista_transacciones: list["Transaccion"] = []

# --- MODELOS 

class ClienteBase(BaseModel):
    name: str
    age: int
    description: str | None = None

class Cliente(ClienteBase):
    id: int | None = None

# Aquí está tu estructura exacta de la Factura: id, fecha, cliente, valortotal
class FacturaBase(BaseModel):
    fecha: str
    cliente_id: int
    valor_total: float

class Factura(FacturaBase):
    id: int | None = None

# Aquí está tu estructura de Transacción: id, descripcion, factura
class TransaccionBase(BaseModel):
    descripcion: str
    factura_id: int

class Transaccion(TransaccionBase):
    id: int | None = None


# --- ENDPOINTS CLIENTES ---
 # Aqui se mostrara una lista de clientes, cada cliente con su id, nombre, edad y descripción.
@app.get("/clientes")
async def listar_clientes():
    return {"clientes": lista_clientes}

3
@app.post("/clientes", response_model=Cliente)
async def create_clients(data_cliente: ClienteBase):

    #se agrega un nuevo cliente a la lista de clientes, validando los datos de entrada con el modelo ClienteBase y luego creando un nuevo objeto Cliente con un ID asignado.
    nuevo_cliente = Cliente.model_validate(data_cliente.model_dump())

    #cada cliente nuevo se le asigna un ID incremental basado en la longitud de la lista de clientes, asegurando que cada cliente tenga un ID.
    nuevo_cliente.id = len(lista_clientes) + 1

    #se agrega un cliente a la lista
    lista_clientes.append(nuevo_cliente)
    return nuevo_cliente

#reto crear un endpoint y que me remote un solo cliente
@app.get("/clientes/{id}", response_model=Cliente)
async def get_client(id: int):
    for client in lista_clientes:
        if client.id == id:
            return client
    return {"message": "cliente no encontrado"}

#reto crear un endpoint para eliminar un cliente
@app.delete("/clientes/{id}")
async def delete_client(id: int):
    for client in lista_clientes:
        if client.id == id:
            lista_clientes.remove(client)
            return {"message": "cliente eliminado"}
    return {"message": "cliente no encontrado"}

#reto crear un endpoint para actualizar un cliente
@app.put("/clientes/{id}", response_model=Cliente)
async def update_cliente(id: int, data_cliente: ClienteBase):
    for cliente in lista_clientes:
        if cliente.id == id:
            # 1. Validamos y volcamos los datos entrantes en un diccionario o nuevo objeto
            datos_nuevos = data_cliente.model_dump()
            
            # 2. Actualizamos los atributos del cliente existente en la lista
            cliente.name = datos_nuevos["name"]
            cliente.age = datos_nuevos["age"]
            cliente.description = datos_nuevos["description"]
            
            return cliente
        return {"message": "cliente no encontrado"}


 # --- ENDPOINTS FACTURAS ---
@app.get("/facturas")
async def listar_facturas():
     return {"facturas": lista_facturas}

@app.post("/facturas", response_model=Factura)
async def crear_factura(data_f: FacturaBase):
     # Validamos y creamos la factura con su ID correspondiente
     nueva_f = Factura.model_validate(data_f.model_dump())
     nueva_f.id = len(lista_facturas) + 1
     lista_facturas.append(nueva_f)
     return nueva_f

@app.get("/facturas/{id}", response_model=Factura)
async def get_factura(id: int):
     for f in lista_facturas:
         if f.id == id:
             return f
     return {"message": "factura not found"}


 # --- ENDPOINTS TRANSACCIONES ---

@app.get("/transacciones")
async def listar_transacciones():
     return {"transactions": lista_transacciones}

@app.post("/transacciones", response_model=Transaccion)
async def crear_transaccion(data_t: TransaccionBase):
     # Validamos y creamos la transacción relacionándola con la factura
     nueva_t = Transaccion.model_validate(data_t.model_dump())
     nueva_t.id = len(lista_transacciones) + 1
     lista_transacciones.append(nueva_t)
     return nueva_t

@app.get("/transacciones/{id}", response_model=Transaccion)
async def get_transaction(id: int):
     for t in lista_transacciones:
         if t.id == id:
             return t
     return {"message": "transaction not found"}