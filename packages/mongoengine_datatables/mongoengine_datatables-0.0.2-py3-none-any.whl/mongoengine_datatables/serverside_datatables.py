'''DataTables server-side for Flask-MongoEngine'''
import json
import re

from bson import json_util
from mongoengine.fields import (BooleanField, DecimalField,
                                EmbeddedDocumentField,
                                EmbeddedDocumentListField, FloatField,
                                IntField, ListField, LongField, ObjectIdField,
                                ReferenceField, SequenceField)
from mongoengine.queryset.visitor import Q, QCombination


class DataTables(object):
    def __init__(self, model, request_args, embed_search={}, q_obj=[],
                 custom_filter={}):
        '''
        :param model: The MongoEngine model
        :param request_args: Passed as Flask request.values.get('args')
        :param embed_search: For specific search in EmbeddedDocumentField
        :param q_obj: Additional search results in reference collection
        :param custom_filter: Additional filter
        '''

        self.model = model
        self.request_args = request_args
        self.columns = self.request_args.get('columns')
        self.search_string = self.request_args.get('search', {}).get('value')
        self.embed_search = embed_search
        self.q_obj = q_obj
        self.custom_filter = custom_filter

        _num_types = {IntField, BooleanField, DecimalField, FloatField,
                      LongField, SequenceField}
        _embed_types = {EmbeddedDocumentField, EmbeddedDocumentListField}

        self.field_type_dict = {}
        for k, v in model._fields.items():
            if type(v) in _num_types:
                self.field_type_dict[k] = 'number'
            elif type(v) in {ReferenceField}:
                self.field_type_dict[k] = 'reference'
            elif type(v) in {ObjectIdField}:
                self.field_type_dict[k] = 'objectID'
            elif type(v) in {ListField}:
                self.field_type_dict[k] = 'list'
            elif type(v) in _embed_types:
                self.field_type_dict[k] = 'embed'
            else:
                self.field_type_dict[k] = 'other'

    @property
    def total_records(self):
        if self.custom_filter:
            return str(self.model.objects(**self.custom_filter).count())
        return str(self.model.objects().count())

    @property
    def search_terms(self):
        return str(self.request_args.get("search")["value"]).split()

    @property
    def requested_columns(self):
        return [column["data"] for column in self.request_args.get("columns")]

    @property
    def draw(self):
        return self.request_args.get("draw")

    @property
    def start(self):
        return self.request_args.get("start")

    @property
    def limit(self):
        _length = self.request_args.get("length")
        if _length == -1:
            return None
        return _length

    @property
    def order_dir(self):
        ''' Return '' for 'asc' or '-' for 'desc' '''
        _dir = self.request_args.get("order")[0]["dir"]
        _MONGO_ORDER = {'asc': '', 'desc': '-'}
        return _MONGO_ORDER[_dir]

    @property
    def order_column(self):
        '''
        DataTables provides the index of the order column,
        but Mongo .sort wants its name.
        '''
        _order_col = self.request_args.get("order")[0]["column"]
        return self.requested_columns[_order_col]

    @property
    def get_search_query(self):
        _column_names = [d['data']
                         for d in self.columns if d['data']
                         in self.field_type_dict.keys()]
        queries = []
        for col in _column_names:
            _q = self.search_string
            if self.field_type_dict.get(col) == 'number':
                if _q.isdigit():
                    queries.append(Q(**{col + '__icontains': _q}))
            elif self.field_type_dict.get(col) == 'objectID':
                continue
            elif self.field_type_dict.get(col) == 'embed':
                if not self.embed_search:
                    continue
                for field in self.embed_search.get(col)['fields']:
                    _emb = f'{col}__{field}__icontains'
                    queries.append(Q(**{_emb: _q}))
            elif self.field_type_dict.get(col) == 'list':
                escaped = re.escape(_q)
                regexp = re.compile(f'.*{escaped}.*', re.IGNORECASE)
                queries.append(Q(**{col: regexp}))
            else:
                queries.append(Q(**{col + '__icontains': _q}))

        if self.q_obj:
            queries.append(self.q_obj)
        _search_query = QCombination(QCombination.OR, queries)
        if self.custom_filter:
            _search_query = (_search_query & Q(**self.custom_filter))
        return _search_query

    def results(self):
        _res = self.model.objects(self.get_search_query)
        _order_by = f'{self.order_dir}{self.order_column}'
        _results = _res.order_by(_order_by).skip(
            self.start).limit(self.limit).as_pymongo()

        # Fix 'ObjectId' is not JSON serializable
        data = json.loads(json_util.dumps(_results))
        return dict(data=data, count=_res.count())

    def get_rows(self):
        return {
            'recordsTotal': self.total_records,
            'recordsFiltered': self.results().get('count'),
            'draw': int(str(self.draw)),
            'data': self.results().get('data')
        }
