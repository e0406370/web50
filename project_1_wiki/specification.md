# Website Specifications

## Entry Page

- [x] Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
- [x] If the entry exists:
  - [x] Display the Markdown-converted content of the entry.
  - [x] The page title should include the name of the entry.
- [x] If the entry does **NOT** exist:
  - [x] Display an error page indicating that the requested page was not found.
- [x] Use the appropriate `util` function to fetch the entry content.

## Index Page

- [x] On `index.html`, list all encyclopedia entries.
- [x] Each entry name should be a clickable link that navigates directly to that entry page.

## Search

- [x] Add a search box to the sidebar to allow users to search for an encyclopedia entry.
- [x] If the search query **matches** the name of an encyclopedia entry exactly:
  - [x] Redirect the user directly to that entry page.
- [x] If the search query **does not match** any entry name exactly:
  - [x] Display a search results page listing all entries where the query is a substring.
  - [x] Each result should be a clickable link to the corresponding entry page.

## New Page

- [x] Add a “Create New Page” link in the sidebar.
- [x] The new page should:
  - [x] Provide text input field for the title and `textarea` field for the Markdown content of the page.
  - [x] Include a button to save the new entry.
- [x] If an entry already exists with the provided title:
  - [x] Display an error message to the user.
- [x] If the entry does **NOT** exist:
  - [x] Save the new entry to disk.
  - [x] Redirect the user to the new entry’s page.

## Edit Page

- [x] On each entry page, include a link to edit the page.
- [x] The edit page should:
  - [x] Contain a `textarea` pre-populated with the existing Markdown content.
  - [x] Allow the user to update the content.
  - [x] Include a button to save the changes.
- [x] After saving:
  - [x] Update the entry on disk.
  - [x] Redirect the user to the updated entry’s page.

## Random Page

- [x] Include a “Random Page” link in the sidebar.
- [x] Clicking it should take the user to a randomly chosen encyclopedia entry.

## Markdown to HTML Conversion

- [x] Convert each entry’s Markdown content to HTML before displaying it on the entry page.
- [x] You may use the `markdown2` package (`pip3 install markdown2`) for this conversion.
