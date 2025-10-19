# covers/serializers.py
from rest_framework import serializers
from .models import Cover

class CoverSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Cover
        fields = ['id', 'template_style', 'image_path', 'image_url', 
                  'is_selected', 'created_at', 'generation_params']
        read_only_fields = ['id', 'created_at']
    
    def get_image_url(self, obj):
        from django.conf import settings
        # Check if the image file exists on disk
        import os
        from pathlib import Path
        
        full_path = Path(settings.MEDIA_ROOT) / obj.image_path
        if not os.path.isfile(full_path):
            print(f"WARNING: Image file does not exist: {full_path}")
            # Return a fallback image
            return f"{settings.MEDIA_URL}covers/fallback.png"
        
        return f"{settings.MEDIA_URL}{obj.image_path}"
