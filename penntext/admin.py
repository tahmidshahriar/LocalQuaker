from django.contrib import admin
from penntext.models import Subject, Sell, UserProfile, TicketSell, HouseholdSell, Term, SubletsSell, Other
from django import forms

admin.site.register(Subject)
admin.site.register(Sell)
admin.site.register(TicketSell)
admin.site.register(UserProfile)
admin.site.register(HouseholdSell)
admin.site.register(SubletsSell)
admin.site.register(Other)
admin.site.register(Term)
