from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=400, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(default=0.0)
    tags = models.JSONField(default=list)
    def __str__(self): return f'Video:{self.pk}'
class Segment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='segments')
    start = models.FloatField()
    end = models.FloatField()
    transcript = models.TextField(blank=True)
    asr_lattice = models.JSONField(null=True, blank=True)
    asr_confidence = models.FloatField(null=True, blank=True)
class Embedding(models.Model):
    owner_type = models.CharField(max_length=16)
    owner_id = models.BigIntegerField()
    vector = models.BinaryField()
    dim = models.IntegerField(default=512)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [models.Index(fields=['owner_type','owner_id'])]
