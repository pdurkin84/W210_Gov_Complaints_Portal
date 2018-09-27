# Place to put ideas for discussion

### 27-Sept

- Should we create a separate web/REST servers for our model?  I have used the Stanford NLP server to do sentiment analysis, basically just install it as a webserver and interact with it over a REST API.  This would decouple our "complaint classification" from our UI and any other features or tools.  It abstracts the classification from our application and then could be something that is shipped separately.
- Should we provide multi-level classification?  e.g. a high level classification such as "Police" and something lower like "parking violation".  Two purposes, firstly we can redirect to various entities based on higher and/or lower level classification, and secondly we might find that some subclassifications may belong to two top level classifications and so knowing which one might be important.
- Should we talk to FixMyStreets about what we could do that they would use?
- Need to figure out how to remove duplicate tickets?  We haven't talked much about this, and it would mean that we need to compare to existing cases, but not those we have trained on.  So we will need to keep new cases separate from the ones we initially train on.
- The ability to accept mislabeled complaints and use them in the next round of training.  This may have a consequence that we would need to build separate models for each entity since one entities classification of a complaint might be different than another entity, and they would continually clash.  Some ability to provide custom training on top.
- Ability to recognize fake complaints - maybe just for a post-MIDS implementation as this could be huge amounts of work, however a "fake" class may be appropriate
