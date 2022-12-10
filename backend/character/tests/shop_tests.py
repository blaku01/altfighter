from django.test import TestCase
from character.tasks import refresh_character_shops
from users.factories import UserFactory
from character.factories import CharacterFactory
from item.factories import ItemFactory

class RefreshCharacterShopsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = UserFactory()


        # Create a test character for the user
        self.character = CharacterFactory(created_by=self.user)


        # Create some items for the character's shop
        self.items = ItemFactory.create_batch(2, belongs_to=self.character)


    def test_refresh_character_shops(self):
        # Call the refresh_character_shops() function
        refresh_character_shops()

        # Verify that new items have been created for the character's shop
        self.assertGreater(self.character.shop.count(), 0)

        # Verify that the new items have the correct attributes
        for item in self.character.shop:
            self.assertEqual(item.belongs_to, self.character)
            self.assertIn(item.type, [1, 2, 3, 4, 5, 6])
            self.assertGreater(item.price, 0)
            self.assertIn(item.damage, [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
            self.assertIn(
                item.block_chance, [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25]
            )
            self.assertGreater(item.strength, 0)
            self.assertGreater(item.agility, )
            self.assertGreater(item.vitality, 0)
            self.assertGreater(item.luck, 0)
