---
title: README
description: 
published: true
date: 2025-01-23T21:07:43.185Z
tags: 
editor: markdown
dateCreated: 2025-01-23T21:07:43.185Z
---

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
