class PrimarySecondaryRouter:
    """
    A router to control all database operations on models in the
    primary and secondary databases.
    """

    route_app_labels = {'app1', 'app2'}  # Adjust this to match your apps

    def db_for_read(self, model, **hints):
        """
        Attempts to read app1 and app2 models go to secondary.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'secondary'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write app1 and app2 models go to secondary.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'secondary'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the primary or secondary databases is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the app's models only appear in the relevant database.
        """
        if app_label in self.route_app_labels:
            return db == 'secondary'
        return db == 'default'
