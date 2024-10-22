from faker import Faker
from locustTesting.models import Post, Comment

fake = Faker()

def generate_post():
    body = [Post(title= f"title {_ +1}") for _ in range(5000)]
    Post.objects.bulk_create(body)
    print("fake Posts created")

def generate_comments():
    body = [ Comment(body= fake.text()) for _ in range(5000)]
    Comment.objects.bulk_create(body)
    print("fake Comments created")

