from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review
from django.contrib.messages import get_messages
from datetime import datetime

class SubmitReviewViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_submit_review_view(self):
        response = self.client.get(reverse('submit_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/submit_review.html')
        self.assertContains(response, '<form')

    def test_post_submit_review_view(self):
        post_data = {
            'rating': 5,
            'comment': 'Great product!'
        }
        response = self.client.post(reverse('submit_review'), data=post_data, follow=True)
        
        # Debugging: Print form errors if the response code is 200
        if response.status_code == 200:
            form = ReviewForm(data=post_data)
            if not form.is_valid():
                print(form.errors)
        
        self.assertRedirects(response, reverse('home'))

        # Check if the review was created
        self.assertTrue(Review.objects.filter(comment='Great product!').exists())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Your review has been added successfully!' for message in messages))

class ViewReviewsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.review1 = Review.objects.create(user=self.user, rating=5, comment='Excellent!', created_at=datetime.now())
        self.review2 = Review.objects.create(user=self.user, rating=4, comment='Good!', created_at=datetime.now())

    def test_view_reviews_view(self):
        response = self.client.get(reverse('view_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/view_reviews.html')
        self.assertContains(response, 'Excellent!')
        self.assertContains(response, 'Good!')
