# Posting events and news

The club posts events and news through **Pages CMS**, an outside editor that signs in with GitHub and
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

- Events show under **Upcoming** until their date has passed, then move to **Past events**.
- Everything is optional except title, type and date.
- Switch on **Hide from the website** to save a draft without publishing it.
- The text is plain text: leave a blank line between paragraphs.
- Photos you upload are stored in `assets/uploads`. Wide photos (about 1600 x 800) look best.

## Posting news

Same steps, but choose **News**. News has its own page on the website (the News link in the menu). The short summary appears on the card and the article opens on its own page.

## How it works (for whoever maintains the site)

- Each post is one small JSON file in `content/events/` or `content/news/`, created by the CMS.
- `scripts/build_content.py` gathers them into `data/events.json` and `data/news.json`. The GitHub
  Pages workflow runs it on every push, so a CMS save publishes automatically.
- A post with a missing title or date is skipped with a warning in the workflow log instead of breaking the deploy.
- The CMS form fields are defined in `.pages.yml`.
- The news list is the page `#news`. Single pages have addresses like `#event/mentor-fair` and `#news/new-partner`.
