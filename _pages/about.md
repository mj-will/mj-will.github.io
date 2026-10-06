---
permalink: /
title: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Hi, I'm Michael, a postdoctoral researcher at the [Max Planck Institute for Gravitational Physics (Albert Einstein Institute)][aei] in Potsdam.
My main research interest is the intersection between gravitational-wave astrophysics, machine learning and Bayesian statistics.
I'm also a member of the LIGO-Virgo-KAGRA Collaboration, where I hold the role of Parameter Estimation co-chair, and I recently
joined the LISA Consortium.

I first got involved in gravitational-wave research as an undergraduate intern working with
Chris Messenger in the [Institute for Gravitational Research][igr] at the University of Glasgow.
The project involved training a convolutional neural network to detect gravitational-wave
signals from binary black hole mergers.

I then did my PhD with John Veitch and Chris Messenger at the [Institute for Gravitational Research][igr]
and focused on developing techniques to accelerate Bayesian inference algorithms for
characterizing gravitational-wave signals.

Before moving to Potsdam, I was a Research Fellow at the [Institute of Cosmology & Gravitation][icg]
at the University of Portsmouth where I worked with Ian Harry.

## Recent highlights
<ul class="highlights-list">
  {% for item in site.data.highlights limit:5 %}
    <li>
      <span class="highlight-date">{{ item.date }}</span>
      <span class="highlight-text">
        {% if item.url %}
          {% if item.url contains '://' %}
            <a href="{{ item.url }}">{{ item.title }}</a>
          {% else %}
            <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
          {% endif %}
        {% else %}
          {{ item.title }}
        {% endif %}
      </span>
    </li>
  {% endfor %}
</ul>

[igr]: https://www.gla.ac.uk/schools/physics/research/groups/igr/members/
[icg]: https://www.port.ac.uk/research/institute-of-cosmology-and-gravitation
[aei]: https://www.aei.mpg.de/
