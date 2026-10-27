import secrets
from django.db import migrations, models

SHORT_CODE_CHARACTERS = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz"


def generate_short_code(length=6):
    return "".join(secrets.choice(SHORT_CODE_CHARACTERS) for _ in range(length))


def populate_short_codes(apps, schema_editor):
    Grupo = apps.get_model("core", "Grupo")
    used_codes = set(
        Grupo.objects.exclude(codigo_curto__isnull=True)
        .exclude(codigo_curto="")
        .values_list("codigo_curto", flat=True)
    )

    for grupo in Grupo.objects.filter(models.Q(codigo_curto__isnull=True) | models.Q(codigo_curto="")):
        while True:
            code = generate_short_code()
            if code not in used_codes:
                used_codes.add(code)
                grupo.codigo_curto = code
                grupo.encurtador_url = f"/c/{code}"
                grupo.save(update_fields=["codigo_curto", "encurtador_url"])
                break


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_grupo_encurtador_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='codigo_curto',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True, unique=True, verbose_name='Código Curto'),
        ),
        migrations.RunPython(populate_short_codes, reverse_code=migrations.RunPython.noop),
    ]
