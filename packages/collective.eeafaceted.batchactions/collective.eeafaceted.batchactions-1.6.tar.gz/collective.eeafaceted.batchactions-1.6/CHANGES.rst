Changelog
=========


1.6 (2020-12-21)
----------------

- After action applied, do not reload the entire page,
  just reload the current faceted results.
  [gbastien]
- Use `CheckBoxFieldWidget` instead `SelectFieldWidget` to manage labels to
  (un)select in `LabelsBatchActionForm` to avoid manipulation with
  `CTRL+click` for selection. Adapted and rationalized translations.
  [gbastien]
- Add a `collective.fingerpointing` entry when applying action to know
  which action was applied on how much elements.
  [gbastien]

1.5 (2020-04-23)
----------------

- Make sure elements are treated in received `uids` order. Need to rely on
  `imio.helpers` to use `content.uuidsToCatalogBrains(ordered=True)`.
  [gbastien]

1.4 (2019-11-25)
----------------

- Added view to change labels. (button is not added)
  [sgeulette]
- Added base view to change a collective.contact.widget field.
  [sgeulette]

1.3 (2019-05-16)
----------------

- Moved method `browser.views.brains_from_uids` to `utils`, added helper method
  `utils.listify_uids` that turns the data uids that is a string with each UID
  separated by a comma into a real python list.
  [gbastien]
- Display number of elements affected by action in the batch action form description.
  [gbastien]

1.2 (2019-03-08)
----------------

- Added weight attribute on batch action forms to order them.
  [sgeulette]
- Improved brains_from_uids
  [sgeulette]
- Added utils method
  [sgeulette]

1.1 (2018-08-31)
----------------

- Don't apply changes if form errors
  [sgeulette]

1.0 (2018-06-20)
----------------

- Moved js variables to `collective.eeafaceted.z3ctable`.
  [gbastien]

0.7 (2018-06-06)
----------------

- Render batch action form in overlay by default, but otherwise with form 'overlay' attribute set to False.
  [sgeulette]

0.6 (2018-01-06)
----------------

- Added condition on apply button.
  [sgeulette]
- Added _update_widgets method
  [sgeulette]

0.5 (2018-01-05)
----------------

- Some changes to made it working with a simple z3c.table.
  [sgeulette]

0.4.1 (2017-12-01)
------------------

- Fixed english po file.
  [gbastien]

0.4 (2017-12-01)
----------------

- Added `collective_eeafaceted_batchactions_js_variables.js` that allows to
  translate the `no_selected_items` message.
  [gbastien]

0.3 (2017-11-30)
----------------

- Renamed `BatchActionForm` to `BaseBatchActionForm` to show that it is the base
  form to inherit from to build new batch action.  Make it inherit from
  `Form` instead `EditForm`.
  [gbastien]
- Refactored the way form is updated and applied : two methods are there to be
  overrided : `_update` that is called in the `update` process and `_apply` that
  is called by `handleApply`.  This way it is easy to build an new action
  without having to think about basic default behavior.
  [gbastien]
- In the `TransitionBatchActionForm`, sort selectable transitions alphabetically.
  [gbastien]

0.2 (2017-11-24)
----------------

- Use `getMultiAdapter` instead `restrictedTraverse` when getting the form
  in the viewlet to speed up things.
  [gbastien]
- Added attribute `button_with_icon` to a batch action, if set to True,
  a particular CSS class is added to the button so it can be skinned
  with an icon easily.
  [gbastien]
- Register a `batch_actions.css` resource for basic styling.
  [gbastien]

0.1 (2017-11-23)
----------------

- Initial release.
  [IMIO]
