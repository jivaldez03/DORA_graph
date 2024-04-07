
create_relatedcontrol_relationship = """
                        // adding relationship between ControlEnhancement (leaves)
                        MATCH (c:Category)-[rd:CATEGORY_DET]->(cd:Control)-[rdp:ENHANCEMENT_DET]->(cdp:ControlEnhancement)
                        UNWIND cdp.controls as relatedcontrol
                        WITH cdp, cdp.controls as controls, relatedcontrol, split(relatedcontrol,'-') as rcontrol
                        WITH cdp, controls, relatedcontrol, rcontrol[0] as sID, rcontrol[1] as sSUBID
                        MATCH (CDT:Control {ID: sID, SUBID: toInteger(sSUBID)})
                        MERGE (cdp)-[r:RELATED_CONTROL]->(CDT)
                        ON MATCH SET r.ctUpdate = datetime()
                        ON CREATE SET r.ctInsert = datetime()
                        RETURN cdp.ID as ID, cdp.SUBID as SUBID, relatedcontrol, sID, sSUBID
                        UNION ALL
                        // adding relationship between Control (roots)
                        MATCH (c:Category)-[rd:CATEGORY_DET]->(cd:Control)
                        UNWIND cd.controls as relatedcontrol
                        WITH cd, cd.controls as controls, relatedcontrol, split(relatedcontrol,'-') as rcontrol
                        WITH cd, controls, relatedcontrol, rcontrol[0] as sID, rcontrol[1] as sSUBID
                        MATCH (CDT:Control {ID: sID, SUBID: toInteger(sSUBID)})
                        MERGE (cd)-[r:RELATED_CONTROL]->(CDT)
                        ON MATCH SET r.ctUpdate = datetime()
                        ON CREATE SET r.ctInsert = datetime()
                        RETURN cd.ID as ID, cd.SUBID as SUBID, relatedcontrol, sID, sSUBID
                        """

