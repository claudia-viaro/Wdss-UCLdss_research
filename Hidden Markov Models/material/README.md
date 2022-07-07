# Hidden Markov Models

A Markov chain is a model that tells us something about the probabilities of sequences of random variables, states, each of which can take on values from some set. These sets can be words, or tags, or symbols representing anything, like the weather. A Markov chain makes a very strong assumption that if we want to predict the future in the sequence, all that matters is the current state. The states before the current state have no impact on the future except via the current state. <br /> 

It’s as if to predict tomorrow’s weather you could examine today’s weather but you weren’t allowed to look at yesterday’s weather. In many cases, however, the events we are interested in are hidden: we don’t observe them directly. For example we don’t normally observe part-of-speech tags in a text. Rather, we see words, and must infer the tags from the word sequence. We call the tags hidden because they are not observed. A hidden Markov model (HMM) allows us to talk about both observed events Hidden Markov model (like words that we see in the input) and hidden events (like part-of-speech tags) that we think of as causal factors in our probabilistic model. 

## Literature 

Bible books:
- "Hidden markov models for time series : an introduction using R" by Walter Zucchini, Iain L. MacDonald, Roland Langrock <br />

Other books:
- "	Hidden Markov models in finance : further developments and applications. Volume II" by Rogemar S. Mamon, Robert J. Elliott

Non-books material:
- [Markov Models From The Bottom Up, with Python](https://ericmjl.github.io/essays-on-data-science/machine-learning/markov-models/)
- [Bayesian Methods for Hackers](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers): PyMC library, not sure if needed
- 

## Optional (and more advanced) readings


## How to access papers/textbooks
You can access papers by using your university credentials on the journal webpage. You can access textbook by searching the title in your university library online reporitory, if you cn't let me know and we'll find a way.

