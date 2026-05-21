import os
from django.db import models
from django.contrib.auth.models import User

class Character(models.Model):
    """
    Represents a core community character. Features dynamic, environment-configurable 
    tier labels and an automated threshold calculation algorithm inside the save() method.
    """
    # Dynamic labels fetched directly from the environment (.env)
    TIER_CHOICES = [
        ('S', os.environ.get('TIER_LABEL_S', 'S Tier')),
        ('A', os.environ.get('TIER_LABEL_A', 'A Tier')),
        ('B', os.environ.get('TIER_LABEL_B', 'B Tier')),
        ('C', os.environ.get('TIER_LABEL_C', 'C Tier')),
        ('D', os.environ.get('TIER_LABEL_D', 'D Tier')),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Character Name")
    score = models.IntegerField(default=0, verbose_name="Score Points")
    tier = models.CharField(max_length=1, choices=TIER_CHOICES, default='C', verbose_name="Tier Level")
    description = models.TextField(blank=True, verbose_name="Character Analysis")
    pic_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Image URL")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Retrieve total active community registered members
        total_users = User.objects.count()
        
        # Dynamic threshold coefficient (Ensures a minimum baseline value of 1)
        coefficient = max(1, total_users * 0.5) 

        # Dynamic Automated Tier Boundary Calculation
        if self.score >= coefficient:               # 50% or more of total user metrics
            self.tier = 'S'
        elif self.score >= (coefficient * 0.4):     # 20% or more of total user metrics
            self.tier = 'A'
        elif self.score >= (coefficient * 0.1):     # 5% or more of total user metrics
            self.tier = 'B'
        elif self.score >= 0:
            self.tier = 'C'
        else:
            self.tier = 'D'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_tier_display()}"

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"
        ordering = ['-score']


class Codex(models.Model):
    """
    Official knowledge base dictionary storing special terminology and definitions.
    """
    term = models.CharField(max_length=100, unique=True, verbose_name="Term")
    definition = models.TextField(verbose_name="Definition")

    def __str__(self):
        return self.term

    class Meta:
        verbose_name = "Term"
        verbose_name_plural = "Codices"


class Vote(models.Model):
    """
    Tracks community votes on characters. Supports both Upvotes (+1) and Downvotes (-1).
    Enforces a strict unique pair constraint to prevent voting inflation.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)  # 1 = Upvote, -1 = Downvote

    class Meta:
        unique_together = ('user', 'character')
        verbose_name = "User Vote"
        verbose_name_plural = "User Votes"


class CharacterSuggestion(models.Model):
    """
    Temporary table holding community-submitted character nominations pending admin integration.
    """
    name = models.CharField(max_length=100, verbose_name="Suggested Character Name")
    reason = models.TextField(verbose_name="Reason for Suggestion")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Image URL")
    suggested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Suggested By")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Suggested by: {self.suggested_by})"

    class Meta:
        verbose_name = "Character Suggestion"
        verbose_name_plural = "Character Suggestions"


class CodexSuggestion(models.Model):
    """
    Temporary table holding community-submitted codex definitions pending admin integration.
    """
    term = models.CharField(max_length=100, verbose_name="Suggested Term")
    definition = models.TextField(verbose_name="Suggested Definition")
    suggested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Suggested By")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.term} (Suggested by: {self.suggested_by})"

    class Meta:
        verbose_name = "Codex Suggestion"
        verbose_name_plural = "Codex Suggestions"