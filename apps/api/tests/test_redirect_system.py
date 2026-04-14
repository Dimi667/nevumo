import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from apps.api.models import Provider, UrlRedirect
from apps.api.services.provider_service import resolve_provider_slug_safe, resolve_provider_slug


class RedirectSystemTests(unittest.TestCase):
    """Test the redirect system functionality."""

    def test_resolve_current_slug_no_redirect(self):
        """Test that current slug returns provider without redirect."""
        provider = Provider(id=uuid4(), slug='current-slug')
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = provider

        result_provider, redirect_slug = resolve_provider_slug_safe('current-slug', db)
        
        self.assertEqual(result_provider, provider)
        self.assertIsNone(redirect_slug)

    def test_resolve_single_redirect(self):
        """Test single redirect from old slug to new slug."""
        from unittest.mock import patch
        
        provider = Provider(id=uuid4(), slug='new-slug')
        db = MagicMock()
        
        # Mock resolve_provider_slug to simulate redirect scenario
        with patch('apps.api.services.provider_service.resolve_provider_slug') as mock_resolve:
            # Simulate: old-slug redirects to new-slug, new-slug resolves to provider
            mock_resolve.return_value = (provider, 'old-slug')
            
            result_provider, redirect_slug = resolve_provider_slug_safe('old-slug', db)
        
        self.assertEqual(result_provider, provider)
        self.assertEqual(redirect_slug, 'old-slug')

    def test_prevent_redirect_loop(self):
        """Test that redirect loops are prevented."""
        # Create loop: A -> B -> A
        redirect_a = UrlRedirect(id=uuid4(), old_slug='slug-a', new_slug='slug-b', active=True)
        redirect_b = UrlRedirect(id=uuid4(), old_slug='slug-b', new_slug='slug-a', active=True)
        provider_a = Provider(id=uuid4(), slug='slug-a')
        provider_b = Provider(id=uuid4(), slug='slug-b')
        db = MagicMock()
        
        visited_slugs = []
        def mock_query_side_effect(model):
            if model == Provider:
                mock_result = MagicMock()
                # Return None for first call, then providers for subsequent calls
                if len(visited_slugs) == 0:
                    mock_result.filter.return_value.first.return_value = None
                elif 'slug-a' in str(mock_result):
                    mock_result.filter.return_value.first.return_value = provider_a
                else:
                    mock_result.filter.return_value.first.return_value = provider_b
                return mock_result
            elif model == UrlRedirect:
                mock_result = MagicMock()
                mock_filter = MagicMock()
                mock_result.filter.return_value = mock_filter
                # Track visited slugs to simulate loop
                current_slug = 'slug-a' if len(visited_slugs) == 0 else 'slug-b'
                visited_slugs.append(current_slug)
                target_redirect = redirect_a if current_slug == 'slug-a' else redirect_b
                mock_filter.filter.return_value.order_by.return_value.first.return_value = target_redirect
                return mock_result
            return MagicMock()
        
        db.query.side_effect = mock_query_side_effect

        result_provider, redirect_slug = resolve_provider_slug_safe('slug-a', db)
        
        # Should return None, None due to loop detection
        self.assertIsNone(result_provider)
        self.assertIsNone(redirect_slug)

    def test_max_depth_protection(self):
        """Test that max depth prevents infinite chains."""
        db = MagicMock()
        
        def mock_query_side_effect(model):
            if model == Provider:
                mock_result = MagicMock()
                mock_result.filter.return_value.first.return_value = None  # Never find provider
                return mock_result
            elif model == UrlRedirect:
                mock_result = MagicMock()
                mock_filter = MagicMock()
                mock_result.filter.return_value = mock_filter
                mock_filter.filter.return_value.order_by.return_value.first.return_value = UrlRedirect(
                    id=uuid4(),
                    provider_id=uuid4(),
                    old_slug=f'slug-{mock_query_side_effect.call_count}',
                    new_slug=f'slug-{mock_query_side_effect.call_count + 1}',
                    active=True
                )
                mock_query_side_effect.call_count += 1
                return mock_result
            return MagicMock()
        
        mock_query_side_effect.call_count = 0
        db.query.side_effect = mock_query_side_effect

        result_provider, redirect_slug = resolve_provider_slug_safe('slug-0', db, max_depth=3)
        
        # Should return None, None due to max depth
        self.assertIsNone(result_provider)
        self.assertIsNone(redirect_slug)


if __name__ == '__main__':
    unittest.main()
