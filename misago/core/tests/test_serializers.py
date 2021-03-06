from rest_framework import serializers

from django.test import TestCase

from misago.categories.models import Category
from misago.core.serializers import MutableFields
from misago.threads import testutils
from misago.threads.models import Thread


class MutableFieldsSerializerTests(TestCase):
    def test_subset_fields(self):
        """classmethod subset_fields creates new serializer"""
        category = Category.objects.get(slug='first-category')
        thread = testutils.post_thread(category=category)

        fields = ('id', 'title', 'replies', 'last_poster_name')

        serializer = TestSerializer.subset_fields(*fields)
        self.assertEqual(
            serializer.__name__,
            'TestSerializerIdTitleRepliesLastPosterNameSubset'
        )
        self.assertEqual(serializer.Meta.fields, fields)

        serialized_thread = serializer(thread).data
        self.assertEqual(serialized_thread, {
            'id': thread.id,
            'title': thread.title,
            'replies': thread.replies,
            'last_poster_name': thread.last_poster_name,
        })

        self.assertFalse(TestSerializer.Meta.fields == serializer.Meta.fields)

    def test_exclude_fields(self):
        """classmethod exclude_fields creates new serializer"""
        category = Category.objects.get(slug='first-category')
        thread = testutils.post_thread(category=category)

        kept_fields = ('id', 'title', 'weight')
        removed_fields = tuple(set(TestSerializer.Meta.fields) - set(kept_fields))

        serializer = TestSerializer.exclude_fields(*removed_fields)
        self.assertEqual(serializer.__name__, 'TestSerializerIdTitleWeightSubset')
        self.assertEqual(serializer.Meta.fields, kept_fields)

        serialized_thread = serializer(thread).data
        self.assertEqual(serialized_thread, {
            'id': thread.id,
            'title': thread.title,
            'weight': thread.weight,
        })

        self.assertFalse(TestSerializer.Meta.fields == serializer.Meta.fields)

    def test_extend_fields(self):
        """classmethod extend_fields creates new serializer"""
        category = Category.objects.get(slug='first-category')
        thread = testutils.post_thread(category=category)

        added_fields = ('category',)

        serializer = TestSerializer.extend_fields(*added_fields)

        serialized_thread = serializer(thread).data
        self.assertEqual(serialized_thread['category'], category.pk)


class TestSerializer(serializers.ModelSerializer, MutableFields):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'replies',
            'has_unapproved_posts',
            'started_on',
            'last_post_on',
            'last_post_is_event',
            'last_post',
            'last_poster_name',
            'is_unapproved',
            'is_hidden',
            'is_closed',
            'weight',
        )
