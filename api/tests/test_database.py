from help import HelpAPI

class TestDB():
    helper = HelpAPI()

    # def client()

    def test_register_new_user(self, client):
        response = self.helper.post_json(
            client,
            '/api/v2/auth/signup',
            {
                'username': 'phiona',
                'email': 'nanaphiona9@gmail.com',
                'phone_no': '+256758363563',
                'password': 'password'
            })
        assert response.status_code == 201

    def test_login_new_user(self, client):
        self.helper.post_json(
            client,
            '/api/v2/auth/signup',
            {
                'username': 'phiona',
                'email': 'nanaphiona9@gmail.com',
                'phone_no': '+256758363563',
                'password': 'password'
            })

        response = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })
        assert response.json['username'] == 'phiona'
        assert response.status_code == 200
        # delete the user afterwards

    def test_invalid_login(self, client):
        response = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'passwords'
            })
        assert response.status_code == 401

    def test_admin_login(self, client):
        response = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        assert response.status_code == 200

    def test_add_menu_item(self, client):
        # Login as admin
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        response2 = self.helper.post_json_with_token(
            client,
            '/api/v2/menu',
            {
                'item_name': 'admin_item',
                'price': '5000',
            },
            response1.json['token']
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 201

    def test_place_order(self, client):
        # Login as admin and add item to menu
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )

        response2 = self.helper.post_json_with_token(
            client,
            '/api/v2/menu',
            {
                'item_name': 'Fried Eggs',
                'price': '3000'
            },
            response1.json['token']
        )
        # Ensure that you are logged in as user
        response3 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })
        response4 = self.helper.post_json_with_token(
            client,
            '/api/v2/users/orders',
            {
                'username': response3.json['username'],
                'item_name': 'Fried Eggs',
                'quantity': '1',
            },
            response3.json['token']
        )
        assert response1.status_code == 200
        assert response2.status_code == 201
        assert response3.status_code == 200
        assert response4.status_code == 201

    def test_order_history(self, client):
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })

        response2 = client.get(
            '/api/v2/users/orders',
            headers={'Authorization': response1.json['token']}
        )
        assert response1.status_code == 200
        assert response2.status_code == 200

    # def test_fetch_specific_order(self):
    #     # login as admin
    #     response1 = self.helper.post_json(
    #         client,
    #         '/api/v2/auth/login',
    #         {
    #             'username': 'phiona',
    #             'password': 'password'
    #         })

    #     response2 = client.get(
    #         '/api/v2/orders/0',
    #         headers={'Authorization': response1.json['token']}
    #     )
    #     assert response1.status_code == 200
    #     assert response2.status_code == 200

    # def test_fetch_all_orders(self):
    #     pass

    # def test_view_menu(self):
    #     pass

    def test_update_order_status(self, client):
        # admin adds an order to menu
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        response2 = self.helper.post_json_with_token(
            client,
            '/api/v2/menu',
            {
                'item_name': 'Chicken',
                'price': '5000'
            },
            response1.json['token']
        )
        # user places an order
        response3 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })

        response4 = self.helper.post_json_with_token(
            client,
            '/api/v2/users/orders',
            {
                'username': response3.json['username'],
                'item_name': 'Chicken',
                'quantity': '1'
            },
            response3.json['token']
        )
       
        # admin then updates it
        response5 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        response6 = self.helper.put_json_with_token(
            client,
            '/api/v2/orders/0',
            {
                'username': response3.json['username'],
                'item_name': 'Fried Eggs',
                'status_name': 'Processing',
            },
            response5.json['token']
        )
        assert response1.status_code == 200
        assert response2.status_code == 201
        assert response3.status_code == 200
        assert response4.status_code == 201
        assert response5.status_code == 200
        assert response6.status_code == 200
