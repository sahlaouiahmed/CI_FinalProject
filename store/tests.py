from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import ShippingForm, ProductForm
from django.conf import settings
from unittest.mock import patch
from django.contrib.messages import get_messages


########### PASS #############
class ProductListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(
            name='Seed Product',
            description='Description of seed product',
            price=10.00,
            image=SimpleUploadedFile(name='seed.jpg', content=b'', content_type='image/jpeg'),
            category='seed',
            stock=10
        )
        self.product2 = Product.objects.create(
            name='Supply Product',
            description='Description of supply product',
            price=20.00,
            image=SimpleUploadedFile(name='supply.jpg', content=b'', content_type='image/jpeg'),
            category='supply',
            stock=5
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')
        self.assertContains(response, 'Seed Product')
        self.assertContains(response, 'Supply Product')

    def test_product_list_view_with_query(self):
        response = self.client.get(reverse('product_list'), {'q': 'Seed'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')
        self.assertContains(response, 'Seed Product')
        self.assertNotContains(response, 'Supply Product')

    def test_product_list_view_with_category(self):
        response = self.client.get(reverse('product_list'), {'category': 'seed'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')
        self.assertContains(response, 'Seed Product')
        self.assertNotContains(response, 'Supply Product')

    def test_product_list_view_with_query_and_category(self):
        response = self.client.get(reverse('product_list'), {'q': 'Seed', 'category': 'seed'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')
        self.assertContains(response, 'Seed Product')
        self.assertNotContains(response, 'Supply Product')


############# PASS #############
class ProductDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(
            name='Seed Product',
            description='Description of seed product',
            price=10.00,
            image=SimpleUploadedFile(name='seed.jpg', content=b'', content_type='image/jpeg'),
            category='seed',
            stock=10
        )
        self.product2 = Product.objects.create(
            name='Another Seed Product',
            description='Description of another seed product',
            price=15.00,
            image=SimpleUploadedFile(name='another_seed.jpg', content=b'', content_type='image/jpeg'),
            category='seed',
            stock=5
        )
        self.product3 = Product.objects.create(
            name='Supply Product',
            description='Description of supply product',
            price=20.00,
            image=SimpleUploadedFile(name='supply.jpg', content=b'', content_type='image/jpeg'),
            category='supply',
            stock=5
        )

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')
        self.assertContains(response, 'Seed Product')
        self.assertContains(response, 'Description of seed product')

    def test_related_products(self):
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')
        self.assertContains(response, 'Another Seed Product')
        self.assertNotContains(response, 'Supply Product')


############### PASS ###############
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages

class AddToCartViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Test Product',
            description='Description of test product',
            price=10.00,
            image=SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg'),
            category='seed',
            stock=10
        )

    def test_add_to_cart_success(self):
        response = self.client.get(reverse('add_to_cart', kwargs={'product_id': self.product.id}), follow=True)
        self.assertRedirects(response, reverse('product_list'))

        # Check if the cart item was created
        cart_item = CartItem.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

        # Refresh the product instance from the database
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Test Product has been added to your cart successfully!' for message in messages))

    def test_add_to_cart_out_of_stock(self):
        self.product.stock = 0
        self.product.save()
        
        response = self.client.get(reverse('add_to_cart', kwargs={'product_id': self.product.id}), follow=True)
        self.assertRedirects(response, reverse('product_list'))

        # Check if the cart item was not created
        self.assertFalse(CartItem.objects.filter(user=self.user, product=self.product).exists())

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Sorry, this product is out of stock.' for message in messages))

############## PASS #################
class CartViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(
            name='Test Product',
            description='Description of test product',
            price=10.00,
            image=SimpleUploadedFile(name='test.jpg', content=b'test content', content_type='image/jpeg'),
            category='seed',
            stock=10
        )
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def test_cart_view(self):
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')

        # Log response content for debugging
        with open('response.html', 'w') as f:
            f.write(response.content.decode())

        self.assertContains(response, 'Test Product')

        # Simplified check for the presence of quantity input
        self.assertIn(f'id="quantity_{self.cart_item.id}"', response.content.decode())
        self.assertIn(f'name="quantity"', response.content.decode())
        self.assertIn(f'value="1"', response.content.decode())

    def test_cart_view_empty(self):
        # Remove cart items to simulate an empty cart
        CartItem.objects.all().delete()

        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')
        self.assertNotContains(response, 'Test Product')
        self.assertContains(response, 'Your cart is empty')

############## PASS #################
class UpdateCartViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(
            name='Test Product',
            description='Description of test product',
            price=10.00,
            image=SimpleUploadedFile(name='test.jpg', content=b'test content', content_type='image/jpeg'),
            category='seed',
            stock=10
        )
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def test_update_cart_quantity(self):
        response = self.client.post(reverse('update_cart', kwargs={'item_id': self.cart_item.id}), data={'quantity': 5}, follow=True)
        self.assertRedirects(response, reverse('cart_view'))

        # Refresh the cart item from the database
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Cart updated successfully.' for message in messages))

    def test_update_cart_exceed_stock(self):
        response = self.client.post(reverse('update_cart', kwargs={'item_id': self.cart_item.id}), data={'quantity': 15}, follow=True)
        self.assertRedirects(response, reverse('cart_view'))

        # Refresh the cart item from the database
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 1)  # Quantity should remain unchanged

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == f"Only {self.product.stock} items available in stock." for message in messages))

    def test_update_cart_remove_item(self):
        response = self.client.post(reverse('update_cart', kwargs={'item_id': self.cart_item.id}), data={'quantity': 0}, follow=True)
        self.assertRedirects(response, reverse('cart_view'))

        # Check if the cart item was removed
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Item removed from cart.' for message in messages))


############ PASS #################
class DeleteCartItemViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(
            name='Test Product',
            description='Description of test product',
            price=10.00,
            image=SimpleUploadedFile(name='test.jpg', content=b'test content', content_type='image/jpeg'),
            category='seed',
            stock=10
        )
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def test_delete_cart_item(self):
        response = self.client.post(reverse('delete_cart_item', kwargs={'item_id': self.cart_item.id}), follow=True)
        self.assertRedirects(response, reverse('cart_view'))

        # Check if the cart item was deleted
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        print([message.message for message in messages])  # Print all messages for debugging
        self.assertTrue(any(message.message == 'Item removed from cart.' for message in messages))


########## fail ##############
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import ShippingForm
from django.conf import settings
from unittest.mock import patch

class CheckoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(
            name='Test Product',
            description='Description of test product',
            price=10.00,
            image=SimpleUploadedFile(name='test.jpg', content=b'test content', content_type='image/jpeg'),
            category='seed',
            stock=10
        )
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

    @patch('stripe.checkout.Session.create')
    def test_checkout_success(self, mock_stripe_session_create):
        mock_stripe_session_create.return_value.id = 'test_session_id'
        mock_stripe_session_create.return_value.url = 'https://example.com/checkout-session'

        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001'
        }

        response = self.client.post(reverse('checkout'), data=form_data, follow=True)

        if response.status_code == 400:
            print("Form errors:")
            form = ShippingForm(data=form_data)
            if not form.is_valid():
                print(form.errors)
            print(response.content.decode())

        self.assertRedirects(response, 'https://example.com/checkout-session')

        # Verify that the session data is stored correctly
        session_data = self.client.session['checkout_data']
        self.assertEqual(session_data['first_name'], 'John')
        self.assertEqual(session_data['last_name'], 'Doe')
        self.assertEqual(session_data['email'], 'johndoe@example.com')
        self.assertEqual(session_data['address'], '123 Main St')
        self.assertEqual(session_data['city'], 'New York')
        self.assertEqual(session_data['state'], 'NY')
        self.assertEqual(session_data['zip_code'], '10001')
        self.assertEqual(session_data['amount'], 20.00)  # 2 items at $10 each

    def test_checkout_get(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/checkout.html')
        self.assertIsInstance(response.context['form'], ShippingForm)
        self.assertContains(response, settings.STRIPE_PUBLIC_KEY)



########## PASS ##########
class ShippingFormTestCase(TestCase):
    def test_shipping_form_valid(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001'
        }
        form = ShippingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_shipping_form_invalid(self):
        form_data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001'
        }
        form = ShippingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('email', form.errors)

############## PASS ################
class ProductFormTestCase(TestCase):
    def test_product_form_valid(self):
        form_data = {
            'name': 'Test Product',
            'description': 'Description of test product',
            'price': 10.00,
            'category': 'seed',
            'stock': 10
        }
        # Use a small valid image byte content
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9'
            b'\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00'
            b'\x00\x02\x02\x4c\x01\x00\x3b'
        )
        image = SimpleUploadedFile(name='test.jpg', content=image_content, content_type='image/jpeg')
        form = ProductForm(data=form_data, files={'image': image})
        
        if not form.is_valid():
            print("Form errors:", form.errors)
        
        self.assertTrue(form.is_valid())

    def test_product_form_invalid(self):
        form_data = {
            'name': '',
            'description': 'Description of test product',
            'price': 10.00,
            'category': 'seed',
            'stock': 10
        }
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9'
            b'\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00'
            b'\x00\x02\x02\x4c\x01\x00\x3b'
        )
        image = SimpleUploadedFile(name='test.jpg', content=image_content, content_type='image/jpeg')
        form = ProductForm(data=form_data, files={'image': image})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
