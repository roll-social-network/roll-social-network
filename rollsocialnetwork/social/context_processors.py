"""
social context processors
"""

def social(request):
    """
    social context processor
    """
    if hasattr(request, "user_profile"):
        user_profile = request.user_profile
    else:
        user_profile = None
    return {
        "user_profile": user_profile,
    }
