import unittest
from unittest import TestCase
from news.models import *

from NewsPaper.news.models import Author, Post


class TestUpdateR(unittest, TestCase):
    def test_store(self, id=1):
        a1 = Author.objects.get(id)
        var = a1.ratingAuthor
        Post
        Post.objects.get(id).like()
