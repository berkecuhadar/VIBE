import os
import requests
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib import messages
from allauth.socialaccount.signals import pre_social_login
from allauth.exceptions import ImmediateHttpResponse

@receiver(pre_social_login)
def verify_discord_server_membership(sender, request, sociallogin, **kwargs):
    """
    Interceptors social authentication lifecycles. If the login provider is Discord,
    it queries the Discord REST API to enforce active membership inside a specific
    community server (Guild ID) configured via environment parameters.
    """
    if sociallogin.account.provider == 'discord':
        access_token = sociallogin.token.token
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            # Query the authenticated user's current guild layout from Discord API
            response = requests.get('https://discord.com/api/users/@me/guilds', headers=headers, timeout=10)
        except requests.RequestException:
            messages.error(request, "Authentication Failed: Unable to establish connection with Discord API backend.")
            raise ImmediateHttpResponse(redirect('home_page'))
        
        if response.status_code == 200:
            guilds = response.json()
            
            # Fetch target Guild ID dynamically from the environment configuration
            target_guild_id = os.environ.get('DISCORD_GUILD_ID', '')
            
            # Map out all unique IDs of guilds the user is currently associated with
            user_guild_ids = [guild['id'] for guild in guilds]
            
            # Authorization Gate check
            if target_guild_id not in user_guild_ids:
                messages.error(
                    request, 
                    "ACCESS DENIED: Authorization failed. You must be a registered member of the official community server."
                )
                # Short-circuit the Allauth pipeline immediately and boot the user back to the landing view
                raise ImmediateHttpResponse(redirect('home_page'))
        else:
            messages.error(request, "Authentication Error: Discord server validation handshake failed.")
            raise ImmediateHttpResponse(redirect('home_page'))