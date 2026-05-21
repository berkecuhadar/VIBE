from django import forms

class CharacterSuggestionForm(forms.Form):
    """
    Form interface for community members to submit character nominations.
    Styled with custom utility classes for a dark-themed Tailwind CSS UI layout.
    """
    name = forms.CharField(
        max_length=100, 
        label="Character Name", 
        widget=forms.TextInput(attrs={'class': 'w-full bg-gray-800 rounded p-2 text-white'})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full bg-gray-800 rounded p-2 text-white'}), 
        label="Reason for Suggestion"
    )
    image_url = forms.URLField(
        required=False, 
        label="Image URL (Optional)", 
        widget=forms.URLInput(attrs={'class': 'w-full bg-gray-800 rounded p-2 text-white'})
    )


class CodexSuggestionForm(forms.Form):
    """
    Form interface for community members to submit terminology or lore definitions.
    Features detailed hover/focus micro-interactions using Tailwind transitions.
    """
    term = forms.CharField(
        max_length=100, 
        label="Suggested Term", 
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-800 rounded p-2 text-white border border-gray-700 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition-all'
        })
    )
    definition = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full bg-gray-800 rounded p-2 text-white border border-gray-700 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition-all'
        }), 
        label="Definition & Context"
    )