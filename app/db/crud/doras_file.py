"""
UPDATING AND CLEANING SCRIPTS TO LOAD EXTERNAL DORA's FILE
"""

dora_properties_params = """
        category: $category
        , domain: $domain 
        , article_heading: article_heading
        , section_heading : $section_heading
        , chapter : $chapter 
        , section : $section
        , article : $article
        , paragraph : $paragraph
        , point: $point
        , sub_point : $sub_point
        , related_to: $related_to
        , responsible: $responsible
        , stipulation: $stipulation
        , full_text : $full_text
        """

initializing_database = """
        MATCH (n)
        DETACH DELETE n
        """
create_dora_record_file = """
        CREATE (n:Record_File)
        SET n += {{ {properties}, ctInsert: datetime() }} 
        RETURN n
        """

domain_cat_other = """
        // COLLECT VALUES FOR CENTRAL (CATALOG) NODES
        MATCH (n:Record_File)
        WITH COLLECT(DISTINCT n.category) as lcategory, COLLECT(DISTINCT n.domain) as ldomain
                , COLLECT (DISTINCT n.responsible) as lresp, COLLECT (DISTINCT n.stipulation) as lstip
        // CATEGORIES  vs Record_File
        UNWIND lcategory as category
        MERGE (so:Category {name:category})
        WITH ldomain, lresp, lstip
        MATCH (n:Record_File)
        MATCH (so:Category where so.name = n.category)
        MERGE (so)-[:CATEGORY]->(n)
        // domain  vs Record_File
        WITH DISTINCT ldomain, lresp, lstip
        UNWIND ldomain as domain
        MERGE (dm:Domain {name:domain})
        WITH lresp, lstip
        MATCH (n:Record_File)
        MATCH (dm:Domain) where dm.name = n.domain
        MERGE (dm)-[:DOMAIN]->(n)
        // responsible  vs Record_File
        WITH DISTINCT lresp, lstip
        UNWIND lresp as responsible
        MERGE (re:Responsible {name:responsible})
        WITH DISTINCT lstip
        MATCH (n:Record_File)
        MATCH (re:Responsible) where re.name = n.responsible
        MERGE (re)-[:RESPONSIBLE]->(n)
        // lstipulation  vs Record_File
        WITH DISTINCT lstip
        UNWIND lstip as stipulation
        MERGE (st:Stipulation {name:stipulation})
        WITH st 
        MATCH (n:Record_File)
        MATCH (st:Responsible) where st.name = n.stipulation
        MERGE (st)-[:STIPULATION]->(n)
        """

articles = """       
        MATCH (n:Record_File)
        WITH DISTINCT n.article as article, n.article_heading as article_heading
        MERGE (ar:Article {name:article_heading, ID: article})
        WITH ar
        MATCH (n:Record_File)
        MATCH (ar:Article) where ar.ID = n.article
        MERGE (ar)<-[:RECORD_FILE]-(n)
        WITH ar, n
        MATCH (dm:Domain)-[:DOMAIN]->(n)
        MERGE (dm)-[:DOMAIN]->(ar)        
        """

paragraph = """
        //article-paragraph
        MATCH (ar:Article)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(sp:Category)
        MERGE (p:Paragraph {art_ID:ar.ID, par_ID: toInteger(COALESCE(n.paragraph,'0'))})
        MERGE (p)<-[:RECORD_FILE]-(n)
        MERGE (p)<-[:PARAGRAPH]-(ar)
        """



point = """
        //paragraph-point
        MATCH (p:Paragraph)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(sp:Category)        
        MERGE (pt:Point {art_ID:p.art_ID, par_ID: p.par_ID, point: toString(COALESCE(n.point,''))})
        MERGE (pt)<-[:RECORD_FILE]-(n)
        MERGE (pt)<-[:POINT]-(p)
        """


sub_point = """
        //point-subpoint
        MATCH (p:Paragraph)-[:POINT]->(pt:Point)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(sp:Category)        
        MERGE (spt:Sub_Point {art_ID:p.art_ID, par_ID: toInteger(p.par_ID), point: pt.point, sub_point: COALESCE(toInteger(n.sub_point),'')})
        MERGE (spt)<-[:RECORD_FILE]-(n)
        MERGE (spt)<-[:SUB_POINT]-(pt)
        """

fulltext = """
        MATCH (spt:Sub_Point)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(so:Category)
        MERGE (ft:Full_Text {full_text:n.full_text})
        SET ft.related_to = n.related_to
        MERGE(spt)-[:FULL_TEXT]->(ft)
        MERGE(n)-[:RECORD_FILE]->(ft)
        MERGE(so)-[:CATEGORY]->(ft)
        WITH ft,n 
        MATCH (res:Responsible {name:n.responsible})
        MATCH (stip:Stipulation {name:n.stipulation})
        MERGE(ft)<-[:RESPONSIBLE]-(res)
        MERGE(ft)<-[:STIPULATION]-(stip)
        """

paragraph_fulltext = """
        MATCH (pt:Point)
        where pt.point = ''
        MATCH (pt)<-[:POINT]-(p:Paragraph)
        MATCH (pt)-[:SUB_POINT]->(:Sub_Point)-[]->(ft:Full_Text)
        MERGE (p)-[:FULL_TEXT]->(ft)
        RETURN pt
        """

point_fulltext = """
        MATCH (pt:Point)-[]-(spt:Sub_Point)
        where spt.sub_point = ''
        MATCH (pt)-[]->(spt)-[]->(ft:Full_Text)
        MERGE (pt)-[:FULL_TEXT]->(ft)
        """

record_file_delete = """
        MATCH (n:Record_File)
        DETACH DELETE n
        """

related_to_Article = """
        MATCH (ft:Full_Text) 
        where not ft.related_to is null
        WITH ft, size(ft.related_to) as eles
        UNWIND ft.related_to as relationt
        WITH ft, relationt, split(relationt,';') as relationto
        where  relationto[1] = ""  and relationto[2]= "" // and pointto = 'A'
        MATCH (ar:Article {ID: toInteger(relationto[0])})
        MERGE (ar)-[:RELATED_TO]->(ft)
        """

related_to_Paragraph = """
        MATCH (ft:Full_Text) 
        where not ft.related_to is null
        WITH ft, size(ft.related_to) as eles
        UNWIND ft.related_to as relationt
        WITH ft, relationt, split(relationt,';') as relationto
        where relationto[1] <> ""  and relationto[2] = "" // and pointto = 'P'
        MATCH (ar:Article {ID: toInteger(relationto[0])})-[:PARAGRAPH]->(p:Paragraph {par_ID:toInteger(relationto[1])})
        MERGE (p)-[:RELATED_TO]->(ft)
        """

related_to_Point = """
        MATCH (ft:Full_Text) 
        where not ft.related_to is null
        WITH ft, size(ft.related_to) as eles
        UNWIND ft.related_to as relationt
        WITH ft, relationt, split(relationt,';') as relationto
        where relationto[1] <> ""  and relationto[2] <> "" // and pointto = 'T'
        MATCH (ar:Article {ID: toInteger(relationto[0])})-[:PARAGRAPH]->(p:Paragraph {par_ID:toInteger(relationto[1])})-[:POINT]-(pt:Point {point:relationto[2]})
        MERGE (pt)-[:RELATED_TO]->(ft)
        """

false_par_fulltext = """
        MATCH (p:Paragraph)
        SET p.ID = p.par_ID, p.art_ID = null, p.par_ID = null
        WITH p
        MATCH (p)-[:POINT]->(pt:Point)
        SET pt.ID = pt.point, pt.par_ID = null, pt.art_ID = null, pt.point = null
        WITH pt
        MATCH (pt)-[:SUB_POINT]->(spt:Sub_Point)
        SET spt.ID = spt.sub_point, spt.art_ID = null, spt.par_ID = null, spt.point = null, spt.sub_point = null
        """

false_pt_fulltext = """
        MATCH (pt:Point)
        where pt.point = ""
        DETACH DELETE pt
        """

false_spt_fulltext = """
        MATCH (spt:Sub_Point)
        where spt.sub_point = ""
        MATCH (spt)-[r:FULL_TEXT]-(ft:Full_Text)
        delete r
        DETACH DELETE spt
        """


