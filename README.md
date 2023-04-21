# River City Rainbow Collective Website
## Architecture
* MkDocs for markdown based static site generation
* Netlify CMS integration for end user edits
* Github Actions for standard CI actions
* CLoudflare pages for industry grade site performance

## Design goals
1. Create a website that enables the community tp update it in real time
1. Reduce the friction for making updates, preferrably from a mobile first approach
1. Secure discord based OAuth flow that checks user roles for the editor role then loads standard github token for edits.
