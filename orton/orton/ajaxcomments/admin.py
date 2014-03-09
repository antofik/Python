import reversion
import admin_site as admin
from models import *


class CommentAdmin(reversion.VersionAdmin):
    pass

admin.site.register(AjaxComment, CommentAdmin)