from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Character, Codex, Vote, CharacterSuggestion, CodexSuggestion

# --- Standard Model Registrations ---

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    # 'get_tier_display' used dynamically to show .env custom labels in the list view
    list_display = ('name', 'get_tier_label', 'score', 'created_at')
    list_filter = ('tier', 'created_at')
    search_fields = ('name', 'description')

    @admin.display(description='Dynamic Tier Label', ordering='tier')
    def get_tier_label(self, obj):
        """
        Fetches the human-readable label from TIER_CHOICES which is driven by .env config.
        """
        return obj.get_tier_display()


@admin.register(Codex)
class CodexAdmin(admin.ModelAdmin):
    list_display = ('term',)
    search_fields = ('term', 'definition')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'character', 'value')
    list_filter = ('value',)
    search_fields = ('user__username', 'character__name')


# --- Smart Approval Panels for Community Suggestions ---

@admin.register(CharacterSuggestion)
class CharacterSuggestionAdmin(admin.ModelAdmin):
    """
    Admin panel extension that allows administrators to review community-submitted 
    character suggestions and batch-approve them into the core system.
    """
    list_display = ('name', 'suggested_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'suggested_by__username')
    actions = ['approve_and_integrate_characters']

    @admin.action(description=_("Approve and migrate selected suggestions to Core Characters"))
    def approve_and_integrate_characters(self, request, queryset):
        added_count = 0
        
        for oneri in queryset:
            Character.objects.create(
                name=oneri.name,
                description=f"{oneri.reason} (Suggested by: {oneri.suggested_by.username if oneri.suggested_by else 'Anonymous'})",
                pic_url=oneri.image_url,
                tier='C',  # Default baseline tier assignment
                score=0
            )
            oneri.delete()  # Clean up the pending tracking queue after migration
            added_count += 1
            
        self.message_user(
            request, 
            f"Successfully approved and integrated {added_count} characters into the core ecosystem."
        )


@admin.register(CodexSuggestion)
class CodexSuggestionAdmin(admin.ModelAdmin):
    """
    Admin panel extension that allows administrators to review community-submitted 
    codex definitions and merge them safely into the master Codex list.
    """
    list_display = ('term', 'suggested_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('term', 'suggested_by__username')
    actions = ['approve_and_integrate_codex']

    @admin.action(description=_("Approve and migrate selected suggestions to Master Codex"))
    def approve_and_integrate_codex(self, request, queryset):
        added_count = 0
        
        for oneri in queryset:
            Codex.objects.get_or_create(
                term=oneri.term,
                defaults={
                    'definition': f"{oneri.definition} (Contributed by: {oneri.suggested_by.username if oneri.suggested_by else 'Anonymous'})"
                }
            )
            oneri.delete()
            added_count += 1
            
        self.message_user(
            request, 
            f"Successfully merged {added_count} terms into the Master Codex."
        )