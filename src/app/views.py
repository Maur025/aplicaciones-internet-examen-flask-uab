from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from .extensions import appbuilder
from .models import Server, Metric, AlertConfiguration, AlertHistory, MetricHistory


# @current_app.errorhandler(404)
# def page_not_found(e):
#    return (
#        render_template(
#            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
#        ),
#        404,
#    )


class ServerModelView(ModelView):
    datamodel = SQLAInterface(Server)
    label_columns = {'name': 'Nombre', 'host': 'Host', 'port': 'Puerto', 'created_at': 'Fecha de creación',
                     'updated_at': 'Fechaa de actualización'}

    list_columns = ['name', 'host', 'port', 'created_at', 'updated_at']

    add_columns = ['name', 'host', 'port']
    edit_columns = ['name', 'host', 'port']
    show_columns = ['name', 'host', 'port', 'created_at', 'updated_at']
    search_columns = ['name', 'host', 'port']

    search_exclude_columns = ['id']


class MetricModelView(ModelView):
    datamodel = SQLAInterface(Metric)
    label_columns = {'name': 'Nombre', 'code': 'Código', 'unit': 'Unidad', 'created_at': 'Fecha de creación',
                     'updated_at': 'Fechaa de actualización'}

    list_columns = ['name', 'code', 'unit', 'created_at', 'updated_at']

    add_columns = ['name', 'code', 'unit']
    edit_columns = ['name', 'code', 'unit']
    show_columns = ['name', 'code', 'unit', 'created_at', 'updated_at']
    search_columns = ['name', 'code', 'unit']

    search_exclude_columns = ['id']


class AlertConfigurationModelView(ModelView):
    datamodel = SQLAInterface(AlertConfiguration)

    label_columns = {'min_value': 'Valor minimo',
                     'max_value': 'Valor maximo',
                     'remain_value_min': 'alertar en (minutos)',
                     'created_at': 'Fecha de creación',
                     'updated_at': 'Fechaa de actualización'}

    list_columns = ['server', 'metric', 'min_value', 'max_value', 'remain_value_min', 'created_at', 'updated_at']

    add_columns = ['server', 'metric', 'min_value', 'max_value', 'remain_value_min']
    edit_columns = ['min_value', 'max_value', 'remain_value_min']
    show_columns = ['server', 'metric', 'min_value', 'max_value', 'remain_value_min', 'created_at', 'updated_at']
    search_columns = ['server', 'metric', 'min_value', 'max_value', 'remain_value_min']

    search_exclude_columns = ['id', 'metric_id', 'server_id']


class MetricHistoryModelView(ModelView):
    datamodel = SQLAInterface(MetricHistory)
    label_columns = {'metric': 'Metrica',
                     'value': 'Valor',
                     'unit': 'Unidad',
                     'created_at': 'Fecha de creación',
                     'updated_at': 'Fechaa de actualización'}

    list_columns = ['server', 'metric', 'value', 'unit', 'created_at', 'updated_at']

    add_columns = ['server', 'metric', 'value', 'unit']
    edit_columns = []
    show_columns = ['server', 'metric', 'value', 'unit', 'created_at', 'updated_at']
    search_columns = ['server', 'metric', 'value', 'unit']

    search_exclude_columns = ['id', 'server_id']


class AlertHistoryModelView(ModelView):
    datamodel = SQLAInterface(AlertHistory)
    label_columns = {'metric': 'Metrica',
                     'value': 'Valor',
                     'unit': 'Unidad',
                     'state': 'Estado',
                     'min_value': 'Valor minimo',
                     'max_value': 'Valor maximo',
                     'remain_value_min': 'alertar en (minutos)',
                     'created_at': 'Fecha de creación',
                     'updated_at': 'Fechaa de actualización'}

    list_columns = ['server', 'metric', 'value', 'unit', 'state', 'min_value', 'max_value', 'remain_value_min',
                    'created_at',
                    'updated_at']

    add_columns = ['server', 'metric', 'value', 'unit', 'state', 'min_value', 'max_value', 'remain_value_min']
    edit_columns = ['state']
    show_columns = ['server', 'metric', 'value', 'unit', 'state', 'min_value', 'max_value', 'remain_value_min',
                    'created_at', 'updated_at']
    search_columns = ['server', 'metric', 'value', 'unit', 'state', 'min_value', 'max_value', 'remain_value_min']

    search_exclude_columns = ['id', 'server_id']


appbuilder.add_view(ServerModelView, 'Servidores', icon='fa-server', category='Inicio',
                    category_icon='fa-home')

appbuilder.add_view(MetricModelView, 'Metricas', icon='fa-measure ', category='Inicio',
                    category_icon='fa-home')

appbuilder.add_view(AlertConfigurationModelView, 'Configuración de Alertas', icon='fa-box ', category='Inicio',
                    category_icon='fa-home')

appbuilder.add_view(AlertHistoryModelView, 'Historial de Alertas', icon='fa-box ', category='Inicio',
                    category_icon='fa-home')

appbuilder.add_view(MetricHistoryModelView, 'Historial de Metricas', icon='fa-box ', category='Inicio',
                    category_icon='fa-home')
