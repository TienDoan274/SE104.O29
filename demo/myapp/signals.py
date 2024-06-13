# myapp/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    # Chỉ tạo superuser khi chạy lệnh migrate
    if kwargs.get('app_config').name == 'myapp':
        # Tạo superuser nếu chưa tồn tại
        if not CustomUser.objects.filter(username='admin123').exists():
            # Tạo superuser trực tiếp mà không cần lệnh createsuperuser
            CustomUser.objects.create_superuser(
                username='admin123',
                email='',
                password='password123'
            )
