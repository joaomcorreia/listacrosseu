# Generated migration for SEO fields addition

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),  # Adjust based on your existing migrations
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='Optional. Use to specify the preferred URL for this page to prevent duplicate content issues.', verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='category',
            name='og_description',
            field=models.CharField(blank=True, help_text='Description when shared on social media. Falls back to meta_description if empty.', max_length=200, verbose_name='Open Graph Description'),
        ),
        migrations.AddField(
            model_name='category',
            name='og_image',
            field=models.URLField(blank=True, help_text='Image when shared on social media. Recommended size: 1200x630px.', verbose_name='Open Graph Image'),
        ),
        migrations.AddField(
            model_name='category',
            name='og_title',
            field=models.CharField(blank=True, help_text='Title when shared on social media. Falls back to meta_title if empty.', max_length=120, verbose_name='Open Graph Title'),
        ),
        migrations.AddField(
            model_name='category',
            name='robots',
            field=models.CharField(blank=True, default='index,follow', help_text='Controls how search engines crawl this page. Common values: index,follow | noindex,nofollow | index,nofollow', max_length=50, verbose_name='Robots'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Recommended: 120-160 characters. This appears as the snippet under the title in search results.', max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Recommended: 50-60 characters. This appears as the clickable headline in search results.', max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='business',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='Optional. Use to specify the preferred URL for this page to prevent duplicate content issues.', verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='business',
            name='og_description',
            field=models.CharField(blank=True, help_text='Description when shared on social media. Falls back to meta_description if empty.', max_length=200, verbose_name='Open Graph Description'),
        ),
        migrations.AddField(
            model_name='business',
            name='og_image',
            field=models.URLField(blank=True, help_text='Image when shared on social media. Recommended size: 1200x630px.', verbose_name='Open Graph Image'),
        ),
        migrations.AddField(
            model_name='business',
            name='og_title',
            field=models.CharField(blank=True, help_text='Title when shared on social media. Falls back to meta_title if empty.', max_length=120, verbose_name='Open Graph Title'),
        ),
        migrations.AddField(
            model_name='business',
            name='robots',
            field=models.CharField(blank=True, default='index,follow', help_text='Controls how search engines crawl this page. Common values: index,follow | noindex,nofollow | index,nofollow', max_length=50, verbose_name='Robots'),
        ),
        migrations.AlterField(
            model_name='business',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Recommended: 120-160 characters. This appears as the snippet under the title in search results.', max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AlterField(
            model_name='business',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Recommended: 50-60 characters. This appears as the clickable headline in search results.', max_length=70, verbose_name='Meta Title'),
        ),
    ]