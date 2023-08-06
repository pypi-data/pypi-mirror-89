from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EntitySnapshotRecord",
            fields=[
                ("uid", models.BigAutoField(primary_key=True, serialize=False)),
                ("application_name", models.CharField(max_length=32)),
                ("originator_id", models.UUIDField()),
                ("originator_version", models.BigIntegerField()),
                ("topic", models.TextField()),
                ("state", models.BinaryField()),
            ],
            options={"db_table": "entity_snapshots"},
        ),
        migrations.CreateModel(
            name="IntegerSequencedRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("sequence_id", models.UUIDField()),
                ("position", models.BigIntegerField()),
                ("topic", models.TextField()),
                ("state", models.BinaryField()),
            ],
            options={"db_table": "integer_sequenced_items"},
        ),
        migrations.CreateModel(
            name="NotificationTrackingRecord",
            fields=[
                ("uid", models.BigAutoField(primary_key=True, serialize=False)),
                ("application_name", models.CharField(max_length=32)),
                ("upstream_application_name", models.CharField(max_length=32)),
                ("pipeline_id", models.IntegerField()),
                ("notification_id", models.BigIntegerField()),
            ],
            options={"db_table": "notification_tracking"},
        ),
        migrations.CreateModel(
            name="SnapshotRecord",
            fields=[
                ("uid", models.BigAutoField(primary_key=True, serialize=False)),
                ("sequence_id", models.UUIDField()),
                ("position", models.BigIntegerField()),
                ("topic", models.TextField()),
                ("state", models.BinaryField()),
            ],
            options={"db_table": "snapshots"},
        ),
        migrations.CreateModel(
            name="StoredEventRecord",
            fields=[
                ("uid", models.BigAutoField(primary_key=True, serialize=False)),
                ("application_name", models.CharField(max_length=32)),
                ("originator_id", models.UUIDField()),
                ("originator_version", models.BigIntegerField()),
                ("pipeline_id", models.IntegerField()),
                ("notification_id", models.BigIntegerField()),
                ("topic", models.TextField()),
                ("state", models.BinaryField()),
                ("causal_dependencies", models.TextField()),
            ],
            options={"db_table": "stored_events"},
        ),
        migrations.CreateModel(
            name="TimestampSequencedRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("sequence_id", models.UUIDField()),
                ("position", models.DecimalField(decimal_places=6, max_digits=24)),
                ("topic", models.TextField()),
                ("state", models.BinaryField()),
            ],
            options={"db_table": "timestamp_sequenced_items"},
        ),
        migrations.AddIndex(
            model_name="timestampsequencedrecord",
            index=models.Index(fields=["position"], name="position_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="timestampsequencedrecord",
            unique_together={("sequence_id", "position")},
        ),
        migrations.AlterUniqueTogether(
            name="storedeventrecord",
            unique_together={
                ("application_name", "originator_id", "originator_version"),
                ("application_name", "pipeline_id", "notification_id"),
            },
        ),
        migrations.AlterUniqueTogether(
            name="snapshotrecord", unique_together={("sequence_id", "position")}
        ),
        migrations.AlterUniqueTogether(
            name="notificationtrackingrecord",
            unique_together={
                (
                    "application_name",
                    "upstream_application_name",
                    "pipeline_id",
                    "notification_id",
                )
            },
        ),
        migrations.AlterUniqueTogether(
            name="integersequencedrecord", unique_together={("sequence_id", "position")}
        ),
        migrations.AlterUniqueTogether(
            name="entitysnapshotrecord",
            unique_together={
                ("application_name", "originator_id", "originator_version")
            },
        ),
    ]
