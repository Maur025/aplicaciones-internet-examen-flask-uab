from ..extensions import db
from ..models import Server


def get_server_models(server_request_list) -> list[Server]:
    server_models = []

    for server_request in server_request_list:
        server_models.append(
            Server(name=server_request['name'], host=server_request['host'], port=server_request['port']))

    return server_models


def add_servers(server_request_list) -> None:
    server_to_create_list = get_server_models(server_request_list)
    server_to_create_names = [server.name for server in server_to_create_list]

    servers_registered_list = db.session.query(Server).where(Server.name.in_(server_to_create_names)).all()

    server_registered_names = {server.name for server in servers_registered_list}

    servers = [server for server in server_to_create_list if server.name not in server_registered_names]

    if not servers:
        print('No new servers to save')
        return

    try:
        db.session.add_all(servers)
        db.session.commit()

        print('Servers saved successfully')
    except Exception as ex:
        db.session.rollback()
        print(f'Error saving servers: {ex}')
