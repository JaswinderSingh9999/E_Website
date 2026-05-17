from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=50)
    country = models.CharField(max_length=100)   
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Order(models.Model):
    order_id = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'   # ✅ IMPORTANT
    )
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product_name

class Product(models.Model):
    pr_name = models.CharField(max_length=100)
    pr_details = models.TextField()
    pr_price = models.DecimalField(max_digits=10, decimal_places=2)
    pr_url_image = models.ImageField(upload_to='products/')
    def __str__(self):
        return self.pr_name

# courses
class Course(models.Model):
    co_title = models.CharField(max_length=200)
    co_details = models.TextField()
    co_image = models.ImageField(upload_to='courses/')

    def __str__(self):
        return self.co_title

# Teacher 
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to='teachers/')

    def __str__(self):
        return self.name

# FAQ 
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
# Contact Info (left side)
class ContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.email


# Contact Form (right side form data)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# Newsletter
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# Footer Main Content
class Footer(models.Model):
    newsletter_title = models.CharField(max_length=200)
    newsletter_desc = models.TextField()

    about_title = models.CharField(max_length=200)
    about_desc = models.TextField()

    def __str__(self):
        return "Footer Content"


# Footer Contact
class FooterContact(models.Model):
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField()

    def __str__(self):
        return self.email