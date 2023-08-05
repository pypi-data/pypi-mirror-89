# -*- python -*-
'''
djfim.base
'''

import json
import logging


from django.apps import apps


from djfim.settings import app_settings


def _get_model_class(app_name, app_label):
    mod = apps.get_app_config(app_name).get_model(app_label)
    return mod


class BasePolicy(object):
    '''
    base-class of policy provider
    '''

    def increment(self, val):
        '''
        increase the value of the release number

        :param val: (int)

        :return: int
        '''
        raise NotImplementedError('sub-class must implement this')


class PLUS_ONE(BasePolicy):
    '''
    increment release number by one(1)
    '''
    def increment(self, val):
        return (val + 1)


class PLUS_TEN(BasePolicy):
    '''
    increment release number by ten(10)
    '''
    def increment(self, val):
        return (val + 10)


class Map(object):
    '''
    data model mapping interface
    '''

    FK_BLACKLIST = (
        'added_by',
        'created_by',
        'last_modified_by',
        'modified_by',
        'updated_by',
    )

    def getMappedModel(self):
        target = _get_model_class(self.app_name, self.app_label)
        return target

    def checkFKMap(self, field, local, upstream, local_map, release):
        '''
        :param field: (Field/ForeignKey)
        :param local: (Model)
        :param upstream: (Model)
        :param local_map: (dict/list)
        :param release: (int)
        '''
        field_name = field.attname
        if self.isBlacklistFK(field_name):
            return None

        target_model = field.related_model
        local_val = getattr(local, field_name)
        upstream_val = getattr(upstream, field_name)
        local_target_entry = self.__class__.objects.get(
            app_name=target_model._meta.app_label,
            app_label=target_model._meta.model_name,
            local_pk=local_val,
            upstream_pk=upstream_val,
            release=release,
        )
        local_target_rec = local_target_entry.find_local_mapped_entry()
        if local_target_rec:
            return None
        else:
            raise ValueError('local mapped target is missing')

    def isBlacklistFK(self, field_name):
        '''
        :param field_name: (string)

        :return: (boolean)
        '''
        val = (field_name in self.FK_BLACKLIST)
        return val

    def getFKList(self, model_cls):
        '''
        :param model_cls: (`Model`)

        :return: symbolic names of the foreign key fields (list of string)
        '''
        fk_list = list()
        from django.db.models import ForeignKey
        field_list = model_cls._meta.fields
        for field in field_list:
            if isinstance(field, ForeignKey):
                fk_list.append(field.attname)
        return fk_list

    def getTargetContextKey(self, target, up_id=None, **kwargs):
        '''
        :param target: (`Model`)
        :param up_id: user specified pk value (integer0

        :return: (string)

        DEV-NOTE: the algorithm/schema of the target record context key defined here may be interchangeable.
        DEV-NOTE: another way is to inject the policy object when `Actuator` object performs related actions.
        '''
        SCHEMA = 'up-{app}-{mod}-{up_id}'
        fmt_data = {
            'app': self.app_name,
            'mod': self.app_label,
            'up_id': self.upstream_pk,
        }
        if target is not None:
            fmt_data = {
                'app': target._meta.app_label,
                'mod': target._meta.model_name,
                'up_id': up_id,
            }
        ret = SCHEMA.format(**fmt_data)
        return ret

    def compareRecord(self, local_rec, upstream_rec, **kwargs):
        '''
        :param local_rec: (`Model` instance)
        :param : ()
        TODO: not fully implemented yet
        compareRecord(self.find_local_mapped_entry(), self.getMappedModel()(**self.data))
        '''
        cmp_ret = dict()

        MODEL = self.getMappedModel()
        field_lst = MODEL._meta.fields

        for field in field_lst:
            field_name = field.attname
            if isinstance(field, models.ForeignKey):
                try:
                    fk_cmp = self.checkFKMap(field, local_rec, upstream_rec)
                    if fk_cmp is None:
                        cmp_ret[field_name] = True
                    else:
                        cmp_ret[field_name] = fk_cmp
                except ValueError:
                    cmp_ret[field_name] = False
                    # NOTE: may need to deal with the missing record, or log this exception
                    #raise
            else:
                cmp_ret[field_name] = getattr(loca_rec, field_name) == getattr(upstream_rec, field_name)
        return cmp_ret

    class Meta:
        abstract = True


class RecordException(Exception):
    def __init__(self, *args, **kwargs):
        super(RecordException, self).__init__(*args, **kwargs)


class Actuator(object):
    LOG_NAME = 'djfim.base'

    MSG_EMPTY_DATA = 'no data read from file'
    MSG_INVALID_RELEASE = 'invalid release'
    MSG_INVALID_ARG = 'invalid argument datatype'

    DEFAULT_INCREMENT = 'PLUS_ONE'

    def __init__(self):
        self.settings = app_settings

    def getLogger(self):
        logger = logging.getLogger(self.LOG_NAME)
        return logger

    def getModelCls(self):
        '''
        "MODEL": { "app_name":"djfim", "app_label":"FURecord" }
        '''
        return  _get_model_class(self.settings.MODEL['app_name'], self.settings.MODEL['app_label'])

    def prepareModelData(self, item, release):
        '''
        :param item: (dict)
        :param release: (int)

        :return: dict
        '''
        data = dict()
        data['release'] = release
        data['upstream_pk'] = item.get('pk')
        app_ns = item.get('model').rsplit('.', 1)
        data['app_name'] = app_ns[0]
        data['app_label'] = app_ns[1]
        data['data'] = item.get('fields')
        data['local_pk'] = None
        return data

    def loadFromFile(self, f, **kwargs):
        '''
        :param f: (file-like object)

        :return: int
        '''
        item_count = 0
        data = json.load(f)
        if len(data):
            current_rel = self.getLatestRelease(**kwargs)
            new_rel = self.incrementRelease(current_rel, **kwargs)
            MODEL = self.getModelCls()
            for item in data:
                item_data = self.prepareModelData(item, release=new_rel)
                new_rec = MODEL(**item_data)
                new_rec.save()
                #
                item_count += 1
        else:
            raise ValueError(self.MSG_EMPTY_DATA)
        return item_count

    def getReleaseData(self, release, **kwargs):
        '''
        :param release: (int)

        :return: `QuerySet`
        '''
        rel_entries = self.getModelCls().objects.filter(release=release).order_by('id')
        return rel_entries

    def getLatestRelease(self, **kwargs):
        '''
        return the latest release number

        :note: zero will be returned if there is no data exist

        :return: int
        '''
        release_set = set(self.getModelCls().objects.values_list('release', flat=True))
        val = 0
        if len(release_set):
            val = max(release_set)
        return val

    def incrementRelease(self, current_rel, alt_release=None, **kwargs):
        '''
        :param current_rel: (int)

        :param alt_release: alternative release number to be used (int)

        :return: int
        '''
        if isinstance(alt_release, (int, long)):
            return alt_release

        pol_cls = getattr(
            self.settings,
            'RELEASE_INCREMENT_POLICY',
            self.DEFAULT_INCREMENT
        )
        pol_obj = globals()[pol_cls]()
        return pol_obj.increment(current_rel)

    def applyRelease(self, release=None, **kwargs):
        '''
        apply the specified release

        :param release: (None or int)
        '''
        release_to_apply = release if release is not None else self.getLatestRelease(**kwargs)
        items = self.getReleaseData(release_to_apply, **kwargs)
        #-todo: try to get previous release, and do update instead of create;
        previous_release = self.getRekaseData()

        item_count = items.count()
        if item_count > 0:
            self.merge(items, **kwargs)
        else:
            raise ValueError(self.MSG_INVALID_RELEASE)
        pass

    def merge(self, dataset, **kwargs):
        merge_stats = dict()
        local_fk_mapping = dict() #list()

        for item in dataset:
            self.createRecord(item, relContext=local_fk_mapping, **kwargs)
            pass  #-end-for-item-in-dataset
        return merge_stats

    def createRecord(self, item, relContext=None, **kwargs):
        '''
        :param relContext: foreign key context of the current working release (dict)
        '''
        assert isinstance(relContext, dict), self.MSG_INVALID_ARG
        # TODO: try to get previous release/local data
        #item.find_local_mapped_entry()

        local_rec = item.create_local_record(context=relContext, **kwargs)
