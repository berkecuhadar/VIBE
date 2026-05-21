from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Character, Codex, Vote, CharacterSuggestion, CodexSuggestion
from .forms import CharacterSuggestionForm, CodexSuggestionForm

def home_page(request):
    """
    Traffic Controller: Renders the secure landing/login gate if unauthenticated,
    otherwise fetches and displays the live ranking leaderboard for community members.
    Ordered primarily by accumulated score points, then by creation date.
    """
    if not request.user.is_authenticated:
        return render(request, 'vibe/login.html')
    
    # Highest scores float to the top; ties broken by the newest entries first
    characters = Character.objects.all().order_by('-score', '-created_at')
    return render(request, 'vibe/home_page.html', {'characters': characters})


@login_required
def codex_page(request):
    """
    Knowledge Base: Houses the official terminology, dictionary acronyms, 
    and community jargon meanings.
    """
    terms = Codex.objects.all().order_by('term')
    return render(request, 'vibe/codex_page.html', {'terms': terms})


@login_required
def suggest_character(request):
    """
    Community Hub: Interface enabling active users to submit custom character 
    nominations to the staging pipeline.
    """
    if request.method == 'POST':
        form = CharacterSuggestionForm(request.POST)
        if form.is_valid():
            CharacterSuggestion.objects.create(
                name=form.cleaned_data['name'],
                reason=form.cleaned_data['reason'],
                image_url=form.cleaned_data['image_url'],
                suggested_by=request.user
            )
            messages.success(request, 'Character suggestion has been successfully submitted for administrative review.')
            return redirect('home_page')
    else:
        form = CharacterSuggestionForm()
    return render(request, 'vibe/suggest_character.html', {'form': form})


@login_required
def suggest_codex(request):
    """
    Glossary Contributions: Interface enabling active users to submit vocabulary 
    or terminology updates to the master Codex.
    """
    if request.method == 'POST':
        form = CodexSuggestionForm(request.POST)
        if form.is_valid():
            CodexSuggestion.objects.create(
                term=form.cleaned_data['term'],
                definition=form.cleaned_data['definition'],
                suggested_by=request.user
            )
            messages.success(request, 'Codex term definition has been successfully logged for administrative review.')
            return redirect('codex_page')
    else:
        form = CodexSuggestionForm()
    return render(request, 'vibe/suggest_codex.html', {'form': form})


@login_required
def cast_vote(request, character_id, vote_type):
    """
    Anti-Inflation Voting Protocol: Guards database from duplicated voting spam.
    Enforces a strict policy where one user maps to exactly one state per character (+1 or -1).
    Swapping sides recalculates the delta mathematically by a multiplier of 2.
    """
    character = get_object_or_404(Character, id=character_id)
    target_value = 1 if vote_type == 'up' else -1
    
    # Locate existing ledger entry or spin up a new ledger slot for this specific pair
    vote_record, created = Vote.objects.get_or_create(user=request.user, character=character)
    
    if created:
        # First-time voting interaction for this character
        vote_record.value = target_value
        vote_record.save()
        character.score += target_value
        character.save()
        messages.success(request, 'Your vote has been recorded successfully.')
        
    elif vote_record.value != target_value:
        # User is shifting alignment (e.g., swapping from Downvote to Upvote or vice versa)
        # The scoring gap requires an offset calculation of exactly 2 points
        character.score += (target_value * 2) 
        vote_record.value = target_value
        vote_record.save()
        character.save()
        messages.success(request, 'Your vote adjustment has been processed.')
        
    # If vote_record.value == target_value, pass cleanly (Duplicated clicks are ignored safely)
        
    return redirect('home_page')