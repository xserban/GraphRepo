# def delete_all():
#     # get total #of nodes
#     res = session.run("MATCH(n) RETURN COUNT(*) AS n")
#     total_nodes = 0
#     for item in res:
#         total_nodes = item["n"]
#     print("\n Existing nodes in db:", total_nodes)

#     # get total #of relationships
#     res1 = session.run("MATCH (n)-[r]->() RETURN COUNT(r) as r")
#     total_rels = 0
#     for item in res1:
#         total_rels = item["r"]
#     print("\n Existing relationships in db:", total_rels)

#     # delete all nodes in batches (for faster deletion)
#     while total_nodes > 0:
#         res = session.run(
#             "MATCH(n) WITH n LIMIT 10000 DETACH DELETE n RETURN COUNT(n) AS count")
#         count = 0
#         for item in res:
#             count = item["count"]  # updates deleeted node count here
#         total_nodes = total_nodes-count
#     print("\n #of nodes in db after deletion completed = ", total_nodes)


# start = time.time()
# delete_all()
# print("\n Pre cleanup time (sec): ", time.time()-start)

# for prot in fileList:
#     print("\n\n", prot)
#     if os.path.exists(prot+"_AllCCs_maxDist11.csv"):
#         print("\n Already Processed.")
#         continue
#     start = time.time()
#     delete_all()
#     pre_time = time.time()-start
#     print("\n Pre cleanup time (sec): ", pre_time)

#     # Database preparation
#     session.run("CREATE INDEX ON :MyNode(Name)")

#     # 1. Create graph
#     start = time.time()
#     session.run("USING PERIODIC COMMIT "
#                 "LOAD CSV FROM 'file:///'+{prot}+'_conflict_resolved.txt' AS line "
#                 "MERGE (n:MyNode {Name:line[0]}) "
#                 "MERGE (m:MyNode {Name:line[1]}) "
#                 "MERGE (n) -[:TO {dist:line[2]}] -> (m) ", prot=prot)

#     end = time.time()
#     step1_time = end - start
#     print("\n Step 1 time (in sec) = ", end-start)

#     # 2 find CCs
#     start = time.time()
#     result = session.run("CALL algo.unionFind.stream('MyNode', 'TO', {graph:'huge'}) "
#                          "YIELD nodeId,setId "
#                          "MATCH (n) "
#                          "WHERE id(n)=nodeId "
#                          "WITH setId,collect(nodeId) as nodes, collect(n.Name) as labels,count(*) as size_of_component "
#                          "ORDER BY size_of_component DESC "
#                          "RETURN setId as componentId,size_of_component,labels as connectedTSRkeys ")
#     end = time.time()
#     step2_time = end - start
#     print("\n Step 2 time (in sec) = ", end-start)
#    # 3. save result
#     start = time.time()
#     # newline='' <- to avoid blank line between two rows
#     with open(prot+"_AllCCs_maxDist11.csv", "w") as csvfile:
#         writer = csv.writer(csvfile, delimiter=',')
#         writer.writerow(
#             ['componentId', 'size_of_component', 'connectedTSRkeys'])
#         for record in result:
#             record = str(record)[:-1].replace(", ",
#                                               ",").replace("'", "").split()
#             print("\n", record[1], record[2], record[3])
#             writer.writerow([record[1].split("=")[1], record[2].split("=")[
#                             1], record[3].split("=")[1]])
#     end = time.time()
#     step3_time = end - start
#     print("\n Step 3 time (in sec) = ", end-start)

#     # 4. delete graph
#     start = time.time()
#     delete_all()
#     end = time.time()
#     post_time = end - start
#     print("\n Post cleanup time (in sec) = ", end-start)

#     print("\n Total time = ", pre_time+step1_time +
#           step2_time+step3_time+post_time)

# driver.close()
