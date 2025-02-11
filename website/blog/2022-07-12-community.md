---
title: 2022-07-12-community
description: 
published: true
date: 2025-02-11T20:58:46.110Z
tags: 
editor: markdown
dateCreated: 2025-01-23T16:27:05.212Z
---

# The Need for Community
River City Rainbow Collective is my attempt at building an inclusive and supportive LGBTQIA+ community in the Central Illinois area. After experiencing what a truly supportive community feels like, both online and in-person, it made me question if that kind of community existed here already. I spent a couple weeks hanging out around facebook (🤢) and analyzing the community landscape there. After getting a grasp on what was currently available to LGBTQIA+ people, I decided that what I'm looking for doesn't exist yet.
 
It's tough being queer in the conservative midwest, so why not try and build the kind of community that I wish existed, be the change I want to see in the world...
 
What I'm attempting to cultivate here, with your help, is a hybrid online/offline community where the majority of the interpersonal interactions happen online (since the geographical span of this group will be 40+ min travel), where we schedule regular, in-person meetups to maintain that real, tangible aspect of these connections, to reinforce that we aren't just random profile pics on the internet.
 
Along with that community is this website, which is technologically designed to be re-built and re-deployed with every change to the codebase. This sort of design enables automatic website content generation. I'll go into more details later if you're curious, but the main point is that the goal of this website is to constantly evolve and be kept updated through a communal effort instead of being the responsibility of one person to update and maintain. There's a lot of magic hand-waving there, but I believe it's possible to find a way for everyone to contribute without being good with computers; that's my goal at least.
 
To wrap this section up, the mission is to cultivate a place to quickly and easily connect with other LGBTQIA+ people in the Central Illinois area, and to build a recommended resource site for us and others in the area who need that kind of assistance.
 
## Background
 
In June 2022, I attended a hobbyist 3D printing convention that I attend just about every year called Midwest Rep Rap Fest. MRRF is always a special time for me, not just because of the printers, but because it's the only weekend out of the year that I get to see all my online friends in person, in one place. This year was especially meaningful for me, because it was the first year I attended while being openly out as transgender, specificially as a non-binary femme person. All the people worth interacting with (and I use those words intentionally) in that community were incredibly warm and welcoming of me as I am, and even went out of their way to politely ask if there were any major changes to how I'd like to be referenced, which was incredible to experience firsthand. So like, people like this actually exist, so why am I not surrounding myself with more people like this?
 
Another important note about that weekend, is that I was able to connect with the other gender non-conforming people there and it really quelled the imposter-syndrome for me to be in the presence of others going through the exact same challenges and personal struggles as I am right now. It really opened my eyes to how critically important connecting with others like yourself is. I've had that with my creative endeavors with River City Labs Makerspace in Peoria, but so far, I haven't experienced that same level of connection locally like I did with my other trans girlies at MRRF. Coming home was a harrowing experience when reality sunk in that I wouldn't be seeing those people's actual faces and expressions for another year.
 
Soon after that weekend, I joined an online discord community started by a trans-femme tiktoker for other trans-femmes and once again I was faced with that overwhelming sense of community as we all shared our struggles, joys, and the everday dealings of managing dysphoria. That community has already been such an invaluable resource for me personally as a newly realized trans person that I once again wished I had that kind of community here in Central Illinois, how amazing would it be to have people locally to talk to, to meet up for coffee, to be there to support each other when we need it, because we need it now more than ever.
 
It reminded me of back when I was indoctrinated into evangelical christanity as a child (I will happily spill that de-constructed tea if there's interest). Religious bullshit aside, one thing I've never managed to find outside of religion is that sense of community in the real world. Why doesn't that exist? Why isn't it more prevalent? Maybe we're just more affected by that lack of social support outside of the church because of being geographically located in the bible belt. I want to replicate that sense of belongingness and community that I experienced as part of the church, but without the religious and cultural baggage. Just to be clear, my beef with evangelical christianity is mostly due to the culty culture that surrounds the religion, not the religion itself. I still hold a lot of Jesus' teaching to heart, but everything else the modern church has become is just a culture of hatred and colonialism. * steps off soapbox *
 
With that said, I realized that if the kind of community I wanted didn't already exist, that it was up to me to create it. I've always been a fan of "be the change you want to see in the world", and have been working on "putting the energy out that you want to receive" which has some parallels with the former. I posted in the local LGBTQ Peoria facebook group what I was thinking about doing and if anyone else feels the need for it too, and I got a response back from another trans non-binary femme person in the area! I was floored that literally anyone else felt the same way I did. So we've been working together to flesh out this idea for a new community made for us, by us!
 
## The Social Platform
 
I decided on Discord because it's a modern social chat platform that focuses more on real-time communication and connection over something like facebook. Facebook was an obvious contender due to everyone and their dog being on it already, but as we've seen with the last election cycle and the current political landscape, I no longer trust facebook with anything as sensitive as queer communications. It's not like I trust Discord that much more, but they don't have a historical track record of being a part of the problem. There are other, much more secure and privacy conscious social platforms to use, but they end up being niche enough that non-technical people wouldn't care to join. I'm totally up for discussing the merits of other platforms, I just saw Discord as the quickest and easiest way to get this community going with the least amount of effort.
 
## The Technology
 
This is where things get exciting! At least for me anyways. The hope is that the community will work to flesh out this website with valuable resources and events, maybe even personal blog posts, to help support LGBTQIA+ people in our area.
 
"But Sage, I don't know how to code, and I'm not very good with computers". I design and build information systems for my day job, a large part of that is being able to design easy to use interfaces for non-technical people.
 
My hope is that with some good discussions between those in the community, we can identify some ways in which people feel comfortable contributing content to the website, whether it's a custom Discord /slash command or a google form; we have many avenues to explore that can equally accomplish the task.
 
The website itself is built on [Docusaurus](https://docusaurus.io/), which is designed to quickly build a documentation website. I chose the documentation website format because the intent of this site is for referencing information. It may not look like the prettiest site, but the intent is to quickly find what you're looking for, and hopefully look good while doing it.
 
Docusaurus outputs a static html site, which means all the pages are pre-generated and ready to be used, this means the site will be wicked fast to load, and the search happens locally on your device instead of the cloud, so it's also super fast. I also spent a lot of time and effort to make sure the site looks good on mobile, assuming that most access will be on a mobile device.
 
Now that we have the foundation of the website covered, the cool part is how it all ties together. The secret sauce here is in the Continuous Integration and Continuous Deployment (called CI/CD in the coding biz), where any changes made to the website's code will automatically trigger a new build and new deployment of the site. Coupled with a custom discord/google form integration, maybe some daily scraping of local event calendars and resources, the website starts to change and update on its own, triggered by code changes made by our custom integrations. The site will start to take on a life of its own. A proper technological golem if you will. I've always wanted to be a techno-mancer!

[Update 4/21/2023]
I've refactored the site to mkdocs-material since it's simpler to customize, auto generates the navigation, and has perfect local search by default. I'm currently working to integrate it with Decap CMS which should provide a clean and modern UI for anyone in the collective to update it. I still need to figure out the discord auth piece, but we're getting there!
 
## Conclusion
 
If you made it this far, thanks for sticking around! I'm really excited to get this community off the ground and see how it grows. I can't wait to connect with you all and to support you in your journey. If any of this resonates with you, then please join the Discord server by clicking the invite link on our `Welcome` page and join our grassroots collective!

## Author
Sage Peterson (She/They)
