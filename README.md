## What is the goal? 

In line with the goal to find ways to produce scientific research at scale, 
this package offers a simple interface to collect papers from multiple sources, 
sort their relevance to a topic. 

Currently, papers are sourced from Semantic Scholar's paper api. 
The process to sort through them is heavily inspired by what I *think* Elicit.org also uses 
to sort papers according to a query. This is even described in their website. 
However, their code is not open-sourced, which leaves me to do this exercise by myself. 

The process is as follows: 
- Query from semantic scholar. 
- Then, openai's Babbage model does a text embedding of the abstract of the 
article. 
- The same model does a text embedding on the query. 
- The articles are then ranked by cosine similarity of the query vector, 
versus the embedding


### Installation 
Git clone this repository.
Then, just run the Dash server on your local host. 

### Motivation 


The goal is to create software that creates scientific blog posts at scale.
- We first have a paper collection later. This gets literature on a given topic, and searches for it. 
- In additional abstraction, there should also be multiple variants of queries that can give better results. 
- The semantic scholar api is used here, with a methodology that is similar to ought. 
- I also need to write some logic that takes out stop words. 
- I need a way to generate LaTeX equations for me. 

Once we get a paper, we structure the text into different sections. 
Standard writing is split into sections. The sections have a conclusion, and an introduction. 
The section should be a class, motivated by prompts. 


## How Is this more usable? 
This is more usable because 




### Outline an abstract structure for a science paper 
After this, there should be a referencing layer. 
The prompts for a conclusion are quite standard, and it is probably the easiest to systematise this section. 

### There should be a way to connect ideas in different papers. 
To create new ideas, we need to connect them in some way, and backtest them against some existing hypothesis. 
This is what makes an idea valuable. My first thought on connecting 
ideas between different papers was computing a similarity metric 

What other things make an idea valuable? We can consult epistomology here. 
There is a method to link together ideas from different papers here 
- https://arxiv.org/pdf/1708.04725.pdf

Also, we could build a graph. 

### Can we describe formulae with this?
We can use gpt-3 to write mathematical equations. 

### What is the next reasonable step 
Expose this to a python web page, for easy use. 

### What is the best way of displaying this information? 
Well, we could do a table popup when clicked - this would make things a bit easier. 