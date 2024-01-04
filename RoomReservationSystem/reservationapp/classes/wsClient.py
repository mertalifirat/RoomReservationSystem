import asyncio
import websockets
import json
import pdb

class Client():
    uri = "ws://127.0.0.1:1422"
    def __init__(self):
        self.server_shut_down = False
        self.websocket = None
        self.uri = "ws://127.0.0.1:1422"
        
    async def connect(self):
        self.websocket = websockets.connect(self.uri)
    

    async def make_request(self, request):

        request_type = request["command"].upper()
        if request_type == "CREATE_USER":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            username = await self.websocket.recv(1024).decode("utf8")
            if (
                username
            ):  # Server returned id of created user which means user creation is successful.
                print(f"User({username}) created successfully.")

        elif request_type == "LOGIN":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            pdb.set_trace()
            return (await self.websocket.recv(4096).decode("utf8"))

        elif request_type == "LIST_ORGANIZATIONS": 
                
            await self.websocket.send(str.encode(json.dumps(request)))
            pdb.set_trace()
            return (await self.websocket.recv(4096).decode("utf8"))

        elif request_type == "ATTACH_ORGANIZATION":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(4096).decode("utf8"))

        elif request_type == "DETACH_ORGANIZATION":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(4096).decode("utf8"))    

        elif request_type == "LIST_ROOMS": #List rooms in attached organization
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(4096).decode("utf8"))

        elif request_type == "ADD_ROOM": #Working hours are in format: %H:%M-%H:%M
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(4096).decode("utf8"))

        elif request_type == "ACCESS":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(4096).decode("utf8"))

        elif request_type == "DELETE_ROOM":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(1024).decode("utf8"))

        elif request_type == "LIST_RESERVED_EVENTS":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(4096).decode("utf8"))

        elif request_type == "RESERVE": #Start format is: %Y-%m-%d-%H:%M
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(1024).decode("utf8"))

        elif request_type == "DELETE_RESERVATION": #Start and end are in format: %Y-%m-%d-%H:%M
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(1024).decode("utf8"))
        elif request_type == "READ_EVENT":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(4096).decode("utf8"))    
        elif request_type == "UPDATE_EVENT":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(1024).decode("utf8"))
        elif request_type == "DELETE_EVENT":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(1024).decode("utf8"))                   
        elif request_type == "LOGOUT":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(1024).decode("utf8"))

        elif request_type == "EXIT":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv(1024).decode("utf8"))
            self.server_shut_down = True          
        elif request_type == "SAVE":
            
            await self.websocket.send(str.encode(json.dumps(request)))
            return(await self.websocket.recv().decode("utf8"))
                
        else:
            return("Invalid command")

if __name__ == "__main__":
    
    
    client = Client()
    client.connect()
