from django.contrib import admin

# Register your models here.
from .models import Users, Games, GameCollection, Comments, Posts, Community, Game_news, FAQ

admin.site.register(Users)
admin.site.register(Games)
admin.site.register(GameCollection)
admin.site.register(Comments)
admin.site.register(Posts)
admin.site.register(Community)
admin.site.register(Game_news)
admin.site.register(FAQ)
