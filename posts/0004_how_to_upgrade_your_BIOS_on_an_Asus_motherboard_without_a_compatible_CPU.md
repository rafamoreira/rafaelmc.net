---
title: How to upgrade your BIOS on an Asus motherboard without a compatible CPU, or the sad state of search
date: 2024-10-09
tags:
  - hardware
  - asus
  - tech
  - google
  - seo
  - spam
  - AI
---

Here's how you do it, because apparently Asus can't be bothered to tell you:

1. Go to the Asus website and download the correct BIOS file for your motherboard, if you use windows, run the `renamer.exe` that comes with it, otherwise just look at the listing how it should be named (too difficult to provide a file with the correct name already, I guess)
2. Format a USB drive as FAT, and put this file on the root of the drive.
3. Put the USB drive on the BIOS designated port.
4. Turn off the pc, if still on.
5. Hold the BIOS flashback button for a few seconds.
6. The LED will start to blink.
7. After a few seconds the green LED will start to blink faster.
	1. if instead of blinking faster the LED goes back to solid or shut it off, there's a problem with your USB drive, it could be anything, bad format, bad BIOS file, wrong name, pay attention to every requirement.
8. After a few minutes (around 5 on my case) the flashing LED will stop and the BIOS should be flashed with the correct version.

## Why am I writing this?

A few weeks ago we got some new heavy-duty machines on work with the brand-new Ryzen 9950x and an Asus B650 motherboard, and although the B650 is compatible with Zen 5, a new BIOS is necessary to use the processor. These motherboards were manufactured in Dec, 23, so they are only compatible up to Ryzen 7000 series out of the box.

We had the privilege of choosing components for this machine, and we carefully selected motherboards that supported Zen 5 without needing a Ryzen 7000 on hand. The model in question? Asus TUF GAMING B650M-PLUS WIFI. It does indeed support this feature, but good luck figuring out how.

We're programmers, not IT wizards or system integrators. We were just fooling around building these PCs like regular consumers would. I've built countless systems in the past, but I've been out of the loop for a few years. I thought, "What could go wrong?" In the end, nothing did, but holy smokes, what a crappy journey.
## ASUS manuals are a waste of trees

First off, hats off to Asus for constantly changing feature names with subtle differences. It's like they're trying to confuse us on purpose. The feature in question is now called "BIOS FlashBack™ button," but it used to be "BIOS USB FlashBack," or something equally forgettable.

Another point for Asus for not including a single word about this feature in the manual. They only bothered to mention the regular process of updating the BIOS through the interface, which is super helpful when you don't have a compatible processor.

There are a few scattered pages around their website, mostly with old instructions, and not applicable for this MOBO, but the previous(?) process that I was familiar with my personal X470 CH7. 

## The sad state of search

Now for the most infuriating part. All I wanted was a simple written guide or manual on how this works. But no, that would be too easy. The current state of search engines is so depressingly bad that nothing actually useful came up in any of my queries. Just outdated results from the official website and a ton of SEO spam trying to make me click their affiliate links. I don't even doubt that one of those sites had the answers I needed, buried between 23 pages of AI-generated word salad.

After a lot of frustration I found a [video](https://www.youtube.com/watch?v=frQApIktgyM) describing the exact problem that I wanted to solve. And while I respect the creator, it's really frustrating to me to have to sit through a 12 minutes video about something that could be described in 194 words, which is the first part of this post.

Everything about this process annoys me to no end. Writing this post brought back all those feelings of frustration and disbelief. I'm even starting to question myself: am I being unrealistic to think that an expensive piece of hardware should come with a decent manual? Is it too much to ask for clear, accessible information about a critical feature? Apparently, for Asus, the answer is "yes." 