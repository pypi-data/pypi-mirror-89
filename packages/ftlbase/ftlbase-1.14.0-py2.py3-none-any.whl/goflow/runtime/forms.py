from django.urls import reverse_lazy

from goflow.apptools.widgets import GoFlowColumn
from goflow.runtime.models import WorkItem, ProcessInstance
from table import Table
from table.columns import DatetimeColumn, Column


class ProcessWorkItemTable(Table):
    # id = Column(field='instance.pk')
    date = DatetimeColumn(field='date')
    user = Column(field='user')
    descricao = Column(header='Descrição', field='instance.content_object')
    activity = Column(field='activity')
    priority = Column(field='priority')
    status = Column(field='status')

    class Meta:
        model = WorkItem
        # ajax = True
        # sort = [(0, 'asc'), ]
        std_button = False
        search = False
        pagination = False
        totals = False
        info = False
        std_button_create = {'text': 'Incluir novo atendimento', 'icon': 'fa fa-plus-square fa-fw',
                             'href': reverse_lazy('atendimentoAdd'),
                             "className": 'btn btn-primary btn-sm', }


class ProcessesInstanceTable(Table):
    id = Column(header='#', field='pk')
    process = Column(header='Processo', field='subject')
    descricao = Column(header='Descrição', field='content_object')
    status = Column(header='Status', field='status')
    activity = Column(header='Atividade', field='activity')
    status2 = Column(header='Status Ativ', field='activity_status')
    priority = Column(header='Prioridade', field='priority')
    user = Column(field='user')  # OU É user_name??????????????????????
    creationTime = DatetimeColumn(field='creationTime')
    action = GoFlowColumn(header='Ação', field='instance')

    class Meta:
        model = ProcessInstance
        # ajax = True
        # sort = [(0, 'asc'), ]
        # std_button = False
        std_button_create = False