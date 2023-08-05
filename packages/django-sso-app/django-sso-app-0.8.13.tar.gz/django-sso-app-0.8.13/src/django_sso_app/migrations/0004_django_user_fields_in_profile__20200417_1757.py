# Generated by Django 2.2.11 on 2020-04-17 15:57

from django.db import migrations, models
import django_sso_app.core.apps.profiles.models

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Profile = apps.get_model("django_sso_app", "Profile")
    db_alias = schema_editor.connection.alias
    for p in Profile.objects.using(db_alias):
        p.django_user_email = p.user.email
        p.django_user_username = p.user.username
        p.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('django_sso_app', '0003_emailaddress'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', django_sso_app.core.apps.profiles.models.SsoIdPKManager()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='django_user_email',
            field=models.EmailField(blank=True, editable=False, max_length=254, null=True, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='profile',
            name='django_user_username',
            field=models.CharField(blank=True, editable=False, max_length=150, null=True, verbose_name='user username'),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
