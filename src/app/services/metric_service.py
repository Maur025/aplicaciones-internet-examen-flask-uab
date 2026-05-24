from ..extensions import db
from ..models import MetricHistory, Server


def get_server_models(metric_request_list, servers_map) -> list[MetricHistory]:
    metrics_models = []

    for metric_request in metric_request_list:
        metrics_models.append(
            MetricHistory(server_id=servers_map[metric_request['server']], metric=metric_request['metric'],
                          value=metric_request['value'], unit=metric_request['unit']))

    return metrics_models


def add_metrics(metric_request_list) -> None:
    servers = db.session.query(Server).all()
    server_key_ids = {server.name: server.id for server in servers}

    metrics_to_create = get_server_models(metric_request_list, servers_map=server_key_ids)

    if not metrics_to_create:
        return

    try:
        db.session.add_all(metrics_to_create)
        db.session.commit()

        print('Metrics saving successfully')
    except Exception as ex:
        db.session.rollback()
        print(f'Error saving metrics: {ex}')

    print()
