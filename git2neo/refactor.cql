create constraint on (u:User) assert u.email is unique;

// create users
begin
MATCH (c:Commit)
MERGE (a:Author:User {email:c.author_email}) ON CREATE SET a.name = c.author_name
CREATE (a)-[:AUTHORED]->(c);
commit

create index on :User(name);
create constraint on (y:Year) assert y.year is unique;

// create time tree
begin
MATCH (c:Commit)
MERGE (y:Year {year:substring(c.date,0,4)})
MERGE (m:Month {month:substring(c.date,5,2)})-[:IN_YEAR]->(y)
MERGE (d:Day {date:c.date, day:substring(c.date,8,2)})-[:IN_MONTH]->(m)
CREATE (c)-[:ON_DAY]->(d);
commit