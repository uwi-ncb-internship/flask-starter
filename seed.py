from app.extensions import db
from app.models import User, Product

def seed_data():
    # Create and add Users
    user1 = User('Jack Quick', 'jquick@example.com', 'Password123', 'Admin')
    user2 = User('Flo Bryant', 'fbryant@example.com', 'Password123', 'Regular')
    db.session.add_all([user1, user2])

    # Create and add Products
    product1 = Product('Dining Armchair in Pink', 'Designed for comfort, these dining chairs are upholstered in a soft fabric and foam-filled for extra cushioning.', 199.00, 'published', 'pink-chair_0_21_0_2.jpg', 1)
    product2 = Product('Side Table', "With a clean, modern aesthetic our furniture range is made from predominantly solid oak and oak veneers for a durable and visually striking finish. You'll enjoy the beautiful natural grain of the wood, as well as the enduring style and an elegant profile that will stand the test of time.", 125.00, 'pending', 'side-table_0_21_0_2.jpg', 1)
    product3 = Product('Basic Bar Stool', "You can't go wrong with a stool so full of right angles that is! Square on top, square on the sides, squares for support. Plump your tuchus on this conveniently vented seat and enjoy that morning coffee at your kitchen bar while you muse about your day. Finished with a light stain with steel reinforced foot rests for extra durability.", 99.99, 'published', '(Wood & Co.) Basic Bar Stool.jpg', 2)
    product4 = Product('White & Wood Chair', "This chair features a modern design with a white plastic bucket seat on four natural finished wooden legs. Geometric steel support bars ensure the chair can support even the heftiest of bums. Round plastic feet tip each leg to protect your floors. Optional soft fabric pads included for extra protection.", 249.20, 'pending', '(Modern Furnishings) White & Wood Chair - 1_2.jpg', 2)
    db.session.add_all([product1, product2, product3, product4])

    db.session.commit()

# if __name__ == "__main__":
#     seed_data()