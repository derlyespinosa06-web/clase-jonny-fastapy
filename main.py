from fastapi import FastAPI
from modelos.cliente import Client, Clientcreate, Clientt
from modelos.facture import Facture
from modelos.transaction import Transaction

app = FastAPI()

list_clients: list[Client] = []
facture: list[Facture] = []
transaction: list[Transaction] = []

#models

@app.get("/clientes")
async def Listar_clientes():
    return {"clients": list_clients}

@app.post("/clientes", response_model=Client)
async def create_clients(date_client: Clientcreate):

    Client_val = Clientt.model_validate(date_client.model_dump()) #el model dump convierte el objeto date_client en un diccionario para que pueda ser validado por el modelo Clientt

    Client_val.id = len(list_clients) + 1 #asignamos un id al cliente que se va a crear, el id es igual al tamaño de la lista de clientes + 1
    
    list_clients.append(Client_val) #agregamos el cliente a la lista de clientes
    return Client_val

#reto: crear un nuevo endponint y que me remote un solo cliente 
@app.get("/clientes/{id}", response_model=Client)
async def get_client(id: int):
    for client in list_clients:
        if client.id == id:
            return client
    return {"message": "client not found"}

@app.delete("/clientes/{id}", response_model=Client)
async def delete_client(id: int):
    for client in list_clients:
        if client.id == id:
            list_clients.remove(client) #remove elimina el cliente de la lista de clientes
            return {"message": "client deleted"}
    return {"message": "client not found"}

@app.put("/clientes/{id}", response_model=Client)
async def update_client(id: int, date_client: Clientcreate):
    for client in list_clients:
        if client.id == id:
            cli_val = Clientt.model_validate(date_client.model_dump()) #validamos el cliente que se va a actualizar
            client.name = cli_val.name
            client.age = cli_val.age
            client.description = cli_val.description
            return client


'''
Create models (transaction, facture,)
Facture/(id, date, client, totalvalue)
transaction(id, description, facture)
'''
# FACTURES ENDPOINTS
@app.get("/facturas")
async def list_factures():
    return {"factures": facture}

@app.post("/facturas", response_model=Facture)
async def create_facture(new_facture: Facture):
    new_facture.id = len(facture) + 1
    facture.append(new_facture)
    return new_facture

@app.get("/facturas/{id}", response_model=Facture)
async def get_facture(id: int):
    for f in facture:
        if f.id == id:
            return f
    return {"message": "facture not found"}

@app.delete("/facturas/{id}")
async def delete_facture(id: int):
    for f in facture:
        if f.id == id:
            facture.remove(f)
            return {"message": "facture deleted"}
    return {"message": "facture not found"}

# TRANSACTIONS ENDPOINTS
@app.get("/transacciones")
async def list_transactions():
    return {"transactions": transaction}

@app.post("/transacciones", response_model=Transaction)
async def create_transaction(new_transaction: Transaction):
    new_transaction.id = len(transaction) + 1
    transaction.append(new_transaction)
    return new_transaction

@app.get("/transacciones/{id}", response_model=Transaction)
async def get_transaction(id: int):
    for t in transaction:
        if t.id == id:
            return t
    return {"message": "transaction not found"}

@app.delete("/transacciones/{id}")
async def delete_transaction(id: int):
    for t in transaction:
        if t.id == id:
            transaction.remove(t)
            return {"message": "transaction deleted"}
    return {"message": "transaction not found"}
