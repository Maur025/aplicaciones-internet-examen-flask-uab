from flask_appbuilder import ModelView, BaseView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from markdown import markdown

from .extensions import appbuilder, db
from .ia_integration import metrics_analyzer, enhanced_analytic_response
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


class ReportView(BaseView):
    route_base = '/reports'

    @expose('/total-alerts')
    def index(self):
        total_alerted_alerts = db.session.query(db.func.count(AlertHistory.id)).where(
            AlertHistory.state == 'ALERTED').scalar() or 0

        total_viewed_alerts = db.session.query(db.func.count(AlertHistory.id)).where(
            AlertHistory.state == 'VIEWED').scalar() or 0

        metrics_group_query = db.session.query(MetricHistory.metric.label('metric_name'),
                                               db.func.count(MetricHistory.id).label('total_count')).group_by(
            MetricHistory.metric).all()

        metrics_history_report = {row.metric_name: row.total_count for row in metrics_group_query}

        servers_history_string = self.get_resume_servers_as_string()
        metrics_analyzed = metrics_analyzer(servers_history_string)
        metrics_analyzed_html = markdown(metrics_analyzed)

        enhanced_analysis = enhanced_analytic_response(metrics_analyzed)

        print(enhanced_analysis)

        return self.render_template("reports.html", total_alerted_alerts=total_alerted_alerts,
                                    total_viewed_alerts=total_viewed_alerts,
                                    metrics_history_report=metrics_history_report,
                                    metrics_analyzed=enhanced_analysis, metrics_analyzed_html=metrics_analyzed_html)

    def get_resume_servers_as_string(self):
        servers = db.session.query(Server).all()

        servers_as_string = ''

        for server in servers:
            last_history = db.session.query(MetricHistory).where(MetricHistory.server_id == server.id).order_by(
                MetricHistory.created_at.desc()).limit(30).all()

            servers_as_string += f'''Servidor - {server.name} | {server.host} | {server.port}
            Ultimos 30 valores registrados:
            |fecha | metrica | valor | unidad|
            |------|---------|-------|-------|\n'''

            if len(last_history) < 1:
                servers_as_string += 'Sin valores registrados\n'
                continue

            for metric in last_history:
                servers_as_string += f'|{metric.created_at}|{metric.metric}|{metric.value}|{metric.unit}|\n'

            servers_as_string += '\n'

        # print(servers_as_string)
        return servers_as_string


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

appbuilder.add_view_no_menu(ReportView())

appbuilder.add_link('Total de alertas', href='/reports/total-alerts', icon='fa-chart-bar',
                    category='Reportes',
                    category_icon='fa-chart-bar')
