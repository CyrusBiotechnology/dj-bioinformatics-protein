from __future__ import absolute_import

from django.contrib import admin

from .models import FASTA


class FASTAAdmin(admin.ModelAdmin):

    search_fields = [
        'description',
        'sequence',
        'hash'
    ]

    readonly_fields = (
        'hash',
    )

admin.site.register(FASTA, FASTAAdmin)
