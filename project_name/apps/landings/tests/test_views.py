from user_auth.tests.fixtures import active_user


class DescribeLoading:
    """Test that each landing loads"""
    def it_loads_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def it_loads_dashboard_page(self, client, active_user):
        with active_user.login():
            response = client.get('/dashboard')
            assert response.status_code == 200
