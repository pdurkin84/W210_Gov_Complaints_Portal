# Place to put ideas for discussion

### 29-Sept
- What tools will we use?  There is a week of async on choosing tools.  We need tools for:
	- Processes: codegiant, anything else?
	- Implementation:
		- Our model
		- Our data stores
		- Our interfaces
		- Supporting infrastructure
		- Do we want a public dns?
- The project name?  Alternatives for government could be municipal, urban, services?  Alternatives for compaints could be notification...Municipal Services notification system?
- What do we need to have prepare for our first presentation?
- What are the first tasks we need to get done to get the project rolling?
	- We probably need to do an EDA
	- How much more work required for our MVP?
	- What are the metrics we can define for our products?
	- What are our unknonwns and our assumptions?
	- Are there any ethical considerations?

### 27-Sept

- Should we create a separate web/REST servers for our model?  I have used the Stanford NLP server to do sentiment analysis, basically just install it as a webserver and interact with it over a REST API.  This would decouple our "complaint classification" from our UI and any other features or tools.  It abstracts the classification from our application and then could be something that is shipped separately.
- Should we provide multi-level classification?  e.g. a high level classification such as "Police" and something lower like "parking violation".  Two purposes, firstly we can redirect to various entities based on higher and/or lower level classification, and secondly we might find that some subclassifications may belong to two top level classifications and so knowing which one might be important.
- Should we talk to FixMyStreets about what we could do that they would use?
- Need to figure out how to remove duplicate tickets?  We haven't talked much about this, and it would mean that we need to compare to existing cases, but not those we have trained on.  So we will need to keep new cases separate from the ones we initially train on.
- The ability to accept mislabeled complaints and use them in the next round of training.  This may have a consequence that we would need to build separate models for each entity since one entities classification of a complaint might be different than another entity, and they would continually clash.  Some ability to provide custom training on top.
- Ability to recognize fake complaints - maybe just for a post-MIDS implementation as this could be huge amounts of work, however a "fake" class may be appropriate
- Put in an I am not a robot on the submission page
- Can we use mechanical turk to label?
- Instead of classifying to match some entity we spoke about providing our own classifications and allowing an entity to then choose where to route the complaint based on the classification.  If we have a separate server just returning the classification then our app that does this is separate from the app that does the classication.
- Use Cassandra for the database.  A relational DB like MySQL might be better as we can query based on non-keys, however Cassandra makes replication trivial, it's a lot more complicated with MySQL
