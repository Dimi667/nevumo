import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from uuid import uuid4

from apps.api.exceptions import NevumoException
from apps.api.models import ProviderSlugHistory, UrlRedirect
from apps.api.services.provider_service import update_provider_profile, validate_slug


class SlugManagementTests(unittest.TestCase):
    def test_validate_slug_allows_hyphenated_values(self) -> None:
        is_valid, error = validate_slug("my-business-name")
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_update_provider_profile_blocks_second_slug_change(self) -> None:
        provider = SimpleNamespace(
            id=uuid4(),
            slug="current-slug",
            slug_change_count=1,
            business_name="Demo",
            description=None,
            availability_status="active",
        )
        db = MagicMock()

        with self.assertRaises(NevumoException) as ctx:
            update_provider_profile(
                provider,
                db,
                business_name=None,
                description=None,
                availability_status=None,
                slug="new-slug",
            )

        self.assertEqual(ctx.exception.code, "SLUG_CHANGE_LIMIT_EXCEEDED")

    def test_update_provider_profile_records_history_and_redirect(self) -> None:
        provider = SimpleNamespace(
            id=uuid4(),
            slug="old-slug",
            slug_change_count=0,
            business_name="Demo",
            description=None,
            availability_status="active",
        )
        db = MagicMock()

        provider_query = MagicMock()
        provider_filter = MagicMock()
        provider_self_exclusion_filter = MagicMock()
        provider_query.filter.return_value = provider_filter
        provider_filter.filter.return_value = provider_self_exclusion_filter
        provider_self_exclusion_filter.first.return_value = None

        redirect_query = MagicMock()
        redirect_filter = MagicMock()
        redirect_self_exclusion_filter = MagicMock()
        redirect_query.filter.return_value = redirect_filter
        redirect_filter.filter.return_value = redirect_self_exclusion_filter
        redirect_self_exclusion_filter.first.return_value = None

        db.query.side_effect = [provider_query, redirect_query]

        updated = update_provider_profile(
            provider,
            db,
            business_name=None,
            description=None,
            availability_status=None,
            slug="new-slug",
            request_ip="127.0.0.1",
            user_agent="UnitTest/1.0",
        )

        self.assertIs(updated, provider)
        self.assertEqual(provider.slug, "new-slug")
        self.assertEqual(provider.slug_change_count, 1)
        self.assertEqual(db.add.call_count, 2)

        first_record = db.add.call_args_list[0].args[0]
        second_record = db.add.call_args_list[1].args[0]
        self.assertIsInstance(first_record, ProviderSlugHistory)
        self.assertIsInstance(second_record, UrlRedirect)
        self.assertEqual(first_record.old_slug, "old-slug")
        self.assertEqual(first_record.new_slug, "new-slug")
        self.assertEqual(second_record.old_slug, "old-slug")
        self.assertEqual(second_record.new_slug, "new-slug")

    # -------------------------------------------------------------------------
    # Regression tests for city_slug parameter fix
    # -------------------------------------------------------------------------

    def test_update_provider_profile_no_crash_when_city_slug_omitted(self) -> None:
        """Regression test: update_provider_profile should not crash when city_slug is omitted.

        Previously, the function declared city_ids but used city_slug internally,
        causing a NameError when slug validation ran.
        """
        provider = SimpleNamespace(
            id=uuid4(),
            slug="old-slug",
            slug_change_count=0,
            business_name="Demo",
            description=None,
            availability_status="active",
        )
        db = MagicMock()

        # Mock queries to simulate slug available (not taken)
        provider_query = MagicMock()
        provider_filter = MagicMock()
        provider_self_exclusion_filter = MagicMock()
        provider_query.filter.return_value = provider_filter
        provider_filter.filter.return_value = provider_self_exclusion_filter
        provider_self_exclusion_filter.first.return_value = None

        redirect_query = MagicMock()
        redirect_filter = MagicMock()
        redirect_self_exclusion_filter = MagicMock()
        redirect_query.filter.return_value = redirect_filter
        redirect_filter.filter.return_value = redirect_self_exclusion_filter
        redirect_self_exclusion_filter.first.return_value = None

        db.query.side_effect = [provider_query, redirect_query]

        # This should NOT raise NameError about city_slug
        updated = update_provider_profile(
            provider,
            db,
            slug="new-slug",
        )

        self.assertEqual(updated.slug, "new-slug")

    def test_update_provider_profile_slug_taken_raises_nevumo_exception(self) -> None:
        """Regression test: slug-taken branch should raise NevumoException, not NameError.

        When a slug is already taken, the function should raise a NevumoException
        with code SLUG_TAKEN and include suggestions, not crash with NameError.
        """
        provider = SimpleNamespace(
            id=uuid4(),
            slug="old-slug",
            slug_change_count=0,
            business_name="Demo",
            description=None,
            availability_status="active",
        )
        db = MagicMock()

        # Mock: another provider already has this slug
        other_provider = SimpleNamespace(id=uuid4(), slug="taken-slug")
        provider_query = MagicMock()
        provider_filter = MagicMock()
        provider_self_exclusion_filter = MagicMock()
        provider_query.filter.return_value = provider_filter
        provider_filter.filter.return_value = provider_self_exclusion_filter
        provider_self_exclusion_filter.first.return_value = other_provider  # slug taken

        db.query.return_value = provider_query

        with self.assertRaises(NevumoException) as ctx:
            update_provider_profile(
                provider,
                db,
                slug="taken-slug",
            )

        self.assertEqual(ctx.exception.code, "SLUG_TAKEN")
        self.assertIn("suggestions", ctx.exception.extra_data or {})


if __name__ == "__main__":
    unittest.main()
