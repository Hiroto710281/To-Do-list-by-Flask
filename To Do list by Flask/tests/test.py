import os
import unittest
from importlib import import_module


class FlaskTestCase(unittest.TestCase):
    path = os.path.abspath(
        os.path.dirname(__file__)
    ).replace("tests", "")
    sqlite_path = path + "db/todo.db"

    def setUp(self):
        import shutil

        shutil.copyfile(
            "./db/todo_original.db", "./db/todo.db"
        )

    def __valid_add_task(self, c):
        result = c.post(
            "/add",
            data=dict(
                name="iPhone",
                memo="MEMO",
                duedate="2018-01-01",
            ),
            follow_redirects=True,
        ).get_data(as_text=True)
        assert "<td>2018-01-01</td>" in result
        assert "iPhone" in result
        assert "<td>未完了</td>" in result

    def test_add_task(self):
        flask_app = import_module("views")
        flask_app.app.testing = True

        with flask_app.app.test_client() as c:
            self.__valid_add_task(c)

    def test_delete_task(self):
        flask_app = import_module("views")
        flask_app.app.testing = True

        with flask_app.app.test_client() as c:
            result = c.get("/delete/1").get_data(
                as_text=True
            )
            assert "<td>メールを書く</td>" not in result

    def test_edit_task(self):
        flask_app = import_module("views")
        flask_app.app.testing = True

        with flask_app.app.test_client() as c:
            result = c.post(
                "/edit/2",
                data=dict(
                    name="iPhoneX",
                    memo="修正しました",
                    duedate="2018-03-01",
                    status="完了済",
                ),
                follow_redirects=True,
            ).get_data(as_text=True)

            assert "<td>2018-03-01</td>" in result
            assert "iPhoneX" in result
            assert "<td>完了済</td>" in result
            assert "<td>修正しました</td>" in result


if __name__ == "__main__":
    unittest.main()
