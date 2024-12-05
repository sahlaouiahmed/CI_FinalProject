# Kitchen Garden

Welcome to Kitchen Garden – your ultimate destination for all things gardening! Whether you're a seasoned green thumb or just starting your journey into the world of gardening, our platform is designed to cater to your needs with a wide range of gardening supplies and products.

At Kitchen Garden, we believe that everyone deserves a slice of nature, no matter where they live. Our mission is to provide you with the best tools, seeds, and accessories to create your own lush, thriving garden, be it on a balcony, backyard, or a small windowsill. Our carefully curated selection of products ensures that you can cultivate your garden with ease and enjoyment.

Our user-friendly website allows you to browse through an extensive collection of high-quality products, add your favorite items to the cart, and seamlessly checkout with our secure payment system powered by Stripe. With detailed product descriptions, customer reviews, and expert gardening tips, we're here to support you every step of the way.

Join our community of gardening enthusiasts and discover the joy of growing your own plants, herbs, and vegetables. At Kitchen Garden, we are committed to helping you bring the beauty of nature into your home.

Start your gardening adventure with us today and let your garden flourish with Kitchen Garden!

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Technologies](#TechnologiesUsed)
- [UserStories](#UserStories)
- [AppsOverview](#AppsOverview)
- [ERD](#ERD)

## Features

- User authentication and authorization
- Product listing with search and filter capabilities
- Shopping cart functionality
- Order management
- Checkout system with Stripe integration
- **Educational Articles:** Access a variety of articles and resources designed especially for beginners. Learn about selecting the right plants, understanding soil types, essential gardening tools, and seasonal maintenance tips.
- User-friendly interface

## Usage

Once the development server is running, you can access the application in your web browser at [KitchenGarden](https://ci-finalproject-93798f70d775.herokuapp.com/). From there, you can:

- Browse products
- Add products to your shopping cart
- Proceed to checkout and complete orders
- Manage your account and view order history
- **Read Educational Articles:** New to gardening? Our platform offers a wealth of articles that cover everything you need to get started. From planting tips to seasonal advice, we've got you covered.

## Technologies Used

- Django: Backend framework
- HTML/CSS: Frontend design
- JavaScript: Frontend interactivity
- Stripe: Payment processing
- PostgreSQL: Database (for production)
- Python: Programming language

## User Stories

### Store App

- **As a user,** I want to browse a catalog of gardening products so that I can find items to purchase.
- **As a user,** I want to search for specific products so that I can quickly locate the items I need.
- **As a user,** I want to add products to my shopping cart so that I can purchase multiple items in one order.
- **As a user,** I want to view the items in my shopping cart so that I can review my selections before checkout.
- **As a user,** I want to update the quantity of items in my shopping cart so that I can purchase the correct amount.
- **As a user,** I want to remove items from my shopping cart so that I can adjust my order.
- **As a user,** I want to proceed to checkout and provide my shipping information so that I can complete my purchase.
- **As a user,** I want to securely pay for my order using Stripe so that I can complete my purchase with confidence.

### Reviews App

- **As a user,** I want to read reviews for products so that I can make informed purchasing decisions.
- **As a user,** I want to leave a review for a product I purchased so that I can share my experience with others.
- **As a user,** I want to rate products I have purchased so that I can provide feedback to the store.
- **As a user,** I want to see the average rating for a product so that I can quickly gauge its quality.

### Articles App

- **As a user,** I want to read articles about gardening so that I can learn more about different gardening techniques and tips.
- **As a user,** I want to filter articles based on categories so that I can find information relevant to my interests.
- **As a user,** I want to search for specific articles so that I can quickly find the information I need.
- **As a user,** I want to comment on articles so that I can engage with the community and share my thoughts.
- **As a user,** I want to like articles that I found helpful so that I can show my appreciation and support the authors.

## User Stories

### Store App

- **As a user,** I want to browse a catalog of gardening products so that I can find items to purchase.
- **As a registered user,** I want to add products to my shopping cart so that I can purchase multiple items in one order.
- **As a registered user,** I want to view the items in my shopping cart so that I can review my selections before checkout.
- **As a registered user,** I want to proceed to checkout and provide my shipping information so that I can complete my purchase.
- **As a registered user,** I want to securely pay for my order using Stripe so that I can complete my purchase with confidence.

### Reviews App

- **As a user,** I want to read reviews about the website and services so that I can make informed decisions about using the platform.
- **As a registered user,** I want to leave a review about my experience with the website and services so that I can share feedback with others.
- **As a registered user,** I want to rate the website and services so that I can provide feedback to help improve the platform.

### Articles App

- **As a user,** I want to read articles about gardening so that I can learn more about different gardening techniques and tips.
- **As a user,** I want to search for specific articles so that I can quickly find the information I need.

### Account Management

- **As a user,** I want to create an account so that I can manage my orders and preferences.
- **As a registred user,** I want to log in to my account so that I can access my personal dashboard and order history.
- **As a registred user,** I want to reset my password if I forget it so that I can regain access to my account.

### Website Functionalities

- **As a user,** I can browse and search for gardening products.
- **As a registred user,** I can add products to my shopping cart and review them before checkout.
- **As a registred user,** I can securely complete my purchase using Stripe.
- **As a registered user,** I can read and leave reviews about the website and services.
- **As a user,** I can read articles on various gardening topics.
- **As a registred user,** I can manage my account and view my order history.

## Apps Overview

### Core App

The Core app serves as the backbone of the project, handling essential functionalities such as the home page, contact page, and subscription management. This app ensures that users can navigate the main sections of the website, get in touch through the contact page, and subscribe to newsletters and updates.

**Key Features:**
- Home page management with essential information and navigation links.
- Contact page for users to reach out with inquiries or feedback.
- Subscription functionality to allow users to sign up for newsletters and updates.

### Store App

The Store app is the heart of the Kitchen Garden project, offering a comprehensive catalog of gardening products. Users can browse, search, and filter products, add items to their shopping cart, and proceed to a secure checkout using Stripe. The app also includes features for order management and tracking.

**Key Features:**
- Product catalog with search and filter capabilities.
- Shopping cart functionality.
- Secure checkout with Stripe integration.
- Order management and tracking.

### Articles App

The Articles app provides a wealth of information on various gardening topics. Users can access educational articles, search for specific topics, and filter content based on their interests. This app aims to support users in their gardening journey by offering expert tips and advice.

**Key Features:**
- Access to a library of gardening articles.
- Search and filter functionality for articles.
- Educational content aimed at beginners and experienced gardeners alike.

### Reviews App

The Reviews app enables users to leave feedback about their experiences with the website and services. Users can share their thoughts, rate the overall service, and help others make informed decisions. This app focuses on collecting valuable user input to continually improve the platform and ensure customer satisfaction.

**Key Features:**
- Users can read and write reviews about the website and services.
- Star rating system to provide quantitative feedback.
- Moderation tools to ensure the quality and relevance of reviews.

## ERD

### Article Model

**Entity:** `Article`
- **Attributes:**
  - `id` (Primary Key)
  - `title`: `CharField` (max_length=200)
  - `content`: `TextField`
  - `image`: `ImageField` (upload_to='static/images/articles')
  - `published_date`: `DateTimeField` (default=timezone.now)
  - `updated_date`: `DateTimeField` (auto_now=True)

```plaintext
+-----------------+
|     Article     |
+-----------------+
| id (PK)         |
| title           |
| content         |
| image           |
| published_date  |
| updated_date    |
+-----------------+
```

### Profile Model

**Entity:** `Profile`
- **Attributes:**
  - `id` (Primary Key)
  - `user`: `OneToOneField` (User, on_delete=models.CASCADE)
  - `is_subscribed`: `BooleanField` (default=True)

```plaintext
+-----------------+
|     Profile     |
+-----------------+
| id (PK)         |
| user            |
| is_subscribed   |
+-----------------+
```


### Product Model

**Entity:** `Product`
- **Attributes:**
  - `id` (Primary Key)
  - `name`: `CharField` (max_length=255)
  - `description`: `TextField`
  - `price`: `DecimalField` (max_digits=10, decimal_places=2)
  - `image`: `ImageField` (upload_to='static/images/products')
  - `category`: `CharField` (max_length=50, choices=CATEGORY_CHOICES)
  - `stock`: `PositiveIntegerField` (default=0)
  - `created_at`: `DateTimeField` (auto_now_add=True)
  - `updated_at`: `DateTimeField` (auto_now=True)

```plaintext
+-----------------+
|     Product     |
+-----------------+
| id (PK)         |
| name            |
| description     |
| price           |
| image           |
| category        |
| stock           |
| created_at      |
| updated_at      |
+-----------------+
```


### CartItem Model

**Entity:** `CartItem`
- **Attributes:**
  - `id` (Primary Key)
  - `user`: `ForeignKey` (User, on_delete=models.CASCADE)
  - `product`: `ForeignKey` (Product, on_delete=models.CASCADE)
  - `quantity`: `PositiveIntegerField` (default=1)

```plaintext
+-----------------+
|    CartItem     |
+-----------------+
| id (PK)         |
| user            |
| product         |
| quantity        |
+-----------------+
```


### Order Model

**Entity:** `Order`
- **Attributes:**
  - `id` (Primary Key)
  - `user`: `ForeignKey` (User, on_delete=models.CASCADE)
  - `first_name`: `CharField` (max_length=100)
  - `last_name`: `CharField` (max_length=100)
  - `email`: `EmailField`
  - `address`: `CharField` (max_length=255)
  - `city`: `CharField` (max_length=100)
  - `state`: `CharField` (max_length=100)
  - `zip_code`: `CharField` (max_length=10)
  - `items`: `JSONField` (default=dict)
  - `total_amount`: `DecimalField` (max_digits=10, decimal_places=2, default=0.0)
  - `created_at`: `DateTimeField` (auto_now_add=True)

```plaintext
+-----------------+
|      Order      |
+-----------------+
| id (PK)         |
| user            |
| first_name      |
| last_name       |
| email           |
| address         |
| city            |
| state           |
| zip_code        |
| items           |
| total_amount    |
| created_at      |
+-----------------+
```


### Review Model

**Entity:** `Review`
- **Attributes:**
  - `id` (Primary Key)
  - `user`: `ForeignKey` (User, on_delete=models.CASCADE)
  - `rating`: `IntegerField` (choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
  - `comment`: `TextField`
  - `created_at`: `DateTimeField` (auto_now_add=True)

```plaintext
+-----------------+
|     Review      |
+-----------------+
| id (PK)         |
| user            |
| rating          |
| comment         |
| created_at      |
+-----------------+
```
