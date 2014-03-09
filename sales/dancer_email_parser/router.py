__author__ = 'anton'

class router:
    parserScheme = 'parser'
    parserApp = 'dancer_email_parser'

    def db_for_read(self, model, **hint):
        if model._meta.app_label == self.parserApp:
            return self.parserScheme
        return None

    def db_for_write(self, model, **hint):
        if model._meta.app_label == self.parserApp:
            return self.parserScheme
        return None

    def allow_relation(self, obj1, obj2, **hint):
        if obj1._meta.app_label == self.parserApp:
            return self.parserScheme
        return None

    def allow_syncdb(self, db, model):
        if db==self.parserScheme:
            return model._meta.app_label==self.parserApp
        elif model._meta.app_label==self.parserApp:
            return False
        return None
