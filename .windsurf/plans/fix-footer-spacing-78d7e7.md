# Fix Footer Link Spacing in ProviderWidget

Add CSS margin-right to the first footer link to create visible spacing between "Общи условия" and "Политика за поверителност" instead of using HTML spaces which get compressed by the browser.

## Changes
File: `apps/web/components/ProviderWidget.tsx`
- Add `mr-3` (margin-right: 0.75rem) class to the first link
- Remove the HTML space characters between links
