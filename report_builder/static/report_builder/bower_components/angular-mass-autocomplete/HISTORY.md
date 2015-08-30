MassAutocomplete
================

### v0.2.3
- Fixed suggestion box opened when no item or other item is selected (Issue #20 - Thanks @pfiaux for opening the issue).
- Prevent suggestion box from flushing when loading new results (Issue #21 - Thanks @dkulchenko for opening the issue).
- Prevent form submittion on enter (Issue #23 - Thanks @alxdnlnko  for the PR).

### v0.2.2
- Added option auto_select_first to select the first suggestion automatically (issue #10).
- AC item directive is now using an isolated scope (issues #14 and #15).
- Fixed close suggestion box on blur (issue #11).
- Fixed value watch on destroy (issue #6).
- Generate dist with gulp.
- Fixed https references in gh-pages (Thank @dustinchilson for noticing).

### v0.2.1
- Don't clear value on detach (issue #6).
- Fixed bug causing values to be cleared on detach.
- Moved to semantic versioning.

### v0.2
- Dropped jquery dependency (issue #1).
- Fixed Long press on menu item does not select the item.
- Unbinding event from current element on detach when element does not exists (issue #3).
- Selecting an item from the list with the keyboard is not always passing the object to the on_select callback (issue #4).

### v0.1
- Initial
