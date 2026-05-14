from fastapi import FastAPI
from modelos.cliente import Client, Clientcreate, Clientt

app = FastAPI()

list_clients: list[Client] = []

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
    return {"message": "client not found"}
#uv pip list para ver las dependencias