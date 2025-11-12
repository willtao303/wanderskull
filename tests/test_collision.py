import wanderskull.utils.collision as Collision


class TestCollision:
    value = 0

    def test_rect_rect(self):
        assert Collision.rect_rect(0, 0, 5, 5, 4, 0, 5, 5)
        assert not Collision.rect_rect(0, 0, 5, 5, 0, 5, 5, 5)
        assert Collision.rect_rect(0, 0, 5, 5, 4, 0, 5, 5, True)
        assert not Collision.rect_rect(0, 0, 5, 5, 0, 5, 5, 5, True)
