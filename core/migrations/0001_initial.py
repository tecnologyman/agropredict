# Generated for AgroPredict Styled MVP
from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('Arica y Parinacota', 'Arica y Parinacota'), ('Tarapacá', 'Tarapacá'), ('Antofagasta', 'Antofagasta'), ('Atacama', 'Atacama'), ('Coquimbo', 'Coquimbo'), ('Valparaíso', 'Valparaíso'), ('Metropolitana', 'Metropolitana'), ('O’Higgins', 'O’Higgins'), ('Maule', 'Maule'), ('Ñuble', 'Ñuble'), ('Biobío', 'Biobío'), ('La Araucanía', 'La Araucanía'), ('Los Ríos', 'Los Ríos'), ('Los Lagos', 'Los Lagos'), ('Aysén', 'Aysén'), ('Magallanes', 'Magallanes')], max_length=40)),
                ('arbol_frutal', models.CharField(choices=[('manzana', 'Manzana'), ('cereza', 'Cereza')], default='manzana', max_length=16)),
                ('superficie_ha', models.FloatField()),
                ('temp_prom_anual_c', models.FloatField()),
                ('precip_anual_mm', models.FloatField()),
                ('radiacion_anual_wm2', models.FloatField()),
                ('produccion_esperada_t', models.FloatField()),
                ('proyeccion_json', models.TextField(help_text='JSON de 5 periodos')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-creado']},
        ),
    ]
