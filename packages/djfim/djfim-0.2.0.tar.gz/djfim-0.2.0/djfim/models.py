# -*- python -*-
"""
djfim.models
"""

from django.db import models

from django.contrib.postgres.fields import JSONField


from djfim.base import Map, RecordException


class FURecord(Map, models.Model):
    """
    fixture update record

    NOTE: this model class is PostgreSQL-specific
    """

    class Meta:
        #abstract = False
        abstract = True

    ## internal use
    release = models.PositiveIntegerField()
    ## Django framework convention
    app_name = models.CharField(max_length=128)
    ## Django framework convention
    app_label = models.CharField(max_length=128)
    ## data store
    data = JSONField() #models.TextField(null=True)
    ## ID mapping, upstream
    upstream_pk = models.IntegerField()
    ## ID mapping, local
    local_pk = models.IntegerField(null=True)

    def find_local_mapped_entry(self):
        MODEL = self.getMappedModel()
        linked_rec = None
        try:
            if self.local_pk is None:
                raise ValueError('no local mapping saved')
            linked_rec = MODEL.objects.get(id=self.local_pk)
        except (MODEL.DoesNotExist, MODEL.MultipleObjectsReturned) as e:
            # NOTE: may need to handle the NotFound exception explicitly
            raise RecordException(e, self)
            pass
        return linked_rec

    def create_local_record(self, context, **kwargs):
        '''
        NOTE: this method may throw exception if DB constraint is violated.

        :param context: this dictionary will be updated within this method (dict)

        :return: `Model` instance
        '''
        MODEL = self.getMappedModel()
        fk_lst = self.getFKList(MODEL)
        local_remap = self.extract_fk_map(fk_lst, context, **kwargs)
        record = MODEL(
            **(
                self.patch_upstream_data(
                    self.data,
                    local_map=local_remap
                )
            )
        )
        #try:
        record.save()
        # post_save: a) update working context;
        new_rec_key = self.getTargetContextKey(MODEL, self.upstream_pk)
        context[new_rec_key] = record.id
        #except MODEL.ConstraintError as e:
        #    raise RecordException(e, self)
        # post_save: b) save the map;
        self.local_pk = record.id
        self.save(update_fields=['local_pk',])
        return record

    def extract_fk_map(self, fk_list, context, **kwargs):
        '''
        :param fk_list: (list of string)
        :param context: (dict)

        :return: (dict)
        '''
        ret = dict()
        for item in fk_list:
            if self.isBlacklistFK(item):
                #ret[item] = bl_fk_value
                continue
            else:
                #-todo: need to construct the unified key in order to get the correct value;
                up_fk_id = self.data[item]
                ctx_key = self.getTargetContextkey(item, up_fk_id, **kwargs)
                ret[item] = context[ctx_key]
        return ret

    def patch_upstream_data(self, upstream_data, local_map):
        '''
        :param upstream_data: (dict)
        :param local_map: (dict)

        :return: (dict)
        '''
        merged_data = dict()
        merged_data.update(upstream_data)
        merged_data.update(local_map)
        return merged_data
