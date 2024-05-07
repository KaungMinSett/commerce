from django.contrib import admin

# Register your models here.

from .models import User, Auction_lists, Category, Watchlists, Bids, Comments

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "starting_bid", "created_by", "created_at", "is_active", 'get_category')
    list_filter = ("created_at", "is_active")
    search_fields = ("title", "created_by__username")
    ordering = ("created_at",)

    def get_category(self, obj):
        return ', '.join([category.name for category in obj.category.all()])
    
    get_category.short_description = 'category'


class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", 'bid', 'user', 'created_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('auction', 'comment', 'user')

admin.site.register(User)
admin.site.register(Auction_lists, AuctionAdmin)
admin.site.register(Category)
admin.site.register(Watchlists)
admin.site.register(Bids, BidAdmin)
admin.site.register(Comments, CommentAdmin)