# Posting events, publications and the team

The club posts events and publications through **Pages CMS**, an outside editor that signs in with GitHub and
shows simple forms. Nothing is installed on the website itself.

## One-time setup (a club admin does this once)

1. Go to <https://app.pagescms.org> and sign in with GitHub.
2. When asked, install the Pages CMS GitHub app on the `riverfishh/M-A-website-Real` repository.
3. To let another committee member post, add them as a collaborator with **Write** access in
   GitHub: repository **Settings > Collaborators**. They sign in to Pages CMS with their own GitHub account.

The "Club admin" link in the website footer opens the CMS for this repository.

## Posting an event

1. Open the repository in Pages CMS and choose **Events**, then **Add an entry**.
2. Fill in the form: title, type, date, times (24-hour, like `18:30`), location, photo, speakers and the text about the event.
3. Save. The website updates about a minute or two later (GitHub rebuilds the site).

- Events have their own page on the website (the Events link in the menu). They show under **Upcoming** until their date has passed, then move to **Past events**.
- Everything is optional except title, type and date.
- Switch on **Hide from the website** to save a draft without publishing it.
- The text is plain text: leave a blank line between paragraphs.
- Photos you upload are stored in `assets/uploads`. Wide photos (about 1600 x 800) look best.

## Posting a publication

Choose **Publications**, then **Add an entry**, and upload the **PDF**. On the website the PDF opens in a
built-in viewer with page arrows, zoom and a Download button. The optional **Cover photo** and
**Short summary** appear on the publication card, and the optional **Text under the PDF** is shown below
the viewer. Without a PDF the entry is shown as a plain text article.

Publications have their own page on the website (the Publications link in the menu).

## Managing the team page

The Team link opens a page with a panel for each department.

- **Add a person:** choose **Team members**, then **Add an entry**. Fill in the name, pick the department,
  write the role, and upload a photo. A portrait photo (about 800 x 1000) works best. Under the photo the
  site shows the department, the name and the role. Without a photo the initials are shown.
- **Order:** the optional "Position in the list" number puts people first (heads are usually 1). People
  with the same number are sorted by name.
- **Someone leaves:** switch on **Hide from the website** instead of deleting them.
- **What a department does:** choose **Departments** to edit each department's short description and key tasks.
  If you rename a department there, also pick the new name on the people in it.

## How it works (for whoever maintains the site)

- Each post is one small JSON file in `content/events/`, `content/news/` (publications) or `content/team/`, created by the CMS.
  Department descriptions are in `content/departments.json`.
- `scripts/build_content.py` gathers them into `data/events.json` and `data/news.json`. The GitHub
  Pages workflow runs it on every push, so a CMS save publishes automatically.
- A post with a missing title or date is skipped with a warning in the workflow log instead of breaking the deploy.
- The CMS form fields are defined in `.pages.yml`.
- The PDF viewer uses the PDF.js library, loaded from cdnjs when a PDF is opened (the browser needs internet access). If it cannot load, the page shows the Download button instead.
- The event list is the page `#events` and the publications list is `#publications`. Single pages have addresses like `#event/mentor-fair` and `#publication/new-partner`.
