all_nodes = """
        MATCH (d:Domain)-[]-(ar:Article)-[]-(p:Paragraph)-[]-(pt:Point)-[]-(ft:Full_Text)-[]-(cat:Category)
        optional match (p)-[r]-(ft2:Full_Text)
        optional match (pt)-[r2]-(spt:Sub_Point)-[]-(ft3:Full_Text)
        RETURN d, ar,p,pt,spt,ft,cat, r2, r, ft2, ft3 limit 1500
        """

search_by_article = """
        MATCH (ar:Article {ID:28})
        optional match (ar)-[]-(p:Paragraph)
        optional match (p)-[]-(pt:Point)
        optional match (pt)-[]-(spt:Sub_Point)
        optional match (spt)-[]-(ft:Full_Text)
        return ar, p,pt,spt, ft
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
        match (n)
        detach delete n
        """
create_dora_record_file = """
        create (n:Record_File)
        set n += {{ {properties}, ctInsert: datetime() }} 
        return n
        """



domain_cat_other = """
        // COLLECT VALUES FOR CENTRAL (CATALOG) NODES
        match (n:Record_File)
        with collect(distinct n.category) as lcategory, collect(distinct n.domain) as ldomain
                , collect (distinct n.responsible) as lresp, collect (distinct n.stipulation) as lstip
        // CATEGORIES  vs Record_File
        unwind lcategory as category
        merge (so:Category {name:category})
        with ldomain, lresp, lstip
        match (n:Record_File)
        match (so:Category where so.name = n.category)
        merge (so)-[:CATEGORY]->(n)
        // domain  vs Record_File
        with distinct ldomain, lresp, lstip
        unwind ldomain as domain
        merge (dm:Domain {name:domain})
        with lresp, lstip
        match (n:Record_File)
        match (dm:Domain) where dm.name = n.domain
        merge (dm)-[:DOMAIN]->(n)
        // responsible  vs Record_File
        with distinct lresp, lstip
        unwind lresp as responsible
        merge (re:Responsible {name:responsible})
        with distinct lstip
        match (n:Record_File)
        match (re:Responsible) where re.name = n.responsible
        merge (re)-[:RESPONSIBLE]->(n)
        // lstipulation  vs Record_File
        with distinct lstip
        unwind lstip as stipulation
        merge (st:Stipulation {name:stipulation})
        with st 
        match (n:Record_File)
        match (st:Responsible) where st.name = n.stipulation
        merge (st)-[:STIPULATION]->(n)
        """

articles = """       
        match (n:Record_File)
        with distinct n.article as article, n.article_heading as article_heading
        merge (ar:Article {name:article_heading, ID: article})
        with ar
        match (n:Record_File)
        match (ar:Article) where ar.ID = n.article
        merge (ar)<-[:RECORD_FILE]-(n)
        with ar, n
        match (dm:Domain)-[:DOMAIN]->(n)
        merge (dm)-[:DOMAIN]->(ar)        
        """

paragraph = """
        //article-paragraph
        match (ar:Article)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(sp:Category)
        merge (p:Paragraph {art_ID:ar.ID, par_ID: toInteger(coalesce(n.paragraph,'0'))})
        merge (p)<-[:RECORD_FILE]-(n)
        merge (p)<-[:PARAGRAPH]-(ar)
        """



point = """
        //paragraph-point
        match (p:Paragraph)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(sp:Category)        
        merge (pt:Point {art_ID:p.art_ID, par_ID: p.par_ID, point: toString(coalesce(n.point,''))})
        merge (pt)<-[:RECORD_FILE]-(n)
        merge (pt)<-[:POINT]-(p)
        """


sub_point = """
        //point-subpoint
        match (p:Paragraph)-[:POINT]->(pt:Point)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(sp:Category)        
        merge (spt:Sub_Point {art_ID:p.art_ID, par_ID: toInteger(p.par_ID), point: pt.point, sub_point: coalesce(toInteger(n.sub_point),'')})
        merge (spt)<-[:RECORD_FILE]-(n)
        merge (spt)<-[:SUB_POINT]-(pt)
        """

fulltext = """
        match (spt:Sub_Point)<-[:RECORD_FILE]-(n:Record_File)<-[:CATEGORY]-(so:Category)
        merge (ft:Full_Text {full_text:n.full_text})
        set ft.full_text = n.full_text
            , ft.related_to = n.related_to
            , ft.responsible = n.responsible
            , ft.stipulation = n.stipulation
        merge(spt)-[:FULL_TEXT]->(ft)
        merge(n)-[:RECORD_FILE]->(ft)
        merge(so)-[:CATEGORY]->(ft)
        with ft,n, so
        match (res:Responsible {name:ft.responsible})
        match (stip:Stipulation {name:ft.stipulation})
        merge(ft)<-[:RESPONSIBLE]-(res)
        merge(ft)<-[:STIPULATION]-(stip)
        """

paragraph_fulltext = """
        match (pt:Point)
        where pt.point = ''
        match (pt)<-[]-(p:Paragraph)
        match (pt)-[]->(:Sub_Point)-[]->(ft:Full_Text)
        merge (p)-[:FULL_TEXT]->(ft)
        return pt
        """

point_fulltext = """
        match (pt:Point)-[]-(spt:Sub_Point)
        where spt.sub_point = ''
        match (pt)-[]->(spt)-[]->(ft:Full_Text)
        merge (pt)-[:FULL_TEXT]->(ft)
        """

record_file_delete = """
        MATCH (n:Record_File)
        DETACH DELETE n
        """

related_to_Article = """
        MATCH (ft:Full_Text) 
        where not ft.related_to is null
        with ft, size(ft.related_to) as eles
        unwind ft.related_to as relationt
        with ft, relationt, split(relationt,';') as relationto
        where  relationto[1] = ""  and relationto[2]= "" // and pointto = 'A'
        match (ar:Article {ID: toInteger(relationto[0])})
        merge (ar)-[:RELATED_TO]->(ft)
        """

related_to_Paragraph = """
        MATCH (ft:Full_Text) 
        where not ft.related_to is null
        with ft, size(ft.related_to) as eles
        unwind ft.related_to as relationt
        with ft, relationt, split(relationt,';') as relationto
        where relationto[1] <> ""  and relationto[2] = "" // and pointto = 'P'
        match (ar:Article {ID: toInteger(relationto[0])})-[:PARAGRAPH]->(p:Paragraph {par_ID:toInteger(relationto[1])})
        merge (p)-[:RELATED_TO]->(ft)
        """

related_to_Point = """
        MATCH (ft:Full_Text) 
        where not ft.related_to is null
        with ft, size(ft.related_to) as eles
        unwind ft.related_to as relationt
        with ft, relationt, split(relationt,';') as relationto
        where relationto[1] <> ""  and relationto[2] <> "" // and pointto = 'T'
        match (ar:Article {ID: toInteger(relationto[0])})-[:PARAGRAPH]->(p:Paragraph {par_ID:toInteger(relationto[1])})-[:POINT]-(pt:Point {point:relationto[2]})
        merge (pt)-[:RELATED_TO]->(ft)
        """

false_par_fulltext = """
        match (p:Paragraph)
        set p.art_ID = null
        with p
        match (p)-[]->(pt:Point)
        set pt.par_ID = null, pt.art_ID = null
        with pt
        match (pt)-[]->(spt:Sub_Point)
        set spt.par_ID = null, spt.art_ID = null, spt.point = null
        """

false_pt_fulltext = """
        match (pt:Point)
        where pt.point = ""
        detach delete pt
        """

false_spt_fulltext = """
        match (spt:Sub_Point)
        where spt.sub_point = ""
        match (spt)-[r:FULL_TEXT]-(ft:Full_Text)
        delete r
        detach delete spt
        """

complete_extraction = """
        match (art:Article)
        call { with art
        match (art)-[:PARAGRAPH]->(p:Paragraph)-[rf:FULL_TEXT]->(ft:Full_Text) //-[:STIPULATION]-(st:Stipulation)
        return p.par_ID as par, '' as point, '' as subpoint,  ft.full_text as ft
        union all
        match (art)-[:PARAGRAPH]->(p:Paragraphp)-[:POINT]-(pt:Point)-[rf2:FULL_TEXT]->(ft:Full_Text)
        where pt.point <> ""
        return p.par_ID as par, pt.point as point, '' as subpoint,  ft.full_text as ft
        union all
        match (art)-[:PARAGRAPH]->(p:Paragraph)-[:POINT]-(pt:Point)-[:SUB_POINT]-(spt:Sub_Point)-[:FULL_TEXT]->(ft:Full_Text)
        where spt.sub_point <> ""
        return p.par_ID as par, pt.point as point, spt.sub_point as subpoint,  ft.full_text as ft
        }
        return art.ID as article, par, point, subpoint,  ft
        order by article, par, point, subpoint
        """

create_root =   """
                MERGE (N:NIST {ID:'NIST'})
                on create set N.ctInsert = datetime()
                on match set N.ctUpdate = datetime()
                set N.name = 'NIST'
                WITH N
                MERGE (NP:NIST_Publication {ID:'NIST 800-53 R5'})
                on create set NP.ctInsert = datetime()
                on match set NP.ctUpdate = datetime()
                set NP.name = 'NIST Special Publication 800-53 release 5'
                WITH N,NP
                MERGE (N)-[R:PUBLICATION]->(NP)
                on create set R.ctInsert = datetime()
                on match set R.ctUpdate = datetime()
                WITH NP
                MATCH (C:Category)
                MERGE (C)<-[RCP:CATEGORY_PUB]-(NP)
                on create set RCP.ctInsert = datetime()
                on match set RCP.ctUpdate = datetime()
                RETURN C,NP
                """

