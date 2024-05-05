all_nodes = """
        // getting the complete graph
        MATCH (d:Domain)-[]-(ar:Article)-[]-(p:Paragraph)-[]-(pt:Point)-[]-(ft:Full_Text)-[]-(cat:Category)
        OPTIONAL MATCH (p)-[r]-(ft2:Full_Text)
        OPTIONAL MATCH (pt)-[r2]-(spt:Sub_Point)-[]-(ft3:Full_Text)
        RETURN d, ar, p, pt, spt, ft, cat, r2, r, ft2, ft3 
        """

search_by_article = """
        // exploring specific article        
        MATCH (do)-[:DOMAIN]->(ar:Article {ID:28}) // changing the ID for the article ID you need to explore
        OPTIONAL MATCH (ar)-[:PARAGRAPH]->(p:Paragraph)        
        OPTIONAL MATCH (p)-[:POINT]->(pt:Point)
        OPTIONAL MATCH (pt)-[:SUB_POINT]->(spt:Sub_Point)
        OPTIONAL MATCH (p)-[:FULL_TEXT]->(ft:Full_Text)<-[:STIPULATION]-(s)
        OPTIONAL MATCH (pt)-[:FULL_TEXT]->(ftp:Full_Text)<-[:STIPULATION]-(sp)
        OPTIONAL MATCH (spt)-[:FULL_TEXT]->(fts:Full_Text)<-[:STIPULATION]-(sts)
        OPTIONAL MATCH (r)-[:RESPONSIBLE]->(ft)<-[:CATEGORY]-(c)
        OPTIONAL MATCH (rtp)-[:RESPONSIBLE]->(ftp)<-[:CATEGORY]-(ctp)
        OPTIONAL MATCH (rts)-[:RESPONSIBLE]->(fts)<-[:CATEGORY]-(cts)
        RETURN do, ar, p, pt, spt, ft, ftp, fts, s, sp, sts, c, ctp, cts, r, rtp, rts
        """

complete_article_extraction = """
        // getting a complete sequencial articles list
        MATCH (do)-[:DOMAIN]->(art:Article)        
        call { WITH art
        MATCH (art)-[:PARAGRAPH]->(p:Paragraph)-[rf:FULL_TEXT]->(ft:Full_Text) 
        RETURN p.ID as par, '' as point, '' as subpoint,  ft.full_text as ft
        union all
        WITH art
        MATCH (art)-[:PARAGRAPH]->(p:Paragraph)-[:POINT]->(pt:Point)-[rf2:FULL_TEXT]->(ft:Full_Text)
        RETURN p.ID as par, pt.ID as point, '' as subpoint,  ft.full_text as ft
        union all
        WITH art
        MATCH (art)-[:PARAGRAPH]->(p:Paragraph)-[:POINT]->(pt:Point)-[:SUB_POINT]->(spt:Sub_Point)-[:FULL_TEXT]->(ft:Full_Text)
        RETURN p.ID as par, pt.ID as point, spt.ID as subpoint,  ft.full_text as ft
        }
        RETURN do.chapter as chapter, art.ID as article, par as paragraph, point, subpoint,  ft
        order by article, paragraph, point, subpoint
        """
