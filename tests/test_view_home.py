from base import (
    IntegrationTestBase,
)


class IntegrationTest(IntegrationTestBase):
    def test_get_home(self):
        """ GET Home page

        GET / 301

        """
        self.app.get('/', status=302)
