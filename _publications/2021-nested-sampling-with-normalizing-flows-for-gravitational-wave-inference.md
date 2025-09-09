---
title: "Nested sampling with normalizing flows for gravitational-wave inference"
collection: publications
category: manuscripts
permalink: /publication/2102.11056/
date: 2021-01-01
excerpt: ''
venue: 'Phys. Rev. D'
arxivurl: 'https://arxiv.org/abs/2102.11056'
---
<p>We present a novel method for sampling iso-likelihood contours in nested sampling using a type of machine learning algorithm known as normalising flows and incorporate it into our sampler nessai. Nessai is designed for problems where computing the likelihood is computationally expensive and therefore the cost of training a normalising flow is offset by the overall reduction in the number of likelihood evaluations. We validate our sampler on 128 simulated gravitational wave signals from compact binary coalescence and show that it produces unbiased estimates of the system parameters. Subsequently, we compare our results to those obtained with dynesty and find good agreement between the computed log-evidences whilst requiring 2.07 times fewer likelihood evaluations. We also highlight how the likelihood evaluation can be parallelised in nessai without any modifications to the algorithm. Finally, we outline diagnostics included in nessai and how these can be used to tune the sampler's settings.</p>
