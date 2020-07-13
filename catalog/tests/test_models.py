from django.test import TestCase

from catalog.models import Author


# Create your tests here.
class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')

    def setUp(self):
        self.author = Author.objects.get(id=1)

    def test_first_name_label(self):
        field_label = self.author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'Имя')

    def test_last_name_label(self):
        field_label = self.author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'Фамилия')

    def test_date_of_birth(self):
        field_label = self.author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'Дата рождения')

    def test_date_of_death_label(self):
        field_label = self.author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Дата смерти')

    def test_first_name_max_length(self):
        max_length = self.author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        max_length = self.author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        expected_object_name = f'{self.author.last_name} {self.author.first_name}'
        self.assertEqual(expected_object_name, str(self.author))

    def test_get_absolute_url(self):
        self.assertEqual(self.author.get_absolute_url(), '/catalog/author/1')
